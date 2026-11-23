# Data sources

Raw files are not committed (`raw/` is git-ignored). Each extractor reads a raw file and writes a JSON summary in
`data/`, which is committed. To reproduce a summary, get the raw file below and run its extractor.

**Status** says how the raw file was obtained. *Download*: fetched directly from the URL by Claude; the hash is of
the file as fetched. *Upload*: supplied by Eleonora in an earlier session (18-20 Nov 2026); the file was not kept and
its hash was not recorded, so the summary can be regenerated only from a fresh copy, which may differ if the
publisher has revised it.

## Files used by the current model

| Source | Raw file | URL | Retrieved | Status / sha256 | Extractor -> summary |
|---|---|---|---|---|---|
| LBNL, *Queued Up*: interconnection queue data through 2025 (CC BY 4.0) | `LBNL_Ix_Queue_Data_File_thru2025.xlsx` | https://emp.lbl.gov/queues (refuses automated requests) | Nov 2026 | Upload | `extract_lbnl.py` -> `lbnl_targets.json`; `extract_engine_inputs.py` -> `engine_inputs.json`; `extract_interconnection_benchmark.py` -> `interconnection_benchmark.json` |
| EIA-860, 2025 annual (generators, plants, ownership) | `eia8602025.zip` | https://www.eia.gov/electricity/data/eia860/xls/eia8602025.zip | 23 Nov 2026 | Download, `2b27929d26cc1da9ad6a530da1cac6718cd8496098ee560c4d47cfffd96d08ba` | `extract_engine_inputs.py`, `extract_federal_nexus.py` (earlier copy was uploaded) |
| EIA-860M, September 2026 (monthly generator inventory) | `september_generator2026.xlsx` | https://www.eia.gov/electricity/data/eia860m/xls/september_generator2026.xlsx | 23 Nov 2026 | Download, `bcef74e1af991680731aeecfda967f5950db4ce739bb584edd8b8774c7e6da17` | `extract_eia860m.py` -> `eia860m_targets.json` (earlier copy was uploaded); Phase 1 fleet |
| EIA-860M, December 2021 | `december_generator2021.xlsx` | https://www.eia.gov/electricity/data/eia860m/ (archive) | Nov 2026 | Upload | `extract_eia860m.py` |
| EIA-860 annual additions (for the backcast) | EIA-860 2025 | as above | Nov 2026 | Upload | `eia860_additions.json` |
| BLM Surface Management Agency (land ownership) | SMA geodata | https://www.blm.gov (publisher) | Nov 2026 | Upload | `extract_federal_nexus.py` -> `federal_nexus_targets.json` |
| USACE ORM final individual permits | ORM export | https://www.usace.army.mil (publisher) | Nov 2026 | Upload | `extract_engine_inputs.py`, `combine_federal_hooks.py` |
| USDA RUS electric program awards | RUS award list | https://www.rd.usda.gov (publisher) | Nov 2026 | Upload | `combine_federal_hooks.py` -> `federal_nexus_combined.json` |
| CEQ EIS Timeline Data 2010-2024 | CEQ workbook | https://ceq.doe.gov (publisher) | Nov 2026 | Upload | `extract_ceq_eis.py` -> `ceq_eis_targets.json`, `ceq_electricity_eis.csv` |
| Case-level NEPA litigation export (1,821 cases, 2001-22) | case export | (supplied) | Nov 2026 | Upload | `extract_nepa_cases.py` -> `nepa_case_targets.json`; `extract_limitation_experiment.py` -> `limitation_experiment.json` |
| BLM ePlanning NEPA register (2,594 energy actions) | ePlanning export | https://eplanning.blm.gov | Nov 2026 | Upload | `extract_blm_eplanning.py` -> `blm_eplanning_targets.json` |
| BLM MLRS solar development grants (741 cases; 459 with filing dates) | MLRS exports | https://mlrs.blm.gov | Nov 2026 | Upload | `extract_mlrs.py` -> `mlrs_targets.json`; `extract_mlrs_filing.py` -> `mlrs_filing_targets.json` |
| Wind habitat conservation plans | Dryad file list | https://doi.org/10.5061/dryad.59zw3r2kf | Nov 2026 | Upload | `extract_wind_hcp.py` -> `wind_hcp_targets.json` |
| Sabin Center Climate Backtracker | export | https://climate.law.columbia.edu (publisher) | Nov 2026 | Upload | `extract_backtracker.py` -> `backtracker_summary.json` |
| Sabin Center, contested renewable projects and local restrictions (2026) | report tables | https://climate.law.columbia.edu | Nov 2026 | Upload | `extract_permits_opposition.py` -> `permits_opposition_targets.json` |
| DOE NEPA document lists (EAs, EISs) | DOE lists | https://www.energy.gov/nepa (publisher) | Nov 2026 | Upload | `extract_permits_opposition.py`, `combine_federal_hooks.py` |
| Bennon & Wilson (2023), 53 ELR 10836; RFF | paper | - | - | literature value | `params.LIT_EIS` |
| EIA Electric Power Monthly capacity factors; NREL ATB (offshore wind) | tables | https://www.eia.gov/electricity/monthly/ | - | literature value | `params.CF` |
| S.5653 as introduced (30 Sep 2026) | `BILLS-119s5653is.htm` | https://www.govinfo.gov/content/pkg/BILLS-119s5653is/html/BILLS-119s5653is.htm | 23 Nov 2026 | Download, `422863b1a4c35847d0f585f502cdf77150eacf940cff305b0f1fd08e8ed7cdfe` | `docs/bill_question_map.md` |

## Access from the cloud environment (23 Nov 2026)
- Reachable: eia.gov file downloads, govinfo.gov, nerc.com.
- Refused automated requests (HTTP 403): emp.lbl.gov, congress.gov (site and API), ferc.gov.
- api.eia.gov needs a free API key.
