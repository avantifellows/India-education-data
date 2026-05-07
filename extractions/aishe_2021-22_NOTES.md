# AISHE 2021-22 extractions — notes & caveats

Five extraction CSVs are derived from `sources/aishe_2021-22_final_report.xlsx`
by the scripts in `scripts/aishe_2021-22_*`. Read this before using the data.

## What's in each file

| File | Source sheet | Cut |
|---|---|---|
| `aishe_2021-22_outturn_state_level.csv` | Table 33 | 36 states/UTs × 8 levels (PhD / M.Phil / PG / UG / PG Diploma / Diploma / Certificate / Integrated) × 3 gender → 864 rows |
| `aishe_2021-22_outturn_ug_discipline.csv` | Table 35 | 40 UG disciplines (Engineering & Technology, Arts, Science, Commerce, …) × 3 gender → 120 rows. Discipline-totals only (sub-disciplines like Aeronautical Engineering not retained). |
| `aishe_2021-22_outturn_programme_by_social_category.csv` | Table 34a | 227 degree programmes (B.A., B.Tech., MBBS, …) × 8 social categories (All / SC / ST / OBC / PwD / Muslim / Other Minority / EWS) × 3 gender → 5,448 rows. **National-level only.** |
| `aishe_2021-22_programme_to_discipline_mapping.csv` | derived | The heuristic mapping used to roll programmes up to disciplines. Audit-able. |
| `aishe_2021-22_outturn_discipline_by_social_category.csv` | derived | Programme-level rows in Table 34a aggregated up to discipline level using the mapping above. **National-level only.** |

## Important caveat for the discipline × social category file

The Final Report Excel does NOT publish a discipline × social category cut for
out-turn. The closest source is Table 34a (programme × social category), and
this extraction rolls programmes up to AISHE's discipline taxonomy via a
name-based heuristic mapping. **Two AISHE tables — Table 35 (disciplines) and
Table 34a (programmes) — use incompatible classification paradigms**:

- **Table 35** classifies students by the *subject* they study (Hindi, Physics,
  History, …) and rolls those subjects up into AISHE's 40 disciplines (Indian
  Language, Science, Social Science, …). A B.A. student majoring in Hindi
  shows up under "Indian Language", not "Arts".
- **Table 34a** classifies students by the *degree programme* they're enrolled
  in (B.A., B.Sc., M.A., …) without subject information. Every B.A. student
  shows up in the same row regardless of subject.

The degree-name → discipline rollup we built therefore **cannot recover the
subject-based disciplines** (Indian Language, Social Science, Foreign Language,
etc.) — those students are mostly enrolled in B.A./M.A./B.Sc. programmes and
get rolled up to Arts or Science by name.

### Reliable discipline numbers from this rollup

These disciplines are predominantly served by named programmes that map cleanly
from name to discipline. Use the rollup with confidence:

- Engineering & Technology (B.Tech, B.E., M.Tech, M.E., B.Arch, M.Arch, …)
- Medical Science (MBBS, BDS, BAMS, BHMS, BUMS, B.Pharm, …)
- Law (LLB, LLM, BA-LLB, BBA-LLB, …)
- Management (BBA, MBA, PGDM, …)
- Education (B.Ed., M.Ed., D.Ed., B.El.Ed., …)
- Commerce (B.Com., M.Com., …)
- IT & Computer (BCA, MCA)
- Agriculture (B.Agri, …)
- Veterinary & Animal Sciences (B.V.Sc., M.V.Sc.)
- Fisheries Science (B.F.Sc., M.F.Sc.)
- Fine Arts (BFA, MFA, B.Mus., M.Mus., B.Dance, …)
- Library & Information Science
- Journalism & Mass Communication
- Physical Education
- Paramedical Science (Nursing, MLT, Physiotherapy, etc. — but see note below)

### Unreliable from this rollup — DO NOT USE for these disciplines

- **Indian Language** — almost everyone is enrolled in B.A./M.A. and rolls up
  to "Arts" in this extraction. Use Table 35 instead (UG only) for the
  subject-level number.
- **Social Science** — same problem. Most students are in B.A./M.A. degrees.
- **Foreign Language**, **Linguistics**, **Cultural Studies**, **Religious
  Studies**, **Defence Studies**, **Area Studies**, **Gandhian Studies**,
  **Women Studies**, **Disability Studies** — all subject-level disciplines
  that don't have dedicated degree programmes; not recoverable from 34a.
- **Arts** in this rollup is *over-counted* — it absorbs B.A. students who in
  Table 35 belong to Indian Language / Social Science / Foreign Language /
  etc.
- **Science** in this rollup is *over-counted* for the same reason — it
  absorbs B.Sc. students who in Table 35 belong to Medical Science
  sub-disciplines, etc.

### Paramedical vs Medical Science

Nursing programmes (A.N.M., G.N.M., B.Sc. Nursing, M.Sc. Nursing) are mapped
here to "Paramedical Science" by their typical AISHE classification, but
AISHE Table 35 only shows ~8,000 graduates under Paramedical Science at UG
level (vs. 220,000+ in the rollup). This suggests AISHE's Table 35 may
classify Nursing under Medical Science. If you want the Table-35-consistent
number, edit the mapping CSV and re-run script 03c.

### Validation cross-checks that *do* work

- `outturn_state_level.csv` UG total summed across states = 7,754,223
- `outturn_ug_discipline.csv` Total summed across disciplines = 7,754,223 ✓
  (Tables 33 and 35 reconcile exactly.)
- `outturn_programme_by_social_category.csv` All-Categories Total summed
  across all 227 programmes = 10,738,573, which matches the all-levels India
  total in Table 33 (UG+PG+PhD+M.Phil+Diploma+Certificate+Integrated) ✓.

## Geographic scope

Tables 33 and 33a are the only state-wise out-turn tables in the published
Excel. Tables 34, 34a, 35, 36 are **national-level only**. There is no
state × discipline × social-category cut in the published AISHE 2021-22 data.
