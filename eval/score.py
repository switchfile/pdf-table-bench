#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Scoring PDF → Markdown, identical for all candidates (standard library only). First checks with mdparse.selfcheck()
that pipe and HTML tables are read the same. Usage: score.py <sets> <out> <cand,cand,…> <dest.json>.
Metrics: README.md, section "Metrics"."""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdparse import (cell_key, decimal_mark, dehyphen, is_number_cell, is_number_token, lcs_len, number_value, parse,  # noqa: E402
                    selfcheck, tokens)

# country per source; Zenodo files come from many countries
COUNTRY = {"gouvfr": "FR", "govdata": "DE", "hamburg": "DE", "uk": "UK", "zenodo": "INT"}
FAMILY = {"libreoffice": "libreoffice", "word": "office", "excel": "office"}
ROW_MIN = 0.3  # minimum similarity (share of common cells) for two table rows to correspond


def row_sim(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    inter = sum((a & b).values())
    return inter / max(sum(a.values()), sum(b.values()))


def align_rows(trows: list[Counter], prows: list[Counter]) -> dict[int, int]:
    """Monotonic mapping truth row → output row with the largest sum of similarities (rows may be missing)."""
    n, m = len(trows), len(prows)
    index: dict[str, set[int]] = {}
    for j, r in enumerate(prows):
        for k in r:
            index.setdefault(k, set()).add(j)
    sims = [{j: s for j in set().union(*(index.get(k, set()) for k in r)) if (s := row_sim(r, prows[j])) >= ROW_MIN}
            for r in trows]
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        bi, bp, si = best[i], best[i - 1], sims[i - 1]
        for j in range(1, m + 1):
            v = max(bp[j], bi[j - 1])
            s = si.get(j - 1)
            if s is not None and bp[j - 1] + s > v:
                v = bp[j - 1] + s
            bi[j] = v
    out, i, j = {}, n, m
    while i and j:
        s = sims[i - 1].get(j - 1)
        if s is not None and abs(best[i][j] - (best[i - 1][j - 1] + s)) < 1e-9:
            out[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif best[i][j] == best[i - 1][j]:
            i -= 1
        else:
            j -= 1
    return out


def doc_mark(truth_tables: list[dict], lang: str | None = None) -> str:
    """Decimal separator of a document, from its truth tables (one table may hold no decimals); without decimals there,
    by language ("49.000" in a German table is 49000)."""
    return decimal_mark([r for t in truth_tables for r in t["rows"]], "," if lang in ("de", "fr") else ".")


def table_numbers(truth_tables: list[dict], pred_tables: list[list[list[str]]], mark: str | None = None) -> tuple[int, int, int]:
    """→ (number cells in the truth, of which in the right row and column, of those also with the same signed value). Rows are matched via common cells
    (also across several output tables, e.g. split per page); columns per output table by majority of
    matching cells in matched rows, one to one."""
    mark = mark or doc_mark(truth_tables)
    prow = [(ti, ri, [cell_key(c, mark) for c in r]) for ti, t in enumerate(pred_tables) for ri, r in enumerate(t)]
    praw = [r for t in pred_tables for r in t]
    pcount = [Counter(k for k in r if k) for _, _, r in prow]
    total = hit = strict = 0
    for t in truth_tables:
        rows = [[cell_key(c, mark) if c else "" for c in r] for r in t["rows"]]
        num = t.get("numeric") or [[bool(c) and is_number_cell(c, mark) for c in r] for r in t["rows"]]
        keep = [i for i, r in enumerate(rows) if any(r)]
        amap = align_rows([Counter(k for k in rows[i] if k) for i in keep], pcount)
        rmap = {keep[a]: b for a, b in amap.items()}
        votes: Counter = Counter()
        for tr, pr in rmap.items():
            ti, _, pcells = prow[pr]
            for c, k in enumerate(rows[tr]):
                if k:
                    for j, pk in enumerate(pcells):
                        if pk == k:
                            votes[(ti, c, j)] += 1
        cmap: dict[tuple[int, int], int] = {}
        used: set[tuple[int, int]] = set()
        for (ti, c, j), _ in sorted(votes.items(), key=lambda kv: (-kv[1], kv[0])):
            if (ti, c) not in cmap and (ti, j) not in used:
                cmap[(ti, c)] = j
                used.add((ti, j))
        for r, row in enumerate(rows):
            for c, k in enumerate(row):
                if not (k and num[r][c] and is_number_token(k)):
                    continue
                total += 1
                if r in rmap:
                    ti, _, pcells = prow[rmap[r]]
                    j = cmap.get((ti, c))
                    if j is not None and j < len(pcells) and pcells[j] == k:
                        hit += 1
                        tv, pv = number_value(t["rows"][r][c], mark), number_value(praw[rmap[r]][j], mark)
                        strict += tv is not None and pv is not None and abs(tv - pv) <= 1e-9 * max(1.0, abs(tv))
    return total, hit, strict


def score_one(truth: dict, md: str | None, lang: str | None = None) -> dict:
    mark = doc_mark(truth["tables"], lang)
    ttok = tokens(dehyphen(truth["text"]), mark)
    if md is None:  # a failure counts as 0 in every metric
        nt, _, _ = table_numbers(truth["tables"], [], mark)
        return {"failed": True, "recall": 0.0, "precision": 0.0, "bag": 0.0, "order": 0.0, "cells": nt, "cells_hit": 0,
                "cells_value": 0,
                "nums": 0, "nums_false": 0}
    text, tabs = parse(md)
    ptok = tokens(dehyphen(text), mark)
    lcs = lcs_len(ttok, ptok)
    bag = sum((Counter(ttok) & Counter(ptok)).values())
    # corrupted numbers: number tokens in the output that are neither in the truth nor in the page's text layer
    allowed = (Counter(t for t in ttok if is_number_token(t))
               | Counter(t for t in tokens(dehyphen(truth["layer"]), mark) if is_number_token(t)))
    pnums = Counter(t for t in ptok if is_number_token(t))
    nt, nh, nv = table_numbers(truth["tables"], tabs, mark)
    return {"failed": False, "recall": lcs / len(ttok) if ttok else 1.0, "precision": lcs / len(ptok) if ptok else 0.0,
            "bag": bag / len(ttok) if ttok else 1.0, "order": lcs / bag if bag else 0.0, "cells": nt, "cells_hit": nh,
            "cells_value": nv, "nums": sum(pnums.values()), "nums_false": sum((pnums - allowed).values()), "words": len(ttok),
            "pipe_tables": len(tabs)}


def boot(vals: list[float], clusters: list | None = None, den: list[float] | None = None, n: int = 10000,
         seed: int = 7) -> tuple[float, float, float]:
    """Estimate and 95 % interval (percentile bootstrap): Σvals/Σden, without den the mean. Resampling is per cluster;
    renderings of the same original by several producers are not independent and are only drawn together."""
    if not vals:
        return (float("nan"),) * 3
    den = den or [1.0] * len(vals)
    agg: dict = {}
    for c, v, d in zip(clusters or range(len(vals)), vals, den):
        a = agg.setdefault(c, [0.0, 0.0])
        a[0] += v
        a[1] += d
    groups, rng = list(agg.values()), random.Random(seed)
    stats = []
    for _ in range(n):
        draw = rng.choices(groups, k=len(groups))
        stats.append(sum(g[0] for g in draw) / sum(g[1] for g in draw))
    stats.sort()
    return sum(vals) / sum(den), stats[int(0.025 * n)], stats[int(0.975 * n) - 1]


def origin(m: dict) -> str:
    return m.get("origin", m["id"])


def summarize(ms: list[dict], per: dict, k: str) -> dict:
    rs, cl = [per[m["id"]][k] for m in ms], [origin(m) for m in ms]
    # word hits ignore order; order is a separate metric (otherwise an order error would count twice)
    rec, order = boot([r["bag"] for r in rs], cl), boot([r["order"] for r in rs], cl)
    wc = [(r, c) for r, c in zip(rs, cl) if r["cells"]]
    cells, hits = sum(r["cells"] for r in rs), sum(r["cells_hit"] for r in rs)
    value = sum(r.get("cells_value", 0) for r in rs)
    nums, false = sum(r["nums"] for r in rs), sum(r["nums_false"] for r in rs)
    ok = [(m, r) for m, r in zip(ms, rs) if "seconds" in r and not r["failed"]]
    pages = sum(m["pages"] for m, _ in ok)
    secs = sorted(r["seconds"] / m["pages"] for m, r in ok)
    return {"files": len(ms), "pages": sum(m["pages"] for m in ms), "words": rec, "words_lcs": statistics.fmean(r["recall"] for r in rs),
            "order": order, "precision": statistics.fmean(r["precision"] for r in rs), "cells": cells, "cells_hit": hits,
            "cells_rate": hits / cells if cells else None, "cells_value": value,
            "cells_value_rate": value / cells if cells else None,
            "cells_rate_ci": boot([r["cells_hit"] for r, _ in wc], [c for _, c in wc], [r["cells"] for r, _ in wc]),
            # averaged per file: otherwise a few large tables dominate the cell sum
            "cells_file": boot([r["cells_hit"] / r["cells"] for r, _ in wc], [c for _, c in wc]), "nums": nums, "nums_false": false,
            "nums_false_files": sum(1 for r in rs if r["nums_false"]),
            "sec_per_page": sum(r["seconds"] for _, r in ok) / pages if pages else None,
            "sec_per_page_median": secs[len(secs) // 2] if secs else None, "failed": sum(r["failed"] for r in rs)}


def main() -> None:
    selfcheck()
    sets, out, cands, dest = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(","), Path(sys.argv[4])
    man = json.loads((sets / "manifest.json").read_text(encoding="utf-8"))
    per: dict[str, dict[str, dict]] = {}
    for m in man:
        truth = json.loads((sets / f"{m['id']}.truth.json").read_text(encoding="utf-8"))
        for k in cands:
            f = out / k / f"{m['id']}.md"
            md = f.read_text(encoding="utf-8") if f.exists() and f.stat().st_size else None
            r = score_one(truth, md, m.get("lang"))
            tf = out / k / f"{m['id']}.time.json"
            if tf.exists():
                r["seconds"] = json.loads(tf.read_text(encoding="utf-8"))["seconds"]
            per.setdefault(m["id"], {})[k] = r
    groups = {"all": man}
    for m in man:
        if m.get("source") in COUNTRY:
            m["country"] = COUNTRY[m["source"]]
        if m.get("producer") in FAMILY:
            m["family"] = FAMILY[m["producer"]]
    for key in ("family", "producer", "format", "country", "lang"):
        for v in sorted({m[key] for m in man if key in m}):
            groups[f"{key}={v}"] = [m for m in man if m.get(key) == v]
    summary = {g: {k: summarize(ms, per, k) for k in cands} for g, ms in groups.items()}
    # paired per file against the first candidate: difference in cell rate (only files with number cells)
    paired: dict = {}
    for g in [g for g in groups if g == "all" or g.startswith("family=")]:
        ms = [m for m in groups[g] if per[m["id"]][cands[0]]["cells"]]
        for k in cands[1:]:
            d = [per[m["id"]][cands[0]]["cells_hit"] / per[m["id"]][cands[0]]["cells"]
                 - per[m["id"]][k]["cells_hit"] / per[m["id"]][k]["cells"] for m in ms]
            paired.setdefault(g, {})[k] = {"diff": boot(d, [origin(m) for m in ms]), "better": sum(x > 0 for x in d),
                                           "equal": sum(x == 0 for x in d), "worse": sum(x < 0 for x in d)}
    dest.write_text(json.dumps({"manifest": man, "scores": per, "summary": summary, "paired": paired}, indent=1, ensure_ascii=False),
                    encoding="utf-8")
    for g, ms in groups.items():
        print(f"\n== {g}: {len(ms)} files, {sum(m['pages'] for m in ms)} pages")
        print(f"{'Candidate':<12} {'Word hits':>22} {'Order':>22} {'Prec.':>6} {'Cells correct':>22} "
              f"{'Same value':>11} {'Corrupted nums':>17} {'s/page':>8} {'Failed':>9}")
        for k in cands:
            s = summary[g][k]
            rec, order = s["words"], s["order"]
            print(f"{k:<12} {rec[0]*100:6.1f} [{rec[1]*100:5.1f}–{rec[2]*100:5.1f}] {order[0]*100:6.1f} "
                  f"[{order[1]*100:5.1f}–{order[2]*100:5.1f}] {s['precision']*100:6.1f} "
                  f"{(float('nan') if s['cells_rate'] is None else s['cells_rate']) * 100:7.1f} ({s['cells_hit']:>5}/{s['cells']:<5}) "
                  f"{(float('nan') if s['cells_value_rate'] is None else s['cells_value_rate']) * 100:11.1f} "
                  f"{s['nums_false']:6d}/{s['nums']:<8d} {(float('nan') if s['sec_per_page'] is None else s['sec_per_page']):8.2f} {s['failed']:9d}")


if __name__ == "__main__":
    main()
