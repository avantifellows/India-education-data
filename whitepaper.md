# India's education-to-employment funnel — a data-grounded picture

*Working paper. May 2026. Based on the open datasets and extracts in this repository.*

---

## Executive summary

Across 24.7 crore Indian school-going children, a narrow funnel produces a small elite tier of well-paid graduates while the vast majority — including most "STEM" graduates — emerge into low-paid, informal employment. The data shows:

- **49% of school children are in government schools; 40% in private fee-paying schools; 10% in government-aided** (UDISE+ 2024-25).
- **About 1.29 crore students pass Class XII each year**, of whom Science is now the largest stream at **47%** (overtaking Arts).
- **Girls have parity** in school enrolment (48%), Class 11-12 (50%), and Class XII Science (46%), but the parity breaks at college Engineering (29% female).
- **About 77.5 lakh UG graduates emerge each year**, but only **~2.6 lakh (3.3%) come from the four "elite" tiers** — IITs, NITs/IIITs, government MBBS colleges, and other NIRF-top-200 engineering schools — where placement rates are 70-100% and median salaries are ₹7-17 lakh.
- The other **~11.3 lakh STEM graduates (14.5% of all UG)** earn ₹2.7 lakh median at 36% regular-employment rates — statistically indistinguishable from a non-STEM degree.
- **About 80% of Indian households earn under ₹5 lakh/year**, yet capture an estimated ~10% of elite-STEM seats. A child from this group is **roughly 36 times less likely** to win an elite STEM seat than a child from the top 20%.

The "STEM premium" in India is therefore concentrated in roughly **the top 3% of college graduates**, and access to that tier is steeply gated by household income at the Class XI / JEE / NEET stage.

---

## 1. Approach and data philosophy

This paper synthesises the most current publicly available data on each stage of the Indian education pipeline:

| Stage | Primary source | Year |
|---|---|---|
| School enrolment | UDISE+ Dashboard (MoE) | 2024-25 |
| Class X & XII board results | MoE "Results of Secondary and Higher Secondary Examinations" | 2024 |
| Higher education enrolment + graduation | AISHE Final Report | 2021-22 (latest published) |
| Engineering capacity (current) | AICTE Annual Report + dashboard JSON API | 2024-25 / 2025-26 |
| Medical capacity (current) | NMC UG Seat Matrix | 2024-25 |
| Per-institute NIRF data | NIRF aggregate (BigQuery) + Avanti's College DB scorecards | 2025 cycle |
| Employment outcomes + earnings | Periodic Labour Force Survey (PLFS) Annual | 2023-24 |
| Household income distribution | PRICE ICE 360° survey + PLFS + CBDT income tax data | 2021-2024 |

We rely on three principles:

1. **Sectoral regulators trump aggregated rankings when both exist.** AICTE knows engineering capacity better than AISHE (AISHE has a 3-year lag); NMC knows MBBS seats better than anyone. AISHE remains the canonical source for non-regulated disciplines (Arts, Science, Commerce, etc.).
2. **Trend extrapolation where current data is missing.** AISHE 2021-22 is the latest released; AISHE 2022-23 / 2023-24 / 2024-25 are collected but unpublished. We linear-extrapolate the 2019-20 → 2021-22 panel forward to 2025-26 for disciplines without a sectoral regulator.
3. **PLFS triangulates everything downstream.** Where institutional placement data is absent (the long tail of non-NIRF colleges), PLFS unit data on actual wages and employment status by age × education × technical-education-bucket fills the gap.

All numbers in this paper are traceable: every figure points to a CSV in `extractions/` which points to a raw file in `sources/` (or a documented URL in `sources/SOURCES.md`).

---

## 2. The school stage — 24.7 crore children

**India has 24.7 crore students in school (Pre-K through Class XII)** as of UDISE+ 2024-25.

### Where they go to school

| Management type | Enrolment | Share | Girls share |
|---|---:|---:|---:|
| Government | 12.1 cr | **49.1%** | 51% |
| Private unaided (fee-paying) | 9.8 cr | **39.5%** | 44% |
| Government-aided | 2.6 cr | 10.3% | 49% |
| Unrecognised / madrasa / other | 0.3 cr | 1.1% | 43% |

The conventional narrative that "India is mostly government school" is increasingly out of date. **Nearly 40% of Indian school children are in fee-paying private schools** — a remarkable share for a low-income country. Boys are disproportionately represented in private schools (56%); girls disproportionately in government (51% of government enrolment) — families spend more on boys' education when paying out of pocket.

At Class 11-12 specifically, the picture shifts:
- Government drops to **40%** of Cls 11-12 enrolment
- Private unaided stays at **39%**
- Aided rises sharply to **21%** (state-board higher secondaries are disproportionately aided)

So at the Class XII pass-out level, the cohort is already skewed away from pure government schooling.

### Class XII pass-outs by stream (2024)

About **1.29 crore students pass Class XII** each year, with Science now the dominant stream:

| Stream | Annual passes | Share | Girls share |
|---|---:|---:|---:|
| **Science** | 61.0 lakh | **47%** | 46% |
| Arts | 49.2 lakh | 38% | 55% |
| Commerce | 16.8 lakh | 13% | 48% |
| Vocational | 2.3 lakh | 2% | 43% |

Science overtook Arts at the Class XII pass-out level over the last two decades. **Girls have effective parity at Class XII** (50% overall; 46% in Science specifically) — a much-improved starting position than the standard pipeline-loss narrative suggests.

### CBSE/CISCE share — the central-board fee-paying cohort

Of the 1.29 crore Class XII passes, roughly **14.2 lakh (11%) come from CBSE + CISCE after subtracting KV and JNV**. This is a useful proxy for the "fee-paying central-board urban cohort" — disproportionately middle-class and urban, disproportionately the supply pool for elite engineering/medical entrance exams.

State boards (the big ones being UP, Bihar, Maharashtra, Tamil Nadu, Karnataka, Madhya Pradesh, West Bengal) account for the remaining ~89% of Class XII passes.

---

## 3. The higher-education stage — 77.5 lakh UG graduates

Per AISHE 2021-22 (latest published), India produces **about 77.5 lakh undergraduate graduates each year** across all disciplines:

| Discipline | Annual UG graduates | Share | Female % |
|---|---:|---:|---:|
| **Arts** | 24.16 lakh | **31.2%** | 54% |
| **Science** (B.Sc) | 11.97 lakh | 15.4% | 54% |
| **Commerce** | 11.28 lakh | 14.5% | 50% |
| **Engineering & Technology** | 8.30 lakh | **10.7%** | **29%** |
| Education (B.Ed/D.El.Ed) | 7.04 lakh | 9.1% | 65% |
| Medical Science (MBBS + BDS + AYUSH + Pharm + Nursing) | 2.94 lakh | 3.8% | 62% |
| Social Science | 2.64 lakh | 3.4% | 51% |
| IT & Computer (BCA / B.Sc IT) | 2.58 lakh | 3.3% | 42% |
| Management (BBA) | 2.09 lakh | 2.7% | 40% |
| Law | 1.08 lakh | 1.4% | 33% |
| Other disciplines (40+ smaller categories) | ~5.4 lakh | 7.0% | varies |

**STEM-track UG (Engineering + IT/Computer + Medical) is 13.82 lakh per year — about 17.8% of all UG graduates.** The other 82% are Arts/Science/Commerce/Education/Management/Law graduates.

### The gender story at college

The girls-Engineering dropoff is real but not what the popular narrative implies. **Girls cross college Engineering's threshold at 29%** — but they dominate Education (65%), Medical (62%), Arts (54%), Science (54%), and Commerce (50%). The story isn't "girls don't go to college" — it's **"girls cluster into helping-profession and humanities disciplines and away from engineering, law, and management"**.

Even within Engineering, however, the female share has been steadily climbing: from **27.4% in 2014-15 to 31.6% in 2021-22** (AICTE dashboard data), with projections to 32-33% by 2025-26 — driven by the CSE-led intake surge attracting more female enrolment than legacy engineering branches.

---

## 4. The elite engineering and medical tier — 5-bucket split

We grouped all STEM-track UG graduates into five buckets based on the publishing institute's tier, to see where the well-paid jobs actually go:

| Bucket | Institutes | Annual grads | % of all UG | Employment % | Avg pay |
|---|---:|---:|---:|---:|---:|
| **1. IITs** | 23 | 15,647 | **0.20%** | **92%** | **₹17.2 L** |
| **2. NITs / IIITs** | 57 | 29,510 | 0.38% | 89% | ₹10.1 L |
| **3. Government MBBS** | 423 | 54,000 | 0.70% | **100%** | ₹7.0 L (Junior Resident start) |
| **4. NIRF Top-200 Engineering** (non-IIT/NIT/IIIT) | 137 | 155,398 | 2.00% | 71% | ₹7.5 L |
| **5. All other STEM** (non-elite engg + IT/Computer + non-MBBS medical) | thousands | **1,126,803** | **14.53%** | **36%** | **₹2.7 L** |
| **STEM-track UG total** | | 1,381,358 | 17.81% | | |
| Non-STEM UG (Arts/Sci/Com/Edu/Law/…) | | 6,372,865 | 82.19% | 28% | ~₹2.8 L |
| **ALL UG graduates** | | **7,754,223** | **100%** | | |

A few things become uncomfortably clear:

- **Only 3.3% of all UG graduates (~254K students) end up in the four elite tiers.** They capture nearly all of India's well-paid first-jobs (₹7-17 L) and 70-100% placement rates.
- **The remaining 14.5% of all UG who hold a STEM-track degree (1.13 million students) earn ₹2.7 L on average at 36% regular-employment rates** — statistically indistinguishable from a Bachelor's of Arts.
- **The IITs collectively produce just 15,647 graduates a year** — about 0.2% of all UG grads, or 1 in 500.
- **The NIRF top-200 engineering total of ~200K grads is roughly 22% of all engineering UG grads, but captures the vast majority of well-paid placements.** The other 78% of engineering graduates produce a long-tail cohort whose earnings (PLFS-derived ~₹2.3 L) are below the all-Class-XII-graduate baseline.

### Why bucket 5 is so much larger and worse-paid than people think

PLFS Annual 2023-24 tells us the average engineering graduate aged 25-30 in a regular salaried job earns ₹4.9 L/year. NIRF tells us the top 200 engineering colleges have median salaries of ₹7.5-18 L. Back-calculating, the *non-NIRF-top-200* engineering cohort (~6.3 lakh annual grads) must earn around ₹2.3 L/year on average — below the median pay of a generic Indian college graduate. Combined with similar PLFS readings for non-MBBS medical degrees (₹3.65 L) and BCA/BSc-IT (₹2.8 L), the entire "long tail of STEM" is paid like Arts/Science/Commerce.

This isn't a measurement artefact. It's the dominant reality of "engineering education" in India for the median Class XII Science student.

---

## 5. The access gap

We can compute the rough probability that a child from the bottom 80% of households (those earning under ₹5 lakh/year per PRICE ICE 360°) wins an elite STEM seat:

**Assume:**
- 1.30 crore Class XII pass-outs annually
- ~300,000 elite STEM seats (IIT + NIT + IIIT + NIRF top-200 engineering + government MBBS)
- Bottom 80% of households produce ~80% of Class XII grads (proportional baseline)
- Bottom 80% capture only ~10% of elite STEM seats (the working assumption — see caveats below)

**Then:**

| Pool | Class XII grads | Elite seats | Odds |
|---|---:|---:|---:|
| Bottom 80% of households (<₹5 L/yr) | 1.04 cr | 30,000 | **0.29%** |
| Top 20% of households | 26 lakh | 270,000 | **10.38%** |
| **Ratio** | | | **≈ 36×** |

**A child from the bottom 80% of Indian households is roughly 36 times less likely to win an elite-STEM seat than a child from the top 20%.**

The "10% of elite seats" figure is a working estimate rather than a published statistic — it's roughly consistent with the constitutional EWS quota (10% reservation for households below ₹8 L), with studies of IIT student backgrounds, and with the very steep urban-vs-rural and English-medium-vs-vernacular gradient in JEE/NEET success. If the true share is 15% instead of 10%, the ratio drops to 21×; if 5%, it rises to 76×. The headline conclusion — at least an order of magnitude gap — is robust to that range.

### Why the gap is so steep

Three reinforcing channels:

1. **English medium and CBSE/CISCE pipeline.** Elite engineering and medical entrance prep (JEE, NEET) is heavily skewed toward English-medium, CBSE/CISCE schooling, and is more accessible to students in urban centres with private coaching access. **~11% of Class XII grads come through CBSE + CISCE (excluding KV/JNV) — and roughly 80% of IIT/AIIMS-tier seats** flow through this gate.

2. **Coaching capture.** The JEE/NEET coaching industry (Kota, Hyderabad, Delhi-NCR) is a parallel education system costing ₹2-10 lakh over 2 years. Families below ₹5 L/yr cannot afford this without scholarship support. Within the elite-college population, a disproportionate share comes from coaching-saturated districts.

3. **Information asymmetry.** Stream choice at Class XI (Science vs Commerce vs Arts), entrance-exam selection, college-vs-coaching trade-offs — all require sophisticated information that doesn't reach first-generation college aspirants without a structured intervention.

---

## 6. Capacity is growing — but slowly, and on top of an old elite

The supply side is expanding. AICTE's approved first-year B.Tech intake reached **14.90 lakh seats in 2024-25** (a 67% increase from the 2017-18 trough) and **15.98 lakh in 2025-26** — an eight-year high, driven primarily by Computer Science / AI / data-science branches. NMC has added **about 64,000 MBBS seats since 2014**, including **+19,400 seats from 2024-25 to 2025-26 alone** — pushing MBBS capacity to 1.38 lakh seats across 816 colleges.

But headcount expansion alone doesn't change the access pattern. The elite-tier institutions (IITs, AIIMS, top-tier private engineering) are not expanding proportionally — their share of intake is shrinking even as their absolute numbers tick up slowly. The growth is concentrated in:

- **Private engineering colleges** (largely NIRF-unranked, low-tier placements)
- **New medical colleges in tier-2 and tier-3 districts** (better than no MBBS, but the rural-doctor compensation problem remains)
- **Computer Science / IT** branches across all tiers — including non-NIRF colleges where placement is uncertain

So the supply growth widens the "long tail" more than it broadens the elite. **The 36× access gap will narrow only if either (a) elite tier capacity grows materially or (b) the non-elite tier's placement outcomes improve markedly.** Neither is happening at the scale required.

---

## 7. Methodology notes and limitations

### Where each metric comes from

| Metric | Source |
|---|---|
| School enrolment by management | UDISE+ Dashboard Report 4000, AY 2024-25 |
| Class XII passes by board × stream | MoE "Results of Secondary and Higher Secondary Examinations 2024" |
| KV/JNV passes | KVS Annual Reports 2021-22, 2022-23, 2023-24 + NVS 2023-24 Appendix XI |
| AISHE UG grads by discipline | AISHE Final Report 2021-22, Tables 12 / 35 / 34a |
| AISHE 3-year linear extrapolation to 2025-26 | AISHE Final Reports 2019-20, 2020-21, 2021-22 |
| AICTE engineering intake current | AICTE Annual Report 2024-25 Table 2.1 + AICTE Dashboard API |
| AICTE engineering gender split | AICTE Dashboard JSON API (facilities.aicte-india.org) |
| NMC MBBS seats | NMC Revised UG Seat Matrix 2024-25 (31-Mar-2025) |
| NIRF rankings + per-institute placement | NIRF aggregate (BigQuery `external_data_sources.nirf_fact_aggregate`) for 2025 cycle; College DB scorecards (scraped per-institute NIRF Mandatory Disclosure PDFs) for institutes outside top-100 |
| Earnings + employment by education | PLFS Annual 2023-24, age 25-30, by PLFS technical-education bucket |
| Household income distribution | PRICE ICE 360° Survey 2021 + cross-check vs PLFS + CBDT income-tax filings |

### Caveats

1. **AISHE is 3 years behind.** Our latest published AISHE is 2021-22; 2022-23 has been "imminent" for 18+ months. Extrapolations beyond 2024 carry growing uncertainty. AICTE and NMC fill this for their sectoral coverage but most AISHE disciplines lack a sectoral regulator.

2. **PLFS technical-education buckets are very coarse.** PLFS has just 5 codes (Agriculture / Engineering / Medical / Crafts / Other), so it can't distinguish Engineering UG from Engineering Diploma, and it collapses Arts / Science / Commerce / Law into "Graduate non-technical". This forces the bucket-5 cohort in our STEM split to use PLFS readings that mix with non-STEM grads.

3. **NIRF top-200 doesn't include every elite engineering college.** Some major private institutions don't participate in NIRF. The 200K "elite" envelope is an under-count by maybe 10-15%.

4. **"Government MBBS = 100% placed" is technically true but not directly comparable to NIRF placement rates.** MBBS graduates enter clinical practice via compulsory internship → NEET-PG → specialisation or general practice. There is no "campus placement" event for MBBS. Starting Junior Resident salary in the government sector (₹56,000/month, 7th CPC) is the right comparator; post-PG specialist salary 4-6 years later (~₹15-25 L) is not.

5. **The 36× access gap rests on an unverified ~10% share assumption.** This is an educated estimate consistent with the constitutional EWS-quota share of 10% reservation, with student-background studies of IIT/IIM cohorts, and with the urban/English-medium-saturation of JEE/NEET top scorers. A rigorous study would survey current IIT/NIT/AIIMS students on family income. Until such data exists, treat the 36× as a working approximation in the 20× — 50× band.

6. **Household income data is imperfect.** PRICE ICE 360° asks self-reported income (under-reports affluent end); PLFS measures wage earnings only (under-reports self-employed and capital income); CBDT measures filers (under-reports informal sector). The "80% below ₹5 L" figure is the cross-source triangulated best estimate.

---

## 8. What to do with this

This document doesn't prescribe policy — that's outside its remit. But three observations might shape how to read it:

1. **The "STEM premium" framing is misleading for most Indians.** Telling a Class XI student "do Science / engineering / coding" is, on average, telling them to enrol in a long-tail college where they will graduate into ₹2-3 lakh/year informal employment. The premium is real only for the top 3% who reach an elite-tier institution.

2. **The access gap is at the entrance, not at school.** Girls have parity in school. Bottom-quintile students pass Class XII at similar rates to top-quintile students (when both attend school). The dramatic skew opens at the JEE/NEET/CUET stage — driven by coaching, English-medium-CBSE pipeline, and information asymmetry. Interventions that reach the bottom 80% at Class XI with structured coaching, scholarship-funded entrance prep, and information about non-obvious career paths (where placement-adjusted ROI is highest) would have the largest impact.

3. **Capacity is growing where it matters least.** New private engineering colleges add seats to a market where median wage is already below ₹3 L. New AIIMS and government medical colleges genuinely add elite capacity, but at a pace that won't close the access gap on a generation's time horizon. The binding constraint is not capacity; it's preparation quality and information access for bottom-80% households.

---

## Appendix — file references

All numbers in this paper trace to specific extractions:

| Section | CSV |
|---|---|
| §2 School enrolment | `sources/udise_2024-25_enrolment_by_location_category_management_class.xlsx` |
| §2 Class XII passes by stream | `extractions/moe_results_class_xii_stream_2020-2024.csv` |
| §2 Class XII overall passes | `extractions/moe_results_overall_class_x_xii_2020-2024.csv` |
| §2 KV/JNV residual | `extractions/kv_jnv_results_class_x_xii.csv` |
| §3 AISHE UG by discipline | `extractions/aishe_2021-22_outturn_ug_discipline.csv` |
| §3 AISHE 3-year panel + extrapolation | `extractions/aishe_ug_discipline_panel_2019-22.csv`, `extractions/aishe_ug_discipline_extrapolated_2024-26.csv` |
| §3 AICTE gender trend | `extractions/aicte_dashboard_panel_national_program_level.csv` |
| §4 5-bucket split | **`extractions/stem_pipeline_buckets_2024-25.csv`** |
| §4 IIT/NIT/IIIT scorecards | `extractions/iit_nit_iiit_scorecards.csv` |
| §4 NIRF 2025 institute-level placement | `extractions/nirf_2025_top_institutes_placement.csv` |
| §6 Current capacity 2025-26 | `extractions/higher_ed_capacity_2025-26_consolidated.csv` |

Per-dataset methodology notes:

- `extractions/aishe_2021-22_NOTES.md` — AISHE schema + classification caveats
- `extractions/moe_results_NOTES.md` — MoE board-results methodology + CBSE stream-data gap
- `extractions/kv_jnv_NOTES.md` — KV/JNV consolidation + "Private CBSE" derivation
- `extractions/higher_ed_capacity_2025-26_NOTES.md` — AISHE-vs-AICTE-vs-NMC reconciliation
- `extractions/nirf_2025_NOTES.md` — NIRF placement schema
- `sources/SOURCES.md` — every raw source URL + provenance

Repo: [github.com/avantifellows/India-education-data](https://github.com/avantifellows/India-education-data)
