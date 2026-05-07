# India education data

Cleaned, machine-readable extracts from the Indian government's public school-
and higher-education statistics reports. Each dataset is paired with the
script that produced it from the underlying PDF / XLSX source, so the pipeline
is auditable end-to-end.

## Layout

```
sources/        Raw downloaded files (PDFs, XLSX) — kept as-is
scripts/        Python scripts that parse sources -> extractions
extractions/    Tidy long-form CSVs + per-dataset NOTES.md
outputs/        (reserved for analytical deliverables)
```

`sources/SOURCES.md` lists every source file with its provenance URL.
`extractions/*_NOTES.md` documents schemas, validation, and known gaps for
each CSV.

## Datasets

### UDISE+ (school enrolment)

| File | What |
|---|---|
| [`extractions/udise_2024-25_*`](extractions/) | Source XLSX preserved in `sources/`. State × management × school-category × class enrolment for AY 2024-25, all 36 states/UTs, with every class Cls-1 to Cls-12 broken out by gender. From UDISE+ Dashboard Report 4000. |

### AISHE 2021-22 (higher education)

Latest published AISHE — 2022-23 / 2023-24 / 2024-25 are collected but not yet released by MoE.

| File | Cut |
|---|---|
| [`extractions/aishe_2021-22_outturn_state_level.csv`](extractions/) | State × level (PhD / M.Phil / PG / UG / Diploma / Cert / Integrated) × gender → out-turn |
| [`extractions/aishe_2021-22_outturn_ug_discipline.csv`](extractions/) | UG discipline × gender → out-turn |
| [`extractions/aishe_2021-22_outturn_programme_by_social_category.csv`](extractions/) | 227 programmes × 8 social categories × gender → out-turn (national) |
| [`extractions/aishe_2021-22_programme_to_discipline_mapping.csv`](extractions/) | Audit-able heuristic: programme name → AISHE discipline |
| [`extractions/aishe_2021-22_outturn_discipline_by_social_category.csv`](extractions/) | Programme rollup → discipline level |
| [`extractions/aishe_2021-22_NOTES.md`](extractions/aishe_2021-22_NOTES.md) | **Read first.** Caveats: AISHE Tables 35 vs 34a use incompatible classification paradigms (subject vs degree-name); Indian Language and Social Science cuts are not recoverable from the programme rollup. |

### MoE board examination results 2020 / 2021 / 2022 / 2024

MoE didn't publish a 2023 edition. 2024 is latest.

| File | Cut |
|---|---|
| [`extractions/moe_results_overall_class_x_xii_2020-2024.csv`](extractions/) | Class X + Class XII overall results, year × board × gender → registered, appeared, passed, pass% |
| [`extractions/moe_results_class_xii_stream_2020-2024.csv`](extractions/) | Class XII stream-wise (Arts / Commerce / Science / Vocational), year × board × social_category × stream × gender → passed |
| [`extractions/moe_results_NOTES.md`](extractions/moe_results_NOTES.md) | Schema, gaps, sanity-checks. CBSE stream breakdown is genuinely missing in 2020 and 2021 (the MoE compilation gives only the All-Streams total for CBSE in those years). |

### KV + JNV — for "Private CBSE" estimation

CBSE itself publishes pass-% by school type (CTSA / JNV / KV / Govt-aided / Govt / Independent) but **not candidate counts** by type. To estimate "Private CBSE" graduates, subtract KV + JNV pass counts from CBSE total. KV counts are from KVS annual reports; JNV counts from NVS annual reports.

| File | What |
|---|---|
| [`extractions/kv_jnv_results_class_x_xii.csv`](extractions/) | year × board (KV / JNV) × class × stream → appeared, passed, pass% |
| [`extractions/kv_jnv_NOTES.md`](extractions/kv_jnv_NOTES.md) | Includes the "Private CBSE" subtraction table for 2022 and 2024. KV counts unavailable for 2020 / 2021 (KVS only publishes 3 recent annual reports). |

## How to use

Each `extractions/*_NOTES.md` is the canonical doc for that dataset — schema, validations, caveats, and any known data quality issues. Read these before joining or aggregating across datasets.

Each script in `scripts/` is deterministic: re-running it on the same `sources/` produces identical CSV output. To regenerate from scratch:

```bash
python3 scripts/aishe_2021-22_01_state_level_outturn.py
python3 scripts/aishe_2021-22_02_ug_discipline_outturn.py
python3 scripts/aishe_2021-22_03a_programme_outturn_by_social_category.py
python3 scripts/aishe_2021-22_03b_programme_to_discipline_mapping.py
python3 scripts/aishe_2021-22_03c_outturn_discipline_by_social_category.py
python3 scripts/moe_results_01_extract_class_xii_stream.py
python3 scripts/moe_results_02_extract_overall.py
python3 scripts/kv_jnv_consolidate_results.py
```

Dependencies: `python>=3.10`, `pdfplumber`, `openpyxl`. NVS PDFs (gitignored) need to be downloaded separately — see [sources/SOURCES.md](sources/SOURCES.md).

## Adding a dataset

1. Drop the raw source(s) into `sources/` and add the URL/provenance to `sources/SOURCES.md`.
2. Write a parser in `scripts/` named `<dataset>_NN_<step>.py`.
3. Output to `extractions/` as long-form CSV.
4. Document schema, validation, and known caveats in `extractions/<dataset>_NOTES.md`.
