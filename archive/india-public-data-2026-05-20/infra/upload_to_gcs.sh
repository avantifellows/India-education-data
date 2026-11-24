#!/usr/bin/env bash
# Stage raw source files + generated Parquet to a GCS bucket for the annual
# BigQuery refresh.
#
# ───────────────────────────────────────────────────────────────────────────
# REVIEWER: set BUCKET before running. Nothing uploads until this is a real
# bucket. Suggested layout under the bucket:
#     <bucket>/raw/education/      committed + external education source files
#     <bucket>/raw/plfs/           PLFS unit-level microdata (gitignored bulk)
#     <bucket>/parquet/education/  generated parquet for BQ load
# ───────────────────────────────────────────────────────────────────────────
set -euo pipefail

BUCKET="gs://REPLACE_WITH_BUCKET"     # <-- REVIEWER: fill this in

if [[ "$BUCKET" == *REPLACE_WITH_BUCKET* ]]; then
  echo "ERROR: edit infra/upload_to_gcs.sh and set BUCKET first." >&2
  exit 1
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"

# 1. In-repo education raw sources (committed, re-downloadable but convenient to stage)
gsutil -m rsync -r "$REPO/education/sources" "$BUCKET/raw/education"

# 2. Generated education parquet (BQ load inputs)
gsutil -m rsync -r "$REPO/education/parquet" "$BUCKET/parquet/education"

# 3. PLFS in-repo docs (layouts, manuals)
gsutil -m rsync -r "$REPO/plfs/raw/docs" "$BUCKET/raw/plfs/docs"

# ── External bulk (NOT in the repo — hard to re-download). Re-point the source
#    paths to wherever the canonical copies currently live, then uncomment. ──
#
# NVS annual reports (Google Drive originals) + AICTE 2023-24 report:
# EXT_EDU="/path/to/India Public Education Data/sources"
# gsutil -m cp "$EXT_EDU"/nvs_annual_report_*.pdf            "$BUCKET/raw/education/"
# gsutil -m cp "$EXT_EDU"/aicte_annual_report_2023-24.pdf    "$BUCKET/raw/education/"
#
# PLFS unit-level microdata (~2.9 GB raw + ~2.3 GB clean), microdata.gov.in-gated:
# PLFS_DIR="/path/to/PLFS"
# gsutil -m rsync -r "$PLFS_DIR/raw"   "$BUCKET/raw/plfs/data"
# gsutil -m rsync -r "$PLFS_DIR/clean" "$BUCKET/raw/plfs/clean"

echo "Done. See infra/raw_manifest.csv for the full inventory + checksums."
