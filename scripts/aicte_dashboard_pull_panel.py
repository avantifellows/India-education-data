"""
Pull AICTE's public dashboard API for a year-by-year panel of approved
intake, enrolment, girls, boys for each programme × level.

API endpoint: https://facilities.aicte-india.org/dashboard/pages/php/dashboardserver.php
The endpoint returns JSON with:
  records.girls / records.boys      — scalars for the SELECTED year
  records.intake / .enrollment / .passed / .placed / .instituecount
                                    — 11-element arrays, one per year
                                      (index 0 = 2012-13 ... index 10 = 2022-23)

The dashboard's data only goes through AY 2022-23 (and 2022-23 enrolment is
incomplete in the live data). For 2023-24 / 2024-25 / 2025-26 we use AICTE's
Annual Report 2024-25 + press release figures separately.

Output: extractions/aicte_dashboard_panel_2012-2023.csv
"""
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extractions" / "aicte_dashboard_panel_2012-2023.csv"

ITYPE = ",".join([
    "Private", "Central University",
    "Deemed to be University(Govt)", "Deemed to be University(Pvt)",
    "Deemed University(Government)", "Deemed University(Private)",
    "Government", "Govt aided", "Private-Aided", "Private-Self Financing",
    "State Government University", "State Private University",
    "Unaided - Private", "University Managed",
    "University Managed-Govt", "University Managed-Private",
])
STATE = ",".join([
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh",
    "Assam", "Bihar", "Chandigarh", "Chhattisgarh",
    "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Orissa", "Puducherry",
    "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
])

YEAR_LABEL = {
    0: "2012-13", 1: "2013-14", 2: "2014-15", 3: "2015-16", 4: "2016-17",
    5: "2017-18", 6: "2018-19", 7: "2019-20", 8: "2020-21", 9: "2021-22",
    10: "2022-23",
}

# (program, level) combinations to pull
PROG_LEVELS = [
    ("Engineering and Technology", "UG"),
    ("Engineering and Technology", "PG"),
    ("Engineering and Technology", "DIPLOMA"),
    ("Management", "PG"),
    ("MCA", "PG"),
    ("Pharmacy", "UG"),
    ("Architecture", "UG"),
    ("Hotel Management and Catering", "UG"),
]


def fetch(year_idx: int, program: str, level: str) -> dict:
    params = {
        "year": year_idx, "institutiontype": ITYPE, "level": level,
        "program": program, "state": STATE, "Minority": 1, "Women": 1,
    }
    qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = (
        "https://facilities.aicte-india.org/dashboard/pages/php/"
        f"dashboardserver.php?{qs}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def safe_int(v):
    if v in (None, "", "null"):
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def main() -> None:
    rows = []
    for program, level in PROG_LEVELS:
        for yr_idx in range(11):
            try:
                d = fetch(yr_idx, program, level)
            except Exception as e:
                print(f"err {program}/{level}/{yr_idx}: {e}")
                continue
            rec = d.get("records", {})
            girls = safe_int(rec.get("girls"))
            boys = safe_int(rec.get("boys"))
            intake_arr = rec.get("intake", [])
            enrol_arr = rec.get("enrollment", [])
            intake = safe_int(intake_arr[yr_idx]) if yr_idx < len(intake_arr) else None
            enrol = safe_int(enrol_arr[yr_idx]) if yr_idx < len(enrol_arr) else None
            fpct = (
                round(girls / (girls + boys) * 100, 1)
                if girls is not None and boys is not None and (girls + boys) > 0
                else None
            )
            rows.append({
                "program": program,
                "level": level,
                "year": YEAR_LABEL[yr_idx],
                "approved_intake": intake,
                "enrolled": enrol,
                "girls": girls,
                "boys": boys,
                "female_pct": fpct,
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["program", "level", "year", "approved_intake",
                        "enrolled", "girls", "boys", "female_pct"],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {OUT}")

    # Print Engineering UG headline
    print("\n=== AICTE Engineering UG — 11-year panel ===")
    print(f"{'Year':10s} {'Intake':>10s} {'Enrol':>10s} {'Girls':>10s} {'Boys':>10s} {'Female %':>9s}")
    for r in rows:
        if r["program"] == "Engineering and Technology" and r["level"] == "UG":
            print(
                f"{r['year']:10s} "
                f"{r['approved_intake']:>10,} "
                f"{r['enrolled']:>10,} "
                f"{r['girls']:>10,} "
                f"{r['boys']:>10,} "
                f"{(r['female_pct'] or 0):>8.1f}%"
            )


if __name__ == "__main__":
    main()
