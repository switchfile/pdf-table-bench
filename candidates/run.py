#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""PDF → Markdown per candidate, one process for all files (models and libraries loaded once), time per file
excluding load time. Usage (inside the candidates image): run.py <candidate> <sets-dir> <out-dir>"""
from __future__ import annotations

import json
import signal
import subprocess
import sys
import time
from pathlib import Path

FILE_SECONDS = 600


class Timeout(Exception):
    pass


def _alarm(*_):
    raise Timeout()


def markitdown():
    from markitdown import MarkItDown

    md = MarkItDown(enable_plugins=False)
    return lambda pdf: md.convert(str(pdf)).text_content


def docling():
    from docling.document_converter import DocumentConverter

    conv = DocumentConverter()
    return lambda pdf: conv.convert(str(pdf)).document.export_to_markdown()


def pymupdf4llm():
    import pymupdf4llm as p

    return lambda pdf: p.to_markdown(str(pdf))


def pdftotext():
    return lambda pdf: subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, text=True,
                                      check=True).stdout


def switchfile():
    """Public API (POST /v1/convert, target md, JSON response, then download of the result file); key from
    SWITCHFILE_API_KEY. The time includes upload, queueing and download."""
    import os
    import urllib.request
    import uuid

    key = os.environ["SWITCHFILE_API_KEY"]
    base = os.environ.get("SWITCHFILE_API", "https://api.switchfile.io")

    def call(req: urllib.request.Request, auth: bool = True) -> bytes:
        if auth:
            req.add_header("Authorization", f"Bearer {key}")
        # the default Python-urllib user agent is refused at the edge
        req.add_header("User-Agent", "pdf-table-bench/1")
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()

    def conv(pdf) -> str:
        body, ctype = _multipart({"to": "md"}, pdf)
        req = urllib.request.Request(f"{base}/v1/convert?wait=30", data=body, method="POST",
                                     headers={"Content-Type": ctype, "Idempotency-Key": uuid.uuid4().hex})
        c = json.loads(call(req))
        while c.get("status") in ("queued", "processing"):
            c = json.loads(call(urllib.request.Request(f"{base}/v1/conversions/{c['id']}?wait=30")))
        if c.get("status") != "finished":
            raise RuntimeError(f"conversion {c.get('status')}: {(c.get('error') or {}).get('code')}")
        # result URL is pre-signed; it needs no API key
        return call(urllib.request.Request(c["result"]["files"][0]["url"]), auth=False).decode("utf-8")

    return conv


def _multipart(fields: dict[str, str], pdf) -> tuple[bytes, str]:
    import uuid

    b = uuid.uuid4().hex
    parts = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields.items()]
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{pdf.name}"\r\n'
                 f'Content-Type: application/pdf\r\n\r\n'.encode() + pdf.read_bytes() + f"\r\n--{b}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={b}"


def cloudconvert():
    """CloudConvert public API v2: import/upload → convert (pdf → md, no options) → export/url; key from
    CLOUDCONVERT_API_KEY. Writes date, engine and credits per file (no job ids, no URLs) to <out>/<id>.meta.json;
    the full task responses go to CLOUDCONVERT_RAW_DIR if set (not published). Jobs are deleted after the download."""
    import datetime
    import io
    import os
    import urllib.request
    import zipfile

    key = os.environ["CLOUDCONVERT_API_KEY"]
    api = "https://api.cloudconvert.com/v2"
    raw = Path(os.environ["CLOUDCONVERT_RAW_DIR"]) if os.environ.get("CLOUDCONVERT_RAW_DIR") else None
    out = Path(sys.argv[3])

    def req(method: str, url: str, body: bytes | None = None, ctype: str = "application/json", auth: bool = True):
        r = urllib.request.Request(url, data=body, method=method, headers={"Content-Type": ctype} if body else {})
        if auth:
            r.add_header("Authorization", f"Bearer {key}")
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.read()

    def conv(pdf) -> str:
        tasks = {"up": {"operation": "import/upload"},
                 "conv": {"operation": "convert", "input": "up", "input_format": "pdf", "output_format": "md"},
                 "out": {"operation": "export/url", "input": "conv"}}
        job = json.loads(req("POST", f"{api}/jobs", json.dumps({"tasks": tasks}).encode()))["data"]
        try:
            form = next(t for t in job["tasks"] if t["name"] == "up")["result"]["form"]
            body, ctype = _multipart(form["parameters"], pdf)
            req("POST", form["url"], body, ctype, auth=False)
            job = json.loads(req("GET", f"https://sync.api.cloudconvert.com/v2/jobs/{job['id']}"))["data"]
            t = {x["name"]: x for x in job["tasks"]}
            c = t["conv"]
            if raw:
                raw.mkdir(parents=True, exist_ok=True)
                (raw / f"{pdf.stem}.json").write_text(json.dumps(job, indent=1), encoding="utf-8")
            (out / f"{pdf.stem}.meta.json").write_text(json.dumps({
                "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
                "status": c.get("status"), "engine": c.get("engine"), "engine_version": c.get("engine_version"),
                "credits": c.get("credits")}), encoding="utf-8")
            if job["status"] != "finished":
                raise RuntimeError(f"job {job['status']}: {c.get('code')} {str(c.get('message'))[:120]}")
            f = t["out"]["result"]["files"][0]
            data = req("GET", f["url"], auth=False)
            if f["filename"].lower().endswith(".zip"):
                # Markdown with images comes as an archive; only the Markdown is scored and kept
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    mds = [n for n in z.namelist() if n.lower().endswith(".md")]
                    return "\n\n".join(z.read(n).decode("utf-8") for n in mds)
            return data.decode("utf-8")
        finally:
            try:
                req("DELETE", f"{api}/jobs/{job['id']}")
            except Exception:  # noqa: BLE001 – CloudConvert deletes jobs after 24 h anyway
                pass

    return conv


def pdfplumber():
    """pdfplumber writes no Markdown: tables from the default table finder as pipe tables, remaining text as lines,
    both ordered top to bottom. The thinnest wrapper that shows the library fairly."""
    import pdfplumber as pp

    def cell(c) -> str:
        return " ".join((c or "").split()).replace("|", "\\|")

    def conv(pdf) -> str:
        out = []
        with pp.open(str(pdf)) as doc:
            for page in doc.pages:
                tables = page.find_tables()
                boxes = [t.bbox for t in tables]

                def outside(obj, boxes=boxes):
                    cx, cy = (obj["x0"] + obj["x1"]) / 2, (obj["top"] + obj["bottom"]) / 2
                    return not any(x0 <= cx <= x1 and t0 <= cy <= t1 for x0, t0, x1, t1 in boxes)

                items = [(ln["top"], ln["text"]) for ln in page.filter(outside).extract_text_lines()]
                for t in tables:
                    rows = [r for r in t.extract() if any(c for c in r)]
                    if not rows:
                        continue
                    w = max(len(r) for r in rows)
                    lines = ["| " + " | ".join(cell(c) for c in r + [None] * (w - len(r))) + " |" for r in rows]
                    lines.insert(1, "|" + "---|" * w)
                    items.append((t.bbox[1], "\n" + "\n".join(lines) + "\n"))
                out.extend(text for _, text in sorted(items, key=lambda x: x[0]))
                out.append("")
        return "\n".join(out)

    return conv


def main() -> None:
    name, sets, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    convert = globals()[name]()
    load = time.perf_counter() - t0
    signal.signal(signal.SIGALRM, _alarm)
    pdfs = sorted(sets.glob("*.pdf"))
    for pdf in pdfs:
        fid = pdf.stem
        signal.alarm(FILE_SECONDS)
        t = time.perf_counter()
        try:
            md = convert(pdf)
            ok = True
        except Timeout:
            md, ok = "", False
            print("time limit", fid, flush=True)
        except Exception as e:  # noqa: BLE001 – a failure scores 0, the run continues
            md, ok = "", False
            print("error", fid, type(e).__name__, str(e)[:200], flush=True)
        finally:
            signal.alarm(0)
        secs = time.perf_counter() - t
        if ok:
            (out / f"{fid}.md").write_text(md, encoding="utf-8")
        (out / f"{fid}.time.json").write_text(json.dumps({"seconds": round(secs, 3)}), encoding="utf-8")
    (out / "_run.json").write_text(json.dumps({"candidate": name, "load_seconds": round(load, 2), "files": len(pdfs)}),
                                   encoding="utf-8")
    print(name, len(pdfs), "files, load", round(load, 1), "s, total", round(time.perf_counter() - t0, 1), "s")


if __name__ == "__main__":
    main()
