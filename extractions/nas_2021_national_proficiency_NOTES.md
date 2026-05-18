# NAS 2021 national proficiency aggregates

Output of `scripts/nas_2021_aggregate_national.py`.

## What this file is

National-level (cross-state) aggregates of NAS 2021 performance by management
(state govt / govt aided / private recognised / central govt) and by location
(rural / urban), for Classes 3, 5, 8, 10 across all NAS subjects (language,
math, evs, sst, sci, eng, mil).

NAS publishes only state-level percent-correct data and proficiency-band
shares. The national figures here are **student-weighted** aggregates of
state values, using state participation counts × management-share-of-
participation as weights.

## Source

`gsidhu/NAS-2021-data` — scrape of nas.gov.in dashboard, cloned to
`sources/nas_2021_data/`. Rights belong to MoE/NCERT; this is a clean
aggregation of their public dashboard data.

## Columns

| col | meaning |
|---|---|
| grade | 3 / 5 / 8 / 10 |
| subject | language / math / evs / sst / sci / eng / mil |
| dimension | "management" or "location" |
| category | one of: State Govt, Govt Aided, Private Recognised, Central Govt, Rural, Urban |
| pct_correct_mean | average % correct on test (national student-weighted) |
| pct_proficient_advanced | % of students at Proficient or Advanced (top tail) |
| pct_basic_below_basic | % of students at Basic or Below Basic (bottom tail) |

NAS scoring scale: % correct is on the raw test out of 100. Proficient+Advanced
is a combined top-tail band derived from item-response theory; the cutoff is
set per (grade, subject) but the *share* in this band is reported as a single
percentage.

NAS does NOT publish the four-band split (Below Basic / Basic / Proficient /
Advanced) separately in the dashboard data — only the two collapsed bands. So
"Proficient+Advanced" is the closest available proxy to "top-tail mastery".

## Key findings (Class 5 Math)

| Category | % Proficient+Advanced | Notes |
|---|---:|---|
| State Govt | 28.50% | Reference (largest group) |
| Govt Aided | 19.31% | Worst-performing management |
| Private Recognised | 22.75% | **20% below State Govt at top tail** |
| Central Govt | 23.47% | Includes KV, JNV — JNV not yet selected at C5 |
| Rural | 25.62% | **14% above Urban at top tail** |
| Urban | 22.39% | |

**The NAS data does NOT support a "private outperforms govt at the top tail"
narrative at Class 5 Math.** Private Recognised has a *smaller* share of
top-tail students than State Govt schools. Rural locations have a *larger*
share than Urban.

Pattern across grades for Private vs State Govt at top tail:

| Grade | Private / State Govt ratio |
|---|---:|
| 3 | 0.92× (private slightly below) |
| 5 | 0.80× (private clearly below) |
| 8 | 1.13× (private modestly above) |
| 10 | 1.31× (private clearly above) |

The private advantage emerges only from Class 8 onwards. Through Classes 3–5,
state government schools nationally have more top-tail students than private.

## Caveats

1. **Heterogeneity within "Private Recognised."** This NAS category mixes
   elite high-fee schools with low-fee budget private schools. The category
   mean averages across both. NAS does not break out elite-only or
   English-medium-only subsets.

2. **Sample base.** NAS 2021 sampled ~3.4M students from 1.18 lakh schools
   across 720 districts. Sampling is designed for state-level inference; the
   national aggregation here is a derivation, not a NAS-published figure.

3. **Central Govt at Class 5 is pre-JNV-selection.** JNV admits at Class 6.
   Class 5 Central Govt scores reflect KV and other central schools, not yet
   the JNVST-selected cohort. From Class 8 onwards, the Central Govt category
   includes JNV students and rises sharply at the top tail (31.30% at C8,
   33.72% at C10 vs 23.47% at C5).

4. **Proficient+Advanced is a wider band than "ASSET top 5%".** NAS's top
   tail captures roughly the top quarter of takers at grade-level curriculum,
   not the top 5%. Not directly comparable to ASSET top 5% (which is a much
   smaller fraction at a much harder bar).

5. **Weighting.** National aggregation uses
   `total_student × share-of-management-or-location / 100` as the weight per
   state. This is the best proxy available; NAS doesn't publish raw student
   counts by category × state.
