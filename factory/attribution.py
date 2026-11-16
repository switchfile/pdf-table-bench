#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DATA-SOURCES.md with the attribution each license asks for. Usage: attribution.py fetch <manifest> <attribution.json>
(catalog metadata: creators, provider, last update, license link), then attribution.py <manifest> <attribution.json> <out.md>"""
import json
import sys
import textwrap
import time
import urllib.request
from pathlib import Path

LINKS = {
    "Open Government Licence v3.0": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    "Datenlizenz Deutschland – Namensnennung – Version 2.0": "https://www.govdata.de/dl-de/by-2-0",
    "Datenlizenz Deutschland – Zero – Version 2.0": "https://www.govdata.de/dl-de/zero-2-0",
    "Licence Ouverte / Open Licence 2.0 (Etalab)": "https://www.etalab.gouv.fr/licence-ouverte-open-licence/",
    "Licence Ouverte / Open Licence 1.0 (Etalab)": "https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Licence_Ouverte.pdf",
    "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC0 1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
}
LICENCE_OUVERTE = ("fr-lo", "lov2")
# Catalog title is a person's name (privacy review); the file name of the resource is used instead
TITLE_FROM_FILE = {"en-xlsx-3e677a9c40"}


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "pdf-md-benchmark-attribution/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fetch(man: list[dict]) -> dict:
    out = {}
    for m in man:
        a: dict = {}
        if m["source"] == "zenodo":
            rec = get("https://zenodo.org/api/records/" + m["landing"].rstrip("/").rsplit("/", 1)[1])
            a["creators"] = [c["name"] for c in rec["metadata"]["creators"]]
        elif m["source"] == "gouvfr":
            d = get("https://www.data.gouv.fr/api/1/datasets/" + m["landing"].rstrip("/").rsplit("/", 1)[1] + "/")
            if d.get("organization"):
                a["provider"] = d["organization"]["name"]
            elif d.get("owner"):
                a["provider"] = f"{d['owner']['first_name']} {d['owner']['last_name']}".strip()
            res = [r for r in d["resources"] if r["url"] == m["url"]]
            if m["license_id"] in LICENCE_OUVERTE and res:
                a["updated"] = res[0]["last_modified"][:10]
            if m["license_id"] == "cc-by":
                lic = {x["id"]: x for x in get("https://www.data.gouv.fr/api/1/datasets/licenses/")}["cc-by"]
                a["license_url"] = lic["url"]
        elif m["source"] == "uk" and m["license_id"] == "cc-by":
            d = get("https://ckan.publishing.service.gov.uk/api/action/package_show?id="
                    + m["landing"].split("/dataset/", 1)[1].split("/", 1)[0])["result"]
            a["license_url"] = d["license_url"]
        if a:
            out[m["id"]] = a
        time.sleep(0.2)
    return {"retrieved": time.strftime("%Y-%m-%d"), "items": out}


def render(man: list[dict], att: dict) -> str:
    items = att["items"]
    lines = ["# Data sources and licenses", "",
             "Every PDF in this benchmark was generated from the public original listed below. The originals are not",
             "redistributed here; each row links the original and its catalog page and gives its SHA-256. The PDFs are",
             "derived works: printed with LibreOffice (version in `factory/Dockerfile`), Microsoft Word for Mac or Microsoft",
             "Excel for Mac; workbooks reduced to at most four printed sheets and 20 pages. Truth files are extracted from the",
             "originals; candidate outputs contain the text of the documents. Each item stays under the license of its",
             "original. **The data were changed:** format conversion to PDF, sheet selection, long sheets cut to their first",
             "pages (print area; field `crop` in `data/manifest.json`), document information (author, title) removed.",
             "",
             "Publishers do not endorse this benchmark. Logos, crests and trade marks in the documents belong to their owners",
             "and are not licensed by this repository. To have a document removed, see \"Corrections and removal\" in the",
             "README.",
             "",
             "Contains public sector information licensed under the Open Government Licence v3.0.",
             "",
             *textwrap.wrap(f"Column \"publisher / creators\": the provider named by the catalog; for Zenodo all creators of the record. "
             f"Column \"updated\": last update of the resource in the catalog, as the Licence Ouverte asks. Catalog "
             f"metadata retrieved {att['retrieved']}. \"CC BY (version not stated)\": the catalog names Creative Commons "
             f"Attribution without a version; the link is the one the catalog gives.", 114),
             "",
             "| id | publisher / creators | title | license | updated | original | fetched | SHA-256 |",
             "|---|---|---|---|---|---|---|---|"]
    for m in sorted(man, key=lambda m: m["id"]):
        a = items.get(m["id"], {})
        pub = "; ".join(a["creators"]) if "creators" in a else a.get("provider") or m["publisher"].split(":", 1)[-1]
        title = m["url"].rstrip("/").rsplit("/", 1)[-1] if m["id"] in TITLE_FROM_FILE else (m["title"] or "")
        title = title.replace("|", "/").replace("\n", " ")[:80]
        if m["license"] == "CC BY":
            lic = f"[CC BY (version not stated)]({a['license_url']})"
        else:
            lic = f"[{m['license']}]({LINKS[m['license']]})"
        lines.append(f"| {m['id']} | {pub.replace('|', '/')} | {title} | {lic} | {a.get('updated', '')} | [file]({m['url']}) "
                     f"([page]({m['landing']})) | {m['fetched'][:10]} | `{m['sha256'][:16]}…` |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if sys.argv[1] == "fetch":
        man = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        Path(sys.argv[3]).write_text(json.dumps(fetch(man), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        man = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        att = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        Path(sys.argv[3]).write_text(render(man, att), encoding="utf-8")
