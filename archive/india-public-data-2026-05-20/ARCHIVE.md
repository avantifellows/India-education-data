# india-public-data (archived 2026-11-24)

`avantifellows/india-public-data` was a short-lived consolidation of this repo
(as `education/`) with the PLFS pipeline (as `plfs/`). Its last commit was on
2026-05-20, 30 minutes after this repo's last commit. The GitHub repo has since
been deleted. Its only surviving copy was a Dropbox folder, which was removed on
2026-11-24 after a file-by-file check:

| Files | Where they live now |
|---|---|
| 168 | identical blobs already in git history (this repo, external_data_sources, data-assistant) |
| 215 | identical copies on disk outside git (raw PDFs/XLSX, NAS csv_data, PLFS raw docs), not deleted |
| 19  | `education/parquet/*.parquet`, regenerable: each equals its `extractions/*.csv` (checked with pandas) |
| 9   | **unique, kept here** |

The 9 kept files, at their original paths:

- `docs/whitepaper.md`: a later, more neutral edit of `../../whitepaper.md`
  (§7 "Key observations", §8 "Implications" rewritten as descriptive patterns
  rather than prescriptions). Not merged into the live whitepaper; that is an
  editorial choice.
- `README.md`, `education/README.md`, `education/extractions/aishe_2021-22_NOTES.md`:
  wording revisions of the same docs here.
- `education/scripts/build_parquet.py`: converts every `extractions/*.csv` to
  parquet for BigQuery load. Not in this repo's `scripts/`.
- `infra/`: a GCS staging script (bucket never filled in, so it never ran), its
  manifest builder, and `raw_manifest.csv` (sha256 of each raw source file).
- `gitignore.txt`: the consolidated repo's `.gitignore`, renamed so it doesn't apply here.
