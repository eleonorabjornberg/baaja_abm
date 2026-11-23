# baaja_abm

Agent-based model of what the **Bipartisan American Affordability and Jobs Act of 2026 (BAAJA)**, introduced as S.5653 and
passed by the Senate on 19 Nov 2026 as a substitute to H.R. 2347, would do to
US electricity supply through Nov 2041: what gets built (**renewables vs gas**), and whether each region keeps enough
firm capacity to meet peak demand. Personal experiment, not peer reviewed.
Parameters come from data wherever data exist; the rest are listed below as assumptions with ranges, and each
simulation shows how its result moves across those ranges.

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

Numbers updated 23 Nov 2026 for the Senate-passed text (see `docs/bill_question_map.md`) and Phases 0-2 in
`HANDOFF.md`. Intervals in Sims 1-6 are seed noise at central assumption values; `results/uncertainty.md` draws every
assumption range at once (below).

**Current law.** About 1,105 GW of new capacity online by Nov 2041: renewables 657 GW, gas 178 GW, storage 255 GW (plus
retained hydro). Renewables are 64% of new-build generation.

**Everything in the bill that the data can size** (Sims 1, 2, 4 together, central values): **+10 GW** [+8, +12]:
renewables +6.6 GW, gas +1.0 GW, storage +0.3 GW (plus retained hydro). That is under 1% more capacity than current
law, about 6:1 renewables to gas. Across all assumption ranges at once: **+10 GW [+6, +16]**. If 2025's request mix continues, renewables +4.6 GW and gas +2.4 GW (about 2:1).

Change from the 20 Nov version (+15 GW, renewables +11.2): Sec.2213's deadlines are no longer assumed always met
(-3.9 GW renewables), and the Senate-passed Sec.1401 protects permits less (-0.4 GW).

1. **Permitting (Sim 1)**: renewables +5.4 GW [+3.9, +7.1], gas +1.0 GW.
   - The largest single provision is still **Sec.2213** (federal-land rights-of-way deadlines), all renewable (+3.9 GW). Its 30- and 90-day clocks have no enforcement (no sponsor petition or court order, unlike Sec.1106),
     so the share of applications where they are met is a range, 25-100% (central 50%), giving +3.5 to +9.6 GW.
     Current-law intake is measured from BLM MLRS filing dates: filing to NEPA notice takes a median 10.5 months
     (n=60; 90% CI 8.3-16.0), with a long tail (a quarter take over two years).
   - Check: 9.6% of resolved BLM solar applications were authorized (MLRS); the model has 8.9% of federal-nexus solar
     projects reaching operation.
   - Median months to a federal permit: **renewables 9.3 -> 7.2**, gas 9.6 -> 9.1. Months from request to operation
     barely move (renewables 61 -> 61, gas 37 -> 37): interconnection is the binding gate.
   - Gas has more federal exposure than wind or solar (~33% of new gas MW has a federal hook, mostly Army Corps
     individual permits, vs ~5% wind and ~11% solar), but its reviews are short Corps EAs, so deadlines barely bind.
2. **Litigation (Sim 2)**: the court provisions cut suits by about 70% (134 -> 40 over 15 years), but add only
   +0.7 GW, because only ~9.5% of energy suits ever win an injunction.
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

**Bottom line for renewables vs gas.** The provisions the data can size favour renewables (about 5:1 in GW), mainly
through federal-land rights-of-way and the court changes that hit local opposition, but they are small: about +10 GW
on 1,105. Whether BAAJA matters for supply depends on what FERC does under Sec.2106 in RTO/ISO markets: the data
bracket it between no change and ERCOT's pace (+209 GW), and nothing measured picks a point inside. Sim 7 replaces
this dial with an agent-based queue that sizes the bill's actual mechanisms (below).

6. **Supply and adequacy (Sim 6, Phase 1)**. The model's additions are placed in the nine LBNL regions and added to
   the EIA-860 fleet less retirements, against NERC's 2025 peak-demand forecast and reference margin levels.
   - **Current law: the national shortfall below planning reserve margins grows from 8 GW (2027) to 68 GW (2035) and
     129 GW (2041).** Almost all of it is **PJM** (63 GW in 2035, below its reference margin from about 2028, because
     NERC's PJM margin rises to 35% as more of its supply is wind, solar and batteries) and later **CAISO** (5 GW in
     2035). ERCOT, the West, the Southeast and SPP stay well above their margins.
   - **BAAJA's data-sized provisions cut the 2035 shortfall by 0.3 GW** (0.6 GW in 2041). A 10% Sec.2106 cut takes off
     2.1 GW (5.3 in 2041); ERCOT's pace takes off 11.5 GW (28 in 2041), mostly in PJM and CAISO.
   - What moves the shortfall most is outside the bill: demand growth (28-120 GW in 2035 across 0.5-1.5x NERC's
     growth) and how far the capacity credit of wind, solar and batteries falls (51-91 GW).
   - Check: with the fleet put on NERC's existing-certain basis for 2026 (a per-region factor, 0.77-1.13), the model's
     margins follow NERC's anticipated margins where NERC counts the same resources; CAISO sits lower because NERC
     counts its Tier 1 batteries and uses a wider California area.
   - Without feedback from scarcity to new requests (Phase 2), surpluses are not self-correcting (ERCOT 80% in 2035)
     and shortfalls are not filled by new entry, so the shortfall is an upper bound on what current law delivers.

7. **Grid access as interacting agents (Sim 7, Phase 2)**. Each region's grid operator studies requests in clusters
   (ERCOT one by one) at a throughput fitted to LBNL request -> agreement times (2010-19 cohorts; 2020-24 held out);
   developers enter on the published wait and their region's projected shortfall, and leave at study results when the
   allocated upgrade cost exceeds their value. Sec.2106 is published locations with a fixed fee and a single decision
   point with non-refundable security, in RTOs that change their process (drawn per RTO, 2106(d)); Sec.2109 adds
   hosting room per transmission line; Sec.2110 is a throughput gain the bill does not size (central 0).
   - **BAAJA as a whole: +31 GW [+14, +47] by 2041** (renewables +18, gas +9, storage +2.5), against +10 GW with the
     exogenous grid. About 2:1 renewables to gas, because Sec.2106 helps gas far more than the permitting provisions
     do (gas is +8 of Sec.2106's +20 GW; the mechanism behind that is not yet broken down).
   - **Sec.2106 alone: +20 GW [+3, +36]**; if every RTO changes its process, BAAJA gives +50 GW [+43, +55]. Whether
     RTOs adopt (`adopt_2106`) moves the result from +11 to +50 GW, the largest single range. Read structurally,
     Sec.2106 is worth far less than the ERCOT-pace ceiling of Sim 3 (+209 GW): fewer speculative requests enter
     (MISO -15%), waits fall by 1-2.5 months and the signed share rises 1.5-3 points, which is not a 42% cut in study time.
   - Sec.2109's hosting room adds about +5 GW; a 25% Sec.2110 throughput gain would add another +17 GW.
   - Most of the gain is in **MISO** (+12 GW; +22 GW if every RTO adopts), then PJM (+5) and SPP (+3).
   - **Adequacy**: BAAJA cuts the 2035 national shortfall by 1.5 GW [0.1, 3.1] (3.8 GW in 2041); 2.5 GW if every RTO
     adopts. ADEQUACY_LEVELS
   - The current-law level is uncertain: the growth of upgrade cost with capacity signed (`kappa`, from LBNL cost data)
     moves current-law GW from 761 to 1,007; strict entry rules under 2106(a)(3) (`q_min_2106` 0.5) would cut the gain
     to +6 GW, because they also keep out requests that would have finished.
   - Fit: request -> agreement times by cohort fit MISO, CAISO and ERCOT well, including the 2020-21 holdouts (MISO
     45 vs 51 and 45 vs 48 months; ERCOT within 2 months every year); regions without their own data fit poorly.
     Withdrawal by month 24 matches LBNL in 8 of 9 regions, but the model front-loads withdrawal (see known limits).

**All assumption ranges at once (`results/uncertainty.md`).** 400 Latin-hypercube samples, each paired. Data-sized
provisions: **+10 GW [+6, +16]**, 2035 shortfall -0.3 GW [-0.7, -0.0]. Sec.2213's compliance range explains about half of
the variance in GW. Drawing the two interconnection dials across their ranges as well: +35 GW [+8, +188], and
Sec.2106's dial explains 81% of the variance. Current-law shortfall in 2035: 66 GW [26, 124].

## Validation
Backcast, current law, Jan 2010 to Dec 2025, with LBNL requests by year (`results/backcast.md`). Cumulative 2018-25
additions, model vs EIA-860: onshore wind 1.02, **storage 1.14** (was 0.54), gas 0.84, solar 0.80. Two Phase 1 changes
fixed storage: the seeded queue's projects with signed agreements now finish on the measured agreement-to-operation time
(29 months for batteries, LBNL 2022-25) rather than a fitted 62 months, and storage completion is LBNL's own (9.1%).
Model year 1 (Nov 2026-Oct 2027) matches EIA-860's 2024-25 average additions by technology (a calibrated window for
seeded projects already overdue). Regional withdrawal hazards fit LBNL completion by region (`results/calibration.json`).

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
| BLM solar right-of-way outcomes (check) | BLM MLRS solar development grants (741 cases): 9.6% of resolved applications authorized vs 8.7% model completion for federal-nexus solar | `extract_mlrs.py` |
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
| `kappa` | 1.56 | 2.17 | 5.14 | Grid agents: growth of upgrade cost with capacity signed. **From data**: LBNL cost studies, 2018+ vs 2010-17 requests |
| `restudy_rho`, `restudy_months` | 0.1, 3 | 0.3, 6 | 0.6, 12 | Grid agents: re-study cost rise after withdrawals; months from first result to agreement in cluster regions |
| `tx_hosting_gw` | 0.5 | 1.5 | 3.0 | Grid agents: GW of interconnection room added by one transmission project |
| `adopt_2106` | 0 | 0.5 | 1.0 | Sec.2106(d): chance that an RTO's process changes rather than being found compliant, drawn per RTO |
| `planned_share_2106` | 0.25 | 0.5 | 0.9 | Sec.2106(a)(2): share of requests able to use a published location |
| `q_min_2106` | 0.1 | 0.25 | 0.5 | Sec.2106(a)(3): lowest chance of completing at which a request still enters, given non-refundable security |
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
- **Storage backcast runs high** (1.14 of EIA-860 2018-25 additions, after Phase 1 fixed the earlier 0.54).
- **Gas pipelines and LNG are not simulated**; Sim 2 compares their litigation (10 NEPA cases a year vs 4 for renewables) from data.
- **No prices or emissions.** In Sims 1-6 arrivals stay at the 2021-25 average (or 2025's mix); only Sim 7's grid
  agents let new requests respond to waits and regional scarcity. Demand is NERC's forecast, not modelled.
- **Supply is capacity accounting, not dispatch**: firm capacity at on-peak shares against NERC's reference margins; no
  hourly reliability model, no imports beyond NERC's firm transfers.
- **Regions are LBNL's nine**, matched to NERC assessment areas; CAISO and the West differ most from NERC's areas.
- **Transmission MW enter only through Sim 7's grid agents** (hosting room per finished project, an assumption range);
  Sims 1-6 keep the earlier treatment, where transmission provisions change only transmission projects' own timing.
- **Grid agents, fit gaps** (`results/sim7_grid_agents.md`, validation section):
  - completed projects take longer from request to operation than LBNL's medians (about 14-21 months), because a
    longer wait does not raise withdrawal in the model, so completed projects are not selected for short waits;
  - MISO's modelled wait to agreement (about 27-35 months) is shorter than recent cohorts (45-50);
  - ERCOT withdraws twice as fast in the first two years as the data (0.34 vs 0.17 by month 24), from study results
    rather than the background hazard, which sits at its floor;
  - SPP and the West have no queue data of their own and use pooled operator settings that fit poorly.

## Run
```bash
pip install -r requirements.txt
python run.py --all --runs 100    # calibrate, backcast, seven simulations -> results/, figures/
python run.py --recalibrate-grid --sim 7 --runs 100   # refit the grid agents only, then Sim 7
python run.py --uncertainty 400   # all assumption ranges at once -> results/uncertainty.md
python run.py --sim 3 --runs 50   # one simulation, reusing results/calibration.json
python -m pytest -q
```

## Layout
`baaja/params.py` parameters, data hooks, assumption register · `baaja/model.py` engine · `baaja/calibrate.py` ·
`baaja/experiments.py` paired runs, sweeps, backcast · `baaja/supply.py` fleet, demand, adequacy · `baaja/uncertainty.py`
joint sampling · `baaja/grid.py` grid operators and developers (Phase 2) · `baaja/sims/` the seven simulations · `baaja/plots.py` ·
`data/` extractors and JSON targets · `docs/bill_question_map.md` · `legacy/` v1 and the original v3.
