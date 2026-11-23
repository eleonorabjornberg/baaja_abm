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
| EIA-860 annual 2015 | `eia8602015.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602015.zip | 23 Nov 2026 | Download, `d93225cc01f24f8eaf4b8b447b83c2b527608391b12a573819b1b2b6e2888334` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2016 | `eia8602016.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602016.zip | 23 Nov 2026 | Download, `27d17d22b9cf0da8167579a05ae04383ba3b3432f53080af84a99427b9020124` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2017 | `eia8602017.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602017.zip | 23 Nov 2026 | Download, `da9f1a1f8528324ff47019229d0f3648efe8c5997f18449f10d6aad2daa68e5c` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2018 | `eia8602018.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602018.zip | 23 Nov 2026 | Download, `46864f69f190da9a0d1096964984219d7728b4c626c3bc8a48767507632b18df` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2019 | `eia8602019.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602019.zip | 23 Nov 2026 | Download, `6fe0d37858359c50772fbcb1a6cfca0a3fbf442423ddf4e0d33df929caa1ea7b` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2020 | `eia8602020.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602020.zip | 23 Nov 2026 | Download, `ce519fd0b02c74b8c4231dc023bf07f922ae5f2a018fcaf88914502f61aa89ea` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2021 | `eia8602021.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602021.zip | 23 Nov 2026 | Download, `ac35e582335ed5f82c1177361d6e8e82cff083ae85a5ec668815d21e0aef3ee5` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2022 | `eia8602022.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602022.zip | 23 Nov 2026 | Download, `a6f6b00f480ccfb7436804f5cb9984f27c3e0c20cfcbe9b4ed057285b5a68980` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2023 | `eia8602023.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602023.zip | 23 Nov 2026 | Download, `1447e23e608bea1523961542a90eb93ea86715067a37f211282541461049b46f` | Phase 1 fleet history, regional backcast |
| EIA-860 annual 2024 | `eia8602024.zip` | https://www.eia.gov/electricity/data/eia860/archive/xls/eia8602024.zip | 23 Nov 2026 | Download, `0aaae04812cd4ab87a3e346bdf93848a3cc15053fd4dc2a4cf82d2aeac95f12b` | Phase 1 fleet history, regional backcast |
| EIA-923 2025 (generation and fuel by plant) | `f923_2025.zip` | https://www.eia.gov/electricity/data/eia923/xls/f923_2025.zip | 23 Nov 2026 | Download, `1bff7092a86f6678c069c986829da5a23104048fc1aafb65b0776e3c904284de` | Phase 1 capacity factors, TWh by region |
| EIA-861 2025 (retail sales, peak by utility) | `f8612025.zip` | https://www.eia.gov/electricity/data/eia861/zip/f8612025.zip | 23 Nov 2026 | Download, `f59f6c732bf685fe0a1591b32227f5ce572dc0dfd26bb5caaeed128ac4e3a396` | Phase 1 demand cross-check |
| NERC 2025 Long-Term Reliability Assessment (published Feb 2026) | `NERC_LTRA_2025.pdf` | https://www.nerc.com/pa/RAPA/ra/Reliability%20Assessments%20DL/NERC_LTRA_2025.pdf | 23 Nov 2026 | Download, `a3217a96b26f6d3e0dffa08c1151abedadc31a9a3d9a8be325afc0fc518369ca` | Phase 1 peak demand, on-peak capacity, reference margins |
| ERCOT Capacity, Demand and Reserves report, Dec 2025 | `CapacityDemandandReservesReport_December2025.xlsx` | https://www.ercot.com/files/docs/2025/12/19/CapacityDemandandReservesReport_December2025.xlsx | 23 Nov 2026 | Download, `c26afc32ca220a61b0ec9854b074917d933a37bffa8a164f7d2ff7df6135db67` | Phase 1 ERCOT capacity contributions |
| NYISO interconnection queue, 31 Oct 2026 | `NYISO-Interconnection-Queue-10312026.xlsx` | https://www.nyiso.com/interconnections | 23 Nov 2026 | Download, `6fefffbefe5f69d93b44dde9d81b27e119beb5adbe4f8d12cf3cc45bef538140` | Phase 2 queue calibration |
| PJM ELCC report 2026 and preliminary class ratings DY28-42 | `2026-pjm-elcc-rrs.pdf; preliminary-elcc-class-ratings-for-period-dy28-dy42-elcc.pdf` | https://www.pjm.com/planning/resource-adequacy-planning/effective-load-carrying-capability | 23 Nov 2026 | Download, `2cac1dae50e3a665f13646926ff1bb9e07d770679e677e8a0aaa83d95b7488a1` | Phase 1 firm capacity |
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
| Senate-passed substitute to H.R. 2347 (KAT26804 V62; passed 19 Nov 2026) | `KAT26804_V62.pdf` | https://www.energy.senate.gov/wp-content/uploads/2026/11/KAT26804_V62.pdf | 23 Nov 2026 | Download, `4ce3b2f06e8be69695fe6fc34b5784f0e4d451ec033f0405ce587167f3799857` | `docs/bill_question_map.md`; text via `pdftotext -layout` |
| Manager's substitute as released 7 Nov 2026 (KAT26764) | `ANS_HR2347_2026-11-07.pdf` | https://www.epw.senate.gov/wp-content/uploads/media/doc/11.7.26%20ANS%20to%20H.R.%202347.pdf | 23 Nov 2026 | Download, `17a0efcf8d0cd5e952287b996e5390dae4f196a31d4d0e89951ca996ab10c7eb` | reference |

## Access from the cloud environment (23 Nov 2026)
- Reachable: eia.gov file downloads, govinfo.gov, nerc.com, energy.senate.gov, epw.senate.gov, ercot.com, nyiso.com, pjm.com documents.
- Interactive only (no direct file link found): SPP, ISO-NE and PJM queue exports; not needed while the LBNL workbook covers those regions.
- All hashes are also in `raw/SHA256SUMS`.
- Refused automated requests (HTTP 403): emp.lbl.gov, congress.gov (site and API), ferc.gov, misoenergy.org.
- api.eia.gov needs a free API key.
