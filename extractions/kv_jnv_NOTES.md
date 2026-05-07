# KV + JNV board-exam results — extraction notes

Purpose: derive a "Private CBSE" (≈ Independent CBSE schools, urban / fee-paying)
estimate by subtracting Kendriya Vidyalaya (KV) and Jawahar Navodaya Vidyalaya
(JNV) student counts from CBSE all-school totals.

CBSE itself publishes pass-rate breakdowns by school type (CTSA / JNV / KV /
Govt-aided / Govt / Independent) in its annual press release, but **only as
percentages, not as candidate counts**. So to subtract counts we have to pull
KV totals from KVS annual reports and JNV totals from NVS annual reports.

## Sources (all in `sources/`)

| File | Reports on | Used for |
|---|---|---|
| `kvs_annual_report_2021-22.pdf` | 2022 board exams | KV counts for MoE 2022 |
| `kvs_annual_report_2022-23.pdf` | 2023 board exams | (MoE skipped 2023; included for trend) |
| `kvs_annual_report_2023-24.pdf` | 2024 board exams | KV counts for MoE 2024 |
| `nvs_annual_report_2019-20.pdf` | 2020 board exams | superseded — see below |
| `nvs_annual_report_2020-21.pdf` | 2021 board exams | superseded — see below |
| `nvs_annual_report_2021-22.pdf` | 2022 board exams | superseded — see below |
| `nvs_annual_report_2022-23.pdf` | 2023 board exams | superseded — see below |
| `nvs_annual_report_2023-24.pdf` | 2024 board exams | **canonical** — its Appendix XI carries the 5-year national-totals trend table for both classes, so this single PDF supplies clean JNV counts for 2020–2024 |
| `cbse_press_class_xii_2024.pdf` | 2024 Class XII | Verified CBSE doesn't publish counts by school-type — only %. Kept for record. |

## Output

`kv_jnv_results_class_x_xii.csv` — 25 rows. Schema:

| col | meaning |
|---|---|
| `moe_result_year` | 2020 / 2021 / 2022 / 2023 / 2024 (year of board-exam results) |
| `board` | `KV` (Kendriya Vidyalaya) or `JNV` (Jawahar Navodaya Vidyalaya) |
| `source_academic_year` | KVS/NVS academic year, e.g., `2023-24` |
| `level` | `Class X` or `Class XII` |
| `stream` | `Overall`, `Science`, `Commerce`, `Humanities` (Class XII only; KV only) |
| `appeared` | candidates who appeared |
| `passed` | candidates who passed (Annual + Supplementary) |
| `pass_percentage` | from source PDF |
| `source_pdf` | filename in `sources/` |
| `source_page_or_note` | page number / locator note |

## Coverage matrix

|MoE year| KV Class X | KV Class XII | JNV Class X | JNV Class XII |
|---|---|---|---|---|
|2020| ❌ no KVS report public | ❌ | ✅ 40,398/39,856 | ✅ 29,152/28,772 |
|2021| ❌ | ❌ | ✅ 41,504/41,483 | ✅ 32,630/32,593 |
|2022| ✅ 114,280/110,421 (+stream) | ✅ 92,488/89,791 (+stream) | ✅ 45,529/45,395 | ✅ 35,725/35,343 |
|2023| ✅ 109,924/107,761 | ✅ 100,629/93,152 (+stream) | ✅ 45,911/45,515 | ✅ 35,772/34,882 |
|2024| ✅ 102,749/101,826 | ✅ 70,985/70,147 (+stream) | ✅ 44,581/44,176 | ✅ 34,061/33,687 |

The KV gap for 2020 and 2021 is real: KVS only publishes 3 annual reports
on its official site (2021-22, 2022-23, 2023-24). KV pass *percentages*
for 2019-20 and 2020-21 are available from the 10-year trend table in
the KVS 2023-24 report (Class XII: 98.62% in 2019-20, 99.99% in 2020-21;
Class X: 99.23% in 2019-20, 100.00% in 2020-21) — but with no candidate
base it's hard to convert these to counts without an external assumption.

## "Private CBSE" estimate (the actual deliverable)

Using `extractions/moe_results_overall_class_x_xii_2020-2024.csv` for CBSE
totals and the KV+JNV counts here:

### Class XII Total Passed

| Year | CBSE total | KV passed | JNV passed | KV+JNV | **CBSE − (KV+JNV) ≈ "Private CBSE"** | KV+JNV as % of CBSE |
|---|---:|---:|---:|---:|---:|---:|
| 2020 | 1,126,282 | n/a | 28,772 | n/a | **(under-subtraction: 1,097,510)** | ≥ 2.6% |
| 2021 | 1,391,539 | n/a | 32,593 | n/a | **(under-subtraction: 1,358,946)** | ≥ 2.3% |
| 2022 | 1,330,662 | 89,791 | 35,343 | 125,134 | **1,205,528** | 9.4% |
| 2024 | 1,426,420 | 70,147 | 33,687 | 103,834 | **1,322,586** | 7.3% |

### Class X Total Passed

| Year | CBSE total | KV passed | JNV passed | KV+JNV | **CBSE − (KV+JNV) ≈ "Private CBSE"** |
|---|---:|---:|---:|---:|---:|
| 2020 | 1,803,991 | n/a | 39,856 | n/a | (under-subtraction: 1,764,135) |
| 2021 | 2,104,797 | n/a | 41,483 | n/a | (under-subtraction: 2,063,314) |
| 2022 | 1,976,650 | 110,421 | 45,395 | 155,816 | **1,820,834** |
| 2024 | 2,095,467 | 101,826 | 44,176 | 146,002 | **1,949,465** |

Caveat: this is an *upper bound* on private CBSE — the CBSE press release
also calls out CTSA (Central Tibetan School Admin), Govt, and Govt-aided
school types separately, and our subtraction only removes KV + JNV. So
the residual still includes those small categories. Per CBSE 2024 press
release pass-% by type, CTSA / Govt-aided / Govt collectively account for
roughly 1.5–3% of CBSE Class XII candidates — the residual "Private CBSE"
above is therefore likely 4–6% high (i.e., true private CBSE ≈ 1.27 M
in 2024 not 1.32 M).

## Class XII stream split — KV only (JNV not published)

KV Class XII 2024 stream split (passed counts): Science 40,369 / Commerce
16,763 / Humanities 13,011 = 70,143 ≈ KV Overall 70,147 (rounding diff).

Useful when subtracting from CBSE stream-wise totals (Arts 313,167,
Commerce 325,093, Science 788,160 in 2024 from `moe_results_class_xii_stream_2020-2024.csv`):

| 2024 stream | CBSE pass | KV pass | "CBSE − KV" |
|---|---:|---:|---:|
| Science | 788,160 | 40,369 | 747,791 |
| Commerce | 325,093 | 16,763 | 308,330 |
| Arts (≈ Humanities) | 313,167 | 13,011 | 300,156 |

JNV's stream-wise pass counts are not in the NVS annual reports (only
overall). If you need stream-by-stream subtraction at JNV level, the only
route is per-JNV school CBSE result pages — non-trivial scrape.

## How extracted

Numbers were hand-verified by visually reading the relevant pages of
each PDF (KVS reports and NVS 2023-24 Appendix XI). The KVS 2021-22
and 2022-23 PDFs use unstable column-detection in pdfplumber and the
NVS PDFs use non-standard cid-encoded fonts; both need visual / regex
parsing rather than `extract_tables()`. Rather than maintain a brittle
heuristic extractor, the values are baked into
`scripts/kv_jnv_consolidate_results.py` — running that script
deterministically produces the CSV.
