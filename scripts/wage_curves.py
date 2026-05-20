#!/usr/bin/env python3
"""
wage_curves.py — Single source of truth for life-stage wage curves
used in Avanti's RoI and impact calculations.

Loads `extractions/stem_pipeline_buckets_2024-25.csv` (which encodes
NIRF-2025 starting medians + PLFS-2023-24 age-band growth multipliers
+ NIRF / PLFS employment rates, documented in §4 of `whitepaper.md`)
and re-keys the five buckets to the donor-brief tier labels used
downstream.

Public API:

    load_wage_curves() -> dict[tier, dict]
        {'early','mid','senior'} in ₹ Lakhs
        'employment_rate' as fraction 0-1
        'expected_early','expected_mid','expected_senior' = raw × rate

    cumulative_10y_cr(tier, employment_adjusted=True) -> ₹ Crore
        Lifetime earnings over years 1-10 (5 yr early + 5 yr mid).
        Default is employment-adjusted (expected earnings).

    TIER_ORDER -> canonical tier label order

Employment-rate sources (per CSV):
    IIT             0.92  NIRF placement rate
    NIT/IIIT        0.89  NIRF placement rate
    MBBS/BDS        1.00  100% — compulsory internship + NEET-PG funnel
    Top State Eng   0.71  NIRF placement rate (top-100 + 101-200)
    Other Sci       0.36  PLFS Annual 2023-24 regular-employment rate
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "extractions" / "stem_pipeline_buckets_2024-25.csv"

# CSV bucket name → donor-brief tier label
BUCKET_TO_TIER = {
    "1. IITs":                                                                  "IIT",
    "2. NITs / IIITs":                                                          "NIT/IIIT",
    "3. Govt MBBS colleges":                                                    "MBBS/BDS",
    "4. Top-200 NIRF Engineering (non-IIT/NIT/IIIT)":                           "Top State Eng",
    "5. All other STEM grads (non-elite engineering + IT/Computer + non-MBBS medical)":
                                                                                "Other Sci",
}

TIER_ORDER = ["IIT", "NIT/IIIT", "MBBS/BDS", "Top State Eng", "Other Sci"]


def load_wage_curves() -> dict[str, dict]:
    """Return {tier → {early, mid, senior, employment_rate,
                       expected_early, expected_mid, expected_senior}}.

    Raw pay is the NIRF / govt-pay-scale median at graduation;
    progression by PLFS age-band multipliers.
    Employment rate is the share of the cohort in regular employment
    at the early-career age band — multiply through to get expected
    earnings for a randomly-drawn graduate from the bucket.
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Wage curves CSV missing: {CSV_PATH}")
    out: dict[str, dict] = {}
    with CSV_PATH.open() as f:
        for row in csv.DictReader(f):
            tier = BUCKET_TO_TIER.get(row["bucket"])
            if tier is None:
                continue
            early    = float(row["avg_pay_24_29_lakh"])
            mid      = float(row["avg_pay_30_34_lakh"])
            senior   = float(row["avg_pay_35_40_lakh"])
            emp_rate = float(row["employment_rate_pct"]) / 100.0
            out[tier] = {
                "early":             early,
                "mid":               mid,
                "senior":            senior,
                "employment_rate":   emp_rate,
                "expected_early":    early  * emp_rate,
                "expected_mid":      mid    * emp_rate,
                "expected_senior":   senior * emp_rate,
            }
    missing = set(TIER_ORDER) - set(out)
    if missing:
        raise ValueError(f"Wage curves CSV is missing tiers: {missing}")
    return out


def expected_earnings_cr(tier: str,
                          n_early: int = 5,
                          n_mid: int = 5,
                          n_senior: int = 0,
                          curves: dict | None = None,
                          employment_adjusted: bool = True) -> float:
    """₹ Crore expected earnings summed over an arbitrary horizon.

    Pass year counts for each life-stage band. Common horizons:
        1-yr  post-grad     → n_early=1, n_mid=0
        5-yr  post-grad     → n_early=5, n_mid=0
        10-yr post-grad     → n_early=5, n_mid=5   (default)
        15-yr post-grad     → n_early=5, n_mid=5, n_senior=5

    `employment_adjusted=True` (default) multiplies by the bucket's
    employment rate — i.e. expected earnings for a randomly-drawn
    graduate, not "if-employed" earnings.
    """
    curves = curves or load_wage_curves()
    c = curves[tier]
    if employment_adjusted:
        pay = (n_early  * c["expected_early"]
             + n_mid    * c["expected_mid"]
             + n_senior * c["expected_senior"])
    else:
        pay = (n_early  * c["early"]
             + n_mid    * c["mid"]
             + n_senior * c["senior"])
    return pay / 100   # ₹L → ₹Cr


# Backwards-compatible alias (older callers expect the 10-yr form)
def cumulative_10y_cr(tier: str,
                       curves: dict | None = None,
                       employment_adjusted: bool = True) -> float:
    return expected_earnings_cr(tier, n_early=5, n_mid=5,
                                 curves=curves,
                                 employment_adjusted=employment_adjusted)


if __name__ == "__main__":
    print(f"Loading {CSV_PATH.relative_to(ROOT)} …\n")
    curves = load_wage_curves()
    print(f"  {'Tier':<16}{'Emp%':>7}{'Early':>9}{'Mid':>9}{'Senior':>9}"
          f"{'10y-gross':>12}{'10y-expected':>14}")
    for t in TIER_ORDER:
        c = curves[t]
        gross = cumulative_10y_cr(t, curves, employment_adjusted=False)
        exp_  = cumulative_10y_cr(t, curves, employment_adjusted=True)
        print(f"  {t:<16}{c['employment_rate']*100:>6.0f}%"
              f"{c['early']:>7.1f} L{c['mid']:>7.1f} L{c['senior']:>7.1f} L"
              f"{gross:>9.2f} Cr{exp_:>11.2f} Cr")
