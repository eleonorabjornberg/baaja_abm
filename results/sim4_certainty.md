# Simulation 4: permit certainty across administrations

Executive halts hit permitted projects that are not yet online after a change of administration hostile to their side. Offshore wind's halt probability is anchored on the 2025 stop-work orders; other technologies are ranges. Sec.1401 leaves a residual (central 10%) for its exceptions.

## Halted GW by political path, and what Sec.1401 adds (BAAJA with vs without Sec.1401)

| political path | halted GW, law | BAAJA w/o 1401 | BAAJA | 1401 gain: Renewable (new) | 1401 gain: Fossil (gas) | 1401 gain: Storage |
|---|---|---|---|---|---|---|
| random (default) | 8.1 | 9.2 | 0.9 | +1.2 [+0.0, +3.3] | +0.1 [+0.0, +0.4] | +0.0 [+0.0, +0.1] |
| always hostile to renewables | 15.1 | 17.3 | 1.7 | +2.5 [+0.7, +4.5] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.1] |
| always hostile to fossil | 1.0 | 1.0 | 0.1 | +0.0 [+0.0, +0.0] | +0.2 [+0.0, +0.5] | +0.0 [+0.0, +0.0] |

## Projects halted and cancelled, by technology (random politics; law vs BAAJA)

| technology | halted, law | halted, BAAJA | cancelled (courts or halts) |
|---|---|---|---|
| Gas | 2.4 | 0.3 | 0.7 -> 0.1 |
| Offshore wind | 8.5 | 0.9 | 2.5 -> 0.2 |
| Onshore wind | 0.4 | 0.0 | 0.3 -> 0.0 |
| Solar | 5.3 | 0.8 | 1.9 -> 0.3 |
| Storage | 1.0 | 0.1 | 0.2 -> 0.0 |
| Transmission | 2.1 | 0.3 | 1.4 -> 0.1 |

## Plant lifetimes (EIA-860 retired generators)

Plants built from 2026 do not reach retirement age before 2041, so lifetimes do not change the 2041 totals. The bill's operating-permit terms (NPDES 10 years, Sec.1203) matter for existing gas plants' renewals, which this model does not track.

| technology | median age at retirement | MW-weighted mean | GW retired since 2015 |
|---|---|---|---|
| Coal | 56 | 50 | 84.4 |
| Gas | 45 | 46 | 35.8 |
| Geothermal | 23 | 26 | 0.3 |
| Hydro | 86 | 64 | 0.8 |
| Onshore wind | 21 | 22 | 1.0 |
| Solar | 8 | 9 | 0.1 |
| Storage | 7 | 5 | 0.4 |

## Sensitivity (all provisions; other values central)

| assumption | low / high | renewable GW gain | gas GW gain | halted GW change | what it is |
|---|---|---|---|---|---|
| halt_mult_1401 | 0.0 / 0.3 | +10.0 / +9.7 | +1.2 / +1.2 | -8.1 / -5.3 | Sec.1401: residual halt probability relative to current law |
| halt_mult_other (current law) | 0.5 / 2.0 | +9.8 / +10.0 | +1.2 / +1.3 | -6.7 / -8.3 | multiplier on halt probabilities for technologies other than offshore wind |
| p_kill_halt (current law) | 0.1 / 0.5 | +9.6 / +10.3 | +1.2 / +1.2 | -7.2 / -7.2 | P(cancelled | halted) |
| halt_len (current law) | 4 / 12 | +9.6 / +10.1 | +1.2 / +1.2 | -7.2 / -7.2 | months a halted project is stopped |
