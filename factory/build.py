#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Step 3 (in the factory image, offline): original → PDF with LibreOffice, truth from the original.
Usage: build.py <fetched.json> <originals-dir> <dest-dir> [jobs]   or   build.py one <id> <lang> <fmt> <file> <dest>"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
from mdparse import loose_tokens as tokens  # noqa: E402  (the data set was selected with it)

MAX_PAGES = 20          # max pages per PDF
MAX_SHEETS = 4          # max sheets per workbook
MAX_SHEET_CELLS = 40000  # larger sheets are not read for the truth (would not fit 20 pages anyway)
MIN_CELLS = 12          # sheets with fewer filled cells are not a table
MIN_COVERAGE = 0.97     # share of truth words found in the PDF text layer (otherwise the truth is wrong)
# Reverse direction: share of PDF words found in the truth. Below it the PDF prints content the truth lacks
# (sheets that could not be hidden, chart text, text frames); in the first run all others were at 0.89 or above
MIN_LAYER_IN_TRUTH = 0.85
MIN_PAGE_COVERAGE = 0.9  # per page block of a table: share of its words on exactly that printed page
# and no row of a page block may be printed on another page (see misplaced_rows)
# Follow-up draws (not draws 1 and 2): a sheet that would exceed the page limit is cropped to its first pages
# (print area; very wide sheets keep two column pages). Open-data tables are often long lists and would otherwise
# all be dropped at the page limit.
CROP_PAGES = int(os.environ.get("BENCH_CROP_PAGES", "0"))
FILE_SECONDS = 300
LOCALE = {"de": "de-DE", "en": "en-GB", "fr": "fr-FR"}
PROFILE = """<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema">
<item oor:path="/org.openoffice.Setup/L10N"><prop oor:name="ooSetupSystemLocale" oor:op="fuse"><value>%s</value></prop></item>
</oor:items>
"""
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"


def pdftotext(pdf: Path, page: int | None = None, layout: bool = False) -> str:
    only = ["-f", str(page), "-l", str(page)] if page else []
    return subprocess.run(["pdftotext", "-enc", "UTF-8", *(["-layout"] if layout else []), *only, str(pdf), "-"],
                          capture_output=True, text=True).stdout


def misplaced_rows(tables: list[dict], pdf: Path) -> list[tuple[int, int, list[int]]]:
    """Rows of page block k that the PDF prints on another page instead of page k+1: (block, row, pages). A row is on a
    page if its words occur in order on one printed line; rows with fewer than two filled cells, or found on no page
    (wrapped cells), prove nothing."""
    lines = [[f" {' '.join(tokens(x))} " for x in pdftotext(pdf, k + 1, layout=True).split("\n") if x.strip()]
             for k in range(len(tables))]
    out = []
    for k, t in enumerate(tables):
        for i, row in enumerate(t["rows"]):
            cells = [c for c in row if c]
            if len(cells) < 2:
                continue
            seq = f" {' '.join(tokens(' '.join(cells)))} "
            if any(seq in x for x in lines[k]):
                continue
            other = [q + 1 for q, page in enumerate(lines) if q != k and any(seq in x for x in page)]
            if other:
                out.append((k, i, other))
    return out


def pages_of(pdf: Path) -> int:
    m = re.search(r"^Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout, re.M)
    return int(m.group(1)) if m else 0


def strip_info(pdf: Path) -> None:
    """Reduce the document info to producer and date and drop XMP metadata: author and title fields would otherwise carry
    names from the originals. Page content stays unchanged."""
    p = subprocess.run(["qpdf", "--json=2", "--json-key=qpdf", str(pdf)], capture_output=True, text=True)
    if p.returncode not in (0, 3):  # 3: success with warnings (e.g. PDFs from macOS)
        raise RuntimeError("qpdf: " + p.stderr[:200])
    j = json.loads(p.stdout)
    objs = j["qpdf"][1]
    trailer = objs["trailer"]["value"]
    upd = {}
    if trailer.get("/Info"):
        info = objs[f"obj:{trailer['/Info']}"]["value"]
        upd[f"obj:{trailer['/Info']}"] = {"value": {k: v for k, v in info.items() if k in ("/Producer", "/Creator", "/CreationDate")}}
    root = objs[f"obj:{trailer['/Root']}"]["value"]
    if "/Metadata" in root:
        upd[f"obj:{trailer['/Root']}"] = {"value": {k: v for k, v in root.items() if k != "/Metadata"}}
    if not upd:
        return
    f = pdf.with_suffix(".info.json")
    f.write_text(json.dumps({"qpdf": [{"jsonversion": 2}, upd]}), encoding="utf-8")
    q = subprocess.run(["qpdf", str(pdf), f"--update-from-json={f}", "--replace-input"], capture_output=True)
    f.unlink()
    if q.returncode not in (0, 3):
        raise RuntimeError("qpdf: " + q.stderr.decode()[:200])


def coverage(truth_text: str, layer: str) -> float:
    t, l = Counter(tokens(truth_text)), Counter(tokens(layer))
    return sum((t & l).values()) / sum(t.values()) if t else 0.0


class Office:
    """One LibreOffice process per file with its own profile (locale of the language, so numbers without a fixed
    locale in their format appear in the PDF as a user of that language would see them)."""

    def __init__(self, tmp: Path, lang: str) -> None:
        import uno

        (tmp / "prof" / "user").mkdir(parents=True)
        (tmp / "prof" / "user" / "registrymodifications.xcu").write_text(PROFILE % LOCALE[lang], encoding="utf-8")
        self.pipe = f"ob{os.getpid()}"
        self.proc = subprocess.Popen(["soffice", f"-env:UserInstallation=file://{tmp}/prof", "--headless", "--invisible",
                                      "--norestore", "--nologo", "--nodefault", f"--accept=pipe,name={self.pipe};urp;"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        for _ in range(120):
            try:
                ctx = resolver.resolve(f"uno:pipe,name={self.pipe};urp;StarOffice.ComponentContext")
                break
            except Exception:  # noqa: BLE001 – process still starting
                time.sleep(0.5)
        else:
            raise RuntimeError("LibreOffice does not start")
        self.desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

    @staticmethod
    def prop(name: str, value):
        from com.sun.star.beans import PropertyValue

        p = PropertyValue()
        p.Name, p.Value = name, value
        return p

    def open(self, path: Path):
        import uno

        return self.desktop.loadComponentFromURL(uno.systemPathToFileUrl(str(path)), "_blank", 0,
                                                 (self.prop("Hidden", True), self.prop("ReadOnly", True)))

    def pdf(self, doc, dest: Path, filt: str, pages: int) -> Path:
        import uno

        fd = uno.Any("[]com.sun.star.beans.PropertyValue", (self.prop("PageRange", f"1-{pages}"),))
        args = (self.prop("FilterName", filt), self.prop("FilterData", fd))
        uno.invoke(doc, "storeToURL", (uno.systemPathToFileUrl(str(dest)), uno.Any("[]com.sun.star.beans.PropertyValue", args)))
        return dest

    def close(self) -> None:
        try:
            self.desktop.terminate()
        except Exception:  # noqa: BLE001 – process already gone
            pass
        try:
            self.proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def trim(rows: list[list[str]], num: list[list[bool]]) -> dict | None:
    """Drop empty outer rows and columns (the print area often starts before the table)."""
    keep_r = [i for i, r in enumerate(rows) if any(r)]
    if not keep_r:
        return None
    keep_c = [j for j in range(len(rows[0])) if any(rows[i][j] for i in keep_r)]
    span = range(keep_r[0], keep_r[-1] + 1)
    return {"rows": [[rows[i][j] for j in keep_c] for i in span],
            "numeric": [[num[i][j] and bool(rows[i][j]) for j in keep_c] for i in span]}


def blocks(lo: int, hi: int, breaks) -> list[tuple[int, int]]:
    cuts = sorted({lo, *(b.Position for b in breaks if lo < b.Position <= hi)})
    return [(c, (cuts[k + 1] if k + 1 < len(cuts) else hi + 1)) for k, c in enumerate(cuts)]


def used_area(sh):
    cur = sh.createCursor()
    cur.gotoStartOfUsedArea(False)
    cur.gotoEndOfUsedArea(True)
    return cur.getRangeAddress()


def col_name(c: int) -> str:
    s = ""
    c += 1
    while c:
        c, r = divmod(c - 1, 26)
        s = chr(65 + r) + s
    return s


def crop(sh) -> str | None:
    """Print area of at most CROP_PAGES pages (whole page blocks from the top left); returns the range in A1 notation.
    Only valid after the sheet has been printed (before that it has no page breaks)."""
    a = used_area(sh)
    rb = blocks(a.StartRow, a.EndRow, sh.getRowPageBreaks())
    cb = blocks(a.StartColumn, a.EndColumn, sh.getColumnPageBreaks())
    if len(cb) > CROP_PAGES // 2:
        cb = cb[:2]
        a.EndColumn = cb[-1][1] - 1
    a.EndRow = rb[min(len(rb), CROP_PAGES // len(cb)) - 1][1] - 1
    sh.setPrintAreas((a,))
    return f"{col_name(a.StartColumn)}{a.StartRow + 1}:{col_name(a.EndColumn)}{a.EndRow + 1}"


def sheet_grid(doc, sh) -> dict | None:
    """All visible cells of the print area as one grid (displayed text, cell type), plus title rows and columns as
    grid indices and the print order; basis for page blocks following another producer's print (adopt)."""
    areas = list(sh.getPrintAreas()) or [used_area(sh)]
    if len(areas) != 1:
        return None
    a = areas[0]
    if (a.EndRow - a.StartRow + 1) * (a.EndColumn - a.StartColumn + 1) > MAX_SHEET_CELLS:
        return None
    rows = [r for r in range(a.StartRow, a.EndRow + 1) if sh.Rows.getByIndex(r).IsVisible]
    cols = [c for c in range(a.StartColumn, a.EndColumn + 1) if sh.Columns.getByIndex(c).IsVisible]
    tr = sh.TitleRows if sh.PrintTitleRows else None
    tc = sh.TitleColumns if sh.PrintTitleColumns else None
    grid_s, grid_n = [], []
    for r in rows:
        rs, rn = [], []
        for c in cols:
            x = sh.getCellByPosition(c, r)
            kind = x.Type.value
            rs.append(x.getString().strip() if kind != "EMPTY" else "")
            rn.append(kind == "VALUE" or (kind == "FORMULA" and x.FormulaResultType2 == 1))
        grid_s.append(rs)
        grid_n.append(rn)
    style = doc.StyleFamilies.getByName("PageStyles").getByName(sh.PageStyle)
    return {"rows": grid_s, "numeric": grid_n, "down_first": bool(style.PrintDownFirst),
            "title_rows": [k for k, r in enumerate(rows) if tr is not None and tr.StartRow <= r <= tr.EndRow],
            "title_cols": [k for k, c in enumerate(cols) if tc is not None and tc.StartColumn <= c <= tc.EndColumn]}


def grids(manifest: Path, raw: Path, dest: Path) -> None:
    """Grids of the printed sheets of each XLSX file in the manifest (cropped as in the build)."""
    import uno

    dest.mkdir(parents=True, exist_ok=True)
    for m in json.loads(manifest.read_text(encoding="utf-8")):
        if m["format"] != "xlsx":
            continue
        with tempfile.TemporaryDirectory() as t:
            off = Office(Path(t), m["lang"])
            try:
                doc = off.open(raw / f"{m['id']}.xlsx")
                out = []
                for name in m["sheets"]:
                    sh = doc.Sheets.getByName(name)
                    if name in m.get("crop", {}):
                        a = uno.createUnoStruct("com.sun.star.table.CellRangeAddress")
                        a.Sheet = sh.RangeAddress.Sheet
                        a.StartColumn, a.StartRow, a.EndColumn, a.EndRow = a1_range(m["crop"][name])
                        sh.setPrintAreas((a,))
                    out.append(sheet_grid(doc, sh))
                doc.close(True)
            finally:
                off.close()
        (dest / f"{m['id']}.grid.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
        print(m["id"], "grid", [None if g is None else (len(g["rows"]), len(g["rows"][0]) if g["rows"] else 0) for g in out],
              flush=True)


def a1_range(s: str) -> tuple[int, int, int, int]:
    def one(x: str) -> tuple[int, int]:
        letters, digits = re.fullmatch(r"([A-Z]+)(\d+)", x).groups()
        c = 0
        for ch in letters:
            c = c * 26 + ord(ch) - 64
        return c - 1, int(digits) - 1
    (c0, r0), (c1, r1) = map(one, s.split(":"))
    return c0, r0, c1, r1


def sheet_pages(doc, sh) -> list[dict] | None:
    """Visible cells of a sheet as displayed text (as the spreadsheet prints it) and cell type, one table per printed
    page in print order: a wide sheet prints its columns across several pages, and a converter then sees several
    tables. Page breaks are only valid after the sheet has been printed."""
    areas = list(sh.getPrintAreas()) or [used_area(sh)]
    style = doc.StyleFamilies.getByName("PageStyles").getByName(sh.PageStyle)
    down_first = style.PrintDownFirst
    trows = sh.TitleRows if sh.PrintTitleRows else None
    tcols = sh.TitleColumns if sh.PrintTitleColumns else None
    vis_r: dict[int, bool] = {}
    vis_c: dict[int, bool] = {}
    cache: dict[tuple[int, int], tuple[str, bool]] = {}

    def cell(c: int, r: int) -> tuple[str, bool]:
        if (c, r) not in cache:
            x = sh.getCellByPosition(c, r)
            kind = x.Type.value
            cache[c, r] = (x.getString().strip() if kind != "EMPTY" else "",
                           kind == "VALUE" or (kind == "FORMULA" and x.FormulaResultType2 == 1))
        return cache[c, r]

    def rows_in(lo: int, hi: int) -> list[int]:
        for r in range(lo, hi):
            if r not in vis_r:
                vis_r[r] = sh.Rows.getByIndex(r).IsVisible
        return [r for r in range(lo, hi) if vis_r[r]]

    def cols_in(lo: int, hi: int) -> list[int]:
        for c in range(lo, hi):
            if c not in vis_c:
                vis_c[c] = sh.Columns.getByIndex(c).IsVisible
        return [c for c in range(lo, hi) if vis_c[c]]

    pages = []
    for a in areas:
        if (a.EndRow - a.StartRow + 1) * (a.EndColumn - a.StartColumn + 1) > MAX_SHEET_CELLS:
            return None
        rb = blocks(a.StartRow, a.EndRow, sh.getRowPageBreaks())
        cb = blocks(a.StartColumn, a.EndColumn, sh.getColumnPageBreaks())
        order = [(r, c) for c in cb for r in rb] if down_first else [(r, c) for r in rb for c in cb]
        for (r0, r1), (c0, c1) in order:
            rows = rows_in(r0, r1)
            cols = cols_in(c0, c1)
            # repeated title rows and columns appear on every page that does not already start with them
            if trows is not None and r0 > trows.EndRow:
                rows = rows_in(trows.StartRow, trows.EndRow + 1) + rows
            if tcols is not None and c0 > tcols.EndColumn:
                cols = cols_in(tcols.StartColumn, tcols.EndColumn + 1) + cols
            if not rows or not cols:
                continue
            grid = [[cell(c, r) for c in cols] for r in rows]
            t = trim([[x[0] for x in row] for row in grid], [[x[1] for x in row] for row in grid])
            if t is not None:
                pages.append(t)
    return pages


def xlsx(off: Office, src: Path, tmp: Path, dest: Path, fid: str) -> dict:
    doc = off.open(src)
    if doc is None:
        return {"reason": "unreadable"}
    try:
        sheets = doc.Sheets
        visible = [i for i in range(sheets.Count) if sheets.getByIndex(i).IsVisible]
        # Pass 1: print each sheet alone (the others hidden), pages and text layer per sheet
        chosen, total, why, crops = [], 0, Counter(), {}
        for i in visible:
            if len(chosen) == MAX_SHEETS:
                break
            sh = sheets.getByIndex(i)
            for j in visible:
                sheets.getByIndex(j).IsVisible = j == i
            one = off.pdf(doc, tmp / f"s{i}.pdf", "calc_pdf_Export", MAX_PAGES + 1)
            n = pages_of(one)
            area = None
            if CROP_PAGES and total + n > MAX_PAGES and not list(sh.getPrintAreas()):
                area = crop(sh)
                if area:
                    one = off.pdf(doc, tmp / f"s{i}.pdf", "calc_pdf_Export", MAX_PAGES + 1)
                    n = pages_of(one)
            for j in visible:
                sheets.getByIndex(j).IsVisible = True
            if n == 0 or total + n > MAX_PAGES:
                why["page limit"] += 1
                continue
            pages = sheet_pages(doc, sh)
            if not pages or sum(1 for t in pages for r in t["rows"] for c in r if c) < MIN_CELLS:
                why["sheet too small or too large"] += 1
                continue
            # check: as many non-empty page blocks as printed pages, otherwise the mapping is unproven
            if len(pages) != n:
                why["page blocks do not match the print"] += 1
                continue
            if any(coverage("\n".join(" | ".join(r) for r in t["rows"]), pdftotext(one, k + 1)) < MIN_PAGE_COVERAGE
                   for k, t in enumerate(pages)) or misplaced_rows(pages, one):
                why["page block not on its own page"] += 1
                continue
            text = "\n".join(" | ".join(r) for t in pages for r in t["rows"])
            cov = coverage(text, pdftotext(one))
            if cov < MIN_COVERAGE:
                why[f"coverage below {MIN_COVERAGE}"] += 1
                continue
            chosen.append((i, sh.Name, pages, cov, n))
            if area:
                crops[sh.Name] = area
            total += n
        if not chosen:
            return {"reason": ", ".join(sorted(why)) or "no visible sheet"}
        keep = {i for i, *_ in chosen}
        for j in visible:
            sheets.getByIndex(j).IsVisible = j in keep
        pdf = off.pdf(doc, dest / f"{fid}.pdf", "calc_pdf_Export", MAX_PAGES + 1)
    finally:
        doc.close(True)
    tables = [t for _, _, pages, _, _ in chosen for t in pages]
    text = "\n\n".join("\n".join(" | ".join(c for c in r if c) for r in t["rows"]) for t in tables)
    return {"pdf": pdf, "text": text, "tables": tables, "sheets": [n for _, n, *_ in chosen],
            "coverage": round(min(c for *_, c, _ in chosen), 4), **({"crop": crops} if crops else {})}


# --- DOCX: truth straight from word/document.xml (body text and tables in document order) ---

def run_text(el, out: list[str], boxes: list) -> None:
    """Text of a paragraph part; deleted text, field codes and hidden text do not count. Text boxes become separate
    paragraphs after the paragraph; for alternate content only the first choice (the fallback duplicates the text)."""
    for ch in el:
        tag = ch.tag
        if tag == f"{MC}AlternateContent":
            choice = ch.find(f"{MC}Choice")
            if choice is not None:
                run_text(choice, out, boxes)
            continue
        if tag in (f"{W}del", f"{W}instrText", f"{W}delText", f"{W}rPr", f"{W}pPr"):
            continue
        if tag == f"{W}r":
            rpr = ch.find(f"{W}rPr")
            if rpr is not None and rpr.find(f"{W}vanish") is not None:
                continue
        if tag == f"{W}t":
            out.append(ch.text or "")
        elif tag in (f"{W}tab", f"{W}ptab"):
            out.append("\t")
        elif tag in (f"{W}br", f"{W}cr"):
            out.append("\n")
        elif tag == f"{W}noBreakHyphen":
            out.append("-")
        elif tag == f"{W}txbxContent":
            boxes.append(ch)
        else:
            run_text(ch, out, boxes)


def block(el, paras: list[str], tables: list[dict]) -> None:
    for ch in el:
        if ch.tag == f"{W}p":
            out: list[str] = []
            boxes: list = []
            run_text(ch, out, boxes)
            paras.append("".join(out))
            for b in boxes:
                block(b, paras, tables)
        elif ch.tag == f"{W}tbl":
            grid = table(ch)
            tables.append({"rows": grid, "numeric": None})
            paras.extend(" | ".join(c for c in r if c) for r in grid)
        elif ch.tag in (f"{W}sdt", f"{W}sdtContent", f"{W}customXml", f"{W}ins", f"{W}smartTag"):
            block(ch, paras, tables)


def cell_text(tc) -> str:
    paras: list[str] = []
    block(tc, paras, [])  # nested tables become text of the outer cell
    return re.sub(r"\s+", " ", " ".join(paras)).strip()


def table(tbl) -> list[list[str]]:
    """Grid with gridSpan and vMerge: value in the first cell of a merge, the others empty."""
    rows = []
    for tr in tbl.findall(f"{W}tr"):
        row: list[str] = []
        trpr = tr.find(f"{W}trPr")
        before = trpr.find(f"{W}gridBefore") if trpr is not None else None
        if before is not None:
            row.extend([""] * int(before.get(f"{W}val", "0")))
        for tc in [x for x in tr if x.tag == f"{W}tc"] + [x for s in tr if s.tag == f"{W}sdt"
                                                         for c in s if c.tag == f"{W}sdtContent" for x in c if x.tag == f"{W}tc"]:
            pr = tc.find(f"{W}tcPr")
            span = int(pr.find(f"{W}gridSpan").get(f"{W}val", "1")) if pr is not None and pr.find(f"{W}gridSpan") is not None else 1
            vm = pr.find(f"{W}vMerge") if pr is not None else None
            cont = vm is not None and vm.get(f"{W}val", "continue") == "continue"
            row.append("" if cont else cell_text(tc))
            row.extend([""] * (span - 1))
        rows.append(row)
    width = max((len(r) for r in rows), default=0)
    return [r + [""] * (width - len(r)) for r in rows]


def docx(off: Office, src: Path, tmp: Path, dest: Path, fid: str) -> dict:
    with zipfile.ZipFile(src) as z:
        xml = z.read("word/document.xml")
    if b"<w:del " in xml or b"<w:ins " in xml or b"<w:moveFrom" in xml:
        return {"reason": "tracked changes (print shows deleted text)"}
    body = ET.fromstring(xml).find(f"{W}body")
    paras: list[str] = []
    tables: list[dict] = []
    block(body, paras, tables)
    text = "\n".join(p for p in paras if p.strip())
    if len(tokens(text)) < 50:
        return {"reason": "too little text"}
    doc = off.open(src)
    if doc is None:
        return {"reason": "unreadable"}
    try:
        pdf = off.pdf(doc, tmp / "all.pdf", "writer_pdf_Export", MAX_PAGES + 1)
    finally:
        doc.close(True)
    if pages_of(pdf) > MAX_PAGES or pages_of(pdf) == 0:
        return {"reason": "page limit"}
    cov = coverage(text, pdftotext(pdf))
    if cov < MIN_COVERAGE:
        return {"reason": f"coverage below {MIN_COVERAGE}"}
    out = dest / f"{fid}.pdf"
    shutil.copyfile(pdf, out)
    tables = [t for t in tables if len(t["rows"]) >= 2 and any(c for r in t["rows"] for c in r)]
    return {"pdf": out, "text": text, "tables": tables, "coverage": round(cov, 4)}


def one(fid: str, lang: str, fmt: str, src: Path, dest: Path) -> dict:
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        off = Office(tmp, lang)
        try:
            r = (xlsx if fmt == "xlsx" else docx)(off, src, tmp, dest, fid)
        finally:
            off.close()
    if "pdf" not in r:
        return r
    pdf = r.pop("pdf")
    strip_info(pdf)
    layer = pdftotext(pdf)
    if coverage(layer, r["text"]) < MIN_LAYER_IN_TRUTH:
        pdf.unlink()
        return {"reason": f"PDF text not in the truth (below {MIN_LAYER_IN_TRUTH})"}
    truth = {"text": r["text"], "tables": r["tables"], "layer": layer}
    (dest / f"{fid}.truth.json").write_text(json.dumps(truth, ensure_ascii=False), encoding="utf-8")
    cells = sum(1 for t in r["tables"] for row in t["rows"] for c in row if c)
    return {"pages": pages_of(pdf), "tables": len(r["tables"]), "cells": cells, "coverage": r["coverage"],
            **{k: r[k] for k in ("sheets", "crop") if k in r}}


def resplit(grids: list, pdf: Path, n: int) -> list[dict] | None:
    """Page blocks following the producer's print: page by page, find the columns (first page of a column block) and
    rows whose cells are on the page. Each word on the page backs only one cell (otherwise zeros and repeated names
    would match on every page); only non-empty cells count; a single missing row does not end the block.
    None if the pages do not add up."""
    pages = [Counter(tokens(pdftotext(pdf, k + 1))) for k in range(n)]

    def share(g, cells, pool):
        """Share of cells whose words are still in the page's pool; those words are consumed."""
        cells = [(i, j) for i, j in cells if g["rows"][i][j]]
        if not cells:
            return None
        hit = 0
        for i, j in cells:
            need = Counter(tokens(g["rows"][i][j]))
            if all(pool[k] >= v for k, v in need.items()):
                pool.subtract(need)
                hit += 1
        return hit / len(cells)

    out, p = [], 0
    for g in grids:
        if g is None or not g["rows"]:
            return None
        nr, nc, tr, tc = len(g["rows"]), len(g["rows"][0]), set(g["title_rows"]), set(g["title_cols"])
        body = [i for i in range(nr) if i not in tr]

        def col_end(page, rs, cs):
            ev = [i for i in body if i >= rs][:40]
            ce, s = cs, Counter(page)
            for j in range(cs, nc):
                f = share(g, [(i, j) for i in ev], s)
                if f is not None and f < 0.6:
                    break
                ce = j + 1
            return ce

        def row_end(page, rs, cs, ce):
            re_, i, s = rs, rs, Counter(page)
            while i < nr:
                f = share(g, [(i, j) for j in range(cs, ce)], s)
                if f is not None and f < 0.5:
                    nxt = share(g, [(i + 1, j) for j in range(cs, ce)], Counter(s)) if i + 1 < nr else None
                    if nxt is None or nxt < 0.6:
                        break
                i += 1
                re_ = i
            return re_

        def block(rs, re_, cs, ce):
            rows = ([i for i in sorted(tr) if rs > max(tr)] if tr else []) + list(range(rs, re_))
            cols = ([j for j in sorted(tc) if cs > max(tc)] if tc else []) + list(range(cs, ce))
            return trim([[g["rows"][i][j] for j in cols] for i in rows], [[g["numeric"][i][j] for j in cols] for i in rows])

        def has(rs, re_, cs, ce):
            return any(g["rows"][i][j] for i in range(rs, re_) for j in range(cs, ce))

        if g["down_first"]:
            cs = 0
            while has(0, nr, cs, nc):
                if p >= n:
                    return None
                ce = col_end(pages[p], 0, cs)
                if ce == cs:
                    return None
                rs = 0
                while has(rs, nr, cs, ce):
                    if p >= n:
                        return None
                    re_ = row_end(pages[p], rs, cs, ce)
                    t = block(rs, re_, cs, ce) if re_ > rs else None
                    if t is None:
                        return None
                    out.append(t)
                    p, rs = p + 1, re_
                cs = ce
        else:
            rs, cuts = 0, []
            while has(rs, nr, 0, nc):
                cs, k, re_ = 0, 0, None
                while has(rs, nr, cs, nc):
                    if p >= n:
                        return None
                    if k >= len(cuts):
                        cuts.append(col_end(pages[p], rs, cs))
                    ce = cuts[k]
                    if ce == cs:
                        return None
                    if re_ is None:
                        re_ = row_end(pages[p], rs, cs, ce)
                    t = block(rs, re_, cs, ce) if re_ > rs else None
                    if t is None:
                        return None
                    out.append(t)
                    p, cs, k = p + 1, ce, k + 1
                rs = re_
    return out if p == n else None


def rounded_display(truth: dict, layer: str) -> int:
    """Excel shows numbers in General format with only as many digits as the column fits (4,565122265 instead of
    4,56512226512227). If a number cell is not in the text layer but a rounding of exactly that value is, the rounded
    display applies for this PDF. The value still comes from the original; returns the number of adjusted cells."""
    have, n = set(tokens(layer)), 0
    for tb in truth["tables"]:
        for row, nums in zip(tb["rows"], tb["numeric"]):
            for k, (s, num) in enumerate(zip(row, nums)):
                m = re.fullmatch(r"(-?\d+)([.,])(\d+)", s)
                if not num or not m or tokens(s)[0] in have:
                    continue
                v = float(f"{m.group(1)}.{m.group(3)}")
                for d in range(len(m.group(3)) - 1, -1, -1):
                    r = f"{v:.{d}f}".rstrip("0").rstrip(".") if d else f"{v:.0f}"
                    r = r.replace(".", m.group(2))
                    if tokens(r) and tokens(r)[0] in have:
                        row[k], n = r, n + 1
                        break
    if n:
        truth["text"] = "\n\n".join("\n".join(" | ".join(c for c in r if c) for r in tb["rows"]) for tb in truth["tables"])
    return n


def adopt(manifest: Path, pdfs: Path, truths: Path, dest: Path, grid_dir: Path | None = None) -> None:
    """Adopt PDFs from another producer (e.g. Word for Mac, factory/office_mac.py): same truth from the original,
    same checks as above, only the text layer is new."""
    dest.mkdir(parents=True, exist_ok=True)
    res = []
    for m in json.loads(manifest.read_text(encoding="utf-8")):
        src = pdfs / f"{m['id']}.pdf"
        if not src.exists():
            res.append({"id": m["id"], "reason": "no PDF from the producer"})
            continue
        truth = json.loads((truths / f"{m['id']}.truth.json").read_text(encoding="utf-8"))
        out = dest / f"{m['id']}.pdf"
        shutil.copyfile(src, out)
        strip_info(out)
        n, layer = pages_of(out), pdftotext(out)
        shown = rounded_display(truth, layer) if m["format"] == "xlsx" else 0
        # XLSX: the truth is split per printed page; if the producer breaks pages differently, even by one row, it no
        # longer fits. Then derive page blocks from the original's grid following its print, with the same per-page check.
        def paged_bad(tables):
            return m["format"] == "xlsx" and (len(tables) != n or any(
                coverage("\n".join(" | ".join(r) for r in t["rows"]), pdftotext(out, k + 1)) < MIN_PAGE_COVERAGE
                for k, t in enumerate(tables)) or bool(misplaced_rows(tables, out)))
        paged, split = paged_bad(truth["tables"]), False
        gf = grid_dir / f"{m['id']}.grid.json" if grid_dir else None
        if paged and gf and gf.exists():
            g = json.loads(gf.read_text(encoding="utf-8"))
            rounded_display({"tables": [x for x in g if x]}, layer)
            tables = resplit(g, out, n)
            if tables and not paged_bad(tables):
                truth["tables"], paged, split = tables, False, True
                truth["text"] = "\n\n".join("\n".join(" | ".join(c for c in r if c) for r in tb["rows"]) for tb in tables)
        why = ("page limit" if not 0 < n <= MAX_PAGES else
               "page blocks do not match the producer's print" if paged else
               f"coverage below {MIN_COVERAGE}" if coverage(truth["text"], layer) < MIN_COVERAGE else
               f"PDF text not in the truth (below {MIN_LAYER_IN_TRUTH})" if coverage(layer, truth["text"]) < MIN_LAYER_IN_TRUTH
               else None)
        if why:
            out.unlink()
            res.append({"id": m["id"], "reason": why, "pages": n, **({"rounded": shown} if shown else {})})
            continue
        (dest / f"{m['id']}.truth.json").write_text(json.dumps({**truth, "layer": layer}, ensure_ascii=False), encoding="utf-8")
        res.append({"id": m["id"], "pages": n, "pages_other": m["pages"], "coverage": round(coverage(truth["text"], layer), 4),
                    **({"rounded": shown} if shown else {}), **({"resplit": True} if split else {})})
    (dest / "build.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    ok = [r for r in res if "reason" not in r]
    print(len(ok), "of", len(res), "adopted;", sum(r["pages"] for r in ok), "pages;",
          sum(r["pages"] != r["pages_other"] for r in ok), "with a different page count")


def main() -> None:
    if sys.argv[1] == "adopt":  # adopt <manifest> <pdf-dir> <truth-dir> <dest> [grid-dir]
        adopt(*map(Path, sys.argv[2:7]))
        return
    if sys.argv[1] == "grids":  # grids <manifest> <originals-dir> <dest>
        grids(*map(Path, sys.argv[2:5]))
        return
    if sys.argv[1] == "strip":  # strip metadata from already built PDFs
        for f in sys.argv[2:]:
            strip_info(Path(f))
        return
    if sys.argv[1] == "one":
        fid, lang, fmt, src, dest = sys.argv[2:7]
        try:
            res = one(fid, lang, fmt, Path(src), Path(dest))
        except Exception as e:  # noqa: BLE001 – broken file: dropped with a reason
            res = {"reason": f"error {type(e).__name__}: {str(e)[:120]}"}
        print(json.dumps(res, ensure_ascii=False))
        return
    fetched = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    raw, dest = Path(sys.argv[2]), Path(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)

    def run(c: dict) -> dict:
        try:
            p = subprocess.run([sys.executable, "-I", __file__, "one", c["id"], c["lang"], c["format"],
                                str(raw / f"{c['id']}.{c['format']}"), str(dest)],
                               capture_output=True, text=True, timeout=FILE_SECONDS)
            r = json.loads(p.stdout.strip().splitlines()[-1])
        except subprocess.TimeoutExpired:
            r = {"reason": "time limit"}
        except (ValueError, IndexError):
            r = {"reason": "aborted"}
        print(c["id"], json.dumps(r, ensure_ascii=False), flush=True)
        return {"id": c["id"], **r}

    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(run, fetched))
    (dest / "build.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    ok = [r for r in res if "pages" in r]
    print(len(ok), "of", len(res), "originals built,", sum(r["pages"] for r in ok), "pages")


if __name__ == "__main__":
    main()
