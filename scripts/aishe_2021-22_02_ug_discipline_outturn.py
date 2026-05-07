"""
Parse AISHE 2021-22 Table 35 (UG Out-turn by Major Discipline) into a tidy long-form CSV.

Source: sources/aishe_2021-22_final_report.xlsx, sheet '35UGDisc'
Output: extractions/aishe_2021-22_outturn_ug_discipline.csv

Sheet structure: Discipline col may be repeated for multi-subject disciplines
(e.g., Engineering & Technology spans many sub-disciplines like Aeronautical
Engineering before the 'Engineering & Technology Total' row). We keep the
discipline-level totals only (subject == None OR discipline ends with 'Total').

Output columns: discipline, gender, out_turn
"""
import csv
import openpyxl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "aishe_2021-22_final_report.xlsx"
OUT = ROOT / "extractions" / "aishe_2021-22_outturn_ug_discipline.csv"


def main() -> None:
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["35UGDisc"]

    # Cols (0-indexed): 0=S.No., 1=Discipline, 2=Subject, 3=Male, 4=Female, 5=Total.
    # Discipline-total rows have Subject (col 2) == None.
    rows_out = []
    for row in ws.iter_rows(min_row=4, values_only=True):
        disc, subj, male, female, total = row[1], row[2], row[3], row[4], row[5]
        if disc is None:
            continue
        disc = str(disc).strip()
        # Normalise discipline-total rows (col 1 may be 'X Total')
        if disc.endswith("Total"):
            disc = disc[: -len("Total")].strip()
        # Keep only discipline-total rows (no subject)
        if subj not in (None, "") and not str(disc).endswith("Total"):
            continue
        if not isinstance(total, (int, float)):
            continue
        rows_out.append({"discipline": disc, "gender": "Male", "out_turn": int(male or 0)})
        rows_out.append({"discipline": disc, "gender": "Female", "out_turn": int(female or 0)})
        rows_out.append({"discipline": disc, "gender": "Total", "out_turn": int(total or 0)})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["discipline", "gender", "out_turn"])
        w.writeheader()
        w.writerows(rows_out)

    disciplines = sorted({r["discipline"] for r in rows_out})
    grand = sum(r["out_turn"] for r in rows_out if r["gender"] == "Total")
    print(f"Wrote {len(rows_out):,} rows ({len(disciplines)} disciplines x 3 gender) -> {OUT}")
    print(f"  Sanity: All-India UG out-turn (sum of discipline totals) = {grand:,}")


if __name__ == "__main__":
    main()
