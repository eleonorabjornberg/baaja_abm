# baaja_abm

Agent-based model of what the **Bipartisan American Affordability and Jobs Act of 2026 (BAAJA)**, introduced as S.5653 and
passed by the Senate on 19 Nov 2026 as a substitute to H.R. 2347, would do to
US electricity supply through Nov 2041: what gets built (**renewables vs gas**), and whether each region keeps enough
firm capacity to meet peak demand. Personal experiment, not peer reviewed.
Parameters come from data wherever data exist; the rest are listed below as assumptions with ranges, and each
simulation shows how its result moves across those ranges.

**Write-up (Phase 4):** [`docs/brief.md`](docs/brief.md) is the methods and results brief, with figures, limits, a
reproducibility note and a comparison with published estimates (Rhodium, RFF, SEIA). [`docs/ODD.md`](docs/ODD.md) is the
full model description in ODD form (Grimm et al. 2020).

## The seven simulations
Each one maps a research question to bill sections (`docs/bill_question_map.md`), runs paired against current law
(same seeds and political draws), and reports renewable vs gas. Numbers: mean [5th, 95th percentile] over 100 runs.

| # | Simulation | Bill sections | Result file |
|---|---|---|---|
| 1 | Permitting and build-out time | 1105-1109, 1202, 1302, 1402(c), 2102, 2213, 2229 | `results/sim1_permitting.md` |
| 2 | Litigation: how much, by whom, outcome | 1110, 2201 (+ state courts outside the bill) | `results/sim2_litigation.md` |
| 3 | Grid access | 2106, 2110 | `results/sim3_grid.md` |
| 4 | Permit certainty across administrations | 1401, 1402, (1203, 1204 permit terms) | `results/sim4_certainty.md` |
| 5 | Utility vs merchant decision control | 2104-2108 | `results/sim5_decision_control.md` |
| 6 | Supply and resource adequacy by region and year | all of the above | `results/sim6_supply.md` |
| 7 | Grid access as interacting agents (Phase 2) | 2106, 2109, 2110 (+ 2101, 2102, 2214 through transmission) | `results/sim7_grid_agents.md` |

## Results

Numbers updated 24 Nov 2026 for the Senate-passed text (see `docs/bill_question_map.md`) and Phases 0-3 in
`HANDOFF.md`. Intervals in Sims 1-6 are seed noise at central assumption values; `results/uncertainty.md` draws every
assumption range at once (below).

**Current law.** About 1,090 GW of new capacity online by Nov 2041 in the simpler model (972 GW with the grid agents of
Sim 7): renewables 657 GW, gas 178 GW, storage 255 GW (relicensed hydro excluded). Renewables are 64% of new-build generation.

**Everything in the bill that the data can size** (Sims 1, 2, 4 together, central values): **+8.0 GW of new
capacity** [+6.1, +9.6] (+9.7 GW with relicensed hydro): renewables +6.6 GW, gas +1.0 GW, storage +0.3 GW. That is
under 1% more capacity than current law, about 6:1 renewables to gas. Across all assumption ranges at once:
**+8.0 GW [+4.6, +13.1]**. If 2025's request mix continues, renewables +4.5 GW and gas +2.3 GW (about 2:1).

Change from the 20 Nov version (+15 GW, renewables +11.2): Sec.2213's deadlines are no longer assumed always met
(-3.9 GW renewables), and the Senate-passed Sec.1401 protects permits less (-0.4 GW).

1. **Permitting (Sim 1)**: renewables +5.4 GW [+3.9, +7.1], gas +1.0 GW.
   - The largest single provision is still **Sec.2213** (federal-land rights-of-way deadlines), all renewable (+3.9 GW). Its 30- and 90-day clocks have no enforcement (no sponsor petition or court order, unlike Sec.1106),
     so the share of applications where they are met is a range, 25-100% (central 50%), giving +3.5 to +9.6 GW.
     Current-law intake is measured from BLM MLRS filing dates: filing to NEPA notice takes a median 10.5 months
     (n=60; 90% CI 8.3-16.0), with a long tail (a quarter take over two years).
   - Check: 9.6% of resolved BLM solar applications were authorized (MLRS); the model has 8.9% of federal-nexus solar
     projects reaching operation.
   - Median months to a federal permit: **renewables 9.4 -> 7.2**, gas 9.6 -> 9.1. Months from request to operation
     barely move (renewables 61 -> 61, gas 37 -> 37): interconnection is the binding gate.
   - Gas has more federal exposure than wind or solar (~33% of new gas MW has a federal hook, mostly Army Corps
     individual permits, vs ~5% wind and ~11% solar), but its reviews are short Corps EAs, so deadlines barely bind.
2. **Litigation (Sim 2)**: the court provisions cut suits by about 70% (119 -> 35 over 15 years, all technologies), but
   add only +0.9 GW (renewables +0.7), because only ~9.5% of energy suits ever win an injunction.
   - **Courts after *Seven County* (May 2025)**, an assumption range because no case data after 2022 were available:
     if challengers' NEPA remedies fall by 30-50% and suits by 20-40%, the court provisions are worth +0.2 to +0.5 GW
     instead of +0.9, and all data-sized provisions +9.0 to +9.3 GW instead of +9.7 (same seeds; both runs on the same
     court baseline). Current law itself gains only +0.4 to +0.7 GW from the more deferential courts.
   - Suit rates for energy EAs and CEs come from district-court suits per BLM + DOE review, 2012-21.
   - How challengers respond to the 150-day limit comes from a natural experiment: highway/transit approvals have had
     a 150-180 day limit since 2005, and those suits bunch just inside it; ~39% of would-be late filers file in time
     (range 26-100%).
   - Renewables are sued mostly by **local groups and residents** (about 70% of renewable suits). They lose the most
     under the 150-day limit and comment-exhaustion rule.
   - Outside the bill's reach: ~80% of litigated renewable projects in the Sabin database were fought in state courts
     or administrative venues.
3. **Grid access (Sim 3)** still dominates everything else, but the bill fixes no size. In the Senate-passed text
   **Sec.2106 applies only to RTOs/ISOs** ("Transmission Organizations"), so ERCOT (outside FERC's reach), the
   Southeast and most of the West are outside it, and FERC may find existing processes already compliant (2106(d)).
   At a 10% cut in RTO study time: +41 GW total (renewables +27, gas +4, storage +8).
   - The data bracket the effect but can't point to a value. Floor: past queue reforms show no measured shortening.
     Ceiling: ERCOT's pace, a 42% cut, worth **+209 GW** (renewables +135, gas +17, storage +55). Down from +303 GW
     in Phase 0, because ERCOT's own projects no longer count as covered.
4. **Permit certainty (Sec.1401, Sim 4)**: the passed text adds an exception for action "taken pursuant to any
   applicable law or regulation", which could cover stop-work orders like 2025's. With a residual halt risk of 50%
   (range 10-100%), halted GW fall from ~5 to ~3, worth +0.3 GW of renewables in a random political future and
   +0.7 GW if every administration is hostile to renewables.
5. **Decision control (Sim 5)**: about 80% of the gain goes to merchant-owned capacity. With Sec.2106 limited to
   RTOs/ISOs, its gain falls almost entirely in ISO markets. Sim 5's current law is now within ~4% of Sims 1-4
   (gas 173 vs 178 GW, storage 276 vs 285; it was 158 GW of gas before).

**Does the 2025-26 build-out have to continue? (regime comparison)** 2025 requests broke from 2021-25: gas x2.1 and
geothermal x2.2 (firm power for data centers), solar x0.65, storage x0.69, offshore wind x0.10. That mixes data-center
demand with federal policy changes, and the data can't separate them, so every simulation is also run with each
technology at its 2025 request rate.

| | 2021-25 requests (central) | 2025 requests continue |
|---|---|---|
| Current law, GW by 2041: renewables / gas / storage | 657 / 178 / 255 | 583 / 305 / 203 |
| Renewable share of new generation | 64% | 49% |
| BAAJA, data-sized provisions: renewables / gas / storage | +6.6 / +1.0 / +0.3 | +4.5 / +2.3 / +0.2 |
| BAAJA + 10% Sec.2106 cut (FERC RTOs): renewables / gas / storage | +27 / +4 / +8 | +19 / +9 / +6 |

**Bottom line for renewables vs gas.** The provisions the data can size favor renewables (about 6:1 in GW), mainly
through federal-land rights-of-way and the court changes that hit local opposition, but they are small: +8 GW of new
capacity on about 1,090. Sim 7's grid agents put the bill as a whole at +36.5 GW [+11.2, +60.5] by 2041 (about 4:1
renewables to gas) when each RTO adopts Sec.2106 with probability 0.5, between +6.5 GW if none does and +65.0 GW if all
do. Whether BAAJA matters for supply depends on what RTOs and FERC do under Sec.2106: the simpler model's dial brackets
it between no change and ERCOT's pace (+209 GW), and nothing measured picks a point inside. Sim 7 replaces this dial
with an agent-based queue that sizes the bill's actual mechanisms (below).

6. **Supply and adequacy (Sim 6)**. The model's additions are placed in the nine LBNL regions and added to the EIA-860
   fleet less retirements, against NERC's 2025 peak-demand forecast and Reference Margin Levels.
   - **Current law: the national shortfall below planning reserve margins grows from 9 GW (2027) to 59 GW (2035) and
     107 GW (2041).** Almost all of it is **PJM** (53 GW in 2035, below its reference margin from about 2028, because
     PJM's installed-capacity margin rises to 35% as more of its supply is wind, solar and batteries) and later
     **CAISO** (5 GW in 2035). MISO and ISO-NE first fall below their margins in 2027 (median across runs) and stay
     close to them. ERCOT, the West, the Southeast and SPP stay well above their margins.
   - **BAAJA's data-sized provisions cut the 2035 shortfall by 0.5 GW** (0.9 GW in 2041). A 10% Sec.2106 cut takes off
     3.2 GW (8.0 in 2041); ERCOT's pace takes off 14.7 GW (39 in 2041), mostly in PJM, MISO and CAISO.
   - What moves the shortfall most is outside the bill: demand growth (18-121 GW in 2035 across 0.5-1.5x NERC's
     growth) and how far the capacity credit of wind, solar and batteries falls (53-78 GW).
   - Check: with the fleet put on NERC's existing-certain basis for 2026 (a per-region factor, 0.77-1.13), the model's
     margins follow NERC's anticipated margins where NERC counts the same resources; CAISO sits lower because NERC
     counts its Tier 1 batteries and uses a wider California area.
   - Without feedback from scarcity to new requests, surpluses are not self-correcting (ERCOT 66% in 2035) and
     shortfalls are not filled by new entry; Sim 7 adds that feedback.

7. **Grid access as interacting agents (Sim 7)**. Each region's grid operator studies requests in clusters (ERCOT one
   by one) at a throughput fitted to LBNL request -> agreement times (2010-19 cohorts; 2020-24 held out); developers
   enter on the published wait and their region's projected shortfall, and leave at study results when the allocated
   upgrade cost exceeds their value. Sec.2106 is published locations with a fixed fee (set on the expected upgrade
   cost) and a single decision point with non-refundable security, in RTOs that change their process (drawn per RTO,
   2106(d)); Sec.2109 adds hosting room per transmission line; Sec.2110 is a throughput gain the bill does not size
   (central 0). New capacity below excludes relicensed hydro (+1.8 GW in every BAAJA scenario).
   - Current law includes the transmission MISO (LRTP Tranches 1 and 2.1), SPP (2025 ITP) and PJM (2025 RTEP, 500 kV
     and above) have already approved, as hosting room in both runs (`data/planned_tx.json`); a re-study round fitted
     to SPP's cluster postings (`data/spp_restudy.json`: cost change 0.1 per withdrawn share, request-level change
     median -8% with spread 0.6, agreement 17 months after the first result); and LBNL's share of requests that fail
     at any cost (`value_a`: 23% in RTO regions, 51% elsewhere).
   - **BAAJA as a whole: +36.5 GW [+11.2, +60.5] by 2041** (renewables +25.3, gas +6.4, storage +4.8) on a current law
     of 972 GW, against +8.0 GW with the exogenous grid.
   - **If no RTO adopts Sec.2106: +6.5 GW [+4.6, +8.3]; if every RTO adopts: +65.0 GW [+57.7, +71.1].** Sec.2109's
     hosting room adds about +3.8 GW in the central case; a 25% Sec.2110 throughput gain brings it to +57.5 GW. Without
     the approved transmission, current law is 948 GW and the central gain +24.7 GW (against 973 and +29.3 in the same 20 runs).
   - The entry screen in 2106(a)(3) keeps out the quarter of new requests least likely to complete within their
     technology and region (range 10-50%; LBNL's 12-month withdrawal shares of 2015-19 requests have a median of about 0.3
     across RTOs). This relative screen replaced an absolute probability threshold after the results were seen. Every
     RTO adopts: no screen +72.1 GW, relative +65.0, absolute +41.0 (p = 0.5: +41.0 / +36.5 / +23.9; 100 paired runs,
     `results/sec2106_decomposition.md`). Keeping out half the requests gives +15.0 GW; a tenth, +32.6 GW (20 runs).
   - What Sec.2106 does (every RTO adopts, `python run.py --decomposition`): the single decision point adds +61.6 GW
     over BAAJA without Sec.2106, published locations +4.0, the relative screen -7.1. The single decision point is
     worth that much because it removes the current-law re-study round. With costs unchanged by re-study Sec.2106 adds
     +43.1 GW; with a five-month round (Order No. 2023's 150-day restudy deadline) +34.2 GW; with no re-study round
     +1.1 GW. Titles I-II alone (no Sec.2106, no Sec.2109) give +3.0 GW.
   - Timing: the gain is +0.3 GW in 2030 and +19.0 GW in 2035, because the rules apply to studies from month 36.
   - Most of the gain is in **MISO** (+20.2 GW; +39.1 GW if every RTO adopts; 62-64% of the Sec.2106
     increment). With PJM's study throughput relative to arrivals (0.97 against MISO's fitted 0.59), MISO's every-RTO
     gain is +24.7 GW. PJM gains +4.6 GW (+7.6 if every RTO adopts, +15.4 without the screen).
   - **Adequacy**: BAAJA cuts the 2035 national shortfall by 4.9 GW [0.4, 9.7] (5.3 GW in 2041); 9.0 GW if every RTO
     adopts. With agents, the current-law shortfall is **68 GW in 2035** and 112 GW in 2041, mostly PJM (56 GW in 2035).
   - The current-law level is uncertain: the growth of upgrade cost with capacity signed (`kappa`, from LBNL cost
     data) moves current-law GW from 900 to 1,060 (central 973 in these 20 runs) and BAAJA's gain from +25.4 to +35.0 GW (20 runs).
   - Fit: see Validation and `results/backcast.md`. Storage in ERCOT now fits (0.145 vs 0.117 completion); geothermal
     outside the West misses (0.20 vs 0.14); five value scales sit at a bound of their range.

**All assumption ranges at once (`results/uncertainty.md`).** 400 Latin-hypercube samples per row, each paired
(including the post-*Seven County* court range). Data-sized provisions: **+8.0 GW of new capacity [+4.6, +13.1]**
(median, 5th-95th percentile), 2035 shortfall -0.4 GW [-0.9, -0.1]; Sec.2213's compliance range explains about half
of the variance. Drawing the two interconnection dials across their ranges as well: +33.5 GW [+6.5, +188.7], and
Sec.2106's dial explains 76% of the variance. **With the grid agents and all their assumptions drawn: +37.7 GW [+4.6,
+90.1]** (renewables +25.5, gas +6.9, storage +5.7), 2035 shortfall -3.2 GW [-12.0, -0.1]; realized RTO adoption
explains the most (54%), then Sec.2110 throughput (12%); nothing else above 3%. By adoption: +11.2 GW if no RTO
adopts, +38.0 if some do, +67.2 if all do (medians). Current-law shortfall in 2035: 59-68 GW (medians) [21, 132]
across the three samples, driven by demand growth.

## Validation
Backcast, current law, Jan 2010 to Dec 2025, with LBNL requests by year and each request's region drawn from LBNL's
requests by region in its request year (`results/backcast.md`, `python run.py --backcast`). Both grid models are run
on the same requests; EIA-860 additions by region use nameplate capacity (regions sum to the national total within 2%).

| 2018-25 additions, model / EIA-860 | solar | onshore wind | gas | storage |
|---|---|---|---|---|
| Exogenous grid (Sims 1-6) | 0.82 | 1.00 | 0.84 | 1.08 |
| Grid agents (Sim 7) | 0.67 | 0.83 | 0.80 | 0.41 |

- **By region** the error is larger than nationally: weighted mean absolute log ratio across regions 0.42 (exogenous)
  and 0.52 (agents). Both models put too little solar and storage in ERCOT and CAISO and too much in PJM, ISO-NE and
  NYISO, because regions are drawn from where requests were made, not where projects finished; the Southeast's
  gas is about a third of EIA's 16 GW (not yet explained; utility-built plants may be under-counted in the queue data).
- **The agents' storage and solar shortfall** is timing: 2020-22 storage and solar requests take 62-66 months from
  request to operation in the agents (39-60 with the exogenous grid), so many finish after 2025. Most of the gap is
  in CAISO and ERCOT and is the same gap as "completed projects are not selected for short waits" (known limits).
- **Withdrawal timing of 2015-19 requests** (fitted at 12, 36 and 60 months): the agents match LBNL by region within
  0.01 at 12 and 36 months, and within 0.07 at 24 months (not fitted). At 60 months MISO is 0.74 vs 0.62 even with its
  hold at the bound (CAISO, ISO-NE and MISO hold at the 240-month bound). The exogenous model withdraws 0.42-0.73 of requests by month 12 (data 0.09-0.58).
- **Holdout (2020-23 requests, used in no fit)** is mixed: the agents withdraw too fast in CAISO (0.59 vs 0.12 by month
  12) and PJM (0.30 vs 0.13), too slowly in NYISO (0.40 vs 0.72) and the West (0.09 vs 0.33). PJM's own queue file
  confirms LBNL's shift (0.28 of 2015-19 requests withdrawn within 12 months, 0.11 of 2020-23 requests).
- Model year 1 (Nov 2026-Oct 2027) matches EIA-860's 2024-25 average additions by technology (a calibrated window for
  seeded projects already overdue). Request -> agreement times are fitted to LBNL 2010-19 cohorts and checked on 2020-21
  (Sim 7).

## Data register ([D])
| What | Source | Extractor -> file |
|---|---|---|
| arrivals, active queue end-2025, interconnection times, completion, time to COD, built sizes (2022-25 CODs), hybrid storage, ISO vs non-ISO | LBNL Queued Up data file through 2025 (CC BY 4.0) | `extract_lbnl.py`, `extract_engine_inputs.py` |
| federal nexus by technology | EIA-860 2025 plants x BLM Surface Management Agency; federal balancing areas; USACE individual permits (placebo-netted); RUS awards | `extract_federal_nexus.py`, `combine_federal_hooks.py` |
| EIS counts and durations by technology | CEQ EIS Timeline Data 2010-2024 | `extract_ceq_eis.py` |
| challenger mix, win rates, filing delays, injunctions, vacatur, case length | case-level NEPA litigation export (1,821 cases, 2001-22) | `extract_nepa_cases.py` |
| Corps standard-permit processing time | USACE ORM final individual permits | `extract_engine_inputs.py` |
| adaptation to a 150-day limit | FHWA/FTA highway/transit suits (150-180 day limit) vs other NEPA suits, case-level export | `extract_limitation_experiment.py` |
| interconnection bracket for Sec.2106 | LBNL request -> agreement times, ERCOT vs CAISO/MISO | `extract_interconnection_benchmark.py` |
| late-stage completion, planned pipeline | EIA-860M Dec 2021 and Sep 2026 | `extract_eia860m.py` |
| right-of-way intake time (filing -> NEPA notice) | BLM MLRS solar development grants with filing dates (459 cases; 60 clean base cases) | `extract_mlrs_filing.py` |
| BLM solar right-of-way outcomes (check) | BLM MLRS solar development grants (741 cases): 9.6% of resolved applications authorized vs 8.9% model completion for federal-nexus solar | `extract_mlrs.py` |
| wind habitat conservation plans | Dryad doi:10.5061/dryad.59zw3r2kf file list x EIA-860 | `extract_wind_hcp.py` |
| federal actions against wind/solar 2025-26 | Sabin Climate Backtracker | `extract_backtracker.py` |
| state vs federal venue of renewable opposition | Sabin Center 2026 contested projects and restrictions | `extract_permits_opposition.py` |
| BLM energy NEPA actions: review type, durations, suit rates (with the case data) | BLM ePlanning export (2,594 actions) | `extract_blm_eplanning.py` |
| DOE EAs and EISs | DOE NEPA document lists | `extract_permits_opposition.py`, `combine_federal_hooks.py` |
| EIS litigation rates by sector | Bennon & Wilson 2023 (53 ELR 10836); RFF | `params.LIT_EIS` |
| retirement ages, annual additions, ownership | EIA-860 2025 | `extract_engine_inputs.py`, `extract_federal_nexus.py` |
| capacity factors | EIA Electric Power Monthly; NREL ATB (offshore wind) | `params.CF` |
| bill text | GovInfo BILLS-119s5653is; Senate-passed substitute KAT26804 V62 | `docs/bill_question_map.md` |
| regions: request shares, completion by region, time since signed IA, IA -> operation | LBNL Queued Up through 2025 | `extract_regions.py` -> `region_targets.json` |
| grid agents: request -> agreement time by region and cohort (2010-24), withdrawal timing (2015-19 cohorts), completion by type and region, network-upgrade cost and completion by cost (MISO, PJM, SPP, NYISO, ISO-NE, CAISO) | LBNL Queued Up through 2025; LBNL interconnection cost studies | `extract_grid.py` -> `grid_targets.json`; fitted in `calibrate.calibrate_grid` |
| existing fleet, announced retirements, vintages, capacity factors | EIA-860 2025, EIA-860M Sep 2026, EIA-923 2025 | `extract_fleet.py` -> `fleet_targets.json` |
| peak demand, firm transfers, existing-certain capacity, reference margins | NERC 2025 Long-Term Reliability Assessment | `extract_demand.py` -> `demand_targets.json` |
| capacity credit of wind, solar, storage | NERC 2025 LTRA (2026); PJM preliminary ELCC class ratings DY2028-42 (2041) | `supply.ONPEAK_2026`, `ONPEAK_2041_PJM` |
| first-year additions (seeded queue timing) | EIA-860 2024-25 additions | `calibrate.overdue_targets` |

Raw files supplied by you (LBNL, USACE, NEPA cases, Sabin, DOE, RUS) are not committed; the extractors regenerate
the JSON summaries in `data/` from them.

## Assumption register ([A], low / central / high)
| key | low | central | high | what it is |
|---|---|---|---|---|
| `ea_share_nonEIS` | 0.32 | 0.53 | 0.67 | share of non-EIS reviews that are EAs. **From data**: BLM ePlanning (central: actions naming >= 20 MW; low: all energy actions) |
| `intake_pub` | 8.3 | 10.5 | 16.0 | median months from federal-land right-of-way filing to NEPA notice, current law. **From data**: BLM MLRS filing dates (n=60), range = 90% CI of the median; projects draw around it (log-sd 1.39) |
| `intake_oth` | 1 | 3 | 6 | months from application to start of review, other federal nexus |
| `nonnepa_hydro` | 36 | 48 | 60 | hydro relicensing months outside NEPA |
| `lit_ea` | 0.0025 | 0.005 | 0.01 | P(sued given EA) for gas and hydro only: all-sector case data x ~10,000 EAs/yr (CEQ estimate) |
| `lit_data_mult` | 0.5 | 0.75 | 1.0 | scale on the **data-based** EA/CE suit rates for renewables (4.8% / 1.4%) and transmission (8.6% / 0.8%): district-court suits / BLM + DOE reviews 2012-21; < 1 because other agencies' reviews are missing from the denominator |
| `lit_ce` | 0.0001 | 0.0002 | 0.0005 | P(sued given CE) |
| `p_kill_vac` | 0.1 | 0.2 | 0.4 | P(project cancelled given permit vacated) |
| `remand_months` | 6 | 12 | 18 | delay after vacatur, current law |
| `delay_weight` | 0 | 1 | 1 | weight of litigation/halt delay in the sponsor's withdrawal clock |
| `halt_len`, `p_kill_halt`, `halt_mult_other` | 4, 0.1, 0.5 | 8, 0.25, 1 | 12, 0.5, 2 | executive halts (offshore wind's probability is from 2025 data) |
| `deadline_bind` | 0.25 | 0.5 | 1.0 | Sec.1106: share of over-deadline reviews cut to deadline + 4 months |
| `ce_shift` | 0 | 0.1 | 0.25 | Sec.1105/1108: EAs that become CEs |
| `recond_ce` | 0.1 | 0.25 | 0.5 | Sec.2102: transmission EAs that become CEs |
| `geo_ce` | 0.5 | 0.85 | 1.0 | Sec.2229: geothermal reviews that stop being major actions |
| `intake_pub_baaja` | 3 | 4 | 6 | Sec.2213: months to start of review on federal land |
| `comply_2213` | 0.25 | 0.5 | 1.0 | Sec.2213: share of new federal-land applications whose deadlines are met (no enforcement mechanism) |
| `nonnepa_hydro_baaja` | 30 | 36 | 42 | Sec.1202: hydro months outside NEPA |
| `late_adapt` | 0.26 | 0.39 | 1.0 | Sec.1110/2201: late filers who file within 150 days instead. **From data**: FHWA/FTA limitation natural experiment (`data/limitation_experiment.json`) |
| `exhaust_injury` | 0.6 | 0.8 | 0.95 | Sec.1110: timely suits passing comment exhaustion + direct injury |
| `suit_payoff` | 0.4 | 0.6 | 1.0 | Sec.1110: suits filed when the only remedy is remand, relative to now |
| `inj_nonNEPA` | 0 | 0.3 | 0.5 | Sec.1110: injunctions resting on non-NEPA laws (still allowed) |
| `nepa_win_mult` | 0.5 | 1.0 | 1.0 | court baseline after *Seven County* (May 2025): challengers' NEPA win, injunction and vacatur rates relative to 2001-22, in both runs |
| `nepa_suit_mult` | 0.6 | 1.0 | 1.0 | court baseline after *Seven County*: NEPA suits filed relative to 2001-22, in both runs |
| `lit_months_baaja` | 8 | 12 | 16.4 | Sec.1110/2201: months in litigation under appeals-court jurisdiction |
| `halt_mult_1401` | 0.1 | 0.5 | 1.0 | Sec.1401: residual halt probability; the passed text exempts action "pursuant to any applicable law or regulation" |
| `ix_2110`, `ix_2106` | 0, 0 | 0, 0 | 0.05, 0.42 | interconnection study-time cuts; 2110 all providers, 2106 RTO/ISO markets only. Sec.2106 ceiling **from data**: ERCOT's pace vs CAISO/MISO (`data/interconnection_benchmark.json`); Sim 3 sweeps 0-42% |
| `ix_rule_month` | 24 | 36 | 48 | months until the rules affect studies |
| `ret_hazard_old` | 0.01 | 0.03 | 0.06 | Supply: annual retirement probability of coal, gas, oil units past the median retirement age (ages from EIA-860) with no announced date |
| `ret_announced` | 0.6 | 1.0 | 1.0 | Supply: share of announced retirements that happen on schedule (low = delays like the 2025 DOE 202(c) orders) |
| `elcc_decline` | 0 | 0.5 | 1 | Supply: how far wind, solar, storage capacity credit falls by 2041, from NERC 2025 national values (0) to PJM's 2041/42 ratings (1) |
| `demand_growth_mult` | 0.5 | 1.0 | 1.5 | Supply: multiplier on NERC's forecast demand growth |
| `entry_wait_elast` | 0 | 0.3 | 1.0 | Grid agents: elasticity of new requests to the published wait |
| `scarcity_beta` | 0 | 1 | 3 | Grid agents: developer value and entry rise with the region's projected shortfall (4 years ahead) |
| `kappa` | 0 | 2.17 | 5.14 | Grid agents: growth of upgrade cost with capacity signed (0 in ERCOT, which does not allocate network upgrades to generators). **From data**: LBNL cost studies, 2018+ vs 2010-17 requests |
| `restudy_rho`, `restudy_months` | 0, 8 | 0.1, 17 | 0.6, 29 | Grid agents: re-study cost change per withdrawn share above SPP's median; months from first result to agreement in cluster regions. **From data**: SPP DISIS postings, clusters 2016-23, Phase 2 to latest restudy posting (censored; low 8 = Order No. 2023's pro forma 150-day restudy plus 90-day facilities study) |
| `restudy_scale` | 0.5 | 1 | 1.5 | Grid agents: scale on the request-level log cost change at re-study, drawn from SPP's changes between Phase 2 and the latest posting. **From data**: SPP DISIS |
| `tx_hosting_gw` | 0.5 | 1.5 | 3.0 | Grid agents: GW of interconnection room added by one transmission project |
| `adopt_2106` | 0 | 0.5 | 1.0 | Sec.2106(d): chance that an RTO's process changes rather than being found compliant, drawn per RTO |
| `planned_share_2106` | 0.25 | 0.5 | 0.9 | Sec.2106(a)(2): share of requests able to use a published location |
| `screen_2106` | 0.1 | 0.25 | 0.5 | Sec.2106(a)(3): share of new requests that non-refundable security and withdrawal penalties keep out, those least likely to complete within their technology and region |
| `lag_2106` | 0 | 0.5 | 1.0 | Sec.2106(a)(3): how long a developer holds its queue position after an adverse study result, relative to current law (withdrawal penalties shorten it; 0 = leaves at once) |
| `fee_mult_2106` | 0.8 | 1.0 | 1.5 | Sec.2106(a)(2): fixed fee as a multiple of the region's median upgrade cost |
| `g_2110` | 0 | 0 | 0.25 | Sec.2110: study throughput gain (the bill sets no target) |
| `hosting_2109` | 0 | 0.1 | 0.3 | Sec.2109: extra hosting room per transmission project |

Other assumptions without a range: transmission and hydro-relicensing arrival rates; offshore wind (800 MW) and
geothermal (40 MW) project sizes; EIS litigation rates for offshore wind, hydro and storage; relative court-loss odds
of a truncated review (1.6); halt probabilities other than offshore wind.

## Known limits
- **Onshore wind's federal nexus is a lower bound.** With wind habitat conservation plans added (+2.7 points), it is
  7-9%; FWS publishes no list of specific eagle permits, so the true share is somewhat higher.
- **EA/CE data are BLM and DOE only.** Corps, USFS and FWS reviews are missing, so EA/CE suit rates are scaled down by a range.
- **Backcast fit is national, not regional** (Validation): regional additions miss by about 40-50% on average, and the
  grid agents' 2018-25 storage is 0.41 of EIA's.
- **Gas pipelines and LNG are not simulated**; Sim 2 compares their litigation (10 NEPA cases a year vs 4 for renewables) from data.
- **No prices or emissions.** In Sims 1-6 arrivals stay at the 2021-25 average (or 2025's mix); only Sim 7's grid
  agents let new requests respond to waits and regional scarcity. Demand is NERC's forecast, not modeled.
- **Supply is capacity accounting, not dispatch**: firm capacity at on-peak shares against NERC's reference margins; no
  hourly reliability model, no imports beyond NERC's firm transfers.
- **Regions are LBNL's nine**, matched to NERC assessment areas; CAISO and the West differ most from NERC's areas.
- **Transmission MW enter only through Sim 7's grid agents** (hosting room per finished project, an assumption range);
  Sims 1-6 keep the earlier treatment, where transmission provisions change only transmission projects' own timing.
- **Grid agents, fit gaps** (`results/sim7_grid_agents.md`, `results/backcast.md`):
  - completed projects take longer from request to operation than LBNL's medians, because a longer wait does not
    raise withdrawal in the model, so completed projects are not selected for short waits; in the backcast this
    pushes 2020-22 storage and solar past 2025;
  - withdrawal timing is fitted in the backcast with a first-year and a later background hazard and a hold after an
    adverse study result; the hold sits at its 20-year bound in CAISO, ISO-NE and MISO, i.e. those requests
    stay in the queue rather than withdraw, and MISO still withdraws too much by month 60;
  - signing is too fast out of sample: MISO's 2021 cohort is 62% signed by Dec 2025 in the model against 36%, and
    PJM's pooled settings sign 99% of its 2020 cohort against 3%;
  - the re-study round is fitted to SPP alone, with clusters that predate Order No. 2023;
  - SPP and the West have no queue data of their own and use pooled operator settings that fit poorly.
- **`lag_2106` has no effect on GW**: in the grid agents a developer's decision to leave is made at the study result;
  the hold only delays when the withdrawal is recorded. Sec.2106(a)(3)'s penalties act through `screen_2106` alone.
- **Suit counts differ between grid models**: with the agents, more requests stay alive to a federal decision, so
  current-law suits 2026-41 are 185 (exogenous 119) and BAAJA's cut in suits is larger.
- **Courts after *Seven County* (May 2025)** are an assumption range (`nepa_win_mult`, `nepa_suit_mult`): no
  case data after 2022 were available.

## Run
```bash
pip install -r requirements.txt
python run.py --all --runs 100    # calibrate, backcast, seven simulations -> results/, figures/
python run.py --recalibrate-grid --sim 7 --runs 100   # refit the grid agents only, then Sim 7
python run.py --uncertainty 400   # all assumption ranges at once -> results/uncertainty.md
python run.py --backcast          # 2010-25 backcast, both grid models -> results/backcast.md
python run.py --decomposition --runs 100   # where the Sec.2106 gain comes from -> results/sec2106_decomposition.md
python run.py --brief-figures     # figures for docs/brief.md from results/*.json -> figures/brief_*.png
python run.py --sim 3 --runs 50   # one simulation, reusing results/calibration.json
python -m pytest -q
```

## Layout
`baaja/params.py` parameters, data hooks, assumption register · `baaja/model.py` engine · `baaja/calibrate.py` ·
`baaja/experiments.py` paired runs, sweeps · `baaja/validation.py` 2010-25 backcast by region · `baaja/supply.py` fleet, demand, adequacy · `baaja/uncertainty.py`
joint sampling · `baaja/grid.py` grid operators and developers (Phase 2) · `baaja/sims/` the seven simulations · `baaja/plots.py` ·
`baaja/brief_figures.py` figures for the brief · `data/` extractors and JSON targets · `docs/bill_question_map.md` · `docs/ODD.md` ·
`docs/brief.md` · `legacy/` v1 and the original v3.
