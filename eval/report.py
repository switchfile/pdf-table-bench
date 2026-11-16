#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Result tables (Markdown) from scores.json. Usage: report.py <scores.json> [group,group,…]"""
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
groups = sys.argv[2].split(",") if len(sys.argv) > 2 else list(data["summary"])
# pdftotext writes no tables, so it is shown as a baseline and left out of the paired comparison
BASELINE = "pdftotext"
LABEL = {"docling": "Docling", "pdfplumber": "pdfplumber + our wrapper", "pdftotext": "pdftotext (baseline)"}


def pct(v, ci=None) -> str:
    if v is None:
        return "–"
    s = f"{v * 100:.1f}"
    return f"{s} [{ci[0] * 100:.1f}–{ci[1] * 100:.1f}]" if ci else s


for g in groups:
    rows = data["summary"][g]
    any_k = next(iter(rows.values()))
    print(f"\n**{g}**: {any_k['files']} files, {any_k['pages']} pages\n")
    print("| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | "
          "Reading order | s/page (median) | Failed |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    # ordered by the mean per file: the cell sum depends on a few large workbooks
    order = sorted(rows, key=lambda k: -(rows[k]["cells_file"][0] or 0) if rows[k]["cells"] else 0)
    for k in order:
        s = rows[k]
        cells = f"{pct(s['cells_rate'], s['cells_rate_ci'][1:])} ({s['cells_hit']}/{s['cells']})" if s["cells"] else "–"
        sp = "–" if s["sec_per_page"] is None else f"{s['sec_per_page']:.2f} ({s['sec_per_page_median']:.2f})"
        cf = pct(s["cells_file"][0], s["cells_file"][1:]) if s["cells"] else "–"
        print(f"| {LABEL.get(k, k)} | {cf} | {cells} | {s['nums_false']} ({s['nums_false_files']}) | {pct(s['words'][0], s['words'][1:])} | "
              f"{pct(s['order'][0], s['order'][1:])} | {sp} | {s['failed']} |")

first = next(iter(data["summary"]["all"]))
for g, pairs in data.get("paired", {}).items():
    print(f"\nPaired per file against {first}, numbers in right cell, {g} (files with numeric cells):\n")
    print("| Candidate | Difference, points [95 % CI] | first better / equal / worse |")
    print("|---|---:|---:|")
    for k, p in pairs.items():
        if k == BASELINE:
            continue
        d = p["diff"]
        print(f"| {LABEL.get(k, k)} | {d[0] * 100:+.1f} [{d[1] * 100:+.1f}; {d[2] * 100:+.1f}] | {p['better']} / {p['equal']} / {p['worse']} |")
