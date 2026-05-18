# NIRF 2025 — top institute rankings + placement data

Pulled from BigQuery: `avantifellows.external_data_sources.nirf_fact_aggregate`.
This table is maintained by the Avanti data team and aggregates per-institute
Mandatory-Disclosure data sheets that NIRF publishes annually on
[nirfindia.org](https://www.nirfindia.org/Rankings/2025/Ranking.html).

## Source

- **BigQuery table**: `avantifellows.external_data_sources.nirf_fact_aggregate`
- **Ranking year**: 2025 (latest, released August 2025)
- **Cohort academic_year**: 2023-24 (the most recent cohort with placement data)
- **Pull date**: see git commit timestamp

## Files

| File | What |
|---|---|
| `nirf_2025_top_institutes_placement.csv` | 987 rows: every ranked institute × programme-type with placement, across 8 NIRF categories (Engineering, Medical, Pharmacy, Management, Architecture & Planning, Law, Dental, Agriculture). |
| `nirf_2025_engineering_tier_aggregate.csv` | Engineering only, summarised by tier (Top 10 / 11-25 / 26-50 / 51-100). |

## Schema (key columns)

| Column | Meaning |
|---|---|
| `ranking_year` | NIRF cycle (e.g. 2025) |
| `ranking_category` | Engineering / Medical / Pharmacy / Management / Architecture and Planning / Law / Dental / Agriculture and Allied Sectors |
| `nirf_rank` | Rank within category (1 = best) |
| `institute_name`, `state`, `city` | Identity & geography |
| `overall_score` | NIRF score out of 100 |
| `academic_year` | Cohort year (e.g. 2023-24 = students who graduated in 2023-24) |
| `type` | Programme type — `UG [4 Years Program(s)]` (B.Tech), `UG [5 Years Program(s)]` (B.Arch, integrated), `PG [2 Year Program(s)]` (M.Tech / MS), `PG [3 Year Program(s)]`, `PG [5 Year Program(s)]` (dual degree) |
| `first_year_intake` | Students *admitted* in that cohort (entry year). NULL for the latest cohort whose entry-year metadata isn't filed. |
| `graduating_on_time` | Students who graduated in stipulated time (= cohort that took placement) |
| `students_placed` | Of those graduates, how many got placed |
| `median_salary` | Median annual salary in ₹ of placed students |

## Headline: NIRF Engineering Top-100, AY 2023-24 (B.Tech UG)

| Tier | Institutes | Graduates | Placed | Placement % | Avg median salary |
|---|---:|---:|---:|---:|---:|
| **Top 10** | 10 | 8,921 | 6,782 | **76.0%** | **₹18.72 L/yr** |
| Top 11-25 | 15 | 27,916 | 22,299 | 79.9% | ₹13.11 L |
| Top 26-50 | 25 | 35,592 | 24,447 | 68.7% | ₹11.51 L |
| Top 51-100 | 47 | 42,928 | 28,492 | 66.4% | ₹9.85 L |
| **TOTAL** | **97** | **115,357** | **82,020** | **71.1%** | — |

(NIRF doesn't publish per-college placement for ranks 101-300; only the top 100 is fully disclosed at the institute level — bands below are reported in aggregate.)

## How this connects to the rest of the pipeline

| Stage | Cohort size | Source |
|---|---:|---|
| Class XII passes 2024 | 1.29 crore | MoE 2024 board results |
| Class XII Science stream passes | ~61 lakh | MoE 2024 stream tables |
| Engineering UG total annual grads | ~8.3 lakh (AISHE 2021-22) → ~9 L projected 2023-24 | AISHE Table 35 + AICTE intake |
| **NIRF Top-100 Engineering UG grads** | **115,357** (~13% of all Engineering grads) | This file |
| **NIRF Top-100 Engineering placed** | **82,020** (~9% of all Engineering grads) | This file |
| NIRF Top-10 Engineering grads | 8,921 (~1% of all Engineering grads) | This file |

So the NIRF Top-100 engineering colleges produce roughly **1 in 8 engineering graduates** in India each year, and roughly **1 in 11 are placed from this elite tier**. The remaining ~87% of engineering grads come from non-NIRF-ranked or unranked colleges.

## Cross-check vs PLFS earnings

Per PLFS 2023-24, engineering degree holders aged 25-30 in regular salaried jobs earn an average of **₹4.90 lakh/year** (₹40,869/month).

NIRF Top-100 (B.Tech) median salary: **₹9.85 L (51-100) to ₹18.72 L (Top 10)**.

The gap implies that the non-NIRF-Top-100 cohort (~7-8 lakh engineering grads / year) earns substantially below the PLFS average — likely ₹2-4 lakh/year median, since the PLFS overall average is pulled up by the NIRF-elite tail.

## How to re-pull

```bash
bq query --use_legacy_sql=false --format=csv --max_rows=2000 \
'SELECT ranking_category, nirf_rank, institute_name, state, city, overall_score,
        academic_year, type, first_year_intake, graduating_on_time,
        students_placed, median_salary
   FROM `avantifellows.external_data_sources.nirf_fact_aggregate`
  WHERE ranking_year = 2025
    AND academic_year = "2023-24"
    AND students_placed IS NOT NULL
  ORDER BY ranking_category, nirf_rank, type' \
  > extractions/nirf_2025_top_institutes_placement.csv
```

Requires `bq` CLI authenticated against the `avantifellows` GCP project.

## Caveats

1. **NIRF top-100 ≠ "all good engineering colleges"** — NIRF coverage is voluntary; some institutions choose not to participate. Most major IITs/NITs/BITS/VIT/MNITs are in. State-tier engineering colleges are under-represented.
2. **Placement count = institution-reported** — colleges self-disclose; NIRF audits but not exhaustively.
3. **Median salary is a median, not mean** — top-tail placements (₹50L+ at IITs) don't pull the median up; the mean would be 1.5-2× higher.
4. **"Placed" includes higher-studies-cum-placement at some colleges** — definition is institution-discretionary.
5. **Ranks 101-300 band data is in NIRF but bucketed** — for fine-grained ranks beyond 100, need to query band-level data separately (`ranking_category = "Engineering"` + `nirf_rank IS NULL` filter exists in the table).
