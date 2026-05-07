"""
Roll up the programme-level out-turn (Table 34a, parsed by 03a) to discipline level
using the programme -> discipline mapping (built by 03b).

Inputs:
  extractions/aishe_2021-22_outturn_programme_by_social_category.csv  (from 03a)
  extractions/aishe_2021-22_programme_to_discipline_mapping.csv       (from 03b)

Output:
  extractions/aishe_2021-22_outturn_discipline_by_social_category.csv

Output columns: discipline, social_category, gender, out_turn

Validation: prints discipline-level totals for All Categories x Total alongside
the AISHE Table 35 (UG) discipline totals for the same disciplines, where the
two should be in the same ballpark for predominantly-UG disciplines (Engineering
& Technology, Arts, Science, Commerce, etc.). They will not match exactly because
Table 34a covers all levels (UG + PG + PhD + Diploma + Certificate) whereas
Table 35 is UG-only.
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROG_CSV = ROOT / "extractions" / "aishe_2021-22_outturn_programme_by_social_category.csv"
MAP_CSV = ROOT / "extractions" / "aishe_2021-22_programme_to_discipline_mapping.csv"
UG_CSV = ROOT / "extractions" / "aishe_2021-22_outturn_ug_discipline.csv"
OUT = ROOT / "extractions" / "aishe_2021-22_outturn_discipline_by_social_category.csv"


def main() -> None:
    # Load mapping
    prog_to_disc: dict[str, str] = {}
    with MAP_CSV.open() as f:
        for row in csv.DictReader(f):
            prog_to_disc[row["programme"]] = row["discipline"]

    # Aggregate programme rows -> (discipline, social_category, gender) -> sum
    agg: dict[tuple[str, str, str], int] = defaultdict(int)
    unmapped_progs = set()
    with PROG_CSV.open() as f:
        for row in csv.DictReader(f):
            disc = prog_to_disc.get(row["programme"])
            if disc is None:
                unmapped_progs.add(row["programme"])
                disc = "Others"
            key = (disc, row["social_category"], row["gender"])
            agg[key] += int(row["out_turn"])

    # Sort: discipline asc, social_category in declared order, gender M/F/T
    cat_order = [
        "All Categories",
        "Scheduled Caste",
        "Scheduled Tribe",
        "Other Backward Classes",
        "Persons with Disability",
        "Muslim",
        "Other Minority Communities",
        "EWS",
    ]
    gen_order = ["Male", "Female", "Total"]
    cat_idx = {c: i for i, c in enumerate(cat_order)}
    gen_idx = {g: i for i, g in enumerate(gen_order)}
    sorted_keys = sorted(agg.keys(), key=lambda k: (k[0], cat_idx.get(k[1], 99), gen_idx.get(k[2], 99)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["discipline", "social_category", "gender", "out_turn"])
        w.writeheader()
        for k in sorted_keys:
            w.writerow({"discipline": k[0], "social_category": k[1], "gender": k[2], "out_turn": agg[k]})

    print(f"Wrote {len(sorted_keys):,} rows ({len({k[0] for k in agg})} disciplines x {len(cat_order)} categories x {len(gen_order)} genders) -> {OUT}")
    if unmapped_progs:
        print(f"  WARNING: {len(unmapped_progs)} programmes had no entry in the mapping CSV (treated as 'Others')")

    # Cross-check vs Table 35 (UG-only) for sanity. Table 34a covers all levels,
    # so 34a totals will exceed Table 35 totals; the comparison is only directional.
    table35: dict[str, int] = {}
    if UG_CSV.exists():
        with UG_CSV.open() as f:
            for row in csv.DictReader(f):
                if row["gender"] == "Total":
                    table35[row["discipline"]] = int(row["out_turn"])
    print("\n=== Sanity check: Table 34a (all levels) discipline totals vs Table 35 (UG only) ===")
    print(f"{'Discipline':35s} {'34a All Cat / Total':>20s} {'Table 35 (UG)':>15s} {'34a as % of UG':>15s}")
    for disc in sorted({k[0] for k in agg}):
        v34a = agg.get((disc, "All Categories", "Total"), 0)
        v35 = table35.get(disc)
        if v35 and v35 > 0:
            pct = f"{(v34a / v35 * 100):.0f}%"
        else:
            pct = "—"
        v35_s = f"{v35:,}" if v35 is not None else "—"
        print(f"{disc:35s} {v34a:>20,} {v35_s:>15s} {pct:>15s}")


if __name__ == "__main__":
    main()
