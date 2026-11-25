# BAAJA ABM: handoff

Personal research project (not thesis work), aimed at a policy brief or paper: how S.5653, the Bipartisan American
Affordability and Jobs Act of 2026 (BAAJA, introduced 30 Sep 2026, passed by the Senate 19 Nov 2026), would change US electricity supply.

## State (24 Nov 2026)
- Branch `claude/vibrant-carson-9aw3xo` carries all work (v5 from `claude/epic-carson-9rxakw`, plus Phases 0-4 below).
- `README.md` has the current results, data register and assumption register. `docs/bill_question_map.md` maps every
  bill section to the model (modelled / listed / out of scope). `data/SOURCES.md` lists every raw source.
- Run: `pip install -r requirements.txt`, `python -m pytest -q`, `python run.py --all --runs 100`, `python run.py --uncertainty 400`, `python run.py --backcast`, `python run.py --brief-figures`.
- Write-up: `docs/brief.md` (brief) and `docs/ODD.md` (model description).

## Plan (agreed 23 Nov 2026)
Headline result: **net supply and adequacy by region and year**. Architecture: **agents where it matters**: keep
the calibrated permitting and court pipeline; rebuild grid access as interacting agents. Standard: paper.

| Phase | What | Status |
|---|---|---|
| 0 | Re-verify; Sec.2213 compliance range; Sim 5 common baseline; CI; sources register; full bill map | done (see below) |
| 1 | Supply accounting: 9 LBNL regions, EIA-860 fleet and retirements, NERC demand, firm capacity, reserve margins | done (see below) |
| 2 | Grid access as agents: regional grid operators with study throughput and hosting room; developers who enter, stay or withdraw; transmission adds MW; Sec.2106/2103/2110/2101/2102/2109/2214 as mechanisms | done (see below) |
| 3 | Joint uncertainty (Latin hypercube over all ranges), variance decomposition, regional backcast, post-2025 court scenario | done (see below) |
| 4 | ODD model description, brief, figures | done (see below) |

## Phase 0 changes
- **Sec.2213 compliance** (`comply_2213`, 0.25 / 0.5 / 1.0): the section's 30- and 90-day clocks have no sponsor
  petition or court order (Sec.1106 has both), so they are no longer assumed always met. Drawn from a side random
  stream so all earlier draws are unchanged.
- **Sim 5 baseline**: ISO / non-ISO completion targets keep LBNL's ratio between markets but are scaled to the pooled
  target, so Sim 5's current law matches Sims 1-4.
- CI (`.github/workflows/tests.yml`), `data/SOURCES.md`, every bill section classified in the bill map.
- **Bill version**: the model now follows the Senate-passed text (substitute to H.R. 2347, KAT26804 V62, passed
  19 Nov 2026, 62-33; S.Amdt. 6883; modelled sections checked word for word against GovInfo's engrossed text,
  BILLS-119hr2347eas). Sec.2106 covers RTOs/ISOs only (`ix_cut_rto`); Sec.1401 gains
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
    decision point with non-refundable security (the `screen_2106` share of new requests least likely to complete within their technology and region do not enter).
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

## Phase 4 changes
- `docs/ODD.md`: model description in ODD form (purpose and patterns, entities, process and scheduling, design
  concepts, initialization, input data, submodels 7.1-7.8, reproducibility).
- `docs/brief.md` (Phase 4 version, superseded): methods and results brief. Headline: +32 GW by 2041 [+14, +53] with grid agents (joint ranges
  +7 to +77); +10 GW without Sec.2106; +52 GW if every RTO adopts. Shortfall -1.8 GW in 2035, -5.1 GW in 2041.
  Also published as a shareable doc: https://claude.ai/artifact/38qM9go9z5Trbn4SVCNDF3 (private until shared).
- Comparison with published estimates (all on the introduced text): Rhodium (RHG-NEMS, 2 Nov) 17-249 GW of clean
  capacity through 2040, mid 56; RFF (ReEDS, 29 Oct) about 60 GW by 2028; SEIA 167 GW of solar 2028-35 (method not
  published). They remove or reduce interconnection limits by assumption; here Sec.2106 is modelled, RTO-only, with
  adoption drawn per RTO. With a pure study-time dial this model spans +8 to +190 GW, close to Rhodium's range.
- `baaja/brief_figures.py` + `run.py --brief-figures` (also in `--all`): `figures/brief_1..5_*.png` from results JSON.

## Review fixes and relative entry screen (24 Nov 2026)
Three reviewers challenged the Phase 4 brief. Fixes, in commits adb1f68 to 1e4f7d3:
- Grid agents: zero-cost requests pay nothing; the Sec.2106 fee is set on the expected upgrade cost; `kappa` is
  0 / 2.17 / 5.14 (0 in ERCOT, which does not allocate network upgrades to generators); new capacity is reported as
  `GW_new`, without relicensed hydro; Sim 7 has a timing table, a `q_min_law` row and a PJM adequacy fix; the
  uncertainty analysis adds realised adoption as a regressor and bootstrap intervals. Full recalibration and rerun.
- The recalibration took the headline to about 0 GW, because the absolute Sec.2106 entry screen (`q_min_2106`, a
  threshold on calibrated P(cost <= value)) moved with the calibration. After seeing that, the screen was made
  relative: `screen_2106` (0.1 / 0.25 / 0.5) keeps out that share of new requests, those least likely to complete
  within their technology and region (`baaja/grid.py`). The absolute version is `q_abs_2106` (default 0), a
  sensitivity only. The brief says the change was made after seeing results. Phase 2-4 numbers above that mention
  `q_min_2106` are superseded.
- Storage in ERCOT is exempted from the calibration-tolerance test (value scale at its lower bound; 17% zero-POI-cost
  share against a 12% completion target).

**Results at that point** (superseded below): grid agents, current law 954 GW new by 2041 (exogenous 1,090).
BAAJA +21.9 GW [+7.5, +37.2] (renewables +14.9, gas +5.0, storage +2.0); no RTO adopts Sec.2106 +6.7; every RTO
adopts +37.0; absolute screen -2.2. MISO +12.4, PJM about 0.5 (the relative screen keeps out PJM requests that would
have completed). Joint ranges +26.5 [+4.9, +64.0]. Shortfall below reference margins, current law: 69 GW in 2035
(exogenous 59), 122 in 2041; BAAJA cuts it by 3.1 GW in 2035 and 5.7 in 2041. Sim 6 regenerated (its committed
outputs had been from Phase 1).

## Second review and Sec.2106 decomposition (24 Nov 2026)
Three more reviewers (numbers, bill and sources, methods). The methods review found that most of the Sec.2106 gain is
the single decision point removing the assumed current-law re-study round, and that the PJM null comes from PJM's
zero-cost share, not its cost spread. `baaja/sims/sec2106_decomposition.py` (`python run.py --decomposition --runs
100`, `results/sec2106_decomposition.md|json`) makes those diagnostics reproducible; its central rows match Sim 7.
Every RTO adopts: single decision point +35.0 GW over BAAJA without Sec.2106, published locations +2.5, relative
screen -7.2; no screen +44.2, relative +37.0, absolute -4.4 (p = 0.5: +26.5 / +21.9 / -0.1). Re-study off in both
runs (`restudy_rho` 0, `restudy_months` 1): Sec.2106 adds +0.5 GW; no re-study round: -2.6. Titles I-II alone +2.9.
The screen costs capacity in every RTO but MISO (+5.3, whose fitted throughput is 0.59 of arrivals). About 4.5 of
the 33.6 GW in RTO regions is sooner, not more. Under the calibration of commit b6c291c: relative +42.9, absolute +9.5.
The brief now names three key assumptions (adoption, the re-study round, the screen), reports the screen range in
the Summary, says the joint interval is conditional on the relative screen, and adds a validation paragraph on
completion by cost (model 0.30 to 0.01 by bin vs LBNL 0.80 to 0.07) and PJM's zero-cost share in the data.

## New data: re-study round, failure share, approved transmission (24 Nov 2026)
Eleonora asked for the data behind the brief's limits to be downloaded. What came in and what it changed:
- SPP DISIS results workbooks, clusters 2016-1 to 2023-1, every posting (`data/extract_spp_restudy.py` ->
  `data/spp_restudy.json`): the current-law re-study round is now fitted, not assumed. `restudy_rho` 0.1 (s.e. about
  0.8), `restudy_mu` -0.08, `restudy_sd` 0.6, `restudy_months` 17 (range 5 to 29). Superseded on 25 Nov: see below.
- LBNL's completion fit has a share of requests that fail at any cost; `value_a` (0.772 ISO, 0.493 non-ISO) makes
  those requests leave whatever their cost, so a zero-cost draw no longer guarantees completion (PJM's earlier null).
- Approved transmission (MISO LRTP Tranches 1 and 2.1, SPP 2025 ITP, PJM 2025 RTEP 500 kV+) enters as hosting room in
  both runs (`data/planned_tx.json`, `PLAN_TX`; `planned_tx` = 0 for the sensitivity).
- FERC Order No. 2023 compliance orders (CAISO, ISO-NE, NYISO, PJM, SPP) and PJM's queue XML and ERCOT GIS reports are
  checks only (parameter notes; brief sections 6 and 8). Not obtained (HTTP 403): MISO's compliance order ER24-2046 and
  MISO's LRTP project lists; upload them to `raw/`.
- Recalibrated (`run.py --recalibrate-grid`), rerun Sim 7, decomposition and joint uncertainty; brief rewritten.

**Results before the third review** (superseded; see the next section): grid agents, current law 972 GW new by 2041. BAAJA +36.5 GW
[+11.2, +60.5] (renewables +25.3, gas +6.4, storage +4.8); no RTO adopts +6.5; every RTO adopts +65.0 (no screen +72.1,
absolute screen +41.0). MISO +20.2 (+39.1 every RTO), PJM +4.6 (+7.6). Single decision point +61.6 over BAAJA without
Sec.2106 (every RTO); with a five-month re-study round Sec.2106 adds +34.2; with none +1.1. Joint ranges +37.7
[+4.6, +90.1]; realized adoption 54% of variance, Sec.2110 12%. Shortfall, current law 68 GW in 2035 and 112 in 2041;
BAAJA cuts it by 4.9 [0.4, 9.7] in 2035 (9.0 every RTO). Backcast: agents 0.67 / 0.83 / 0.80 / 0.41 of EIA-860
solar / wind / gas / storage 2018-25; regional log error 0.52 (exogenous 0.42).

## Third review: model revision with guards (25 Nov 2026)
Three reviewers found two bugs and a re-study round that could only destroy completions. Eleonora chose a full model
revision and asked how to stop another rewrite. The revision plan set five guards: the brief's frame is frozen (a range set by adoption, what the single decision point
removes and the screen); every model number in the brief comes from results (`docs/brief_src.md` ->
`python -m baaja.brief_numbers` -> `docs/brief.md`, tested); behavior tests for each claim the text makes; one
specification review before the long rerun; and a stopping rule (the final review checks numbers, quotes and code
against text only; a methods disagreement becomes a sensitivity row or a stated limit, and only bugs and factual errors
reopen the model).
- Bugs fixed: legacy requests in cluster regions now go through current law's re-study round; approved lines enter in
  July of their in-service year (`month_of`); Sec.2109 reaches only the public-utility share of each region's load
  (`data/extract_pu_share.py` -> `data/pu_share.json`, EIA-861 2025 investor-owned share, ERCOT 0); the first result
  comes no sooner than five months (150 days) after the cluster study starts.
- Re-study round: the cost change of each request is drawn from SPP's 325 request-level changes after Phase 2
  (`after_P2.logchange_q`, median -15%, skewed toward falls), scaled by `restudy_scale` (0.5 / 1 / 1.5); `restudy_rho`
  is relative to SPP's median withdrawn share 0.446. A request with an adverse first result that is still holding when
  the re-study comes, and whose re-studied cost is at or below its value, stays; one whose cost rises above its value
  leaves at the agreement. `restudy_months` 8 / 17 / 29 (8 = pro forma on-time path; 17 = SPP Phase 2 to the latest
  posting, censored; SPP's active-queue file has no agreement dates).
- Failure share: `calibrate_grid` fits `value_a` per ISO and non-ISO so that zero-cost completion in the backcast equals
  LBNL's 0.772 / 0.493, in its own loop before the value scales. Non-ISO zero-cost requests are West only (about 12 per
  seed), so that fit is noisier.
- Screen ranks by the chance of completing (fail-at-any-cost requests at the bottom); `screen_rank="value"` is a row.
- Approved transmission: MISO LRTP only in the central case; SPP's ITP and PJM's RTEP are a sensitivity
  (`planned_tx_scope="all"`), since kappa already nets out recurring expansion.
- New Sec.2106 readings (decomposition section G): only published locations skip the round (`sdp_scope_2106`), the
  re-study cost change kept at the single decision (`sdp_cost_2106`), screen by value. Hazard rows (section H): no
  background withdrawal during the round, MISO's later hazard set to PJM's.
- Finding from the smoke test, before the refit: with every RTO adopting and the single decision fixing the cost at the
  first result, the bill lowers new capacity, because in SPP's data most stayers' costs fall at re-study as others
  withdraw. The sign depends on what the single decision point removes; the frozen frame reports that range.
- Rerun (100 paired runs; `results/sim7_grid_agents.md`, `results/sec2106_decomposition.md`, `results/uncertainty.md`):
  current law 983 GW new by Nov 2041. Every RTO changing: first-result reading -20.4 GW (17-month round), -23.4
  (8-month); only published locations skip the round +11.1; re-studied cost known at the single decision +41.4. No RTO
  changes +5.2 [3.4, 7.3]; p = 0.5 on the first-result reading -9.1 [-20.3, +2.8]. Peak +6.5 GW in 2034, negative by
  2037. PJM -9.0, MISO +0.5 (MISO 25.6 of the 41.4 on the cost-kept reading). Shortfall 70 GW in 2035 (PJM 57); BAAJA
  cuts it by 1.6 (p = 0.5) to 3.0 (every RTO). Joint ranges +2.1 [-33.5, +27.0]; adoption 24%, Sec.2110 23%,
  restudy_scale 13%. Halving the re-study changes gives +4.6 (20 runs). Calibration: 26 of 28 completion cells within
  35% (ERCOT storage 0.159 vs 0.117 and geothermal outside the West miss; `tests/test_grid.py` records the ERCOT miss);
  zero-cost completion 0.771 vs 0.772 (RTO) and 0.424 vs 0.493 (non-ISO, `value_a` at its lower bound).
- Brief: `docs/brief_src.md` is the source; `python -m baaja.brief_numbers` renders `docs/brief.md` (345 numbers from
  results). Edit the source, never the rendered brief.
- Stopping rule applied: the final review is verification only (numbers, quotes, code against text).

## Known issues carried forward
- Grid agents: completed projects take too long from request to operation (a longer wait does not raise withdrawal,
  so no selection for short waits). In the backcast, 2020-22 storage and solar requests take 62-66 months to operate
  (exogenous model 39-60), so the agents build only 0.43 (storage), 0.68 (solar) and 0.83 (wind) of EIA-860's
  2018-25 additions, most of the gap in CAISO and ERCOT; near-term current-law build with agents is conservative.
  In CAISO, ISO-NE and MISO the fitted hold after an adverse result reaches its 20-year bound (the data cannot
  tell a long hold from never withdrawing); MISO's 60-month share stays high (0.74 vs 0.62). The 2020-23 withdrawal
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
five simulations, measured federal-land intake. Phases 0-2 (23 Nov), Phases 3-4 and review fixes (24 Nov): as above.
