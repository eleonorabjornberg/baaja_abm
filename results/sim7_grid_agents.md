# Simulation 7: grid access as an agent-based system

Interconnection is no longer a drawn study time. Each region's grid operator studies requests in clusters (ERCOT: one by one) at a throughput fitted to LBNL request-to-agreement times and adapting to the arrival rate; developers enter on the published wait and on their region's projected capacity shortfall, and leave at study results when the allocated network-upgrade cost exceeds their private value (both from LBNL cost data). Upgrade costs rise as capacity is signed and fall as transmission is built. Sec.2106 becomes published locations with a fixed fee and a single decision point in RTOs that change their process (drawn per RTO); Sec.2110 a throughput multiplier (0 by default: the bill does not size it); Sec.2109 extra hosting per transmission line built after the rule. Every scenario is paired with current law under the same agents. Numbers: mean [5th, 95th percentile] across 100 runs, GW online by Nov 2041.

## What the grid sections add (difference from current law, grid agents)

New capacity excludes relicensed hydro (existing plants kept in service), shown separately. 'BAAJA' draws each RTO's adoption of a new Sec.2106 process with probability 0.5, so its interval mostly reflects which RTOs adopt; the 'without Sec.2106' and 'adopted by every RTO' rows bound it. 'Without Sec.2106' keeps Sec.2109's extra hosting room and Titles I-II.

| scenario (grid agents) | renewable GW | gas GW | storage GW | new capacity GW | relicensed hydro GW (not new) | on-peak accredited GW 2035 | shortfall GW 2035 | shortfall GW 2041 |
|---|---|---|---|---|---|---|---|---|
| BAAJA | +25.3 [+8.4, +42.3] | +6.4 [+0.2, +14.2] | +4.8 [+1.4, +9.3] | +36.5 [+11.2, +60.5] | +1.8 [+1.2, +2.4] | +8.0 [+1.7, +13.3] | -4.9 [-9.7, -0.4] | -5.3 [-8.8, -1.9] |
| BAAJA without Sec.2106 | +4.9 [+3.6, +6.4] | +0.6 [+0.0, +1.3] | +1.0 [+0.5, +1.6] | +6.5 [+4.6, +8.3] | +1.8 [+1.2, +2.4] | +0.7 [+0.3, +1.1] | -0.2 [-0.5, -0.1] | -1.0 [-1.6, -0.4] |
| BAAJA without Sec.2109 hosting | +22.8 [+5.8, +39.8] | +6.1 [+0.0, +13.6] | +3.8 [+0.6, +7.9] | +32.7 [+7.7, +56.5] | +1.8 [+1.2, +2.4] | +7.9 [+1.5, +13.2] | -4.9 [-9.6, -0.3] | -4.7 [-8.2, -1.3] |
| Sec.2106 only | +19.8 [+2.7, +37.0] | +5.8 [-0.0, +12.9] | +3.7 [+0.4, +7.6] | +29.2 [+5.0, +53.4] | +0.0 [+0.0, +0.0] | +7.2 [+1.2, +12.1] | -4.7 [-9.3, -0.2] | -4.4 [-7.7, -0.9] |
| BAAJA, Sec.2106 adopted by every RTO | +44.5 [+38.7, +49.1] | +12.4 [+9.3, +15.8] | +8.2 [+5.7, +10.7] | +65.0 [+57.7, +71.1] | +1.8 [+1.2, +2.4] | +14.3 [+12.2, +17.0] | -9.0 [-11.6, -6.6] | -9.0 [-12.8, -5.9] |
| BAAJA + Sec.2110 throughput +25% | +37.3 [+24.2, +51.3] | +10.8 [+5.3, +16.6] | +9.4 [+7.0, +13.9] | +57.5 [+38.0, +76.2] | +1.8 [+1.2, +2.4] | +14.2 [+7.4, +20.2] | -6.4 [-10.8, -2.4] | -6.0 [-10.7, -2.3] |

## Timing: new capacity online, cumulative difference from current law

Sec.2106 and Sec.2110 apply from the rule month (ix_rule_month, central 36 months after enactment: an assumption; the statute gives FERC 18 months for the rule and providers 2 years to file), to requests made from then on; requests already in the queue keep the current process.

| year (to Nov) | current law: new GW online that year | BAAJA: cumulative GW vs current law | BAAJA without Sec.2106: cumulative GW vs current law | BAAJA, Sec.2106 adopted by every RTO: cumulative GW vs current law |
|---|---|---|---|---|
| 2028 | 90 | +0.0 [+0.0, +0.2] | +0.0 [+0.0, +0.2] | +0.0 [+0.0, +0.2] |
| 2030 | 109 | +0.3 [+0.0, +0.7] | +0.3 [+0.0, +0.7] | +0.3 [+0.0, +0.7] |
| 2032 | 55 | +0.6 [+0.1, +1.5] | +0.6 [+0.1, +1.5] | +0.6 [+0.1, +1.5] |
| 2033 | 62 | +2.9 [+0.9, +5.1] | +1.1 [+0.3, +2.0] | +4.6 [+3.1, +6.3] |
| 2035 | 56 | +19.0 [+5.1, +32.6] | +1.8 [+0.8, +2.8] | +34.0 [+30.7, +38.1] |
| 2038 | 53 | +29.2 [+8.8, +51.2] | +3.7 [+2.3, +5.3] | +53.3 [+47.8, +58.2] |
| 2041 | 50 | +36.5 [+11.2, +60.5] | +6.5 [+4.6, +8.3] | +65.0 [+57.7, +71.1] |

## Exogenous study times vs grid agents

Sims 1-6 draw each request's study time; here it comes out of the queue. The two current laws differ mainly through upgrade-cost growth with capacity signed (kappa: compare its low end, 0, in the sensitivity table) and through study results that remove projects whose upgrade costs exceed their value.

| grid model | current law new GW 2041 | BAAJA minus current law, new GW | renewable GW | gas GW | storage GW |
|---|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 1090 [1070, 1113] | +8.0 [+6.1, +9.6] | +6.6 [+4.7, +8.2] | +1.0 [+0.4, +1.6] | +0.3 [+0.1, +0.6] |
| grid agents (this simulation) | 972 [956, 987] | +36.5 [+11.2, +60.5] | +25.3 [+8.4, +42.3] | +6.4 [+0.2, +14.2] | +4.8 [+1.4, +9.3] |

### Current law: capacity shortfall below reference margins

With grid agents, developers respond to their region's projected shortfall, so surpluses and shortfalls are no longer fixed by the 2021-25 request mix, but fewer projects get through the queue overall.

| grid model | shortfall GW 2027 | shortfall GW 2035 | shortfall GW 2041 | regions below reference margin, 2035 |
|---|---|---|---|---|
| exogenous study times (Sims 1-6) | 9 [9, 10] | 59 [55, 62] | 107 [103, 111] | 3.4 [2.0, 4.0] |
| grid agents (this simulation) | 9 [9, 10] | 68 [65, 71] | 112 [109, 116] | 3.8 [3.0, 4.0] |

| region | reserve margin 2035: exogenous / agents | shortfall GW 2035: exogenous / agents |
|---|---|---|
| CAISO | 12% / 8% | 4.6 / 7.0 |
| ERCOT | 66% / 55% | 0.0 / 0.0 |
| ISO-NE | 12% / 12% | 0.4 / 0.4 |
| MISO | 8% / 6% | 1.2 / 4.4 |
| NYISO | 23% / 19% | 0.0 / 0.0 |
| PJM | 9% / 7% | 52.8 / 56.4 |
| SPP | 30% / 26% | 0.0 / 0.0 |
| Southeast | 29% / 27% | 0.0 / 0.0 |
| West | 40% / 29% | 0.0 / 0.0 |

## By region (requests made in the first five model years, Nov 2026 to Oct 2031; mean across runs)

| region | law: requests/yr | law: months to agreement | law: share signed | law: withdrawn at results | law: GW online 2041 | BAAJA: requests/yr | BAAJA: months | BAAJA: share signed | BAAJA: GW | 2106 everywhere: GW |
|---|---|---|---|---|---|---|---|---|---|---|
| CAISO | 173 | 37 | 0.11 | 0.25 | 40 | -11 | -2.6 | +0.011 | +1.7 | +2.7 |
| ERCOT | 504 | 26 | 0.18 | 0.63 | 208 | +0 | +0.0 | +0.000 | +0.5 | +0.5 |
| ISO-NE | 117 | 30 | 0.15 | 0.48 | 22 | -6 | -2.4 | +0.016 | +2.2 | +4.0 |
| MISO | 572 | 31 | 0.08 | 0.55 | 157 | -26 | -3.1 | +0.012 | +20.2 | +39.1 |
| NYISO | 232 | 30 | 0.07 | 0.48 | 28 | -13 | -2.8 | +0.008 | +2.6 | +4.4 |
| PJM | 446 | 30 | 0.13 | 0.52 | 129 | -26 | -2.8 | +0.009 | +4.6 | +7.6 |
| SPP | 231 | 32 | 0.08 | 0.78 | 61 | -12 | -2.7 | +0.005 | +2.6 | +4.6 |
| Southeast | 408 | 30 | 0.16 | 0.30 | 140 | +0 | -0.0 | +0.000 | +0.5 | +0.5 |
| West | 686 | 39 | 0.13 | 0.63 | 187 | +0 | -0.0 | +0.001 | +1.7 | +1.7 |

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
| ERCOT | 0.10 / 0.10 | 0.17 / 0.17 | 0.26 / 0.24 | 0.42 / 0.35 |
| ISO-NE | 0.29 / 0.29 | 0.41 / 0.40 | 0.51 / 0.50 | 0.63 / 0.59 |
| MISO | 0.16 / 0.16 | 0.39 / 0.43 | 0.57 / 0.56 | 0.75 / 0.62 |
| NYISO | 0.40 / 0.39 | 0.51 / 0.52 | 0.61 / 0.59 | 0.74 / 0.69 |
| PJM | 0.30 / 0.30 | 0.39 / 0.42 | 0.48 / 0.48 | 0.62 / 0.59 |
| SPP | 0.14 / 0.14 | 0.27 / 0.23 | 0.60 / 0.27 | 0.86 / 0.58 |
| Southeast | 0.47 / 0.46 | 0.56 / 0.58 | 0.63 / 0.61 | 0.72 / 0.71 |
| West | 0.09 / 0.09 | 0.20 / 0.24 | 0.39 / 0.42 | 0.69 / 0.68 |

| region | background withdrawal hazard, %/month: first 12 months | after 12 months, to construction | mean hold after an adverse study result, months |
|---|---|---|---|
| CAISO | 7.01 | 0.78 | 240 |
| ERCOT | 0.81 | 0.59 | 102 |
| ISO-NE | 2.80 | 1.43 | 240 |
| MISO | 1.43 | 2.65 | 240 |
| NYISO | 4.18 | 1.42 | 148 |
| PJM | 2.94 | 0.75 | 95 |
| SPP | 1.21 | 0.08 | 16 |
| Southeast | 5.12 | 1.25 | 93 |
| West | 0.81 | 1.02 | 34 |

### Developers: value relative to LBNL's P(complete | cost) fit

One scale per technology and region, fitted so completion of new requests matches the regional LBNL targets. Values below 1 mean fewer requests complete than LBNL's cost-completion relation alone implies.

| technology | region | value scale (fitted to completion) |
|---|---|---|
| Gas | all (pooled) | 2.55 |
| Gas | ERCOT | 0.39 |
| Gas | MISO | 6.00 |
| Gas | SPP | 0.75 |
| Gas | Southeast | 148.37 |
| Gas | West | 4.36 |
| Geothermal | all (pooled) | 5.91 |
| Geothermal | West | 2.46 |
| Offshore wind | all (pooled) | 0.01 |
| Onshore wind | all (pooled) | 1.06 |
| Onshore wind | ERCOT | 0.14 |
| Onshore wind | MISO | 0.89 |
| Onshore wind | NYISO | 3.02 |
| Onshore wind | SPP | 0.30 |
| Onshore wind | West | 1.61 |
| Solar | CAISO | 0.84 |
| Solar | ERCOT | 0.06 |
| Solar | ISO-NE | 3.10 |
| Solar | MISO | 0.33 |
| Solar | NYISO | 0.50 |
| Solar | PJM | 0.25 |
| Solar | SPP | 0.03 |
| Solar | Southeast | 6.08 |
| Solar | West | 1.56 |
| Storage | CAISO | 0.56 |
| Storage | ERCOT | 0.01 |
| Storage | ISO-NE | 0.62 |
| Storage | MISO | 0.05 |
| Storage | NYISO | 0.12 |
| Storage | PJM | 0.06 |
| Storage | SPP | 0.01 |
| Storage | Southeast | 148.37 |
| Storage | West | 3.55 |

### Time from request to operation, completed projects

Known gap: in the agents model, waiting longer does not make a request more likely to withdraw (the background hazard is small and fitted to withdrawal timing), so completed projects are not selected for short waits as in the data and their median time to operation is longer than LBNL's. This lowers current-law GW by 2041 relative to the exogenous model; the bill's effect is a paired difference under the same agents.

| technology | LBNL median months request -> operation (completed) | exogenous grid (model) | grid agents (model) |
|---|---|---|---|
| Solar | 62 | 62 | 64 |
| Onshore wind | 52 | 52 | 65 |
| Gas | 37 | 38 | 48 |
| Storage | - | 40 | 62 |

### Developers: completion by allocated network-upgrade cost (ISO regions)

LBNL counts requests resolved by 2024 (completed vs withdrawn); the model counts every 2026-41 request that received a study result, so the level differs; the gradient is the check.

| allocated cost $/kW | model: share completing | LBNL: share completing (resolved requests) | LBNL n |
|---|---|---|---|
| 0-10 | 0.30 | 0.80 | 426 |
| 10-50 | 0.17 | 0.67 | 476 |
| 50-100 | 0.11 | 0.59 | 365 |
| 100-200 | 0.08 | 0.42 | 297 |
| 200-400 | 0.04 | 0.18 | 225 |
| 400+ | 0.02 | 0.07 | 306 |

## Sensitivity: grid assumptions at the low and high end of their ranges (20 paired runs each)

kappa's low end is 0 (upgrade cost does not rise with capacity signed): it shows how much of the gap between the agents' current law and the exogenous model comes from cost growth.

| assumption | low / high | BAAJA minus current law, new GW | current law new GW | what it is |
|---|---|---|---|---|
| entry_wait_elast (current law) | 0.0 / 1.0 | +27.3 / +29.8 | 971 / 983 | elasticity of new requests to the published wait for a study result |
| scarcity_beta (current law) | 0.0 / 3.0 | +30.6 / +24.1 | 976 / 973 | developer value and entry rise by exp(beta x change in the region's projected capacity shortfall as a share of peak demand, 4 years ahead) |
| kappa (current law) | 0.0 / 5.14 | +35.0 / +25.4 | 1060 / 900 | growth of network-upgrade cost with capacity signed, per share of the regional fleet [D: LBNL cost data, 2018+ vs 2010-17 requests; central = median of MISO, SPP, PJM, high = PJM, low = 0; not ERCOT] |
| restudy_rho (current law) | 0.0 / 0.6 | +28.3 / +34.0 | 978 / 951 | re-study: cost change for remaining requests per unit withdrawn MW share [D: SPP, slope of cluster cost ratio on withdrawn share through the origin, 0.11, s.e. about 0.8; zero not excluded] |
| restudy_mu (current law) | -0.4 / 0.0 | +25.9 / +30.4 | 989 / 968 | re-study: median log change in a remaining request's upgrade cost [D: SPP, Phase 2 to latest posting, -0.08; low = mean among changed, -0.39; high 0: requests whose cost rose most may have left] |
| restudy_sd (current law) | 0.3 / 1.0 | +26.6 / +32.4 | 988 / 956 | re-study: spread (s.d. of log change) of a remaining request's upgrade cost [D: SPP, interquartile range / 1.349 = 0.62; low = one posting step, 0.31; high = s.d., 0.97] |
| restudy_months (current law) | 10 / 29 | +26.2 / +29.7 | 973 / 973 | months from first complete study result to agreement in cluster regions [D: SPP, Phase 2 to latest restudy posting, median of 8 clusters 16.8, range 10.5-28.7] |
| tx_hosting_gw (current law) | 0.5 / 3.0 | +23.4 / +37.8 | 956 / 1002 | GW of interconnection room added by one transmission project |
| adopt_2106 (bill) | 0.0 / 1.0 | +7.0 / +66.2 | 973 / 973 | Sec.2106(d): probability that an RTO's process changes rather than being found compliant, drawn per RTO [A; check: under Order No. 2023 FERC let every RTO keep its existing cluster process through variations and accepted all five filings in part, so outcomes were alike across RTOs; independence per RTO understates that] |
| planned_share_2106 (bill) | 0.25 / 0.9 | +28.3 / +30.7 | 973 / 973 | Sec.2106(a)(2): share of requests able to use a published location |
| screen_2106 (bill) | 0.1 / 0.5 | +32.6 / +15.0 | 973 / 973 | Sec.2106(a)(3): share of requests that non-refundable security and withdrawal penalties keep out, those least likely to complete within their technology and region [A; check: LBNL 12-month withdrawal shares of 2015-19 requests in FERC RTOs run 0.14 (SPP) to 0.58 (CAISO), median about 0.29; Johnston, Liu and Yang find deposits deter mainly such quick leavers] |
| lag_2106 (bill) | 0.0 / 1.0 | +29.3 / +29.3 | 973 / 973 | Sec.2106(a)(3): months a developer holds its queue position after an adverse study result, relative to current law, with a single decision point and withdrawal penalties (0 = leaves at once) |
| fee_mult_2106 (bill) | 0.8 / 1.5 | +30.3 / +27.9 | 973 / 973 | Sec.2106(a)(2): fixed fee as a multiple of the region's expected (mean) upgrade cost, zero-cost requests included; 1 = the fee recovers expected upgrade cost |
| g_2110 (bill) | 0.0 / 0.25 | +29.3 / +53.0 | 973 / 973 | Sec.2110: study throughput gain (rulemaking with no target) |
| hosting_2109 (bill) | 0.0 / 0.3 | +25.5 / +37.1 | 973 / 973 | Sec.2109: extra hosting room per transmission project (advanced transmission technologies) |

### Current law with an entry screen

Sec.2106(a)(3)'s non-refundable security and withdrawal penalties are modelled as an entry screen: in an RTO that changes its process, the share screen_2106 (central 0.25) of new requests least likely to complete, ranked within their technology and region, do not enter. Order 2023 already requires readiness deposits and withdrawal penalties; the second row screens out a 0.1 share in both runs, to show how much of Sec.2106's screening effect is already in place. The third row is the previous specification, an absolute threshold (enter only if the chance that upgrade cost comes in below value is at least 0.25). It was replaced after the recalibration because that chance is in units the calibration moves: where a fitted value scale sits at its lower bound, almost no request passes.

| entry screens | current law new GW | BAAJA minus current law | every RTO adopts Sec.2106 |
|---|---|---|---|
| current law: none; Sec.2106: relative 0.25 (central) | 973 | +29.3 | +66.2 |
| current law: 0.1 share screened (Order 2023 deposits) | 972 | +30.7 | +68.0 |
| Sec.2106: absolute screen at 0.25 (previous specification) | 973 | +17.0 | +41.8 |

## Planned transmission under current law

Regional portfolios approved by 2025 (MISO LRTP Tranches 1 and 2.1, SPP 2025 ITP, PJM 2025 RTEP 500 kV and above; data/planned_tx.json) add hosting room in both runs from their in-service years, converted to transmission project-equivalents at the average cost of a Tranche 1 project. The second row leaves them out.

| planned transmission | current law new GW | BAAJA minus current law | every RTO adopts Sec.2106 |
|---|---|---|---|
| approved portfolios in both runs (central) | 973 | +29.3 | +66.2 |
| left out | 948 | +24.7 | +55.2 |
