# Simulation 6: electricity supply and resource adequacy (regime "2025")

Supply = existing fleet (EIA-860, end-2025) minus retirements plus what the model's queue brings online, by LBNL region. Firm capacity, peak demand and the reference margin level (RML, the reserve margin a region plans to) follow NERC's 2025 Long-Term Reliability Assessment. Wind, solar and batteries count at an on-peak share that falls over time (central: halfway between NERC's 2025 national values and PJM's 2041/42 ratings). The model has no feedback from scarcity to building yet (Phase 2), so surpluses in some regions are not self-correcting and shortfalls are not filled by new entry.

## Current law: the United States

| peak year | peak demand GW (NERC) | installed GW | renewable / gas / storage / coal+oil GW | firm GW | reserve margin % | regions below RML (of 9) | shortfall GW | generation TWh |
|---|---|---|---|---|---|---|---|---|
| 2027 | 820 | 1311 | 429 / 509 / 80 / 183 | 988 | 20.5 [20.2, 20.7] | 1.9 | 8.3 [7.3, 9.3] | 4436 |
| 2030 | 883 | 1640 | 652 / 558 / 161 / 159 | 1135 | 28.6 [27.8, 29.6] | 1.4 | 20.1 [17.5, 22.2] | 5022 |
| 2035 | 952 | 1961 | 846 / 655 / 211 / 139 | 1263 | 32.7 [31.6, 33.9] | 2.6 | 68.5 [64.8, 71.9] | 5729 |
| 2041 | 1044 | 2243 | 977 / 764 / 269 / 123 | 1362 | 30.5 [29.5, 31.6] | 3.3 | 131.0 [127.3, 133.8] | 6354 |

## Current law: by region (reserve margin, % of peak demand; 5th-95th percentile across runs)

| region | RML 2035 % | reserve margin 2030 % | reserve margin 2035 % | reserve margin 2041 % | runs below RML in 2035 | median first year below RML | shortfall 2035 GW |
|---|---|---|---|---|---|---|---|
| CAISO | 18.0 | 22.8 [21.0, 24.6] | 11.0 [8.4, 13.6] | -5.6 [-7.9, -3.8] | 100% | 2032 | 5.0 [3.2, 6.9] |
| ERCOT | 13.8 | 59.1 [54.5, 63.1] | 88.2 [82.4, 94.0] | 101.4 [95.0, 107.3] | 0% | - | 0.0 [0.0, 0.0] |
| ISO-NE | 13.0 | 14.0 [9.9, 18.7] | 12.3 [6.9, 18.1] | 7.1 [1.9, 12.4] | 59% | 2027 | 0.5 [0.0, 1.6] |
| MISO | 8.9 | 11.4 [8.9, 14.3] | 26.7 [23.3, 30.2] | 38.8 [34.4, 43.2] | 0% | 2027 | 0.0 [0.0, 0.0] |
| NYISO | 15.0 | 25.3 [21.8, 28.3] | 22.7 [18.6, 25.9] | 16.0 [12.7, 19.8] | 0% | - | 0.0 [0.0, 0.0] |
| PJM | 35.1 | 14.9 [13.7, 16.3] | 3.5 [2.1, 5.2] | -11.8 [-13.0, -10.5] | 100% | 2028 | 63.0 [59.5, 65.7] |
| SPP | 19.0 | 31.3 [27.1, 35.3] | 41.3 [35.0, 46.0] | 43.4 [36.3, 51.3] | 0% | - | 0.0 [0.0, 0.0] |
| Southeast | 15.0 | 31.6 [29.6, 33.6] | 35.5 [32.4, 38.4] | 37.9 [34.8, 41.2] | 0% | - | 0.0 [0.0, 0.0] |
| West | 12.8 | 47.8 [45.4, 50.5] | 56.6 [52.8, 60.4] | 55.8 [51.1, 59.9] | 0% | - | 0.0 [0.0, 0.0] |

## What BAAJA changes: the United States (difference from current law, paired)

| scenario | firm GW 2030 | firm GW 2035 | firm GW 2041 | shortfall GW 2035 | shortfall GW 2041 | regions below RML 2035 | TWh 2041 |
|---|---|---|---|---|---|---|---|
| BAAJA (data-sized provisions) | +0.6 [+0.2, +1.2] | +2.2 [+1.4, +3.1] | +4.0 [+2.7, +5.3] | -0.3 [-0.6, -0.0] | -0.5 [-1.0, -0.2] | -0.03 | +20 |
| BAAJA + Sec.2106 10% cut | +0.6 [+0.2, +1.2] | +7.3 [+5.8, +9.2] | +16.3 [+13.8, +18.7] | -1.9 [-2.6, -1.3] | -4.8 [-6.0, -3.7] | -0.14 | +72 |
| BAAJA + Sec.2106 ceiling (42% cut) | +0.6 [+0.2, +1.2] | +33.1 [+29.4, +35.9] | +76.2 [+71.2, +81.2] | -10.0 [-11.9, -8.5] | -24.3 [-26.7, -21.4] | -0.55 | +322 |

## What BAAJA changes: by region in 2035 (mean difference from current law)

| region | BAAJA (data-sized provisions): firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 10% cut: firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 ceiling (42% cut): firm GW / margin pts / shortfall GW (2035) |
|---|---|---|---|
| CAISO | +0.0 / +0.1 / -0.0 | +0.5 / +0.7 / -0.5 | +2.8 / +3.9 / -2.8 |
| ERCOT | +0.3 / +0.3 / +0.0 | +0.3 / +0.3 / +0.0 | +0.3 / +0.3 / +0.0 |
| ISO-NE | +0.0 / +0.2 / -0.0 | +0.3 / +1.0 / -0.1 | +1.7 / +6.4 / -0.4 |
| MISO | +0.3 / +0.3 / +0.0 | +2.4 / +1.8 / +0.0 | +12.1 / +8.9 / +0.0 |
| NYISO | +0.0 / +0.1 / +0.0 | +0.4 / +1.2 / +0.0 | +2.3 / +6.9 / +0.0 |
| PJM | +0.2 / +0.1 / -0.2 | +1.2 / +0.6 / -1.2 | +6.8 / +3.4 / -6.8 |
| SPP | +0.2 / +0.3 / +0.0 | +1.2 / +1.8 / +0.0 | +6.1 / +9.3 / +0.0 |
| Southeast | +0.4 / +0.2 / +0.0 | +0.4 / +0.2 / +0.0 | +0.4 / +0.2 / +0.0 |
| West | +0.6 / +0.5 / +0.0 | +0.6 / +0.5 / +0.0 | +0.6 / +0.5 / +0.0 |

## Sensitivity to the supply assumptions (each at its low and high end, others central; 2035)

| assumption | low / high | law: shortfall 2035 GW | law: regions below RML 2035 | data-sized BAAJA: shortfall change GW | + 10% Sec.2106: shortfall change GW | what it is |
|---|---|---|---|---|---|---|
| ret_hazard_old | 0.01 / 0.06 | 64 / 74 | 2.3 / 3.1 | -0.2 / -0.3 | -1.8 / -2.0 | annual retirement probability of coal, gas and oil units with no announced retirement once past the median age at retirement (coal 56, gas/oil 45 years) [A; ages D: EIA-860] |
| ret_announced | 0.6 / 1.0 | 63 / 68 | 2.5 / 2.6 | -0.2 / -0.3 | -1.9 / -1.9 | share of announced retirements (EIA-860/860M) that happen on schedule; low = delays such as the 2025 DOE 202(c) orders keeping coal units open |
| elcc_decline | 0.0 / 1.0 | 52 / 90 | 1.1 / 3.1 | -0.2 / -0.2 | -1.5 / -1.6 | how far on-peak shares of wind, solar and batteries fall by 2041: 0 = NERC 2025 national values throughout, 1 = PJM's 2041/42 preliminary ELCC ratings, linear in time |
| demand_growth_mult | 0.5 / 1.5 | 28 / 120 | 1.1 / 3.1 | -0.2 / -0.3 | -1.2 / -2.0 | multiplier on NERC's forecast growth in net internal demand (2026-35 path, extended to 2041 at the 2030-35 rate) |

## Checks against NERC

Existing fleet firm capacity in 2026 vs NERC's existing-certain resources; the ratio is applied to the existing fleet so that reserve margins are on NERC's basis. NERC's anticipated reserve margin counts only Tier 1 additions (signed contracts, under construction), so it falls faster than the model's after 2028.

| region | fleet firm GW 2026 (unscaled) | NERC existing-certain + transfers GW | scale applied | reserve margin 2030: NERC anticipated / model | 2035: NERC / model |
|---|---|---|---|---|---|
| CAISO | 67.5 | 76.4 | 1.13 | 42.7 / 22.8 | 33.3 / 11.0 |
| ERCOT | 112.4 | 93.9 | 0.83 | 29.9 / 59.1 | 22.8 / 88.2 |
| ISO-NE | 32.5 | 27.6 | 0.85 | 23.6 / 14.0 | 16.9 / 12.3 |
| MISO | 161.1 | 126.3 | 0.78 | 4.3 / 11.4 | -1.9 / 26.7 |
| NYISO | 42.3 | 37.4 | 0.87 | 22.5 / 25.3 | 15.4 / 22.7 |
| PJM | 196.7 | 189.7 | 0.96 | 13.9 / 14.9 | -0.3 / 3.5 |
| SPP | 67.3 | 71.5 | 1.06 | 22.6 / 31.3 | 16.0 / 41.3 |
| Southeast | 244.2 | 232.4 | 0.95 | 24.8 / 31.6 | 18.0 / 35.5 |
| West | 157.4 | 123.2 | 0.77 | 25.5 / 47.8 | 7.3 / 56.6 |
