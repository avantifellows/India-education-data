# Higher-education capacity AY 2025-26 — methodology

This is a *current dataset* exercise: the goal is to produce 2025-26 estimates that match the 2024-25 UDISE / Class XII data we already have, since AISHE itself is 3 years behind.

## Sources, by tier of authority

### Tier 1 — sectoral regulators (preferred where available)

These bodies regulate seat capacity directly and publish updated figures every year. Their numbers are *current* (2024-25 / 2025-26), not lagged. We use them in preference to AISHE wherever they cover the discipline.

| Authority | Disciplines covered | Latest year | Source |
|---|---|---|---|
| **AICTE** (All India Council for Technical Education) | Engineering, Pharmacy, MBA, MCA, Architecture, Hotel Mgmt | 2025-26 approval cycle | aicte.gov.in / aicte-india.org dashboard + media reporting |
| **NMC** (National Medical Commission) | MBBS only (allopathic medicine) | 2024-25 + 2025-26 announced | [NMC UG Seat Matrix 2024-25](https://www.nmc.org.in/wp-content/uploads/2025/04/Revised%20UG%20Seat%20Matrix%202024-25%20on%2031-03-2025.pdf) (in `sources/`) |

### Tier 2 — AISHE linear extrapolation

For disciplines without a sectoral regulator (Arts, Science, Commerce, Education, Social Science, Indian Language, Foreign Language, Library Science, Physical Education, Law, Agriculture, etc.), we extrapolate from the 3-year AISHE panel:

- AISHE 2019-20 (Final Report Excel)
- AISHE 2020-21 (Final Report Excel)
- AISHE 2021-22 (Final Report Excel — latest available)

Method: simple linear least-squares fit on (year, value) for each (discipline × gender × metric) tuple. Project to 2024-25 and 2025-26.

The fit and projection are in `aishe_ug_discipline_extrapolated_2024-26.csv`. Source code: `scripts/aishe_panel_02_extrapolate_to_2025-26.py`.

## Output

- `aishe_ug_discipline_panel_2019-22.csv` — clean 3-year AISHE panel (688 rows: 3 years × ~40 disciplines × {enrolment, out-turn} × {Male, Female, Total}).
- `aishe_ug_discipline_extrapolated_2024-26.csv` — projections to 2024-25 and 2025-26 for every discipline × gender × metric.
- `higher_ed_capacity_2025-26_consolidated.csv` — **the headline file**: AICTE + NMC (where available) + AISHE-extrapolated (everywhere else), one row per (discipline, metric, year).

## What AICTE actually publishes — and what it doesn't

**Three AICTE source channels used:**

1. **AICTE Annual Report 2024-25 PDF** (`sources/aicte_annual_report_2024-25.pdf`, 312 pages) — Table 2.1 lists approved-intake by programme for AY 2023-24 vs AY 2024-25. Engineering & Technology total = 26.14 lakh approved seats (UG+PG+Diploma combined). **No gender breakdown in the AR PDF** — the only gender-specific content is on AICTE's Pragati / Saraswati scholarship beneficiaries (small subset).

2. **AICTE Dashboard** (`facilities.aicte-india.org/dashboard/...`) — *this is where the gender data lives.* The dashboard exposes a JSON API at `dashboard/pages/php/dashboardserver.php` that returns scalar `girls` / `boys` enrolment counts per (year, program, level, state, institution-type) filter combination, plus 11-year arrays for intake / enrolment / passed / placed. Coverage: **2012-13 through 2021-22 reliably; 2022-23 is incomplete in the live dashboard** (enrolment dropped to ~31K from ~826K — clearly partial reporting). 2023-24, 2024-25, 2025-26 are not yet in the dashboard (only intake / press-release figures available for those years).

3. **AICTE press releases** — first announce AY-specific top-line numbers (15.98 lakh first-year B.Tech intake for 2025-26, 5,875 institutions, +7% YoY) before the Annual Report PDF lands.

**What AICTE does NOT publicly publish:**

- **SC / ST / OBC / EWS social-category breakdown** — the dashboard has no filter for this and the AR doesn't break enrolment out by category. AICTE collects category data via its DCF (Data Capture Format) but only publishes scholarship beneficiary counts under category. AISHE has SC / ST / OBC / Muslim / Other Minority / EWS / PwD breakdowns at programme level (Table 34a), so for that cut see the AISHE extracts.
- **Family income / parental occupation / parental education** — these are collected on the DCF (specifically for fee-waiver and EWS-eligibility checks) but AICTE does **not** publish aggregates anywhere we can find. To get this you'd need either: (a) RTI request to AICTE for anonymised aggregate, (b) IHDS / NSS survey data which has tertiary-education by household characteristics, or (c) the Society of Women Engineers' India Tertiary Education research that occasionally cites AICTE pull-data.

## Engineering UG female % — actual AICTE dashboard data 2012-22

Pulled directly from `facilities.aicte-india.org` API (see `scripts/aicte_dashboard_pull_panel.py`, output in `extractions/aicte_dashboard_panel_2012-2023.csv`):

| Year | Approved Intake | Enrolled | Girls | Boys | Female % |
|---|---:|---:|---:|---:|---:|
| 2012-13 | 15.49 lakh | 9.66 lakh | 320,284 | 645,913 | 33.1% |
| 2013-14 | 16.34 lakh | 9.45 lakh | 260,050 | 684,342 | 27.5% |
| 2014-15 | 17.05 lakh | 8.75 lakh | 240,179 | 635,058 | 27.4% |
| 2015-16 | 16.31 lakh | 8.55 lakh | 238,347 | 616,665 | 27.9% |
| 2016-17 | 15.57 lakh | 7.86 lakh | 228,165 | 557,797 | 29.0% |
| 2017-18 | 14.76 lakh | 7.51 lakh | 219,774 | 530,573 | 29.3% |
| 2018-19 | 14.05 lakh | 7.22 lakh | 212,320 | 509,643 | 29.4% |
| 2019-20 | 13.29 lakh | 7.41 lakh | 217,171 | 524,016 | 29.3% |
| 2020-21 | 12.87 lakh | 7.19 lakh | 213,408 | 500,074 | 29.9% |
| 2021-22 | 12.53 lakh | 8.26 lakh | 231,435 | 500,088 | 31.6% |
| **2025-26 (projected)** | **15.98 lakh** | — | — | — | **32.8%** (linear fit on 2014-22 trend) |

The 2012-13 row's high 33.1% female is anomalous (likely data-quality issue in the early dashboard data) — the steady trend from 2014-15 onward is the reliable signal. Female % bottomed out at ~27% in the engineering-bubble peak (2014-15) and has climbed steadily ever since, breaching 31% in 2021-22. Linear fit on 2014-22 projects ~32.8% for 2025-26.

**Note**: girls + boys enrolled does NOT equal approved intake (approved intake is seats; enrolled is actual students that filled them; vacancy was 25-45% historically, dropping to 16% in 2024-25). Female % is computed on enrolled, which is the more meaningful denominator for "who is actually doing engineering".

## Headline numbers (AY 2025-26)

### Engineering — from AICTE (authoritative, current)

- **15.98 lakh first-year B.Tech / B.E. seats approved across 5,875 institutions** (+7% YoY)
- 2024-25 baseline: 14.90 lakh approved, 12.53 lakh filled (vacancy 16.4%)
- Discipline mix in 2024-25 first-year fill: CSE 31% (3.90 lakh), Mech 19%, Civil 14%, ECE 13%, Electrical 10%, others 13%
- AICTE Dashboard year-by-year gender splits (above) show female % climbing 27.4% (2014-15) → 31.6% (2021-22). Projection for 2025-26 = ~32.8%.

### MBBS — from NMC (authoritative, current)

- **1,37,600 MBBS seats across 816 colleges in 2025-26** (up from 1,18,190 / 780 in 2024-25)
- Management mix (2024-25): Govt 48.3%, Trust 38.9%, Society 6.3%, Private 3.7%, mixed 2.8%
- Net seat addition over decade: ~64,000 seats since 2014 (54% growth; pace has accelerated post-2020)

### Annual graduates by discipline — from AISHE extrapolation (2025-26 estimate)

| Discipline | 2021-22 actual | 2025-26 projected | 4-yr growth | Female % |
|---|---:|---:|---:|---:|
| Arts | 24.16 lakh | **31.33 lakh** | +29.7% | 50.0% |
| Commerce | 11.28 lakh | **15.12 lakh** | +34.0% | 45.8% |
| Science | 11.97 lakh | **14.21 lakh** | +18.7% | 52.0% |
| Education | 7.04 lakh | **8.06 lakh** | +14.6% | 59.0% |
| IT & Computer | 2.58 lakh | **4.31 lakh** | +66.8% | 36.6% |
| Medical Science (broad) | 2.94 lakh | **3.98 lakh** | +35.7% | 56.0% |
| Social Science | 2.64 lakh | **3.96 lakh** | +49.9% | 49.0% |
| Management | 2.09 lakh | **3.35 lakh** | +60.1% | 36.7% |
| Law | 1.08 lakh | **1.55 lakh** | +43.2% | 32.4% |

## Caveats — please read

### a) AICTE intake ≠ AISHE graduates

AICTE numbers are **first-year approved seats** for the upcoming academic year. AISHE numbers are **annual graduates** (final-year passers, lagged 3-4 years from when they entered). The two are not directly comparable:

- AICTE 2025-26 first-year intake (15.98 lakh) → these students will graduate 2028-29
- AICTE 2021-22 first-year intake → these students graduated 2024-25
- AISHE 2021-22 reports graduates from cohorts that entered 2017-18

For "engineering capacity in 2025-26", AICTE is the right metric. For "engineering graduates produced in 2025-26", you'd want AICTE's 2021-22 first-year intake × completion rate. We don't have completion rate; AISHE 2021-22 implies it's ~65% (8.3 lakh AISHE-reported E&T graduates ÷ ~12-13 lakh AICTE 2017-18 intake).

### b) Why is engineering "+0.6%" CAGR in our AISHE panel but AICTE shows seats growing 7%?

AISHE 2019-20 → 2021-22 captured the *tail end of engineering's decline* (oversupply from the early 2010s boom and many seats going unfilled). AICTE then *lifted intake caps* and CSE-led demand surged post-2022 — so 2024-25 / 2025-26 are growth years that the AISHE linear fit doesn't see. **The AISHE-extrapolated +2.4% growth for Engineering through 2025-26 is therefore an underestimate**; AICTE's data showing +67% growth from 2017-18 trough to 2024-25 is the truer picture.

This is why we use AICTE for Engineering, not the AISHE extrapolation.

### c) Linear extrapolation overstates fast-growing disciplines

IT & Computer +66.8%, Management +60.1%, Social Science +49.9%, Law +43.2% — these are linear-fit projections from a 3-year panel that captured a period of expanding AISHE response coverage (more colleges responding each year). Some of the apparent "growth" is simply better measurement. **Treat 4-year growth >40% with skepticism** — the real number is likely 50-70% of what's projected for these disciplines.

### d) Linear extrapolation works better for stable disciplines

Arts (+29.7%), Commerce (+34.0%), Science (+18.7%), Education (+14.6%) — these are the disciplines with high coverage already in 2019-20 AISHE, so the year-on-year growth captured is closer to real growth. Use these projections more confidently.

### e) Medical Science is broader than MBBS

AISHE's "Medical Science" includes MBBS + BDS (dental) + AYUSH (BAMS/BHMS/BUMS) + B.Pharm + B.Sc Nursing + several other allied health programmes. NMC only regulates MBBS (~1.18 lakh seats in 2024-25), which is roughly 30-35% of the broader Medical Science discipline as AISHE counts it (2.94 lakh graduates 2021-22). For a full medical-pharmacy-nursing capacity picture we'd also need DCI (dental), PCI (pharmacy), INC (nursing), CCIM (Indian medicine).

### f) What this dataset *isn't*

- Not state-wise (the consolidated CSV is national totals only — though the underlying NMC PDF + AICTE state-wise data could give us state breakdown if needed)
- Not by gender for AICTE/NMC numbers (those publishers don't break out enrolment by gender at this aggregate level; use the AISHE-derived female share % as a baseline)
- Not actual 2025-26 graduates — for forecasted *graduates in 2025-26* you need AICTE / NMC enrolment from ~4 years prior × completion rate. We have the inputs but didn't compute that derivation.

## Reproducing this dataset

```bash
# 1. Download AISHE source Excels (already in sources/, but to refresh):
#    Already documented in sources/SOURCES.md

# 2. Build the 3-year AISHE panel
python3 scripts/aishe_panel_01_extract_ug_discipline_3year.py

# 3. Linear-extrapolate to 2024-25 and 2025-26
python3 scripts/aishe_panel_02_extrapolate_to_2025-26.py

# 4. Combine with AICTE/NMC current-year data
python3 scripts/higher_ed_capacity_2025-26_consolidated.py
```

When AISHE 2022-23 / 2023-24 / 2024-25 are eventually released by MoE, re-run step 2 with the additional years and the projection becomes much firmer (5-year linear fit instead of 3).
