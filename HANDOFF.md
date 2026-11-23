# BAAJA ABM: handoff

Personal research project (not thesis work), aimed at a policy brief or paper: how S.5653, the Bipartisan American
Affordability and Jobs Act of 2026 (BAAJA, introduced 30 Sep 2026, passed by the Senate 19 Nov 2026), would change US electricity supply.

## State (23 Nov 2026)
- Branch `claude/vibrant-carson-9aw3xo` carries all work (v5 from `claude/epic-carson-9rxakw`, plus Phases 0-1 below).
- `README.md` has the current results, data register and assumption register. `docs/bill_question_map.md` maps every
  bill section to the model (modelled / listed / out of scope). `data/SOURCES.md` lists every raw source.
- Run: `pip install -r requirements.txt`, `python -m pytest -q`, `python run.py --all --runs 100`, `python run.py --uncertainty 400`.

## Plan (agreed 23 Nov 2026)
Headline result: **net supply and adequacy by region and year**. Architecture: **agents where it matters**: keep
the calibrated permitting and court pipeline; rebuild grid access as interacting agents. Standard: paper.

| Phase | What | Status |
|---|---|---|
| 0 | Re-verify; Sec.2213 compliance range; Sim 5 common baseline; CI; sources register; full bill map | done (see below) |
| 1 | Supply accounting: 9 LBNL regions, EIA-860 fleet and retirements, NERC demand, firm capacity, reserve margins | done (see below) |
| 2 | Grid access as agents: regional grid operators with study throughput and hosting room; developers who enter, stay or withdraw; transmission adds MW; Sec.2106/2103/2110/2101/2102/2109/2214 as mechanisms | in progress |
| 3 | Joint uncertainty (Latin hypercube over all ranges), variance decomposition, regional backcast, post-2025 court scenario | harness done (`baaja/uncertainty.py`) |
| 4 | ODD model description, brief, figures | |

## Phase 0 changes
- **Sec.2213 compliance** (`comply_2213`, 0.25 / 0.5 / 1.0): the section's 30- and 90-day clocks have no sponsor
  petition or court order (Sec.1106 has both), so they are no longer assumed always met. Drawn from a side random
  stream so all earlier draws are unchanged.
- **Sim 5 baseline**: ISO / non-ISO completion targets keep LBNL's ratio between markets but are scaled to the pooled
  target, so Sim 5's current law matches Sims 1-4.
- CI (`.github/workflows/tests.yml`), `data/SOURCES.md`, every bill section classified in the bill map.
- **Bill version**: the model now follows the Senate-passed text (substitute to H.R. 2347, KAT26804 V62, passed
  19 Nov 2026, 62-33 per committee press releases). Sec.2106 covers RTOs/ISOs only (`ix_cut_rto`); Sec.1401 gains
  an exception for action "pursuant to any applicable law or regulation" (`halt_mult_1401` 0.1 / 0.5 / 1.0).
- Before any change, all five simulations and the backcast reproduced the committed 20 Nov results exactly.
- Headline: data-sized provisions **+10 GW** by 2041 (renewables +6.7, gas +1.2, storage +0.4), down from +15;
  Sec.2106 ceiling +303 GW (was +456).

## Phase 1 changes
- **Regions**: each project gets one of LBNL's nine regions (`model.draw_region`, own random stream), drawn within its
  ISO / non-ISO market from 2021-25 request shares (active-queue shares for the seeded queue). Sec.2106 covers the six
  FERC RTOs only (`params.RTO_IDX`): ERCOT, the Southeast and the West are outside it.
- **Regional withdrawal hazards** fitted to LBNL completion by region (`calibrate.calibrate_regions`), scaled so the
  pooled target is unchanged. Sim 5's market hazards are skipped when regional ones exist.
- **Seeded queue timing**: projects with a signed IA finish on the measured IA -> operation time (LBNL 2022-25) given
  how long ago they signed; those already overdue finish within a window calibrated so model year 1 matches EIA-860's
  2024-25 additions (`calibrate.calibrate_overdue`). Storage now uses LBNL's own completion (9.1%) and no fitted
  build time. Backcast storage 0.54 -> 1.14.
- **Supply accounting** (`baaja/supply.py`, Sim 6): EIA-860 fleet by region and group, announced retirements plus an
  age hazard, NERC demand / transfers / reference margins, on-peak shares, a per-region factor to NERC's
  existing-certain basis. Four supply assumptions with ranges.
- **Joint uncertainty** (`baaja/uncertainty.py`, `results/uncertainty.md`): Latin hypercube over every assumption,
  paired, rank-regression variance shares.
- Results: data-sized BAAJA +9.7 GW by 2041 (+10 [+6, +16] across all ranges); Sec.2106 ceiling +209 GW (ERCOT now
  excluded); current-law shortfall vs reference margins 68 GW in 2035, mostly PJM; BAAJA's data-sized provisions cut
  it by 0.3 GW.

## Known issues carried forward
- Not yet agent-based: projects are independent draws; interconnection is an exogenous time draw and Sec.2106 a dial.
- Simulation intervals are seed noise at central values; `results/uncertainty.md` has the joint ranges.
- Completion targets treat still-active 2000-20 requests as failures; interconnection times come only from projects
  that signed agreements (Phase 2 calibration with survival methods).
- No feedback from scarcity to entry: regional surpluses (ERCOT, West) and shortfalls (PJM) are not self-correcting (Phase 2).
- Court parameters from 2001-22 cases, before *Seven County Infrastructure Coalition v. Eagle County* (2025).
- Bill version: Senate-passed text, read from the Senate PDF; congress.gov status not yet confirmed (site refuses automated requests). The House may change it.

## Data access from the cloud environment
eia.gov file downloads, govinfo.gov and nerc.com work. emp.lbl.gov, congress.gov and ferc.gov refuse automated
requests; LBNL files need an upload. api.eia.gov needs a free key.

## Still wanted from Eleonora
- A list of federal actions against already-permitted energy projects, 2017-26 (project, technology, date, action,
  outcome): would replace Sim 4's assumed halt rates for technologies other than offshore wind.
- MLRS wind and geothermal right-of-way cases with filing dates (same format as the solar file).

## History
v1: generic projects with an agency queue (`legacy/`). v3: technologies, two gates, assumed parameters. v4: LBNL
calibration, challenger agents. v5 (18-20 Nov): federal nexus, EIS counts, court parameters, seeded queue, backcast,
five simulations, measured federal-land intake. Phase 0 (23 Nov): as above.
