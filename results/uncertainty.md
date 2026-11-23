# Joint uncertainty: all assumption ranges at once

400 Latin-hypercube samples per row, each paired current law vs BAAJA with its own seed and political path. Every [A] assumption (permitting, courts, halts, supply) is drawn from its range; values are drawn so the central value is the median. 'Grid dials' are the interconnection study-time cuts the bill does not size: Sec.2110 (0-5%) and Sec.2106 (0 to ERCOT's pace, RTO/ISO markets only). The grid-agents row replaces the dials with Phase 2's queue model and also draws its assumptions (entry, scarcity response, cost growth, re-study, transmission hosting; Sec.2106 adoption, published-location share, fee, Sec.2110 throughput, Sec.2109 hosting).

## Median [5th, 95th percentile] of BAAJA minus current law, by 2041 unless noted

| sample | total GW | renewable GW | gas GW | storage GW | suits 2026-41 | firm GW 2035 | shortfall GW 2035 | shortfall GW 2041 | current-law shortfall GW 2035 |
|---|---|---|---|---|---|---|---|---|---|
| grid dials at 0 (data-sized provisions) | +10.0 [+6.1, +15.5] | +6.7 [+3.6, +11.7] | +1.1 [+0.4, +2.2] | +0.3 [+0.0, +0.6] | -71.0 [-111.0, -35.0] | +1.8 [+1.0, +3.0] | -0.3 [-0.7, -0.0] | -0.7 [-2.0, -0.2] | 66 [26, 124] |
| grid dials across their ranges | +35.3 [+7.8, +187.6] | +21.6 [+4.9, +123.7] | +3.8 [+0.4, +17.1] | +6.9 [+0.1, +48.6] | -71.0 [-111.0, -35.0] | +5.8 [+1.3, +29.8] | -1.0 [-10.1, -0.1] | -3.2 [-28.5, -0.4] | 69 [28, 121] |
| grid agents (Phase 2), their assumptions drawn | +32.5 [+7.1, +81.0] | +17.9 [+3.6, +49.1] | +9.0 [+0.9, +23.1] | +3.5 [-1.8, +11.1] | -166.0 [-230.1, -96.0] | +7.5 [+1.2, +18.8] | -1.0 [-7.0, -0.1] | -3.6 [-17.3, -0.0] | 74 [34, 134] |

## What drives the result (grid dials at 0 (data-sized provisions))

| result | R^2 (rank regression) | largest shares of variance |
|---|---|---|
| GW total | 0.70 | comply_2213 47%; nonnepa_hydro 11%; intake_pub 5%; deadline_bind 3%; ce_shift 2%; halt_mult_1401 2% |
| shortfall change GW 2035 | 0.19 | comply_2213 7%; demand_growth_mult 5%; intake_pub 1%; elcc_decline 1%; halt_mult_1401 1%; exhaust_injury 1% |

## What drives the result (grid dials across their ranges)

| result | R^2 (rank regression) | largest shares of variance |
|---|---|---|
| GW total | 0.92 | ix_2106 81%; ix_2110 12%; comply_2213 1%; deadline_bind 0%; ix_rule_month 0%; nonnepa_hydro 0% |
| shortfall change GW 2035 | 0.88 | ix_2106 82%; ix_2110 5%; demand_growth_mult 2%; ix_rule_month 1%; comply_2213 0%; deadline_bind 0% |

## What drives the result (grid agents (Phase 2), their assumptions drawn)

| result | R^2 (rank regression) | largest shares of variance |
|---|---|---|
| GW total | 0.67 | adopt_2106 17%; q_min_2106 16%; g_2110 10%; hosting_2109 5%; tx_hosting_gw 4%; kappa 3% |
| shortfall change GW 2035 | 0.57 | adopt_2106 24%; demand_growth_mult 12%; elcc_decline 5%; q_min_2106 3%; restudy_months 3%; g_2110 2% |
