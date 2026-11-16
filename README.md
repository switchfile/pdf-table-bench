# Business PDF to Markdown: table cells and corrupted numbers

An open, reproducible benchmark for PDF → Markdown on native (born-digital) business documents. It measures what
page-level OCR benchmarks usually do not: whether every number lands in the right table cell, and whether the
converter writes numbers that are not in the document as written there.

This benchmark is published by Aura UG (haftungsbeschränkt), the company that makes switchfile, one of the candidates.
We ran every candidate ourselves, switchfile included; see [Who publishes this](#who-publishes-this) and
[Disclaimer](#disclaimer).

## Data

- 82 public spreadsheets (XLSX) and Word documents (DOCX) from government open-data portals and Zenodo, in English,
  German and French, under licenses that allow redistribution of derived works (Open Government Licence v3.0,
  Datenlizenz Deutschland 2.0, Licence Ouverte 1.0/2.0, CC BY 4.0, CC0). Sources, licenses, checksums and fetch
  dates: [DATA-SOURCES.md](DATA-SOURCES.md) and `data/manifest.json`. Country of the source: France (data.gouv.fr),
  Germany (GovData, Hamburg), United Kingdom (data.gov.uk), international (Zenodo). No country supplies more than
  half of the numeric cells (France 40 %, Germany 39 %, UK 11 %, international 9 %, LibreOffice set).
- Two originals were removed after a privacy review because they contain personal data of third parties
  (`data/removed.json`, `factory/remove.py`). They are absent from all sets, outputs and scores, and the build logs
  list them as removed.
- Four draws: two broad ones (seeds 20261115, 20261116) and two that add only German and UK spreadsheets (seeds
  20261117, 20261118), because the first draws left France with most numeric cells. In the last two draws a sheet that
  would exceed 20 pages is cut to its first pages (print area; field `crop` in the manifest).
- Two producer families, reported side by side: Microsoft Office (Word and Excel) and LibreOffice (Writer and Calc).
  Each program runs on every original it can open:
  - LibreOffice 25.2 (MPL-2.0): all 82 originals, pinned build in a container (`factory/Dockerfile`), with the locale of the
    document's language. 404 pages.
  - Microsoft Word and Excel for Mac 16.115 (macOS 26.5) run under a Microsoft 365 Business Standard subscription;
    the licence was checked in each app's About dialog before the run (2026-11-15; `data/office-license.json`).
  - Word: the Word documents, exported one at a time by `factory/office_mac.py`
    (AppleScript; stops on any dialog and when Word sends more than telemetry). 36 of 37 documents, 206 pages; Word
    could not open one file without repairing it. Log: `data/word-render.jsonl`.
  - Excel: the spreadsheets, prepared by `factory/excel_prep.py` (only the sheets and print
    areas LibreOffice printed) and exported one at a time by `factory/office_mac.py --app excel` through the menus
    (Save As, PDF, whole workbook, "best for printing", which is the local export; Excel otherwise suggests its online
    service). Excel runs with the document's locale as a launch argument (`-AppleLocale`), not a system setting.
    42 of 45 workbooks, 171 pages. Log: `data/excel-render.jsonl`.
  - Word and Excel PDFs are kept with the same truth and the same checks (`build.py adopt`; `data/build-word.json`,
    `data/build-excel.json`, `data/manifest-*.json`, `data/pdf-*/`, `data/truth-*/`). Two adjustments for Excel, both
    logged per file: where Excel rounds a General-format number to the column width, the rounded display of the same
    original value is used; where Excel breaks pages differently, the per-page truth blocks are recomputed from the
    original's cell grid (`build.py grids`) by matching each Excel page, then checked as before.
- The truth comes from the original file, not from the PDF:
  - XLSX: every visible cell of the printed sheets as the spreadsheet displays it (number formats applied), with its
    cell type (number or text). One truth table per printed page, in print order: a wide sheet prints its columns on
    several pages, so a converter sees several tables. A sheet is kept only if it has as many non-empty page blocks as
    printed pages and each block is at least 90 % on its own page.
  - DOCX: paragraphs and tables in document order, read from `word/document.xml` (merged cells: value in the first
    cell). Headers, footers and footnotes are not part of the truth.
- A file is kept only if at least 97 % of its truth words appear in the PDF's text layer (so cut-off cells such as
  `###` do not count against a converter), it prints to at most 20 pages and has no tracked changes.
  Conversely, at least 85 % of the PDF's words must be in the truth (catches sheets that could not be hidden,
  chart labels and floating text boxes). `data/build*.json` list every original and why it was dropped. 45
  spreadsheets and 37 Word documents remain; 28,688 truth cells, 14,351 of them numeric (LibreOffice set).

## Metrics

All candidates are scored by the same code (`eval/`, standard library only). Pipe tables and HTML tables are parsed
into the same grid; `python3 -I eval/mdparse.py --selfcheck` checks that.

| Metric | Definition |
|---|---|
| Numbers in the right cell | Numeric truth cells found in the matching row and column of an output table. Truth rows are matched to output rows by shared cells (monotone alignment, at least 30 % overlap, across all output tables); columns by majority vote within the matched rows, one to one. Numbers are compared without thousands and decimal separators. Output without tables scores 0 here. |
| Corrupted numbers | Numbers in the output that do not stand in the original like that: torn apart (`2` split off `CaCl2`), glued together (`65 280` from two cells), repeated, or new. Counted as number tokens that occur more often in the output than in the truth and the PDF's own text layer together. |
| Word recall | Share of the truth's tokens found in the output, regardless of order (multiset). |
| Reading order | Longest common token subsequence between output and truth, divided by the tokens they share regardless of order. |
| Time per page | Wall time per document divided by its pages, one document at a time. Open tools: 4 CPU cores, no network, Python libraries already loaded, on a shared server. switchfile and CloudConvert: through their public APIs, including upload, queueing and network. Compare orders of magnitude within each group, not across groups. |

Means and cell sums come with 95 % bootstrap intervals clustered by source document: all renderings of one original
(LibreOffice, Word or Excel) are drawn together, because they are not independent; the same holds for the paired
per-file difference against the first candidate. Numbers in the right cell are reported two ways with equal weight:
the mean per file (every document counts once) and the sum over all numeric cells (a few large tables carry most
cells). Results are reported for Word, Excel and LibreOffice PDFs side by side and split by country, format and
language. Every candidate gets one attempt per PDF with a limit of 600 s; a PDF without output counts as a failure and
scores 0. Full report: [RESULTS.md](RESULTS.md); outputs in `results/outputs/` (LibreOffice), `results/outputs-word/`
and `results/outputs-excel/`; per-file scores in `results/scores-2026-11-16-all.json`; run windows in `results/runs.json`.

## Results (2026-11-16)

Numbers in the right cell, in percent: mean per file (every PDF counts once) and summed over all numeric cells (large
tables count more), with 95 % intervals for all PDFs; per producer as per file \| summed. Failures count as 0.

<!-- RESULTS-TABLE -->
| Candidate | all PDFs, per file | all PDFs, summed | Word PDFs | Excel PDFs | LibreOffice PDFs | failed |
|---|---:|---:|---:|---:|---:|---:|
| switchfile | 94.1 [90.7; 97.1] | 97.2 [95.6; 98.7] | 98.9 \| 99.5 | 93.1 \| 99.4 | 93.7 \| 95.1 | 0 |
| CloudConvert | 82.6 [75.1; 89.3] | 68.4 [38.0; 95.5] | 97.9 \| 97.3 | 79.9 \| 65.9 | 80.7 \| 67.6 | 0 |
| pymupdf4llm | 81.6 [74.0; 88.4] | 68.3 [37.9; 95.3] | 97.7 \| 97.2 | 79.9 \| 65.9 | 78.7 \| 67.3 | 0 |
| Docling | 67.6 [56.7; 77.9] | 57.2 [29.3; 86.6] | 98.9 \| 99.5 | 59.0 \| 53.6 | 65.7 \| 56.0 | 0 |
| pdfplumber + our wrapper | 48.5 [35.8; 61.5] | 48.1 [20.6; 79.2] | 58.8 \| 67.1 | 41.2 \| 45.7 | 50.9 \| 48.4 | 0 |
| markitdown | 36.9 [26.8; 47.1] | 39.7 [21.3; 64.2] | 41.7 \| 56.9 | 39.7 \| 39.0 | 33.8 \| 38.5 | 0 |
| pdftotext (baseline) | 0.0 [0.0; 0.0] | 0.0 [0.0; 0.0] | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 | 0 |
<!-- /RESULTS-TABLE -->

Corrupted numbers, word recall, reading order, time per page, paired differences and the split by country, format
and language: [RESULTS.md](RESULTS.md). These results hold for these documents, versions and the date stated; see
[Disclaimer](#disclaimer).

## Candidates

`candidates/run.py <name> <pdf-dir> <out-dir>` runs one candidate on all PDFs. Pinned versions of the open tools are
in `candidates/Dockerfile`; each candidate runs with its default settings. All candidates were run on 2026-11-16.

| Candidate | Version | License |
|---|---|---|
| switchfile (`pdf → md`) | public API, production as measured on 2026-11-16, 12:36–12:42 UTC | proprietary service of Aura UG (haftungsbeschränkt), the publisher |
| CloudConvert (PDF to Markdown API, `output_format: md`) | public API, measured 2026-11-16 | proprietary service of Lunaweb GmbH; run by us through its public API with default settings |
| Docling | 2.150.1 | MIT; models Apache-2.0 / CDLA-Permissive-2.0 / MIT |
| markitdown | 0.1.9 | MIT |
| PyMuPDF (`pymupdf4llm.to_markdown`) | 2.1 | AGPL-3.0 or Artifex commercial (measured, not bundled) |
| pdfplumber, with a minimal Markdown wrapper (ours) | 0.11.10 | MIT |
| pdftotext (Poppler), baseline: plain text, no table output | 25.03.0 | GPL-2.0 or GPL-3.0 (core library) |

switchfile and CloudConvert were measured through their public APIs from one client on the same day
(`candidates/run.py switchfile`, needs `SWITCHFILE_API_KEY`; `candidates/run.py cloudconvert`, needs
`CLOUDCONVERT_API_KEY`). CloudConvert runs one job per PDF with `input_format: pdf`, `output_format: md` and no other
options; the date and the engine name and version that its API reported for each PDF are in
`results/cloudconvert-tasks.json`. Both services have no version numbers and can change; the outputs in `results/`
show what each returned on that date. Their time per page includes upload, queueing and network and is not comparable
with the open tools. pdftotext starts one process per document; its time includes start-up.

pdfplumber has no Markdown writer; the minimal wrapper we wrote in `candidates/run.py` writes its default table
finder's tables as pipe tables and the remaining text lines in page order. pdftotext writes plain text without tables;
it is listed as a baseline for word recall and reading order, not as a competitor, and is left out of the paired
comparison.

## Reproduce

```bash
python3 -I factory/discover.py 20261115 data/candidates.json
python3 -I factory/fetch.py data/candidates.json work/originals data/fetched.json
docker build -t bench-factory factory
docker run --rm --network none -v "$PWD:/d" bench-factory python3 -I /d/factory/build.py \
  /d/data/fetched.json /d/work/originals /d/work/set 4   # second draw: data/fetched2.json
docker build -t bench-candidates candidates
docker run --rm --network none --cpus 4 -v "$PWD:/d" bench-candidates \
  /opt/docling/bin/python -I /d/candidates/run.py docling /d/work/set /d/work/out/docling
python3 -I factory/remove.py data/removed.json   # removed originals, see Data
python3 -I candidates/run.py switchfile work/set work/out/switchfile       # public API, SWITCHFILE_API_KEY
python3 -I candidates/run.py cloudconvert work/set work/out/cloudconvert   # public API, CLOUDCONVERT_API_KEY
python3 -I eval/score.py work/set work/out switchfile,cloudconvert,pymupdf4llm,docling,pdfplumber,markitdown,pdftotext scores.json
python3 -I eval/report.py scores.json all,format=xlsx,format=docx
```

Draws 3 and 4 (German and UK spreadsheets): `discover.py 20261117 data/candidates3.json <exclusions> xlsx
uk,govdata,hamburg 150 data/manifest.json` (seed 20261118, 400 for draw 4), fetch as above, then `build.py` with
`-e BENCH_CROP_PAGES=4`.

Word and Excel PDFs (on a Mac with Office, German menus): `python3 factory/office_mac.py in out` for the DOCX
originals; `factory/excel_prep.py data/manifest.json work/originals work/xprep`, then per language
`python3 factory/office_mac.py --app excel --locale fr_FR work/xprep-fr out` (de_DE, en_GB). In the factory container:
`build.py grids data/manifest.json work/originals work/grid`, then `build.py adopt <manifest> <out> data/truth
work/set-excel work/grid`. Scores over all producers: `eval/combine.py work/all work/out-all
libreoffice,data/manifest.json,data/pdf,data/truth,work/out word,data/manifest-word.json,data/pdf-word,data/truth-word,work/out-word,-msword
excel,data/manifest-excel.json,data/pdf-excel,data/truth-excel,work/out-excel,-msexcel`, then `score.py` on `work/all`.

Catalog contents change over time; `data/fetched.json` pins the exact files by URL and SHA-256. `DATA-SOURCES.md`:
`factory/attribution.py fetch data/manifest.json data/attribution.json` (catalog metadata), then
`factory/attribution.py data/manifest.json data/attribution.json DATA-SOURCES.md`.

## Who publishes this

This benchmark is published by Aura UG (haftungsbeschränkt), Hamburg, Germany, the company that makes switchfile,
one of the candidates. We chose the data, wrote the scoring code and ran every candidate ourselves, switchfile
included. switchfile was developed with test documents of a similar kind (public office files from the same
portals); the report shows where that may have helped it. The data, every output and the scoring code are in this
repository so that anyone can check the results.

Contact: hello@switchfile.io. Legal notice (Impressum): https://switchfile.io/imprint

## Disclaimer

Results describe the listed versions with default settings on this data set on the date stated. Other documents,
versions or settings can give different results. They are not a general statement about the quality of any
project. pdfplumber is measured through a minimal Markdown wrapper written by us; pdftotext writes plain text and is
listed as a baseline only.

Product names are trademarks of their owners. They are used here to identify the software measured and do not imply
endorsement by or affiliation with their owners. switchfile is not affiliated with CloudConvert or Lunaweb GmbH. Logos, crests and trade marks inside the documents belong to their
owners and are not licensed by this repository. The publishers of the original documents do not endorse this
benchmark.

The code is provided under the MIT License without warranty. The documents and derived files are provided as is,
under the license of each original ([DATA-SOURCES.md](DATA-SOURCES.md)).

## Corrections and removal

If you maintain a candidate and think a result is wrong, open an issue. If you hold rights in one of the documents,
or are named in one and want it removed, write to hello@switchfile.io (or open an issue without personal details).
We answer within 30 days.

## License

- Code (`eval/`, `factory/`, `candidates/`): MIT ([LICENSE](LICENSE)).
- Scores and reports written by us (`results/scores-*.json`, `RESULTS.md`, this README): CC BY 4.0
  (https://creativecommons.org/licenses/by/4.0/), credit "Aura UG (haftungsbeschränkt), PDF to Markdown benchmark".
- PDFs, truth files and candidate outputs (`data/pdf*/`, `data/truth*/`, `results/outputs*/`): the license of each
  original, listed with its attribution in [DATA-SOURCES.md](DATA-SOURCES.md).
