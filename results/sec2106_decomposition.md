# Where the Sec.2106 gain comes from (grid agents)

Mean [5th, 95th percentile] across 100 paired runs; every case is paired with current law under the same seeds, political draws and assumption changes. New capacity excludes relicensed hydro. GW online by Nov 2041.

## A. Sec.2106 by component

The single decision point removes the current-law re-study round (the cost of those who stay moves with the withdrawn share, restudy_rho, and by a request-level shock, restudy_mu and restudy_sd, and the agreement comes restudy_months later). Published locations add a share of requests at sites the provider has studied, at a fixed fee. The entry screen keeps out the requests least likely to complete.

| case (every RTO adopts unless p=0.5) | BAAJA minus current law, new GW | of which Sec.2106 | RTO regions, GW |
|---|---|---|---|
| without Sec.2106 | +6.5 [+4.6, +8.3] |  | +3.8 [+2.4, +5.3] |
| single decision point only | +68.1 [+61.7, +73.2] | +61.6 | +65.4 [+59.1, +70.7] |
| + published locations (no screen) | +72.1 [+65.4, +77.2] | +65.7 | +69.4 [+63.1, +74.3] |
| + relative screen (central) | +65.0 [+57.7, +71.1] | +58.6 | +62.4 [+55.1, +68.0] |
| + absolute screen instead | +41.0 [+34.0, +46.5] | +34.6 | +38.3 [+31.8, +43.8] |
| relative screen, no published locations | +60.5 [+53.6, +66.4] | +54.0 | +57.8 [+50.5, +63.7] |
| p=0.5: no screen | +41.0 [+13.5, +67.0] | +34.5 | +38.3 [+10.4, +63.7] |
| p=0.5: relative screen (central) | +36.5 [+11.2, +60.5] | +30.0 | +33.8 [+8.3, +57.2] |
| p=0.5: absolute screen | +23.9 [+3.6, +45.0] | +17.4 | +21.2 [+1.0, +42.0] |
| Titles I-II only (no Sec.2106, no Sec.2109) | +3.0 [+1.7, +4.6] | -3.4 | +1.6 [+0.4, +3.2] |
| p=0.5 without Sec.2109 | +32.7 [+7.7, +56.5] | +26.2 | +31.2 [+6.5, +55.2] |

## B. The current-law re-study round

Both current law and the bill change. With no re-study round under current law, Sec.2106's single decision point has nothing to remove.

| current-law re-study round (law and bill) | current law new GW | without Sec.2106 | single decision point only | every RTO, full Sec.2106 | p=0.5, full Sec.2106 |
|---|---|---|---|---|---|
| central (rho 0.1, mu -0.08, sd 0.6, 17 months) | 972 | +6.5 | +68.1 | +65.0 | +36.5 |
| no cost shock (sd=0, mu=0) | 992 | +6.5 | +58.2 | +55.1 | +31.3 |
| costs unchanged by re-study | 1002 | +6.7 | +52.8 | +49.8 | +28.6 |
| months=5 (Order No. 2023 restudy deadline) | 972 | +6.5 | +41.6 | +40.7 | +23.7 |
| no re-study round | 1002 | +6.7 | +6.7 | +7.9 | +6.5 |

## By region: the entry screen

| region (every RTO adopts) | no screen | relative screen | screen effect | absolute screen | throughput / arrivals | zero-cost share | cost spread (sigma) |
|---|---|---|---|---|---|---|---|
| CAISO | +4.0 | +2.7 | -1.3 | +2.6 | 1.85 | 0.080 | 1.35 |
| ISO-NE | +4.7 | +4.0 | -0.7 | +2.9 | 0.68 | 0.011 | 1.39 |
| MISO | +33.5 | +39.1 | +5.6 | +33.8 | 0.59 | 0.025 | 1.21 |
| NYISO | +5.5 | +4.4 | -1.2 | +1.6 | 0.56 | 0.031 | 1.04 |
| PJM | +15.4 | +7.6 | -7.8 | -2.6 | 0.97 | 0.137 | 1.50 |
| SPP | +6.4 | +4.6 | -1.7 | -0.0 | 0.77 | 0.041 | 1.11 |

## C. PJM and MISO counterfactuals

| counterfactual (every RTO adopts) | PJM, full Sec.2106 | PJM, no screen | MISO, full Sec.2106 | MISO, no screen |
|---|---|---|---|---|
| as calibrated | +7.6 | +15.4 | +39.1 | +33.5 |
| PJM zero-cost share = MISO's | +10.7 | +13.9 | +39.1 | +33.5 |
| PJM cost spread = MISO's | +8.0 | +15.3 | +39.1 | +33.5 |
| MISO throughput = PJM's | +7.6 | +15.4 | +24.7 | +31.2 |

| post-rule requests that sign (every RTO adopts, mean per run) | with zero upgrade cost |
|---|---|
| PJM, Gas | 3 of 29 |
| MISO, Gas | 2 of 148 |
| PJM, Offshore wind | 3 of 3 |
| PJM, Onshore wind | 4 of 22 |
| MISO, Onshore wind | 7 of 185 |
| PJM, Solar | 175 of 482 |
| MISO, Solar | 41 of 510 |
| PJM, Storage | 109 of 162 |
| MISO, Storage | 31 of 76 |

## E. More or sooner

Capacity from new requests in RTO regions. 'Ever complete' counts requests that reach operation after Nov 2041 too; the difference is capacity the bill brings forward rather than adds.

| case | new RTO requests online by Nov 2041, GW | that ever complete, GW | sooner, not more | requests made in the rule's first six years: online by Nov 2041 | that ever complete |
|---|---|---|---|---|---|
| without Sec.2106 | +3.7 | +6.8 | -3.1 | +2.5 | +2.4 |
| + published locations (no screen) | +69.3 | +63.5 | +5.9 | +37.4 | +36.7 |
| + relative screen (central) | +62.3 | +48.4 | +13.8 | +29.0 | +28.3 |
| p=0.5: relative screen (central) | +33.7 | +27.4 | +6.3 | +15.8 | +15.2 |

## F. Screen specification under the earlier calibration

| calibration before the Nov 2026 refit (commit b6c291c), every RTO adopts | BAAJA minus current law, new GW |
|---|---|
| without Sec.2106 | +6.3 [+4.4, +8.2] |
| relative screen (central) | +68.1 [+60.7, +73.9] |
| no screen | +73.3 [+68.0, +79.5] |
| absolute screen | +42.3 [+35.5, +49.2] |

