"""
Parse AISHE 2021-22 Table 34a (Programme-wise Out-turn for Social Categories,
PWD, Minority) into a tidy long-form CSV. This is the raw programme-level slice;
the discipline rollup is produced by 03c_outturn_discipline_by_social_category.py.

Source: sources/aishe_2021-22_final_report.xlsx, sheet '34a'
Output: extractions/aishe_2021-22_outturn_programme_by_social_category.csv

Sheet column layout (1-indexed):
  1=S.No., 2=Programme, then 8 social categories x M/F/T = 24 value columns:
    All Categories, Scheduled Caste, Scheduled Tribe, Other Backward Classes,
    Persons with Disability, Muslim, Other Minority Communities, EWS.

Output columns: programme, social_category, gender, out_turn
"""
import csv
import openpyxl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "aishe_2021-22_final_report.xlsx"
OUT = ROOT / "extractions" / "aishe_2021-22_outturn_programme_by_social_category.csv"

CATEGORIES = [
    "All Categories",
    "Scheduled Caste",
    "Scheduled Tribe",
    "Other Backward Classes",
    "Persons with Disability",
    "Muslim",
    "Other Minority Communities",
    "EWS",
]
GENDERS = ["Male", "Female", "Total"]


def main() -> None:
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["34a"]

    rows_out = []
    for row in ws.iter_rows(min_row=5, values_only=True):
        prog = row[1]
        if prog is None or not str(prog).strip():
            continue
        prog = str(prog).strip()
        for ci, cat in enumerate(CATEGORIES):
            for gi, gender in enumerate(GENDERS):
                col_idx = 2 + ci * 3 + gi
                val = row[col_idx] if col_idx < len(row) else None
                rows_out.append(
                    {
                        "programme": prog,
                        "social_category": cat,
                        "gender": gender,
                        "out_turn": int(val) if isinstance(val, (int, float)) else 0,
                    }
                )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["programme", "social_category", "gender", "out_turn"])
        w.writeheader()
        w.writerows(rows_out)

    n_progs = len({r["programme"] for r in rows_out})
    grand = sum(r["out_turn"] for r in rows_out if r["social_category"] == "All Categories" and r["gender"] == "Total")
    print(f"Wrote {len(rows_out):,} rows ({n_progs} programmes x {len(CATEGORIES)} categories x {len(GENDERS)} gender) -> {OUT}")
    print(f"  Sanity: All-India out-turn (sum of programme All-Categories totals) = {grand:,}")


if __name__ == "__main__":
    main()
