# BAAJA ABM: handoff

Personal research project (not thesis work), aimed at a policy brief or paper: how S.5653, the Bipartisan American
Affordability and Jobs Act of 2026 (BAAJA, introduced 30 Sep 2026, passed by the Senate 19 Nov 2026), would change US electricity supply.

## State (23 Nov 2026)
- Branch `claude/vibrant-carson-9aw3xo` carries all work (v5 from `claude/epic-carson-9rxakw`, plus Phases 0-3 below).
- `README.md` has the current results, data register and assumption register. `docs/bill_question_map.md` maps every
  bill section to the model (modelled / listed / out of scope). `data/SOURCES.md` lists every raw source.
- Run: `pip install -r requirements.txt`, `python -m pytest -q`, `python run.py --all --runs 100`, `python run.py --uncertainty 400`, `python run.py --backcast`.

## Plan (agreed 23 Nov 2026)
Headline result: **net supply and adequacy by region and year**. Architecture: **agents where it matters**: keep
the calibrated permitting and court pipeline; rebuild grid access as interacting agents. Standard: paper.

| Phase | What | Status |
|---|---|---|
| 0 | Re-verify; Sec.2213 compliance range; Sim 5 common baseline; CI; sources register; full bill map | done (see below) |
| 1 | Supply accounting: 9 LBNL regions, EIA-860 fleet and retirements, NERC demand, firm capacity, reserve margins | done (see below) |
| 2 | Grid access as agents: regional grid operators with study throughput and hosting room; developers who enter, stay or withdraw; transmission adds MW; Sec.2106/2103/2110/2101/2102/2109/2214 as mechanisms | done (see below) |
| 3 | Joint uncertainty (Latin hypercube over all ranges), variance decomposition, regional backcast, post-2025 court scenario | done (see below) |
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

**Phase 2 results** (`results/sim7_grid_agents.md`, 100 paired runs). Grid agents, current law: 945 GW new by 2041
(exogenous 1,105). BAAJA +31 GW [+14, +47] (renewables +18, gas +9, storage +2.5); without Sec.2106 +10.5 (matches
the exogenous +9.7); Sec.2106 alone +20 [+3, +36]; every RTO adopting +50; Sec.2109 about +5; a 25% Sec.2110 gain
+17 more. Most of the gain is in MISO. Shortfall below reference margins, current law: 74 GW in 2035 (exogenous 68),
almost all PJM; BAAJA cuts it by 1.5 GW (2.5 if every RTO adopts). Largest ranges: `adopt_2106` (+11 to +50),
`q_min_2106` (+34 to +6), `kappa` (current law 761-1,007 GW). `run.py --uncertainty N` adds a grid-agents sample
whenever `grid_cal` exists.

## Phase 3 changes
- **Regional backcast** (`baaja/validation.py`, `run.py --backcast`, also in `--all`; `results/backcast.md|json`):
  Jan 2010 - Dec 2025 under current law, both grid models, against EIA-860 additions 2018-25 nationally and by region
  and technology (new `additions_by_year` in `data/fleet_targets.json`, nameplate MW), and against LBNL withdrawal
  timing of the same request cohorts (2015-19), plus a 2020-23 holdout. Each backcast request's region is drawn from
  LBNL's requests by region in its own request year (new `requests_by_year` in `data/region_targets.json`;
  `region_by_year=True`; forward runs keep 2021-25 shares).
- **Grid agents refitted in the backcast** (`calibrate.calibrate_grid`), so model and data cohorts are the same
  requests; the Phase 2 fit used 2026-30 model cohorts against 2015-19 data and front-loaded withdrawal (almost all of
  it at study results by 36 months). Withdrawal now has three parts, each fitted by region: a first-year background
  hazard (12-month share), a later background hazard (36-month share), and a hold after an adverse study result
  (exponential, regional mean; 60-month share). 24 months is a check. Value scales still fitted to completion (now of
  2010-19 requests by end-2025). Construction time with agents is LBNL's measured agreement -> operation time instead
  of the exogenous model's fitted build time. P(EIS | federal review) is refitted with the agents on (they keep more
  requests alive to a federal decision). Sec.2106(a)(3) shortens the hold (`lag_2106`, 0-1, central 0.5).
- **Court baseline after *Seven County*** (May 2025): `nepa_win_mult` (challengers' NEPA win, injunction and vacatur
  rates; 0.5-1.0, central 1.0 = 2001-22 data) and `nepa_suit_mult` (suits filed; 0.6-1.0), applied to current law and
  BAAJA alike (BAAJA's remaining injunctions rest on non-NEPA laws and are not scaled). No 2023-26 case data, so an
  assumption range. Sim 2 has a new section; both are in the joint-uncertainty draws.
- Tests: `tests/test_phase3.py` (two-piece clock, region by request year, court baseline, backcast identities, joint
  sample reproducible, joint interval no narrower than seed-only); `tests/test_grid.py` updated for the backcast fit.

**Phase 3 results.**
- Sim 7 with the refitted agents (100 paired runs): current law 910 GW new by 2041 (exogenous 1,105); BAAJA +32 GW
  [+14, +53] (renewables +19, gas +8, storage +3.5); without Sec.2106 +9.8 (exogenous +9.7); Sec.2106 alone +22
  [+3, +41]; every RTO adopting +52; Sec.2109 about +5.5; a 25% Sec.2110 gain +13 more. MISO +12, PJM +7, CAISO +2.
  Shortfall below reference margins, current law: 71 GW in 2035, 137 in 2041 (almost all PJM); BAAJA cuts it by 1.8 GW
  in 2035 and 5.1 in 2041. Ranges: `adopt_2106` +10 to +52, `q_min_2106` +35 to +6, `kappa` current law 743-965 GW.
  `lag_2106` has no effect on GW (+27 at both ends): the hold only delays when a decided withdrawal is recorded.
- Joint uncertainty (400 samples per row): data-sized provisions +9.8 GW [+6.0, +15.2]; with the grid dials
  +34 [+8, +190]; with the grid agents and all their assumptions +31 [+7, +77], 2035 shortfall -1.5 [-7.9, -0.1].
  Largest variance shares: `comply_2213` 46% (data-sized); `ix_2106` 76% (dials); `q_min_2106` 19% and `adopt_2106`
  17% (agents). The court-baseline range explains about 1%.
- Court baseline (Sim 2): with NEPA remedies x0.5-0.7 and suits x0.6-1.0, the court provisions are worth +0.2 to
  +0.5 GW (central +0.9) and all data-sized provisions +9.0 to +9.3 (central +9.7).
- Backcast 2018-25, model / EIA-860: exogenous solar 0.82, wind 1.00, gas 0.84, storage 1.08; agents 0.67, 0.81, 0.80,
  0.42. Regional weighted mean absolute log error 0.42 (exogenous) and 0.51 (agents). Withdrawal timing of 2015-19
  requests fits LBNL by region at 12-36 months (agents); 2020-23 holdout mixed.
- With the agents, current-law suits 2026-41 are 185 (exogenous 119): more requests stay alive to a federal decision.
  BAAJA's cut in suits is therefore larger in agents runs (-137 vs -81 for all data-sized provisions in Sim 2).

## Known issues carried forward
- Grid agents: completed projects take too long from request to operation (a longer wait does not raise withdrawal,
  so no selection for short waits). In the backcast, 2020-22 storage and solar requests take 62-66 months to operate
  (exogenous model 39-60), so the agents build only 0.42 (storage), 0.67 (solar) and 0.81 (wind) of EIA-860's
  2018-25 additions, most of the gap in CAISO and ERCOT; near-term current-law build with agents is conservative.
  In CAISO, ISO-NE, MISO and NYISO the fitted hold after an adverse result reaches its 20-year bound (the data cannot
  tell a long hold from never withdrawing); MISO's 60-month share stays high (0.75 vs 0.62). The 2020-23 withdrawal
  holdout is mixed by region (PJM and CAISO withdraw less early in the data than the model; SPP, West and NYISO more).
  SPP and West use pooled operator settings. ERCOT's LBNL withdrawal shares are probably too low (thin early data).
- Simulation intervals in Sims 1-7 are seed noise at central values; `results/uncertainty.md` has the joint ranges.
- Completion targets treat still-active 2000-20 requests as failures; interconnection times come only from projects
  that signed agreements (Phase 2 calibration with survival methods).
- Sims 1-6 have no feedback from scarcity to entry; only Sim 7's agents do.
- Court parameters from 2001-22 cases; the post-*Seven County* baseline is an assumption range (no 2023-26 case data).
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
