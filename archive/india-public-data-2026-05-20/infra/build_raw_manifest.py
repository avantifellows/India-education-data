"""Generate infra/raw_manifest.csv — inventory of every raw source artifact
that backs the extractions, with size, sha256, and whether it ships in-repo or
must be staged separately to GCS.

Two classes of raw input:
  in_repo  = committed under education/sources/ or plfs/raw/docs/ (small,
             re-downloadable from public URLs)
  external = gitignored bulk that is hard to re-download (NVS Drive PDFs,
             AICTE 201 MB report, PLFS microdata.gov.in unit data). These do
             NOT ship in git; the canonical copy is on GCS (or Dropbox, TBD).

For external files we record the local Dropbox path the team is currently
using so they can be staged to the bucket; that path is environment-specific
and should be re-pointed by whoever runs the upload.
"""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "infra" / "raw_manifest.csv"

# External bulk that is gitignored / not in the monorepo. Sizes are approximate.
# `local_path` is relative to the Claude working dir (sibling repos) and is
# environment-specific — re-point before uploading.
EXTERNAL = [
    ("education", "nvs_annual_report_2019-20.pdf", "~102 MB",
     "Google Drive (see education/sources/SOURCES.md)",
     "../India Public Education Data/sources/nvs_annual_report_2019-20.pdf"),
    ("education", "nvs_annual_report_2020-21.pdf", "~157 MB",
     "Google Drive (see education/sources/SOURCES.md)",
     "../India Public Education Data/sources/nvs_annual_report_2020-21.pdf"),
    ("education", "nvs_annual_report_2021-22.pdf", "~160 MB",
     "Google Drive (see education/sources/SOURCES.md)",
     "../India Public Education Data/sources/nvs_annual_report_2021-22.pdf"),
    ("education", "nvs_annual_report_2022-23.pdf", "~99 MB",
     "Google Drive (see education/sources/SOURCES.md)",
     "../India Public Education Data/sources/nvs_annual_report_2022-23.pdf"),
    ("education", "nvs_annual_report_2023-24.pdf", "~83 MB",
     "Google Drive (see education/sources/SOURCES.md)",
     "../India Public Education Data/sources/nvs_annual_report_2023-24.pdf"),
    ("education", "aicte_annual_report_2023-24.pdf", "~201 MB",
     "https://www.aicte.gov.in/downloads/annual-reports/English-Annual%20Report%202023-24.pdf",
     "../India Public Education Data/sources/aicte_annual_report_2023-24.pdf"),
    ("plfs", "raw/ (PLFS unit-level microdata, all releases)", "~2.9 GB",
     "https://microdata.gov.in (gated login; cannot be redistributed)",
     "../PLFS/raw/"),
    ("plfs", "clean/ (parsed canonical CSVs, all releases)", "~2.3 GB",
     "regenerable via plfs/scripts/parse_data.py from raw/",
     "../PLFS/clean/"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    rows = []

    # In-repo raw sources: education/sources (excluding the vendored NAS csv_data
    # tree which is itself derived, and *.md docs) + plfs/raw/docs
    for base, pipeline in [(ROOT / "education" / "sources", "education"),
                           (ROOT / "plfs" / "raw" / "docs", "plfs")]:
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() == ".md":
                continue
            if "nas_2021_data" in p.parts and p.suffix.lower() == ".csv":
                continue  # vendored derived data, not a raw download
            size_mb = p.stat().st_size / 1e6
            rows.append({
                "pipeline": pipeline,
                "filename": str(p.relative_to(ROOT)),
                "size": f"{size_mb:.1f} MB",
                "in_repo": "yes",
                "source": "committed",
                "sha256": sha256(p),
            })

    for pipeline, fname, size, source, _local in EXTERNAL:
        rows.append({
            "pipeline": pipeline,
            "filename": fname,
            "size": size,
            "in_repo": "no",
            "source": source,
            "sha256": "",  # not hashed (large / not in repo)
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["pipeline", "filename", "size",
                                          "in_repo", "source", "sha256"])
        w.writeheader()
        w.writerows(rows)
    n_in = sum(1 for r in rows if r["in_repo"] == "yes")
    n_ext = len(rows) - n_in
    print(f"Wrote {len(rows)} rows -> {OUT} ({n_in} in-repo, {n_ext} external)")


if __name__ == "__main__":
    main()
