"""
Project AISHE UG enrolment + out-turn by discipline forward to AY 2024-25
and AY 2025-26 using a simple linear fit on the 3-year panel
(2019-20 → 2020-21 → 2021-22).

Output: extractions/aishe_ug_discipline_extrapolated_2024-26.csv
Schema: target_year, metric, discipline, gender, value_estimate,
        method, slope_per_year, base_year_value, growth_pct_total

Methodology and caveats are documented in the accompanying NOTES file.
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "extractions" / "aishe_ug_discipline_panel_2019-22.csv"
OUT = ROOT / "extractions" / "aishe_ug_discipline_extrapolated_2024-26.csv"

# Map AISHE year string -> integer year-index (academic year start)
YEAR_INDEX = {
    "2019-20": 2019,
    "2020-21": 2020,
    "2021-22": 2021,
}
TARGET_YEARS = {
    "2024-25": 2024,
    "2025-26": 2025,
}

# Disciplines we exclude from output (aggregator rows captured by extractor)
EXCLUDE_DISCIPLINES = {"Grand", "All India", "Grand Total", "Total"}


def linear_fit(xs, ys):
    """Return (slope, intercept) from a simple least-squares fit."""
    n = len(xs)
    if n < 2:
        return 0.0, ys[0] if ys else 0.0
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    if den == 0:
        return 0.0, mean_y
    slope = num / den
    intercept = mean_y - slope * mean_x
    return slope, intercept


def main():
    # Load panel
    rows = list(csv.DictReader(PANEL.open()))
    # Index: (metric, discipline, gender) -> list of (year_int, value)
    by_key = defaultdict(list)
    for r in rows:
        d = r["discipline"].strip()
        if d in EXCLUDE_DISCIPLINES:
            continue
        if d.startswith("Grand") or d.lower() in ("all india",):
            continue
        yr = YEAR_INDEX.get(r["aishe_year"])
        if yr is None:
            continue
        by_key[(r["metric"], d, r["gender"])].append((yr, int(r["value"])))

    out_rows = []
    for (metric, disc, gender), points in sorted(by_key.items()):
        if len(points) < 2:
            continue
        # Sort by year
        points.sort()
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        # Need a non-zero last value for meaningful projection
        if max(ys) == 0:
            continue
        slope, intercept = linear_fit(xs, ys)
        base_year_val = ys[-1]
        base_year = xs[-1]
        for target_label, target_int in TARGET_YEARS.items():
            est = slope * target_int + intercept
            # Floor at 0 (negative projections meaningless)
            est = max(0.0, est)
            yrs_forward = target_int - base_year
            growth_pct = ((est / base_year_val) - 1) * 100 if base_year_val else 0
            out_rows.append({
                "target_year": target_label,
                "metric": metric,
                "discipline": disc,
                "gender": gender,
                "value_estimate": int(round(est)),
                "method": f"linear fit on {len(points)} years (2019-22)",
                "slope_per_year": round(slope, 1),
                "base_year_value": base_year_val,
                "base_year": f"{base_year}-{(base_year+1)%100:02d}",
                "years_extrapolated": yrs_forward,
                "growth_pct_total": round(growth_pct, 1),
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "target_year", "metric", "discipline", "gender", "value_estimate",
        "method", "slope_per_year", "base_year", "base_year_value",
        "years_extrapolated", "growth_pct_total",
    ]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {len(out_rows)} rows -> {OUT}")

    # Print headline 2025-26 projections
    print("\n=== Projected UG OUT-TURN (graduates) by major discipline, AY 2025-26 ===")
    proj = {(r["discipline"], r["gender"]): r for r in out_rows
            if r["target_year"] == "2025-26" and r["metric"] == "out_turn"}
    print(f"{'Discipline':30s} {'2021-22':>11s} {'2025-26 est':>12s} {'4-yr +%':>8s} {'female %':>9s}")
    disc_totals = sorted(
        {d for d, g in proj if g == "Total"},
        key=lambda d: -proj[(d, "Total")]["value_estimate"],
    )
    for d in disc_totals[:15]:
        t_proj = proj[(d, "Total")]
        f_proj = proj.get((d, "Female"))
        female_pct = (f_proj["value_estimate"] / t_proj["value_estimate"] * 100
                      if f_proj and t_proj["value_estimate"] else 0)
        print(f"{d:30s} {t_proj['base_year_value']:>11,} "
              f"{t_proj['value_estimate']:>12,} {t_proj['growth_pct_total']:>+7.1f}% "
              f"{female_pct:>8.1f}%")


if __name__ == "__main__":
    main()
