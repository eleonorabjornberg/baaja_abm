# Where the Sec.2106 gain comes from (grid agents)

Mean [5th, 95th percentile] across 100 paired runs; every case is paired with current law under the same seeds, political draws and assumption changes. New capacity excludes relicensed hydro. GW online by Nov 2041.

## A. Sec.2106 by component

The single decision point removes the current-law re-study round (withdrawals raise the cost of those who stay, restudy_rho, and add restudy_months before agreement). Published locations add a share of requests at sites the provider has studied, at a fixed fee. The entry screen keeps out the requests least likely to complete.

| case (every RTO adopts unless p=0.5) | BAAJA minus current law, new GW | of which Sec.2106 | RTO regions, GW |
|---|---|---|---|
| without Sec.2106 | +6.7 [+5.0, +8.8] |  | +3.5 [+2.1, +5.1] |
| single decision point only | +41.7 [+37.3, +46.4] | +35.0 | +38.5 [+34.8, +42.5] |
| + published locations (no screen) | +44.2 [+39.9, +48.8] | +37.5 | +41.0 [+36.5, +45.2] |
| + relative screen (central) | +37.0 [+32.0, +42.8] | +30.3 | +33.7 [+28.4, +38.8] |
| + absolute screen instead | -4.4 [-11.4, +1.0] | -11.1 | -7.6 [-13.7, -2.2] |
| relative screen, no published locations | +34.3 [+29.5, +39.6] | +27.6 | +31.0 [+26.3, +35.8] |
| p=0.5: no screen | +26.5 [+11.6, +42.0] | +19.8 | +23.2 [+8.7, +38.4] |
| p=0.5: relative screen (central) | +21.9 [+7.5, +37.2] | +15.2 | +18.7 [+4.5, +34.0] |
| p=0.5: absolute screen | -0.1 [-17.7, +18.8] | -6.9 | -3.4 [-20.6, +15.5] |
| Titles I-II only (no Sec.2106, no Sec.2109) | +2.9 [+1.6, +4.5] | -3.8 | +1.5 [+0.3, +3.0] |
| p=0.5 without Sec.2109 | +17.8 [+3.4, +33.0] | +11.1 | +16.3 [+2.0, +31.2] |

## B. The current-law re-study round

Both current law and the bill change. With no re-study penalty under current law, Sec.2106's single decision point has little to remove.

| current-law re-study round (law and bill) | current law new GW | without Sec.2106 | single decision point only | every RTO, full Sec.2106 | p=0.5, full Sec.2106 |
|---|---|---|---|---|---|
| central (rho 0.3, 6 months) | 954 | +6.7 | +41.7 | +37.0 | +21.9 |
| rho=0 | 988 | +7.2 | +27.7 | +22.9 | +14.8 |
| months=1 | 955 | +6.7 | +24.2 | +21.7 | +13.9 |
| rho=0, months=1 | 988 | +7.2 | +10.2 | +7.7 | +6.7 |
| months=0 | 988 | +7.2 | +7.2 | +4.6 | +5.1 |

## By region: the entry screen

| region (every RTO adopts) | no screen | relative screen | screen effect | absolute screen | throughput / arrivals | zero-cost share | cost spread (sigma) |
|---|---|---|---|---|---|---|---|
| CAISO | +2.5 | +1.4 | -1.1 | -0.1 | 1.85 | 0.080 | 1.35 |
| ISO-NE | +2.8 | +2.4 | -0.5 | +0.6 | 0.68 | 0.011 | 1.39 |
| MISO | +18.3 | +23.5 | +5.3 | +12.7 | 0.59 | 0.025 | 1.21 |
| NYISO | +4.0 | +3.0 | -1.0 | -0.7 | 0.56 | 0.031 | 1.04 |
| PJM | +9.0 | +0.7 | -8.3 | -17.0 | 0.97 | 0.137 | 1.50 |
| SPP | +4.5 | +2.8 | -1.7 | -3.2 | 0.77 | 0.041 | 1.11 |

## C. PJM and MISO counterfactuals

| counterfactual (every RTO adopts) | PJM, full Sec.2106 | PJM, no screen | MISO, full Sec.2106 | MISO, no screen |
|---|---|---|---|---|
| as calibrated | +0.7 | +9.0 | +23.5 | +18.3 |
| PJM zero-cost share = MISO's | +5.6 | +8.0 | +23.5 | +18.3 |
| PJM cost spread = MISO's | +0.9 | +9.0 | +23.5 | +18.3 |
| MISO throughput = PJM's | +0.7 | +9.0 | +13.6 | +16.9 |

| post-rule requests that sign (every RTO adopts, mean per run) | with zero upgrade cost |
|---|---|
| PJM, Gas | 5 of 28 |
| MISO, Gas | 4 of 118 |
| PJM, Offshore wind | 3 of 3 |
| PJM, Onshore wind | 5 of 19 |
| MISO, Onshore wind | 9 of 111 |
| PJM, Solar | 216 of 427 |
| MISO, Solar | 49 of 303 |
| PJM, Storage | 133 of 135 |
| MISO, Storage | 36 of 59 |

## E. More or sooner

Capacity from new requests in RTO regions. 'Ever complete' counts requests that reach operation after Nov 2041 too; the difference is capacity the bill brings forward rather than adds.

| case | new RTO requests online by Nov 2041, GW | that ever complete, GW | sooner, not more | requests made in the rule's first six years: online by Nov 2041 | that ever complete |
|---|---|---|---|---|---|
| without Sec.2106 | +3.4 | +6.0 | -2.7 | +2.3 | +2.2 |
| + published locations (no screen) | +40.9 | +44.1 | -3.3 | +25.7 | +25.4 |
| + relative screen (central) | +33.6 | +29.2 | +4.5 | +18.3 | +17.9 |
| p=0.5: relative screen (central) | +18.6 | +17.2 | +1.4 | +10.1 | +9.9 |

## F. Screen specification under the earlier calibration

| calibration before the Nov 2026 refit (commit b6c291c), every RTO adopts | BAAJA minus current law, new GW |
|---|---|
| without Sec.2106 | +7.7 [+5.6, +9.6] |
| relative screen (central) | +42.9 [+37.8, +48.3] |
| no screen | +49.4 [+45.4, +54.5] |
| absolute screen | +9.5 [+3.4, +17.0] |

