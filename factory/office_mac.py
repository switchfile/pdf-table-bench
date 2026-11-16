#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Additional PDF producers: DOCX → PDF with Word for Mac, XLSX → PDF with Excel for Mac, one file at a time, on
the Mac itself. Standard library only, Python 3.9; Excel with German UI.
Usage: office_mac.py [--app word|excel] [--locale fr_FR] <in> <out>"""
import argparse
import json
import os
import pty
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

# per app: process name, sandbox id, input extension, export and close (AppleScript)
APPS = {
    "word": ("Microsoft Word", "com.microsoft.Word", "docx",
             'save as document "{name}" file name "{dst}" file format format PDF', "close every document saving no",
             "count of documents"),
    # Excel is driven via the menus (System Events): the measurement machine lacks automation permission for Excel, and
    # "Save As" lets us explicitly choose local PDF output (Excel suggests the Microsoft online service).
    "excel": ("Microsoft Excel", "com.microsoft.Excel", "xlsx", "", "", ""),
}
WORD = APP_ID = EXT = EXPORT = CLOSE = COUNT = ""
SANDBOX = Path()
# Shared lock for all scripts that drive Word (or Excel) on this Mac; other runs take it too.
LOCK = Path(os.environ.get("WORD_MAC_LOCK", "/tmp/sfbench-word.lock"))
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
# Local export sends only telemetry, independent of file size (Word 1–35 KB per file; Excel 58 KB just for opening
# and closing without export). More than this base plus half the file size suggests an upload: retry once, abort
# the second time.
NET_BASES = {"docx": 20_000, "xlsx": 80_000}

DIALOGS = r'''
tell application "System Events"
	if not (exists process "{app}") then return ""
	tell process "{app}"
		set out to ""
		repeat with w in windows
			set sr to ""
			try
				set sr to subrole of w
			end try
			if sr is not "AXStandardWindow" then
				try
					set out to out & (value of every static text of w as text) & linefeed
				end try
			else
				try
					if (count of sheets of w) > 0 then set out to out & (value of every static text of sheet 1 of w as text) & "(sheet)" & linefeed
				end try
			end if
		end repeat
		return out
	end tell
end tell
'''


def osa(script: str, timeout: float):
    """(rc, stdout, stderr); rc 124 on timeout."""
    try:
        p = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def tell(body: str, timeout: float):
    return osa(f'with timeout of {int(timeout)} seconds\ntell application "{WORD}"\n{body}\nend tell\nend timeout', timeout + 10)


def dialog_text() -> str:
    """Text of open dialogs without file names (the message goes to the terminal, even for sets that only show totals)."""
    return re.sub(r"[\w.-]+\.(?:pdf|docx|xlsx)", "<file>", osa(DIALOGS.replace("{app}", WORD), 20)[1]).strip()[:300]


def doc_count() -> int:
    rc, out, _ = tell(COUNT, 20)
    return int(out) if rc == 0 and out.isdigit() else -1


def word_pid():
    out = subprocess.run(["pgrep", "-x", WORD], capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else None


NETTOPS = []  # started nettop processes: always killed on exit


def stop_nettops():
    for proc in NETTOPS:
        if proc.poll() is None:
            proc.kill()
            proc.wait(5)


class NetMeter(threading.Thread):
    """Bytes sent by Word, via nettop in delta mode (one block per second; the first block is the total since
    process start and does not count)."""

    def __init__(self, pid):
        super().__init__(daemon=True)
        self.pid, self.sent, self.ok, self.proc = pid, 0, False, None

    def run(self):
        # On a pipe nettop buffers several blocks; through a pseudo-terminal one block arrives per second.
        master, slave = pty.openpty()
        try:
            self.proc = subprocess.Popen(["nettop", "-P", "-d", "-x", "-L", "0", "-s", "1", "-J", "bytes_in,bytes_out"],
                                         stdout=slave, stderr=subprocess.DEVNULL)
            NETTOPS.append(self.proc)
        except OSError:
            os.close(master)
            return
        finally:
            os.close(slave)
        blocks = 0
        try:
            for line in os.fdopen(master, "r", errors="replace"):
                cells = line.strip().split(",")
                if cells and cells[0] == "":
                    blocks += 1
                    self.ok = blocks >= 2
                elif blocks >= 2 and cells[0].endswith(f".{self.pid}") and len(cells) >= 3 and cells[2].isdigit():
                    self.sent += int(cells[2])
        except OSError:
            pass

    def stop(self):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.join(5)


# Excel: window to front, "Save As…", PDF, entire workbook, "Best for printing" (local); German UI labels.
# The dialog saves to "Documents"; returns 0 only when all settings read back correctly.
XL_SAVE = r"""
tell application "System Events" to tell process "Microsoft Excel"
	set frontmost to true
	set w to first window whose name is "{stem}"
	perform action "AXRaise" of w
	delay 0.5
	click menu item "Speichern unter..." of menu 1 of menu bar item "Datei" of menu bar 1
	repeat 50 times
		if (count of sheets of w) > 0 then exit repeat
		delay 0.2
	end repeat
	set g to splitter group 1 of sheet 1 of w
	click pop up button 2 of g
	delay 0.7
	keystroke "PDF"
	key code 36
	delay 1.5
	set g to splitter group 1 of sheet 1 of w
	if (value of pop up button 2 of g) does not start with "PDF" then error "Format: " & (value of pop up button 2 of g)
	click radio button "Arbeitsmappe" of g
	click radio button "Optimal geeignet zum Drucken" of g
	delay 0.3
	if value of radio button "Optimal geeignet zum Drucken" of g is not 1 then error "local PDF export not selected"
	if value of radio button "Arbeitsmappe" of g is not 1 then error "entire workbook not selected"
	if value of pop up button "Ort:" of g is not "Dokumente" then error "location: " & (value of pop up button "Ort:" of g)
	set value of text field "Sichern unter:" of g to "{name}"
	delay 0.3
	click button "Sichern" of g
end tell
"""
# Close without saving; after opening foreign workbooks Excel often asks whether to save changes.
XL_CLOSE = r"""
tell application "System Events" to tell process "Microsoft Excel"
	repeat with w in (every window whose subrole is "AXStandardWindow")
		set frontmost to true
		perform action "AXRaise" of w
		delay 0.3
		click menu item "Schließen" of menu 1 of menu bar item "Datei" of menu bar 1
		delay 1
		try
			if (count of sheets of w) > 0 then click (first button of sheet 1 of w whose name contains "Nicht speichern")
		end try
		delay 0.5
	end repeat
	return count of (every window whose subrole is "AXStandardWindow")
end tell
"""
XL_WINDOWS = r"""
tell application "System Events" to tell process "Microsoft Excel" to return name of every window
"""


def xl_export(src: Path, dst: Path, timeout: float):
    """(rc, error) for Excel; dst is in ~/Documents (the dialog's location) and must not exist beforehand."""
    subprocess.run(["open", "-g", "-a", WORD, str(src)], check=False)
    t_end = time.time() + timeout
    while src.stem not in osa(XL_WINDOWS, 20)[1].split(", "):
        if time.time() > t_end:
            return 124, "workbook does not open"
        if dialog_text():
            return 1, "dialog while opening"
        time.sleep(0.5)
    time.sleep(1)
    rc, _, err = osa(XL_SAVE.replace("{stem}", src.stem).replace("{name}", dst.stem), 60)
    if rc != 0:
        return rc, err
    last = -1
    while time.time() < t_end:
        if dst.exists() and dst.stat().st_size == last and last > 0:
            return 0, ""
        last = dst.stat().st_size if dst.exists() else -1
        if dialog_text():
            return 1, "dialog while saving"
        time.sleep(1)
    return 124, "no PDF"


def render_one(docx: Path, out_dir: Path, work: Path, timeout: float) -> dict:
    fid = docx.stem
    src, dst = work / docx.name, work / f"{fid}.pdf"
    if EXT == "xlsx":
        dst = Path.home() / "Documents" / f"sfbench-{fid}.pdf"
        if dst.exists():
            sys.exit(f"ERROR: {dst} already exists; not overwriting a foreign file")
    shutil.copyfile(docx, src)
    net = NetMeter(word_pid())
    net.start()
    time.sleep(1.5)
    t0 = time.time()
    if EXT == "xlsx":
        rc, err = xl_export(src, dst, timeout)
    else:
        # open returns before the document is in the list
        rc, _, err = tell(f'''open (POSIX file "{src}")
repeat 300 times
	if ({COUNT}) > 0 then exit repeat
	delay 0.2
end repeat
{EXPORT.format(name=src.name, dst=dst)}''', timeout)
    rec = {"id": fid, "rc": rc, "s": round(time.time() - t0, 2), "bytes": docx.stat().st_size}
    if rc != 0:
        rec["error"] = err[:200]
        rec["dialogs"] = dialog_text()
    if EXT == "xlsx":
        osa(XL_CLOSE, 60)
    else:
        tell(CLOSE, 60)
    time.sleep(1.5)
    net.stop()
    if net.ok:
        rec["net_out"] = net.sent
    rec["ok"] = rc == 0 and dst.exists() and dst.stat().st_size > 0
    if rec["ok"]:
        shutil.move(str(dst), str(out_dir / f"{fid}.pdf"))
    elif dst.exists():
        dst.unlink()
    for f in work.iterdir():
        f.unlink()
    return rec


def xl_start(locale: str) -> None:
    """Excel with the locale of the document language, for this process only (no system setting)."""
    pid = word_pid()
    if pid:
        cmd = subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True, text=True).stdout
        if not locale or f"-AppleLocale {locale}" in cmd:
            return
        if osa(XL_WINDOWS, 20)[1].strip():
            sys.exit("ERROR: Excel is running with another locale and has windows open; please close them")
        osa('tell application "System Events" to tell process "Microsoft Excel" to click menu item "Excel beenden" of '
            'menu 1 of menu bar item "Excel" of menu bar 1', 30)
        for _ in range(60):
            if word_pid() is None:
                break
            time.sleep(1)
        else:
            sys.exit("ERROR: Excel does not quit")
    subprocess.run(["open", "-g", "-a", WORD] + (["--args", "-AppleLocale", locale] if locale else []), check=False)
    for _ in range(60):
        if word_pid():
            break
        time.sleep(1)
    time.sleep(8)
    names = [n for n in osa(XL_WINDOWS, 20)[1].split(", ") if n]
    # start windows (German UI labels): template gallery and empty "Mappe1"
    if "Neue und zuletzt verwendete Dateien öffnen" in names:
        osa('tell application "System Events" to tell process "Microsoft Excel" to click button "Abbrechen" of '
            'window "Neue und zuletzt verwendete Dateien öffnen"', 20)
    if all(re.fullmatch(r"Mappe\d+|Neue und zuletzt verwendete Dateien öffnen", n) for n in names):
        osa(XL_CLOSE, 60)


def doc_windows() -> int:
    if EXT != "xlsx":
        return doc_count()
    rc, out, _ = osa(XL_WINDOWS, 20)
    return len([n for n in out.split(", ") if n]) if rc == 0 else -1


def acquire_lock():
    try:
        LOCK.mkdir()
    except FileExistsError:
        try:
            other = int((LOCK / "pid").read_text())
            os.kill(other, 0)
            sys.exit(f"ERROR: {WORD} is busy (lock {LOCK}, process {other})")
        except (ValueError, OSError):
            shutil.rmtree(LOCK, ignore_errors=True)
            LOCK.mkdir()
    (LOCK / "pid").write_text(str(os.getpid()))


def main(argv=None):
    global WORD, APP_ID, EXT, EXPORT, CLOSE, COUNT, SANDBOX
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", choices=sorted(APPS), default="word")
    ap.add_argument("in_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--timeout", type=float, default=180)
    ap.add_argument("--locale", default="", help="Excel only: locale for numbers and dates, e.g. fr_FR")
    a = ap.parse_args(argv)
    WORD, APP_ID, EXT, EXPORT, CLOSE, COUNT = APPS[a.app]
    # Office for Mac is sandboxed: input and output only under this folder
    SANDBOX = Path(os.environ.get("WORD_MAC_SANDBOX", str(Path.home() / f"Library/Containers/{APP_ID}/Data/Documents")))
    if not Path(f"/Applications/{WORD}.app").exists():
        sys.exit(f"ERROR: {WORD} is not installed")
    files = sorted(a.in_dir.glob(f"*.{EXT}"))
    bad = [p.name for p in files if not ID_RE.match(p.stem)]
    if bad:
        sys.exit(f"ERROR: invalid file names {bad[:3]}")
    a.out_dir.mkdir(parents=True, exist_ok=True)
    acquire_lock()
    work = SANDBOX / f"sfbench-wordpdf-{os.getpid()}"
    summary = {"files": 0, "ok": 0, "failed": [], "net_out": 0}
    # also on external termination: stop nettop, remove lock and work folder (finally)
    signal.signal(signal.SIGTERM, lambda *_: sys.exit("ERROR: aborted"))
    try:
        if EXT == "xlsx":
            xl_start(a.locale)
        elif word_pid() is None:
            subprocess.run(["open", "-g", "-a", WORD], check=False)
            time.sleep(8)
        # the driver closes all documents after each file; other open documents would be lost
        if doc_windows() != 0:
            sys.exit(f"ERROR: {WORD} has documents open or does not respond; please close them")
        # an open dialog blocks every open; requests then pile up in Word
        if dialog_text():
            sys.exit(f"ERROR: {WORD} shows a dialog; please close it: {dialog_text()}")
        work.mkdir(parents=True, exist_ok=True)
        for docx in files:
            rec = render_one(docx, a.out_dir, work, a.timeout)
            summary["net_out"] += rec.get("net_out", 0)
            if rec.get("net_out", 0) > NET_BASES[EXT] + rec["bytes"] // 2:
                # On first opening some files Word sends up to a few MB to Microsoft (content unknown), on the second
                # opening of the same file only telemetry. Online conversion, by contrast, uploads on every export:
                # retry once, only then abort. net_out_first keeps the first value.
                time.sleep(10)
                first = rec["net_out"]
                rec = render_one(docx, a.out_dir, work, a.timeout)
                rec["net_out_first"] = first
            print(json.dumps(rec, ensure_ascii=False), flush=True)
            summary["files"] += 1
            summary["ok"] += rec["ok"]
            summary["net_out"] += rec.get("net_out", 0) if "net_out_first" in rec else 0
            if not rec["ok"]:
                summary["failed"].append(rec["id"])
                if dialog_text():
                    sys.exit(f"ERROR: {WORD} shows a dialog after file {summary['files']}; run stopped: {dialog_text()}")
            if "net_out" not in rec:
                sys.exit("ERROR: nettop returns no values; no run without network measurement")
            if rec["net_out"] > NET_BASES[EXT] + rec["bytes"] // 2:
                sys.exit(f"ERROR: {WORD} sent more than telemetry twice for file {summary['files']} ({rec['net_out_first']} and "
                         f"{rec['net_out']} bytes): export is not local")
    finally:
        stop_nettops()
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(LOCK, ignore_errors=True)
    # counters only: the line goes to the terminal, even for sets that show no file names
    print(json.dumps({"summary": summary | {"failed": len(summary["failed"])}}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
