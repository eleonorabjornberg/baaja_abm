# Simulation 2: litigation

Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).

## Outcome vs current law (GW)

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 659 [643, 675] | 179 [171, 191] | 217 [210, 225] | 64.4% |
| Court provisions only (Sec.1110/2201) | +0.8 [+0.1, +1.7] | +0.0 [+0.0, +0.2] | +0.0 [+0.0, +0.1] | +0.03 pts |
| All data-based provisions | +9.9 [+7.5, +13.3] | +1.2 [+0.4, +2.2] | +1.3 [+0.7, +1.8] | +0.23 pts |

## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)

| group | challenger | law | courts only | all | challenger win rate (law) |
|---|---|---|---|---|---|
| Renewable (new) | National NGO | 1.8 | 0.5 | 0.7 | 27% |
| Renewable (new) | Local group / residents | 27.7 | 8.1 | 11.8 | 22% |
| Renewable (new) | Tribe | 4.2 | 1.4 | 2.0 | 17% |
| Renewable (new) | State / local government | 1.0 | 0.3 | 0.4 | 26% |
| Renewable (new) | Business | 4.2 | 1.1 | 1.4 | 19% |
| Fossil (gas) | National NGO | 0.4 | 0.1 | 0.1 | 35% |
| Fossil (gas) | Local group / residents | 0.7 | 0.2 | 0.2 | 29% |
| Fossil (gas) | Tribe | 0.2 | 0.1 | 0.1 | 30% |
| Fossil (gas) | State / local government | 0.1 | 0.0 | 0.0 | 44% |
| Fossil (gas) | Business | 0.2 | 0.0 | 0.0 | 18% |
| Storage | National NGO | 0.1 | 0.0 | 0.0 | 44% |
| Storage | Local group / residents | 1.2 | 0.3 | 0.3 | 21% |
| Storage | Tribe | 0.2 | 0.1 | 0.1 | 14% |
| Storage | State / local government | 0.0 | 0.0 | 0.0 | 25% |
| Storage | Business | 0.2 | 0.1 | 0.1 | 8% |

## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)

| technology | suits / yr | vacated | cancelled |
|---|---|---|---|
| Gas | 0.11 -> 0.03 | 0.3 -> 0.0 | 0.7 -> 0.7 |
| Geothermal | 0.12 -> 0.04 | 0.3 -> 0.0 | 0.1 -> 0.0 |
| Offshore wind | 0.82 -> 0.24 | 1.9 -> 0.0 | 2.5 -> 2.2 |
| Onshore wind | 0.49 -> 0.15 | 1.0 -> 0.0 | 0.3 -> 0.1 |
| Solar | 1.15 -> 0.32 | 2.5 -> 0.0 | 1.9 -> 1.4 |
| Storage | 0.12 -> 0.03 | 0.2 -> 0.0 | 0.2 -> 0.2 |
| Transmission | 0.93 -> 0.27 | 4.1 -> 0.0 | 1.4 -> 0.5 |
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
| late_adapt | 0.26 / 1.0 | +0.8 / +0.8 | +0.0 / +0.0 | -45.1 / -30.8 | Sec.1110/2201: share of would-be late filers who file within 150 days instead [D: FHWA/FTA limitation natural experiment, data/limitation_experiment.json; high end = all late highway suits lacked a notice] |
| exhaust_injury | 0.6 / 0.95 | +0.8 / +0.8 | +0.0 / +0.0 | -46.9 / -39.3 | Sec.1110: share of timely suits that pass comment exhaustion + direct injury |
| suit_payoff | 0.4 / 1.0 | +0.8 / +0.8 | +0.0 / +0.0 | -48.4 / -31.1 | Sec.1110: suits filed relative to current law when the only remedy is remand |
| inj_nonNEPA | 0.0 / 0.5 | +0.8 / +0.8 | +0.0 / +0.0 | -42.5 / -42.5 | Sec.1110: share of injunctions that rest on non-NEPA laws (still allowed) |
| lit_months_baaja | 8 / 16.4 | +0.8 / +0.8 | +0.0 / +0.0 | -42.5 / -42.5 | Sec.1110/2201: months in litigation with appeals-court original jurisdiction + expedited review |
| lit_ea (current law) | 0.0025 / 0.01 | +0.8 / +0.8 | +0.0 / +0.1 | -40.6 / -46.5 | P(sued | EA): EA/EIS suit ratio in case data x ~10,000 EAs/yr (CEQ estimate) |
| p_kill_vac (current law) | 0.1 / 0.4 | +0.8 / +0.8 | +0.0 / +0.0 | -42.5 / -42.5 | P(project cancelled | permit vacated) |
| remand_months (current law) | 6 / 18 | +0.7 / +0.8 | +0.0 / +0.0 | -42.5 / -42.5 | delay after vacatur, current law |
