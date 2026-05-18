"""
Build a 6-bucket split of annual STEM-track UG graduates in India for the
latest cohort we have triangulated data on (AISHE 2021-22 base for absolute
volumes; NIRF 2025 / NIRF 2022 / NMC 2024-25 for elite-tier composition;
AICTE 2024-25 for intake totals; PLFS 2023-24 for salaries).

The six buckets the user wants:
  1. IITs                                  (engineering, central)
  2. NITs / IIITs                          (engineering, central)
  3. Govt MBBS colleges                    (medicine, central + state govt)
  4. Top-200 NIRF Engineering (other)      (engineering, mostly private + state)
  5. IT & Computer (BCA / B.Sc IT)         (separate AISHE discipline)
  6. All others                            (the long tail: non-NIRF engg + non-govt medical)

Data sources for each bucket:
  - AISHE 2021-22 Table 35: Engineering & Technology UG out-turn = 829,627
                            Medical Science UG out-turn         = 293,528
                            IT & Computer UG out-turn           = 258,203
                            (Total ~13.82 lakh per year — the STEM-track denominator.)
  - NIRF 2025 (top-100 individual ranks): per-institute graduates_on_time + placed + median_salary
  - NIRF 2022 (ranks 101-200 individually disclosed): supplements 2025
  - NMC seat matrix 2024-25 (in sources/): 60,324 govt MBBS seats of 118,190 total
  - AICTE Annual Report 2024-25 + dashboard: intake totals by programme
  - PLFS Annual 2023-24: avg earnings by PLFS tedu bucket

Output: extractions/stem_pipeline_buckets_2024-25.csv
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extractions" / "stem_pipeline_buckets_2024-25.csv"

# Values traced back to sources (each row has the source spelled out)
ROWS = [
    {
        "bucket": "1. IITs",
        "n_institutes": 23,  # all 23 IITs covered (incl. IIT Goa via direct NIRF PDF in College DB)
        "annual_grads": 15647,   # JoSAA 2024 IIT first-year B.Tech seats = 17,385 × 90% completion
        "annual_placed": 14333,  # 15647 × 91.6% (College DB avg placement rate across 23 IITs)
        "placement_pct": 91.6,
        "median_salary_lakh": 17.2,  # College DB avg median across 23 IITs
        "share_of_stem_pct": round(15647 / 1382000 * 100, 2),
        "source": "JoSAA 2024 seat matrix (17,385 first-year B.Tech seats across 23 IITs) + College DB scorecards (NIRF Mandatory Disclosure PDFs scraped per-institute, incl. IIT Goa which doesn't appear in NIRF aggregate rankings)",
        "notes": "All 23 IITs covered. Median salary range across IITs: ₹12 L (IIT Palakkad) to ₹22.5 L (IIT Guwahati). Top-quartile placements at IIT-B/D/M cross ₹50 L/yr (mean is much higher than median).",
    },
    {
        "bucket": "2. NITs / IIITs",
        "n_institutes": 57,  # 31 NITs + 26 IIITs (per JoSAA 2024)
        "annual_grads": 29510,   # 21806 NIT + 7704 IIIT (JoSAA seats × 90%)
        "annual_placed": 26227,  # weighted avg placement ~89%
        "placement_pct": 88.9,
        "median_salary_lakh": 10.1,  # ₹9.5 L NIT (College DB avg) + ₹12.1 L IIIT (top 17 with data) → weighted
        "share_of_stem_pct": round(29510 / 1382000 * 100, 2),
        "source": "JoSAA 2024 seat matrix (NITs: 24,229 first-year seats / IIITs: 8,560 first-year seats; × 90% completion) + College DB scorecards. 31 of 31 NITs have placement data; 17 of 26 IIITs have placement data — remaining 9 IIITs (newer/PPP) extrapolated using NIT-tier avg.",
        "notes": "Sample placement rates: NIT Trichy 95%, NIT Surathkal 92%, NIT Warangal 89%, NIT Goa 86%; IIIT Allahabad 97%, IIIT Hyderabad 96%, IIIT Bangalore 89%. Smallest NITs/IIITs (Manipur, Mizoram, Sikkim, Sri City, Vadodara, Bhopal etc.) have weaker data coverage.",
    },
    {
        "bucket": "3. Govt MBBS colleges",
        "n_institutes": 423,  # of 780 total per NMC; 51% by seats are govt
        "annual_grads": 54000,   # 60324 seats × 90% completion
        "annual_placed": None,   # MBBS doesn't have "placement" in NIRF sense — all become doctors via PG/internship
        "placement_pct": None,
        "median_salary_lakh": 15.0,  # rough; ₹15-25 L for first-decade post-PG
        "share_of_stem_pct": round(54000 / 1382000 * 100, 2),
        "source": "NMC seat matrix 2024-25 (sources/nmc_mbbs_seat_matrix_2024-25.pdf): 60,324 govt seats of 118,190 total (51%). Completion rate ~90% assumed.",
        "notes": "All MBBS grads functionally 'placed' as junior doctors via internship/PG. Income depends on whether they specialise (most do); MBBS-only general practice in govt sector earns ₹6-8 L; specialist post-PG earns ₹15-25 L.",
    },
    {
        "bucket": "4. Top-200 NIRF Engineering (non-IIT/NIT/IIIT)",
        "n_institutes": 52 + 85,
        "annual_grads": 85992 + 69406,
        "annual_placed": 59729 + 50292,
        "placement_pct": round((59729+50292)/(85992+69406)*100, 1),
        "median_salary_lakh": 7.5,  # weighted: top-100 ₹9.8 L, 101-200 ₹5.1 L
        "share_of_stem_pct": round((85992+69406) / 1382000 * 100, 2),
        "source": "NIRF 2025 top-100 (52 non-IIT/NIT/IIIT institutes) + NIRF 2022 ranks 101-200 (85 institutes). Mostly private + state engineering colleges (BITS, VIT, SRM, Thapar, MANIT, COEP, PSG, Anna Univ campuses, …).",
        "notes": "NIRF 2023+ stopped individual ranking past 100 (bucketed bands instead), so 101-200 is from 2022 cycle. Composition of 101-200 doesn't change much YoY.",
    },
    {
        "bucket": "5. IT & Computer (BCA / B.Sc IT)",
        "n_institutes": None,  # spread across thousands of colleges
        "annual_grads": 258203,
        "annual_placed": None,  # PLFS partial; AISHE doesn't report placement
        "placement_pct": None,
        "median_salary_lakh": 2.8,  # PLFS Graduate-non-technical bucket (BCA mostly lands here)
        "share_of_stem_pct": round(258203 / 1382000 * 100, 2),
        "source": "AISHE 2021-22 Table 35 — IT & Computer discipline UG out-turn = 258,203. Distinct from Engineering & Technology (which includes B.Tech CSE).",
        "notes": "Mostly BCA + B.Sc IT + B.Sc Computer Apps (NOT B.Tech CSE — that's in Engineering & Technology). AICTE 2024-25 Computer Applications intake = 1,32,606 (UG+PG combined). Income closer to ₹2.5-3.5 L typically since these grads compete for entry-level IT-support roles.",
    },
    {
        "bucket": "6. All others (long tail)",
        "n_institutes": None,
        # AISHE Eng total 829,627 - IITs 15,647 - NITs+IIITs 29,510 - NIRF Top-200 (non-IIT/NIT/IIIT) 155,398
        # + AISHE Medical total 293,528 - Govt MBBS 54,000
        "annual_grads": 829627 - 15647 - 29510 - 155398 + 293528 - 54000,
        "annual_placed": None,
        "placement_pct": None,
        "median_salary_lakh": 3.0,
        "share_of_stem_pct": round((829627 - 15647 - 29510 - 155398 + 293528 - 54000) / 1382000 * 100, 2),
        "source": "Engineering & Technology residual (AISHE 8.30 L − IIT 15.6K − NIT+IIIT 29.5K − NIRF-top-200-other 155K = ~629K) + Medical Science residual (AISHE 2.94 L − Govt MBBS 54K = ~240K)",
        "notes": "The vast majority — ~6.3 L engineering grads from non-NIRF colleges + ~2.4 L non-MBBS medical (BDS, AYUSH, B.Pharm, Nursing). PLFS-implied avg salary for this cohort: ₹2.5-3.5 L/year in regular jobs, ~30-40% placement rate at best.",
    },
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["bucket", "n_institutes", "annual_grads", "annual_placed",
            "placement_pct", "median_salary_lakh", "share_of_stem_pct",
            "source", "notes"]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(ROWS)

    total_grads = sum(r["annual_grads"] for r in ROWS if r["annual_grads"])
    total_placed = sum(r["annual_placed"] for r in ROWS if r["annual_placed"])
    print(f"Wrote {len(ROWS)} rows -> {OUT}")
    print(f"\n6-bucket STEM-track UG graduate split (India, annual, cohort 2023-24)")
    print(f"{'Bucket':45s} {'Grads':>10s} {'% STEM':>8s} {'Placed':>8s} {'Place%':>7s} {'MedSal(L)':>10s}")
    print("-" * 92)
    for r in ROWS:
        g = r["annual_grads"] or 0
        p = r["annual_placed"]
        ppct = r["placement_pct"] or 0
        ms = r["median_salary_lakh"] or 0
        share = r["share_of_stem_pct"]
        p_s = f"{p:,}" if p else "—"
        ppct_s = f"{ppct:.0f}%" if ppct else "—"
        print(f"{r['bucket']:45s} {g:>10,} {share:>7.1f}% {p_s:>8s} {ppct_s:>7s} {ms:>9.1f}")
    print(f"\n  TOTAL STEM-track UG grads/yr (AISHE Eng+IT+Medical): 13,82,000")
    print(f"  Captured in 6 buckets: {total_grads:,}")


if __name__ == "__main__":
    main()
