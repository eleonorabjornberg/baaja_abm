# Where the Sec.2106 gain comes from (grid agents)

Mean [5th, 95th percentile] across 100 paired runs; every case is paired with current law under the same seeds, political draws and assumption changes. New capacity excludes relicensed hydro. GW online by Nov 2041.

## A. Sec.2106 by component

The single decision point removes the current-law re-study round (the cost of those who stay moves with the withdrawn share above SPP's, restudy_rho, and by a request-level change drawn from SPP's, scaled by restudy_scale, and the agreement comes restudy_months later). Published locations add a share of requests at sites the provider has studied, at a fixed fee. The entry screen keeps out the requests least likely to complete.

| case (every RTO adopts unless p=0.5) | BAAJA minus current law, new GW | of which Sec.2106 | RTO regions, GW |
|---|---|---|---|
| without Sec.2106 | +5.2 [+3.4, +7.3] |  | +3.1 [+1.7, +4.7] |
| single decision point only | -23.5 [-29.6, -17.3] | -28.7 | -25.6 [-31.6, -19.4] |
| + published locations (no screen) | -21.6 [-27.5, -15.5] | -26.9 | -23.7 [-29.4, -17.6] |
| + relative screen (central) | -20.4 [-27.0, -13.3] | -25.6 | -22.5 [-29.1, -15.1] |
| + absolute screen instead | -69.3 [-77.2, -61.0] | -74.6 | -71.4 [-79.6, -62.8] |
| relative screen, no published locations | -22.4 [-28.5, -15.2] | -27.6 | -24.5 [-30.7, -17.0] |
| p=0.5: no screen | -9.3 [-20.0, +0.8] | -14.5 | -11.4 [-23.0, -0.6] |
| p=0.5: relative screen (central) | -9.1 [-20.3, +2.8] | -14.3 | -11.2 [-22.7, +0.9] |
| p=0.5: absolute screen | -35.7 [-65.6, -3.2] | -40.9 | -37.7 [-67.1, -5.1] |
| Titles I-II only (no Sec.2106, no Sec.2109) | +3.3 [+1.8, +5.2] | -1.9 | +1.8 [+0.5, +3.5] |
| p=0.5 without Sec.2109 | -11.1 [-22.6, +0.1] | -16.4 | -12.6 [-24.1, -1.3] |

## B. The current-law re-study round

Both current law and the bill change. With no re-study round under current law, Sec.2106's single decision point has nothing to remove.

| current-law re-study round or hazard (law and bill) | current law new GW | without Sec.2106 | single decision point only | every RTO, full Sec.2106 | p=0.5, full Sec.2106 |
|---|---|---|---|---|---|
| central (rho 0.1, SPP cost changes at scale 1, 17 months) | 983 | +5.2 | -23.5 | -20.4 | -9.1 |
| no request-level cost change (scale 0) | 871 | +4.5 | +27.4 | +31.3 | +18.1 |
| costs unchanged by re-study | 876 | +4.6 | +25.5 | +29.3 | +17.1 |
| months=8 (Order No. 2023 pro forma) | 985 | +5.2 | -27.2 | -23.4 | -10.8 |
| no re-study round | 876 | +4.6 | +4.6 | +11.7 | +7.9 |
| no background withdrawal during the round | 1019 | +5.5 | -38.4 | -35.3 | -16.7 |
| MISO later hazard = PJM's | 998 | +5.2 | -33.0 | -26.0 | -11.9 |

## G. Readings of Sec.2106

Paired with the central current law. 'Only published locations skip the round' reads the single decision point as limited to requests at studied sites, where 'any limitations from contingencies' can be known in advance; 're-study cost change kept' keeps current law's cost changes but takes the decision at the first result; 'screen ranked by value' ranks requests for the entry screen by private value alone, not by the chance of completing.

| reading of Sec.2106 (every RTO adopts unless p=0.5) | BAAJA minus current law, new GW | RTO regions, GW |
|---|---|---|
| + relative screen (central) | -20.4 [-27.0, -13.3] | -22.5 [-29.1, -15.1] |
| only published locations skip the round | +11.1 [+7.0, +15.9] | +9.0 [+5.3, +13.8] |
| re-study cost change kept | +41.4 [+35.8, +47.5] | +39.3 [+33.8, +45.4] |
| screen ranked by value | -30.4 [-37.3, -23.3] | -32.4 [-39.3, -25.0] |
| p=0.5: relative screen (central) | -9.1 [-20.3, +2.8] | -11.2 [-22.7, +0.9] |
| p=0.5: only published locations skip the round | +7.5 [-1.8, +18.3] | +5.5 [-3.9, +15.9] |
| p=0.5: re-study cost change kept | +23.6 [+7.4, +41.3] | +21.5 [+5.2, +38.9] |
| p=0.5: screen ranked by value | -14.6 [-28.7, +2.0] | -16.7 [-31.0, -0.8] |

## By region: the entry screen

| region (every RTO adopts) | no screen | relative screen | screen effect | absolute screen | throughput / arrivals | zero-cost share | cost spread (sigma) |
|---|---|---|---|---|---|---|---|
| CAISO | -2.0 | -2.3 | -0.3 | -5.0 | 1.85 | 0.080 | 1.35 |
| ISO-NE | -2.5 | -2.6 | -0.1 | -4.6 | 0.68 | 0.011 | 1.39 |
| MISO | -4.7 | +0.5 | +5.2 | -9.9 | 0.59 | 0.025 | 1.21 |
| NYISO | -3.8 | -4.1 | -0.3 | -7.6 | 0.56 | 0.031 | 1.04 |
| PJM | -6.2 | -9.0 | -2.9 | -32.6 | 0.97 | 0.137 | 1.50 |
| SPP | -4.6 | -4.9 | -0.4 | -11.7 | 0.77 | 0.041 | 1.11 |

## C. PJM and MISO counterfactuals

| counterfactual (every RTO adopts) | PJM, full Sec.2106 | PJM, no screen | MISO, full Sec.2106 | MISO, no screen |
|---|---|---|---|---|
| as calibrated | -9.0 | -6.2 | +0.5 | -4.7 |
| PJM zero-cost share = MISO's | -11.4 | -10.8 | +0.5 | -4.7 |
| PJM cost spread = MISO's | -9.4 | -6.5 | +0.5 | -4.7 |
| MISO throughput = PJM's | -9.0 | -6.2 | -11.5 | -10.3 |

| post-rule requests that sign (every RTO adopts, mean per run) | with zero upgrade cost |
|---|---|
| PJM, Gas | 5 of 26 |
| MISO, Gas | 3 of 143 |
| PJM, Offshore wind | 3 of 3 |
| PJM, Onshore wind | 5 of 17 |
| MISO, Onshore wind | 10 of 127 |
| PJM, Solar | 226 of 322 |
| MISO, Solar | 49 of 232 |
| PJM, Storage | 140 of 143 |
| MISO, Storage | 36 of 39 |

## E. More or sooner

Capacity from new requests in RTO regions. 'Ever complete' counts requests that reach operation after Nov 2041 too; the difference is capacity the bill brings forward rather than adds.

| case | new RTO requests online by Nov 2041, GW | that ever complete, GW | sooner, not more | requests made in the rule's first six years: online by Nov 2041 | that ever complete |
|---|---|---|---|---|---|
| without Sec.2106 | +3.1 | +5.1 | -2.1 | +2.0 | +1.9 |
| + published locations (no screen) | -23.8 | -56.3 | +32.5 | -30.9 | -31.7 |
| + relative screen (central) | -22.6 | -56.4 | +33.8 | -30.7 | -31.6 |
| p=0.5: relative screen (central) | -11.3 | -28.7 | +17.4 | -15.8 | -16.4 |

