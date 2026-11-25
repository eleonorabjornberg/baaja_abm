# Where the Sec.2106 gain comes from (grid agents)

Mean [5th, 95th percentile] across 100 paired runs; every case is paired with current law under the same seeds, political draws and assumption changes. New capacity excludes relicensed hydro. GW online by Nov 2041.

## A. Sec.2106 by component

The single decision point removes the current-law re-study round (the cost of those who stay moves with the withdrawn share above SPP's, restudy_rho, and by a request-level change drawn from SPP's, scaled by restudy_scale, and the agreement comes restudy_months later). Published locations add a share of requests at sites the provider has studied, at a fixed fee. The entry screen keeps out the requests least likely to complete.

| case (every RTO adopts unless p=0.5) | BAAJA minus current law, new GW | of which Sec.2106 | RTO regions, GW |
|---|---|---|---|
| without Sec.2106 | +6.2 [+4.5, +8.2] |  | +4.1 [+2.3, +5.8] |
| single decision point only | -22.3 [-28.1, -16.3] | -28.5 | -24.4 [-29.9, -17.9] |
| + published locations (no screen) | -20.4 [-26.1, -14.3] | -26.6 | -22.5 [-28.1, -16.2] |
| + relative screen (central) | -19.1 [-25.7, -12.0] | -25.3 | -21.2 [-27.8, -13.9] |
| + absolute screen instead | -68.2 [-75.6, -59.5] | -74.3 | -70.2 [-77.5, -61.5] |
| relative screen, no published locations | -21.1 [-27.5, -14.0] | -27.3 | -23.2 [-29.6, -15.6] |
| p=0.5: no screen | -8.2 [-18.8, +2.4] | -14.4 | -10.3 [-21.7, +0.4] |
| p=0.5: relative screen (central) | -8.0 [-19.2, +3.4] | -14.2 | -10.1 [-21.4, +1.2] |
| p=0.5: absolute screen | -34.6 [-64.1, -2.5] | -40.8 | -36.7 [-65.6, -4.3] |
| Titles I-II only (no Sec.2106, no Sec.2109) | +3.3 [+1.8, +5.2] | -2.9 | +1.8 [+0.5, +3.5] |
| p=0.5 without Sec.2109 | -11.1 [-22.6, +0.1] | -17.3 | -12.6 [-24.1, -1.3] |

## B. The current-law re-study round

Both current law and the bill change. With no re-study round under current law, Sec.2106's single decision point has nothing to remove.

| current-law re-study round or hazard (law and bill) | current law new GW | without Sec.2106 | single decision point only | every RTO, full Sec.2106 | p=0.5, full Sec.2106 |
|---|---|---|---|---|---|
| central (rho 0.1, SPP cost changes at scale 1, 17 months) | 983 | +6.2 | -22.3 | -19.1 | -8.0 |
| no request-level cost change (scale 0) | 871 | +5.5 | +28.7 | +32.6 | +19.3 |
| costs unchanged by re-study | 876 | +5.6 | +26.8 | +30.7 | +18.2 |
| months=8 (Order No. 2023 pro forma) | 985 | +6.1 | -26.0 | -22.1 | -9.7 |
| no re-study round | 876 | +5.6 | +5.6 | +12.9 | +9.0 |
| no background withdrawal during the round | 1019 | +6.6 | -37.2 | -34.1 | -15.6 |
| MISO later hazard = PJM's | 998 | +6.3 | -31.9 | -24.7 | -10.7 |

## G. Readings of Sec.2106

Paired with the central current law. 'Only published locations skip the round' reads the single decision point as limited to requests at studied sites, where 'any limitations from contingencies' can be known in advance; 're-study cost change kept' keeps current law's cost changes but takes the decision at the first result; 'screen ranked by value' ranks requests for the entry screen by private value alone, not by the chance of completing.

| reading of Sec.2106 (every RTO adopts unless p=0.5) | BAAJA minus current law, new GW | RTO regions, GW |
|---|---|---|
| + relative screen (central) | -19.1 [-25.7, -12.0] | -21.2 [-27.8, -13.9] |
| only published locations skip the round | +12.2 [+8.3, +17.8] | +10.2 [+6.3, +15.5] |
| re-study cost change kept | +42.7 [+37.0, +48.7] | +40.6 [+35.1, +46.6] |
| screen ranked by value | -29.2 [-35.7, -21.7] | -31.2 [-37.8, -23.5] |
| p=0.5: relative screen (central) | -8.0 [-19.2, +3.4] | -10.1 [-21.4, +1.2] |
| p=0.5: only published locations skip the round | +8.6 [-0.8, +19.3] | +6.5 [-3.1, +17.2] |
| p=0.5: re-study cost change kept | +24.7 [+7.7, +42.8] | +22.7 [+5.7, +40.4] |
| p=0.5: screen ranked by value | -13.5 [-27.6, +2.7] | -15.6 [-29.7, -0.0] |

## By region: the entry screen

| region (every RTO adopts) | no screen | relative screen | screen effect | absolute screen | throughput / arrivals | zero-cost share | cost spread (sigma) |
|---|---|---|---|---|---|---|---|
| CAISO | -2.0 | -2.3 | -0.3 | -5.0 | 1.85 | 0.080 | 1.35 |
| ISO-NE | -2.5 | -2.6 | -0.1 | -4.6 | 0.68 | 0.011 | 1.39 |
| MISO | -3.5 | +1.8 | +5.3 | -8.7 | 0.59 | 0.025 | 1.21 |
| NYISO | -3.8 | -4.1 | -0.3 | -7.6 | 0.56 | 0.031 | 1.04 |
| PJM | -6.2 | -9.0 | -2.9 | -32.6 | 0.97 | 0.137 | 1.50 |
| SPP | -4.6 | -4.9 | -0.4 | -11.7 | 0.77 | 0.041 | 1.11 |

## C. PJM and MISO counterfactuals

| counterfactual (every RTO adopts) | PJM, full Sec.2106 | PJM, no screen | MISO, full Sec.2106 | MISO, no screen |
|---|---|---|---|---|
| as calibrated | -9.0 | -6.2 | +1.8 | -3.5 |
| PJM zero-cost share = MISO's | -11.4 | -10.8 | +1.8 | -3.5 |
| PJM cost spread = MISO's | -9.4 | -6.5 | +1.8 | -3.5 |
| MISO throughput = PJM's | -9.0 | -6.2 | -10.4 | -9.2 |

| post-rule requests that sign (every RTO adopts, mean per run) | with zero upgrade cost |
|---|---|
| PJM, Gas | 5 of 26 |
| MISO, Gas | 3 of 145 |
| PJM, Offshore wind | 3 of 3 |
| PJM, Onshore wind | 5 of 17 |
| MISO, Onshore wind | 10 of 130 |
| PJM, Solar | 226 of 322 |
| MISO, Solar | 49 of 240 |
| PJM, Storage | 140 of 143 |
| MISO, Storage | 36 of 40 |

## E. More or sooner

Capacity from new requests in RTO regions. 'Ever complete' counts requests that reach operation after Nov 2041 too; the difference is capacity the bill brings forward rather than adds.

| case | new RTO requests online by Nov 2041, GW | that ever complete, GW | sooner, not more | requests made in the rule's first six years: online by Nov 2041 | that ever complete |
|---|---|---|---|---|---|
| without Sec.2106 | +4.0 | +6.8 | -2.8 | +2.8 | +2.6 |
| + published locations (no screen) | -22.6 | -54.5 | +31.9 | -30.1 | -30.9 |
| + relative screen (central) | -21.3 | -54.4 | +33.1 | -30.0 | -30.8 |
| p=0.5: relative screen (central) | -10.2 | -26.9 | +16.7 | -15.0 | -15.6 |

