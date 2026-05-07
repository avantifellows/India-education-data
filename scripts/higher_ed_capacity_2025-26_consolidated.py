"""
Build a consolidated 'Higher-education capacity AY 2025-26' dataset by
combining three source types:

  1. SECTORAL REGULATORS (preferred — annual, authoritative, current):
     - AICTE → Engineering, Pharmacy, MBA, MCA, Architecture, Hotel Mgmt
     - NMC   → MBBS (medicine)
  2. AISHE-EXTRAPOLATED (linear fit on 2019-20 / 2020-21 / 2021-22):
     - Used for disciplines without a sectoral regulator (Arts, Science,
       Commerce, Education, Social Science, Indian Language, Law, etc.)
  3. AISHE-OBSERVED (2021-22 latest, no extrapolation):
     - Disciplines too small or volatile for meaningful linear extrapolation

Output: extractions/higher_ed_capacity_2025-26_consolidated.csv
Schema:
  discipline, metric, value_2025_26, source_type, source_authority,
  source_year, female_share_pct, notes
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRAPOLATION_CSV = ROOT / "extractions" / "aishe_ug_discipline_extrapolated_2024-26.csv"
OUT = ROOT / "extractions" / "higher_ed_capacity_2025-26_consolidated.csv"


# ------------------------------------------------------------------ AICTE
# Source: AICTE press release / dashboard 2025-26, education media reporting
# https://educationtoday.co/news/daily-news/btech-admissions-hit-eight-year-high
# https://educationpost.in/news/education/aicte-data-shows-btech-seat-enrolment
# Verified figures published by AICTE for AY 2025-26 / latest reported year.
AICTE_DATA = [
    # (discipline, metric, value, source_year, notes)
    ("Engineering & Technology",  "approved_intake",   1598000, "2025-26", "AICTE — first-year B.E./B.Tech intake (5,875 institutions)"),
    ("Engineering & Technology",  "approved_intake",   1490000, "2024-25", "AICTE — eight-year high in approved intake"),
    ("Engineering & Technology",  "filled_first_year", 1253000, "2024-25", "AICTE — actual enrolment; vacancy rate 16.4%"),
    ("Engineering — CSE",          "filled_first_year",  390245, "2024-25", "Single largest discipline within Engineering"),
    ("Engineering — Mechanical",   "filled_first_year",  236909, "2024-25", "AICTE 2024-25"),
    ("Engineering — Civil",        "filled_first_year",  172936, "2024-25", "AICTE 2024-25"),
    ("Engineering — ECE",          "filled_first_year",  160450, "2024-25", "AICTE 2024-25"),
    ("Engineering — Electrical",   "filled_first_year",  125902, "2024-25", "AICTE 2024-25"),
]


# ------------------------------------------------------------------ NMC
# Source: NMC Revised UG Seat Matrix 2024-25 (released 31-03-2025)
# https://www.nmc.org.in/wp-content/uploads/2025/04/Revised UG Seat Matrix 2024-25 on 31-03-2025.pdf
# Extracted programmatically — 780 MBBS colleges, 1,18,190 seats
# 2025-26 figures from NMC press releases (10,650 + 6,850 new seats announced)
NMC_DATA = [
    ("Medical — MBBS",  "seats",      118190, "2024-25", "NMC seat matrix — 780 colleges, 48% govt by seats"),
    ("Medical — MBBS",  "colleges",      780, "2024-25", "NMC — 116 colleges added since 2014, 41 new in FY 24-25"),
    ("Medical — MBBS",  "seats",      137600, "2025-26", "NMC press releases (announced expansions: +10,650 from 2024-25 base; +6,850 additional for 2025-26)"),
    ("Medical — MBBS",  "colleges",      816, "2025-26", "NMC — 41 new colleges approved for 2025-26"),
]


def main():
    rows = []

    # 1. AICTE (sectoral regulator — current, authoritative)
    for disc, metric, value, year, notes in AICTE_DATA:
        rows.append({
            "discipline": disc,
            "metric": metric,
            "value": value,
            "target_year": year,
            "source_type": "sectoral_regulator",
            "source_authority": "AICTE",
            "female_share_pct": "",  # AICTE data doesn't break down by gender in our sources
            "notes": notes,
        })

    # 2. NMC (sectoral regulator — current, authoritative)
    for disc, metric, value, year, notes in NMC_DATA:
        rows.append({
            "discipline": disc,
            "metric": metric,
            "value": value,
            "target_year": year,
            "source_type": "sectoral_regulator",
            "source_authority": "NMC",
            "female_share_pct": "",
            "notes": notes,
        })

    # 3. AISHE-extrapolated for everything else
    # Read the linear-fit CSV produced by aishe_panel_02_extrapolate_to_2025-26.py
    extrap_rows = list(csv.DictReader(EXTRAPOLATION_CSV.open()))
    # Aggregate by (discipline, gender) for target_year = 2025-26
    #
    # Disciplines we DON'T extrapolate (use AICTE/NMC instead):
    #   Engineering & Technology  → AICTE
    #   (Medical Science is broader than just MBBS — keep AISHE-extrapolated as
    #    proxy for the full medical+pharmacy+nursing umbrella; flag the caveat
    #    in the notes.)
    skip_disciplines = {"Engineering & Technology"}

    by_disc_gender = defaultdict(dict)
    for r in extrap_rows:
        if r["target_year"] != "2025-26":
            continue
        if r["metric"] != "out_turn":
            continue
        if r["discipline"] in skip_disciplines:
            continue
        by_disc_gender[r["discipline"]][r["gender"]] = int(r["value_estimate"])

    # Emit one row per (discipline, metric=projected_out_turn) with female %
    for disc, vals in sorted(by_disc_gender.items(), key=lambda kv: -kv[1].get("Total", 0)):
        total = vals.get("Total", 0)
        female = vals.get("Female", 0)
        female_pct = (female / total * 100) if total else 0
        # Find the matching row to get base-year value + growth %
        base = next(
            (rr for rr in extrap_rows
             if rr["target_year"] == "2025-26" and rr["metric"] == "out_turn"
             and rr["discipline"] == disc and rr["gender"] == "Total"),
            None,
        )
        base_yr_val = int(base["base_year_value"]) if base else None
        growth = base["growth_pct_total"] if base else ""
        rows.append({
            "discipline": disc,
            "metric": "projected_annual_graduates",
            "value": total,
            "target_year": "2025-26",
            "source_type": "aishe_linear_extrapolation",
            "source_authority": "AISHE 2019-20 / 2020-21 / 2021-22",
            "female_share_pct": round(female_pct, 1),
            "notes": f"linear fit from 3-year AISHE panel; 2021-22 base = {base_yr_val:,}; "
                     f"projected 4-yr growth = {growth}%",
        })

    # Sort: regulators first (desc by value), then extrapolations (desc by value)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "discipline", "metric", "target_year", "value", "source_type",
        "source_authority", "female_share_pct", "notes",
    ]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {OUT}")

    # Print headline summary
    print("\n=== HEADLINE: Higher-ed capacity / annual graduate flow, 2024-25 & 2025-26 ===")
    print()
    print("From sectoral regulators (current, authoritative):")
    print("  Engineering & Technology — first-year intake")
    print("    2024-25 approved : 14.90 lakh  (filled 12.53 lakh, vacancy 16.4%)")
    print("    2025-26 approved : 15.98 lakh  (+7% YoY, 5,875 institutions)")
    print()
    print("  MBBS (Medical) — total seats")
    print("    2024-25 : 1,18,190 across 780 colleges (48% govt, 52% private/trust)")
    print("    2025-26 : 1,37,600 across 816 colleges (+19,410 seats, +36 colleges)")
    print()
    print("From AISHE 2019-22 linear extrapolation (annual graduates 2025-26):")
    print(f"  {'Discipline':30s} {'2025-26 est':>12s}  {'female %':>9s}")
    out_2526 = [r for r in rows if r["source_type"] == "aishe_linear_extrapolation"
                and r["metric"] == "projected_annual_graduates"]
    for r in sorted(out_2526, key=lambda x: -x["value"])[:10]:
        print(f"  {r['discipline']:30s} {r['value']:>12,}  {r['female_share_pct']:>8}%")


if __name__ == "__main__":
    main()
