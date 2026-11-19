# Simulation 2: litigation

Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).

## Outcome vs current law (GW)

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 659 [644, 675] | 179 [171, 191] | 219 [212, 227] | 64.4% |
| Court provisions only (Sec.1110/2201) | +0.9 [+0.1, +1.8] | +0.0 [+0.0, +0.2] | +0.1 [+0.0, +0.3] | +0.03 pts |
| All data-based provisions | +8.2 [+5.9, +11.2] | +1.2 [+0.4, +2.2] | +0.3 [+0.0, +0.6] | +0.17 pts |

## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)

| group | challenger | law | courts only | all | challenger win rate (law) |
|---|---|---|---|---|---|
| Renewable (new) | National NGO | 2.3 | 0.7 | 1.0 | 28% |
| Renewable (new) | Local group / residents | 38.2 | 11.2 | 17.2 | 22% |
| Renewable (new) | Tribe | 6.0 | 1.9 | 2.9 | 16% |
| Renewable (new) | State / local government | 1.3 | 0.4 | 0.5 | 30% |
| Renewable (new) | Business | 5.7 | 1.6 | 2.3 | 19% |
| Fossil (gas) | National NGO | 0.4 | 0.1 | 0.1 | 35% |
| Fossil (gas) | Local group / residents | 0.7 | 0.2 | 0.2 | 29% |
| Fossil (gas) | Tribe | 0.2 | 0.1 | 0.1 | 30% |
| Fossil (gas) | State / local government | 0.1 | 0.0 | 0.0 | 44% |
| Fossil (gas) | Business | 0.2 | 0.0 | 0.0 | 18% |
| Storage | National NGO | 2.0 | 0.6 | 0.5 | 29% |
| Storage | Local group / residents | 34.5 | 9.9 | 9.7 | 22% |
| Storage | Tribe | 5.7 | 1.8 | 1.7 | 18% |
| Storage | State / local government | 1.2 | 0.3 | 0.3 | 25% |
| Storage | Business | 5.5 | 1.6 | 1.4 | 17% |

## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)

| technology | suits / yr | vacated | cancelled |
|---|---|---|---|
| Gas | 0.11 -> 0.03 | 0.3 -> 0.0 | 0.7 -> 0.7 |
| Geothermal | 0.18 -> 0.06 | 0.4 -> 0.0 | 0.1 -> 0.0 |
| Offshore wind | 0.89 -> 0.26 | 2.1 -> 0.0 | 2.5 -> 2.2 |
| Onshore wind | 0.49 -> 0.15 | 1.0 -> 0.0 | 0.3 -> 0.1 |
| Solar | 2.00 -> 0.58 | 4.3 -> 0.0 | 2.4 -> 1.6 |
| Storage | 3.26 -> 0.94 | 7.2 -> 0.0 | 1.8 -> 0.4 |
| Transmission | 1.27 -> 0.36 | 5.9 -> 0.0 | 1.9 -> 0.5 |
| Hydro relicense | 0.26 -> 0.09 | 0.8 -> 0.0 | 0.1 -> 0.0 |

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
| late_adapt | 0.26 / 1.0 | +0.9 / +0.9 | +0.0 / +0.0 | -95.2 / -65.3 | Sec.1110/2201: share of would-be late filers who file within 150 days instead [D: FHWA/FTA limitation natural experiment, data/limitation_experiment.json; high end = all late highway suits lacked a notice] |
| exhaust_injury | 0.6 / 0.95 | +0.9 / +0.9 | +0.0 / +0.0 | -99.6 / -83.2 | Sec.1110: share of timely suits that pass comment exhaustion + direct injury |
| suit_payoff | 0.4 / 1.0 | +0.9 / +0.9 | +0.0 / +0.0 | -102.1 / -65.4 | Sec.1110: suits filed relative to current law when the only remedy is remand |
| inj_nonNEPA | 0.0 / 0.5 | +0.9 / +0.9 | +0.0 / +0.0 | -90.0 / -90.0 | Sec.1110: share of injunctions that rest on non-NEPA laws (still allowed) |
| lit_months_baaja | 8 / 16.4 | +0.9 / +0.9 | +0.0 / +0.0 | -90.0 / -90.0 | Sec.1110/2201: months in litigation with appeals-court original jurisdiction + expedited review |
| lit_data_mult (current law) | 0.5 / 1.0 | +0.8 / +0.9 | +0.0 / +0.0 | -73.1 / -107.0 | scale on the energy-specific EA/CE suit rates (renewables, transmission) [D: suits / BLM + DOE reviews, 2012-21]; < 1 because other agencies' reviews are missing from the denominator |
| lit_ea (current law) | 0.0025 / 0.01 | +0.9 / +0.9 | +0.0 / +0.1 | -89.2 / -91.6 | P(sued | EA) for gas and hydro: all-sector case data x ~10,000 EAs/yr (CEQ estimate) |
| p_kill_vac (current law) | 0.1 / 0.4 | +0.9 / +0.9 | +0.0 / +0.0 | -90.0 / -90.0 | P(project cancelled | permit vacated) |
| remand_months (current law) | 6 / 18 | +0.8 / +0.9 | +0.0 / +0.0 | -90.0 / -90.0 | delay after vacatur, current law |
