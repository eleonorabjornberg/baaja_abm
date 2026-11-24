# Simulation 6: electricity supply and resource adequacy (regime "2025")

Supply = existing fleet (EIA-860, end-2025) minus retirements plus what the model's queue brings online, by LBNL region. On-peak accredited capacity ("firm" below), peak demand and the reference margin level (RML, the reserve margin a region plans to) follow NERC's 2025 Long-Term Reliability Assessment. Wind, solar and batteries count at an on-peak share that falls over time (central: halfway between NERC's 2025 national values and PJM's 2041/42 ratings), except in PJM, whose reference margin is an installed-capacity margin that already rises as accreditation falls. This simpler model has no feedback from scarcity to building, so surpluses in some regions are not self-correcting and shortfalls are not filled by new entry; the grid-agent model (Sim 7) adds an entry response.

## Current law: the United States

| peak year | peak demand GW (NERC) | installed GW | renewable / gas / storage / coal+oil GW | firm GW | reserve margin % | regions below RML (of 9) | shortfall GW | generation TWh |
|---|---|---|---|---|---|---|---|---|
| 2027 | 820 | 1311 | 429 / 509 / 80 / 183 | 985 | 20.1 [19.8, 20.3] | 1.9 | 9.3 [8.6, 10.2] | 4436 |
| 2030 | 883 | 1640 | 652 / 558 / 161 / 159 | 1109 | 25.7 [24.9, 26.5] | 2.6 | 21.7 [18.1, 25.6] | 5022 |
| 2035 | 952 | 1961 | 846 / 655 / 211 / 139 | 1221 | 28.3 [27.2, 29.3] | 2.9 | 59.5 [55.2, 63.0] | 5729 |
| 2041 | 1044 | 2243 | 977 / 764 / 269 / 123 | 1311 | 25.6 [24.7, 26.6] | 3.9 | 111.9 [107.4, 115.5] | 6354 |

## Current law: by region (reserve margin, % of peak demand; 5th-95th percentile across runs)

| region | RML 2035 % | reserve margin 2030 % | reserve margin 2035 % | reserve margin 2041 % | runs below RML in 2035 | median first year below RML | shortfall 2035 GW |
|---|---|---|---|---|---|---|---|
| CAISO | 18.0 | 22.8 [21.0, 24.6] | 11.0 [8.4, 13.6] | -5.6 [-7.9, -3.8] | 100% | 2032 | 5.0 [3.2, 6.9] |
| ERCOT | 13.8 | 50.1 [46.3, 53.5] | 72.7 [67.9, 77.5] | 81.7 [76.4, 86.7] | 0% | - | 0.0 [0.0, 0.0] |
| ISO-NE | 13.0 | 12.5 [9.0, 16.4] | 9.5 [4.9, 14.4] | 3.3 [-1.0, 7.8] | 89% | 2027 | 1.0 [0.0, 2.2] |
| MISO | 8.9 | 5.5 [3.5, 7.8] | 15.7 [13.1, 18.5] | 23.7 [20.3, 27.2] | 0% | 2027 | 0.0 [0.0, 0.0] |
| NYISO | 15.0 | 23.7 [20.6, 26.3] | 20.2 [16.6, 22.9] | 12.9 [10.0, 16.1] | 0% | 2040 | 0.0 [0.0, 0.0] |
| PJM | 35.1 | 16.3 [15.1, 17.7] | 8.3 [6.7, 10.0] | -2.9 [-4.2, -1.5] | 100% | 2028 | 53.5 [50.1, 56.6] |
| SPP | 19.0 | 31.3 [27.1, 35.3] | 41.3 [35.0, 46.0] | 43.4 [36.3, 51.3] | 0% | - | 0.0 [0.0, 0.0] |
| Southeast | 15.0 | 30.8 [28.8, 32.6] | 33.9 [30.9, 36.6] | 35.7 [32.7, 38.8] | 0% | - | 0.0 [0.0, 0.0] |
| West | 12.8 | 38.6 [36.7, 40.7] | 41.8 [38.8, 44.7] | 38.4 [34.8, 41.6] | 0% | - | 0.0 [0.0, 0.0] |

## What BAAJA changes: the United States (difference from current law, paired)

| scenario | firm GW 2030 | firm GW 2035 | firm GW 2041 | shortfall GW 2035 | shortfall GW 2041 | regions below RML 2035 | TWh 2041 |
|---|---|---|---|---|---|---|---|
| BAAJA (data-sized provisions) | +0.5 [+0.1, +1.0] | +1.9 [+1.2, +2.8] | +3.5 [+2.4, +4.6] | -0.3 [-0.7, -0.1] | -0.6 [-1.1, -0.2] | -0.01 | +20 |
| BAAJA + Sec.2106 10% cut | +0.5 [+0.1, +1.0] | +6.7 [+5.2, +8.3] | +15.6 [+13.2, +17.7] | -2.1 [-2.9, -1.4] | -6.3 [-7.4, -5.0] | -0.05 | +72 |
| BAAJA + Sec.2106 ceiling (42% cut) | +0.5 [+0.1, +1.0] | +30.8 [+27.5, +33.5] | +74.7 [+70.0, +79.8] | -11.6 [-13.6, -9.9] | -32.0 [-34.7, -29.2] | -0.62 | +322 |

## What BAAJA changes: by region in 2035 (mean difference from current law)

| region | BAAJA (data-sized provisions): firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 10% cut: firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 ceiling (42% cut): firm GW / margin pts / shortfall GW (2035) |
|---|---|---|---|
| CAISO | +0.0 / +0.1 / -0.0 | +0.5 / +0.7 / -0.5 | +2.8 / +3.9 / -2.8 |
| ERCOT | +0.2 / +0.2 / +0.0 | +0.2 / +0.2 / +0.0 | +0.2 / +0.2 / +0.0 |
| ISO-NE | +0.0 / +0.1 / -0.0 | +0.2 / +0.9 / -0.2 | +1.5 / +5.4 / -0.9 |
| MISO | +0.3 / +0.2 / +0.0 | +1.9 / +1.4 / +0.0 | +9.4 / +7.0 / +0.0 |
| NYISO | +0.0 / +0.1 / +0.0 | +0.3 / +1.0 / +0.0 | +2.0 / +6.0 / +0.0 |
| PJM | +0.2 / +0.1 / -0.2 | +1.4 / +0.7 / -1.4 | +7.9 / +4.0 / -7.9 |
| SPP | +0.2 / +0.3 / +0.0 | +1.2 / +1.8 / +0.0 | +6.1 / +9.3 / +0.0 |
| Southeast | +0.4 / +0.2 / +0.0 | +0.4 / +0.2 / +0.0 | +0.4 / +0.2 / +0.0 |
| West | +0.5 / +0.4 / +0.0 | +0.5 / +0.4 / +0.0 | +0.5 / +0.4 / +0.0 |

## Sensitivity to the supply assumptions (each at its low and high end, others central; 2035)

| assumption | low / high | law: shortfall 2035 GW | law: regions below RML 2035 | data-sized BAAJA: shortfall change GW | + 10% Sec.2106: shortfall change GW | what it is |
|---|---|---|---|---|---|---|
| ret_hazard_old | 0.01 / 0.06 | 55 / 66 | 2.6 / 3.7 | -0.3 / -0.3 | -2.1 / -2.3 | annual retirement probability of coal, gas and oil units with no announced retirement once past the median age at retirement (coal 56, gas/oil 45 years) [A; ages D: EIA-860] |
| ret_announced | 0.6 / 1.0 | 54 / 59 | 2.8 / 2.9 | -0.3 / -0.3 | -2.1 / -2.1 | share of announced retirements (EIA-860/860M) that happen on schedule; low = delays such as the 2025 DOE 202(c) orders keeping coal units open |
| elcc_decline | 0.0 / 1.0 | 54 / 70 | 1.3 / 3.8 | -0.2 / -0.4 | -1.5 / -2.4 | how far on-peak shares of wind, solar and batteries fall by 2041: 0 = NERC 2025 national values throughout, 1 = PJM's 2041/42 preliminary ELCC class ratings, linear in time (not in PJM, whose installed reserve margin already rises with the mix) |
| demand_growth_mult | 0.5 / 1.5 | 18 / 113 | 1.3 / 4.0 | -0.2 / -0.5 | -1.5 / -3.1 | multiplier on NERC's forecast growth in net internal demand (2026-35 path, extended to 2041 at the 2030-35 rate) |

## Checks against NERC

Existing fleet firm capacity in 2026 vs NERC's existing-certain resources; the ratio is applied to the existing fleet so that reserve margins are on NERC's basis. NERC's anticipated reserve margin counts only Tier 1 additions (signed contracts, under construction), so it falls faster than the model's after 2028.

| region | fleet firm GW 2026 (unscaled) | NERC existing-certain + transfers GW | scale applied | reserve margin 2030: NERC anticipated / model | 2035: NERC / model |
|---|---|---|---|---|---|
| CAISO | 67.5 | 76.4 | 1.13 | 42.7 / 22.8 | 33.3 / 11.0 |
| ERCOT | 112.4 | 93.9 | 0.83 | 29.9 / 50.1 | 22.8 / 72.7 |
| ISO-NE | 32.5 | 27.6 | 0.85 | 23.6 / 12.5 | 16.9 / 9.5 |
| MISO | 161.1 | 126.3 | 0.78 | 4.3 / 5.5 | -1.9 / 15.7 |
| NYISO | 42.3 | 37.4 | 0.87 | 22.5 / 23.7 | 15.4 / 20.2 |
| PJM | 196.7 | 189.7 | 0.96 | 13.9 / 16.3 | -0.3 / 8.3 |
| SPP | 67.3 | 71.5 | 1.06 | 22.6 / 31.3 | 16.0 / 41.3 |
| Southeast | 244.2 | 232.4 | 0.95 | 24.8 / 30.8 | 18.0 / 33.9 |
| West | 157.4 | 123.2 | 0.77 | 25.5 / 38.6 | 7.3 / 41.8 |
