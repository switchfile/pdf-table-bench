#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Merge the sets of several PDF producers into one set for score.py (copies; per-producer id suffix).
Usage: combine.py <dest-set> <dest-out> <producer>,<manifest>,<pdf-dir>,<truth-dir>,<out-dir>[,<suffix>] …"""
import json
import shutil
import sys
from pathlib import Path

dest, dout = Path(sys.argv[1]), Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=True)
man = []
for spec in sys.argv[3:]:
    producer, manifest, pdfs, truths, outs, *suffix = spec.split(",")
    sfx = suffix[0] if suffix else ""
    for m in json.loads(Path(manifest).read_text(encoding="utf-8")):
        fid = m["id"] + sfx
        shutil.copyfile(Path(pdfs) / f"{m['id']}.pdf", dest / f"{fid}.pdf")
        shutil.copyfile(Path(truths) / f"{m['id']}.truth.json", dest / f"{fid}.truth.json")
        man.append({**m, "id": fid, "producer": producer, "origin": m["id"]})
        for cand in (p for p in Path(outs).iterdir() if p.is_dir()):
            (dout / cand.name).mkdir(parents=True, exist_ok=True)
            for ext in (".md", ".time.json"):
                f = cand / f"{m['id']}{ext}"
                if f.exists():
                    shutil.copyfile(f, dout / cand.name / f"{fid}{ext}")
(dest / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(man), "files")
