# Joint uncertainty: all assumption ranges at once

400 Latin-hypercube samples per row, each paired current law vs BAAJA with its own seed and political path. Every [A] assumption (permitting, courts, halts, supply) is drawn from its range; values are drawn so the central value is the median. 'Grid dials' are the interconnection study-time cuts the bill does not size: Sec.2110 (0-5%) and Sec.2106 (0 to ERCOT's pace, RTO/ISO markets only). The grid-agents row replaces the dials with Phase 2's queue model and also draws its assumptions (entry, scarcity response, cost growth, re-study, transmission hosting; Sec.2106 adoption, published-location share, fee, Sec.2110 throughput, Sec.2109 hosting).

## Median [5th, 95th percentile] of BAAJA minus current law, by 2041 unless noted

New GW excludes relicensed hydro (existing plants kept in service).

| sample | new GW | renewable GW | gas GW | storage GW | suits 2026-41 | firm GW 2035 | shortfall GW 2035 | shortfall GW 2041 | current-law shortfall GW 2035 |
|---|---|---|---|---|---|---|---|---|---|
| grid dials at 0 (data-sized provisions) | +8.0 [+4.6, +13.1] | +6.6 [+3.5, +11.7] | +1.1 [+0.4, +2.0] | +0.3 [+0.0, +0.6] | -64.5 [-102.0, -30.0] | +1.6 [+0.8, +2.6] | -0.4 [-0.9, -0.1] | -0.9 [-2.5, -0.3] | 60 [21, 116] |
| grid dials across their ranges | +33.5 [+6.5, +188.7] | +20.8 [+5.1, +123.8] | +4.0 [+0.7, +16.9] | +7.6 [+0.1, +49.6] | -64.0 [-102.0, -30.0] | +5.1 [+1.0, +29.4] | -1.4 [-13.6, -0.1] | -4.5 [-39.9, -0.5] | 59 [22, 119] |
| grid agents (Phase 2), their assumptions drawn | +26.5 [+4.9, +64.0] | +16.8 [+3.3, +42.1] | +5.3 [+0.4, +14.0] | +3.5 [-1.0, +10.4] | -106.0 [-161.1, -57.0] | +5.5 [+0.8, +13.5] | -2.0 [-8.8, -0.1] | -3.4 [-15.3, +2.2] | 70 [25, 132] |

## What drives the result (grid dials at 0 (data-sized provisions))

| result | R^2 (rank regression) | largest shares of variance [bootstrap 90%] |
|---|---|---|
| GW new | 0.67 | comply_2213 52% [46, 59]; intake_pub 7% [4, 9]; deadline_bind 4% [2, 6]; ce_shift 2% [1, 5]; nepa_win_mult 2% [0, 3]; intake_pub_baaja 1% [0, 2]; ea_share_nonEIS 1% [0, 2]; inj_nonNEPA 0% [0, 1] |
| shortfall change GW 2035 | 0.35 | demand_growth_mult 13% [9, 19]; comply_2213 6% [3, 10]; elcc_decline 5% [2, 9]; deadline_bind 2% [1, 4]; ret_hazard_old 2% [0, 4]; intake_pub 2% [0, 4]; exhaust_injury 1% [0, 3]; lit_ce 1% [0, 2] |

## What drives the result (grid dials across their ranges)

| result | R^2 (rank regression) | largest shares of variance [bootstrap 90%] |
|---|---|---|
| GW new | 0.92 | ix_2106 76% [69, 83]; ix_2110 12% [10, 15]; comply_2213 1% [0, 1]; deadline_bind 0% [0, 0]; intake_oth 0% [0, 0]; intake_pub 0% [0, 0]; exhaust_injury 0% [0, 0]; ix_rule_month 0% [0, 0] |
| shortfall change GW 2035 | 0.89 | ix_2106 75% [68, 81]; ix_2110 6% [4, 8]; demand_growth_mult 3% [2, 4]; elcc_decline 1% [1, 2]; ix_rule_month 0% [0, 1]; comply_2213 0% [0, 1]; deadline_bind 0% [0, 1]; ret_announced 0% [0, 1] |

## What drives the result (grid agents (Phase 2), their assumptions drawn)

| result | R^2 (rank regression) | largest shares of variance [bootstrap 90%] |
|---|---|---|
| GW new | 0.67 (without realised adoption 0.59; realised adoption alone 0.26) | adoption realised (share of RTO capacity) 23% [14, 31]; g_2110 12% [8, 16]; screen_2106 7% [4, 10]; kappa 6% [4, 10]; hosting_2109 6% [3, 9]; restudy_months 2% [1, 4]; restudy_rho 2% [1, 4]; entry_wait_elast 2% [1, 4] |
| shortfall change GW 2035 | 0.67 (without realised adoption 0.55; realised adoption alone 0.28) | adoption realised (share of RTO capacity) 38% [27, 50]; demand_growth_mult 14% [10, 18]; restudy_months 6% [3, 9]; elcc_decline 4% [2, 7]; g_2110 2% [1, 4]; ret_hazard_old 1% [0, 3]; ret_announced 1% [0, 2]; hosting_2109 1% [0, 2] |

| realised Sec.2106 adoption | new GW, BAAJA minus current law: median [5th, 95th] |
|---|---|
| no RTO adopts | +13.3 [+3.2, +28.7] |
| some adopt | +26.5 [+5.1, +62.4] |
| every RTO adopts | +39.3 [+15.4, +71.4] |
