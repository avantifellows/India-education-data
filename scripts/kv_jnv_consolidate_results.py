"""
Consolidate KV (KVS) and JNV (NVS) Class X / Class XII board-exam results
into a single long-form CSV.

Why a hand-curated script: the source PDFs from KVS and NVS use non-standard
fonts where pdfplumber's table extraction is unreliable. We hand-verified
each number against the relevant page of the source PDF and store the
canonical values here. The script emits the CSV; running it again on
unchanged inputs always produces the same output.

KV (Kendriya Vidyalayas) data sources:
  KVS Annual Report 2021-22 — pp. 108, 109, 110, 111, 113-114
  KVS Annual Report 2022-23 — pp. 121, 125, 126, 128, 133
  KVS Annual Report 2023-24 — pp. 107, 109 (Sci/Com), 110 (Hum), 112

JNV (Jawahar Navodaya Vidyalayas) data sources:
  NVS Annual Report 2023-24 — Appendix XI 'COMPARISON OF PASS PERCENTAGES OF
    JNVs WITH PREVIOUS YEARS CLASS-X & XII' (pp. 204-205) carries the
    five-year trend with national APPEARED / PASSED / % counts.

Output: extractions/kv_jnv_results_class_x_xii.csv
Schema: moe_result_year, board, source_academic_year, level, stream,
        appeared, passed, pass_percentage, source_pdf, source_page_or_note
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extractions" / "kv_jnv_results_class_x_xii.csv"

# (moe_result_year, board, source_academic_year, level, stream, appeared,
#  passed, pass_pct, source_pdf, page_or_note)
DATA = [
    # ---- KV: 2022 board exams (KVS Annual Report 2021-22) ----
    (2022, "KV",  "2021-22", "Class X",   "Overall",     114280, 110421, 96.62, "kvs_annual_report_2021-22.pdf", "p114"),
    (2022, "KV",  "2021-22", "Class XII", "Overall",      92488,  89791, 97.08, "kvs_annual_report_2021-22.pdf", "p108 (region-wise consolidated)"),
    (2022, "KV",  "2021-22", "Class XII", "Science",      51911,  50081, 96.47, "kvs_annual_report_2021-22.pdf", "p109"),
    (2022, "KV",  "2021-22", "Class XII", "Commerce",     23512,  22767, 96.83, "kvs_annual_report_2021-22.pdf", "p110"),
    (2022, "KV",  "2021-22", "Class XII", "Humanities",   17047,  16925, 99.28, "kvs_annual_report_2021-22.pdf", "p111"),

    # ---- KV: 2023 board exams (KVS Annual Report 2022-23) ----
    # MoE didn't publish 2023 results; included for completeness / trend.
    (2023, "KV",  "2022-23", "Class X",   "Overall",     109924, 107761, 98.03, "kvs_annual_report_2022-23.pdf", "p133"),
    (2023, "KV",  "2022-23", "Class XII", "Overall",     100629,  93152, 92.57, "kvs_annual_report_2022-23.pdf", "p121"),
    (2023, "KV",  "2022-23", "Class XII", "Science",      56561,  53321, 94.27, "kvs_annual_report_2022-23.pdf", "p125"),
    (2023, "KV",  "2022-23", "Class XII", "Commerce",     24383,  21413, 87.82, "kvs_annual_report_2022-23.pdf", "p126"),
    (2023, "KV",  "2022-23", "Class XII", "Humanities",   19668,  18404, 93.57, "kvs_annual_report_2022-23.pdf", "p128"),

    # ---- KV: 2024 board exams (KVS Annual Report 2023-24) ----
    (2024, "KV",  "2023-24", "Class X",   "Overall",     102749, 101826, 99.10, "kvs_annual_report_2023-24.pdf", "p112"),
    (2024, "KV",  "2023-24", "Class XII", "Overall",      70985,  70147, 98.82, "kvs_annual_report_2023-24.pdf", "p107"),
    (2024, "KV",  "2023-24", "Class XII", "Science",      40734,  40369, 99.10, "kvs_annual_report_2023-24.pdf", "p109"),
    (2024, "KV",  "2023-24", "Class XII", "Commerce",     17086,  16763, 98.11, "kvs_annual_report_2023-24.pdf", "p109"),
    (2024, "KV",  "2023-24", "Class XII", "Humanities",   13161,  13011, 98.86, "kvs_annual_report_2023-24.pdf", "p110"),

    # ---- JNV: from NVS 2023-24 report Appendix XI 5-year trend table ----
    # NVS does not publish stream-wise (Science/Commerce/Humanities) breakdown
    # at the national level in the annual report.
    (2020, "JNV", "2019-20", "Class X",   "Overall",      40398,  39856, 98.66, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2020, "JNV", "2019-20", "Class XII", "Overall",      29152,  28772, 98.70, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2021, "JNV", "2020-21", "Class X",   "Overall",      41504,  41483, 99.99, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2021, "JNV", "2020-21", "Class XII", "Overall",      32630,  32593, 99.94, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2022, "JNV", "2021-22", "Class X",   "Overall",      45529,  45395, 99.71, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2022, "JNV", "2021-22", "Class XII", "Overall",      35725,  35343, 98.93, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2023, "JNV", "2022-23", "Class X",   "Overall",      45911,  45515, 99.14, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2023, "JNV", "2022-23", "Class XII", "Overall",      35772,  34882, 97.51, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2024, "JNV", "2023-24", "Class X",   "Overall",      44581,  44176, 99.09, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
    (2024, "JNV", "2023-24", "Class XII", "Overall",      34061,  33687, 98.90, "nvs_annual_report_2023-24.pdf", "Appendix XI trend table"),
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "moe_result_year", "board", "source_academic_year", "level",
        "stream", "appeared", "passed", "pass_percentage",
        "source_pdf", "source_page_or_note",
    ]
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for row in DATA:
            w.writerow(row)
    print(f"Wrote {len(DATA)} rows -> {OUT}")

    # Quick consistency print: per (year, board, level), Overall counts
    print("\nKV + JNV 'Overall' pass counts by year/level (for subtraction from CBSE total):")
    print(f"{'year':>4} {'level':10s} {'KV passed':>11s} {'JNV passed':>11s} {'KV+JNV':>11s}")
    by_yr_level = {}
    for r in DATA:
        if r[4] != "Overall":
            continue
        by_yr_level.setdefault((r[0], r[3]), {})[r[1]] = r[6]
    for (yr, lvl), d in sorted(by_yr_level.items()):
        kv = d.get("KV")
        jnv = d.get("JNV")
        total = (kv or 0) + (jnv or 0) if (kv or jnv) else None
        print(f"{yr:>4} {lvl:10s} {str(kv or '—'):>11s} {str(jnv or '—'):>11s} {str(total or '—'):>11s}")


if __name__ == "__main__":
    main()
