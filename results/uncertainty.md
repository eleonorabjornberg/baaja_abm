# Joint uncertainty: all assumption ranges at once

400 Latin-hypercube samples per row, each paired current law vs BAAJA with its own seed and political path. Every [A] assumption (permitting, courts, halts, supply) is drawn from its range; values are drawn so the central value is the median. 'Grid dials' are the interconnection study-time cuts the bill does not size: Sec.2110 (0-5%) and Sec.2106 (0 to ERCOT's pace, RTO/ISO markets only). The grid-agents row replaces the dials with Phase 2's queue model and also draws its assumptions (entry, scarcity response, cost growth, re-study, transmission hosting; Sec.2106 adoption, published-location share, fee, Sec.2110 throughput, Sec.2109 hosting).

## Median [5th, 95th percentile] of BAAJA minus current law, by 2041 unless noted

New GW excludes relicensed hydro (existing plants kept in service).

| sample | new GW | renewable GW | gas GW | storage GW | suits 2026-41 | firm GW 2035 | shortfall GW 2035 | shortfall GW 2041 | current-law shortfall GW 2035 |
|---|---|---|---|---|---|---|---|---|---|
| grid dials at 0 (data-sized provisions) | +8.0 [+4.6, +13.1] | +6.6 [+3.5, +11.7] | +1.1 [+0.4, +2.0] | +0.3 [+0.0, +0.6] | -64.5 [-102.0, -30.0] | +1.6 [+0.8, +2.6] | -0.4 [-0.9, -0.1] | -0.9 [-2.5, -0.3] | 60 [21, 116] |
| grid dials across their ranges | +33.5 [+6.5, +188.7] | +20.8 [+5.1, +123.8] | +4.0 [+0.7, +16.9] | +7.6 [+0.1, +49.6] | -64.0 [-102.0, -30.0] | +5.1 [+1.0, +29.4] | -1.4 [-13.6, -0.1] | -4.5 [-39.9, -0.5] | 59 [22, 119] |
| grid agents (Phase 2), their assumptions drawn | +37.7 [+4.6, +90.1] | +25.5 [+4.2, +62.0] | +6.9 [+0.2, +16.7] | +5.7 [+0.2, +14.3] | -106.0 [-160.1, -57.0] | +7.6 [+0.8, +17.8] | -3.2 [-12.0, -0.1] | -3.9 [-18.0, -0.0] | 68 [27, 132] |

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
| GW new | 0.76 (without realised adoption 0.60; realised adoption alone 0.46) | adoption realised (share of RTO capacity) 54% [41, 64]; g_2110 12% [9, 15]; tx_hosting_gw 3% [1, 5]; screen_2106 3% [1, 5]; entry_wait_elast 2% [1, 3]; kappa 2% [1, 3]; hosting_2109 2% [1, 3]; restudy_rho 1% [0, 2] |
| shortfall change GW 2035 | 0.77 (without realised adoption 0.57; realised adoption alone 0.49) | adoption realised (share of RTO capacity) 68% [55, 83]; demand_growth_mult 13% [11, 18]; elcc_decline 6% [4, 9]; adopt_2106 1% [0, 4]; g_2110 1% [0, 3]; ix_rule_month 1% [0, 2]; ret_hazard_old 1% [0, 2]; ret_announced 1% [0, 2] |

| realised Sec.2106 adoption | new GW, BAAJA minus current law: median [5th, 95th] |
|---|---|
| no RTO adopts | +11.2 [+2.2, +48.2] |
| some adopt | +38.0 [+7.6, +86.2] |
| every RTO adopts | +67.2 [+32.6, +117.5] |
