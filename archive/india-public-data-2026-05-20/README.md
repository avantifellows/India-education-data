# india-public-data

Reproducible extractions of India's public education and labour-market data, packaged for annual ingestion into BigQuery.

Two pipelines, one convention: raw government source → parser script → tidy long-form CSV → Parquet for BigQuery load.

```
education/   School + higher-education statistics (UDISE+, MoE boards, AISHE, AICTE, NMC, NIRF, KVS/NVS, NAS)
plfs/        Periodic Labour Force Survey unit-level data (2018-19 → CY2025)
infra/       GCS upload script + raw-file manifest (checksums, sources)
docs/        Analytical write-up synthesising the two pipelines
```

## Pipelines

### `education/`

School- and higher-education statistics. Each dataset has a parser in `education/scripts/`, a CSV in `education/extractions/`, a Parquet in `education/parquet/`, and a `*_NOTES.md` documenting schema and caveats. Source files are in `education/sources/` (`SOURCES.md` lists every provenance URL).

Datasets: UDISE+ 2024-25 school enrolment; MoE board results 2020-2024 (Class X + XII, all boards); KV/JNV results; NAS 2021 proficiency; AISHE 2021-22 UG out-turn + 2019-22 trend; AICTE intake/gender panels 2012-2023; NMC MBBS seat matrix; NIRF 2025 institute placement; consolidated higher-ed capacity 2025-26; STEM-track graduate-to-employment buckets.

See [`education/README.md`](education/README.md) for the full dataset table and regeneration commands.

### `plfs/`

PLFS unit-level survey data across 11 releases, parsed to a canonical schema and loaded to BigQuery. Has its own mature pipeline (`plfs/scripts/`: parse → canonicalize → load_bq) and table schemas (`plfs/schemas/`).

See [`plfs/README.md`](plfs/README.md) for the pipeline and BigQuery schema.

## BigQuery delivery

- **`education/`** emits Parquet to `education/parquet/` via `education/scripts/build_parquet.py` — one file per table, committed for review.
- **`plfs/`** loads to BigQuery via `plfs/scripts/load_bq.py` (parses to Parquet, then loads).

The data team's annual refresh: pull new source files, re-run the parsers, regenerate Parquet, load to BigQuery.

## Raw files and GCS

`infra/raw_manifest.csv` inventories every raw source artifact with size, sha256, and source URL — split into:
- **in-repo** (committed under `education/sources/` and `plfs/raw/docs/`): small, re-downloadable from public URLs.
- **external** (gitignored bulk: NVS PDFs, AICTE 201 MB report, PLFS unit data ~5.2 GB): hard to re-download, staged to GCS instead.

`infra/upload_to_gcs.sh` stages both classes to a bucket. **The bucket is a placeholder — set `BUCKET` before running.** No uploads run without it.

> **Open decision for the data team:** the canonical location for the PLFS bulk (~5.2 GB raw + clean) and the NVS/AICTE PDFs is not yet fixed (currently in Dropbox). Decide GCS vs Dropbox and update `infra/upload_to_gcs.sh` + `raw_manifest.csv` accordingly.

## Regenerate

Requires `python>=3.10`, `pandas`, `pyarrow`, `pdfplumber`, `openpyxl`. PLFS load additionally needs `google-cloud-bigquery`.

```bash
# education
python3 education/scripts/<parser>.py     # see education/README.md for the ordered list
python3 education/scripts/build_parquet.py # CSV -> Parquet

# plfs
python3 plfs/scripts/parse_data.py
python3 plfs/scripts/load_bq.py            # requires the unit-level data + GCP auth

# infra
python3 infra/build_raw_manifest.py
bash infra/upload_to_gcs.sh                # after setting BUCKET
```

## Provenance

All data originates from public sources: UDISE+, Ministry of Education, AISHE, AICTE, NMC, NIRF, KVS, NVS, NCERT/NAS, and MoSPI/PLSF. Per-file URLs are in `education/sources/SOURCES.md`, `infra/raw_manifest.csv`, and the per-dataset `*_NOTES.md` files. PLFS unit-level data is gated behind microdata.gov.in and is not redistributed here.
