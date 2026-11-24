"""Convert every extractions/*.csv into parquet/<name>.parquet for BigQuery load.

Run after the extraction scripts. Parquet is the load format the data team
ingests into BigQuery (one table per file). Re-runnable; overwrites outputs.

Usage:
    python3 education/scripts/build_parquet.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]          # education/
SRC = ROOT / "extractions"
OUT = ROOT / "parquet"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    csvs = sorted(SRC.glob("*.csv"))
    if not csvs:
        print(f"No CSVs in {SRC}", file=sys.stderr)
        return 1
    for csv_path in csvs:
        df = pd.read_csv(csv_path)
        out_path = OUT / f"{csv_path.stem}.parquet"
        df.to_parquet(out_path, index=False, engine="pyarrow")
        print(f"{csv_path.name:55s} {len(df):>7,} rows -> {out_path.name}")
    print(f"\nWrote {len(csvs)} parquet files to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
