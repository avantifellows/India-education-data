"""
NAS 2021 — national-aggregated performance and proficiency by management & location.

Inputs:
  sources/nas_2021_data/csv_data/performance_percentage_statewise/*_by_management.csv
  sources/nas_2021_data/csv_data/performance_percentage_statewise/*_by_location.csv
  sources/nas_2021_data/csv_data/NAS_participation_state.csv

Output:
  extractions/nas_2021_national_proficiency.csv
    Columns: grade, subject, dimension (mgmt/loc), category, pct_correct_mean,
             pct_proficient_advanced, pct_basic_below_basic

Method:
  NAS publishes scaled and percent-correct data at the state level only.
  We aggregate to national using student-count weights, derived as
  total_student × share-of-students-from-this-category. The share columns
  (govt_school, private_school, etc.) are percentages of the state's sampled
  student count from each management/location bucket.

  IMPORTANT: NAS reports "% Proficient and Advance" as a single combined band
  (top tail) and "% Basic and Below Basic" as the bottom tail. They do not
  publish the four-band split separately in this data set.
"""
import pandas as pd
import glob
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "sources/nas_2021_data/csv_data")
OUT = os.path.join(REPO, "extractions/nas_2021_national_proficiency.csv")


def load_mgmt():
    files = glob.glob(f"{SRC}/performance_percentage_statewise/*_by_management.csv")
    return pd.concat([pd.read_csv(f, sep=";") for f in files], ignore_index=True)


def load_loc():
    files = glob.glob(f"{SRC}/performance_percentage_statewise/*_by_location.csv")
    return pd.concat([pd.read_csv(f, sep=";") for f in files], ignore_index=True)


def load_part():
    p = pd.read_csv(f"{SRC}/NAS_participation_state.csv", sep=";")
    # Some states have multiple rows per (state, grade); keep the latest
    return p.sort_values("id").groupby(["state_name", "grade"]).last().reset_index()


def weighted(df_perf, df_part, val_col, share_col):
    """National student-weighted average of val_col across states.
    Weight = total_student × share_col / 100 from participation file.
    """
    m = df_perf.merge(
        df_part[["state_name", "grade", "total_student", share_col]],
        on=["state_name", "grade"],
        how="inner",
    )
    m["wt"] = m["total_student"] * m[share_col] / 100.0
    m = m.dropna(subset=[val_col, "wt"])
    m = m[m["wt"] > 0]
    if m["wt"].sum() == 0:
        return float("nan")
    return (m[val_col] * m["wt"]).sum() / m["wt"].sum()


def main():
    mgmt = load_mgmt()
    loc = load_loc()
    part = load_part()
    rows = []

    mgmt_specs = [
        ("State Govt", "govt", "govt_proficient_and_advance",
         "govt_basic_and_below_basic", "govt_school"),
        ("Govt Aided", "govt_aided", "govt_aided_proficient_and_advance",
         "govt_aided_basic_and_below_basic", "govt_aided_school"),
        ("Private Recognised", "private", "private_proficient_and_advance",
         "private_basic_and_below_basic", "private_school"),
        ("Central Govt", "central_govt", "central_govt_proficient_and_advance",
         "central_govt_basic_and_below_basic", "central_govt_school"),
    ]
    loc_specs = [
        ("Rural", "rural", "rural_proficient_and_advance",
         "rural_basic_and_below_basic", "rural_location"),
        ("Urban", "urban", "urban_proficient_and_advance",
         "urban_basic_and_below_basic", "urban_location"),
    ]

    for grade in [3, 5, 8, 10]:
        for subj in sorted(mgmt["subject"].unique()):
            g = mgmt[(mgmt["grade"] == grade) & (mgmt["subject"] == subj)]
            if len(g) == 0:
                continue
            for cat, pc_col, pa_col, bb_col, share_col in mgmt_specs:
                rows.append({
                    "grade": grade,
                    "subject": subj,
                    "dimension": "management",
                    "category": cat,
                    "pct_correct_mean": weighted(g, part, pc_col, share_col),
                    "pct_proficient_advanced": weighted(g, part, pa_col, share_col),
                    "pct_basic_below_basic": weighted(g, part, bb_col, share_col),
                })
        for subj in sorted(loc["subject"].unique()):
            l = loc[(loc["grade"] == grade) & (loc["subject"] == subj)]
            if len(l) == 0:
                continue
            for cat, pc_col, pa_col, bb_col, share_col in loc_specs:
                rows.append({
                    "grade": grade,
                    "subject": subj,
                    "dimension": "location",
                    "category": cat,
                    "pct_correct_mean": weighted(l, part, pc_col, share_col),
                    "pct_proficient_advanced": weighted(l, part, pa_col, share_col),
                    "pct_basic_below_basic": weighted(l, part, bb_col, share_col),
                })

    df = pd.DataFrame(rows)
    df = df.round(2)
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} rows → {OUT}")
    print("\nSample for Class 5 Math:")
    print(df[(df["grade"] == 5) & (df["subject"] == "math")].to_string(index=False))


if __name__ == "__main__":
    main()
