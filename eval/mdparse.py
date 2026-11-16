#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Each candidate's Markdown → text and tables under the same rules (pipe and HTML tables), words, numbers.
Standard library only. `python3 -I mdparse.py --selfcheck` checks on hand-written examples that all notations
yield the same table."""
from __future__ import annotations

import html
import re
import sys
import unicodedata
from html.parser import HTMLParser

FOLD = str.maketrans({**{c: "-" for c in "‐‑‒–—―−"}, **{c: "'" for c in "‘’‚‛`´"}, **{c: '"' for c in "“”„‟«»"},
                      "\u00ad": None, "\u200b": None, "\ufeff": None, "\u00a0": " ", "\u202f": " ", "\u2009": " "})
SEP_ROW = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")
PIPE_SPLIT = re.compile(r"(?<!\\)\|")


def inline(s: str) -> str:
    """Inline Markdown and HTML → plain text (images are dropped, links keep their text)."""
    s = re.sub(r"\$\$?(.+?)\$\$?", lambda m: latex(m.group(1)), s, flags=re.S)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[\^([^\]]+)\]:?", r" \1 ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"</?[A-Za-z][^>]*>", "", s)
    s = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>~$%&])", r"\1", s)
    s = re.sub(r"(\*\*|__|\*|~~|`)", "", s)
    s = re.sub(r"(?<!\w)_|_(?!\w)", " ", s)
    return html.unescape(s)


def latex(s: str) -> str:
    s = re.sub(r"\\(?:text|mathrm|mathbf|textbf|textit|operatorname|mathit)\s*\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\([%$&#_])", r"\1", s)
    s = re.sub(r"\\[A-Za-z]+", " ", s)
    return re.sub(r"[{}^_]", "", s)


class _Tables(HTMLParser):
    """HTML tables → grid; colspan/rowspan as usual in pipe tables: value in the first cell, the others empty."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self.stack: list[dict] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.stack.append({"rows": [], "row": None, "cell": None, "span": {}})
        elif not self.stack:
            return
        elif tag == "tr":
            self.stack[-1]["row"] = []
        elif tag in ("td", "th"):
            t = self.stack[-1]
            if t["row"] is None:
                t["row"] = []
            t["cell"] = {"text": [], "cs": int(a.get("colspan") or 1), "rs": int(a.get("rowspan") or 1)}
        elif tag == "br" and self.stack[-1]["cell"] is not None:
            self.stack[-1]["cell"]["text"].append(" ")

    def handle_endtag(self, tag):
        if not self.stack:
            return
        t = self.stack[-1]
        if tag in ("td", "th") and t["cell"] is not None:
            t["row"].append(t["cell"])
            t["cell"] = None
        elif tag == "tr" and t["row"] is not None:
            t["rows"].append(t["row"])
            t["row"] = None
        elif tag == "table":
            self.stack.pop()
            grid = _expand(t["rows"])
            if self.stack and self.stack[-1]["cell"] is not None:  # nested: becomes text of the outer cell
                self.stack[-1]["cell"]["text"].append(" ".join(c for r in grid for c in r))
            else:
                self.tables.append(grid)

    def handle_data(self, data):
        if self.stack and self.stack[-1]["cell"] is not None:
            self.stack[-1]["cell"]["text"].append(data)


def _expand(rows: list[list[dict]]) -> list[list[str]]:
    grid: list[list[str]] = []
    pending: dict[tuple[int, int], str] = {}
    for r, row in enumerate(rows):
        out: list[str] = []
        col = 0
        for cell in row:
            while (r, col) in pending:
                out.append(pending.pop((r, col)))
                col += 1
            out.append(clean_cell("".join(cell["text"])))
            for k in range(1, cell["cs"]):
                out.append("")
            for rr in range(1, cell["rs"]):
                for k in range(cell["cs"]):
                    pending[(r + rr, col + k)] = ""
            col += cell["cs"]
        while (r, col) in pending:
            out.append(pending.pop((r, col)))
            col += 1
        grid.append(out)
    return grid


def clean_cell(s: str) -> str:
    return re.sub(r"\s+", " ", inline(s)).strip()


def parse(md: str) -> tuple[str, list[list[list[str]]]]:
    """→ (text in reading order, tables as grids). Tables appear in the text row by row, cells separated by " | "."""
    md = unicodedata.normalize("NFKC", md).translate(FOLD).replace("\r\n", "\n")
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.S)
    tables: list[list[list[str]]] = []

    def html_table(m: re.Match) -> str:
        p = _Tables()
        p.feed(m.group(0))
        tables.extend(p.tables)
        return "\n" + "\n".join(" | ".join(r) for g in p.tables for r in g) + "\n"

    md = re.sub(r"<table\b.*?</table>", html_table, md, flags=re.S | re.I)
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        if "|" in lines[i] and i + 1 < len(lines) and SEP_ROW.match(lines[i + 1]) and "-" in lines[i + 1]:
            block = [lines[i]]
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                block.append(lines[j])
                j += 1
            grid = [pipe_row(r) for r in block]
            tables.append(grid)
            out.extend(" | ".join(r) for r in grid)
            i = j
            continue
        ln = lines[i]
        ln = re.sub(r"^\s{0,3}(#{1,6}\s+|>\s?|[-*+]\s+(\[[ xX]\]\s+)?)", "", ln)
        if re.fullmatch(r"\s*([-*_]\s*){3,}", ln):
            ln = ""
        out.append(inline(ln))
        i += 1
    text = "\n".join(out)
    return text, [[r for r in g if any(c for c in r)] for g in tables if any(any(c for c in r) for r in g)]


def pipe_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [clean_cell(c.replace("\\|", "|")) for c in PIPE_SPLIT.split(s)]


def dehyphen(s: str) -> str:
    """Undo end-of-line hyphenation (the PDF text layer keeps it, many Markdown writers remove it)."""
    return re.sub(r"(\w)-[ \t]*\n[ \t]*(?=[a-zäöüßàâçéèêëîïôûùüÿñæœáíóú])", r"\1", s)


def tokens(s: str) -> list[str]:
    """Words lowercased; numbers without thousands and decimal separators ("1 268 082", "1.268.082" and "1268082" are
    equal, so are "2,1" and "2.1"): the notation of a number does not decide a match."""
    s = unicodedata.normalize("NFKC", s).translate(FOLD).lower()
    # space-separated thousands groups only where the number has no other separators ("201.343 201.343" are two)
    s = re.sub(r"(?<![\d.,])(\d{1,3})((?: \d{3})+)(?!\d|[.,]\d)", lambda m: m.group(1) + m.group(2).replace(" ", ""), s)
    s = re.sub(r"(?<=\d)[.,](?=\d)", "", s)
    return [t for t in re.findall(r"\w+", s) if t.strip("_")]


def cell_key(s: str) -> str:
    """Comparison key of a cell: number cell → digit string, otherwise the words."""
    return " ".join(tokens(s))


def is_number_cell(s: str) -> bool:
    t = tokens(s)
    return len(t) == 1 and t[0].isdigit()


def lcs_len(a: list[str], b: list[str]) -> int:
    """Length of the longest common subsequence (bit-parallel, after Crochemore et al.)."""
    if not a or not b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    pos: dict[str, int] = {}
    for i, t in enumerate(a):
        pos[t] = pos.get(t, 0) | (1 << i)
    full = (1 << len(a)) - 1
    v = full
    for t in b:
        u = v & pos.get(t, 0)
        v = ((v + u) | (v - u)) & full
    return len(a) - bin(v).count("1")


# Three hand-written examples of the same table: terse (escapes, empty spanned cells), padded (<sup>, <br>, bold)
# and HTML. All must yield the same grid.
EXAMPLE_TERSE = """Text before.

| Year | Arrivals | | Rate \\| % |
|---|---|---|---|
| | total | of which foreign¹ | |
| 1990 | 8 208 | 597 752 | 42,0 |
| **2000** | 14 318 | 1 114 501 | 39,4 |
"""
EXAMPLE_PADDED = """Text before.

| Year     | Arrivals  |                                         | Rate \\| %    |
|----------|-----------|-----------------------------------------|-------------|
|          | total     | of which<br>foreign<sup>1</sup>         |             |
| 1990     | 8 208     | 597 752                                 | 42,0        |
| **2000** | 14 318    | 1 114 501                               | 39,4        |
"""
EXAMPLE_HTML = """<table><tr><th>Year</th><th colspan="2">Arrivals</th><th>Rate | %</th></tr>
<tr><td></td><td>total</td><td>of which foreign<sup>1</sup></td><td></td></tr>
<tr><td>1990</td><td>8 208</td><td>597 752</td><td>42,0</td></tr><tr><td><b>2000</b></td><td>14 318</td><td>1 114 501</td><td>39,4</td></tr></table>"""
EXAMPLE_GRID = [["Year", "Arrivals", "", "Rate | %"], ["", "total", "of which foreign1", ""],
                ["1990", "8 208", "597 752", "42,0"], ["2000", "14 318", "1 114 501", "39,4"]]


def selfcheck() -> None:
    """Exits if the hand-written examples do not yield the same grid and the same words."""
    seen = []
    for name, md in (("terse", EXAMPLE_TERSE), ("padded", EXAMPLE_PADDED), ("html", "Text before.\n\n" + EXAMPLE_HTML)):
        text, tabs = parse(md)
        keys = [[cell_key(c) for c in r] for r in tabs[0]] if len(tabs) == 1 else None
        want = [[cell_key(c) for c in r] for r in EXAMPLE_GRID]
        # "¹" becomes "1" under NFKC, <sup>1</sup> becomes "1": both notations give the same digit
        if keys != want:
            raise SystemExit(f"self-check: table from {name} read as {tabs!r}")
        seen.append(tokens(text))
    if not all(s == seen[0] for s in seen):
        raise SystemExit(f"self-check: words differ: {seen!r}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selfcheck"]:
        selfcheck()
        print("self-check ok: all notations yield the same table")
    else:
        text, tabs = parse(open(sys.argv[1], encoding="utf-8").read())
        print(text)
        for t in tabs:
            print(t)
