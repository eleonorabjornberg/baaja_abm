# BAAJA ABM: handoff

Personal research project (not thesis work), aimed at a policy brief or paper: how S.5653, the Bipartisan American
Affordability and Jobs Act of 2026 (BAAJA, introduced 30 Sep 2026), would change US electricity supply.

## State (23 Nov 2026)
- Branch `claude/vibrant-carson-9aw3xo` carries all work (v5 from `claude/epic-carson-9rxakw`, plus Phase 0 below).
- `README.md` has the current results, data register and assumption register. `docs/bill_question_map.md` maps every
  bill section to the model (modelled / listed / out of scope). `data/SOURCES.md` lists every raw source.
- Run: `pip install -r requirements.txt`, `python -m pytest -q`, `python run.py --all --runs 100` (~10 min).

## Plan (agreed 23 Nov 2026)
Headline result: **net supply and adequacy by region and year**. Architecture: **agents where it matters**: keep
the calibrated permitting and court pipeline; rebuild grid access as interacting agents. Standard: paper.

| Phase | What | Status |
|---|---|---|
| 0 | Re-verify; Sec.2213 compliance range; Sim 5 common baseline; CI; sources register; full bill map | done (see below) |
| 1 | Supply accounting: 9 LBNL regions, EIA-860 fleet and retirements, NERC demand, firm capacity, reserve margins | next |
| 2 | Grid access as agents: regional grid operators with study throughput and hosting room; developers who enter, stay or withdraw; transmission adds MW; Sec.2106/2103/2110/2101/2102/2109/2214 as mechanisms | |
| 3 | Joint uncertainty (Latin hypercube over all ranges), variance decomposition, regional backcast, post-2025 court scenario | harness alongside Phase 1 |
| 4 | ODD model description, brief, figures | |

## Phase 0 changes
- **Sec.2213 compliance** (`comply_2213`, 0.25 / 0.5 / 1.0): the section's 30- and 90-day clocks have no sponsor
  petition or court order (Sec.1106 has both), so they are no longer assumed always met. Drawn from a side random
  stream so all earlier draws are unchanged.
- **Sim 5 baseline**: ISO / non-ISO completion targets keep LBNL's ratio between markets but are scaled to the pooled
  target, so Sim 5's current law matches Sims 1-4.
- CI (`.github/workflows/tests.yml`), `data/SOURCES.md`, every bill section classified in the bill map.

## Known issues carried forward
- Not yet agent-based: projects are independent draws; interconnection is an exogenous time draw and Sec.2106 a dial.
- Outcome is new GW only: no fleet, retirements, demand, regions (Phase 1).
- Intervals are seed noise at central values (Phase 3).
- Completion targets treat still-active 2000-20 requests as failures; interconnection times come only from projects
  that signed agreements (Phase 2 calibration with survival methods).
- Storage backcast 0.54 of EIA additions.
- Court parameters from 2001-22 cases, before *Seven County Infrastructure Coalition v. Eagle County* (2025).
- Bill version: model follows the introduced text; a manager's amendment (7 Nov 2026, per C2ES) is not yet on GovInfo.

## Data access from the cloud environment
eia.gov file downloads, govinfo.gov and nerc.com work. emp.lbl.gov, congress.gov and ferc.gov refuse automated
requests; LBNL files need an upload. api.eia.gov needs a free key.

## Still wanted from Eleonora
- A list of federal actions against already-permitted energy projects, 2017-26 (project, technology, date, action,
  outcome): would replace Sim 4's assumed halt rates for technologies other than offshore wind.
- MLRS wind and geothermal right-of-way cases with filing dates (same format as the solar file).
- For Phase 2: the LBNL workbook again (`LBNL_Ix_Queue_Data_File_thru2025.xlsx`), since the site refuses downloads.

## History
v1: generic projects with an agency queue (`legacy/`). v3: technologies, two gates, assumed parameters. v4: LBNL
calibration, challenger agents. v5 (18-20 Nov): federal nexus, EIS counts, court parameters, seeded queue, backcast,
five simulations, measured federal-land intake. Phase 0 (23 Nov): as above.
