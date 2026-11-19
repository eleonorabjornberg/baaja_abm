# Simulation 2: litigation

Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).

## Outcome vs current law (GW)

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 658 [643, 673] | 175 [168, 188] | 218 [212, 226] | 64.8% |
| Court provisions only (Sec.1110/2201) | +0.7 [+0.1, +1.8] | +0.0 [+0.0, +0.2] | +0.1 [+0.0, +0.3] | +0.03 pts |
| All data-based provisions | +7.7 [+5.6, +9.7] | +1.2 [+0.4, +2.0] | +0.3 [+0.0, +0.6] | +0.15 pts |

## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)

| group | challenger | law | courts only | all | challenger win rate (law) |
|---|---|---|---|---|---|
| Renewable (new) | National NGO | 2.2 | 0.6 | 1.0 | 26% |
| Renewable (new) | Local group / residents | 36.8 | 10.8 | 16.4 | 22% |
| Renewable (new) | Tribe | 5.7 | 1.9 | 2.8 | 16% |
| Renewable (new) | State / local government | 1.3 | 0.4 | 0.5 | 30% |
| Renewable (new) | Business | 5.5 | 1.5 | 2.1 | 18% |
| Fossil (gas) | National NGO | 0.4 | 0.1 | 0.1 | 35% |
| Fossil (gas) | Local group / residents | 0.7 | 0.2 | 0.2 | 28% |
| Fossil (gas) | Tribe | 0.2 | 0.1 | 0.1 | 30% |
| Fossil (gas) | State / local government | 0.1 | 0.0 | 0.0 | 44% |
| Fossil (gas) | Business | 0.2 | 0.0 | 0.0 | 19% |
| Storage | National NGO | 2.0 | 0.6 | 0.5 | 29% |
| Storage | Local group / residents | 34.4 | 9.9 | 9.7 | 22% |
| Storage | Tribe | 5.7 | 1.8 | 1.7 | 18% |
| Storage | State / local government | 1.2 | 0.3 | 0.3 | 25% |
| Storage | Business | 5.5 | 1.6 | 1.4 | 17% |

## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)

| technology | suits / yr | vacated | cancelled |
|---|---|---|---|
| Gas | 0.11 -> 0.03 | 0.3 -> 0.0 | 0.6 -> 0.6 |
| Geothermal | 0.20 -> 0.07 | 0.5 -> 0.0 | 0.1 -> 0.0 |
| Offshore wind | 0.78 -> 0.22 | 1.9 -> 0.0 | 1.7 -> 1.4 |
| Onshore wind | 0.53 -> 0.16 | 1.1 -> 0.0 | 0.3 -> 0.1 |
| Solar | 1.92 -> 0.55 | 4.1 -> 0.0 | 2.3 -> 1.6 |
| Storage | 3.26 -> 0.94 | 7.2 -> 0.0 | 1.8 -> 0.4 |
| Transmission | 1.27 -> 0.36 | 5.9 -> 0.0 | 1.9 -> 0.5 |
| Hydro relicense | 0.24 -> 0.08 | 0.8 -> 0.0 | 0.1 -> 0.0 |

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
| late_adapt | 0.26 / 1.0 | +0.7 / +0.7 | +0.0 / +0.0 | -93.5 / -64.1 | Sec.1110/2201: share of would-be late filers who file within 150 days instead [D: FHWA/FTA limitation natural experiment, data/limitation_experiment.json; high end = all late highway suits lacked a notice] |
| exhaust_injury | 0.6 / 0.95 | +0.7 / +0.7 | +0.0 / +0.0 | -97.9 / -81.8 | Sec.1110: share of timely suits that pass comment exhaustion + direct injury |
| suit_payoff | 0.4 / 1.0 | +0.7 / +0.7 | +0.0 / +0.0 | -100.3 / -64.4 | Sec.1110: suits filed relative to current law when the only remedy is remand |
| inj_nonNEPA | 0.0 / 0.5 | +0.8 / +0.7 | +0.0 / +0.0 | -88.4 / -88.4 | Sec.1110: share of injunctions that rest on non-NEPA laws (still allowed) |
| lit_months_baaja | 8 / 16.4 | +0.7 / +0.7 | +0.0 / +0.0 | -88.4 / -88.4 | Sec.1110/2201: months in litigation with appeals-court original jurisdiction + expedited review |
| lit_data_mult (current law) | 0.5 / 1.0 | +0.7 / +0.8 | +0.0 / +0.0 | -71.8 / -105.1 | scale on the energy-specific EA/CE suit rates (renewables, transmission) [D: suits / BLM + DOE reviews, 2012-21]; < 1 because other agencies' reviews are missing from the denominator |
| lit_ea (current law) | 0.0025 / 0.01 | +0.7 / +0.7 | +0.0 / +0.1 | -87.7 / -90.0 | P(sued | EA) for gas and hydro: all-sector case data x ~10,000 EAs/yr (CEQ estimate) |
| p_kill_vac (current law) | 0.1 / 0.4 | +0.7 / +0.8 | +0.0 / +0.0 | -88.4 / -88.4 | P(project cancelled | permit vacated) |
| remand_months (current law) | 6 / 18 | +0.6 / +0.8 | +0.0 / +0.0 | -88.4 / -88.4 | delay after vacatur, current law |
