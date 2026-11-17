# Results: business PDF → Markdown, table cells and corrupted numbers (measured 2026-11-16)

Published by Aura UG (haftungsbeschränkt), the company that makes switchfile, one of the candidates. We chose the
data, wrote the scoring code and ran every candidate ourselves, switchfile included. Scope and limits: README and
"Limitations and bias" below.

## Summary

- **Data:** 82 public originals (45 XLSX, 37 DOCX) from France (data.gouv.fr), Germany (GovData, Hamburg transparency
  portal), the United Kingdom (data.gov.uk) and Zenodo (international); 28,688 truth cells, 14,351 of them numeric
  (LibreOffice set). Numeric cells by country: FR 40 %, DE 39 %, UK 11 %, international 9 %; 65 % of the German
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
  | switchfile | 94.1 [90.7; 97.1] | 97.2 [95.6; 98.7] | 98.9 \| 99.5 | 93.1 \| 99.4 | 93.7 \| 95.1 | 0 |
  | CloudConvert | 82.6 [75.1; 89.3] | 68.4 [38.0; 95.5] | 97.9 \| 97.3 | 79.9 \| 65.9 | 80.7 \| 67.6 | 0 |
  | pymupdf4llm | 81.6 [74.0; 88.4] | 68.3 [37.9; 95.3] | 97.7 \| 97.2 | 79.9 \| 65.9 | 78.7 \| 67.3 | 0 |
  | Docling | 67.6 [56.7; 77.9] | 57.2 [29.3; 86.6] | 98.9 \| 99.5 | 59.0 \| 53.6 | 65.7 \| 56.0 | 0 |
  | pdfplumber + our wrapper | 48.5 [35.8; 61.5] | 48.1 [20.6; 79.2] | 58.8 \| 67.1 | 41.2 \| 45.7 | 50.9 \| 48.4 | 0 |
  | markitdown | 36.9 [26.8; 47.1] | 39.7 [21.3; 64.2] | 41.7 \| 56.9 | 39.7 \| 39.0 | 33.8 \| 38.5 | 0 |
  | pdftotext (baseline) | 0.0 [0.0; 0.0] | 0.0 [0.0; 0.0] | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 | 0 |

  Word, Excel and LibreOffice columns: per file \| summed. Numeric cells: Word 1,463, Excel 12,507, LibreOffice 14,351
  (28,321 in all). pdftotext is a baseline only: plain text, no table output. pdfplumber has no Markdown writer and is
  measured through a minimal wrapper written by us.

- **Failures:** none; every candidate returned output for every PDF.
- **Paired difference, switchfile minus candidate** (points per file on the same PDFs with numeric cells, 95 %
  interval clustered by source document; in brackets: switchfile higher / equal / lower):

  | Candidate | all | Microsoft Office PDFs | LibreOffice PDFs |
  |---|---:|---:|---:|
  | CloudConvert | +11.5 [+5.5; +18.5] (35/55/12) | +9.9 [+1.1; +19.3] (16/29/4) | +13.0 [+4.9; +22.4] (19/26/8) |
  | pymupdf4llm | +12.6 [+6.5; +19.7] (36/55/11) | +10.0 [+1.2; +19.3] (16/30/3) | +14.9 [+6.3; +24.6] (20/25/8) |
  | Docling | +26.6 [+17.4; +36.5] (49/48/5) | +25.0 [+13.5; +37.2] (21/27/1) | +28.0 [+17.3; +39.3] (28/21/4) |
  | pdfplumber + our wrapper | +45.6 [+33.5; +57.7] (55/45/2) | +48.7 [+35.2; +61.9] (29/20/0) | +42.8 [+30.5; +55.1] (26/25/2) |
  | markitdown | +57.2 [+46.1; +68.0] (88/12/2) | +54.3 [+41.3; +66.9] (41/6/2) | +59.9 [+49.4; +70.2] (47/6/0) |

- **Same originals, different producer:** on the same 36 XLSX originals with numeric cells, switchfile changes by −0.4
  [−8.6; +6.6] points per file when Excel instead of LibreOffice prints them (interval includes 0); switchfile minus
  pymupdf4llm is +23.3 [+11.3; +37.0] on LibreOffice and +13.2 [+1.3; +25.5] on Excel PDFs, switchfile minus
  CloudConvert +20.5 [+9.2; +33.3] and +13.2 [+1.3; +25.5]. On 13 DOCX originals with numeric cells, switchfile minus
  Docling on Word PDFs is +0.0 [+0.0; +0.0], minus pymupdf4llm +1.2 [+0.0; +3.6], minus CloudConvert +0.9 [−0.8;
  +3.6]. Table below.
- **Numbers in the right cell by country** (all producers, per file \| summed):

  | Candidate | FR (54) | DE (39) | UK (28) | international (39) |
  |---|---:|---:|---:|---:|
  | switchfile | 93.3 \| 99.4 | 83.4 \| 93.8 | 99.6 \| 99.0 | 99.9 \| 99.8 |
  | CloudConvert | 81.2 \| 94.9 | 75.6 \| 28.5 | 77.0 \| 85.8 | 98.6 \| 97.4 |
  | pymupdf4llm | 81.2 \| 94.9 | 75.2 \| 28.5 | 72.8 \| 84.6 | 98.6 \| 97.4 |
  | Docling | 61.2 \| 85.0 | 50.7 \| 15.4 | 63.5 \| 65.7 | 99.9 \| 99.9 |
  | pdfplumber + our wrapper | 51.1 \| 85.0 | 26.3 \| 4.1 | 54.2 \| 50.3 | 59.8 \| 66.9 |
  | markitdown | 38.2 \| 54.0 | 33.0 \| 10.9 | 26.6 \| 64.9 | 50.5 \| 66.8 |
  | pdftotext (baseline) | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 | 0.0 \| 0.0 |

- **Corrupted numbers** (numbers that do not stand in the original like that: torn apart, glued together, repeated or
  new; definition under Method), total over all PDFs (files affected): switchfile 18 (6), CloudConvert 612 (32),
  pymupdf4llm 245 (22), Docling 454 (37), pdfplumber + our wrapper 413 (25), markitdown 172 (16). Per producer: tables
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
| switchfile | 93.4 | 93.1 | −0.4 [−8.6; +6.6] | – | – | – | – |
| CloudConvert | 72.9 | 79.9 | +7.0 [−5.0; +20.0] | +20.5 [+9.2; +33.3] | +13.2 [+1.3; +25.5] | +0.8 [−1.3; +3.4] | +0.9 [−0.8; +3.6] |
| pymupdf4llm | 70.1 | 79.9 | +9.8 [−3.1; +23.8] | +23.3 [+11.3; +37.0] | +13.2 [+1.3; +25.5] | +1.1 [−0.5; +3.4] | +1.2 [+0.0; +3.6] |
| Docling | 51.4 | 59.0 | +7.6 [−6.0; +21.2] | +42.0 [+28.9; +55.6] | +34.0 [+19.3; +49.2] | +3.2 [−0.2; +9.6] | +0.0 [+0.0; +0.0] |
| pdfplumber + our wrapper | 46.0 | 41.2 | −4.7 [−12.1; +0.0] | +47.5 [+32.1; +62.5] | +51.8 [+35.8; +67.4] | +38.3 [+15.2; +63.0] | +40.1 [+16.1; +64.8] |
| markitdown | 30.4 | 39.7 | +9.3 [+3.9; +15.7] | +63.0 [+50.1; +75.2] | +53.3 [+36.7; +68.5] | +56.1 [+33.3; +78.8] | +57.1 [+35.2; +78.5] |
| pdftotext (baseline) | 0.0 | 0.0 | +0.0 [+0.0; +0.0] | – | – | – | – |

## Results by producer, country and format

"Right cell, mean per file" and "all cells": numbers in the right cell averaged per file or summed over all numeric
cells (hits/numeric cells); corrupted numbers as total (files); word recall and reading order as mean per file; time
per page as total/total (median per file; API services include network); 95 % bootstrap clustered by source
document. Per-file values: `results/scores-2026-11-16-all.json` (Word files end in `-msword`, Excel files in `-msexcel`).

**all**: 160 files, 781 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 94.1 [90.7–97.1] | 97.2 [95.6–98.7] (27539/28321) | 18 (6) | 99.5 [99.3–99.7] | 98.9 [97.9–99.6] | 0.47 (0.59) | 0 |
| cloudconvert | 82.6 [75.1–89.3] | 68.4 [38.0–95.5] (19374/28321) | 612 (32) | 98.3 [97.7–98.9] | 98.1 [97.0–99.0] | 0.62 (0.75) | 0 |
| pymupdf4llm | 81.6 [74.0–88.4] | 68.3 [37.9–95.3] (19330/28321) | 245 (22) | 98.4 [97.7–99.0] | 98.1 [97.0–99.0] | 0.88 (0.74) | 0 |
| Docling | 67.6 [56.7–77.9] | 57.2 [29.3–86.6] (16198/28321) | 454 (37) | 98.2 [96.8–99.3] | 97.2 [96.1–98.3] | 13.90 (10.62) | 0 |
| pdfplumber + our wrapper | 48.5 [35.8–61.5] | 48.1 [20.6–79.2] (13633/28321) | 413 (25) | 98.2 [97.1–99.1] | 98.4 [96.9–99.5] | 0.18 (0.13) | 0 |
| markitdown | 36.9 [26.8–47.1] | 39.7 [21.3–64.2] (11244/28321) | 172 (16) | 98.6 [97.6–99.4] | 87.7 [82.8–91.9] | 0.26 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/28321) | 0 (0) | 99.8 [99.7–99.9] | 79.3 [73.7–84.6] | 0.01 (0.01) | 0 |

**producer=word**: 36 files, 206 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 98.9 [96.6–100.0] | 99.5 [97.6–100.0] (1455/1463) | 9 (2) | 99.6 [99.3–99.8] | 99.6 [99.2–99.8] | 0.44 (0.65) | 0 |
| Docling | 98.9 [96.6–100.0] | 99.5 [97.6–100.0] (1455/1463) | 79 (8) | 99.6 [99.4–99.8] | 99.4 [98.9–99.8] | 10.02 (6.40) | 0 |
| cloudconvert | 97.9 [94.7–100.0] | 97.3 [92.2–100.0] (1424/1463) | 155 (7) | 99.5 [99.2–99.7] | 99.7 [99.4–99.9] | 0.55 (0.77) | 0 |
| pymupdf4llm | 97.7 [94.2–100.0] | 97.2 [91.9–100.0] (1422/1463) | 7 (3) | 99.5 [99.2–99.7] | 99.7 [99.4–99.9] | 0.74 (0.64) | 0 |
| pdfplumber + our wrapper | 58.8 [33.7–83.2] | 67.1 [25.8–93.2] (981/1463) | 21 (6) | 99.5 [99.2–99.8] | 98.5 [95.8–99.9] | 0.21 (0.16) | 0 |
| markitdown | 41.7 [20.8–62.9] | 56.9 [24.4–74.7] (833/1463) | 20 (7) | 99.8 [99.7–99.9] | 94.7 [89.8–98.3] | 0.32 (0.34) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/1463) | 0 (0) | 99.7 [99.5–99.8] | 96.1 [91.9–99.1] | 0.01 (0.02) | 0 |

**producer=excel**: 42 files, 171 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.1 [85.6–98.6] | 99.4 [98.4–99.9] (12437/12507) | 7 (2) | 99.7 [99.4–99.9] | 98.5 [97.3–99.5] | 0.55 (0.63) | 0 |
| cloudconvert | 79.9 [68.6–89.7] | 65.9 [32.7–96.8] (8243/12507) | 85 (7) | 96.9 [95.3–98.3] | 96.7 [94.6–98.4] | 0.72 (0.78) | 0 |
| pymupdf4llm | 79.9 [68.6–89.7] | 65.9 [32.7–96.8] (8243/12507) | 85 (7) | 96.9 [95.3–98.3] | 96.7 [94.6–98.4] | 1.03 (0.89) | 0 |
| Docling | 59.0 [43.9–73.7] | 53.6 [23.2–86.3] (6702/12507) | 170 (8) | 96.2 [91.9–99.5] | 95.1 [92.9–97.1] | 20.78 (16.79) | 0 |
| pdfplumber + our wrapper | 41.2 [25.8–57.2] | 45.7 [14.5–81.0] (5711/12507) | 250 (9) | 97.0 [94.0–99.3] | 98.6 [97.3–99.7] | 0.17 (0.13) | 0 |
| markitdown | 39.7 [27.4–52.6] | 39.0 [19.0–67.9] (4879/12507) | 58 (2) | 98.7 [96.2–99.9] | 81.5 [73.9–88.5] | 0.27 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/12507) | 0 (0) | 99.9 [99.8–100.0] | 61.2 [53.6–69.1] | 0.02 (0.02) | 0 |

**producer=libreoffice**: 82 files, 404 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.7 [89.8–96.9] | 95.1 [92.2–98.0] (13647/14351) | 2 (2) | 99.4 [99.1–99.7] | 98.8 [97.4–99.6] | 0.46 (0.57) | 0 |
| cloudconvert | 80.7 [71.7–88.9] | 67.6 [37.9–94.9] (9707/14351) | 372 (18) | 98.6 [98.0–99.1] | 98.1 [97.0–99.0] | 0.62 (0.74) | 0 |
| pymupdf4llm | 78.7 [69.1–87.3] | 67.3 [37.7–94.5] (9665/14351) | 153 (12) | 98.7 [98.0–99.2] | 98.1 [97.0–99.0] | 0.89 (0.73) | 0 |
| Docling | 65.7 [54.0–76.8] | 56.0 [28.5–85.3] (8041/14351) | 205 (21) | 98.6 [97.6–99.4] | 97.4 [95.9–98.6] | 12.97 (9.58) | 0 |
| pdfplumber + our wrapper | 50.9 [38.1–63.8] | 48.4 [21.2–79.1] (6941/14351) | 142 (10) | 98.3 [97.2–99.2] | 98.2 [96.6–99.4] | 0.16 (0.12) | 0 |
| markitdown | 33.8 [23.7–44.3] | 38.5 [20.5–62.3] (5532/14351) | 94 (7) | 98.0 [96.5–99.2] | 87.8 [83.0–92.0] | 0.22 (0.19) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/14351) | 0 (0) | 99.8 [99.7–99.9] | 81.2 [75.8–86.3] | 0.01 (0.01) | 0 |

**family=office**: 78 files, 377 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 94.6 [89.1–98.8] | 99.4 [98.5–99.8] (13892/13970) | 16 (4) | 99.6 [99.4–99.8] | 99.0 [98.3–99.5] | 0.49 (0.63) | 0 |
| cloudconvert | 84.7 [76.1–92.3] | 69.2 [37.7–96.9] (9667/13970) | 240 (14) | 98.1 [97.1–98.9] | 98.1 [96.9–99.0] | 0.62 (0.77) | 0 |
| pymupdf4llm | 84.6 [76.0–92.2] | 69.2 [37.7–96.8] (9665/13970) | 92 (10) | 98.1 [97.1–98.9] | 98.1 [96.9–99.0] | 0.87 (0.75) | 0 |
| Docling | 69.6 [57.4–81.4] | 58.4 [29.7–88.6] (8157/13970) | 249 (16) | 97.8 [95.4–99.6] | 97.1 [95.8–98.3] | 14.90 (11.53) | 0 |
| pdfplumber + our wrapper | 45.9 [32.4–59.7] | 47.9 [19.5–79.9] (6692/13970) | 271 (15) | 98.2 [96.5–99.4] | 98.6 [97.1–99.6] | 0.20 (0.14) | 0 |
| markitdown | 40.3 [29.7–51.2] | 40.9 [21.8–66.3] (5712/13970) | 78 (9) | 99.2 [97.9–99.9] | 87.6 [82.6–91.9] | 0.29 (0.24) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/13970) | 0 (0) | 99.8 [99.7–99.9] | 77.3 [71.3–83.0] | 0.01 (0.02) | 0 |

**family=libreoffice**: 82 files, 404 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.7 [89.8–96.9] | 95.1 [92.2–98.0] (13647/14351) | 2 (2) | 99.4 [99.1–99.7] | 98.8 [97.4–99.6] | 0.46 (0.57) | 0 |
| cloudconvert | 80.7 [71.7–88.9] | 67.6 [37.9–94.9] (9707/14351) | 372 (18) | 98.6 [98.0–99.1] | 98.1 [97.0–99.0] | 0.62 (0.74) | 0 |
| pymupdf4llm | 78.7 [69.1–87.3] | 67.3 [37.7–94.5] (9665/14351) | 153 (12) | 98.7 [98.0–99.2] | 98.1 [97.0–99.0] | 0.89 (0.73) | 0 |
| Docling | 65.7 [54.0–76.8] | 56.0 [28.5–85.3] (8041/14351) | 205 (21) | 98.6 [97.6–99.4] | 97.4 [95.9–98.6] | 12.97 (9.58) | 0 |
| pdfplumber + our wrapper | 50.9 [38.1–63.8] | 48.4 [21.2–79.1] (6941/14351) | 142 (10) | 98.3 [97.2–99.2] | 98.2 [96.6–99.4] | 0.16 (0.12) | 0 |
| markitdown | 33.8 [23.7–44.3] | 38.5 [20.5–62.3] (5532/14351) | 94 (7) | 98.0 [96.5–99.2] | 87.8 [83.0–92.0] | 0.22 (0.19) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/14351) | 0 (0) | 99.8 [99.7–99.9] | 81.2 [75.8–86.3] | 0.01 (0.01) | 0 |

**country=FR**: 54 files, 246 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.3 [86.6–98.6] | 99.4 [97.6–99.9] (11556/11622) | 0 (0) | 99.8 [99.6–99.9] | 97.8 [95.0–99.7] | 0.49 (0.59) | 0 |
| cloudconvert | 81.2 [68.8–91.8] | 94.9 [86.2–99.0] (11035/11622) | 148 (8) | 97.8 [96.4–98.9] | 98.0 [96.3–99.3] | 0.66 (0.77) | 0 |
| pymupdf4llm | 81.2 [68.8–91.8] | 94.9 [86.2–99.0] (11035/11622) | 148 (8) | 97.8 [96.4–98.9] | 98.0 [96.3–99.3] | 0.98 (0.76) | 0 |
| Docling | 61.2 [42.4–78.2] | 85.0 [53.9–95.4] (9879/11622) | 89 (10) | 97.4 [94.4–99.6] | 96.9 [94.7–98.8] | 16.40 (10.15) | 0 |
| pdfplumber + our wrapper | 51.1 [28.9–72.6] | 85.0 [48.2–97.6] (9883/11622) | 151 (7) | 98.1 [96.1–99.6] | 98.6 [96.6–99.9] | 0.12 (0.08) | 0 |
| markitdown | 38.2 [23.2–54.4] | 54.0 [39.6–78.5] (6280/11622) | 136 (5) | 98.0 [95.8–99.6] | 94.8 [91.2–97.8] | 0.23 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/11622) | 0 (0) | 99.8 [99.6–100.0] | 76.2 [66.9–85.3] | 0.01 (0.01) | 0 |

**country=DE**: 39 files, 197 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 83.4 [73.5–91.7] | 93.8 [83.3–95.6] (10295/10974) | 7 (2) | 99.4 [98.9–99.8] | 99.5 [99.0–99.9] | 0.45 (0.51) | 0 |
| cloudconvert | 75.6 [56.4–91.4] | 28.5 [7.3–93.9] (3133/10974) | 83 (5) | 98.5 [97.6–99.3] | 98.8 [98.2–99.4] | 0.58 (0.64) | 0 |
| pymupdf4llm | 75.2 [56.2–91.0] | 28.5 [7.3–93.7] (3129/10974) | 81 (4) | 98.5 [97.6–99.3] | 98.8 [98.1–99.4] | 0.89 (0.75) | 0 |
| Docling | 50.7 [28.5–73.9] | 15.4 [3.4–64.7] (1693/10974) | 149 (13) | 97.2 [93.5–99.4] | 96.7 [94.7–98.5] | 10.90 (9.12) | 0 |
| markitdown | 33.0 [12.9–54.3] | 10.9 [1.3–49.9] (1200/10974) | 2 (2) | 98.5 [96.3–99.9] | 88.9 [80.4–95.3] | 0.24 (0.19) | 0 |
| pdfplumber + our wrapper | 26.3 [3.8–52.0] | 4.1 [0.5–32.4] (451/10974) | 119 (4) | 96.6 [92.8–99.2] | 98.1 [95.5–100.0] | 0.20 (0.17) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/10974) | 0 (0) | 99.8 [99.6–100.0] | 84.5 [75.5–92.5] | 0.01 (0.01) | 0 |

**country=UK**: 28 files, 88 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 99.6 [98.8–100.0] | 99.0 [96.6–100.0] (3165/3198) | 1 (1) | 99.3 [98.6–99.8] | 98.9 [97.6–99.8] | 0.65 (1.25) | 0 |
| cloudconvert | 77.0 [59.4–91.8] | 85.8 [62.8–95.8] (2744/3198) | 33 (4) | 97.5 [95.2–99.3] | 95.0 [90.3–98.8] | 0.89 (1.57) | 0 |
| pymupdf4llm | 72.8 [55.5–88.5] | 84.6 [59.0–95.0] (2704/3198) | 4 (3) | 97.7 [95.4–99.5] | 95.0 [90.3–98.8] | 0.97 (0.77) | 0 |
| Docling | 63.5 [41.7–83.9] | 65.7 [29.7–90.5] (2101/3198) | 96 (3) | 99.1 [98.0–100.0] | 95.4 [91.7–98.5] | 23.69 (18.14) | 0 |
| pdfplumber + our wrapper | 54.2 [25.0–79.2] | 50.3 [4.4–89.3] (1608/3198) | 122 (4) | 98.9 [97.9–99.7] | 99.5 [98.6–100.0] | 0.14 (0.10) | 0 |
| markitdown | 26.6 [5.0–50.0] | 64.9 [12.9–88.4] (2076/3198) | 0 (0) | 98.1 [95.8–100.0] | 64.9 [50.0–79.6] | 0.25 (0.21) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/3198) | 0 (0) | 99.9 [99.7–100.0] | 57.1 [44.5–70.3] | 0.02 (0.03) | 0 |

**country=INT**: 39 files, 250 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 99.9 [99.8–100.0] | 99.8 [99.5–100.0] (2523/2527) | 10 (3) | 99.5 [99.0–99.8] | 99.7 [99.4–99.9] | 0.42 (0.57) | 0 |
| Docling | 99.9 [99.6–100.0] | 99.9 [99.6–100.0] (2525/2527) | 120 (11) | 99.7 [99.6–99.8] | 99.6 [99.2–99.9] | 10.36 (7.22) | 0 |
| cloudconvert | 98.6 [95.7–100.0] | 97.4 [91.9–100.0] (2462/2527) | 348 (15) | 99.6 [99.4–99.8] | 99.7 [99.4–99.9] | 0.53 (0.64) | 0 |
| pymupdf4llm | 98.6 [95.7–100.0] | 97.4 [91.9–100.0] (2462/2527) | 12 (7) | 99.6 [99.4–99.8] | 99.7 [99.5–99.9] | 0.75 (0.69) | 0 |
| pdfplumber + our wrapper | 59.8 [31.2–88.4] | 66.9 [18.8–95.4] (1691/2527) | 21 (10) | 99.5 [99.0–99.8] | 97.5 [92.9–100.0] | 0.22 (0.19) | 0 |
| markitdown | 50.5 [26.8–74.2] | 66.8 [33.2–81.8] (1688/2527) | 34 (9) | 99.8 [99.7–99.9] | 93.0 [84.6–99.3] | 0.30 (0.28) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/2527) | 0 (0) | 99.8 [99.7–99.9] | 94.3 [86.8–99.5] | 0.01 (0.01) | 0 |

**format=xlsx**: 87 files, 348 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 92.5 [88.0–96.4] | 97.0 [94.9–98.6] (24602/25362) | 8 (3) | 99.5 [99.1–99.8] | 98.3 [96.5–99.5] | 0.55 (0.58) | 0 |
| cloudconvert | 77.1 [67.8–85.7] | 65.0 [32.8–95.0] (16496/25362) | 261 (15) | 97.4 [96.3–98.4] | 96.8 [94.9–98.3] | 0.74 (0.77) | 0 |
| pymupdf4llm | 75.8 [66.6–84.4] | 64.9 [32.7–94.8] (16456/25362) | 232 (14) | 97.4 [96.3–98.4] | 96.8 [94.9–98.3] | 1.09 (0.83) | 0 |
| Docling | 56.9 [44.5–69.6] | 52.4 [22.8–84.6] (13281/25362) | 310 (16) | 97.0 [94.5–98.9] | 95.4 [93.5–97.1] | 18.65 (13.21) | 0 |
| pdfplumber + our wrapper | 44.0 [29.4–59.2] | 45.8 [15.1–80.6] (11626/25362) | 374 (13) | 97.1 [95.1–98.7] | 98.2 [96.7–99.5] | 0.16 (0.11) | 0 |
| markitdown | 34.5 [23.2–46.6] | 37.4 [18.5–64.3] (9494/25362) | 136 (5) | 97.6 [95.8–99.0] | 81.4 [74.2–88.1] | 0.23 (0.17) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/25362) | 0 (0) | 99.9 [99.8–100.0] | 65.1 [58.1–72.1] | 0.01 (0.01) | 0 |

**format=docx**: 73 files, 433 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 98.7 [96.2–100.0] | 99.3 [97.3–100.0] (2937/2959) | 10 (3) | 99.6 [99.3–99.8] | 99.5 [99.1–99.8] | 0.42 (0.59) | 0 |
| cloudconvert | 97.9 [95.2–99.8] | 97.3 [92.6–99.7] (2878/2959) | 351 (17) | 99.5 [99.3–99.7] | 99.7 [99.4–99.9] | 0.52 (0.70) | 0 |
| pymupdf4llm | 97.6 [94.5–99.8] | 97.1 [92.4–99.7] (2874/2959) | 13 (8) | 99.5 [99.3–99.7] | 99.7 [99.4–99.9] | 0.72 (0.63) | 0 |
| Docling | 97.2 [91.5–100.0] | 98.6 [94.1–100.0] (2917/2959) | 144 (21) | 99.7 [99.5–99.8] | 99.4 [99.0–99.8] | 10.08 (5.99) | 0 |
| pdfplumber + our wrapper | 61.0 [35.4–84.5] | 67.8 [26.9–93.4] (2007/2959) | 39 (12) | 99.6 [99.3–99.8] | 98.5 [96.0–99.9] | 0.19 (0.16) | 0 |
| markitdown | 43.5 [22.9–64.1] | 59.1 [25.8–76.3] (1750/2959) | 36 (11) | 99.8 [99.7–99.9] | 95.1 [90.4–98.5] | 0.28 (0.29) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/2959) | 0 (0) | 99.7 [99.5–99.8] | 96.2 [92.1–99.1] | 0.01 (0.01) | 0 |

**lang=de**: 39 files, 197 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 83.4 [73.5–91.7] | 93.8 [83.3–95.6] (10295/10974) | 7 (2) | 99.4 [98.9–99.8] | 99.5 [99.0–99.9] | 0.45 (0.51) | 0 |
| cloudconvert | 75.6 [56.4–91.4] | 28.5 [7.3–93.9] (3133/10974) | 83 (5) | 98.5 [97.6–99.3] | 98.8 [98.2–99.4] | 0.58 (0.64) | 0 |
| pymupdf4llm | 75.2 [56.2–91.0] | 28.5 [7.3–93.7] (3129/10974) | 81 (4) | 98.5 [97.6–99.3] | 98.8 [98.1–99.4] | 0.89 (0.75) | 0 |
| Docling | 50.7 [28.5–73.9] | 15.4 [3.4–64.7] (1693/10974) | 149 (13) | 97.2 [93.5–99.4] | 96.7 [94.7–98.5] | 10.90 (9.12) | 0 |
| markitdown | 33.0 [12.9–54.3] | 10.9 [1.3–49.9] (1200/10974) | 2 (2) | 98.5 [96.3–99.9] | 88.9 [80.4–95.3] | 0.24 (0.19) | 0 |
| pdfplumber + our wrapper | 26.3 [3.8–52.0] | 4.1 [0.5–32.4] (451/10974) | 119 (4) | 96.6 [92.8–99.2] | 98.1 [95.5–100.0] | 0.20 (0.17) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/10974) | 0 (0) | 99.8 [99.6–100.0] | 84.5 [75.5–92.5] | 0.01 (0.01) | 0 |

**lang=en**: 67 files, 338 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 99.7 [99.3–100.0] | 99.4 [98.1–100.0] (5688/5725) | 11 (4) | 99.4 [99.0–99.7] | 99.3 [98.8–99.8] | 0.48 (0.59) | 0 |
| cloudconvert | 87.1 [76.1–95.9] | 90.9 [80.3–97.0] (5206/5725) | 381 (19) | 98.7 [97.7–99.5] | 97.8 [95.6–99.5] | 0.62 (0.77) | 0 |
| pymupdf4llm | 84.8 [73.4–94.4] | 90.2 [78.9–96.4] (5166/5725) | 16 (10) | 98.8 [97.8–99.6] | 97.8 [95.6–99.5] | 0.81 (0.72) | 0 |
| Docling | 80.5 [66.0–92.9] | 80.8 [57.8–95.7] (4626/5725) | 216 (14) | 99.4 [98.9–99.8] | 97.8 [96.1–99.2] | 13.83 (11.20) | 0 |
| pdfplumber + our wrapper | 56.8 [37.0–76.1] | 57.6 [18.0–84.6] (3299/5725) | 143 (14) | 99.3 [98.7–99.7] | 98.3 [95.6–99.9] | 0.20 (0.15) | 0 |
| markitdown | 37.7 [21.1–55.5] | 65.7 [36.8–82.2] (3764/5725) | 34 (9) | 99.1 [98.0–99.8] | 81.3 [72.0–89.8] | 0.28 (0.24) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/5725) | 0 (0) | 99.8 [99.7–99.9] | 78.7 [69.3–87.5] | 0.01 (0.01) | 0 |

**lang=fr**: 54 files, 246 pages

| Candidate | Right cell, mean per file [95 % CI] | Right cell, all cells | Corrupted numbers (files) | Word recall | Reading order | s/page (median) | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| switchfile | 93.3 [86.6–98.6] | 99.4 [97.6–99.9] (11556/11622) | 0 (0) | 99.8 [99.6–99.9] | 97.8 [95.0–99.7] | 0.49 (0.59) | 0 |
| cloudconvert | 81.2 [68.8–91.8] | 94.9 [86.2–99.0] (11035/11622) | 148 (8) | 97.8 [96.4–98.9] | 98.0 [96.3–99.3] | 0.66 (0.77) | 0 |
| pymupdf4llm | 81.2 [68.8–91.8] | 94.9 [86.2–99.0] (11035/11622) | 148 (8) | 97.8 [96.4–98.9] | 98.0 [96.3–99.3] | 0.98 (0.76) | 0 |
| Docling | 61.2 [42.4–78.2] | 85.0 [53.9–95.4] (9879/11622) | 89 (10) | 97.4 [94.4–99.6] | 96.9 [94.7–98.8] | 16.40 (10.15) | 0 |
| pdfplumber + our wrapper | 51.1 [28.9–72.6] | 85.0 [48.2–97.6] (9883/11622) | 151 (7) | 98.1 [96.1–99.6] | 98.6 [96.6–99.9] | 0.12 (0.08) | 0 |
| markitdown | 38.2 [23.2–54.4] | 54.0 [39.6–78.5] (6280/11622) | 136 (5) | 98.0 [95.8–99.6] | 94.8 [91.2–97.8] | 0.23 (0.22) | 0 |
| pdftotext (baseline) | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] (0/11622) | 0 (0) | 99.8 [99.6–100.0] | 76.2 [66.9–85.3] | 0.01 (0.01) | 0 |

Paired per file against switchfile, numbers in right cell, all (files with numeric cells):

| Candidate | Difference, points [95 % CI] | first better / equal / worse |
|---|---:|---:|
| cloudconvert | +11.5 [+5.5; +18.5] | 35 / 55 / 12 |
| pymupdf4llm | +12.6 [+6.5; +19.7] | 36 / 55 / 11 |
| Docling | +26.6 [+17.4; +36.5] | 49 / 48 / 5 |
| pdfplumber + our wrapper | +45.6 [+33.5; +57.7] | 55 / 45 / 2 |
| markitdown | +57.2 [+46.1; +68.0] | 88 / 12 / 2 |

Paired per file against switchfile, numbers in right cell, family=libreoffice (files with numeric cells):

| Candidate | Difference, points [95 % CI] | first better / equal / worse |
|---|---:|---:|
| cloudconvert | +13.0 [+4.9; +22.4] | 19 / 26 / 8 |
| pymupdf4llm | +14.9 [+6.3; +24.6] | 20 / 25 / 8 |
| Docling | +28.0 [+17.3; +39.3] | 28 / 21 / 4 |
| pdfplumber + our wrapper | +42.8 [+30.5; +55.1] | 26 / 25 / 2 |
| markitdown | +59.9 [+49.4; +70.2] | 47 / 6 / 0 |

Paired per file against switchfile, numbers in right cell, family=office (files with numeric cells):

| Candidate | Difference, points [95 % CI] | first better / equal / worse |
|---|---:|---:|
| cloudconvert | +9.9 [+1.1; +19.3] | 16 / 29 / 4 |
| pymupdf4llm | +10.0 [+1.2; +19.3] | 16 / 30 / 3 |
| Docling | +25.0 [+13.5; +37.2] | 21 / 27 / 1 |
| pdfplumber + our wrapper | +48.7 [+35.2; +61.9] | 29 / 20 / 0 |
| markitdown | +54.3 [+41.3; +66.9] | 41 / 6 / 2 |

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

## Same value (added 2026-11-17)

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
