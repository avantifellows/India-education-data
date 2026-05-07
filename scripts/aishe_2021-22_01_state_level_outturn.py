"""
Parse AISHE 2021-22 Table 33 (State-wise Out-turn at various levels) into a tidy long-form CSV.

Source: sources/aishe_2021-22_final_report.xlsx, sheet '33OutTurnState'
Output: extractions/aishe_2021-22_outturn_state_level.csv

Schema:
  Table 33 columns are arranged as: S.No., State, then 8 levels x 3 (Male/Female/Total).
  Levels (in order): Ph.D., M.Phil., Post Graduate, Under Graduate,
                     PG Diploma, Diploma, Certificate, Integrated.

Output columns: state, level, gender, out_turn
"""
import csv
import openpyxl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "aishe_2021-22_final_report.xlsx"
OUT = ROOT / "extractions" / "aishe_2021-22_outturn_state_level.csv"

LEVELS = [
    "Ph.D.",
    "M.Phil.",
    "Post Graduate",
    "Under Graduate",
    "PG Diploma",
    "Diploma",
    "Certificate",
    "Integrated",
]
GENDERS = ["Male", "Female", "Total"]


def main() -> None:
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["33OutTurnState"]

    # Data starts at row 5 (rows 1-4 are titles/headers).
    # Cols: 1=S.No., 2=State, 3..26 = 8 levels x M/F/T.
    # We expect All-India total at row 5 (S.No. blank or 'All India') based on layout;
    # here the data shows S.No. = 1 starts with 'A & N Islands', so each row is a State/UT.
    rows_out = []
    for row in ws.iter_rows(min_row=5, values_only=True):
        sno, state = row[0], row[1]
        if state is None or not str(state).strip():
            continue
        state = str(state).strip()
        # Skip aggregate rows (e.g., 'All India', 'Total') — Table 33 in this workbook
        # does not include an All-India row, but we guard anyway.
        if state.lower() in {"all india", "india", "total"}:
            continue
        # Walk 8 level x 3 gender = 24 value columns starting at col index 2 (0-based).
        for li, level in enumerate(LEVELS):
            for gi, gender in enumerate(GENDERS):
                col_idx = 2 + li * 3 + gi
                val = row[col_idx]
                rows_out.append(
                    {
                        "state": state,
                        "level": level,
                        "gender": gender,
                        "out_turn": int(val) if isinstance(val, (int, float)) else 0,
                    }
                )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["state", "level", "gender", "out_turn"])
        w.writeheader()
        w.writerows(rows_out)

    n_states = len({r["state"] for r in rows_out})
    print(f"Wrote {len(rows_out):,} rows ({n_states} states/UTs x {len(LEVELS)} levels x {len(GENDERS)} gender) -> {OUT}")
    # Quick sanity check: India total UG out-turn (sum of state UG-Total rows)
    ug_total = sum(r["out_turn"] for r in rows_out if r["level"] == "Under Graduate" and r["gender"] == "Total")
    print(f"  Sanity: India UG out-turn (sum of states) = {ug_total:,}")


if __name__ == "__main__":
    main()
