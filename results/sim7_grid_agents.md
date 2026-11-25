# Simulation 7: grid access as an agent-based system

Interconnection is no longer a drawn study time. Each region's grid operator studies requests in clusters (ERCOT: one by one) at a throughput fitted to LBNL request-to-agreement times and adapting to the arrival rate; developers enter on the published wait and on their region's projected capacity shortfall, and leave at study results when the allocated network-upgrade cost exceeds their private value (both from LBNL cost data). Upgrade costs rise as capacity is signed and fall as transmission is built. Sec.2106 becomes published locations with a fixed fee and a single decision point in RTOs that change their process (drawn per RTO); Sec.2110 a throughput multiplier (0 by default: the bill does not size it); Sec.2109 extra hosting per transmission line built after the rule. Every scenario is paired with current law under the same agents. Numbers: mean [5th, 95th percentile] across 100 runs, GW online by Nov 2041.

## What the grid sections add (difference from current law, grid agents)

New capacity excludes relicensed hydro (existing plants kept in service), shown separately. 'BAAJA' draws each RTO's adoption of a new Sec.2106 process with probability 0.5, so its interval mostly reflects which RTOs adopt; the 'without Sec.2106' and 'adopted by every RTO' rows bound it. 'Without Sec.2106' keeps Sec.2109's extra hosting room and Titles I-II.

| scenario (grid agents) | renewable GW | gas GW | storage GW | new capacity GW | relicensed hydro GW (not new) | on-peak accredited GW 2035 | shortfall GW 2035 | shortfall GW 2041 |
|---|---|---|---|---|---|---|---|---|
| BAAJA | -6.4 [-16.8, +4.1] | +3.5 [-0.7, +8.9] | -5.1 [-8.6, -0.7] | -8.0 [-19.2, +3.4] | +1.8 [+1.2, +2.4] | +2.4 [+0.4, +4.8] | -1.7 [-3.8, -0.1] | +3.7 [-1.3, +9.0] |
| BAAJA without Sec.2106 | +4.9 [+3.3, +7.0] | +0.6 [+0.0, +1.1] | +0.7 [+0.2, +1.1] | +6.2 [+4.5, +8.2] | +1.8 [+1.2, +2.4] | +0.7 [+0.3, +1.1] | -0.3 [-0.5, -0.0] | -1.0 [-1.8, -0.4] |
| BAAJA without Sec.2109 hosting | -8.6 [-19.0, +1.9] | +3.0 [-0.9, +8.4] | -5.6 [-9.2, -1.0] | -11.1 [-22.6, +0.1] | +1.8 [+1.2, +2.4] | +2.3 [+0.3, +4.6] | -1.6 [-3.8, -0.1] | +4.2 [-0.8, +9.1] |
| Sec.2106 only | -11.5 [-21.7, -1.2] | +2.8 [-1.3, +8.0] | -5.7 [-9.3, -1.0] | -14.4 [-25.7, -2.6] | +0.0 [+0.0, +0.0] | +1.6 [-0.3, +3.9] | -1.4 [-3.6, +0.0] | +4.7 [-0.4, +9.4] |
| BAAJA, Sec.2106 adopted by every RTO | -15.5 [-20.9, -9.8] | +6.6 [+3.3, +9.3] | -10.2 [-13.3, -7.9] | -19.1 [-25.7, -12.0] | +1.8 [+1.2, +2.4] | +4.0 [+2.0, +5.8] | -3.0 [-4.7, -1.8] | +7.2 [+4.0, +10.1] |
| BAAJA + Sec.2110 throughput +25% | +5.3 [-8.8, +19.9] | +7.7 [+3.8, +12.4] | -0.4 [-5.0, +4.7] | +12.7 [-4.9, +29.9] | +1.8 [+1.2, +2.4] | +7.9 [+5.8, +10.6] | -3.8 [-6.0, -2.1] | +3.0 [-2.2, +8.2] |

## Timing: new capacity online, cumulative difference from current law

Sec.2106 and Sec.2110 apply from the rule month (ix_rule_month, central 36 months after enactment: an assumption; the statute gives FERC 18 months for the rule and providers 2 years to file), to requests made from then on; requests already in the queue keep the current process.

| year (to Nov) | current law: new GW online that year | BAAJA: cumulative GW vs current law | BAAJA without Sec.2106: cumulative GW vs current law | BAAJA, Sec.2106 adopted by every RTO: cumulative GW vs current law |
|---|---|---|---|---|
| 2028 | 90 | +0.0 [+0.0, +0.2] | +0.0 [+0.0, +0.2] | +0.0 [+0.0, +0.2] |
| 2030 | 107 | +0.2 [+0.0, +0.7] | +0.2 [+0.0, +0.7] | +0.2 [+0.0, +0.7] |
| 2032 | 56 | +0.7 [+0.2, +1.5] | +0.7 [+0.2, +1.5] | +0.7 [+0.2, +1.5] |
| 2033 | 64 | +1.5 [+0.4, +2.9] | +1.1 [+0.5, +2.0] | +1.9 [+0.7, +4.1] |
| 2035 | 57 | +3.9 [+1.3, +7.5] | +1.9 [+0.9, +3.0] | +5.6 [+2.7, +10.1] |
| 2038 | 54 | -1.3 [-8.7, +4.2] | +3.7 [+2.4, +5.5] | -5.0 [-10.8, +0.5] |
| 2041 | 52 | -8.0 [-19.2, +3.4] | +6.2 [+4.5, +8.2] | -19.1 [-25.7, -12.0] |

## Exogenous study times vs grid agents

Sims 1-6 draw each request's study time; here it comes out of the queue. The two current laws differ mainly through upgrade-cost growth with capacity signed (kappa: compare its low end, 0, in the sensitivity table) and through study results that remove projects whose upgrade costs exceed their value.

| grid model | current law new GW 2041 | BAAJA minus current law, new GW | renewable GW | gas GW | storage GW |
|---|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 1090 [1070, 1113] | +8.0 [+6.1, +9.6] | +6.6 [+4.7, +8.2] | +1.0 [+0.4, +1.6] | +0.3 [+0.1, +0.6] |
| grid agents (this simulation) | 983 [964, 1004] | -8.0 [-19.2, +3.4] | -6.4 [-16.8, +4.1] | +3.5 [-0.7, +8.9] | -5.1 [-8.6, -0.7] |

### Current law: capacity shortfall below reference margins

With grid agents, developers respond to their region's projected shortfall, so surpluses and shortfalls are no longer fixed by the 2021-25 request mix, but fewer projects get through the queue overall.

| grid model | shortfall GW 2027 | shortfall GW 2035 | shortfall GW 2041 | regions below reference margin, 2035 |
|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 9 [9, 10] | 59 [55, 62] | 107 [103, 111] | 3.4 [2.0, 4.0] |
| grid agents (this simulation) | 9 [9, 10] | 70 [66, 74] | 115 [110, 118] | 3.8 [3.0, 4.0] |

| region | reserve margin 2035: exogenous / agents | shortfall GW 2035: exogenous / agents |
|---|---|---|
| CAISO | 12% / 8% | 4.6 / 7.4 |
| ERCOT | 66% / 56% | 0.0 / 0.0 |
| ISO-NE | 12% / 12% | 0.4 / 0.5 |
| MISO | 8% / 5% | 1.2 / 4.9 |
| NYISO | 23% / 20% | 0.0 / 0.0 |
| PJM | 9% / 6% | 52.8 / 57.2 |
| SPP | 30% / 27% | 0.0 / 0.0 |
| Southeast | 29% / 27% | 0.0 / 0.0 |
| West | 40% / 30% | 0.0 / 0.0 |

## By region (requests made in the first five model years, Nov 2026 to Oct 2031; mean across runs)

| region | law: requests/yr | law: months to agreement | law: share signed | law: withdrawn at results | law: GW online 2041 | BAAJA: requests/yr | BAAJA: months | BAAJA: share signed | BAAJA: GW | 2106 everywhere: GW |
|---|---|---|---|---|---|---|---|---|---|---|
| CAISO | 174 | 38 | 0.10 | 0.24 | 39 | -11 | -1.3 | +0.000 | -1.2 | -2.3 |
| ERCOT | 504 | 26 | 0.19 | 0.62 | 214 | +0 | +0.0 | +0.000 | +0.5 | +0.5 |
| ISO-NE | 117 | 30 | 0.15 | 0.46 | 23 | -6 | -1.0 | -0.000 | -1.2 | -2.6 |
| MISO | 574 | 31 | 0.09 | 0.49 | 157 | -27 | -1.0 | -0.001 | +1.8 | +1.8 |
| NYISO | 232 | 30 | 0.07 | 0.45 | 30 | -13 | -1.0 | -0.003 | -2.1 | -4.1 |
| PJM | 447 | 30 | 0.13 | 0.50 | 125 | -26 | -1.4 | -0.001 | -4.9 | -9.0 |
| SPP | 231 | 32 | 0.08 | 0.76 | 62 | -12 | -1.1 | -0.001 | -2.6 | -4.9 |
| Southeast | 408 | 30 | 0.16 | 0.28 | 140 | +0 | +0.0 | +0.000 | +0.5 | +0.5 |
| West | 689 | 37 | 0.13 | 0.57 | 194 | +0 | +0.0 | +0.000 | +1.1 | +1.1 |

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

### Developers: share of requests withdrawn by months after request (2015-19 cohorts vs model requests of Nov 2026 to Oct 2031)

Withdrawal is fitted in the 2010-25 backcast, where model and data cohorts are the same requests (Phase 3; results/backcast.md): a first-year hazard, a later hazard and a hold after an adverse study result, by region, to LBNL's 12-, 36- and 60-month shares; 24 months is a check. This table shows the forward cohorts of the first five model years under current law next to the 2015-19 data for comparison only: the queue they face is different, so they need not match. In CAISO, ISO-NE and MISO the fitted hold reaches its 20-year bound: developers with an adverse result stay in the queue past 2025, and the data cannot tell a long hold from never withdrawing. Sec.2106(a)(3)'s single decision point and withdrawal penalties shorten the hold (lag_2106).

| region | withdrawn by 12 months: model / data | withdrawn by 24 months: model / data | withdrawn by 36 months: model / data | withdrawn by 60 months: model / data |
|---|---|---|---|---|
| CAISO | 0.58 / 0.58 | 0.62 / 0.60 | 0.66 / 0.65 | 0.72 / 0.69 |
| ERCOT | 0.10 / 0.10 | 0.17 / 0.17 | 0.25 / 0.24 | 0.41 / 0.35 |
| ISO-NE | 0.29 / 0.29 | 0.41 / 0.40 | 0.51 / 0.50 | 0.63 / 0.59 |
| MISO | 0.16 / 0.16 | 0.39 / 0.43 | 0.57 / 0.56 | 0.75 / 0.62 |
| NYISO | 0.40 / 0.39 | 0.50 / 0.52 | 0.60 / 0.59 | 0.72 / 0.69 |
| PJM | 0.30 / 0.30 | 0.38 / 0.42 | 0.48 / 0.48 | 0.62 / 0.59 |
| SPP | 0.14 / 0.14 | 0.20 / 0.23 | 0.56 / 0.27 | 0.86 / 0.58 |
| Southeast | 0.47 / 0.46 | 0.55 / 0.58 | 0.63 / 0.61 | 0.72 / 0.71 |
| West | 0.09 / 0.09 | 0.22 / 0.24 | 0.39 / 0.42 | 0.68 / 0.68 |

| region | background withdrawal hazard, %/month: first 12 months | after 12 months, to construction | mean hold after an adverse study result, months |
|---|---|---|---|
| CAISO | 7.01 | 0.80 | 240 |
| ERCOT | 0.82 | 0.58 | 103 |
| ISO-NE | 2.80 | 1.44 | 240 |
| MISO | 1.43 | 2.68 | 240 |
| NYISO | 4.18 | 1.50 | 227 |
| PJM | 2.94 | 0.87 | 101 |
| SPP | 1.21 | 0.14 | 14 |
| Southeast | 5.12 | 1.32 | 109 |
| West | 0.81 | 1.28 | 38 |

### Developers: value relative to LBNL's P(complete | cost) fit

One scale per technology and region, fitted so completion of new requests matches the regional LBNL targets. Values below 1 mean fewer requests complete than LBNL's cost-completion relation alone implies.

| technology | region | value scale (fitted to completion) |
|---|---|---|
| Gas | all (pooled) | 1.02 |
| Gas | ERCOT | 0.31 |
| Gas | MISO | 2.17 |
| Gas | SPP | 0.37 |
| Gas | Southeast | 148.37 |
| Gas | West | 2.83 |
| Geothermal | all (pooled) | 6.69 |
| Geothermal | West | 2.01 |
| Offshore wind | all (pooled) | 0.01 |
| Onshore wind | all (pooled) | 0.44 |
| Onshore wind | ERCOT | 0.12 |
| Onshore wind | MISO | 0.33 |
| Onshore wind | NYISO | 1.19 |
| Onshore wind | SPP | 0.16 |
| Onshore wind | West | 0.94 |
| Solar | CAISO | 0.31 |
| Solar | ERCOT | 0.05 |
| Solar | ISO-NE | 1.30 |
| Solar | MISO | 0.09 |
| Solar | NYISO | 0.18 |
| Solar | PJM | 0.07 |
| Solar | SPP | 0.01 |
| Solar | Southeast | 3.72 |
| Solar | West | 0.86 |
| Storage | CAISO | 0.18 |
| Storage | ERCOT | 0.01 |
| Storage | ISO-NE | 0.19 |
| Storage | MISO | 0.01 |
| Storage | NYISO | 0.03 |
| Storage | PJM | 0.01 |
| Storage | SPP | 0.01 |
| Storage | Southeast | 148.37 |
| Storage | West | 2.07 |

### Time from request to operation, completed projects

Known gap: in the agents model, waiting longer does not make a request more likely to withdraw (the background hazard is small and fitted to withdrawal timing), so completed projects are not selected for short waits as in the data and their median time to operation is longer than LBNL's. This lowers current-law GW by 2041 relative to the exogenous model; the bill's effect is a paired difference under the same agents.

| technology | LBNL median months request -> operation (completed) | exogenous grid (model) | grid agents (model) |
|---|---|---|---|
| Solar | 62 | 62 | 64 |
| Onshore wind | 52 | 52 | 64 |
| Gas | 37 | 38 | 48 |
| Storage | - | 40 | 61 |

### Developers: completion by allocated network-upgrade cost (ISO regions)

LBNL counts requests resolved by 2024 (completed vs withdrawn); the model counts every 2026-41 request that received a study result, so the level differs; the gradient is the check.

| allocated cost $/kW | model: share completing | LBNL: share completing (resolved requests) | LBNL n |
|---|---|---|---|
| 0-10 | 0.38 | 0.80 | 426 |
| 10-50 | 0.13 | 0.67 | 476 |
| 50-100 | 0.06 | 0.59 | 365 |
| 100-200 | 0.04 | 0.42 | 297 |
| 200-400 | 0.02 | 0.18 | 225 |
| 400+ | 0.01 | 0.07 | 306 |

## Sensitivity: grid assumptions at the low and high end of their ranges (20 paired runs each)

kappa's low end is 0 (upgrade cost does not rise with capacity signed): it shows how much of the gap between the agents' current law and the exogenous model comes from cost growth.

| assumption | low / high | BAAJA minus current law, new GW | current law new GW | what it is |
|---|---|---|---|---|
| entry_wait_elast (current law) | 0.0 / 1.0 | -8.5 / -4.6 | 983 / 995 | elasticity of new requests to the published wait for a study result |
| scarcity_beta (current law) | 0.0 / 3.0 | -6.1 / -9.6 | 988 / 988 | developer value and entry rise by exp(beta x change in the region's projected capacity shortfall as a share of peak demand, 4 years ahead) |
| kappa (current law) | 0.0 / 5.14 | -10.6 / -2.3 | 1065 / 916 | growth of network-upgrade cost with capacity signed, per share of the regional fleet [D: LBNL cost data, 2018+ vs 2010-17 requests; central = median of MISO, SPP, PJM, high = PJM, low = 0; not ERCOT] |
| restudy_rho (current law) | 0.0 / 0.6 | -7.7 / -3.3 | 990 / 966 | re-study: cost change for remaining requests per unit withdrawn MW share above SPP's median (0.45), on top of SPP's request-level changes [D: SPP, slope of cluster cost ratio on withdrawn share through the origin, 0.11, s.e. about 0.8; zero not excluded] |
| restudy_scale (current law) | 0.5 / 1.5 | +5.7 / -18.4 | 927 / 1036 | re-study: scale on the request-level log change in upgrade cost, drawn from SPP's changes from Phase 2 to the latest posting [D: data/spp_restudy.json, 325 requests; median -0.17, 10th and 90th percentiles -2.85 and +0.51] |
| restudy_months (current law) | 8 / 29 | -8.5 / -6.9 | 988 / 986 | months from the first complete study result to the agreement in cluster regions under the current process [D: SPP, Phase 2 to the latest restudy posting, censored, median of 8 clusters 16.8, high 28.7 (SPP's active-queue file gives no agreement dates); low 8 = Order No. 2023's pro forma 150-day cluster restudy plus 90-day facilities study] |
| tx_hosting_gw (current law) | 0.5 / 3.0 | -9.9 / -0.7 | 975 / 1005 | GW of interconnection room added by one transmission project |
| adopt_2106 (bill) | 0.0 / 1.0 | +6.5 / -19.0 | 986 / 986 | Sec.2106(d): probability that an RTO's process changes rather than being found compliant, drawn per RTO [A; check: under Order No. 2023 FERC let every RTO keep its existing cluster process through variations and accepted all five filings in part, so outcomes were alike across RTOs; independence per RTO understates that] |
| planned_share_2106 (bill) | 0.25 / 0.9 | -7.5 / -6.4 | 986 / 986 | Sec.2106(a)(2): share of requests able to use a published location |
| screen_2106 (bill) | 0.1 / 0.5 | -5.4 / -17.2 | 986 / 986 | Sec.2106(a)(3): share of requests that non-refundable security and withdrawal penalties keep out, those least likely to complete within their technology and region [A; check: LBNL 12-month withdrawal shares of 2015-19 requests in FERC RTOs run 0.14 (SPP) to 0.58 (CAISO), median about 0.3; Johnston, Liu and Yang find deposits deter mainly such quick leavers] |
| lag_2106 (bill) | 0.0 / 1.0 | -7.1 / -7.1 | 986 / 986 | Sec.2106(a)(3): months a developer holds its queue position after an adverse study result, relative to current law, with a single decision point and withdrawal penalties (0 = leaves at once) |
| fee_mult_2106 (bill) | 0.8 / 1.5 | -6.6 / -7.5 | 986 / 986 | Sec.2106(a)(2): fixed fee as a multiple of the region's expected (mean) upgrade cost, zero-cost requests included; 1 = the fee recovers expected upgrade cost |
| g_2110 (bill) | 0.0 / 0.25 | -7.1 / +17.3 | 986 / 986 | Sec.2110: study throughput gain (rulemaking with no target) |
| hosting_2109 (bill) | 0.0 / 0.3 | -10.1 / -0.6 | 986 / 986 | Sec.2109: extra hosting room per transmission project (advanced transmission technologies) |

### Current law with an entry screen

Sec.2106(a)(3)'s non-refundable security and withdrawal penalties are modelled as an entry screen: in an RTO that changes its process, the share screen_2106 (central 0.25) of new requests least likely to complete, ranked within their technology and region, do not enter (requests that fail at any cost rank lowest, the rest by private value). Order 2023 already requires readiness deposits and withdrawal penalties; the second row screens out a 0.1 share in both runs, to show how much of Sec.2106's screening effect is already in place. The third row is the previous specification, an absolute threshold (enter only if the chance that upgrade cost comes in below value is at least 0.25). It was replaced after the recalibration because that chance is in units the calibration moves: where a fitted value scale sits at its lower bound, almost no request passes.

| entry screens | current law new GW | BAAJA minus current law | every RTO adopts Sec.2106 |
|---|---|---|---|
| current law: none; Sec.2106: relative 0.25 (central) | 986 | -7.1 | -19.0 |
| current law: 0.1 share screened (Order 2023 deposits) | 995 | -8.2 | -22.6 |
| Sec.2106: absolute screen at 0.25 (previous specification) | 986 | -30.9 | -68.0 |

## Planned transmission under current law

MISO's LRTP Tranches 1 and 2.1 (data/planned_tx.json) add hosting room in both runs from July of their in-service years, converted to transmission project-equivalents at the average cost of a Tranche 1 project. They are a step above MISO's historical pace. SPP's 2025 ITP and PJM's 2025 RTEP (500 kV and above) are counted only in the second row, because upgrade-cost growth (kappa) is fitted to the cost of 2018 and later requests against 2010-17 requests, per GW reaching operation in 2014-21, which already includes recurring regional expansion. The third row leaves approved transmission out.

| approved transmission (both runs) | current law new GW | BAAJA minus current law | every RTO adopts Sec.2106 |
|---|---|---|---|
| MISO LRTP Tranches 1 and 2.1 (central) | 986 | -7.1 | -19.0 |
| with SPP's 2025 ITP and PJM's 2025 RTEP | 993 | -6.3 | -18.5 |
| left out | 969 | -9.1 | -23.8 |
