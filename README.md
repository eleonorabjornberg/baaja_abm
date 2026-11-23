# baaja_abm

Agent-based model of what the **Bipartisan American Affordability and Jobs Act of 2026 (BAAJA)**, introduced as S.5653 and
passed by the Senate on 19 Nov 2026 as a substitute to H.R. 2347, would do to
the US electricity build-out, **renewables vs gas**, through Nov 2041. Personal experiment, not peer reviewed.
Parameters come from data wherever data exist; the rest are listed below as assumptions with ranges, and each
simulation shows how its result moves across those ranges.

## The five simulations
Each one maps a research question to bill sections (`docs/bill_question_map.md`), runs paired against current law
(same seeds and political draws), and reports renewable vs gas. Numbers: mean [5th, 95th percentile] over 100 runs.

| # | Simulation | Bill sections | Result file |
|---|---|---|---|
| 1 | Permitting and build-out time | 1105-1109, 1202, 1302, 1402(c), 2102, 2213, 2229 | `results/sim1_permitting.md` |
| 2 | Litigation: how much, by whom, outcome | 1110, 2201 (+ state courts outside the bill) | `results/sim2_litigation.md` |
| 3 | Grid access | 2106, 2110 | `results/sim3_grid.md` |
| 4 | Permit certainty across administrations | 1401, 1402, (1203, 1204 permit terms) | `results/sim4_certainty.md` |
| 5 | Utility vs merchant decision control | 2104-2108 | `results/sim5_decision_control.md` |

## Results

Numbers updated 23 Nov 2026 for the Senate-passed text (see `docs/bill_question_map.md`) and the Phase 0 fixes in
`HANDOFF.md`. Intervals are still seed noise at central assumption values; joint parameter uncertainty comes in Phase 3.

**Current law.** About 1,135 GW of new capacity online by Nov 2041: renewables 657 GW, gas 178 GW, storage 285 GW (plus
retained hydro). Renewables are 64% of new-build generation.

**Everything in the bill that the data can size** (Sims 1, 2, 4 together, central values): **+10 GW** [+8, +12]:
renewables +6.7 GW, gas +1.2 GW, storage +0.4 GW (plus retained hydro). That is under 1% more capacity than current
law, about 5.6:1 renewables to gas. If 2025's request mix continues, renewables +4.6 GW and gas +2.4 GW (about 2:1).

Change from the 20 Nov version (+15 GW, renewables +11.2): Sec.2213's deadlines are no longer assumed always met
(-3.9 GW renewables), and the Senate-passed Sec.1401 protects permits less (-0.4 GW).

1. **Permitting (Sim 1)**: renewables +5.6 GW [+3.9, +7.4], gas +1.1 GW.
   - The largest single provision is still **Sec.2213** (federal-land rights-of-way deadlines): **+4.0 GW**, all
     renewable. Its 30- and 90-day clocks have no enforcement (no sponsor petition or court order, unlike Sec.1106),
     so the share of applications where they are met is a range, 25-100% (central 50%), giving +3.5 to +9.6 GW.
     Current-law intake is measured from BLM MLRS filing dates: filing to NEPA notice takes a median 10.5 months
     (n=60; 90% CI 8.3-16.0), with a long tail (a quarter take over two years).
   - Check: 9.6% of resolved BLM solar applications were authorized (MLRS); the model has 8.7% of federal-nexus solar
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
   **Sec.2106 applies only to RTOs/ISOs** ("Transmission Organizations"), so the Southeast and most of the West are
   outside it, and FERC may find existing processes already compliant (2106(d)). Every 5% cut in ISO-market study
   time adds about 25 GW by 2041 at small cuts, rising to about 45 GW per 5% near the ceiling. At 10%: +59 GW total, +34 renewable, +5 gas, +18 storage.
   - The data bracket the effect but can't point to a value. Floor: past queue reforms show no measured shortening.
     Ceiling: ERCOT's pace, a 42% cut, worth **+303 GW** (renewables +173, gas +23, storage +106).
   - ERCOT is counted as an ISO market here although FERC's rules do not reach it, so these GW are somewhat
     overstated until the regional version (Phase 1) separates it.
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
| Current law, GW by 2041: renewables / gas / storage | 657 / 178 / 285 | 582 / 306 / 227 |
| Renewable share of new generation | 64% | 49% |
| BAAJA, data-sized provisions: renewables / gas / storage | +6.7 / +1.2 / +0.4 | +4.6 / +2.4 / +0.2 |
| BAAJA + 10% Sec.2106 cut (ISO markets): renewables / gas / storage | +34 / +5 / +18 | +24 / +11 / +12 |

**Bottom line for renewables vs gas.** The provisions the data can size favour renewables (about 5:1 in GW), mainly
through federal-land rights-of-way and the court changes that hit local opposition, but they are small: about +10 GW
on 1,135. Whether BAAJA matters for supply depends on what FERC does under Sec.2106 in RTO/ISO markets: the data
bracket it between no change and ERCOT's pace (+303 GW), and nothing measured picks a point inside. Phase 2 replaces
this dial with an agent-based queue so the bill's actual mechanisms (fixed fees, single decision point, withdrawal
penalties) can be sized.

## Validation
Backcast, current law, Jan 2010 to Dec 2025, with LBNL requests by year (`results/backcast.md`). Cumulative 2018-25
additions, model vs EIA-860: onshore wind 1.02, gas 0.83, solar 0.80, **storage 0.54**. Storage completion is set from
EIA-860M (storage planned in Dec 2021 completes 1.07x as often as solar by Sep 2026) rather than LBNL's 2000-20
cohort; the remaining gap is likely batteries added at existing plants outside the queue, so storage GW are still
low. Calibration fits LBNL completion and time to operation by technology, and CEQ EIS counts
(`results/calibration.json`).

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
| bill text | GovInfo BILLS-119s5653is | `docs/bill_question_map.md` |

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

Other assumptions without a range: transmission and hydro-relicensing arrival rates; offshore wind (800 MW) and
geothermal (40 MW) project sizes; EIS litigation rates for offshore wind, hydro and storage; relative court-loss odds
of a truncated review (1.6); halt probabilities other than offshore wind.

## Known limits
- **Onshore wind's federal nexus is a lower bound.** With wind habitat conservation plans added (+2.7 points), it is
  7-9%; FWS publishes no list of specific eagle permits, so the true share is somewhat higher.
- **EA/CE data are BLM and DOE only.** Corps, USFS and FWS reviews are missing, so EA/CE suit rates are scaled down by a range.
- **Storage is underestimated** (backcast ratio 0.54; storage completion is now set from EIA-860M late-stage data).
- **Gas pipelines and LNG are not simulated**; Sim 2 compares their litigation (10 NEPA cases a year vs 4 for renewables) from data.
- **No prices, demand or emissions feedback**; arrivals stay at the 2021-25 average (gas requests are rising fast).
- **Transmission has no MW in the model**, so transmission provisions affect only transmission projects' own timing.

## Run
```bash
pip install -r requirements.txt
python run.py --all --runs 100    # ~10 min: calibrate, backcast, five simulations -> results/, figures/
python run.py --sim 3 --runs 50   # one simulation, reusing results/calibration.json
python -m pytest -q
```

## Layout
`baaja/params.py` parameters, data hooks, assumption register · `baaja/model.py` engine · `baaja/calibrate.py` ·
`baaja/experiments.py` paired runs, sweeps, backcast · `baaja/sims/` the five simulations · `baaja/plots.py` ·
`data/` extractors and JSON targets · `docs/bill_question_map.md` · `legacy/` v1 and the original v3.
