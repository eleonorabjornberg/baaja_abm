# Simulation 2: litigation

Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).

## Outcome vs current law (GW)

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 658 [642, 674] | 175 [168, 188] | 287 [279, 298] | 64.8% |
| Court provisions only (Sec.1110/2201) | +0.8 [+0.1, +1.7] | +0.0 [+0.0, +0.2] | +0.2 [+0.0, +0.4] | +0.03 pts |
| All data-based provisions | +8.2 [+6.0, +10.3] | +1.2 [+0.4, +2.0] | +0.4 [+0.0, +0.7] | +0.17 pts |

## Same comparison if 2025's request mix continues (regime "2025")

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 582 [568, 599] | 301 [289, 313] | 229 [221, 237] | 48.9% |
| Court provisions only (Sec.1110/2201) | +0.4 [+0.0, +1.1] | +0.1 [+0.0, +0.2] | +0.1 [+0.0, +0.3] | +0.02 pts |
| All data-based provisions | +5.9 [+4.4, +8.1] | +2.4 [+1.3, +3.6] | +0.2 [+0.0, +0.5] | +0.10 pts |

## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)

| group | challenger | law | courts only | all | challenger win rate (law) |
|---|---|---|---|---|---|
| Renewable (new) | National NGO | 2.3 | 0.6 | 1.0 | 28% |
| Renewable (new) | Local group / residents | 37.9 | 11.0 | 17.0 | 22% |
| Renewable (new) | Tribe | 5.8 | 1.9 | 2.8 | 17% |
| Renewable (new) | State / local government | 1.3 | 0.3 | 0.5 | 30% |
| Renewable (new) | Business | 5.9 | 1.6 | 2.3 | 18% |
| Fossil (gas) | National NGO | 0.4 | 0.1 | 0.1 | 35% |
| Fossil (gas) | Local group / residents | 0.7 | 0.2 | 0.2 | 28% |
| Fossil (gas) | Tribe | 0.2 | 0.1 | 0.1 | 30% |
| Fossil (gas) | State / local government | 0.1 | 0.0 | 0.0 | 44% |
| Fossil (gas) | Business | 0.2 | 0.0 | 0.0 | 19% |
| Storage | National NGO | 2.6 | 0.7 | 0.7 | 30% |
| Storage | Local group / residents | 40.8 | 11.6 | 11.4 | 22% |
| Storage | Tribe | 6.8 | 2.0 | 1.9 | 18% |
| Storage | State / local government | 1.5 | 0.4 | 0.3 | 27% |
| Storage | Business | 6.4 | 1.8 | 1.7 | 17% |

## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)

| technology | suits / yr | vacated | cancelled |
|---|---|---|---|
| Gas | 0.11 -> 0.03 | 0.3 -> 0.0 | 0.6 -> 0.6 |
| Geothermal | 0.20 -> 0.07 | 0.5 -> 0.0 | 0.1 -> 0.0 |
| Offshore wind | 0.78 -> 0.22 | 1.9 -> 0.0 | 1.7 -> 1.4 |
| Onshore wind | 0.64 -> 0.19 | 1.4 -> 0.0 | 0.5 -> 0.3 |
| Solar | 1.92 -> 0.55 | 4.1 -> 0.0 | 2.3 -> 1.6 |
| Storage | 3.87 -> 1.10 | 8.7 -> 0.0 | 2.4 -> 0.6 |
| Transmission | 1.27 -> 0.36 | 5.9 -> 0.0 | 1.9 -> 0.5 |
| Hydro relicense | 0.24 -> 0.08 | 0.8 -> 0.0 | 0.1 -> 0.0 |

## Fossil comparison: gas pipelines and LNG vs renewables (case data, 2012-21; current law)

Pipelines and LNG are not a generation technology in the model, but they carry most fossil NEPA litigation. CEQ counts 2.8 pipeline/LNG EISs a year (median 29 months). The last column applies the central Sec.1110 filters (150-day limit with observed filing delays and adaptation, comment exhaustion + direct injury, remand-only payoff) to each group's challenger mix. FERC certificate cases already face Natural Gas Act deadlines (30-day rehearing, 60-day petition) and appeals-court review, so for those the 150-day limit changes little; the remedy limit (no vacatur) is what binds.

| group | NEPA cases / yr | filed > 150 days | challenger wins | injunction | vacatur of remands | suits kept under BAAJA (central) |
|---|---|---|---|---|---|---|
| Renewables (wind, solar, geothermal) | 4.0 | 57% | 24% | 5% | 100% (n=6) | 29% |
| Gas pipelines and LNG | 10.0 | 53% | 31% | 7% | 70% (n=10) | 29% |
| Transmission | 2.5 | 35% | 42% | 8% | 25% (n=8) | 29% |

## Litigation BAAJA does not reach: Sabin Center contested renewable projects (2026 database)

| type | contested | litigated | federal venue | state / administrative only | cancelled |
|---|---|---|---|---|---|
| Solar | 322 | 76 | 9 | 68 | 130 |
| Storage | 17 | 2 | 0 | 2 | 7 |
| Transmission | 14 | 11 | 3 | 8 | 0 |
| Wind | 215 | 111 | 24 | 87 | 90 |

## Sensitivity (court provisions; other values central)

| assumption | low / high | renewable GW gain | gas GW gain | suits change | what it is |
|---|---|---|---|---|---|
| late_adapt | 0.26 / 1.0 | +0.8 / +0.7 | +0.0 / +0.0 | -101.9 / -69.9 | Sec.1110/2201: share of would-be late filers who file within 150 days instead [D: FHWA/FTA limitation natural experiment, data/limitation_experiment.json; high end = all late highway suits lacked a notice] |
| exhaust_injury | 0.6 / 0.95 | +0.8 / +0.7 | +0.0 / +0.0 | -106.5 / -89.2 | Sec.1110: share of timely suits that pass comment exhaustion + direct injury |
| suit_payoff | 0.4 / 1.0 | +0.8 / +0.8 | +0.0 / +0.0 | -109.0 / -70.2 | Sec.1110: suits filed relative to current law when the only remedy is remand |
| inj_nonNEPA | 0.0 / 0.5 | +0.8 / +0.8 | +0.0 / +0.0 | -96.4 / -96.4 | Sec.1110: share of injunctions that rest on non-NEPA laws (still allowed) |
| lit_months_baaja | 8 / 16.4 | +0.8 / +0.8 | +0.0 / +0.0 | -96.4 / -96.4 | Sec.1110/2201: months in litigation with appeals-court original jurisdiction + expedited review |
| lit_data_mult (current law) | 0.5 / 1.0 | +0.7 / +0.8 | +0.0 / +0.0 | -77.0 / -115.3 | scale on the energy-specific EA/CE suit rates (renewables, transmission) [D: suits / BLM + DOE reviews, 2012-21]; < 1 because other agencies' reviews are missing from the denominator |
| lit_ea (current law) | 0.0025 / 0.01 | +0.8 / +0.8 | +0.0 / +0.1 | -95.7 / -98.0 | P(sued | EA) for gas and hydro: all-sector case data x ~10,000 EAs/yr (CEQ estimate) |
| p_kill_vac (current law) | 0.1 / 0.4 | +0.8 / +0.8 | +0.0 / +0.0 | -96.4 / -96.4 | P(project cancelled | permit vacated) |
| remand_months (current law) | 6 / 18 | +0.7 / +0.8 | +0.0 / +0.0 | -96.4 / -96.4 | delay after vacatur, current law |
