# India education data

Cleaned, machine-readable extracts from the Indian government's public school- and higher-education statistics. Each dataset is paired with the script that produced it from the underlying PDF / XLSX / dashboard source, so the pipeline is auditable end-to-end.

## Layout

```
sources/         Raw downloaded files (PDFs, XLSX) — kept as-is + SOURCES.md
scripts/         Python scripts that parse sources → extractions
extractions/     Tidy long-form CSVs + per-dataset NOTES.md
outputs/         (reserved for analytical deliverables)
```

Each `extractions/*_NOTES.md` is the canonical doc for that dataset — schema, validations, caveats. Read these before joining or aggregating across datasets.

## Datasets and how they fit together

The story arc, from school through to "what comes out the other end":

### School pipeline

| Topic | Script(s) | Extraction CSVs | Notes |
|---|---|---|---|
| **UDISE+ 2024-25** — state × management × Cls 1-12 enrolment | (XLSX from dashboard, no script — `sources/udise_2024-25_…xlsx` is already long-form) | — | Reference XLSX in `sources/` |
| **MoE board results 2020/21/22/24** — Class X + XII, all 56 boards | `moe_results_01_extract_class_xii_stream.py`, `moe_results_02_extract_overall.py` | `moe_results_overall_class_x_xii_2020-2024.csv` (1,026 rows), `moe_results_class_xii_stream_2020-2024.csv` (5,567 rows) | [`moe_results_NOTES.md`](extractions/moe_results_NOTES.md) |
| **KV + JNV passes** — for "Private CBSE" estimation | `kv_jnv_consolidate_results.py` | `kv_jnv_results_class_x_xii.csv` | [`kv_jnv_NOTES.md`](extractions/kv_jnv_NOTES.md) |
| **NAS 2021** — national-level student proficiency by subject × grade | `nas_2021_aggregate_national.py` | `nas_2021_national_proficiency.csv` | [`nas_2021_national_proficiency_NOTES.md`](extractions/nas_2021_national_proficiency_NOTES.md) |

### Higher-education pipeline

| Topic | Script(s) | Extraction CSVs | Notes |
|---|---|---|---|
| **AISHE 2021-22** — UG out-turn by state × level, by discipline, by social category | `aishe_2021-22_01_…`, `aishe_2021-22_02_…`, `aishe_2021-22_03a/b/c_…` (5 scripts) | `aishe_2021-22_outturn_*.csv` (4 files) + `aishe_2021-22_program_to_discipline_mapping.csv` | [`aishe_2021-22_NOTES.md`](extractions/aishe_2021-22_NOTES.md) |
| **AISHE 2019-22 panel** — 3-year trend, linear extrapolation to 2025-26 | `aishe_panel_01_extract_ug_discipline_3year.py`, `aishe_panel_02_extrapolate_to_2025-26.py` | `aishe_ug_discipline_panel_2019-22.csv`, `aishe_ug_discipline_extrapolated_2024-26.csv` | See `higher_ed_capacity_2025-26_NOTES.md` |
| **AICTE dashboard panels** — engineering/management/MCA/pharmacy intake + gender 2012-2023, at national / state / institution-type cuts | `aicte_dashboard_pull_panel.py` | `aicte_dashboard_panel_national_program_level.csv`, `…_state_program_level.csv`, `…_inst_type_program_level.csv` | Methodology in `higher_ed_capacity_2025-26_NOTES.md` |
| **Higher-ed capacity AY 2025-26** — consolidated current-year view using AICTE + NMC + AISHE-extrapolated | `higher_ed_capacity_2025-26_consolidated.py` | `higher_ed_capacity_2025-26_consolidated.csv` | [`higher_ed_capacity_2025-26_NOTES.md`](extractions/higher_ed_capacity_2025-26_NOTES.md) |
| **NIRF 2025 placement data** — per-institute graduates, placement, median salary across 8 categories | (pulled via BQ — `avantifellows.external_data_sources.nirf_fact_aggregate`) | `nirf_2025_top_institutes_placement.csv` (987 rows), `nirf_2025_engineering_tier_aggregate.csv` | [`nirf_2025_NOTES.md`](extractions/nirf_2025_NOTES.md) |
| **IIT / NIT / IIIT scorecards** — placement + median salary per institute, sourced from each institute's NIRF Mandatory Disclosure PDF (via Avanti's College DB) | (joined from `../College DB/`) | `iit_nit_iiit_scorecards.csv` (81 rows) | — |

### Headline synthesis

| Topic | Script | Extraction CSV |
|---|---|---|
| **STEM-track UG pipeline buckets** — 5 buckets (IITs / NITs+IIITs / Govt MBBS / NIRF Top-200 Eng / All other STEM) with grads, % of all UG, employment rate, avg pay | `stem_pipeline_buckets_2024-25.py` | `stem_pipeline_buckets_2024-25.csv` |

The final 5-bucket file is the headline deliverable — it combines AISHE volume baselines, NIRF/College-DB elite-institute scorecards, NMC govt-MBBS counts, and PLFS earnings (from `../PLFS/`) into a single comparable view.

## Regenerate end-to-end

Dependencies: `python>=3.10`, `pdfplumber`, `openpyxl`. NVS PDFs (gitignored) need separate download — see [sources/SOURCES.md](sources/SOURCES.md). AICTE dashboard pull requires internet.

```bash
# School pipeline
python3 scripts/moe_results_01_extract_class_xii_stream.py
python3 scripts/moe_results_02_extract_overall.py
python3 scripts/kv_jnv_consolidate_results.py
python3 scripts/nas_2021_aggregate_national.py

# AISHE pipeline (5 sequential scripts)
python3 scripts/aishe_2021-22_01_state_level_outturn.py
python3 scripts/aishe_2021-22_02_ug_discipline_outturn.py
python3 scripts/aishe_2021-22_03a_program_outturn_by_social_category.py
python3 scripts/aishe_2021-22_03b_program_to_discipline_mapping.py
python3 scripts/aishe_2021-22_03c_outturn_discipline_by_social_category.py

# AISHE 3-year panel + extrapolation
python3 scripts/aishe_panel_01_extract_ug_discipline_3year.py
python3 scripts/aishe_panel_02_extrapolate_to_2025-26.py

# AICTE dashboard (network-bound, ~5 min)
python3 scripts/aicte_dashboard_pull_panel.py

# Consolidations
python3 scripts/higher_ed_capacity_2025-26_consolidated.py
python3 scripts/stem_pipeline_buckets_2024-25.py
```

## Cross-repo dependencies

This repo reads from two siblings (no writes):

- **`../PLFS/`** — Periodic Labour Force Survey unit data, for age-25-30 employment rate + earnings by education bucket. Used to fill rows in `stem_pipeline_buckets_2024-25.csv` where NIRF placement data isn't available.
- **`../College DB/`** — Avanti's curated NIRF Mandatory-Disclosure-PDF scorecards per IIT/NIT/IIIT. Used to fill institutes that NIRF aggregate (BQ table) excludes from top-100 (notably IIT Goa).

## Adding a dataset

1. Drop the raw source(s) into `sources/` and add the URL/provenance to [`sources/SOURCES.md`](sources/SOURCES.md).
2. Write a parser in `scripts/` named `<dataset>[_NN_<step>].py`.
3. Output to `extractions/` as long-form CSV.
4. Document schema, validation, and known caveats in `extractions/<dataset>_NOTES.md`.
