"""
Pull AICTE dashboard JSON API at every reasonable cut and save panels.

API endpoint:
  https://facilities.aicte-india.org/dashboard/pages/php/dashboardserver.php

Per (year, program, level, state, institutiontype) filter, the API returns:
  records.girls / records.boys / records.faculties  (scalars for SELECTED year)
  records.intake / .enrollment / .passed / .placed / .instituecount
                                                 (11-element arrays, years
                                                  2012-13 ... 2022-23)

So to get an 11-year time series at any cut we only need to issue ONE query
per cut (the year arg only affects the gender / faculty scalars).

We pull three panels:
  Panel A (national):       program × level × year       =  8 ×  3      ≤ 24
  Panel B (state):          program × level × state      =  8 × 36      = 288
  Panel C (instn-type):     program × level × inst-type  =  8 × 16      = 128

For Panels B and C we set year=9 (2021-22, latest reliable year for gender)
which gives us 11 years of intake/enrolment/passed/placed PLUS the 2021-22
girls / boys scalar. (2022-23 enrolment data is incomplete in the live
dashboard.)

Outputs (all in extractions/):
  aicte_dashboard_panel_national_program_level.csv
  aicte_dashboard_panel_state_program_level.csv
  aicte_dashboard_panel_inst_type_program_level.csv
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "extractions"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ALL_INST = [
    "Private", "Central University",
    "Deemed to be University(Govt)", "Deemed to be University(Pvt)",
    "Deemed University(Government)", "Deemed University(Private)",
    "Government", "Govt aided", "Private-Aided", "Private-Self Financing",
    "State Government University", "State Private University",
    "Unaided - Private", "University Managed",
    "University Managed-Govt", "University Managed-Private",
]
ALL_STATES = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh",
    "Assam", "Bihar", "Chandigarh", "Chhattisgarh",
    "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Orissa", "Puducherry",
    "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
]

YEAR_LABEL = {
    0: "2012-13", 1: "2013-14", 2: "2014-15", 3: "2015-16", 4: "2016-17",
    5: "2017-18", 6: "2018-19", 7: "2019-20", 8: "2020-21", 9: "2021-22",
    10: "2022-23",
}

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

# Throttle requests gently to be a good citizen
DELAY = 0.25  # seconds between requests


def fetch(year_idx: int, program: str, level: str,
          states=ALL_STATES, inst_types=ALL_INST) -> dict:
    params = {
        "year": year_idx,
        "institutiontype": ",".join(inst_types),
        "level": level,
        "program": program,
        "state": ",".join(states),
        "Minority": 1, "Women": 1,
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


def expand_arrays(d: dict, slice_label: str, focal_year_idx: int):
    """Convert one API response into one row per year (11 rows)."""
    rec = d.get("records", {})
    intake = rec.get("intake", []) or []
    enrol = rec.get("enrollment", []) or []
    passed = rec.get("passed", []) or []
    placed = rec.get("placed", []) or []
    instcount = rec.get("instituecount", []) or []
    # Scalars apply to the focal year only
    g_focal = safe_int(rec.get("girls"))
    b_focal = safe_int(rec.get("boys"))
    fac_focal = safe_int(rec.get("faculties"))
    rows = []
    for yi in range(11):
        row = {
            "slice": slice_label,
            "year": YEAR_LABEL[yi],
            "approved_intake": safe_int(intake[yi]) if yi < len(intake) else None,
            "enrolled": safe_int(enrol[yi]) if yi < len(enrol) else None,
            "passed": safe_int(passed[yi]) if yi < len(passed) else None,
            "placed": safe_int(placed[yi]) if yi < len(placed) else None,
            "institutions": safe_int(instcount[yi]) if yi < len(instcount) else None,
            "girls": g_focal if yi == focal_year_idx else None,
            "boys": b_focal if yi == focal_year_idx else None,
            "faculties": fac_focal if yi == focal_year_idx else None,
        }
        rows.append(row)
    return rows


def panel_a_national():
    """Pull each (program, level) at one focal year per year (gender for each)."""
    out = []
    print("Panel A — National × Program × Level × Year")
    for prog, level in PROG_LEVELS:
        for yi in range(11):
            try:
                d = fetch(yi, prog, level)
            except Exception as e:
                print(f"  err {prog}/{level}/{yi}: {e}")
                continue
            rec = d.get("records", {})
            row = {
                "program": prog, "level": level,
                "year": YEAR_LABEL[yi],
                "approved_intake": safe_int((rec.get("intake") or [None]*11)[yi]),
                "enrolled":        safe_int((rec.get("enrollment") or [None]*11)[yi]),
                "passed":          safe_int((rec.get("passed") or [None]*11)[yi]),
                "placed":          safe_int((rec.get("placed") or [None]*11)[yi]),
                "institutions":    safe_int((rec.get("instituecount") or [None]*11)[yi]),
                "girls":           safe_int(rec.get("girls")),
                "boys":            safe_int(rec.get("boys")),
                "faculties":       safe_int(rec.get("faculties")),
            }
            out.append(row)
            time.sleep(DELAY)
    p = OUT_DIR / "aicte_dashboard_panel_national_program_level.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    print(f"  -> wrote {len(out)} rows to {p.name}")
    return out


def panel_b_state(focal_year_idx=9):
    """For each state × (program, level), one query at year=2021-22, gives 11-yr arrays + 2021-22 gender."""
    out = []
    print(f"\nPanel B — State × Program × Level (focal year {YEAR_LABEL[focal_year_idx]})")
    for state in ALL_STATES:
        for prog, level in PROG_LEVELS:
            try:
                d = fetch(focal_year_idx, prog, level, states=[state])
            except Exception as e:
                print(f"  err {state}/{prog}/{level}: {e}")
                continue
            rec = d.get("records", {})
            for yi in range(11):
                row = {
                    "state": state,
                    "program": prog, "level": level,
                    "year": YEAR_LABEL[yi],
                    "approved_intake": safe_int((rec.get("intake") or [None]*11)[yi]),
                    "enrolled":        safe_int((rec.get("enrollment") or [None]*11)[yi]),
                    "passed":          safe_int((rec.get("passed") or [None]*11)[yi]),
                    "placed":          safe_int((rec.get("placed") or [None]*11)[yi]),
                    "institutions":    safe_int((rec.get("instituecount") or [None]*11)[yi]),
                }
                # Gender only for the focal year
                if yi == focal_year_idx:
                    row["girls"] = safe_int(rec.get("girls"))
                    row["boys"]  = safe_int(rec.get("boys"))
                else:
                    row["girls"] = None
                    row["boys"]  = None
                out.append(row)
            time.sleep(DELAY)
    p = OUT_DIR / "aicte_dashboard_panel_state_program_level.csv"
    with p.open("w", newline="") as f:
        cols = ["state","program","level","year","approved_intake","enrolled",
                "passed","placed","institutions","girls","boys"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(out)
    print(f"  -> wrote {len(out)} rows to {p.name}")
    return out


def panel_c_inst_type(focal_year_idx=9):
    """For each institution-type × (program, level), one query."""
    out = []
    print(f"\nPanel C — Institution-Type × Program × Level (focal year {YEAR_LABEL[focal_year_idx]})")
    for itype in ALL_INST:
        for prog, level in PROG_LEVELS:
            try:
                d = fetch(focal_year_idx, prog, level, inst_types=[itype])
            except Exception as e:
                print(f"  err {itype}/{prog}/{level}: {e}")
                continue
            rec = d.get("records", {})
            for yi in range(11):
                row = {
                    "institution_type": itype,
                    "program": prog, "level": level,
                    "year": YEAR_LABEL[yi],
                    "approved_intake": safe_int((rec.get("intake") or [None]*11)[yi]),
                    "enrolled":        safe_int((rec.get("enrollment") or [None]*11)[yi]),
                    "passed":          safe_int((rec.get("passed") or [None]*11)[yi]),
                    "placed":          safe_int((rec.get("placed") or [None]*11)[yi]),
                    "institutions":    safe_int((rec.get("instituecount") or [None]*11)[yi]),
                }
                if yi == focal_year_idx:
                    row["girls"] = safe_int(rec.get("girls"))
                    row["boys"]  = safe_int(rec.get("boys"))
                else:
                    row["girls"] = None
                    row["boys"]  = None
                out.append(row)
            time.sleep(DELAY)
    p = OUT_DIR / "aicte_dashboard_panel_inst_type_program_level.csv"
    with p.open("w", newline="") as f:
        cols = ["institution_type","program","level","year","approved_intake",
                "enrolled","passed","placed","institutions","girls","boys"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(out)
    print(f"  -> wrote {len(out)} rows to {p.name}")
    return out


def main():
    panel_a_national()
    panel_b_state(focal_year_idx=9)
    panel_c_inst_type(focal_year_idx=9)


if __name__ == "__main__":
    main()
