#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Spreadsheet truth follows each render's own page breaks: page block k holds exactly the rows printed on page k+1.
Needs pdftotext (poppler); `python3 -I -m unittest discover eval`."""
from __future__ import annotations

import copy
import json
import shutil
import sys
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
sys.path.insert(0, str(DATA.parent / "factory"))
from build import misplaced_rows, pages_of  # noqa: E402

SETS = {"libreoffice": ("manifest.json", "pdf", "truth"), "excel": ("manifest-excel.json", "pdf-excel", "truth-excel"),
        "word": ("manifest-word.json", "pdf-word", "truth-word")}


def workbooks(producer: str):
    man, pdfs, truths = SETS[producer]
    for m in json.loads((DATA / man).read_text(encoding="utf-8")):
        if m["format"] == "xlsx":
            truth = json.loads((DATA / truths / f"{m['id']}.truth.json").read_text(encoding="utf-8"))
            yield m["id"], truth["tables"], DATA / pdfs / f"{m['id']}.pdf"


@unittest.skipUnless(shutil.which("pdftotext") and shutil.which("pdfinfo"), "needs poppler")
class TruthPages(unittest.TestCase):
    def test_every_row_on_its_page(self):
        for producer in SETS:
            for fid, tables, pdf in workbooks(producer):
                with self.subTest(producer=producer, file=fid):
                    self.assertEqual(len(tables), pages_of(pdf), "one page block per printed page")
                    bad = [(k + 1, " | ".join(c for c in tables[k]["rows"][i] if c)[:60], p)
                           for k, i, p in misplaced_rows(tables, pdf)]
                    self.assertEqual(bad, [], "rows printed on another page than their block (block, row, pages)")

    def test_detects_a_row_on_the_wrong_page(self):
        fid, tables, pdf = next((f, t, p) for f, t, p in workbooks("excel") if f == "en-xlsx-bea458d951")
        moved = copy.deepcopy(tables)
        moved[1]["rows"].insert(0, moved[0]["rows"].pop())
        moved[1]["numeric"].insert(0, moved[0]["numeric"].pop())
        self.assertEqual([(k, i) for k, i, _ in misplaced_rows(moved, pdf)], [(1, 0)])


if __name__ == "__main__":
    unittest.main()
