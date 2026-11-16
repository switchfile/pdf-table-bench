#!/usr/bin/env python3
"""Step 1: openly licensed candidates (XLSX, DOCX) from public catalogues, metadata only.
Usage: discover.py <seed> <dest.json> [excluded.txt] [formats] [sources] [count] [manifest.json]  (excluded: one
URL per line, not published; follow-up draw e.g. "xlsx uk,govdata 150 data/manifest.json")."""
from __future__ import annotations

import hashlib
import json
import random
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

UA = "open-pdf-table-bench/0.1 (research; contact via repository)"
# catalogue licence id → name; only licences that allow redistribution and modification with (or without) attribution
LICENSES = {
    "uk-ogl": "Open Government Licence v3.0",
    "http://dcat-ap.de/def/licenses/dl-by-de/2.0": "Datenlizenz Deutschland – Namensnennung – Version 2.0",
    "http://dcat-ap.de/def/licenses/dl-zero-de/2.0": "Datenlizenz Deutschland – Zero – Version 2.0",
    "http://dcat-ap.de/def/licenses/cc-by/4.0": "CC BY 4.0",
    "http://dcat-ap.de/def/licenses/cc-zero": "CC0 1.0",
    "dl-de-by-2.0": "Datenlizenz Deutschland – Namensnennung – Version 2.0",
    "cc-zero": "CC0 1.0",
    "lov2": "Licence Ouverte / Open Licence 2.0 (Etalab)",
    "fr-lo": "Licence Ouverte / Open Licence 1.0 (Etalab)",
    "cc-by": "CC BY",
    "cc-by-4.0": "CC BY 4.0",
    "cc0-1.0": "CC0 1.0",
}
# per source: (language, format, target count in the pool)
PLAN = [("uk", "en", "xlsx", 45), ("govdata", "de", "xlsx", 45), ("gouvfr", "fr", "xlsx", 45),
        ("gouvfr", "fr", "docx", 30), ("hamburg", "de", "docx", 30), ("zenodo", "en", "docx", 30)]
# only for follow-up draws with a source list (keeps draws 1 and 2 reproducible)
EXTRA = [("hamburg", "de", "xlsx", 45)]
PER_PUBLISHER = 2
PAGES = 6  # random catalogue pages per source


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001 – catalogue briefly unreachable: retry twice
            time.sleep(3 * (i + 1))
    return {}


def ckan(base: str, fmt: str, rng: random.Random, portal: str, landing_tpl: str):
    q = {"fq": f"res_format:{fmt.upper()}", "rows": 0}
    n = get(f"{base}/package_search?" + urllib.parse.urlencode(q)).get("result", {}).get("count", 0)
    for _ in range(PAGES):
        q.update(rows=100, start=rng.randrange(max(1, n - 99)))
        for p in get(f"{base}/package_search?" + urllib.parse.urlencode(q)).get("result", {}).get("results", []):
            pub = p.get("author") or (p.get("organization") or {}).get("title") or p["id"]
            for r in p.get("resources") or []:
                if (r.get("format") or "").lower().strip() == fmt:
                    yield (r.get("url") or "").strip(), r.get("license") or p.get("license_id"), \
                        landing_tpl.format(**p), f"{portal}:{pub}", (r.get("name") or p.get("title") or "")[:200]
        time.sleep(1)


def udata(fmt: str, rng: random.Random):
    base = "https://www.data.gouv.fr/api/1"
    n = get(f"{base}/datasets/?format={fmt}&page_size=1").get("total", 0)
    for _ in range(PAGES):
        page = rng.randint(1, max(1, n // 100))
        for p in get(f"{base}/datasets/?format={fmt}&page_size=100&page={page}").get("data", []):
            pub = (p.get("organization") or p.get("owner") or {}).get("name") or p["id"]
            for r in p.get("resources") or []:
                if (r.get("format") or "").lower().strip() == fmt:
                    yield (r.get("url") or "").strip(), p.get("license"), p.get("page") or "", f"data.gouv.fr:{pub}", \
                        (r.get("title") or p.get("title") or "")[:200]
        time.sleep(1)


def zenodo(fmt: str, rng: random.Random):
    for _ in range(PAGES):
        page = rng.randint(1, 100)
        d = get(f"https://zenodo.org/api/records?file_type={fmt}&size=25&page={page}&sort=mostrecent")
        for h in d.get("hits", {}).get("hits", []):
            md = h.get("metadata", {})
            if (md.get("language") or "eng") != "eng":
                continue
            pub = "zenodo:" + ((md.get("creators") or [{}])[0].get("name") or str(h["id"]))
            for f in h.get("files", []):
                if f["key"].lower().endswith("." + fmt) and f.get("size", 0) < 5_000_000:
                    yield f["links"]["self"], (md.get("license") or {}).get("id"), f"https://zenodo.org/records/{h['id']}", \
                        pub, f["key"][:200]
        time.sleep(1)


def main() -> None:
    seed, dest = int(sys.argv[1]), Path(sys.argv[2])
    excluded = set(Path(sys.argv[3]).read_text().split()) if len(sys.argv) > 3 else set()
    formats = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else {"xlsx", "docx"}
    sources = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
    want_all = int(sys.argv[6]) if len(sys.argv) > 6 else None
    # publishers of the existing set count towards the per-publisher cap
    prior = Counter(m["publisher"] for m in json.loads(Path(sys.argv[7]).read_text(encoding="utf-8"))) \
        if len(sys.argv) > 7 else Counter()
    global PAGES
    if want_all:
        PAGES = max(PAGES, want_all // 10)
    rng = random.Random(seed)
    out = []
    for src, lang, fmt, want in PLAN + (EXTRA if sources else []):
        if fmt not in formats or sources and src not in sources:
            continue
        want = want_all or want
        if src == "uk":
            it = ckan("https://ckan.publishing.service.gov.uk/api/action", fmt, rng, "data.gov.uk",
                      "https://www.data.gov.uk/dataset/{id}/{name}")
        elif src == "govdata":
            it = ckan("https://www.govdata.de/ckan/api/3/action", fmt, rng, "GovData", "https://www.govdata.de/suche/daten/{name}")
        elif src == "hamburg":
            it = ckan("https://suche.transparenz.hamburg.de/api/3/action", fmt, rng, "Transparenzportal Hamburg",
                      "https://suche.transparenz.hamburg.de/dataset/{name}")
        elif src == "gouvfr":
            it = udata(fmt, rng)
        else:
            it = zenodo(fmt, rng)
        pool: dict[str, dict] = {}
        for url, lic, landing, pub, title in it:
            if not url.startswith("https://") or lic not in LICENSES or url in excluded or landing in excluded:
                continue
            key = f"{lang}-{fmt}-{hashlib.sha1(url.encode()).hexdigest()[:10]}"
            pool.setdefault(key, {"id": key, "lang": lang, "format": fmt, "source": src, "publisher": pub, "url": url,
                                  "landing": landing, "title": title, "license": LICENSES[lic], "license_id": lic})
        order = sorted(pool.values(), key=lambda c: c["id"])
        rng.shuffle(order)
        seen: Counter = Counter(prior)
        took = 0
        for c in order:
            if took < want and seen[c["publisher"]] < PER_PUBLISHER and seen["landing:" + c["landing"]] < 1:
                seen[c["publisher"]] += 1
                seen["landing:" + c["landing"]] += 1
                out.append(c)
                took += 1
        print(src, lang, fmt, len(pool), "in pool,", took, "chosen", flush=True)
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
