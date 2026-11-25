# Backcast 2010-2025, current law, vs EIA-860 additions and LBNL withdrawal timing

Phase 3 validation: backcast Jan 2010 - Dec 2025 under current law, with the exogenous grid (Sims 1-6) and with the grid agents (Sim 7), against EIA-860 additions nationally and by region, plus the withdrawal timing of the same request cohorts (2015-19) against LBNL. Requests by year come from LBNL, and in this backcast each request's region is drawn from LBNL's requests by region in its request year [D] (forward runs use 2021-25 shares).

Means over 10 runs per grid model. What was fitted to what: the exogenous model's withdrawal hazards to LBNL completion, in forward runs. The grid agents' operators to LBNL request-to-agreement times (2010-19 cohorts), and, in this backcast, their background withdrawal hazards to the shares of 2015-19 requests withdrawn within 12, 36 and 60 months (a first-year hazard, a later hazard and a hold after an adverse study result, by region) and their value scales to completion of 2010-19 requests (LBNL). The EIS probabilities and overdue windows are refitted with the agents on, and the storage settings were chosen with this backcast in view, so the backcast is not fully independent of the fit. Not fitted, so checks: EIA-860 additions nationally and by region, the 24-month withdrawal shares, and the 2020-2023 cohorts.

## National additions 2018-25

| technology | EIA-860 GW 2018-25 | exogenous grid: model GW (ratio) | grid agents: model GW (ratio) | by year 2018..2025 (exogenous / agents / EIA) |
|---|---|---|---|---|
| Solar | 127.2 | 104.1 (0.82) | 86.7 (0.68) | 4/4/5 5/6/6 7/7/11 11/9/14 15/12/11 18/14/20 20/16/31 24/17/30 |
| Onshore wind | 71.8 | 71.6 (1.00) | 59.8 (0.83) | 6/5/7 7/6/9 11/7/15 13/7/14 11/10/9 9/11/7 7/8/5 7/7/6 |
| Gas | 69.3 | 58.3 (0.84) | 55.9 (0.81) | 11/10/22 9/10/9 7/8/7 7/7/7 7/5/7 8/5/10 4/5/2 5/4/5 |
| Storage | 43.1 | 46.4 (1.08) | 18.5 (0.43) | 1/0/0 1/1/0 1/1/1 3/1/3 5/1/4 8/2/7 12/4/11 16/7/16 |

## By region, 2018-25

Weighted mean absolute log ratio of model to EIA additions across regions (all four technologies): exogenous 0.42, agents 0.52.

| region | Solar GW (exogenous / agents / EIA) | Onshore wind GW (exogenous / agents / EIA) | Gas GW (exogenous / agents / EIA) | Storage GW (exogenous / agents / EIA) | all four, exogenous / EIA | all four, agents / EIA |
|---|---|---|---|---|---|---|
| CAISO | 7.0 / 6.7 / 14.2 | 2.7 / 1.6 / 1.0 | 2.1 / 2.1 / 2.4 | 8.4 / 3.6 / 15.6 | 0.60 | 0.42 |
| ERCOT | 9.3 / 11.0 / 28.8 | 11.1 / 11.7 / 19.7 | 7.1 / 6.9 / 5.2 | 7.0 / 3.2 / 13.8 | 0.51 | 0.49 |
| ISO-NE | 5.4 / 4.0 / 2.8 | 2.4 / 1.9 / 0.4 | 4.1 / 3.7 / 3.1 | 1.7 / 0.4 / 0.7 | 1.93 | 1.41 |
| MISO | 6.8 / 4.7 / 19.9 | 17.4 / 11.1 / 15.9 | 9.0 / 7.4 / 10.2 | 0.7 / 0.2 / 0.8 | 0.72 | 0.50 |
| NYISO | 3.3 / 2.7 / 2.8 | 3.1 / 2.4 / 0.9 | 1.7 / 1.8 / 2.3 | 3.1 / 1.0 / 0.3 | 1.79 | 1.26 |
| PJM | 28.8 / 20.8 / 15.8 | 6.2 / 7.4 / 3.5 | 20.3 / 25.1 / 24.8 | 9.7 / 3.9 / 0.4 | 1.46 | 1.29 |
| SPP | 1.1 / 0.8 / 1.1 | 16.2 / 14.3 / 18.2 | 4.3 / 1.8 / 1.5 | 0.3 / 0.3 / 0.5 | 1.03 | 0.81 |
| Southeast | 19.0 / 16.1 / 23.1 | 1.3 / 0.4 / 0.6 | 5.4 / 4.0 / 16.2 | 2.5 / 0.9 / 2.0 | 0.67 | 0.51 |
| West | 23.6 / 20.0 / 18.2 | 11.3 / 9.0 / 11.5 | 4.4 / 3.0 / 3.9 | 13.1 / 4.9 / 8.5 | 1.25 | 0.88 |

### Each region's share of national additions, 2018-25 (%, exogenous / agents / EIA)

| technology | CAISO | ERCOT | ISO-NE | MISO | NYISO | PJM | SPP | Southeast | West |
|---|---|---|---|---|---|---|---|---|---|
| Solar | 7 / 8 / 11 | 9 / 13 / 23 | 5 / 5 / 2 | 6 / 5 / 16 | 3 / 3 / 2 | 28 / 24 / 12 | 1 / 1 / 1 | 18 / 19 / 18 | 23 / 23 / 14 |
| Onshore wind | 4 / 3 / 1 | 15 / 20 / 28 | 3 / 3 / 0 | 24 / 19 / 22 | 4 / 4 / 1 | 9 / 12 / 5 | 23 / 24 / 25 | 2 / 1 / 1 | 16 / 15 / 16 |
| Gas | 4 / 4 / 3 | 12 / 12 / 7 | 7 / 7 / 4 | 15 / 13 / 15 | 3 / 3 / 3 | 35 / 45 / 36 | 7 / 3 / 2 | 9 / 7 / 23 | 7 / 5 / 6 |
| Storage | 18 / 20 / 37 | 15 / 17 / 33 | 4 / 2 / 2 | 1 / 1 / 2 | 7 / 5 / 1 | 21 / 21 / 1 | 1 / 2 / 1 | 5 / 5 / 5 | 28 / 27 / 20 |

## Withdrawal timing of 2015-19 requests (same cohorts in model and data)

LBNL counts requests still active at end-2025 as not withdrawn; so does the model. ERCOT's early queue data hold few withdrawn requests (under 25 solar requests a year before 2016), so its LBNL withdrawal shares are probably too low.

| region | withdrawn by 12 months (exogenous / agents / LBNL) | withdrawn by 24 months (exogenous / agents / LBNL) | withdrawn by 36 months (exogenous / agents / LBNL) | withdrawn by 60 months (exogenous / agents / LBNL) |
|---|---|---|---|---|
| CAISO | 0.65 / 0.57 / 0.58 | 0.82 / 0.61 / 0.60 | 0.86 / 0.65 / 0.65 | 0.87 / 0.72 / 0.69 |
| ERCOT | 0.42 / 0.10 / 0.10 | 0.61 / 0.17 / 0.17 | 0.69 / 0.24 / 0.24 | 0.73 / 0.38 / 0.35 |
| ISO-NE | 0.53 / 0.29 / 0.29 | 0.72 / 0.40 / 0.40 | 0.79 / 0.50 / 0.50 | 0.82 / 0.63 / 0.59 |
| MISO | 0.65 / 0.17 / 0.16 | 0.82 / 0.40 / 0.43 | 0.86 / 0.56 / 0.56 | 0.88 / 0.75 / 0.62 |
| NYISO | 0.73 / 0.40 / 0.39 | 0.87 / 0.50 / 0.52 | 0.90 / 0.59 / 0.59 | 0.91 / 0.71 / 0.69 |
| PJM | 0.61 / 0.30 / 0.30 | 0.79 / 0.38 / 0.42 | 0.84 / 0.48 / 0.48 | 0.85 / 0.61 / 0.59 |
| SPP | 0.72 / 0.14 / 0.14 | 0.85 / 0.16 / 0.23 | 0.89 / 0.26 / 0.27 | 0.90 / 0.61 / 0.58 |
| Southeast | 0.58 / 0.47 / 0.46 | 0.78 / 0.55 / 0.58 | 0.84 / 0.62 / 0.61 | 0.86 / 0.72 / 0.71 |
| West | 0.59 / 0.09 / 0.09 | 0.79 / 0.23 / 0.24 | 0.84 / 0.42 / 0.42 | 0.86 / 0.69 / 0.68 |

### Holdout: 2020-2023 requests (used in no fit)

| region | withdrawn by 12 months (exogenous / agents / LBNL) | withdrawn by 24 months (exogenous / agents / LBNL) |
|---|---|---|
| CAISO | 0.72 / 0.59 / 0.12 | 0.85 / 0.63 / 0.46 |
| ERCOT | 0.61 / 0.10 / 0.05 | 0.76 / 0.17 / 0.09 |
| ISO-NE | 0.66 / 0.29 / 0.22 | 0.80 / 0.40 / 0.42 |
| MISO | 0.78 / 0.16 / 0.17 | 0.90 / 0.40 / 0.22 |
| NYISO | 0.81 / 0.40 / 0.72 | 0.91 / 0.51 / 0.86 |
| PJM | 0.66 / 0.30 / 0.13 | 0.83 / 0.38 / 0.18 |
| SPP | 0.82 / 0.13 / 0.30 | 0.91 / 0.15 / 0.55 |
| Southeast | 0.58 / 0.46 / 0.37 | 0.78 / 0.55 / 0.45 |
| West | 0.60 / 0.09 / 0.33 | 0.78 / 0.23 / 0.56 |
