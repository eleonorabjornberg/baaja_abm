# BAAJA ABM: handoff

Personal research project (not thesis work), aimed at a policy brief or paper: how S.5653, the Bipartisan American
Affordability and Jobs Act of 2026 (BAAJA, introduced 30 Sep 2026, passed by the Senate 19 Nov 2026), would change US electricity supply.

## State (23 Nov 2026)
- Branch `claude/vibrant-carson-9aw3xo` carries all work (v5 from `claude/epic-carson-9rxakw`, plus Phases 0-2 below).
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
| 2 | Grid access as agents: regional grid operators with study throughput and hosting room; developers who enter, stay or withdraw; transmission adds MW; Sec.2106/2103/2110/2101/2102/2109/2214 as mechanisms | done (see below) |
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

## Phase 2 changes
- **Grid agents** (`baaja/grid.py`; `simulate(..., grid="agents")`; `grid="exogenous"` is unchanged and still drives
  Sims 1-6, so earlier results reproduce exactly). The permitting, court and halt blocks stay vectorised; the grid
  layer is a monthly loop per region over pre-drawn per-project random numbers, so paired runs still share draws.
  - **Operators** (one per region): cluster studies (serial in MISO, CAISO and the other cluster regions; ERCOT
    studies each request on its own) with study throughput that adapts to arrivals. Cluster size, mode, minimum study
    time and throughput settings fitted per region to LBNL request -> agreement times, 2010-19 cohorts; 2020-24 held
    out. Regions without enough data (SPP, West, ...) use a pooled fit.
  - **Developers**: each request has a value (LBNL's P(complete | cost) relation, scaled per technology and region so
    completion matches LBNL) and an allocated network-upgrade cost that rises with capacity already signed (`kappa`,
    from LBNL cost data) and with re-study after withdrawals. At study results a developer withdraws if cost exceeds
    value; before that a background regional hazard (fitted to the share of 2015-19 requests withdrawn by month 24)
    applies. New requests respond to the published wait and to the region's projected shortfall 4 years ahead.
  - **Transmission**: finished transmission projects add hosting room in their region, so Sec.2101/2102/2214 (via
    transmission timing) and Sec.2109 (extra room per project) reach generator MW.
  - **Bill**: Sec.2106 as structure in RTO/ISO regions only, adopted per RTO with probability `adopt_2106` (2106(d)):
    published locations with a fixed per-MW fee (no cost-allocation shock or re-study for those requests), a single
    decision point with non-refundable security (requests below `q_min_2106` chance of completing do not enter).
    Sec.2110 as a throughput gain (central 0, the bill sets no target). Sec.2109 as hosting room.
- **Calibration** (`calibrate.calibrate_grid`, `run.py --recalibrate-grid`): operators, then alternating passes over
  the regional background hazard and the value scales; writes `grid_cal` and `grid_fit` to `results/calibration.json`.
- **Sim 7** (`baaja/sims/sim7_grid_agents.py`, `results/sim7_grid_agents.md`): current law, BAAJA, BAAJA without
  2106, without 2109, 2106 alone, 2106 adopted by every RTO, BAAJA + 2110 at +25%; exogenous runs alongside; regional
  tables; validation (operator fit and holdout, withdrawal curve, value scales, months to operation, completion by
  cost); one-at-a-time sensitivity over every grid assumption.
- `baaja/uncertainty.py` adds a third joint sample with the grid agents and their assumptions drawn.
- Tests: `tests/test_grid.py` (exogenous mode unchanged, determinism, current law has no bill effect, Sec.2106 leaves
  ERCOT/Southeast/West alone, throughput shortens waits, congestion raises withdrawal, operator fit and holdout,
  calibration tolerances).

PHASE2_RESULTS

## Known issues carried forward
- Grid agents: completed projects take 14-21 months longer from request to operation than LBNL's medians (a longer
  wait does not raise withdrawal, so no selection for short waits); MISO waits (27-35 months) shorter than recent
  cohorts (45-50); ERCOT's early withdrawal twice the data's; SPP and West use pooled operator settings that fit
  poorly. Current-law GW by 2041 is lower with agents than with the exogenous grid.
- Simulation intervals are seed noise at central values; `results/uncertainty.md` has the joint ranges.
- Completion targets treat still-active 2000-20 requests as failures; interconnection times come only from projects
  that signed agreements (Phase 2 calibration with survival methods).
- Sims 1-6 have no feedback from scarcity to entry; only Sim 7's agents do.
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
five simulations, measured federal-land intake. Phases 0-2 (23 Nov): as above.
