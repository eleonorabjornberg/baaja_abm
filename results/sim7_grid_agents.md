# Simulation 7: grid access as an agent-based system

Interconnection is no longer a drawn study time. Each region's grid operator studies requests in clusters (ERCOT: one by one) at a throughput fitted to LBNL request-to-agreement times and adapting to the arrival rate; developers enter on the published wait and on their region's projected capacity shortfall, and leave at study results when the allocated network-upgrade cost exceeds their private value (both from LBNL cost data). Upgrade costs rise as capacity is signed and fall as transmission is built. Sec.2106 becomes published locations with a fixed fee and a single decision point in RTOs that change their process (drawn per RTO); Sec.2110 a throughput multiplier (0 by default: the bill does not size it); Sec.2109 extra hosting per transmission line built after the rule. Every scenario is paired with current law under the same agents. Numbers: mean [5th, 95th percentile] across 100 runs, GW online by Nov 2041.

## What the grid sections add (difference from current law, grid agents)

| scenario (grid agents) | renewable GW | gas GW | storage GW | total GW | firm GW 2035 | shortfall GW 2035 | shortfall GW 2041 |
|---|---|---|---|---|---|---|---|
| BAAJA | +17.7 [+8.6, +27.8] | +9.2 [+1.1, +17.8] | +2.5 [-0.0, +5.1] | +31.2 [+14.0, +47.4] | +6.9 [+1.7, +12.3] | -1.5 [-3.1, -0.1] | -3.8 [-6.9, -0.7] |
| BAAJA without Sec.2106 | +6.1 [+4.3, +8.7] | +1.0 [+0.2, +1.8] | +1.6 [+1.0, +2.3] | +10.5 [+8.5, +12.8] | +1.0 [+0.5, +1.6] | -0.2 [-0.5, +0.0] | -0.8 [-1.5, -0.3] |
| BAAJA without Sec.2109 hosting | +14.8 [+5.4, +25.2] | +8.4 [+0.4, +16.4] | +1.0 [-1.4, +3.3] | +26.0 [+8.7, +42.1] | +6.7 [+1.4, +12.1] | -1.4 [-3.0, -0.1] | -3.4 [-6.4, -0.1] |
| Sec.2106 only | +11.4 [+1.6, +21.8] | +8.1 [+0.0, +15.8] | +0.9 [-1.4, +3.2] | +20.5 [+2.5, +35.9] | +5.8 [+0.6, +11.2] | -1.2 [-3.0, +0.0] | -3.1 [-6.0, +0.0] |
| BAAJA, Sec.2106 adopted by every RTO | +28.8 [+22.8, +33.5] | +16.9 [+14.2, +20.0] | +2.9 [+1.2, +4.5] | +50.4 [+43.1, +55.3] | +12.5 [+9.9, +15.4] | -2.5 [-3.5, -1.5] | -6.2 [-8.2, -4.3] |
| BAAJA + Sec.2110 throughput +25% | +27.8 [+21.8, +35.4] | +12.8 [+6.9, +19.1] | +5.9 [+2.9, +8.8] | +48.3 [+37.6, +59.0] | +13.7 [+8.7, +18.8] | -1.7 [-3.2, -0.3] | -4.3 [-7.2, -1.3] |

## Exogenous study times vs grid agents

Sims 1-6 draw each request's study time; here it comes out of the queue. The agents' current law is lower because study results now remove projects whose upgrade costs exceed their value, on top of the fitted hazards.

| grid model | current law total GW 2041 | BAAJA minus current law, total GW | renewable GW | gas GW | storage GW |
|---|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 1105 [1083, 1127] | +9.7 [+7.8, +11.5] | +6.6 [+4.7, +8.2] | +1.0 [+0.4, +1.6] | +0.3 [+0.1, +0.6] |
| grid agents (this simulation) | 945 [928, 964] | +31.2 [+14.0, +47.4] | +17.7 [+8.6, +27.8] | +9.2 [+1.1, +17.8] | +2.5 [-0.0, +5.1] |

## By region (requests made 2026-30; mean across runs)

| region | law: requests/yr | law: months to agreement | law: share signed | law: withdrawn at results | law: GW online 2041 | BAAJA: requests/yr | BAAJA: months | BAAJA: share signed | BAAJA: GW | 2106 everywhere: GW |
|---|---|---|---|---|---|---|---|---|---|---|
| CAISO | 168 | 33 | 0.10 | 0.16 | 43 | -8 | -0.8 | +0.015 | +2.7 | +4.4 |
| ERCOT | 504 | 28 | 0.18 | 0.82 | 188 | +0 | +0.0 | +0.000 | +1.1 | +1.1 |
| ISO-NE | 118 | 32 | 0.12 | 0.70 | 18 | -17 | -1.5 | +0.028 | +0.5 | +0.7 |
| MISO | 565 | 34 | 0.08 | 0.56 | 140 | -83 | -2.4 | +0.024 | +11.7 | +22.0 |
| NYISO | 231 | 31 | 0.07 | 0.61 | 28 | -39 | -1.5 | +0.024 | +2.2 | +3.2 |
| PJM | 453 | 31 | 0.12 | 0.81 | 113 | -58 | -1.5 | +0.025 | +5.1 | +8.4 |
| SPP | 227 | 35 | 0.07 | 0.81 | 59 | -39 | -2.2 | +0.022 | +3.4 | +5.9 |
| Southeast | 400 | 30 | 0.16 | 0.39 | 138 | +0 | -0.0 | +0.000 | +0.8 | +0.8 |
| West | 689 | 38 | 0.14 | 0.58 | 203 | +0 | +0.0 | +0.001 | +2.2 | +2.2 |

## Validation

### Grid operators: months from request to signed agreement, by request year (LBNL)

Fitted on 2010-19 cohorts; 2020-24 cohorts are a holdout. Error: mean squared log ratio of median months plus squared difference in the share signed by Dec 2025, by cohort. Regions without reliable agreement dates take the joint MISO+CAISO fit.

| region | operator | cluster months / mode | min study months | fit error 2010-19 | holdout error 2020-24 | fit cohorts: model/data median months | holdout cohorts: model/data |
|---|---|---|---|---|---|---|---|
| CAISO | own fit | 12/serial | 33 | 0.05 | 0.04 |  | 2020: 38/44; 2021: 39/50 |
| ERCOT | own fit | 1/parallel | 27 | 0.09 | 0.07 |  | 2020: 23/21; 2021: 26/24; 2022: 22/21; 2023: 20/18; 2024: 15/15 |
| ISO-NE | pooled (MISO+CAISO) | 12/serial | 24 | 0.06 | 0.26 |  | 2020: 59/31 |
| MISO | own fit | 12/serial | 15 | 0.05 | 0.08 |  | 2020: 45/51; 2021: 45/48 |
| NYISO | pooled (MISO+CAISO) | 12/serial | 24 | 0.05 | 0.13 |  | - |
| PJM | pooled (MISO+CAISO) | 12/serial | 24 | 0.29 | 0.24 |  | - |
| SPP | pooled (MISO+CAISO) | 12/serial | 24 | 0.70 | 0.56 |  | - |
| Southeast | pooled (MISO+CAISO) | 12/serial | 24 | 0.52 | 0.00 |  | - |
| West | pooled (MISO+CAISO) | 12/serial | 24 | 0.72 | 0.46 |  | 2020: 49/22; 2021: 50/22 |

### Developers: share of requests withdrawn by months after request (2015-19 cohorts vs model 2026-30)

Fitted at 24 months (one pre-agreement hazard per region); 12, 36 and 60 months are checks. Data counts still-active requests as not withdrawn.

| region | withdrawn by 12 months: model / data | withdrawn by 24 months: model / data | withdrawn by 36 months: model / data | withdrawn by 60 months: model / data |
|---|---|---|---|---|
| CAISO | 0.36 / 0.58 | 0.61 / 0.60 | 0.82 / 0.65 | 0.94 / 0.69 |
| ERCOT | 0.06 / 0.10 | 0.34 / 0.17 | 0.56 / 0.24 | 0.75 / 0.35 |
| ISO-NE | 0.08 / 0.29 | 0.40 / 0.40 | 0.85 / 0.50 | 0.90 / 0.59 |
| MISO | 0.17 / 0.16 | 0.44 / 0.43 | 0.88 / 0.56 | 0.95 / 0.62 |
| NYISO | 0.16 / 0.39 | 0.54 / 0.52 | 0.92 / 0.59 | 0.95 / 0.69 |
| PJM | 0.03 / 0.30 | 0.42 / 0.42 | 0.86 / 0.48 | 0.89 / 0.59 |
| SPP | 0.05 / 0.14 | 0.25 / 0.23 | 0.83 / 0.27 | 0.94 / 0.58 |
| Southeast | 0.24 / 0.46 | 0.58 / 0.58 | 0.85 / 0.61 | 0.92 / 0.71 |
| West | 0.11 / 0.09 | 0.24 / 0.24 | 0.69 / 0.42 | 0.88 / 0.68 |

| region | pre-agreement withdrawal hazard, %/month |
|---|---|
| CAISO | 3.60 |
| ERCOT | 0.01 |
| ISO-NE | 0.71 |
| MISO | 1.55 |
| NYISO | 1.49 |
| PJM | 0.29 |
| SPP | 0.44 |
| Southeast | 2.23 |
| West | 0.97 |

### Developers: value relative to LBNL's P(complete | cost) fit

One scale per technology and region, fitted so completion of new requests matches the regional LBNL targets. Values below 1 mean fewer requests complete than LBNL's cost-completion relation alone implies.

| technology | region | value scale (fitted to completion) |
|---|---|
| Gas | 1.00 |
| Gas|ERCOT | 0.29 |
| Gas|MISO | 2.45 |
| Gas|SPP | 1.00 |
| Gas|Southeast | 2.29 |
| Gas|West | 1.87 |
| Geothermal | 4.96 |
| Geothermal|West | 0.68 |
| Offshore wind | 0.10 |
| Onshore wind | 0.39 |
| Onshore wind|ERCOT | 0.12 |
| Onshore wind|MISO | 0.73 |
| Onshore wind|NYISO | 1.15 |
| Onshore wind|SPP | 0.32 |
| Onshore wind|West | 0.90 |
| Solar|CAISO | 1.66 |
| Solar|ERCOT | 0.10 |
| Solar|ISO-NE | 0.66 |
| Solar|MISO | 0.27 |
| Solar|NYISO | 0.29 |
| Solar|PJM | 0.19 |
| Solar|SPP | 0.06 |
| Solar|Southeast | 0.78 |
| Solar|West | 0.69 |
| Storage|CAISO | 0.79 |
| Storage|ERCOT | 0.04 |
| Storage|ISO-NE | 0.19 |
| Storage|MISO | 0.04 |
| Storage|NYISO | 0.11 |
| Storage|PJM | 0.10 |
| Storage|SPP | 0.03 |
| Storage|Southeast | 1.55 |
| Storage|West | 0.95 |

### Time from request to operation, completed projects

Known gap: in the agents model, waiting longer does not make a request more likely to withdraw (the background hazard is small and fitted to withdrawal timing), so completed projects are not selected for short waits as in the data and their median time to operation is longer than LBNL's. This lowers current-law GW by 2041 relative to the exogenous model; the bill's effect is a paired difference under the same agents.

| technology | LBNL median months request -> operation (completed) | exogenous grid (model) | grid agents (model) |
|---|---|---|---|
| Solar | 62 | 62 | 76 |
| Onshore wind | 52 | 52 | 67 |
| Gas | 37 | 38 | 59 |
| Storage | - | 40 | 62 |

### Developers: completion by allocated network-upgrade cost (ISO regions)

LBNL counts requests resolved by 2024 (completed vs withdrawn); the model counts every 2026-41 request that received a study result, so the level differs; the gradient is the check.

| allocated cost $/kW | model: share completing | LBNL: share completing (resolved requests) | LBNL n |
|---|---|---|---|
| 0-10 | 0.67 | 0.80 | 426 |
| 10-50 | 0.30 | 0.67 | 476 |
| 50-100 | 0.14 | 0.59 | 365 |
| 100-200 | 0.08 | 0.42 | 297 |
| 200-400 | 0.04 | 0.18 | 225 |
| 400-1000000000.0 | 0.01 | 0.07 | 306 |

## Sensitivity: grid assumptions at the low and high end of their ranges (20 paired runs each)

| assumption | low / high | BAAJA minus current law, total GW | current law total GW | what it is |
|---|---|---|---|---|
| entry_wait_elast (current law) | 0.0 / 1.0 | +26.3 / +30.7 | 943 / 949 | elasticity of new requests to the published wait for a study result |
| scarcity_beta (current law) | 0.0 / 3.0 | +28.4 / +26.2 | 948 / 941 | developer value and entry rise by exp(beta x change in the region's projected capacity shortfall as a share of peak demand, 4 years ahead) |
| kappa (current law) | 1.56 / 5.14 | +29.3 / +19.3 | 1007 / 761 | growth of network-upgrade cost with capacity signed, per share of the regional fleet [D: LBNL cost data, 2018+ vs 2010-17 requests; MISO, SPP, PJM] |
| restudy_rho (current law) | 0.1 / 0.6 | +21.4 / +33.9 | 972 / 912 | re-study: cost rise for remaining requests per unit withdrawn MW share |
| restudy_months (current law) | 3 / 12 | +24.3 / +31.2 | 945 / 945 | months from first study result to agreement in cluster regions (re-study, facilities) |
| tx_hosting_gw (current law) | 0.5 / 3.0 | +23.1 / +32.9 | 945 / 945 | GW of interconnection room added by one transmission project |
| adopt_2106 (bill) | 0.0 / 1.0 | +10.7 / +50.2 | 945 / 945 | Sec.2106(d): probability that an RTO's process changes rather than being found compliant, drawn per RTO |
| planned_share_2106 (bill) | 0.25 / 0.9 | +23.8 / +32.1 | 945 / 945 | Sec.2106(a)(2): share of requests able to use a published location |
| q_min_2106 (bill) | 0.1 / 0.5 | +34.4 / +5.8 | 945 / 945 | Sec.2106(a)(3): lowest chance of completing (cost below value) at which a request still enters, given non-refundable security and penalties |
| fee_mult_2106 (bill) | 0.8 / 1.5 | +30.2 / +23.2 | 945 / 945 | Sec.2106(a)(2): fixed fee as a multiple of the region's median upgrade cost |
| g_2110 (bill) | 0.0 / 0.25 | +27.0 / +46.0 | 945 / 945 | Sec.2110: study throughput gain (rulemaking with no target) |
| hosting_2109 (bill) | 0.0 / 0.3 | +21.7 / +38.0 | 945 / 945 | Sec.2109: extra hosting room per transmission project (advanced transmission technologies) |
