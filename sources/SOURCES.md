# Source PDFs — provenance and download URLs

Every file in `sources/` is published by an Indian government body (MoE / CBSE / KVS / NVS / UGC). All are public; we re-host them in this repo for reproducibility, except the NVS annual reports which are too large for GitHub (each 83-160 MB, exceeding GitHub's 100 MB file limit). The NVS PDFs are gitignored — download fresh copies via the URLs below if you need them.

## UDISE+ (school enrolment)

| File | Source | Size |
|---|---|---|
| `udise_report_2023-24.pdf` | https://www.education.gov.in/sites/upload_files/mhrd/files/statistics-new/udise_report_nep_23_24.pdf | 11 MB |
| `udise_2024-25_enrolment_by_location_category_management_class.xlsx` | UDISE+ Dashboard Report 4000, AY 2024-25 — pulled via [dashboard.udiseplus.gov.in](https://dashboard.udiseplus.gov.in/) | 217 KB |

## AISHE (higher education)

| File | Source | Size |
|---|---|---|
| `aishe_report_2021-22.pdf` | https://cdnbbsr.s3waas.gov.in/s392049debbe566ca5782a3045cf300a3c/uploads/2025/06/2025060466438560.pdf | 9.3 MB |
| `aishe_2021-22_final_report.xlsx` | https://he.nic.in/aishereport/assets/excel/AISHE%20Final%20Report%202021-22.xlsx | 825 KB |
| `aishe_2020-21_final_report.xlsx` | https://he.nic.in/aishereport/assets/excel/AISHE%20Final%20Report%202020-21.xlsx | 887 KB |
| `aishe_2019-20_final_report.xlsx` | https://he.nic.in/aishereport/assets/excel/AISHE%20Final%20Report%202019-20.xlsx | 754 KB |

The 2019-20, 2020-21, 2021-22 Excels are the panel for the AISHE 3-year linear-extrapolation projection (`scripts/aishe_panel_*`).

## Sectoral regulators — for current-year (2024-25 / 2025-26) capacity

These are used in `extractions/higher_ed_capacity_2025-26_consolidated.csv` to update the AISHE picture to current dates.

| File | Source | Notes |
|---|---|---|
| `nmc_mbbs_seat_matrix_2024-25.pdf` | https://www.nmc.org.in/wp-content/uploads/2025/04/Revised%20UG%20Seat%20Matrix%202024-25%20on%2031-03-2025.pdf | Definitive list of all 780 MBBS colleges + seat counts as of 31-Mar-2025 |

AICTE (engineering, pharmacy, MBA, MCA, architecture) doesn't publish a single canonical PDF of approved intake; their `aicte-india.org` dashboard is interactive. We've cited their announced 2025-26 numbers (15.98 lakh first-year B.Tech intake across 5,875 institutions) directly in the consolidated CSV with reference URLs in the notes column.

## MoE 'Results of Secondary and Higher Secondary Examinations' (board exam compilation)

| File | Source URL |
|---|---|
| `moe_results_secondary_hs_2020.pdf` | https://www.education.gov.in/sites/upload_files/mhrd/files/statistics-new/Result_Secondary_Higher_Secondary_Examination_2020.pdf |
| `moe_results_secondary_hs_2021.pdf` | https://www.education.gov.in/sites/upload_files/mhrd/files/statistics-new/RSHSE2021.pdf |
| `moe_results_secondary_hs_2022.pdf` | https://www.education.gov.in/sites/upload_files/mhrd/files/statistics-new/RSHSE2022.pdf |
| `moe_results_secondary_hs_2024.pdf` | https://www.education.gov.in/sites/upload_files/mhrd/files/statistics-new/result-2024.pdf |

(MoE didn't publish a 2023 edition.)

## CBSE press releases

| File | Source URL |
|---|---|
| `cbse_press_class_xii_2024.pdf` | https://www.cbse.gov.in/cbsenew/documents//PRESS_NOTE_DECLARATION_CLASS_XII_RESULT_2024_21052024.pdf |

Index page: https://www.cbse.gov.in/cbsenew/press.html

## KVS annual reports

Index page: https://kvsangathan.nic.in/en/annual-reports/

| File | Source URL |
|---|---|
| `kvs_annual_report_2021-22.pdf` | https://cdnbbsr.s3waas.gov.in/s32d2ca7eedf739ef4c3800713ec482e1a/uploads/2023/10/2023100384.pdf |
| `kvs_annual_report_2022-23.pdf` | https://cdnbbsr.s3waas.gov.in/s32d2ca7eedf739ef4c3800713ec482e1a/uploads/2023/12/2023122733.pdf |
| `kvs_annual_report_2023-24.pdf` | https://cdnbbsr.s3waas.gov.in/s32d2ca7eedf739ef4c3800713ec482e1a/uploads/2025/01/2025012096.pdf |

## NVS annual reports — gitignored (too large)

Index page: https://navodaya.gov.in/nvs/en/Downloads/

To get these PDFs locally, run:

```bash
cd sources
for entry in \
  "2023-24:1fu22TI72I5pFaHIzzWOCNVK65mqE4C46" \
  "2022-23:1-8ccGYPMfJWPMPRrJJQsc5snUFr_ExtL" \
  "2021-22:1UOktrC3PaqZ6vKwB2wTOTgv4nLQXhq8W" \
  "2020-21:1ncWxKjoLe8gph0a1ZjY8Z39zbzDYpkzt" \
  "2019-20:1nL1iiBFYVDReNcSqUN8jqUFrUa59e1AR"; do
  yr=$(echo $entry | cut -d: -f1); fid=$(echo $entry | cut -d: -f2)
  curl -sL --cookie /tmp/gd.cookie --cookie-jar /tmp/gd.cookie \
    -o "nvs_annual_report_${yr}.pdf" \
    "https://drive.usercontent.google.com/download?id=${fid}&export=download&confirm=t"
done
```

Sizes: 83–160 MB each (5 PDFs, ~600 MB total).

> Note: the headline KV-vs-JNV consolidation in `extractions/kv_jnv_results_class_x_xii.csv` only depends on `nvs_annual_report_2023-24.pdf` — its Appendix XI carries the 5-year national-totals trend table. The other 4 NVS reports were used for cross-verification only.
