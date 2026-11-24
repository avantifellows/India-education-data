#!/usr/bin/env python3
"""Fetch the large source PDFs from GCS into sources/, verifying each checksum.

The PDFs listed in sources/GCS_MANIFEST.csv are too big for git (rule: no data
file over 1MB in git). They live in gs://avantifellows-external-data/<source>/raw/.
The manifest records, per file, its GCS URI, MD5, size, original government URL,
what it contains, and which script or table uses it.

    python3 scripts/fetch_sources.py            # fetch every missing file
    python3 scripts/fetch_sources.py kvs moe    # only files whose name starts with these

Needs `gcloud` authed as an avantifellows.org account with read on the bucket.
A failed download or a checksum mismatch raises; nothing is left half-written.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources" / "GCS_MANIFEST.csv"


def md5_b64(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return base64.b64encode(h.digest()).decode()


def main(prefixes: list[str]) -> int:
    rows = list(csv.DictReader(MANIFEST.open()))
    if prefixes:
        rows = [r for r in rows if r["file"].startswith(tuple(prefixes))]
    for r in rows:
        dest = ROOT / "sources" / r["file"]
        if dest.exists() and md5_b64(dest) == r["md5_base64"]:
            print(f"ok       {r['file']}")
            continue
        tmp = dest.with_name(dest.name + ".part")
        res = subprocess.run(["gcloud", "storage", "cp", r["gcs_uri"], str(tmp)],
                             capture_output=True, text=True)
        if res.returncode != 0:
            tmp.unlink(missing_ok=True)
            raise RuntimeError(f"could not fetch {r['gcs_uri']}:\n{res.stderr.strip()[:500]}")
        got = md5_b64(tmp)
        if got != r["md5_base64"]:
            tmp.unlink()
            raise RuntimeError(f"checksum mismatch for {r['file']}: manifest {r['md5_base64']}, got {got}")
        tmp.replace(dest)
        print(f"fetched  {r['file']}  ({int(r['bytes']) / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
