"""
6-bucket split of annual STEM-track UG graduates in India.

Denominators (per AISHE 2021-22 — latest published):
  - Total UG out-turn (all disciplines)         : 7,754,223
  - Engineering & Technology UG out-turn        :   829,627
  - Medical Science UG out-turn (incl pharm/AYUSH):  293,528
  - IT & Computer UG out-turn (BCA, B.Sc IT)    :   258,203
  - STEM-track UG total (Eng + IT + Medical)    : 1,381,358  (~17.8 % of all UG)

Per-bucket employment rate + salary methodology:

  Buckets 1, 2, 4 (NIRF-ranked institutions):
    Placement rate = institution-reported in NIRF Mandatory Disclosure PDF.
    Median salary = institution-reported median annual salary of placed students.
    Source: NIRF aggregate (BQ external_data_sources.nirf_fact_aggregate)
            + College DB scorecards for institutes that filed NIRF PDFs but
            aren't in published top-100 ranks (incl. IIT Goa, smaller NITs/IIITs).

  Bucket 3 (Govt MBBS):
    Placement rate = ~100 % (all MBBS graduates functionally placed via
    compulsory internship → NEET-PG → govt or private practice).
    Median salary — variable by stage:
      Junior Resident (post-internship, pre-PG) in govt sector ₹0.6-0.9 L/month
      = ~₹7-10 L/yr starting; PLFS Medical bucket (age 25-30, ₹3.65 L mean)
      under-counts this because PLFS Medical pools MBBS with nurses + AYUSH.
      Post-PG specialist (~10 years out): ₹15-25 L. Reported here as starting:
      ~₹7 L (govt JR scale), with note that the long-run median is higher.

  Buckets 5, 6 (no NIRF coverage):
    Employment rate (% in regular salaried jobs) and avg wage from PLFS
    Annual 2023-24 (age 25-30 cohort).
      PLFS bucket "Graduate (non-technical)" covers BCA/BSc-IT (bucket 5)
        and most non-elite graduates: 28.0 % regular, ₹2.80 L/yr avg.
      PLFS bucket "Engineering & Technology" mixes elite + non-elite engg
        (64 % regular, ₹4.90 L avg) — non-elite portion back-calculated
        to ~35 % regular, ~₹2.3 L avg (since 200K elite at ~₹13 L pulls
        the PLFS mean upward).
      PLFS bucket "Medical" mixes MBBS + BDS + AYUSH + nurses + pharma
        (51 % regular, ₹3.65 L avg).
    See PLFS analysis in ../PLFS/analyses/.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extractions" / "stem_pipeline_buckets_2024-25.csv"

# Denominators
TOTAL_UG_GRADS = 7754223   # AISHE 2021-22 Table 35 total UG out-turn
STEM_GRADS = 1381358       # Eng + IT/Computer + Medical


ROWS = [
    {
        "bucket": "1. IITs",
        "n_institutes": 23,
        "annual_grads": 15647,
        "annual_placed": 14333,
        "employment_rate_pct": 91.6,
        "rate_source": "NIRF placement rate (institution-reported)",
        "avg_pay_lakh": 17.2,
        "pay_metric": "median salary (NIRF)",
        "pay_source": "College DB scorecards (NIRF Mandatory Disclosure PDFs)",
        "pct_of_stem_ug": round(15647 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(15647 / TOTAL_UG_GRADS * 100, 2),
        "notes": "All 23 IITs covered (incl. IIT Goa, sourced via direct NIRF PDF scrape since IIT Goa isn't in NIRF aggregate top-100). Median range: ₹12 L (Palakkad) to ₹22.5 L (Guwahati). Top-quartile placements at IIT-B/D/M cross ₹50 L.",
    },
    {
        "bucket": "2. NITs / IIITs",
        "n_institutes": 57,
        "annual_grads": 29510,
        "annual_placed": 26227,
        "employment_rate_pct": 88.9,
        "rate_source": "NIRF placement rate (College DB avg across NITs + IIITs)",
        "avg_pay_lakh": 10.1,
        "pay_metric": "median salary (NIRF)",
        "pay_source": "College DB scorecards (NIRF Mandatory Disclosure PDFs)",
        "pct_of_stem_ug": round(29510 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(29510 / TOTAL_UG_GRADS * 100, 2),
        "notes": "31 NITs (all with placement data) + 26 IIITs (17 with placement, 9 newer/PPP extrapolated at NIT-tier avg). Range: NIT Trichy 95% / ₹14 L → NIT Goa 86% / ₹8 L → IIIT Hyderabad ₹22 L → IIIT Allahabad ₹15 L.",
    },
    {
        "bucket": "3. Govt MBBS colleges",
        "n_institutes": 423,
        "annual_grads": 54000,
        "annual_placed": 54000,
        "employment_rate_pct": 100.0,
        "rate_source": "Compulsory internship + NEET-PG funnel — all MBBS grads become doctors",
        "avg_pay_lakh": 7.0,
        "pay_metric": "starting salary (Junior Resident govt scale)",
        "pay_source": "Govt 7th Pay Commission pay matrix for Junior Residents (~₹56K/month) + cross-checks with PLFS Medical bucket (₹3.65 L) which under-counts due to pooling with nurses/AYUSH",
        "pct_of_stem_ug": round(54000 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(54000 / TOTAL_UG_GRADS * 100, 2),
        "notes": "60,324 govt MBBS seats × 90% completion. ₹7 L is starting JR salary; long-run median rises to ₹15-25 L post-PG specialist (3-5 yrs later). No NIRF placement concept since MBBS doesn't go through campus placement.",
    },
    {
        "bucket": "4. Top-200 NIRF Engineering (non-IIT/NIT/IIIT)",
        "n_institutes": 137,
        "annual_grads": 155398,
        "annual_placed": 110021,
        "employment_rate_pct": 70.8,
        "rate_source": "NIRF placement rate (NIRF 2025 top-100 + NIRF 2022 ranks 101-200)",
        "avg_pay_lakh": 7.5,
        "pay_metric": "weighted median salary (NIRF top-100 + 101-200 average)",
        "pay_source": "NIRF aggregate (BQ external_data_sources)",
        "pct_of_stem_ug": round(155398 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(155398 / TOTAL_UG_GRADS * 100, 2),
        "notes": "BITS, VIT, SRM, Thapar, MANIT, COEP, PSG, Anna Univ campuses, etc. Top-100 median ₹9.8 L; 101-200 median ₹5.1 L. NIRF 2023+ stopped publishing individual ranks past 100, so 101-200 portion uses NIRF 2022 cycle.",
    },
    {
        "bucket": "5. IT & Computer (BCA / B.Sc IT)",
        "n_institutes": None,
        "annual_grads": 258203,
        "annual_placed": None,
        "employment_rate_pct": 28.0,
        "rate_source": "PLFS Annual 2023-24, age 25-30, Graduate (non-technical) bucket",
        "avg_pay_lakh": 2.8,
        "pay_metric": "mean monthly wage for regular salaried × 12",
        "pay_source": "PLFS Annual 2023-24 (₹23,345/month avg regular wage)",
        "pct_of_stem_ug": round(258203 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(258203 / TOTAL_UG_GRADS * 100, 2),
        "notes": "BCA + B.Sc IT + B.Sc Computer Apps. PLFS doesn't have a separate code for these — they land in 'Graduate non-technical' alongside Arts/Sci/Com grads. Most BCA grads compete for entry-level IT-support roles (₹2.5-3.5 L typical) or move to MCA/PGDM.",
    },
    {
        "bucket": "6. All others (long tail engineering + non-MBBS medical)",
        "n_institutes": None,
        "annual_grads": 868600,
        "annual_placed": None,
        "employment_rate_pct": 39.0,
        "rate_source": "PLFS-derived: engineering bucket (64% regular for ALL engg incl. elite) back-calculated for non-elite (~35%) + Medical bucket (51% regular)",
        "avg_pay_lakh": 2.7,
        "pay_metric": "PLFS-derived weighted avg of non-elite engineering (~₹2.3 L) and non-MBBS medical (~₹3.65 L)",
        "pay_source": "PLFS Annual 2023-24, age 25-30, Engineering and Medical buckets",
        "pct_of_stem_ug": round(868600 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(868600 / TOTAL_UG_GRADS * 100, 2),
        "notes": "Engineering residual: AISHE 8.30 L − IIT 15.6K − NIT/IIIT 29.5K − NIRF top-200 (non-IIT/NIT/IIIT) 155K = ~629K (mostly state engineering colleges + tier-3 private). Medical residual: AISHE 2.94 L − Govt MBBS 54K = ~240K (BDS, AYUSH, B.Pharm, Nursing, BPT, etc.).",
    },
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["bucket", "n_institutes", "annual_grads", "annual_placed",
            "employment_rate_pct", "rate_source",
            "avg_pay_lakh", "pay_metric", "pay_source",
            "pct_of_stem_ug", "pct_of_all_ug", "notes"]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(ROWS)

    total_grads_buckets = sum(r["annual_grads"] for r in ROWS)
    print(f"Wrote {len(ROWS)} rows -> {OUT}")
    print(f"\n6-bucket STEM-track UG split (India, ~2023-24 cohort, AISHE 2021-22 base)")
    print(f"Denominators: STEM UG = {STEM_GRADS:,}; ALL UG = {TOTAL_UG_GRADS:,}")
    print()
    print(f"{'Bucket':46s} {'Grads':>9s} {'%STEM':>6s} {'%AllUG':>7s} {'Job%':>5s} {'Pay (L)':>8s}")
    print("-" * 92)
    for r in ROWS:
        print(f"{r['bucket']:46s} "
              f"{r['annual_grads']:>9,} "
              f"{r['pct_of_stem_ug']:>5.1f}% "
              f"{r['pct_of_all_ug']:>6.2f}% "
              f"{r['employment_rate_pct']:>4.0f}% "
              f"{r['avg_pay_lakh']:>7.1f}")
    print("-" * 92)
    print(f"{'STEM-track total (Eng + IT + Medical)':46s} "
          f"{total_grads_buckets:>9,} "
          f"{100.0:>5.1f}% "
          f"{total_grads_buckets/TOTAL_UG_GRADS*100:>6.2f}%")
    non_stem = TOTAL_UG_GRADS - total_grads_buckets
    print(f"{'Non-STEM UG (Arts, Sci, Com, Edu, Law, Mgmt, ...)':46s} "
          f"{non_stem:>9,} "
          f"{'—':>5s}  "
          f"{non_stem/TOTAL_UG_GRADS*100:>6.2f}%  "
          f"~28%   ~2.8")
    print(f"{'ALL UG grads (AISHE 2021-22)':46s} "
          f"{TOTAL_UG_GRADS:>9,} "
          f"{'—':>5s}  "
          f"{100.0:>6.2f}%")


if __name__ == "__main__":
    main()
