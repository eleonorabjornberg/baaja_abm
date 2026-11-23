# Simulation 4: permit certainty across administrations

Executive halts hit permitted projects that are not yet online after a change of administration hostile to their side. Offshore wind's halt probability is anchored on the 2025 stop-work orders; other technologies are ranges. Sec.1401 leaves a residual halt probability for its exceptions: central 50%, range 10-100%, because the Senate-passed text adds an exception for action 'taken pursuant to any applicable law or regulation', which could cover stop-work orders like 2025's.

## Halted GW by political path, and what Sec.1401 adds (BAAJA with vs without Sec.1401)

| political path | halted GW, law | BAAJA w/o 1401 | BAAJA | 1401 gain: Renewable (new) | 1401 gain: Fossil (gas) | 1401 gain: Storage |
|---|---|---|---|---|---|---|
| random (default) | 5.3 | 6.0 | 3.1 | +0.3 [+0.0, +1.1] | +0.0 [+0.0, +0.2] | +0.0 [+0.0, +0.1] |
| always hostile to renewables | 9.6 | 11.1 | 5.7 | +0.7 [+0.1, +1.6] | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.2] |
| always hostile to fossil | 0.9 | 1.0 | 0.5 | +0.0 [+0.0, +0.0] | +0.1 [+0.0, +0.4] | +0.0 [+0.0, +0.0] |

## Same comparison if 2025's request mix continues (regime "2025")

| scenario | renewable GW | gas GW | storage GW | renewable share of new TWh |
|---|---|---|---|---|
| Current law | 583 [566, 600] | 305 [294, 319] | 203 [195, 211] | 48.7% |
| BAAJA | +4.5 [+3.2, +5.8] | +2.3 [+1.1, +3.8] | +0.2 [+0.0, +0.5] | +0.05 pts |
| BAAJA without Sec.1401 | +4.4 [+3.1, +5.7] | +2.2 [+1.1, +3.3] | +0.2 [+0.0, +0.5] | +0.04 pts |

## Projects halted and cancelled, by technology (random politics; law vs BAAJA)

| technology | halted, law | halted, BAAJA | cancelled (courts or halts) |
|---|---|---|---|
| Gas | 2.1 | 1.1 | 0.5 -> 0.2 |
| Offshore wind | 4.5 | 2.6 | 1.4 -> 0.5 |
| Onshore wind | 1.3 | 0.7 | 0.7 -> 0.2 |
| Solar | 7.0 | 4.9 | 2.8 -> 1.1 |
| Storage | 1.7 | 0.8 | 1.6 -> 0.2 |
| Transmission | 2.2 | 1.2 | 1.7 -> 0.3 |

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
| halt_mult_1401 | 0.1 / 1.0 | +6.9 / +6.2 | +1.1 / +1.0 | -4.6 / +0.8 | Sec.1401: residual halt probability relative to current law. The Senate-passed text adds exception (F), action 'taken pursuant to any applicable law or regulation', which could cover stop-work orders like 2025's (issued under existing regulations); high = the exception swallows the rule, low = courts read it narrowly |
| halt_mult_other (current law) | 0.5 / 2.0 | +6.6 / +6.6 | +1.0 / +1.1 | -1.9 / -2.8 | multiplier on halt probabilities for technologies other than offshore wind |
| p_kill_halt (current law) | 0.1 / 0.5 | +6.5 / +6.7 | +1.0 / +1.1 | -2.2 / -2.2 | P(cancelled | halted) |
| halt_len (current law) | 4 / 12 | +6.5 / +6.6 | +1.0 / +1.1 | -2.2 / -2.2 | months a halted project is stopped |
