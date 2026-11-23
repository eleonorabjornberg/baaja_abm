# Simulation 7: grid access as an agent-based system

Interconnection is no longer a drawn study time. Each region's grid operator studies requests in clusters (ERCOT: one by one) at a throughput fitted to LBNL request-to-agreement times and adapting to the arrival rate; developers enter on the published wait and on their region's projected capacity shortfall, and leave at study results when the allocated network-upgrade cost exceeds their private value (both from LBNL cost data). Upgrade costs rise as capacity is signed and fall as transmission is built. Sec.2106 becomes published locations with a fixed fee and a single decision point in RTOs that change their process (drawn per RTO); Sec.2110 a throughput multiplier (0 by default: the bill does not size it); Sec.2109 extra hosting per transmission line built after the rule. Every scenario is paired with current law under the same agents. Numbers: mean [5th, 95th percentile] across 100 runs, GW online by Nov 2041.

## What the grid sections add (difference from current law, grid agents)

| scenario (grid agents) | renewable GW | gas GW | storage GW | total GW | firm GW 2035 | shortfall GW 2035 | shortfall GW 2041 |
|---|---|---|---|---|---|---|---|
| BAAJA | +18.6 [+7.0, +31.0] | +8.1 [+1.3, +16.2] | +3.5 [+0.8, +5.9] | +32.0 [+13.6, +52.8] | +7.8 [+1.7, +14.4] | -1.8 [-3.6, -0.0] | -5.1 [-8.9, -1.2] |
| BAAJA without Sec.2106 | +5.3 [+3.7, +7.0] | +1.0 [+0.4, +1.6] | +1.7 [+0.9, +2.5] | +9.8 [+7.7, +11.9] | +0.9 [+0.4, +1.3] | -0.1 [-0.3, +0.0] | -0.8 [-1.4, -0.4] |
| BAAJA without Sec.2109 hosting | +15.5 [+3.9, +28.2] | +7.3 [+0.4, +15.3] | +1.9 [-0.4, +4.3] | +26.5 [+7.5, +45.5] | +7.6 [+1.3, +14.0] | -1.7 [-3.5, -0.0] | -4.5 [-8.0, -0.3] |
| Sec.2106 only | +13.0 [+1.7, +24.6] | +7.0 [+0.0, +15.1] | +1.8 [-0.5, +4.1] | +21.8 [+2.7, +40.7] | +6.9 [+0.8, +13.2] | -1.6 [-3.5, +0.0] | -4.3 [-7.8, -0.2] |
| BAAJA, Sec.2106 adopted by every RTO | +30.2 [+26.1, +34.7] | +15.0 [+11.5, +18.2] | +4.7 [+3.1, +6.5] | +51.6 [+45.9, +57.7] | +14.1 [+12.2, +16.2] | -3.1 [-4.1, -2.2] | -8.6 [-10.7, -7.1] |
| BAAJA + Sec.2110 throughput +25% | +25.7 [+16.4, +35.1] | +10.9 [+5.6, +17.5] | +6.7 [+3.6, +9.4] | +45.1 [+31.1, +61.0] | +13.1 [+7.5, +19.1] | -1.8 [-3.6, -0.0] | -5.1 [-9.0, -1.3] |

## Exogenous study times vs grid agents

Sims 1-6 draw each request's study time; here it comes out of the queue. The agents' current law is lower because study results now remove projects whose upgrade costs exceed their value, on top of the fitted hazards.

| grid model | current law total GW 2041 | BAAJA minus current law, total GW | renewable GW | gas GW | storage GW |
|---|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 1105 [1083, 1127] | +9.7 [+7.8, +11.5] | +6.6 [+4.7, +8.2] | +1.0 [+0.4, +1.6] | +0.3 [+0.1, +0.6] |
| grid agents (this simulation) | 910 [895, 926] | +32.0 [+13.6, +52.8] | +18.6 [+7.0, +31.0] | +8.1 [+1.3, +16.2] | +3.5 [+0.8, +5.9] |

### Current law: capacity shortfall below reference margins

With grid agents, developers respond to their region's projected shortfall, so surpluses and shortfalls are no longer fixed by the 2021-25 request mix, but fewer projects get through the queue overall.

| grid model | shortfall GW 2027 | shortfall GW 2035 | shortfall GW 2041 | regions below reference margin, 2035 |
|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 8 [7, 9] | 68 [65, 71] | 129 [126, 133] | 2.2 [2.0, 3.0] |
| grid agents (this simulation) | 8 [7, 9] | 71 [69, 74] | 137 [134, 140] | 2.2 [2.0, 3.0] |

| region | reserve margin 2035: exogenous / agents | shortfall GW 2035: exogenous / agents |
|---|---|---|
| CAISO | 12% / 9% | 4.6 / 6.9 |
| ERCOT | 80% / 64% | 0.0 / 0.0 |
| ISO-NE | 15% / 15% | 0.1 / 0.1 |
| MISO | 17% / 13% | 0.0 / 0.0 |
| NYISO | 27% / 23% | 0.0 / 0.0 |
| PJM | 3% / 3% | 63.2 / 64.6 |
| SPP | 30% / 25% | 0.0 / 0.0 |
| Southeast | 30% / 30% | 0.0 / 0.0 |
| West | 54% / 42% | 0.0 / 0.0 |

## By region (requests made 2026-30; mean across runs)

| region | law: requests/yr | law: months to agreement | law: share signed | law: withdrawn at results | law: GW online 2041 | BAAJA: requests/yr | BAAJA: months | BAAJA: share signed | BAAJA: GW | 2106 everywhere: GW |
|---|---|---|---|---|---|---|---|---|---|---|
| CAISO | 173 | 37 | 0.11 | 0.23 | 40 | -13 | -1.3 | +0.015 | +2.0 | +3.4 |
| ERCOT | 504 | 26 | 0.14 | 0.64 | 168 | +0 | -0.0 | +0.000 | +1.1 | +1.1 |
| ISO-NE | 117 | 30 | 0.15 | 0.44 | 22 | -12 | -1.2 | +0.028 | +1.2 | +2.0 |
| MISO | 571 | 31 | 0.07 | 0.51 | 135 | -83 | -2.7 | +0.024 | +12.2 | +22.8 |
| NYISO | 232 | 30 | 0.07 | 0.42 | 28 | -36 | -1.3 | +0.021 | +1.9 | +2.9 |
| PJM | 444 | 30 | 0.13 | 0.47 | 125 | -35 | -1.5 | +0.022 | +7.2 | +11.9 |
| SPP | 231 | 31 | 0.06 | 0.75 | 55 | -40 | -1.4 | +0.019 | +1.9 | +3.1 |
| Southeast | 408 | 30 | 0.15 | 0.28 | 137 | +0 | -0.0 | +0.000 | +0.8 | +0.8 |
| West | 691 | 36 | 0.12 | 0.55 | 185 | +0 | +0.0 | +0.001 | +1.9 | +1.9 |

## Validation

### Grid operators: months from request to signed agreement, by request year (LBNL)

Fitted on 2010-19 cohorts; 2020-24 cohorts are a holdout. Error: mean squared log ratio of median months plus squared difference in the share signed by Dec 2025, by cohort. Regions without reliable agreement dates take the joint MISO+CAISO fit.

| region | operator | cluster months / mode | min study months | fit error 2010-19 | holdout error 2020-24 | fit cohorts: model/data median months | holdout cohorts: model/data |
|---|---|---|---|---|---|---|---|
| CAISO | own fit | 12/serial | 33 | 0.05 | 0.04 | 2010: 42/35; 2014: 45/42; 2017: 39/44; 2019: 43/35 | 2020: 38/44; 2021: 39/50 |
| ERCOT | own fit | 1/parallel | 27 | 0.09 | 0.07 | 2014: 26/31; 2017: 24/20; 2019: 26/20 | 2020: 23/21; 2021: 26/24; 2022: 22/21; 2023: 20/18; 2024: 15/15 |
| ISO-NE | pooled (MISO+CAISO) | 12/serial | 24 | 0.06 | 0.26 | 2014: 31/17; 2019: 48/33 | 2020: 59/31 |
| MISO | own fit | 12/serial | 15 | 0.05 | 0.08 | 2010: 25/21; 2014: 23/20; 2017: 36/33; 2019: 44/45 | 2020: 45/51; 2021: 45/48 |
| NYISO | pooled (MISO+CAISO) | 12/serial | 24 | 0.05 | 0.13 | 2017: 41/42; 2019: 57/40 | - |
| PJM | pooled (MISO+CAISO) | 12/serial | 24 | 0.29 | 0.24 | 2014: 27/36; 2017: 31/44; 2019: 35/26 | - |
| SPP | pooled (MISO+CAISO) | 12/serial | 24 | 0.70 | 0.56 |  | - |
| Southeast | pooled (MISO+CAISO) | 12/serial | 24 | 0.52 | 0.00 |  | - |
| West | pooled (MISO+CAISO) | 12/serial | 24 | 0.72 | 0.46 | 2010: 36/12; 2014: 31/12; 2017: 43/27; 2019: 50/27 | 2020: 49/22; 2021: 50/22 |

### Developers: share of requests withdrawn by months after request (2015-19 cohorts vs model 2026-30)

Withdrawal is fitted in the 2010-25 backcast, where model and data cohorts are the same requests (Phase 3; results/backcast.md): a first-year hazard, a later hazard and a hold after an adverse study result, by region, to LBNL's 12-, 36- and 60-month shares; 24 months is a check. This table shows the forward 2026-30 cohorts under current law next to the 2015-19 data for comparison only: the queue they face is different, so they need not match. In CAISO, ISO-NE, MISO and NYISO the fitted hold reaches its 20-year bound: developers with an adverse result stay in the queue past 2025, and the data cannot tell a long hold from never withdrawing. Sec.2106(a)(3)'s single decision point and withdrawal penalties shorten the hold (lag_2106).

| region | withdrawn by 12 months: model / data | withdrawn by 24 months: model / data | withdrawn by 36 months: model / data | withdrawn by 60 months: model / data |
|---|---|---|---|---|
| CAISO | 0.58 / 0.58 | 0.62 / 0.60 | 0.66 / 0.65 | 0.72 / 0.69 |
| ERCOT | 0.10 / 0.10 | 0.18 / 0.17 | 0.26 / 0.24 | 0.40 / 0.35 |
| ISO-NE | 0.29 / 0.29 | 0.41 / 0.40 | 0.50 / 0.50 | 0.63 / 0.59 |
| MISO | 0.16 / 0.16 | 0.40 / 0.43 | 0.57 / 0.56 | 0.76 / 0.62 |
| NYISO | 0.40 / 0.39 | 0.50 / 0.52 | 0.59 / 0.59 | 0.72 / 0.69 |
| PJM | 0.30 / 0.30 | 0.39 / 0.42 | 0.48 / 0.48 | 0.61 / 0.59 |
| SPP | 0.14 / 0.14 | 0.23 / 0.23 | 0.56 / 0.27 | 0.87 / 0.58 |
| Southeast | 0.47 / 0.46 | 0.55 / 0.58 | 0.63 / 0.61 | 0.72 / 0.71 |
| West | 0.09 / 0.09 | 0.24 / 0.24 | 0.42 / 0.42 | 0.70 / 0.68 |

| region | background withdrawal hazard, %/month: first 12 months | after 12 months, to construction | mean hold after an adverse study result, months |
|---|---|---|---|
| CAISO | 7.01 | 0.80 | 240 |
| ERCOT | 0.82 | 0.74 | 227 |
| ISO-NE | 2.80 | 1.48 | 240 |
| MISO | 1.43 | 2.71 | 240 |
| NYISO | 4.18 | 1.53 | 240 |
| PJM | 2.94 | 1.06 | 159 |
| SPP | 1.21 | 0.43 | 14 |
| Southeast | 5.12 | 1.40 | 120 |
| West | 0.81 | 1.45 | 38 |

### Developers: value relative to LBNL's P(complete | cost) fit

One scale per technology and region, fitted so completion of new requests matches the regional LBNL targets. Values below 1 mean fewer requests complete than LBNL's cost-completion relation alone implies.

| technology | region | value scale (fitted to completion) |
|---|---|---|
| Gas | all (pooled) | 1.60 |
| Gas | ERCOT | 0.24 |
| Gas | MISO | 2.22 |
| Gas | SPP | 0.54 |
| Gas | Southeast | 2.89 |
| Gas | West | 1.00 |
| Geothermal | all (pooled) | 3.87 |
| Geothermal | West | 0.75 |
| Offshore wind | all (pooled) | 0.09 |
| Onshore wind | all (pooled) | 0.81 |
| Onshore wind | ERCOT | 0.13 |
| Onshore wind | MISO | 0.56 |
| Onshore wind | NYISO | 1.28 |
| Onshore wind | SPP | 0.31 |
| Onshore wind | West | 0.45 |
| Solar | CAISO | 0.56 |
| Solar | ERCOT | 0.10 |
| Solar | ISO-NE | 1.77 |
| Solar | MISO | 0.29 |
| Solar | NYISO | 0.38 |
| Solar | PJM | 0.41 |
| Solar | SPP | 0.07 |
| Solar | Southeast | 0.96 |
| Solar | West | 0.44 |
| Storage | CAISO | 0.49 |
| Storage | ERCOT | 0.04 |
| Storage | ISO-NE | 0.43 |
| Storage | MISO | 0.06 |
| Storage | NYISO | 0.15 |
| Storage | PJM | 0.20 |
| Storage | SPP | 0.04 |
| Storage | Southeast | 2.31 |
| Storage | West | 1.00 |

### Time from request to operation, completed projects

Known gap: in the agents model, waiting longer does not make a request more likely to withdraw (the background hazard is small and fitted to withdrawal timing), so completed projects are not selected for short waits as in the data and their median time to operation is longer than LBNL's. This lowers current-law GW by 2041 relative to the exogenous model; the bill's effect is a paired difference under the same agents.

| technology | LBNL median months request -> operation (completed) | exogenous grid (model) | grid agents (model) |
|---|---|---|---|
| Solar | 62 | 62 | 63 |
| Onshore wind | 52 | 52 | 64 |
| Gas | 37 | 38 | 48 |
| Storage | - | 40 | 61 |

### Developers: completion by allocated network-upgrade cost (ISO regions)

LBNL counts requests resolved by 2024 (completed vs withdrawn); the model counts every 2026-41 request that received a study result, so the level differs; the gradient is the check.

| allocated cost $/kW | model: share completing | LBNL: share completing (resolved requests) | LBNL n |
|---|---|---|---|
| 0-10 | 0.66 | 0.80 | 426 |
| 10-50 | 0.32 | 0.67 | 476 |
| 50-100 | 0.17 | 0.59 | 365 |
| 100-200 | 0.10 | 0.42 | 297 |
| 200-400 | 0.06 | 0.18 | 225 |
| 400+ | 0.01 | 0.07 | 306 |

## Sensitivity: grid assumptions at the low and high end of their ranges (20 paired runs each)

| assumption | low / high | BAAJA minus current law, total GW | current law total GW | what it is |
|---|---|---|---|---|
| entry_wait_elast (current law) | 0.0 / 1.0 | +26.0 / +31.0 | 908 / 918 | elasticity of new requests to the published wait for a study result |
| scarcity_beta (current law) | 0.0 / 3.0 | +28.8 / +23.2 | 912 / 914 | developer value and entry rise by exp(beta x change in the region's projected capacity shortfall as a share of peak demand, 4 years ahead) |
| kappa (current law) | 1.56 / 5.14 | +29.5 / +19.7 | 965 / 743 | growth of network-upgrade cost with capacity signed, per share of the regional fleet [D: LBNL cost data, 2018+ vs 2010-17 requests; MISO, SPP, PJM] |
| restudy_rho (current law) | 0.1 / 0.6 | +21.1 / +33.7 | 937 / 880 | re-study: cost rise for remaining requests per unit withdrawn MW share |
| restudy_months (current law) | 3 / 12 | +24.0 / +32.3 | 911 / 911 | months from first study result to agreement in cluster regions (re-study, facilities) |
| tx_hosting_gw (current law) | 0.5 / 3.0 | +23.0 / +33.0 | 911 / 911 | GW of interconnection room added by one transmission project |
| adopt_2106 (bill) | 0.0 / 1.0 | +10.0 / +51.6 | 911 / 911 | Sec.2106(d): probability that an RTO's process changes rather than being found compliant, drawn per RTO |
| planned_share_2106 (bill) | 0.25 / 0.9 | +23.5 / +32.5 | 911 / 911 | Sec.2106(a)(2): share of requests able to use a published location |
| q_min_2106 (bill) | 0.1 / 0.5 | +34.6 / +6.0 | 911 / 911 | Sec.2106(a)(3): lowest chance of completing (cost below value) at which a request still enters, given non-refundable security and penalties |
| lag_2106 (bill) | 0.0 / 1.0 | +27.0 / +27.0 | 911 / 911 | Sec.2106(a)(3): months a developer holds its queue position after an adverse study result, relative to current law, with a single decision point and withdrawal penalties (0 = leaves at once) |
| fee_mult_2106 (bill) | 0.8 / 1.5 | +30.6 / +23.1 | 911 / 911 | Sec.2106(a)(2): fixed fee as a multiple of the region's median upgrade cost |
| g_2110 (bill) | 0.0 / 0.25 | +27.0 / +42.5 | 911 / 911 | Sec.2110: study throughput gain (rulemaking with no target) |
| hosting_2109 (bill) | 0.0 / 0.3 | +21.3 / +38.6 | 911 / 911 | Sec.2109: extra hosting room per transmission project (advanced transmission technologies) |
