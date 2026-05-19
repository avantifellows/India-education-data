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


# PLFS Annual 2023-24 multipliers (regular wage growth ratios vs the 24-29 age band)
# Computed from clean/annual_2023_24/perv1.csv by ../PLFS/.
#  Engineering & Technology: 24-29 ₹4.64 L → 30-34 ₹5.89 L (×1.27) → 35-40 ₹7.15 L (×1.54)
#  Medical (all):             24-29 ₹4.07 L → 30-34 ₹4.90 L (×1.21) → 35-40 ₹6.39 L (×1.57)
#  Graduate (non-technical):  24-29 ₹2.63 L → 30-34 ₹3.40 L (×1.29) → 35-40 ₹4.01 L (×1.53)
PLFS_ENG_MULT  = {"30_34": 1.27, "35_40": 1.54}
PLFS_MED_MULT  = {"30_34": 1.21, "35_40": 1.57}
PLFS_GRAD_MULT = {"30_34": 1.29, "35_40": 1.53}


ROWS = [
    {
        "bucket": "1. IITs",
        "n_institutes": 23,
        "annual_grads": 15647,
        "annual_placed": 14333,
        "employment_rate_pct": 91.6,
        "rate_source": "NIRF placement rate (institution-reported)",
        "avg_pay_24_29_lakh": 17.2,  # NIRF starting median
        "avg_pay_30_34_lakh": round(17.2 * PLFS_ENG_MULT["30_34"], 1),
        "avg_pay_35_40_lakh": round(17.2 * PLFS_ENG_MULT["35_40"], 1),
        "pay_metric": "median salary at graduation (NIRF); progression via PLFS Engineering ×1.27 / ×1.54",
        "pay_source": "College DB scorecards (NIRF MD PDFs) + PLFS Annual 2023-24 age-band growth",
        "pct_of_stem_ug": round(15647 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(15647 / TOTAL_UG_GRADS * 100, 2),
        "notes": "All 23 IITs (incl. IIT Goa, sourced via direct NIRF PDF scrape). Range: ₹12 L (Palakkad) to ₹22.5 L (Guwahati). Top-quartile placements at IIT-B/D/M cross ₹50 L. Progression assumes IIT grads track the PLFS Engineering growth curve; the true IIT progression is likely steeper at the top (FAANG/MBA tracks ~3× by mid-30s) but the median tracks PLFS reasonably.",
    },
    {
        "bucket": "2. NITs / IIITs",
        "n_institutes": 57,
        "annual_grads": 29510,
        "annual_placed": 26227,
        "employment_rate_pct": 88.9,
        "rate_source": "NIRF placement rate (College DB avg across NITs + IIITs)",
        "avg_pay_24_29_lakh": 10.1,
        "avg_pay_30_34_lakh": round(10.1 * PLFS_ENG_MULT["30_34"], 1),
        "avg_pay_35_40_lakh": round(10.1 * PLFS_ENG_MULT["35_40"], 1),
        "pay_metric": "median salary at graduation (NIRF); progression via PLFS Engineering ×1.27 / ×1.54",
        "pay_source": "College DB scorecards (NIRF MD PDFs) + PLFS Annual 2023-24",
        "pct_of_stem_ug": round(29510 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(29510 / TOTAL_UG_GRADS * 100, 2),
        "notes": "31 NITs + 26 IIITs. Range: NIT Trichy 95% / ₹14 L → NIT Goa 86% / ₹8 L → IIIT Hyderabad ₹22 L → IIIT Allahabad ₹15 L. Progression tracks PLFS Engineering curve.",
    },
    {
        "bucket": "3. Govt MBBS colleges",
        "n_institutes": 423,
        "annual_grads": 54000,
        "annual_placed": 54000,
        "employment_rate_pct": 100.0,
        "rate_source": "Compulsory internship + NEET-PG funnel — all MBBS grads become doctors",
        "avg_pay_24_29_lakh": 7.0,   # Junior Resident govt scale
        "avg_pay_30_34_lakh": round(7.0 * PLFS_MED_MULT["30_34"], 1),  # PLFS Medical multiplier
        "avg_pay_35_40_lakh": round(7.0 * PLFS_MED_MULT["35_40"], 1),
        "pay_metric": "starting JR govt scale; progression via PLFS Medical ×1.21 / ×1.57",
        "pay_source": "Govt 7th CPC for JR (₹56K/month start); PLFS Annual 2023-24 Medical bucket for age progression",
        "pct_of_stem_ug": round(54000 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(54000 / TOTAL_UG_GRADS * 100, 2),
        "notes": "60,324 govt MBBS seats × 90% completion. PLFS Medical bucket pools MBBS with nurses/AYUSH/Pharma so age progression here UNDER-counts true MBBS trajectory: post-PG specialists 30-34 typically earn ₹15-20 L; 35-40 specialists ₹20-30 L (vs PLFS-mult ₹8.5 L and ₹11.0 L below).",
    },
    {
        "bucket": "4. Top-200 NIRF Engineering (non-IIT/NIT/IIIT)",
        "n_institutes": 137,
        "annual_grads": 155398,
        "annual_placed": 110021,
        "employment_rate_pct": 70.8,
        "rate_source": "NIRF placement rate (NIRF 2025 top-100 + NIRF 2022 ranks 101-200)",
        "avg_pay_24_29_lakh": 7.5,
        "avg_pay_30_34_lakh": round(7.5 * PLFS_ENG_MULT["30_34"], 1),
        "avg_pay_35_40_lakh": round(7.5 * PLFS_ENG_MULT["35_40"], 1),
        "pay_metric": "weighted NIRF median (top-100 + 101-200); progression via PLFS Engineering",
        "pay_source": "NIRF aggregate (BQ) + PLFS Annual 2023-24",
        "pct_of_stem_ug": round(155398 / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round(155398 / TOTAL_UG_GRADS * 100, 2),
        "notes": "BITS, VIT, SRM, Thapar, MANIT, COEP, PSG, Anna Univ campuses, etc. Top-100 median ₹9.8 L; 101-200 ₹5.1 L. Latter portion from NIRF 2022 cycle.",
    },
    {
        # Bucket 5 — directly PLFS-derived per age band, weighted across the three sub-cohorts.
        # Composition: ~258K BCA/BSc-IT + ~629K non-elite engg + ~240K non-MBBS medical = 1.13M
        # Per-band weighted avg (PLFS Graduate-non-tech for IT, Engineering non-elite back-calc, Medical):
        #   24-29: 258K×2.8 + 629K×2.3 + 240K×3.65   / 1127K ≈ ₹2.70 L  (matches earlier estimate)
        #   30-34: 258K×3.4 + 629K×3.0 + 240K×4.9    / 1127K ≈ ₹3.40 L
        #   35-40: 258K×4.0 + 629K×3.6 + 240K×6.4    / 1127K ≈ ₹4.20 L
        "bucket": "5. All other STEM grads (non-elite engineering + IT/Computer + non-MBBS medical)",
        "n_institutes": None,
        "annual_grads": 258203 + 868600,
        "annual_placed": None,
        "employment_rate_pct": 36.5,
        "rate_source": "PLFS Annual 2023-24, age 24-29: Graduate-non-tech bucket (BCA/BSc-IT 28%), Engineering non-elite back-calc (~35%), Medical (51%).",
        "avg_pay_24_29_lakh": 2.7,
        "avg_pay_30_34_lakh": 3.4,
        "avg_pay_35_40_lakh": 4.2,
        "pay_metric": "PLFS-derived per-age-band weighted avg",
        "pay_source": "PLFS Annual 2023-24 directly (no NIRF multiplier needed — this bucket IS the PLFS cohort)",
        "pct_of_stem_ug": round((258203+868600) / STEM_GRADS * 100, 2),
        "pct_of_all_ug": round((258203+868600) / TOTAL_UG_GRADS * 100, 2),
        "notes": "Composition: ~258K BCA/B.Sc-IT (AISHE IT & Computer) + ~629K state/tier-3 engineering + ~240K non-MBBS medical (BDS, AYUSH, B.Pharm, Nursing). Earnings + employment statistically indistinguishable across these sub-cohorts in PLFS.",
    },
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["bucket", "n_institutes", "annual_grads", "annual_placed",
            "employment_rate_pct", "rate_source",
            "avg_pay_24_29_lakh", "avg_pay_30_34_lakh", "avg_pay_35_40_lakh",
            "pay_metric", "pay_source",
            "pct_of_stem_ug", "pct_of_all_ug", "notes"]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(ROWS)

    total_grads_buckets = sum(r["annual_grads"] for r in ROWS)
    print(f"Wrote {len(ROWS)} rows -> {OUT}")
    print(f"\n5-bucket STEM-track UG split — annual grads + age-banded income progression")
    print(f"Denominators: STEM UG = {STEM_GRADS:,}; ALL UG = {TOTAL_UG_GRADS:,}\n")
    print(f"{'Bucket':46s} {'Grads':>9s} {'%AllUG':>7s} {'Job%':>5s} "
          f"{'24-29':>7s} {'30-34':>7s} {'35-40':>7s}")
    print("-" * 100)
    for r in ROWS:
        print(f"{r['bucket']:46s} "
              f"{r['annual_grads']:>9,} "
              f"{r['pct_of_all_ug']:>6.2f}% "
              f"{r['employment_rate_pct']:>4.0f}% "
              f"{r['avg_pay_24_29_lakh']:>6.1f}L "
              f"{r['avg_pay_30_34_lakh']:>6.1f}L "
              f"{r['avg_pay_35_40_lakh']:>6.1f}L")
    print("-" * 100)
    print(f"{'STEM-track total (Eng + IT + Medical)':46s} "
          f"{total_grads_buckets:>9,} "
          f"{total_grads_buckets/TOTAL_UG_GRADS*100:>6.2f}%")
    non_stem = TOTAL_UG_GRADS - total_grads_buckets
    # Non-STEM uses PLFS Graduate-non-technical bucket directly
    print(f"{'Non-STEM UG (Arts, Sci, Com, Edu, Law, Mgmt, ...)':46s} "
          f"{non_stem:>9,} "
          f"{non_stem/TOTAL_UG_GRADS*100:>6.2f}% "
          f"  28% "
          f"   2.6L "
          f"   3.4L "
          f"   4.0L")
    print(f"{'ALL UG grads (AISHE 2021-22)':46s} "
          f"{TOTAL_UG_GRADS:>9,} "
          f"{100.0:>6.2f}%")


if __name__ == "__main__":
    main()
