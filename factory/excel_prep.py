#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""For the Excel producer: copy each workbook so that only the manifest's sheets ("sheets") are visible and
cropped sheets ("crop") get the same print area, so Excel prints the same cells as LibreOffice. Only
xl/workbook.xml changes. Usage: excel_prep.py <manifest.json> <originals-dir> <dest-dir>"""
import html
import json
import re
import sys
import zipfile
from pathlib import Path


def print_area(xml: str, names: list[str], crop: dict[str, str]) -> str:
    for sheet, rng in crop.items():
        idx = names.index(sheet)
        xml = re.sub(rf'<definedName\b[^>]*name="_xlnm\.Print_Area"[^>]*localSheetId="{idx}"[^>]*>.*?</definedName>', "", xml, flags=re.S)
        xml = re.sub(rf'<definedName\b[^>]*localSheetId="{idx}"[^>]*name="_xlnm\.Print_Area"[^>]*>.*?</definedName>', "", xml, flags=re.S)
        a, b = rng.split(":")
        ref = "'" + sheet.replace("'", "''") + "'!" + "$" + re.sub(r"(\d+)", r"$\1", a) + ":$" + re.sub(r"(\d+)", r"$\1", b)
        node = f'<definedName name="_xlnm.Print_Area" localSheetId="{idx}">{html.escape(ref, quote=False)}</definedName>'
        if "<definedNames>" in xml:
            xml = xml.replace("<definedNames>", "<definedNames>" + node, 1)
        elif "<definedNames/>" in xml:
            xml = xml.replace("<definedNames/>", f"<definedNames>{node}</definedNames>", 1)
        else:
            xml = xml.replace("</sheets>", f"</sheets><definedNames>{node}</definedNames>", 1)
    return xml


def sheet_names(xml: str) -> list[str]:
    return [html.unescape(re.search(r'\bname="([^"]*)"', s).group(1)) for s in re.findall(r"<sheet\b[^>]*/>", xml)]


def hide(xml: str, keep: set[str]) -> str:
    sheets = re.findall(r"<sheet\b[^>]*/>", xml)
    names = [html.unescape(re.search(r'\bname="([^"]*)"', s).group(1)) for s in sheets]
    if not keep & set(names):
        raise ValueError("no selected sheet in the workbook")
    for s, n in zip(sheets, names):
        t = re.sub(r'\s+state="[^"]*"', "", s)
        if n not in keep:
            t = t.replace("<sheet ", '<sheet state="hidden" ', 1)
        xml = xml.replace(s, t, 1)
    # the active sheet must be visible
    first = next(i for i, n in enumerate(names) if n in keep)
    xml = re.sub(r'\bactiveTab="\d+"', f'activeTab="{first}"', xml)
    return re.sub(r'\bfirstSheet="\d+"', f'firstSheet="{first}"', xml)


def main() -> None:
    man, src, dest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), Path(sys.argv[2]), Path(sys.argv[3])
    dest.mkdir(parents=True, exist_ok=True)
    for m in (m for m in man if m["format"] == "xlsx"):
        with zipfile.ZipFile(src / f"{m['id']}.xlsx") as zin, \
                zipfile.ZipFile(dest / f"{m['id']}.xlsx", "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "xl/workbook.xml":
                    xml = hide(data.decode("utf-8"), set(m["sheets"]))
                    data = print_area(xml, sheet_names(xml), m.get("crop", {})).encode("utf-8")
                zout.writestr(item, data)
    print(sum(1 for m in man if m["format"] == "xlsx"), "workbooks prepared")


if __name__ == "__main__":
    main()
