# baaja_abm

Agent-based model of what **S.5653, the Bipartisan American Affordability and Jobs Act of 2026 (BAAJA)** would do to
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

**Current law.** About 1,055 GW of new capacity online by Nov 2041: renewables 659 GW, gas 179 GW, storage 217 GW.
Renewables are 64% of new-build generation.

**Everything in the bill that the data can size** (Simulations 1, 2, 4 together, central values): **+14 GW**
[+11, +17]: renewables +9.9 GW, gas +1.2 GW, storage +1.3 GW. That is about 1.3% more capacity than current law.
The renewable share of new generation rises by +0.2 points.

1. **Permitting (Sim 1)** gives most of that: renewables +7.8 GW [+5.8, +9.8], gas +1.0 GW.
   - The largest single provision is **Sec.2213** (federal-land rights-of-way deadlines): +5.5 GW, all renewable.
     It is also the most uncertain, because current-law right-of-way processing time isn't measured: across 6-18
     months the renewable gain runs +3.4 to +13.0 GW.
   - Median months to a federal permit: **renewables 17 -> 9**, **gas 9.6 -> 9.1**. Months from request to operation
     barely move (renewables 61 -> 61, gas 37 -> 37): interconnection is the binding gate.
   - Gas has more federal exposure than wind or solar (~33% of new gas MW has a federal hook, mostly Army Corps
     individual permits, vs ~5% wind and ~11% solar), but its reviews are short Corps EAs, so deadlines barely bind.
2. **Litigation (Sim 2)**: the court provisions cut suits by about two-thirds (by 28-50 suits over 15 years across
   the assumption ranges), but add only +0.8 GW, because only ~9.5% of energy suits ever win an injunction.
   - How challengers respond to the 150-day limit comes from a natural experiment: highway/transit approvals have had
     a 150-180 day limit since 2005, and those suits bunch just inside it. 27% are filed more than 240 days after the
     decision vs 45% of other NEPA suits, so ~39% of would-be late filers file in time (range 26-100%).
   - Renewables are sued mostly by **local groups and residents** (about 70% of renewable suits). They lose the most
     under the 150-day limit and comment-exhaustion rule (28 -> 9 suits).
   - Vacatur disappears (it is 69% of remands today); cancellations by courts fall modestly.
   - Outside the bill's reach: ~80% of litigated renewable projects in the Sabin database were fought in state courts
     or administrative venues.
3. **Grid access (Sim 3)** dominates everything else, but the bill fixes no size. Sec.2110 only requires a rulemaking
   on computing/AI queue practices; Sec.2106 requires consolidated planning with published interconnection locations
   and fixed costs. Every 5% cut in interconnection study time adds about 35-45 GW by 2041 (renewables ~2/3). At 10%:
   +82 GW total, +53 renewable, +9 gas, +18 storage.
   - The data bracket the effect but can't point to a value. Floor: past queue reforms show no measured shortening
     (MISO's request-to-agreement times rose from ~33 to 45-51 months for 2017-21 requests). Ceiling: ERCOT's pace,
     23 vs 40 months in CAISO/MISO (2015-19 requests), a 42% cut, worth **+427 GW** (renewables +275, gas +46,
     storage +105). Reaching it would also need energy-only interconnection, which the bill does not mandate.
4. **Permit certainty (Sec.1401, Sim 4)**: halted GW falls from ~8 to ~1. That is worth +1.2 GW of renewables in a
   random political future and +2.5 GW if every administration is hostile to renewables; for gas, +0.1-0.2 GW.
   Offshore wind carries most of the risk (anchored on the 2025 stop-work orders).
5. **Decision control (Sim 5)**: about 80% of the gain goes to merchant-owned capacity (EIA-860 ownership by
   technology), split across ISO and non-ISO regions in proportion to where projects are. Transmission sponsorship
   (Sec.2105 no right of first refusal) has no measured link to generator completion and is listed, not simulated.

**Bottom line for renewables vs gas.** The provisions that data can size favour renewables (about 8:1 in GW), mainly
through federal-land rights-of-way and the court changes that hit local opposition. But they are small next to
interconnection. Whether BAAJA is a +14 GW bill or a several-hundred-GW bill depends on what FERC does under
Sec.2106: the data bracket it between no change and ERCOT's pace, but nothing measured picks a point inside.

## Validation
Backcast, current law, Jan 2010 to Dec 2025, with LBNL requests by year (`results/backcast.md`). Cumulative 2018-25
additions, model vs EIA-860: onshore wind 0.92, gas 0.85, solar 0.82, **storage 0.36** (storage completion is
calibrated to the 2000-20 queue cohort, when few batteries finished; recent storage completes more, so storage
GW are underestimated). Calibration fits LBNL completion and time to operation by technology, and CEQ EIS counts
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
| state vs federal venue of renewable opposition | Sabin Center 2026 contested projects and restrictions | `extract_permits_opposition.py` |
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
| `ea_share_nonEIS` | 0.25 | 0.5 | 0.75 | share of non-EIS federal reviews that are EAs (rest CEs); no national EA/CE count |
| `intake_pub` | 6 | 12 | 18 | months from federal-land right-of-way application to start of review, current law |
| `intake_oth` | 1 | 3 | 6 | months from application to start of review, other federal nexus |
| `nonnepa_hydro` | 36 | 48 | 60 | hydro relicensing months outside NEPA |
| `lit_ea` | 0.0025 | 0.005 | 0.01 | P(sued given EA): case-data EA/EIS suit ratio x ~10,000 EAs/yr (CEQ estimate) |
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
| `nonnepa_hydro_baaja` | 30 | 36 | 42 | Sec.1202: hydro months outside NEPA |
| `late_adapt` | 0.26 | 0.39 | 1.0 | Sec.1110/2201: late filers who file within 150 days instead. **From data**: FHWA/FTA limitation natural experiment (`data/limitation_experiment.json`) |
| `exhaust_injury` | 0.6 | 0.8 | 0.95 | Sec.1110: timely suits passing comment exhaustion + direct injury |
| `suit_payoff` | 0.4 | 0.6 | 1.0 | Sec.1110: suits filed when the only remedy is remand, relative to now |
| `inj_nonNEPA` | 0 | 0.3 | 0.5 | Sec.1110: injunctions resting on non-NEPA laws (still allowed) |
| `lit_months_baaja` | 8 | 12 | 16.4 | Sec.1110/2201: months in litigation under appeals-court jurisdiction |
| `halt_mult_1401` | 0 | 0.1 | 0.3 | Sec.1401: residual halt probability |
| `ix_2110`, `ix_2106` | 0, 0 | 0, 0 | 0.05, 0.42 | interconnection study-time cuts. Sec.2106 ceiling **from data**: ERCOT's pace vs CAISO/MISO (`data/interconnection_benchmark.json`); Sim 3 sweeps 0-42% |
| `ix_rule_month` | 24 | 36 | 48 | months until the rules affect studies |

Other assumptions without a range: transmission and hydro-relicensing arrival rates; offshore wind (800 MW) and
geothermal (40 MW) project sizes; EIS litigation rates for offshore wind, hydro and storage; relative court-loss odds
of a truncated review (1.6); halt probabilities other than offshore wind.

## Known limits
- **Onshore wind's federal nexus is a lower bound.** Even if every wind review were an EIS, the model only just
  reproduces CEQ's ~1 wind EIS a year, so the true share with a federal hook is probably higher than 4-7%.
- **No national EA/CE data.** The EA vs CE split and EA litigation rates are ranges.
- **Storage is underestimated** (backcast ratio 0.36).
- **Gas pipelines and LNG are outside the model**, though much fossil NEPA litigation happens there.
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
