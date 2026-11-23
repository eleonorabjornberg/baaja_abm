# Joint uncertainty: all assumption ranges at once

400 Latin-hypercube samples per row, each paired current law vs BAAJA with its own seed and political path. Every [A] assumption (permitting, courts, halts, supply) is drawn from its range; values are drawn so the central value is the median. 'Grid dials' are the interconnection study-time cuts the bill does not size: Sec.2110 (0-5%) and Sec.2106 (0 to ERCOT's pace, RTO/ISO markets only). The grid-agents row replaces the dials with Phase 2's queue model and also draws its assumptions (entry, scarcity response, cost growth, re-study, transmission hosting; Sec.2106 adoption, published-location share, fee, Sec.2110 throughput, Sec.2109 hosting).

## Median [5th, 95th percentile] of BAAJA minus current law, by 2041 unless noted

| sample | total GW | renewable GW | gas GW | storage GW | suits 2026-41 | firm GW 2035 | shortfall GW 2035 | shortfall GW 2041 | current-law shortfall GW 2035 |
|---|---|---|---|---|---|---|---|---|---|
| grid dials at 0 (data-sized provisions) | +9.8 [+6.0, +15.2] | +6.6 [+3.5, +11.7] | +1.1 [+0.4, +2.0] | +0.3 [+0.0, +0.6] | -64.5 [-102.0, -30.0] | +1.8 [+0.9, +2.9] | -0.3 [-0.7, -0.0] | -0.6 [-1.8, -0.1] | 69 [28, 121] |
| grid dials across their ranges | +34.3 [+7.8, +190.3] | +20.8 [+5.1, +123.8] | +4.0 [+0.7, +16.9] | +7.6 [+0.1, +49.6] | -64.0 [-102.0, -30.0] | +5.7 [+1.2, +30.1] | -1.1 [-10.6, -0.1] | -3.2 [-29.4, -0.3] | 65 [29, 124] |
| grid agents (Phase 2), their assumptions drawn | +31.3 [+6.7, +77.0] | +17.1 [+3.4, +44.4] | +7.5 [+0.9, +22.0] | +4.2 [-2.1, +11.4] | -110.0 [-169.0, -62.0] | +7.7 [+1.0, +21.4] | -1.5 [-7.9, -0.1] | -4.4 [-17.4, -0.2] | 73 [28, 139] |

## What drives the result (grid dials at 0 (data-sized provisions))

| result | R^2 (rank regression) | largest shares of variance |
|---|---|---|
| GW total | 0.68 | comply_2213 46%; nonnepa_hydro 12%; intake_pub 6%; deadline_bind 4%; ce_shift 3%; nepa_win_mult 1% |
| shortfall change GW 2035 | 0.27 | demand_growth_mult 8%; comply_2213 6%; intake_pub 2%; deadline_bind 2%; exhaust_injury 2%; ret_hazard_old 1% |

## What drives the result (grid dials across their ranges)

| result | R^2 (rank regression) | largest shares of variance |
|---|---|---|
| GW total | 0.92 | ix_2106 76%; ix_2110 12%; comply_2213 1%; deadline_bind 0%; intake_oth 0%; nonnepa_hydro 0% |
| shortfall change GW 2035 | 0.88 | ix_2106 76%; ix_2110 6%; demand_growth_mult 2%; ix_rule_month 1%; deadline_bind 0%; comply_2213 0% |

## What drives the result (grid agents (Phase 2), their assumptions drawn)

| result | R^2 (rank regression) | largest shares of variance |
|---|---|---|
| GW total | 0.66 | q_min_2106 19%; adopt_2106 17%; hosting_2109 9%; g_2110 5%; kappa 4%; planned_share_2106 3% |
| shortfall change GW 2035 | 0.48 | adopt_2106 22%; demand_growth_mult 12%; elcc_decline 4%; ret_hazard_old 3%; restudy_months 1%; planned_share_2106 1% |
