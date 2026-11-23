# Simulation 6: electricity supply and resource adequacy

Supply = existing fleet (EIA-860, end-2025) minus retirements plus what the model's queue brings online, by LBNL region. Firm capacity, peak demand and the reference margin level (RML, the reserve margin a region plans to) follow NERC's 2025 Long-Term Reliability Assessment. Wind, solar and batteries count at an on-peak share that falls over time (central: halfway between NERC's 2025 national values and PJM's 2041/42 ratings). The model has no feedback from scarcity to building yet (Phase 2), so surpluses in some regions are not self-correcting and shortfalls are not filled by new entry.

## Current law: the United States

| peak year | peak demand GW (NERC) | installed GW | renewable / gas / storage / coal+oil GW | firm GW | reserve margin % | regions below RML (of 9) | shortfall GW | generation TWh |
|---|---|---|---|---|---|---|---|---|
| 2027 | 820 | 1311 | 429 / 509 / 80 / 183 | 988 | 20.5 [20.2, 20.8] | 1.9 | 8.4 [7.4, 9.5] | 4437 |
| 2030 | 883 | 1635 | 652 / 549 / 164 / 159 | 1128 | 27.8 [27.1, 28.6] | 1.5 | 20.6 [18.2, 22.9] | 4992 |
| 2035 | 952 | 1953 | 874 / 593 / 236 / 139 | 1224 | 28.6 [27.4, 29.6] | 2.2 | 67.8 [64.9, 70.7] | 5571 |
| 2041 | 1044 | 2241 | 1051 / 637 / 320 / 123 | 1276 | 22.2 [21.1, 23.5] | 2.8 | 129.2 [125.7, 132.6] | 6058 |

## Current law: by region (reserve margin, % of peak demand; 5th-95th percentile across runs)

| region | RML 2035 % | reserve margin 2030 % | reserve margin 2035 % | reserve margin 2041 % | runs below RML in 2035 | median first year below RML | shortfall 2035 GW |
|---|---|---|---|---|---|---|---|
| CAISO | 18.0 | 22.8 [21.0, 24.8] | 11.7 [9.7, 13.7] | -4.5 [-6.1, -2.2] | 100% | 2033 | 4.6 [3.1, 6.0] |
| ERCOT | 13.8 | 57.9 [53.7, 62.6] | 80.0 [74.9, 85.0] | 83.7 [78.8, 89.2] | 0% | - | 0.0 [0.0, 0.0] |
| ISO-NE | 13.0 | 14.3 [10.5, 18.0] | 15.0 [10.9, 19.1] | 11.7 [7.3, 16.9] | 21% | 2027 | 0.1 [0.0, 0.6] |
| MISO | 8.9 | 9.7 [7.6, 11.9] | 17.3 [14.8, 20.3] | 20.1 [16.4, 23.3] | 0% | 2027 | 0.0 [0.0, 0.0] |
| NYISO | 15.0 | 25.8 [22.8, 29.3] | 26.5 [22.5, 29.9] | 22.0 [18.3, 25.6] | 0% | - | 0.0 [0.0, 0.0] |
| PJM | 35.1 | 14.6 [13.3, 16.0] | 3.4 [1.9, 5.0] | -11.9 [-13.2, -10.6] | 100% | 2028 | 63.2 [60.0, 66.2] |
| SPP | 19.0 | 29.7 [25.8, 33.3] | 30.3 [25.9, 34.9] | 22.9 [17.7, 28.3] | 0% | - | 0.0 [0.0, 0.0] |
| Southeast | 15.0 | 30.7 [29.1, 32.7] | 30.0 [28.1, 32.7] | 26.8 [24.7, 29.6] | 0% | - | 0.0 [0.0, 0.0] |
| West | 12.8 | 47.0 [44.2, 50.0] | 54.1 [50.8, 57.5] | 50.2 [47.2, 53.3] | 0% | - | 0.0 [0.0, 0.0] |

## What BAAJA changes: the United States (difference from current law, paired)

| scenario | firm GW 2030 | firm GW 2035 | firm GW 2041 | shortfall GW 2035 | shortfall GW 2041 | regions below RML 2035 | TWh 2041 |
|---|---|---|---|---|---|---|---|
| BAAJA (data-sized provisions) | +0.3 [+0.1, +0.7] | +1.7 [+1.1, +2.4] | +3.2 [+2.4, +4.1] | -0.3 [-0.8, -0.1] | -0.6 [-1.0, -0.2] | -0.01 | +21 |
| BAAJA + Sec.2106 10% cut | +0.3 [+0.1, +0.7] | +6.5 [+5.0, +7.8] | +14.8 [+12.8, +16.9] | -2.1 [-2.9, -1.5] | -5.3 [-6.5, -4.0] | -0.12 | +75 |
| BAAJA + Sec.2106 ceiling (42% cut) | +0.3 [+0.1, +0.7] | +31.8 [+29.6, +34.7] | +74.9 [+71.2, +78.8] | -11.5 [-13.1, -9.7] | -27.9 [-30.1, -25.5] | -0.35 | +343 |

## What BAAJA changes: by region in 2035 (mean difference from current law)

| region | BAAJA (data-sized provisions): firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 10% cut: firm GW / margin pts / shortfall GW (2035) | BAAJA + Sec.2106 ceiling (42% cut): firm GW / margin pts / shortfall GW (2035) |
|---|---|---|---|
| CAISO | +0.1 / +0.1 / -0.1 | +0.6 / +0.8 / -0.6 | +3.6 / +5.0 / -3.5 |
| ERCOT | +0.2 / +0.2 / +0.0 | +0.2 / +0.2 / +0.0 | +0.2 / +0.2 / +0.0 |
| ISO-NE | +0.1 / +0.2 / -0.0 | +0.4 / +1.7 / -0.1 | +2.5 / +9.1 / -0.1 |
| MISO | +0.2 / +0.2 / +0.0 | +1.6 / +1.2 / +0.0 | +9.3 / +6.8 / +0.0 |
| NYISO | +0.1 / +0.4 / +0.0 | +0.7 / +2.0 / +0.0 | +3.8 / +11.3 / +0.0 |
| PJM | +0.2 / +0.1 / -0.2 | +1.4 / +0.7 / -1.4 | +7.9 / +4.0 / -7.9 |
| SPP | +0.1 / +0.1 / +0.0 | +0.7 / +1.1 / +0.0 | +3.9 / +5.9 / +0.0 |
| Southeast | +0.3 / +0.1 / +0.0 | +0.3 / +0.1 / +0.0 | +0.3 / +0.1 / +0.0 |
| West | +0.5 / +0.4 / +0.0 | +0.5 / +0.4 / +0.0 | +0.5 / +0.4 / +0.0 |

## Sensitivity to the supply assumptions (each at its low and high end, others central; 2035)

| assumption | low / high | law: shortfall 2035 GW | law: regions below RML 2035 | data-sized BAAJA: shortfall change GW | + 10% Sec.2106: shortfall change GW | what it is |
|---|---|---|---|---|---|---|
| ret_hazard_old | 0.01 / 0.06 | 63 / 73 | 2.0 / 2.7 | -0.3 / -0.3 | -2.0 / -2.2 | annual retirement probability of coal, gas and oil units with no announced retirement once past the median age at retirement (coal 56, gas/oil 45 years) [A; ages D: EIA-860] |
| ret_announced | 0.6 / 1.0 | 62 / 68 | 2.2 / 2.2 | -0.3 / -0.3 | -2.0 / -2.1 | share of announced retirements (EIA-860/860M) that happen on schedule; low = delays such as the 2025 DOE 202(c) orders keeping coal units open |
| elcc_decline | 0.0 / 1.0 | 51 / 91 | 1.0 / 3.3 | -0.2 / -0.3 | -1.8 / -2.2 | how far on-peak shares of wind, solar and batteries fall by 2041: 0 = NERC 2025 national values throughout, 1 = PJM's 2041/42 preliminary ELCC ratings, linear in time |
| demand_growth_mult | 0.5 / 1.5 | 28 / 120 | 1.0 / 3.6 | -0.2 / -0.4 | -1.4 / -2.9 | multiplier on NERC's forecast growth in net internal demand (2026-35 path, extended to 2041 at the 2030-35 rate) |

## Checks against NERC

Existing fleet firm capacity in 2026 vs NERC's existing-certain resources; the ratio is applied to the existing fleet so that reserve margins are on NERC's basis. NERC's anticipated reserve margin counts only Tier 1 additions (signed contracts, under construction), so it falls faster than the model's after 2028.

| region | fleet firm GW 2026 (unscaled) | NERC existing-certain + transfers GW | scale applied | reserve margin 2030: NERC anticipated / model | 2035: NERC / model |
|---|---|---|---|---|---|
| CAISO | 67.5 | 76.4 | 1.13 | 42.7 / 22.8 | 33.3 / 11.7 |
| ERCOT | 112.4 | 93.9 | 0.83 | 29.9 / 57.9 | 22.8 / 80.0 |
| ISO-NE | 32.5 | 27.6 | 0.85 | 23.6 / 14.3 | 16.9 / 15.0 |
| MISO | 161.1 | 126.3 | 0.78 | 4.3 / 9.7 | -1.9 / 17.3 |
| NYISO | 42.3 | 37.4 | 0.87 | 22.5 / 25.8 | 15.4 / 26.5 |
| PJM | 196.7 | 189.7 | 0.96 | 13.9 / 14.6 | -0.3 / 3.4 |
| SPP | 67.3 | 71.5 | 1.06 | 22.6 / 29.7 | 16.0 / 30.3 |
| Southeast | 244.2 | 232.4 | 0.95 | 24.8 / 30.7 | 18.0 / 30.0 |
| West | 157.4 | 123.2 | 0.77 | 25.5 / 47.0 | 7.3 / 54.1 |
