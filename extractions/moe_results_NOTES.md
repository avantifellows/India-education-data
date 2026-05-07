# MoE Results of Secondary & Higher Secondary Examinations — extraction notes

Source PDFs (in `sources/`):

- `moe_results_secondary_hs_2020.pdf` — 89 pages (compact format)
- `moe_results_secondary_hs_2021.pdf` — 90 pages (compact format)
- `moe_results_secondary_hs_2022.pdf` — 190 pages (expanded format with management × category breakdowns)
- `moe_results_secondary_hs_2024.pdf` — 190 pages (expanded format)

(MoE didn't publish a 2023 edition. 2025 not yet out.)

The four reports cover Class X (Secondary) and Class XII (Higher Secondary)
exam results for **all 41-56 boards** — CBSE, CISCE, every state board, and
the open-school boards (NIOS + state opens).

Two CSVs are produced from these PDFs by `scripts/moe_results_*`:

## 1. `moe_results_overall_class_x_xii_2020-2024.csv`

Class X and Class XII overall pass figures (Annual + Supplementary, Regular
+ Private students, All Categories), board × year × gender.

**Schema (1,026 rows):**

| column | meaning |
|---|---|
| `year` | 2020, 2021, 2022, 2024 |
| `level` | `Class X` or `Class XII` |
| `state` | State / UT or 'Central' |
| `board` | Full board name (line breaks normalised; some board names may vary slightly across years — see board-name caveat below) |
| `gender` | `Boys`, `Girls`, `Total` |
| `registered` | Students registered (Reg+Private). **Null for 2020/2021** — that schema didn't include a Registered column |
| `appeared` | Students appeared (Reg+Private) |
| `passed_annual_and_supp` | Students passed (Annual + Supplementary combined) |
| `pass_percentage` | Pass rate % |

**Sanity check (all-India sum-of-boards Total Passed):**

| Year | Class X | Class XII |
|---|---:|---:|
| 2020 | 15,768,194 | 12,155,004 |
| 2021 | 18,973,895 | 14,456,792 |
| 2022 | 15,848,975 | 12,465,635 |
| 2024 | 16,337,153 | 12,929,386 |

(2021's spike is the COVID-era universal-promotion year; numbers reconcile
with totals reported on page 1 of each MoE PDF.)

## 2. `moe_results_class_xii_stream_2020-2024.csv`

Class XII stream-wise pass figures (Arts / Commerce / Science / Vocational
+ All-Streams total), board × year × social-category × gender.

**Schema (5,567 rows):**

| column | meaning |
|---|---|
| `year` | 2020, 2021, 2022, 2024 |
| `state` | |
| `board` | |
| `social_category` | `All Categories`, `Scheduled Caste`, `Scheduled Tribe` |
| `stream` | `All Streams`, `Arts`, `Commerce`, `Science`, `Vocational` |
| `gender` | `Boys`, `Girls`, `Total` |
| `students_passed` | Annual + Supplementary, Regular + Private |

The MoE PDF reports a "Share of Pass-Outs by Stream" percentage table in
the next slot (Tables 14/16/18 in 2020/2021, 32/34/36 in 2022/2024). We
**do not** extract those because they're directly derivable from the
counts here.

## Caveats — read these before analysing

### a) CBSE stream-wise breakdown is missing for 2020 and 2021

The MoE compilation publishes CBSE's All-Streams total for those two years,
but the per-stream split (Arts / Commerce / Science / Vocational) is
blacked out. CISCE/ICSE has stream data populated for all four years.

**Genuinely-blacked-out stream rows** (i.e., All-Streams total is
present but every individual stream is empty):

- CBSE 2020 (1,126,282 students with no stream split)
- CBSE 2021 (1,391,539 students with no stream split)
- CBSE 2022 has stream data, but Vocational got blacked out in some
  social-category cuts
- A handful of small Sanskrit / Madrasa / Open boards in 2021/2022

If you need CBSE stream splits for 2020/2021, the source is CBSE's own
press releases (`cbse.gov.in` / annual press releases issued in May–July of
the relevant year). A separate fill step from those press releases is the
cleanest route — the MoE compilation does not have it.

### b) 2020 PDF column-extraction is heuristic

The 2020 PDF was produced with a different layout from later years.
pdfplumber's automatic grid detection is unreliable on it: column positions
drift between pages and rows (one row's State name might be at physical
column 2, the next row's at column 3). The 2020 stream-wise extractor
therefore uses a "compress non-empty cells, assume streams in fixed
left-to-right order" heuristic.

This gives correct results when **all 5 streams** are populated, or when
**Vocational** alone is missing (the vast majority of cases). It can
mis-attribute values if a non-trailing stream (e.g., Commerce) is blacked
out for a board with the rest populated — that situation is rare in the
data but worth knowing.

If a 2020 row looks suspicious, cross-check against the source PDF
`sources/moe_results_secondary_hs_2020.pdf` page 69 onwards.

### c) 2020 / 2021 schema differs from 2022 / 2024

The older reports omit the **Registered** column for the overall tables.
They show: Appeared / Passed Annual / Passed Supplementary / Passed Annual
& Supplementary / Pass %. The newer reports show: Registered / Appeared /
Passed Annual & Supplementary / Pass %.

The unified output schema therefore has `registered` set to `NULL` for
2020 and 2021. `appeared`, `passed_annual_and_supp`, and
`pass_percentage` are populated for all four years.

### d) Board names vary slightly across years

The MoE re-types board names each year, so the same board can appear with
small textual differences across years (e.g., "Council for the Indian
School Certificate Examinations,New Delhi" vs ", New Delhi"; line breaks
get retained as spaces). For trend analysis, fuzzy-join on key tokens
(e.g., "CBSE", "CISCE", "Maharashtra State Board", "Bihar School
Examination Board") rather than exact-match on the board name string.

### e) Class X has no stream breakdown — that's by design, not a gap

In India, students choose a stream only entering Class XI. Class X is a
unified examination across all streams. The MoE compilation correctly
reflects this: Section A (Class X) has no stream tables.

### f) Coverage grew over time

- 2020 — 41 boards (38 Central/State + 3 open in Section B stream tables)
- 2021 — ~45 boards
- 2022 — ~46 boards (expanded format added management-wise breakdown)
- 2024 — ~46 boards regular + 12 open = 58 total in the report

Boards added over time include some smaller Sanskrit / Madrasa boards.
For trend analysis on a fixed set, restrict to boards present in all
four years.

## What we did NOT extract (potentially useful follow-ups)

- **Section A Tables 11/21 (Class X SC/ST overall)** and **Section B
  Tables 11/21 (Class XII SC/ST overall)** — pass figures by board for
  SC and ST students at the overall (non-stream) level. The stream-wise
  cut by SC/ST IS extracted; only the overall non-stream cut by SC/ST
  is omitted. Add if you need it.
- **Open School Board tables (Tables 31-42 in 2022/2024 Section A)** —
  NIOS, state open schools. Currently lumped into the regular tables
  inadvertently for some years; can be cleanly separated if needed.
- **Management-wise breakdown** (Govt / Govt Aided / Private Unaided /
  Others) — present in 2022 and 2024 reports as Section B Tables 1-30
  and Section A counterparts. Not in 2020/2021 reports.
- **Trend tables (Tables 43-45 in 2024)** — the report's own
  pre-computed 2014-2024 trend rollup. We instead build the trend by
  stacking the four annual reports.
- **Pass-out share (%) by stream** — tables 14/16/18 in 2020/2021 and
  32/34/36 in 2022/2024. Skipped — derivable from the stream-count CSV.
