# Results: business PDF → Markdown, table cells and corrupted numbers (measured 2026-11-16, scored 2026-11-18)

Published by Aura UG (haftungsbeschränkt), the company that makes switchfile, one of the candidates. We chose the
data, wrote the scoring code and ran every candidate ourselves, switchfile included. Scope and limits: README and
"Limitations and bias" below.

## Summary

- **Data:** 82 public originals (45 XLSX, 37 DOCX) from France (data.gouv.fr), Germany (GovData, Hamburg transparency
  portal), the United Kingdom (data.gov.uk) and Zenodo (international); 28,688 truth cells, 14,417 of them scored as
  numbers (LibreOffice set). Numeric cells by country: FR 41 %, DE 39 %, UK 11 %, international 9 %; 65 % of the German
  numeric cells come from one workbook. 2 originals were removed after a privacy review (`data/removed.json`); all
  numbers here are computed without them.
- **160 PDFs, 781 pages, two producer families:** Microsoft Office for Mac 16.115 under Microsoft 365 Business
  Standard, Word for 36 of 37 DOCX (206 pages) and Excel for 42 of 45 XLSX (171 pages); LibreOffice 25.2 for all 82
  originals (404 pages). Same truth from the original, same checks.
- **Measurement (2026-11-16):** switchfile and CloudConvert through their public APIs over the internet (2026-11-16
  12:36–12:42 and 2026-11-16 09:52–10:00 UTC); the open tools at pinned versions in a container on a server with 4 CPU
  cores and no network (2026-11-16 09:52–11:45 UTC). Every candidate gets one attempt per PDF with a limit of 600 s; a
  PDF without output counts as a failure and scores 0 everywhere.
- **Numbers in the right cell** (percent; mean per file and summed over all numeric cells, equal weight; all PDFs with
  95 % interval, bootstrap clustered by source document; failures count as 0):

  | Candidate | all, per file | all, summed | Word PDFs | Excel PDFs | LibreOffice PDFs | failed |
  |---|---:|---:|---:|---:|---:|---:|
  | switchfile | 93.8 [90.5; 96.7] | 97.2 [95.5; 98.6] | 98.9 \| 99.5 | 92.6 \| 99.4 | 93.4 \| 95.0 | 0 |
  | CloudConvert | 82.3 [74.8; 89.1] | 68.1 [37.9; 94.9] | 97.9 \| 97.3 | 77.3 \| 65.4 | 81.9 \| 67.5 | 0 |
  | pymupdf4llm | 81.3 [73.7; 88.1] | 68.0 [37.8; 94.7] | 97.7 \| 97.2 | 77.3 \| 65.4 | 79.9 \| 67.2 | 0 |
  | Docling | 67.9 [57.0; 78.3] | 57.1 [29.4; 86.4] | 98.9 \| 99.5 | 59.7 \| 53.5 | 65.9 \| 56.0 | 0 |
  | pdfplumber + our wrapper | 49.1 [36.4; 62.0] | 48.1 [20.7; 78.9] | 58.8 \| 67.1 | 42.0 \| 45.7 | 51.5 \| 48.3 | 0 |
  | markitdown | 36.7 [26.7; 46.9] | 39.5 [21.2; 63.8] | 41.7 \| 56.9 | 39.2 \| 38.9 | 33.8 \| 38.4 | 0 |
  | pdftotext (baseline) | 0.0 [0.0; 0.0] | 0.0 [0.0; 0.0] | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 | 0 |

  Word, Excel and LibreOffice columns: per file \| summed. Numeric cells: Word 1,463, Excel 12,573, LibreOffice 14,417
  (28,453 in all). pdftotext is a baseline only: plain text, no table output. pdfplumber has no Markdown writer and is
  measured through a minimal wrapper written by us.

- **Failures:** none; every candidate returned output for every PDF.
- **Paired difference, switchfile minus candidate** (points per file on the same PDFs with numeric cells, 95 %
  interval clustered by source document; in brackets: switchfile higher / equal / lower):

  | Candidate | all | Microsoft Office PDFs | LibreOffice PDFs |
  |---|---:|---:|---:|
  | CloudConvert | +11.5 [+5.7; +18.4] (41/48/13) | +11.5 [+2.4; +20.9] (20/25/4) | +11.5 [+4.0; +20.4] (21/23/9) |
  | pymupdf4llm | +12.6 [+6.6; +19.5] (42/48/12) | +11.6 [+2.5; +20.9] (20/26/3) | +13.5 [+5.3; +22.8] (22/22/9) |
  | Docling | +25.9 [+16.8; +35.8] (52/44/6) | +24.2 [+13.1; +36.0] (22/26/1) | +27.5 [+16.9; +38.7] (30/18/5) |
  | pdfplumber + our wrapper | +44.8 [+32.8; +56.7] (55/45/2) | +47.8 [+34.6; +61.0] (29/20/0) | +41.9 [+30.0; +54.3] (26/25/2) |
  | markitdown | +57.1 [+46.1; +67.6] (88/12/2) | +54.4 [+41.6; +66.8] (41/6/2) | +59.6 [+49.2; +69.7] (47/6/0) |

- **Same originals, different producer:** on the same 36 XLSX originals with numeric cells, switchfile changes by −0.4
  [−8.6; +6.6] points per file when Excel instead of LibreOffice prints them (interval includes 0); switchfile minus
  pymupdf4llm is +21.0 [+9.9; +34.0] on LibreOffice and +15.3 [+3.1; +27.6] on Excel PDFs, switchfile minus
  CloudConvert +18.2 [+7.8; +30.4] and +15.3 [+3.1; +27.6]. On 13 DOCX originals with numeric cells, switchfile minus
  Docling on Word PDFs is +0.0 [+0.0; +0.0], minus pymupdf4llm +1.2 [+0.0; +3.6], minus CloudConvert +0.9 [−0.8;
  +3.6]. Table below.
- **Numbers in the right cell by country** (all producers, per file \| summed):

  | Candidate | FR (54) | DE (39) | UK (28) | international (39) |
  |---|---:|---:|---:|---:|
  | switchfile | 92.5 \| 99.3 | 83.4 \| 93.8 | 99.6 \| 99.0 | 99.9 \| 99.8 |
  | CloudConvert | 80.7 \| 94.2 | 75.6 \| 28.5 | 76.7 \| 85.4 | 98.3 \| 96.8 |
  | pymupdf4llm | 80.7 \| 94.2 | 75.2 \| 28.5 | 72.5 \| 84.1 | 98.3 \| 96.8 |
  | Docling | 62.5 \| 84.8 | 50.7 \| 15.4 | 63.3 \| 65.4 | 99.6 \| 99.3 |
  | pdfplumber + our wrapper | 52.7 \| 84.6 | 26.3 \| 4.1 | 54.2 \| 50.3 | 59.8 \| 66.9 |
  | markitdown | 37.7 \| 53.5 | 33.0 \| 10.9 | 26.6 \| 64.9 | 50.4 \| 66.6 |
  | pdftotext (baseline) | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 |

- **Corrupted numbers** (numbers that do not stand in the original like that: torn apart, glued together, repeated or
  new; definition under Method), total over all PDFs (files affected): switchfile 28 (8), CloudConvert 732 (37),
  pymupdf4llm 370 (27), Docling 492 (39), pdfplumber + our wrapper 417 (25), markitdown 178 (17). Per producer: tables
  below.
- **Time per page:** open tools in the container (4 cores, no network, shared server): pymupdf4llm 0.88 s, Docling
  13.90 s, pdfplumber + our wrapper 0.18 s, markitdown 0.26 s, pdftotext (baseline) 0.01 s (Docling without GPU).
  Through the public APIs, including upload, queueing and download over the internet from one client in Germany:
  switchfile 0.47 s, CloudConvert 0.62 s. The two groups are not comparable with each other.

## Same originals, different producer

Numbers in the right cell, mean per file, on the same 36 XLSX originals (LibreOffice vs Excel PDF) and
13 DOCX originals (LibreOffice vs Word PDF); 95 % bootstrap over originals.

| Candidate | XLSX LibreOffice | XLSX Excel | Excel − LibreOffice | switchfile − candidate, XLSX LibreOffice | switchfile − candidate, XLSX Excel | switchfile − candidate, DOCX LibreOffice | switchfile − candidate, DOCX Word |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.0 | 92.6 | −0.4 [−8.6; +6.6] | – | – | – | – |
| CloudConvert | 74.8 | 77.3 | +2.6 [−8.8; +14.9] | +18.2 [+7.8; +30.4] | +15.3 [+3.1; +27.6] | +1.3 [−0.9; +3.8] | +0.9 [−0.8; +3.6] |
| pymupdf4llm | 72.0 | 77.3 | +5.3 [−6.9; +18.7] | +21.0 [+9.9; +34.0] | +15.3 [+3.1; +27.6] | +1.6 [−0.2; +3.9] | +1.2 [+0.0; +3.6] |
| Docling | 51.9 | 59.7 | +7.8 [−4.7; +20.6] | +41.1 [+27.8; +54.7] | +33.0 [+18.7; +47.6] | +3.7 [+0.0; +10.1] | +0.0 [+0.0; +0.0] |
| pdfplumber + our wrapper | 46.8 | 42.0 | −4.7 [−12.1; +0.0] | +46.3 [+31.3; +61.0] | +50.6 [+35.1; +65.9] | +38.3 [+15.2; +63.0] | +40.1 [+16.1; +64.8] |
| markitdown | 30.5 | 39.2 | +8.7 [+3.7; +14.3] | +62.5 [+49.8; +74.5] | +53.5 [+37.0; +68.3] | +56.2 [+33.4; +78.9] | +57.2 [+35.2; +78.6] |
| pdftotext (baseline) | 0.0 | 0.0 | +0.0 [+0.0; +0.0] | – | – | – | – |

## Results by producer, country and format

"Right cell, mean per file" and "all cells": numbers in the right cell averaged per file or summed over all numeric
cells (hits/numeric cells); corrupted numbers as total (files); word recall and reading order as mean per file; time
per page as total/total (median per file; API services include network); 95 % bootstrap clustered by source
document. Per-file values: `results/scores-2026-11-18-all.json` (Word files end in `-msword`, Excel files in `-msexcel`).

**all**: 160 files, 781 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.8 [90.5–96.7] | 97.2 [95.5–98.6] (27649/28453) | 28 (8) | 99.5 [99.3–99.7] | 98.9 [97.9–99.6] | 0.47 (0.59) | 0 |
| cloudconvert | 82.3 [74.8–89.1] | 68.1 [37.9–94.9] (19387/28453) | 732 (37) | 98.3 [97.6–98.8] | 98.1 [97.1–99.0] | 0.62 (0.75) | 0 |
| pymupdf4llm | 81.3 [73.7–88.1] | 68.0 [37.8–94.7] (19343/28453) | 370 (27) | 98.3 [97.6–98.9] | 98.1 [97.1–99.0] | 0.88 (0.74) | 0 |
| Docling | 67.9 [57.0–78.3] | 57.1 [29.4–86.4] (16258/28453) | 492 (39) | 98.2 [96.8–99.2] | 97.3 [96.2–98.3] | 13.90 (10.62) | 0 |
| pdfplumber + our wrapper | 49.1 [36.4–62.0] | 48.1 [20.7–78.9] (13691/28453) | 417 (25) | 98.2 [97.1–99.1] | 98.4 [96.9–99.5] | 0.18 (0.13) | 0 |
| markitdown | 36.7 [26.7–46.9] | 39.5 [21.2–63.8] (11253/28453) | 178 (17) | 98.6 [97.6–99.4] | 87.8 [83.0–92.0] | 0.26 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/28453) | 0 (0) | 99.8 [99.7–99.9] | 79.5 [73.9–84.8] | 0.01 (0.01) | 0 |

**producer=word**: 36 files, 206 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 98.9 [96.6–100.0] | 99.5 [97.6–100.0] (1455/1463) | 19 (4) | 99.5 [99.2–99.8] | 99.6 [99.2–99.8] | 0.44 (0.65) | 0 |
| Docling | 98.9 [96.6–100.0] | 99.5 [97.6–100.0] (1455/1463) | 78 (8) | 99.6 [99.4–99.8] | 99.4 [98.9–99.8] | 10.02 (6.40) | 0 |
| cloudconvert | 97.9 [94.7–100.0] | 97.3 [92.2–100.0] (1424/1463) | 152 (7) | 99.5 [99.2–99.7] | 99.7 [99.4–99.9] | 0.55 (0.77) | 0 |
| pymupdf4llm | 97.7 [94.2–100.0] | 97.2 [91.9–100.0] (1422/1463) | 8 (3) | 99.5 [99.2–99.7] | 99.7 [99.4–99.9] | 0.74 (0.64) | 0 |
| pdfplumber + our wrapper | 58.8 [33.7–83.2] | 67.1 [25.8–93.2] (981/1463) | 25 (6) | 99.5 [99.2–99.8] | 98.5 [95.8–99.9] | 0.21 (0.16) | 0 |
| markitdown | 41.7 [20.7–62.9] | 56.9 [24.3–74.7] (832/1463) | 25 (8) | 99.8 [99.7–99.9] | 94.7 [89.7–98.3] | 0.32 (0.34) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/1463) | 0 (0) | 99.7 [99.5–99.8] | 96.1 [91.8–99.1] | 0.01 (0.02) | 0 |

**producer=excel**: 42 files, 171 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 92.6 [85.4–98.1] | 99.4 [98.2–99.8] (12492/12573) | 7 (2) | 99.6 [99.3–99.9] | 98.5 [97.3–99.5] | 0.55 (0.63) | 0 |
| cloudconvert | 77.3 [65.7–87.8] | 65.4 [32.6–95.8] (8227/12573) | 184 (11) | 96.6 [95.1–98.0] | 96.8 [94.7–98.5] | 0.72 (0.78) | 0 |
| pymupdf4llm | 77.3 [65.7–87.8] | 65.4 [32.6–95.8] (8227/12573) | 184 (11) | 96.6 [95.1–98.0] | 96.8 [94.7–98.5] | 1.03 (0.89) | 0 |
| Docling | 59.7 [44.9–74.1] | 53.5 [23.3–86.0] (6724/12573) | 186 (9) | 96.1 [91.8–99.4] | 95.2 [93.0–97.2] | 20.78 (16.79) | 0 |
| pdfplumber + our wrapper | 42.0 [26.5–58.0] | 45.7 [14.7–80.7] (5740/12573) | 250 (9) | 97.0 [94.0–99.2] | 98.7 [97.4–99.7] | 0.17 (0.13) | 0 |
| markitdown | 39.2 [26.9–52.0] | 38.9 [19.0–67.4] (4886/12573) | 58 (2) | 98.6 [96.2–99.9] | 81.8 [74.2–88.8] | 0.27 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/12573) | 0 (0) | 99.9 [99.7–100.0] | 61.6 [53.8–69.5] | 0.02 (0.02) | 0 |

**producer=libreoffice**: 82 files, 404 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.4 [89.7–96.5] | 95.0 [92.2–97.9] (13702/14417) | 2 (2) | 99.4 [99.1–99.7] | 98.8 [97.4–99.6] | 0.46 (0.57) | 0 |
| cloudconvert | 81.9 [73.3–89.4] | 67.5 [37.9–94.6] (9736/14417) | 396 (19) | 98.6 [97.9–99.1] | 98.1 [97.0–99.0] | 0.62 (0.74) | 0 |
| pymupdf4llm | 79.9 [70.9–88.1] | 67.2 [37.7–94.2] (9694/14417) | 178 (13) | 98.6 [98.0–99.2] | 98.1 [97.0–99.0] | 0.89 (0.73) | 0 |
| Docling | 65.9 [54.3–77.0] | 56.0 [28.6–85.1] (8079/14417) | 228 (22) | 98.6 [97.6–99.3] | 97.4 [96.0–98.6] | 12.97 (9.58) | 0 |
| pdfplumber + our wrapper | 51.5 [38.6–64.4] | 48.3 [21.3–78.9] (6970/14417) | 142 (10) | 98.3 [97.2–99.2] | 98.2 [96.6–99.4] | 0.16 (0.12) | 0 |
| markitdown | 33.8 [23.7–44.3] | 38.4 [20.4–61.8] (5535/14417) | 95 (7) | 98.0 [96.5–99.2] | 87.9 [83.1–92.1] | 0.22 (0.19) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/14417) | 0 (0) | 99.8 [99.7–99.9] | 81.3 [76.0–86.4] | 0.01 (0.01) | 0 |

**family=office**: 78 files, 377 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 94.3 [88.9–98.4] | 99.4 [98.4–99.8] (13947/14036) | 26 (6) | 99.6 [99.4–99.8] | 99.0 [98.3–99.5] | 0.49 (0.63) | 0 |
| cloudconvert | 82.8 [73.8–90.8] | 68.8 [37.7–96.1] (9651/14036) | 336 (18) | 97.9 [97.0–98.7] | 98.1 [96.9–99.0] | 0.62 (0.77) | 0 |
| pymupdf4llm | 82.7 [73.8–90.7] | 68.7 [37.7–96.1] (9649/14036) | 192 (14) | 97.9 [97.0–98.7] | 98.1 [96.9–99.0] | 0.87 (0.75) | 0 |
| Docling | 70.1 [57.9–81.6] | 58.3 [29.7–88.3] (8179/14036) | 264 (17) | 97.7 [95.4–99.5] | 97.1 [95.8–98.3] | 14.90 (11.53) | 0 |
| pdfplumber + our wrapper | 46.5 [33.1–60.3] | 47.9 [19.7–79.6] (6721/14036) | 275 (15) | 98.2 [96.5–99.4] | 98.6 [97.1–99.6] | 0.20 (0.14) | 0 |
| markitdown | 39.8 [29.4–50.7] | 40.7 [21.7–65.8] (5718/14036) | 83 (10) | 99.2 [97.8–99.9] | 87.8 [82.8–92.1] | 0.29 (0.24) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/14036) | 0 (0) | 99.8 [99.7–99.9] | 77.5 [71.5–83.1] | 0.01 (0.02) | 0 |

**family=libreoffice**: 82 files, 404 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.4 [89.7–96.5] | 95.0 [92.2–97.9] (13702/14417) | 2 (2) | 99.4 [99.1–99.7] | 98.8 [97.4–99.6] | 0.46 (0.57) | 0 |
| cloudconvert | 81.9 [73.3–89.4] | 67.5 [37.9–94.6] (9736/14417) | 396 (19) | 98.6 [97.9–99.1] | 98.1 [97.0–99.0] | 0.62 (0.74) | 0 |
| pymupdf4llm | 79.9 [70.9–88.1] | 67.2 [37.7–94.2] (9694/14417) | 178 (13) | 98.6 [98.0–99.2] | 98.1 [97.0–99.0] | 0.89 (0.73) | 0 |
| Docling | 65.9 [54.3–77.0] | 56.0 [28.6–85.1] (8079/14417) | 228 (22) | 98.6 [97.6–99.3] | 97.4 [96.0–98.6] | 12.97 (9.58) | 0 |
| pdfplumber + our wrapper | 51.5 [38.6–64.4] | 48.3 [21.3–78.9] (6970/14417) | 142 (10) | 98.3 [97.2–99.2] | 98.2 [96.6–99.4] | 0.16 (0.12) | 0 |
| markitdown | 33.8 [23.7–44.3] | 38.4 [20.4–61.8] (5535/14417) | 95 (7) | 98.0 [96.5–99.2] | 87.9 [83.1–92.1] | 0.22 (0.19) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/14417) | 0 (0) | 99.8 [99.7–99.9] | 81.3 [76.0–86.4] | 0.01 (0.01) | 0 |

**country=FR**: 54 files, 246 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 92.5 [86.7–97.5] | 99.3 [97.1–99.8] (11666/11754) | 1 (1) | 99.7 [99.5–99.9] | 97.9 [95.1–99.7] | 0.49 (0.59) | 0 |
| cloudconvert | 80.7 [68.1–91.5] | 94.2 [85.3–98.3] (11078/11754) | 232 (12) | 97.6 [96.2–98.7] | 98.1 [96.5–99.3] | 0.66 (0.77) | 0 |
| pymupdf4llm | 80.7 [68.1–91.5] | 94.2 [85.3–98.3] (11078/11754) | 232 (12) | 97.6 [96.2–98.7] | 98.1 [96.5–99.3] | 0.98 (0.76) | 0 |
| Docling | 62.5 [44.0–79.6] | 84.8 [54.2–95.1] (9964/11754) | 88 (10) | 97.4 [94.4–99.6] | 97.0 [94.8–98.8] | 16.40 (10.15) | 0 |
| pdfplumber + our wrapper | 52.7 [30.7–73.7] | 84.6 [47.9–97.0] (9941/11754) | 152 (7) | 98.1 [96.1–99.5] | 98.6 [96.7–99.9] | 0.12 (0.08) | 0 |
| markitdown | 37.7 [22.7–54.0] | 53.5 [39.2–76.6] (6293/11754) | 137 (6) | 97.9 [95.7–99.5] | 95.2 [92.2–97.9] | 0.23 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/11754) | 0 (0) | 99.8 [99.6–99.9] | 76.7 [67.4–85.7] | 0.01 (0.01) | 0 |

**country=DE**: 39 files, 197 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 83.4 [73.5–91.7] | 93.8 [83.3–95.6] (10295/10974) | 16 (3) | 99.4 [98.9–99.8] | 99.5 [99.0–99.9] | 0.45 (0.51) | 0 |
| cloudconvert | 75.6 [56.4–91.4] | 28.5 [7.3–93.9] (3133/10974) | 85 (6) | 98.5 [97.6–99.3] | 98.8 [98.2–99.4] | 0.58 (0.64) | 0 |
| pymupdf4llm | 75.2 [56.2–91.0] | 28.5 [7.3–93.7] (3129/10974) | 83 (5) | 98.5 [97.6–99.3] | 98.8 [98.2–99.4] | 0.89 (0.75) | 0 |
| Docling | 50.7 [28.5–73.9] | 15.4 [3.4–64.7] (1693/10974) | 149 (13) | 97.2 [93.5–99.4] | 96.7 [94.7–98.5] | 10.90 (9.12) | 0 |
| markitdown | 33.0 [12.9–54.3] | 10.9 [1.3–49.9] (1200/10974) | 2 (2) | 98.5 [96.3–99.9] | 88.9 [80.4–95.3] | 0.24 (0.19) | 0 |
| pdfplumber + our wrapper | 26.3 [3.8–52.0] | 4.1 [0.5–32.4] (451/10974) | 119 (4) | 96.6 [92.8–99.2] | 98.1 [95.5–100.0] | 0.20 (0.17) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/10974) | 0 (0) | 99.8 [99.6–100.0] | 84.5 [75.5–92.5] | 0.01 (0.01) | 0 |

**country=UK**: 28 files, 88 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 99.6 [98.8–100.0] | 99.0 [96.6–100.0] (3165/3198) | 1 (1) | 99.3 [98.6–99.8] | 98.9 [97.6–99.8] | 0.65 (1.25) | 0 |
| cloudconvert | 76.7 [59.1–91.8] | 85.4 [61.5–95.8] (2730/3198) | 55 (4) | 97.4 [95.2–99.3] | 95.0 [90.3–98.8] | 0.89 (1.57) | 0 |
| pymupdf4llm | 72.5 [55.2–88.3] | 84.1 [57.8–94.9] (2690/3198) | 26 (3) | 97.6 [95.4–99.4] | 95.0 [90.3–98.8] | 0.97 (0.77) | 0 |
| Docling | 63.3 [41.4–83.8] | 65.4 [29.1–90.4] (2092/3198) | 122 (5) | 99.0 [97.9–99.8] | 95.5 [91.8–98.5] | 23.69 (18.14) | 0 |
| pdfplumber + our wrapper | 54.2 [25.0–79.2] | 50.3 [4.4–89.3] (1608/3198) | 122 (4) | 98.9 [97.9–99.7] | 99.5 [98.6–100.0] | 0.14 (0.10) | 0 |
| markitdown | 26.6 [5.0–50.0] | 64.9 [12.9–88.4] (2076/3198) | 0 (0) | 98.1 [95.8–100.0] | 64.9 [50.0–79.6] | 0.25 (0.21) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/3198) | 0 (0) | 99.9 [99.7–100.0] | 57.1 [44.5–70.3] | 0.02 (0.03) | 0 |

**country=INT**: 39 files, 250 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 99.9 [99.8–100.0] | 99.8 [99.5–100.0] (2523/2527) | 10 (3) | 99.5 [99.0–99.8] | 99.7 [99.4–99.9] | 0.42 (0.57) | 0 |
| Docling | 99.6 [99.0–100.0] | 99.3 [98.1–100.0] (2509/2527) | 133 (11) | 99.7 [99.5–99.8] | 99.6 [99.2–99.9] | 10.36 (7.22) | 0 |
| cloudconvert | 98.3 [95.4–100.0] | 96.8 [91.5–100.0] (2446/2527) | 360 (15) | 99.6 [99.3–99.7] | 99.7 [99.4–99.9] | 0.53 (0.64) | 0 |
| pymupdf4llm | 98.3 [95.4–100.0] | 96.8 [91.5–100.0] (2446/2527) | 29 (7) | 99.5 [99.3–99.7] | 99.7 [99.5–99.9] | 0.75 (0.69) | 0 |
| pdfplumber + our wrapper | 59.8 [31.2–88.4] | 66.9 [18.8–95.4] (1691/2527) | 24 (10) | 99.5 [99.0–99.8] | 97.5 [92.9–100.0] | 0.22 (0.19) | 0 |
| markitdown | 50.4 [26.7–74.2] | 66.6 [32.9–81.7] (1684/2527) | 39 (9) | 99.8 [99.7–99.9] | 93.0 [84.5–99.3] | 0.30 (0.28) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/2527) | 0 (0) | 99.8 [99.7–99.9] | 94.3 [86.7–99.5] | 0.01 (0.01) | 0 |

**format=xlsx**: 87 files, 348 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 92.1 [87.8–95.8] | 96.9 [94.8–98.6] (24712/25494) | 8 (3) | 99.5 [99.1–99.7] | 98.3 [96.5–99.5] | 0.55 (0.58) | 0 |
| cloudconvert | 76.8 [67.4–85.5] | 64.8 [32.7–94.5] (16525/25494) | 369 (20) | 97.2 [96.1–98.2] | 96.8 [94.9–98.4] | 0.74 (0.77) | 0 |
| pymupdf4llm | 75.5 [66.2–84.3] | 64.7 [32.7–94.3] (16485/25494) | 340 (19) | 97.3 [96.2–98.3] | 96.8 [94.9–98.4] | 1.09 (0.83) | 0 |
| Docling | 57.5 [45.0–70.1] | 52.4 [23.0–84.4] (13357/25494) | 335 (18) | 96.9 [94.5–98.8] | 95.5 [93.6–97.1] | 18.65 (13.21) | 0 |
| pdfplumber + our wrapper | 44.8 [30.2–59.8] | 45.8 [15.2–80.4] (11684/25494) | 374 (13) | 97.1 [95.0–98.7] | 98.3 [96.7–99.5] | 0.16 (0.11) | 0 |
| markitdown | 34.3 [22.9–46.4] | 37.3 [18.4–63.9] (9507/25494) | 136 (5) | 97.5 [95.8–99.0] | 81.7 [74.5–88.3] | 0.23 (0.17) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/25494) | 0 (0) | 99.9 [99.8–100.0] | 65.4 [58.4–72.4] | 0.01 (0.01) | 0 |

**format=docx**: 73 files, 433 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 98.7 [96.2–100.0] | 99.3 [97.3–100.0] (2937/2959) | 20 (5) | 99.6 [99.3–99.8] | 99.5 [99.1–99.8] | 0.42 (0.59) | 0 |
| cloudconvert | 97.7 [95.0–99.7] | 96.7 [92.4–99.6] (2862/2959) | 363 (17) | 99.5 [99.3–99.7] | 99.7 [99.4–99.9] | 0.52 (0.70) | 0 |
| pymupdf4llm | 97.4 [94.4–99.7] | 96.6 [92.1–99.6] (2858/2959) | 30 (8) | 99.5 [99.3–99.7] | 99.7 [99.4–99.9] | 0.72 (0.63) | 0 |
| Docling | 96.9 [91.3–100.0] | 98.0 [93.7–100.0] (2901/2959) | 157 (21) | 99.6 [99.5–99.8] | 99.4 [99.0–99.8] | 10.08 (5.99) | 0 |
| pdfplumber + our wrapper | 61.0 [35.4–84.5] | 67.8 [26.9–93.4] (2007/2959) | 43 (12) | 99.6 [99.3–99.8] | 98.5 [96.0–99.9] | 0.19 (0.16) | 0 |
| markitdown | 43.4 [22.8–64.1] | 59.0 [25.8–76.2] (1746/2959) | 42 (12) | 99.8 [99.7–99.9] | 95.1 [90.4–98.5] | 0.28 (0.29) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/2959) | 0 (0) | 99.7 [99.5–99.8] | 96.2 [92.1–99.1] | 0.01 (0.01) | 0 |

**lang=de**: 39 files, 197 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 83.4 [73.5–91.7] | 93.8 [83.3–95.6] (10295/10974) | 16 (3) | 99.4 [98.9–99.8] | 99.5 [99.0–99.9] | 0.45 (0.51) | 0 |
| cloudconvert | 75.6 [56.4–91.4] | 28.5 [7.3–93.9] (3133/10974) | 85 (6) | 98.5 [97.6–99.3] | 98.8 [98.2–99.4] | 0.58 (0.64) | 0 |
| pymupdf4llm | 75.2 [56.2–91.0] | 28.5 [7.3–93.7] (3129/10974) | 83 (5) | 98.5 [97.6–99.3] | 98.8 [98.2–99.4] | 0.89 (0.75) | 0 |
| Docling | 50.7 [28.5–73.9] | 15.4 [3.4–64.7] (1693/10974) | 149 (13) | 97.2 [93.5–99.4] | 96.7 [94.7–98.5] | 10.90 (9.12) | 0 |
| markitdown | 33.0 [12.9–54.3] | 10.9 [1.3–49.9] (1200/10974) | 2 (2) | 98.5 [96.3–99.9] | 88.9 [80.4–95.3] | 0.24 (0.19) | 0 |
| pdfplumber + our wrapper | 26.3 [3.8–52.0] | 4.1 [0.5–32.4] (451/10974) | 119 (4) | 96.6 [92.8–99.2] | 98.1 [95.5–100.0] | 0.20 (0.17) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/10974) | 0 (0) | 99.8 [99.6–100.0] | 84.5 [75.5–92.5] | 0.01 (0.01) | 0 |

**lang=en**: 67 files, 338 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 99.7 [99.3–100.0] | 99.4 [98.1–100.0] (5688/5725) | 11 (4) | 99.4 [99.0–99.7] | 99.3 [98.8–99.8] | 0.48 (0.59) | 0 |
| cloudconvert | 86.8 [75.7–95.7] | 90.4 [79.5–96.7] (5176/5725) | 415 (19) | 98.7 [97.6–99.5] | 97.7 [95.6–99.5] | 0.62 (0.77) | 0 |
| pymupdf4llm | 84.5 [73.1–94.1] | 89.7 [78.1–96.1] (5136/5725) | 55 (10) | 98.7 [97.7–99.5] | 97.8 [95.6–99.5] | 0.81 (0.72) | 0 |
| Docling | 80.3 [65.7–92.7] | 80.4 [57.4–95.4] (4601/5725) | 255 (16) | 99.4 [98.9–99.8] | 97.9 [96.1–99.2] | 13.83 (11.20) | 0 |
| pdfplumber + our wrapper | 56.8 [37.0–76.1] | 57.6 [18.0–84.6] (3299/5725) | 146 (14) | 99.3 [98.7–99.7] | 98.3 [95.6–99.9] | 0.20 (0.15) | 0 |
| markitdown | 37.7 [21.1–55.4] | 65.7 [36.7–82.2] (3760/5725) | 39 (9) | 99.1 [98.0–99.8] | 81.3 [72.0–89.8] | 0.28 (0.24) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/5725) | 0 (0) | 99.8 [99.7–99.9] | 78.7 [69.3–87.5] | 0.01 (0.01) | 0 |

**lang=fr**: 54 files, 246 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 92.5 [86.7–97.5] | 99.3 [97.1–99.8] (11666/11754) | 1 (1) | 99.7 [99.5–99.9] | 97.9 [95.1–99.7] | 0.49 (0.59) | 0 |
| cloudconvert | 80.7 [68.1–91.5] | 94.2 [85.3–98.3] (11078/11754) | 232 (12) | 97.6 [96.2–98.7] | 98.1 [96.5–99.3] | 0.66 (0.77) | 0 |
| pymupdf4llm | 80.7 [68.1–91.5] | 94.2 [85.3–98.3] (11078/11754) | 232 (12) | 97.6 [96.2–98.7] | 98.1 [96.5–99.3] | 0.98 (0.76) | 0 |
| Docling | 62.5 [44.0–79.6] | 84.8 [54.2–95.1] (9964/11754) | 88 (10) | 97.4 [94.4–99.6] | 97.0 [94.8–98.8] | 16.40 (10.15) | 0 |
| pdfplumber + our wrapper | 52.7 [30.7–73.7] | 84.6 [47.9–97.0] (9941/11754) | 152 (7) | 98.1 [96.1–99.5] | 98.6 [96.7–99.9] | 0.12 (0.08) | 0 |
| markitdown | 37.7 [22.7–54.0] | 53.5 [39.2–76.6] (6293/11754) | 137 (6) | 97.9 [95.7–99.5] | 95.2 [92.2–97.9] | 0.23 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/11754) | 0 (0) | 99.8 [99.6–99.9] | 76.7 [67.4–85.7] | 0.01 (0.01) | 0 |

Paired per file against switchfile, numbers in right cell, all (files with numeric cells):

| Candidate | Difference, points [95 % CI] | first better / equal / worse |
|---|---:|---:|
| cloudconvert | +11.5 [+5.7; +18.4] | 41 / 48 / 13 |
| pymupdf4llm | +12.6 [+6.6; +19.5] | 42 / 48 / 12 |
| Docling | +25.9 [+16.8; +35.8] | 52 / 44 / 6 |
| pdfplumber + our wrapper | +44.8 [+32.8; +56.7] | 55 / 45 / 2 |
| markitdown | +57.1 [+46.1; +67.6] | 88 / 12 / 2 |

Paired per file against switchfile, numbers in right cell, family=libreoffice (files with numeric cells):

| Candidate | Difference, points [95 % CI] | first better / equal / worse |
|---|---:|---:|
| cloudconvert | +11.5 [+4.0; +20.4] | 21 / 23 / 9 |
| pymupdf4llm | +13.5 [+5.3; +22.8] | 22 / 22 / 9 |
| Docling | +27.5 [+16.9; +38.7] | 30 / 18 / 5 |
| pdfplumber + our wrapper | +41.9 [+30.0; +54.3] | 26 / 25 / 2 |
| markitdown | +59.6 [+49.2; +69.7] | 47 / 6 / 0 |

Paired per file against switchfile, numbers in right cell, family=office (files with numeric cells):

| Candidate | Difference, points [95 % CI] | first better / equal / worse |
|---|---:|---:|
| cloudconvert | +11.5 [+2.4; +20.9] | 20 / 25 / 4 |
| pymupdf4llm | +11.6 [+2.5; +20.9] | 20 / 26 / 3 |
| Docling | +24.2 [+13.1; +36.0] | 22 / 26 / 1 |
| pdfplumber + our wrapper | +47.8 [+34.6; +61.0] | 29 / 20 / 0 |
| markitdown | +54.4 [+41.6; +66.8] | 41 / 6 / 2 |

## Third producer: Excel for Mac

- **Process:** `factory/excel_prep.py` makes a copy of each workbook in which only the sheets LibreOffice printed are
  visible and cut sheets have the same print area. `factory/office_mac.py --app excel` opens each workbook in Excel for
  Mac 16.115 (macOS 26.5.2) and saves it through "Save As … → PDF" as the whole workbook. It drives the menus (System
  Events), reads back every setting in the dialog before saving, holds the same lock as for Word, stops on any
  unexpected dialog and measures Excel's network traffic. Log: `data/excel-render.jsonl`.
- **Local export only:** the dialog suggests "Best for electronic distribution and accessibility (uses Microsoft
  online
  service)". The driver selects "Best for printing" and stops if that does not take. Measured: Excel sends telemetry when it
  opens and closes a workbook, also without any export (idle: 0 bytes) and independent of file size: 6–20 KB per
  workbook in the run used here, 52–63 KB in an earlier run. The threshold for Excel is 80 KB plus half the file size
  (Word: 20 KB); no workbook had to be redone.
- **Locale without a system setting:** Excel formats numbers by locale. The driver starts Excel per language with the
  launch argument `-AppleLocale de_DE | en_GB | fr_FR`; it applies to that Excel process only, the Mac's region stays
  unchanged. Checked on a French workbook: "5 118,00" as with LibreOffice.
- **Same truth, same checks, two adjustments to the producer's print** (`build.py adopt`, reasons and counts in
  `data/build-excel.json`):
  - *Rounding:* Excel shows General-format numbers with as many digits as the column holds (4.565122265 instead of
    LibreOffice's 4.56512226512227). If a numeric cell is not in the text layer but a rounding of exactly its original
    value is, the rounded display counts for this PDF (1 file, 7 cells). The value never comes from the PDF.
  - *Page blocks:* the XLSX truth is split per printed page. Where Excel breaks pages differently, the blocks are
    recomputed from the original's cell grid (`build.py grids`) along Excel's pages: page by page, the columns and rows
    whose cells stand on that page, each word of the page used once. The same per-page check (≥ 90 %) follows.
    Recomputed this way: 17 workbooks; three of them checked by eye (first and last row of each block against the
    page).
- **Dropped (3):** `de-xlsx-76a7055067`, `de-xlsx-4f4e6a3538`, `de-xlsx-fa2af86144`: Excel's pages do not map onto
  blocks of the original unambiguously ("page blocks do not match the producer's print").


## Second producer: Word for Mac

- **Process:** `factory/office_mac.py` on a Mac with Word 16.115 (macOS 26.5.2): open one document at a time, save as
  PDF, close. The driver holds a lock against parallel use of Word, stops on any dialog and measures Word's network
  traffic; if Word sends more than telemetry, the file is discarded and redone once. Log: `data/word-render.jsonl`.
- **Adoption:** `build.py adopt` trims the document information as for the first producer (left: producer "macOS …
  Quartz PDFContext" and date) and checks with the same thresholds against the same truth from the original
  (`data/build-word.json`, `data/manifest-word.json`, `data/pdf-word/`, `data/truth-word/`). The only XMP left is the
  colour-mode block inside the embedded logo of `fr-docx-ddbbc2ea20` (part of the image, not of the document info).
- **Dropped (1):** `en-docx-63f906b7f8`: Word reports unreadable content and wants to repair the document; no PDF
  without repair. LibreOffice opens it without a message.
- **Different page count than LibreOffice (6), all pass the checks:**

  | File | Word | LibreOffice |
  |---|---:|---:|
  | fr-docx-eb0ef2469f | 2 | 3 |
  | de-docx-77beeaad70 | 3 | 5 |
  | de-docx-3a043cc5a1 | 3 | 5 |
  | en-docx-75e588c6f1 | 11 | 13 |
  | en-docx-57ad4ee6b4 | 3 | 4 |
  | en-docx-544406eaaf | 7 | 6 |

- **Network:** for two files Word sent more than the usual telemetry on first opening (26 KB and 712 KB); the driver
  discarded the output and redid it. On second opening only telemetry (at most 29 KB).


## Added German and UK spreadsheets (draws 3 and 4)

- **Why:** in draws 1 and 2 France supplied 69 % of the numeric cells (20 large workbooks from data.gouv.fr). Goal:
  no country above 50 %.
- **Same rules:** only XLSX from data.gov.uk, GovData and the Hamburg transparency portal; the same licenses; checked
  against the exclusion lists of all of the vendor's internal test sets (URLs, dataset pages, SHA-256); at most two
  files per publisher, counted across draws; the same factory and checks. Seeds 20261117 and 20261118
  (`data/candidates3.json`, `data/candidates4.json`).
- **One new rule, for these draws only:** a sheet that would exceed 20 pages is cut to its first pages (print area
  over the first 4 pages of the uncut print; very wide sheets keep two pages of columns; one workbook breaks onto 7
  pages after the cut). Without it only 2 of 33 workbooks passed, because open spreadsheets are mostly long lists. The
  range is in the manifest field `crop`; Excel prints the same range. Draws 1 and 2 are unchanged.
- **Yield:** 75 candidates, 56 downloaded, 17 pass all checks; three of them are dropped (two with the same content as
  another file, one over the publisher limit). Added: 14 workbooks (8 German, 6 UK), 11 of them cut. Reasons per
  file: `data/build-draw3.json`, `data/build-draw4.json`.
- **Caveat:** two thirds of the German numeric cells come from one workbook (Hamburg traffic counts,
  `de-xlsx-24dd6c23dd`). The cell sum depends on that one file; this is why the mean per file stands next to it.
  Royal Armouries (UK) has three files from draw 2, which did not yet count earlier publishers.


## Method

The truth comes from the original, not from the PDF. XLSX: displayed text and cell type of every visible cell of the
printed sheets, one table per printed page in print order (check: as many blocks as pages, each block at least 90 %
on its own page; for Excel recomputed along Excel's pages, see above). DOCX: paragraphs and tables from
`word/document.xml` (no headers, footers or footnotes). Two coverage checks per file (at least 97 % of the truth in the
text layer, at least 85 % of the text layer in the truth), at most 20 pages, no tracked changes. The same metrics for
everyone (`eval/`, standard library only, pipe and HTML tables read the same way, self-check against hand-made
examples):

- **Numbers in the right cell:** numeric truth cells (XLSX: cell type number; DOCX: the cell is exactly one number)
  found in the matching row and column of an output table. Rows matched by shared cells (monotone, at least 30 %
  overlap, across all output tables), columns per table by majority, one to one. Text without tables scores 0.
- **Corrupted numbers:** numbers in the output that do not stand in the original like that: torn apart ("CaCl 2"),
  glued together (two cells as "65 280"), repeated, or new. Counted as number tokens that occur more often in the
  output than in the truth and the PDF's text layer together; numbers compared without thousands and decimal
  separators. The count does not tell whether a value was made up; that takes a look at the output (examples above).
- **Word recall:** share of the truth's words found in the output, regardless of order.
- **Reading order:** longest common word subsequence divided by the words in common.
- **Mean per file and cell sum** are shown side by side with equal weight; tables are ordered by the mean per file,
  because the cell sum depends on a few large workbooks.
- **Intervals:** 95 % percentile bootstrap with 10,000 draws, clustered by source document: all renderings of one
  original (LibreOffice, Word or Excel) are drawn together, because they are not independent. This applies to the
  mean per file, the cell sum (hits/numeric cells of the same draw) and the paired leads.
- **Producers and licences:** LibreOffice 25.2 (MPL-2.0) in the pinned container (`factory/Dockerfile`). Word and
  Excel for Mac 16.115 (build 26110837) under a Microsoft 365 Business Standard subscription of the vendor; checked in
  both apps' About dialog before the run on 2026-11-15 ("License: Microsoft 365 subscription", owned by the company's
  work account). Driven by AppleScript (Word) or through the menus (Excel), without changing system settings.
- **Time per page:** wall time per document divided by its pages, one document at a time. Open tools: 4 cores, no
  network, Python libraries loaded once, pdftotext starts one process per document. switchfile and CloudConvert: from
  request to downloaded Markdown through the public API, including upload, queueing and network.
- **Runs and failures:** all candidates were run in one window (2026-11-16), one attempt per PDF, limit 600 s per PDF,
  no retries. A PDF without output (error, time limit, failed job) counts as a failure and scores 0 in every metric.
  Run windows: `results/runs.json`.

## Candidates and baseline, versions, licenses

| Candidate | Version | License | Source of the license statement |
|---|---|---|---|
| switchfile (`pdf → md`) | public API `api.switchfile.io/v1/convert`, production as measured on 2026-11-16, 12:36–12:42 UTC | proprietary service of Aura UG (haftungsbeschränkt), the publisher | – |
| CloudConvert (PDF to Markdown API, `output_format: md`) | public API `api.cloudconvert.com/v2`, measured 2026-11-16; engine name and version as reported by the API per file in `results/cloudconvert-tasks.json` | proprietary service of Lunaweb GmbH; run by us through its public API with default settings | – |
| Docling | 2.150.1 (docling-core 2.107.0, docling-ibm-models 4.0.4, docling-parse 7.26.0, torch 2.15.0+cpu) | MIT; models: docling-layout-heron Apache-2.0, docling-models CDLA-Permissive-2.0 / Apache-2.0, CodeFormulaV2 CDLA-Permissive-2.0, DocumentFigureClassifier-v2.5 MIT | PyPI `license_expression` "MIT"; Hugging Face model cards |
| markitdown | 0.1.9 (`markitdown[pdf]`) | MIT | PyPI `license_expression` "MIT" |
| PyMuPDF (pymupdf4llm) | pymupdf4llm 2.1 | AGPL-3.0 or Artifex commercial license | package metadata |
| pdfplumber, with a minimal Markdown wrapper (ours) | 0.11.10 | MIT | PyPI classifier |
| pdftotext (baseline: plain text, no table output) | Poppler 25.03.0 (Debian 25.03.0-5+deb13u4) | GPL-2.0 or GPL-3.0 (core library) | `/usr/share/doc/poppler-utils/copyright` |

All candidates with default settings. switchfile and CloudConvert are services without version numbers; their
results describe the service on the date of measurement and can change without notice. CloudConvert: one job per
PDF (`import/upload` → `convert` with `input_format: pdf`, `output_format: md` and no other options → `export/url`),
1 credit per PDF; the job is deleted after the download. If CloudConvert returns an archive, only its Markdown is
kept and scored. pdfplumber has no Markdown writer: a minimal open wrapper written by us in `candidates/run.py`
(default table finder as pipe tables, remaining text by position). Docling: models downloaded at build time, measured
offline with `DOCLING_ARTIFACTS_PATH`.

## Limitations and bias

- **Possible home advantage:** switchfile was developed with test data of a similar kind (public office files from
  the same portals, printed to PDF with LibreOffice). No file is the same, but the distribution is similar.
  On the same XLSX originals, switchfile changes by −0.4 [−8.6; +6.6] points per file when Excel instead of LibreOffice prints them; see "Same originals, different producer".
- **Producers:** LibreOffice, Word for Mac, Excel for Mac. PDFs from InDesign, printer drivers, report generators or
  Office for Windows are missing. The Word and Excel sets are smaller than the LibreOffice set; differences there are
  less certain. The Excel set takes selection, sheets and cut ranges from the LibreOffice set; only the print is
  Excel's own. 85 % of the numeric cells in the Word set come from Zenodo documents.
- **Selection:** at most 20 pages, up to 4 sheets per workbook; sheets whose print does not match the cells
  unambiguously (overflowing text, charts, sheets that cannot be hidden) are dropped (reasons in `data/build*.json`).
  This favours clean tables. In draws 3 and 4 long sheets are cut; their tables end in the middle of the list.
- **Time:** the open tools ran on a shared server with load from other jobs, the services over the internet; compare
  orders of magnitude only. Docling ran without a GPU and would be much faster with one; it ran as two containers
  side by side, each with 4 cores and half of the PDFs.
- **Measured by a competitor:** switchfile and CloudConvert offer competing services; this benchmark is published by
  the maker of switchfile. switchfile is not affiliated with CloudConvert or Lunaweb GmbH.
- **Services change:** switchfile and CloudConvert can change without a version number. The numbers hold for the
  date of measurement; the outputs in `results/` show what each service returned on that date.
- **Native PDFs only:** all PDFs have a text layer. Scanned documents and OCR are not measured.

## Scoring fix (2026-11-18)

**What was wrong.** The tokenizer (`eval/mdparse.py`, `tokens()`) removed "." and "," between digits and dropped the
sign, so `-1.20`, `1.20` and `120` were one token. Cell keys, word tokens and number tokens all came from it: a lost
minus or decimal point still counted as a number in the right cell, as a word hit, and not as a corrupted number. The
"Same value" check added on 2026-11-17 caught this for matched cells only.

**What changed.** Number tokens now carry the signed value; the notation still does not matter. `1 268 082`,
`1.268.082`, `1,268,082` and `1268082` are equal, so are `2,1` and `2.1`, `1.20` and `1.2`, `(1.20)` and `-1.20`
(parentheses in table cells only). A minus counts directly before a number or around a currency sign, and when it
stands apart only if no word, number or currency sign precedes it, so `2019 - 2020` and the accounting zero `£ -` are
not negative. A lone separator before exactly three digits (`1.268`) is read with the document's decimal separator
(from the truth tables, else from the document's language). French amounts with space-separated thousands and
decimals (`92 991,00 €`) were split into two tokens before and fell out of the numeric cells; 132 such cells are now
scored. `factory/build.py` keeps the old tokenizer (`loose_tokens`), because the data set and truth were built with
it. Regression tests: `python3 -I -m unittest discover eval`.

**Effect.** Only the scoring was rerun, on the published outputs of 2026-11-16; no candidate was run again. All 160
files; numeric cells 28,321 → 28,453. Mean per file and cell sum: numbers in the right cell; corrupted numbers: total
(files); word recall: mean per file; last column: right cell / same value (cross-check, see README) after the fix.

| Candidate | Right cell, per file | Right cell, summed | Corrupted numbers | Word recall | Right cell / same value |
|---|---:|---:|---:|---:|---:|
| switchfile | 94.1 → 93.8 | 97.2 → 97.2 | 18 (6) → 28 (8) | 99.5 → 99.5 | 27,649 / 27,649 |
| CloudConvert | 82.6 → 82.3 | 68.4 → 68.1 | 612 (32) → 732 (37) | 98.3 → 98.3 | 19,387 / 19,378 |
| pymupdf4llm | 81.6 → 81.3 | 68.3 → 68.0 | 245 (22) → 370 (27) | 98.4 → 98.3 | 19,343 / 19,334 |
| Docling | 67.6 → 67.9 | 57.2 → 57.1 | 454 (37) → 492 (39) | 98.2 → 98.2 | 16,258 / 16,258 |
| pdfplumber + our wrapper | 48.5 → 49.1 | 48.1 → 48.1 | 413 (25) → 417 (25) | 98.2 → 98.2 | 13,691 / 13,691 |
| markitdown | 36.9 → 36.7 | 39.7 → 39.5 | 172 (16) → 178 (17) | 98.6 → 98.6 | 11,253 / 11,253 |
| pdftotext (baseline) | 0.0 → 0.0 | 0.0 → 0.0 | 0 (0) → 0 (0) | 99.8 → 99.8 | 0 / 0 |

The order of candidates by right cell per file is unchanged, overall and in every group by producer, country, format
and language. In the summed rate two neighbours swap places: Docling and pdfplumber + our wrapper for France (84.8 and
84.6, before 85.0 and 85.0), switchfile and Docling for international files (99.8 and 99.3, before 99.8 and 99.9).
Where a cell lost its decimal point (`73,7` → `737`, `£138.00` → `13800`) or its minus moved behind the number
(`−0.472` → `0.472 -`), it is now a miss and a corrupted number. A cell split in two can now leave a negative-looking
number (`13 | - 19` for the range `13 - 19`); it counts as corrupted. Where the right-cell and same-value counts differ
(9 cells, two candidates), the second parser reads an accounting zero `£ -` before the amount as a minus.

Scores: `results/scores-2026-11-18-all.json`; before the fix: `results/scores-2026-11-17-all.json`.

## Same value (added 2026-11-17)

As published on 2026-11-17, before the scoring fix above.

The cell comparison ignores signs and decimal separators, so a lost minus or decimal point still counted as a hit
(reported by a reader on Reddit). `score.py` now also counts matched cells whose signed value equals the truth.
All 160 files, all numeric cells (28,321); no other number changed:

| Candidate | Right cell | Same value | Cells lost |
|---|---:|---:|---:|
| switchfile | 27,539 (97.2 %) | 27,539 (97.2 %) | 0 |
| cloudconvert | 19,374 (68.4 %) | 19,296 (68.1 %) | 78 |
| pymupdf4llm | 19,330 (68.3 %) | 19,252 (68.0 %) | 78 |
| docling | 16,198 (57.2 %) | 16,168 (57.1 %) | 30 |
| pdfplumber | 13,633 (48.1 %) | 13,633 (48.1 %) | 0 |
| markitdown | 11,244 (39.7 %) | 11,242 (39.7 %) | 2 |
| pdftotext | 0 (0.0 %) | 0 (0.0 %) | 0 |

Scores: `results/scores-2026-11-17-all.json`.
