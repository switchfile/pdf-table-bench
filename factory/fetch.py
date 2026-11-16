#!/usr/bin/env python3
"""Step 2: download candidates (at most 8 MB, genuine OOXML), record SHA-256 and fetch time.
Usage: fetch.py <candidates.json> <originals-dir> <fetched.json> [excluded-sha.txt]"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

UA = "open-pdf-table-bench/0.1 (research; contact via repository)"
MAX_BYTES = 8_000_000
PART = {"xlsx": "xl/workbook.xml", "docx": "word/document.xml"}


def load(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("larger than 8 MB")
    return data


def main() -> None:
    cands = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    dest, out = Path(sys.argv[2]), Path(sys.argv[3])
    excluded = set(Path(sys.argv[4]).read_text().split()) if len(sys.argv) > 4 else set()
    dest.mkdir(parents=True, exist_ok=True)
    done, seen = [], set()
    for c in cands:
        try:
            data = load(c["url"])
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                names = set(z.namelist())
                if PART[c["format"]] not in names or any(n.lower().endswith("vbaproject.bin") for n in names):
                    raise ValueError("not plain OOXML of this format")
                if z.getinfo(PART[c["format"]]).file_size > 50_000_000:
                    raise ValueError("content too large")
        except Exception as e:  # noqa: BLE001 – a broken or foreign file only drops itself
            print("dropped", c["id"], type(e).__name__, str(e)[:80], flush=True)
            continue
        sha = hashlib.sha256(data).hexdigest()
        if sha in excluded or sha in seen:
            print("dropped", c["id"], "checksum already known", flush=True)
            continue
        seen.add(sha)
        (dest / f"{c['id']}.{c['format']}").write_bytes(data)
        done.append({**c, "sha256": sha, "bytes": len(data),
                     "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
        time.sleep(0.5)
    out.write_text(json.dumps(done, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(done), "of", len(cands), "fetched")


if __name__ == "__main__":
    main()
