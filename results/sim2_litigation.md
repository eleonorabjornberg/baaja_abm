# Simulation 2: litigation

Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).

## Outcome vs current law (GW)

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 657 [643, 674] | 178 [169, 187] | 255 [246, 264] | 64.4% |
| Court provisions only (Sec.1110/2201) | +0.7 [+0.1, +1.8] | +0.0 [+0.0, +0.2] | +0.2 [+0.0, +0.4] | +0.03 pts |
| All data-based provisions | +6.6 [+4.7, +8.2] | +1.0 [+0.4, +1.6] | +0.3 [+0.1, +0.6] | +0.13 pts |

## Same comparison if 2025's request mix continues (regime "2025")

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 583 [566, 600] | 305 [294, 319] | 203 [195, 211] | 48.7% |
| Court provisions only (Sec.1110/2201) | +0.4 [+0.0, +1.0] | +0.1 [+0.0, +0.2] | +0.1 [+0.0, +0.3] | +0.02 pts |
| All data-based provisions | +4.5 [+3.2, +5.8] | +2.3 [+1.1, +3.8] | +0.2 [+0.0, +0.5] | +0.05 pts |

## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)

| group | challenger | law | courts only | all | challenger win rate (law) |
|---|---|---|---|---|---|
| Renewable (new) | National NGO | 2.2 | 0.8 | 0.9 | 34% |
| Renewable (new) | Local group / residents | 36.9 | 11.0 | 13.6 | 23% |
| Renewable (new) | Tribe | 6.0 | 1.7 | 2.1 | 19% |
| Renewable (new) | State / local government | 1.2 | 0.3 | 0.4 | 29% |
| Renewable (new) | Business | 6.0 | 1.4 | 1.9 | 16% |
| Fossil (gas) | National NGO | 0.4 | 0.1 | 0.1 | 52% |
| Fossil (gas) | Local group / residents | 0.5 | 0.1 | 0.1 | 29% |
| Fossil (gas) | Tribe | 0.2 | 0.1 | 0.1 | 31% |
| Fossil (gas) | State / local government | 0.1 | 0.0 | 0.0 | 60% |
| Fossil (gas) | Business | 0.3 | 0.1 | 0.1 | 13% |
| Storage | National NGO | 1.9 | 0.5 | 0.5 | 24% |
| Storage | Local group / residents | 29.7 | 9.0 | 8.7 | 22% |
| Storage | Tribe | 4.2 | 1.4 | 1.4 | 16% |
| Storage | State / local government | 1.2 | 0.3 | 0.3 | 26% |
| Storage | Business | 4.8 | 1.3 | 1.3 | 16% |

## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)

| technology | suits / yr | vacated | cancelled |
|---|---|---|---|
| Gas | 0.10 -> 0.03 | 0.4 -> 0.0 | 0.5 -> 0.4 |
| Geothermal | 0.21 -> 0.06 | 0.5 -> 0.0 | 0.1 -> 0.0 |
| Offshore wind | 0.67 -> 0.20 | 1.4 -> 0.0 | 1.4 -> 1.2 |
| Onshore wind | 0.62 -> 0.16 | 1.3 -> 0.0 | 0.7 -> 0.4 |
| Solar | 1.99 -> 0.59 | 4.7 -> 0.0 | 2.8 -> 1.8 |
| Storage | 2.79 -> 0.83 | 6.2 -> 0.0 | 1.6 -> 0.4 |
| Transmission | 1.27 -> 0.39 | 5.9 -> 0.0 | 1.7 -> 0.6 |
| Hydro relicense | 0.30 -> 0.08 | 1.0 -> 0.0 | 0.2 -> 0.0 |

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
| late_adapt | 0.26 / 1.0 | +0.7 / +0.7 | +0.0 / +0.0 | -88.5 / -61.4 | Sec.1110/2201: share of would-be late filers who file within 150 days instead [D: FHWA/FTA limitation natural experiment, data/limitation_experiment.json; high end = all late highway suits lacked a notice] |
| exhaust_injury | 0.6 / 0.95 | +0.7 / +0.7 | +0.0 / +0.0 | -93.0 / -77.7 | Sec.1110: share of timely suits that pass comment exhaustion + direct injury |
| suit_payoff | 0.4 / 1.0 | +0.7 / +0.7 | +0.0 / +0.0 | -95.6 / -59.7 | Sec.1110: suits filed relative to current law when the only remedy is remand |
| inj_nonNEPA | 0.0 / 0.5 | +0.7 / +0.7 | +0.0 / +0.0 | -84.0 / -84.0 | Sec.1110: share of injunctions that rest on non-NEPA laws (still allowed) |
| lit_months_baaja | 8 / 16.4 | +0.7 / +0.7 | +0.0 / +0.0 | -84.0 / -84.0 | Sec.1110/2201: months in litigation with appeals-court original jurisdiction + expedited review |
| lit_data_mult (current law) | 0.5 / 1.0 | +0.7 / +0.7 | +0.0 / +0.0 | -68.7 / -99.6 | scale on the energy-specific EA/CE suit rates (renewables, transmission) [D: suits / BLM + DOE reviews, 2012-21]; < 1 because other agencies' reviews are missing from the denominator |
| lit_ea (current law) | 0.0025 / 0.01 | +0.7 / +0.7 | +0.0 / +0.1 | -83.1 / -85.3 | P(sued | EA) for gas and hydro: all-sector case data x ~10,000 EAs/yr (CEQ estimate) |
| p_kill_vac (current law) | 0.1 / 0.4 | +0.7 / +0.7 | +0.0 / +0.0 | -84.0 / -84.0 | P(project cancelled | permit vacated) |
| remand_months (current law) | 6 / 18 | +0.6 / +0.7 | +0.0 / +0.0 | -84.0 / -84.0 | delay after vacatur, current law |
