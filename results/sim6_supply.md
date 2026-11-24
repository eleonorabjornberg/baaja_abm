# Simulation 6: electricity supply and resource adequacy

Supply = existing fleet (EIA-860, end-2025) minus retirements plus what the model's queue brings online, by LBNL region. On-peak accredited capacity ("firm" below), peak demand and the reference margin level (RML, the reserve margin a region plans to) follow NERC's 2025 Long-Term Reliability Assessment. Wind, solar and batteries count at an on-peak share that falls over time (central: halfway between NERC's 2025 national values and PJM's 2041/42 ratings), except in PJM, whose reference margin is an installed-capacity margin that already rises as accreditation falls. This simpler model has no feedback from scarcity to building, so surpluses in some regions are not self-correcting and shortfalls are not filled by new entry; the grid-agent model (Sim 7) adds an entry response.

## Current law: the United States

| peak year | peak demand GW (NERC) | installed GW | renewable / gas / storage / coal+oil GW | firm GW | reserve margin % | regions below RML (of 9) | shortfall GW | generation TWh |
|---|---|---|---|---|---|---|---|---|
| 2027 | 820 | 1311 | 429 / 509 / 80 / 183 | 985 | 20.1 [19.8, 20.3] | 2.0 | 9.4 [8.6, 10.3] | 4437 |
| 2030 | 883 | 1635 | 652 / 549 / 164 / 159 | 1103 | 25.0 [24.3, 25.6] | 2.6 | 23.8 [21.0, 26.7] | 4992 |
| 2035 | 952 | 1953 | 874 / 593 / 236 / 139 | 1187 | 24.7 [23.8, 25.6] | 3.4 | 58.9 [55.4, 62.1] | 5571 |
| 2041 | 1044 | 2241 | 1051 / 637 / 320 / 123 | 1240 | 18.8 [17.8, 19.8] | 3.6 | 106.6 [102.5, 111.0] | 6058 |

## Current law: by region (reserve margin, % of peak demand; 5th-95th percentile across runs)

| region | RML 2035 % | reserve margin 2030 % | reserve margin 2035 % | reserve margin 2041 % | runs below RML in 2035 | median first year below RML | shortfall 2035 GW |
|---|---|---|---|---|---|---|---|
| CAISO | 18.0 | 22.8 [21.0, 24.8] | 11.7 [9.7, 13.7] | -4.5 [-6.1, -2.2] | 100% | 2033 | 4.6 [3.1, 6.0] |
| ERCOT | 13.8 | 49.2 [45.6, 53.0] | 65.8 [61.6, 70.0] | 66.9 [62.8, 71.5] | 0% | - | 0.0 [0.0, 0.0] |
| ISO-NE | 13.0 | 12.7 [9.5, 15.9] | 11.8 [8.3, 15.2] | 7.3 [3.5, 11.6] | 71% | 2027 | 0.4 [0.0, 1.3] |
| MISO | 8.9 | 4.2 [2.5, 5.9] | 8.4 [6.5, 10.7] | 9.2 [6.3, 11.6] | 66% | 2027 | 1.2 [0.0, 3.3] |
| NYISO | 15.0 | 24.2 [21.5, 27.1] | 23.5 [19.9, 26.5] | 18.1 [14.8, 21.2] | 0% | - | 0.0 [0.0, 0.0] |
| PJM | 35.1 | 16.1 [14.7, 17.4] | 8.6 [7.1, 10.3] | -1.4 [-3.0, 0.1] | 100% | 2028 | 52.8 [49.4, 55.8] |
| SPP | 19.0 | 29.7 [25.8, 33.3] | 30.3 [25.9, 34.9] | 22.9 [17.7, 28.3] | 0% | - | 0.0 [0.0, 0.0] |
| Southeast | 15.0 | 29.8 [28.4, 31.8] | 28.6 [26.8, 31.2] | 25.1 [23.2, 27.8] | 0% | - | 0.0 [0.0, 0.0] |
| West | 12.8 | 38.0 [35.9, 40.3] | 39.8 [37.3, 42.4] | 34.1 [31.8, 36.5] | 0% | - | 0.0 [0.0, 0.0] |

## What BAAJA changes: the United States (difference from current law, paired)

| scenario | firm GW 2030 | firm GW 2035 | firm GW 2041 | shortfall GW 2035 | shortfall GW 2041 | regions below RML 2035 | TWh 2041 |
|---|---|---|---|---|---|---|---|
| BAAJA (data-sized provisions) | +0.3 [+0.1, +0.6] | +1.5 [+0.9, +2.2] | +2.9 [+2.2, +3.7] | -0.5 [-0.9, -0.1] | -0.9 [-1.4, -0.4] | -0.05 | +21 |
| BAAJA + Sec.2106 10% cut | +0.3 [+0.1, +0.6] | +6.1 [+4.7, +7.4] | +15.0 [+12.9, +16.9] | -3.2 [-4.3, -2.1] | -8.0 [-10.1, -6.4] | -0.53 | +75 |
| BAAJA + Sec.2106 ceiling (42% cut) | +0.3 [+0.1, +0.6] | +30.5 [+28.1, +33.0] | +77.4 [+74.0, +81.5] | -14.7 [-18.4, -12.0] | -39.4 [-43.6, -36.5] | -1.50 | +343 |

## What BAAJA changes: by region in 2035 (mean difference from current law)

| region | BAAJA (data-sized provisions): firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 10% cut: firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 ceiling (42% cut): firm GW / margin pts / shortfall GW (2035) |
|---|---|---|---|
| CAISO | +0.1 / +0.1 / -0.1 | +0.6 / +0.8 / -0.6 | +3.6 / +5.0 / -3.5 |
| ERCOT | +0.2 / +0.2 / +0.0 | +0.2 / +0.2 / +0.0 | +0.2 / +0.2 / +0.0 |
| ISO-NE | +0.1 / +0.2 / -0.0 | +0.4 / +1.4 / -0.2 | +2.1 / +7.7 / -0.4 |
| MISO | +0.2 / +0.1 / -0.1 | +1.3 / +0.9 / -0.7 | +7.2 / +5.3 / -1.2 |
| NYISO | +0.1 / +0.3 / +0.0 | +0.6 / +1.8 / +0.0 | +3.3 / +9.8 / +0.0 |
| PJM | +0.2 / +0.1 / -0.2 | +1.7 / +0.9 / -1.7 | +9.6 / +4.8 / -9.6 |
| SPP | +0.1 / +0.1 / +0.0 | +0.7 / +1.1 / +0.0 | +3.9 / +5.9 / +0.0 |
| Southeast | +0.3 / +0.1 / +0.0 | +0.3 / +0.1 / +0.0 | +0.3 / +0.1 / +0.0 |
| West | +0.4 / +0.3 / +0.0 | +0.4 / +0.3 / +0.0 | +0.4 / +0.3 / +0.0 |

## Sensitivity to the supply assumptions (each at its low and high end, others central; 2035)

| assumption | low / high | law: shortfall 2035 GW | law: regions below RML 2035 | data-sized BAAJA: shortfall change GW | + 10% Sec.2106: shortfall change GW | what it is |
|---|---|---|---|---|---|---|
| ret_hazard_old | 0.01 / 0.06 | 53 / 67 | 2.5 / 4.1 | -0.4 / -0.5 | -2.5 / -3.9 | annual retirement probability of coal, gas and oil units with no announced retirement once past the median age at retirement (coal 56, gas/oil 45 years) [A; ages D: EIA-860] |
| ret_announced | 0.6 / 1.0 | 52 / 59 | 2.6 / 3.4 | -0.3 / -0.5 | -2.5 / -3.2 | share of announced retirements (EIA-860/860M) that happen on schedule; low = delays such as the 2025 DOE 202(c) orders keeping coal units open |
| elcc_decline | 0.0 / 1.0 | 53 / 78 | 1.0 / 4.1 | -0.2 / -0.5 | -1.7 / -3.6 | how far on-peak shares of wind, solar and batteries fall by 2041: 0 = NERC 2025 national values throughout, 1 = PJM's 2041/42 preliminary ELCC class ratings, linear in time (not in PJM, whose installed reserve margin already rises with the mix) |
| demand_growth_mult | 0.5 / 1.5 | 18 / 121 | 1.0 / 4.5 | -0.2 / -0.6 | -1.7 / -4.2 | multiplier on NERC's forecast growth in net internal demand (2026-35 path, extended to 2041 at the 2030-35 rate) |

## Checks against NERC

Existing fleet firm capacity in 2026 vs NERC's existing-certain resources; the ratio is applied to the existing fleet so that reserve margins are on NERC's basis. NERC's anticipated reserve margin counts only Tier 1 additions (signed contracts, under construction), so it falls faster than the model's after 2028.

| region | fleet firm GW 2026 (unscaled) | NERC existing-certain + transfers GW | scale applied | reserve margin 2030: NERC anticipated / model | 2035: NERC / model |
|---|---|---|---|---|---|
| CAISO | 67.5 | 76.4 | 1.13 | 42.7 / 22.8 | 33.3 / 11.7 |
| ERCOT | 112.4 | 93.9 | 0.83 | 29.9 / 49.2 | 22.8 / 65.8 |
| ISO-NE | 32.5 | 27.6 | 0.85 | 23.6 / 12.7 | 16.9 / 11.8 |
| MISO | 161.1 | 126.3 | 0.78 | 4.3 / 4.2 | -1.9 / 8.4 |
| NYISO | 42.3 | 37.4 | 0.87 | 22.5 / 24.2 | 15.4 / 23.5 |
| PJM | 196.7 | 189.7 | 0.96 | 13.9 / 16.1 | -0.3 / 8.6 |
| SPP | 67.3 | 71.5 | 1.06 | 22.6 / 29.7 | 16.0 / 30.3 |
| Southeast | 244.2 | 232.4 | 0.95 | 24.8 / 29.8 | 18.0 / 28.6 |
| West | 157.4 | 123.2 | 0.77 | 25.5 / 38.0 | 7.3 / 39.8 |
