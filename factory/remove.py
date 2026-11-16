#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Take originals out of every set (removal requests, privacy review); scores and report are recomputed afterwards.
Usage: remove.py <removed.json> [repo-root]"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1]
removed = {r["id"]: r for r in json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))}
gone = 0


def dump(path: Path, data) -> None:
    end = "\n" if path.read_text(encoding="utf-8").endswith("\n") else ""
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + end, encoding="utf-8")


for f in sorted((root / "data").glob("manifest*.json")):
    man = json.loads(f.read_text(encoding="utf-8"))
    dump(f, [m for m in man if m["id"] not in removed])
# Build logs keep the entry so that the drop is documented like any other
for f in sorted((root / "data").glob("build*.json")):
    res = json.loads(f.read_text(encoding="utf-8"))
    dump(f, [{"id": r["id"], "reason": f"removed after review: {removed[r['id']]['reason']} ({removed[r['id']]['date']})"}
             if r["id"] in removed else r for r in res])
for f in sorted((root / "data").glob("*-render.jsonl")):
    lines = f.read_text(encoding="utf-8").splitlines()
    f.write_text("".join(ln + "\n" for ln in lines if json.loads(ln)["id"] not in removed), encoding="utf-8")
for pattern in ("data/pdf*/{}.pdf", "data/truth*/{}.truth.json", "results/outputs*/*/{}.md", "results/outputs*/*/{}.time.json"):
    for i in removed:
        for p in root.glob(pattern.format(i)):
            p.unlink()
            gone += 1
print(f"{len(removed)} originals removed, {gone} files deleted")
