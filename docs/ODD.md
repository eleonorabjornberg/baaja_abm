# Model description (ODD protocol)

This follows the ODD protocol for agent-based models (Overview, Design concepts, Details; Grimm et al. 2020 update).
Code references are to `baaja/`. Every parameter is tagged in `baaja/params.py` as data [D], with its source in
`data/SOURCES.md`, or assumption [A], with a low / central / high range (README, assumption register).

## 1. Purpose and patterns

**Purpose.** Estimate how S.5653, the Bipartisan American Affordability and Jobs Act of 2026 (BAAJA; Senate-passed
substitute to H.R. 2347, 19 Nov 2026), changes US electricity supply from Nov 2026 to Oct 2041. The output is new
capacity by technology, region and year, and resource adequacy (on-peak accredited capacity against NERC reference margin levels), each
compared with current law in paired runs. The model is built to separate what the bill text and the data can size
from what depends on how agencies, FERC and RTOs implement it.

**Patterns the model must reproduce** (calibration targets and checks, section 7.8):
1. LBNL queue completion by technology and region (share of requests that reach operation).
2. LBNL request -> interconnection agreement times by request cohort, region by region, including MISO's lengthening
   from about 19 to about 50 months (2010-19 fitted, 2020-24 held out).
3. The timing of withdrawal: shares of 2015-19 requests withdrawn by 12, 24, 36 and 60 months, by region.
4. CEQ's count of environmental impact statements a year by technology; BLM filing -> NEPA notice times (MLRS).
5. NEPA case outcomes 2001-22: challenger mix, win rates, injunctions, vacatur, case length.
6. EIA-860 additions 2018-25, nationally and by region (backcast, not fitted), and EIA-860's 2024-25 additions in
   the first model year.
7. NERC 2025 LTRA anticipated reserve margins for 2026 (supply accounting check).

## 2. Entities, state variables and scales

| entity | number | state variables |
|---|---|---|
| **Project** (request) | ~10,000-20,000 per run | technology; request month `t0`; region (one of 9); ISO / non-ISO market; federal nexus; review kind (CE / EA / EIS); permit-decision month; sponsor withdrawal clock `W`; challenger type; sued / injunction / lost / vacated / killed; halted; signed-agreement month `tIA`; construction time; operation month `tCOD`; grid mode only: private value ($/kW), allocated upgrade cost, published-location flag, grid-withdrawal month `gwd`, entered or not |
| **Grid operator** (grid mode) | 9, one per LBNL region | cluster window `C`; serial or parallel studies; minimum study months `d`; throughput `K` (requests/month) and its adaptation rate; legacy queue; cluster in study and its finish month; GW signed since month 0; hosting room from transmission; Sec.2106 adoption (drawn once per RTO) |
| **Developer** (grid mode) | one per generation request | the project's value, cost and decision rules (section 7.5) |
| **Transmission project** | Poisson arrivals | as a project, without an interconnection queue; in grid mode its completion adds hosting room in a region |
| **Court / challenger** | implicit | per-suit draws of filing, timeliness, injunction, outcome, vacatur |
| **Administration** | 4 turnovers (2029, 2033, 2037, 2041) | hostile to renewables or to fossil projects (a political path per run) |
| **Region (supply)** | 9 | existing fleet by technology group and vintage, announced retirements, demand, firm transfers, reference margin |

Technologies: solar (106 MW per request), onshore wind (208), offshore wind (800), gas (222), storage (104),
geothermal (40), transmission, hydro relicensing (50). Sizes are LBNL medians (MW-weighted where relevant).

**Scales.** Time step one month; horizon 180 months (Nov 2026 - Oct 2041; supply reported by peak year 2027-2041).
Backcast: Jan 2010 - Dec 2025. Space: the nine LBNL regions (CAISO, ERCOT, ISO-NE, MISO, NYISO, PJM, SPP,
Southeast, West), mapped to NERC assessment areas for demand. No geography within a region.

## 3. Process overview and scheduling

For each run (seed, political path, parameter set):

1. **Arrivals.** New requests by technology arrive as a Poisson process at the 2021-25 LBNL rate (or the 2025 rate in
   the second regime). Requests active in the LBNL queue at end-2025 are seeded with their observed ages and
   agreement status.
2. **Region and market.** Each request draws its region from LBNL request shares (2021-25 for new requests, the
   active queue for seeded ones; by request year in the backcast).
3. **Federal review** (projects with a federal nexus): review kind, months to the NEPA notice (intake), review
   length, ESA consultation, deadlines (current law or BAAJA), giving a permit-decision month.
4. **Sponsor withdrawal clock**: a regional monthly hazard of withdrawal for reasons outside the model.
5. **Grid access**, either
   - *exogenous* (Sims 1-6): a lognormal study time from LBNL request -> agreement times, shortened by the
     Sec.2106/2110 dials; or
   - *agents* (Sim 7): a monthly loop over months per region (operators run clusters; developers enter, stay or
     withdraw; transmission adds hosting room), section 7.5.
6. **Litigation** on projects still alive at their permit decision: suit, timeliness and standing (BAAJA), injunction,
   outcome, vacatur and remand, cancellation.
7. **Construction** starts at the later of permit and agreement and lasts the measured agreement -> operation time.
8. **Executive halts** at each hostile turnover hit permitted projects not yet online, with a delay and a chance of
   cancellation.
9. **Outcome.** A project is online if it was not withdrawn (clock ran out before construction, or a grid decision)
   or killed, and its operation month is within the horizon.
10. **Supply accounting** (post-processing): existing fleet minus retirements plus additions, firm capacity, reserve
    margin and shortfall against NERC's reference margin, by region and peak year.

Within the grid loop the order each month is: transmission completions update hosting room; the operator publishes
its expected wait; new requests decide whether to enter; throughput adapts; legacy requests are studied oldest first;
clusters whose window has closed (and, in serial regions, whose predecessor is finished) start; study results and
agreements are issued on their dates, and developers decide.

## 4. Design concepts

- **Basic principles.** A project reaches operation only through two parallel gates (federal permit, if any, and
  grid interconnection), and the time it waits exposes it to withdrawal. The bill acts by changing review times and
  types, litigation, halts and the interconnection process; its supply effect is the change in projects that finish.
- **Emergence.** In grid mode, study time, withdrawal, upgrade costs and entry are outcomes of queue volume, operator
  throughput, other developers' decisions and transmission build-out, not inputs. The national effect of Sec.2106
  emerges from which RTOs adopt and how many requests are deterred or kept.
- **Adaptation.** Developers stay if their allocated cost is below their value (raised by regional scarcity); they
  enter less when the published wait is longer and more when their region's projected shortfall grows; under
  Sec.2106(a)(3) they do not enter when their chance of completing is below a threshold. Operators adapt throughput to
  the arrival rate.
- **Objectives.** Developers: proceed while expected value exceeds cost. Operators have no objective; they follow
  fitted rules.
- **Prediction.** Developers use the operator's published wait (backlog / throughput) and the firm capacity expected
  online 4 years ahead in their region (agreements signed so far, built on measured construction times).
- **Sensing.** Developers see their own cost at study results, the published wait, and regional scarcity; not other
  developers' values.
- **Interaction.** Through the operator: withdrawals raise re-study costs for those who stay; capacity signed raises
  later upgrade costs (`kappa`), net of transmission hosting room; a long backlog lengthens everyone's study and deters
  entry. Through supply: firm capacity signed lowers scarcity and so entry.
- **Stochasticity.** Every random draw is made for every project in every scenario in the same order (common random
  numbers); each decision uses its own uniform. Draws added in later versions use their own streams, so earlier
  results reproduce exactly. Current law and BAAJA with the same seed and political path differ only through the
  policy, which gives paired differences with far less noise than independent runs.
- **Collectives.** Clusters of requests studied together; RTOs as a group under Sec.2106.
- **Observation.** By technology, region and model year: GW online, completion, months to permit and to operation,
  suits, wins, vacatur, halts; grid mode adds study times, withdrawal by month, entry and costs; supply adds firm GW,
  reserve margins and shortfall below the reference margin. Results are means with 5-95% intervals over paired runs
  (seed noise) and over joint Latin-hypercube samples (all assumption ranges).

## 5. Initialization

Month 0 is Nov 2026. The LBNL active queue at end-2025 is seeded by technology with observed request ages and the
share holding a signed interconnection agreement; seeded projects with an agreement are part-way through construction
(time since agreement drawn from LBNL agreement dates). The existing fleet is EIA-860 (end-2025, plus EIA-860M through
Sep 2026 for announced retirements). In grid mode each operator starts from its fitted throughput carried to Nov 2026
at the 2025 arrival rate. The political path (which side each administration is hostile to) is drawn per run unless a
scenario fixes it.

## 6. Input data

All raw files are listed with URL, date and hash in `data/SOURCES.md`; extractors in `data/` write the JSON summaries
the model reads. Main sources: LBNL "Queued Up" (queue data through 2025) and interconnection cost studies; EIA-860,
860M and 923; NERC 2025 Long-Term Reliability Assessment; CEQ EIS timelines; BLM ePlanning and MLRS; a 1,821-case
NEPA litigation export (2001-22); FHWA/FTA statute-of-limitations litigation (natural experiment for the 150-day
limit); FWS habitat conservation plans; ERCOT and RTO queue benchmarks; the bill text (GovInfo, Senate PDFs).

## 7. Submodels

### 7.1 Arrivals and regions
Poisson arrivals at LBNL's 2021-25 average requests a year by technology (`regime="2025"`: 2025 requests).
Region by inverse CDF of request shares within the drawn ISO / non-ISO market (`model.draw_region`); backcast by
request year (`draw_region_by_year`).

### 7.2 Federal review
Federal nexus with probability by technology [D: federal hooks, BLM land, Corps permits, HCPs]. Review kind: EIS with
probability `p_eis` (calibrated to CEQ EIS counts), else EA with share `ea_share_nonEIS` [D], else CE. Review length
lognormal around kind medians [D: CEQ, BLM]. Federal-land intake: lognormal around the MLRS median (10.5 months).
BAAJA: Sec.1106 deadlines (1 year EA, 2 years EIS, +4 months) bind for a share `deadline_bind`; Sec.1105/1108 move a
share `ce_shift` of EAs to CEs; Sec.2102 reconductoring CEs; Sec.2229 geothermal; Sec.2213 caps federal-land intake
at 4 months where met (`comply_2213`); Sec.1402(c) 1-year CE cap; Sec.1202 hydro months outside NEPA.

### 7.3 Withdrawal clock
`W = ceil(log(1-u) / log(1-h))` months, with `h` the regional hazard fitted to LBNL completion (exogenous mode). In grid
mode the background clock has a first-year and a later hazard (`grid.pre_clock`), fitted in the backcast. Withdrawal
happens if `W` runs out before construction starts (wait = time to start + litigation and halt delay).

### 7.4 Litigation and halts
Suit probability by review kind and technology [D: district-court suits per BLM + DOE review, 2012-21; NEPA case
export]. Current law: injunction, challenger win (by challenger type, x1.6 for a deadline-truncated review), vacatur
and remand (12 months), cancellation after vacatur. Post-*Seven County* baseline: win, injunction and vacatur scaled
by `nepa_win_mult`, suits by `nepa_suit_mult`, in both runs. BAAJA (Sec.1110/2201): 150-day limit (late filers adapt
by `late_adapt` [D]), comment exhaustion and direct injury (`exhaust_injury`), remand-only remedy (fewer suits,
`suit_payoff`; injunctions only on non-NEPA claims, `inj_nonNEPA`), appeals-court case length. Halts: after each hostile
turnover, permitted projects not yet online are halted with probability by technology [D for offshore wind 2025], for
`halt_len` months, cancelled with `p_kill_halt`; Sec.1401 scales the probability by `halt_mult_1401`.

### 7.5 Grid agents (`baaja/grid.py`)
- **Operator replay and fit.** Requests close into clusters every `C` months (12; ERCOT 1, individual studies). A
  serial operator starts a cluster when the previous one is done; it takes `max(d, live requests / K)` months, with a
  lognormal spread within the cluster. `K` follows the trailing 12-month arrival rate at rate `lambda`. `(d, K0,
  lambda, sigma)` are fitted by grid search on LBNL 2010-19 cohorts (MISO, CAISO, ERCOT each; other regions a pooled
  MISO+CAISO fit) to censoring-consistent medians and signed shares; 2020-24 cohorts are a holdout.
- **Developer value and cost.** Value per kW lognormal [D: LBNL P(complete | upgrade cost)], scaled by technology and
  region (`value_mult`, fitted so completion matches LBNL). Upgrade cost lognormal by region, with LBNL's share of
  requests at zero cost paying nothing [D: LBNL cost studies], times `exp(kappa x (GW signed since 2026 - hosting
  room) / regional fleet GW)`. `kappa` is 0 / 2.17 / 5.14 (low / central / high): central is the median of MISO, SPP
  and PJM, the three cluster markets where LBNL costs rose between 2010-17 and 2018+ requests; high is PJM; low is 0,
  because three regions cannot pin the rate down. NYISO and the Southeast give negative rates and the West (3.7 GW
  connected over a 183 GW fleet) an implausibly large one, so they are not used. ERCOT has `kappa` = 0: it does not
  allocate network upgrades to generators, and its LBNL costs are point-of-interconnection only.
- **Decisions.** At the first study result (R = `restudy_months` before the agreement in cluster regions) a developer
  stays if cost <= value x exp(beta x change in scarcity); withdrawals raise the others' cost by `restudy_rho` x the
  withdrawn MW share and they decide again at the agreement. A developer who leaves holds its queue position for an
  exponential time with regional mean `exit_lag` before the withdrawal is recorded.
- **Entry.** Requests enter with probability `min(mult, 1)`, and extra candidate requests (up to `entry_max` x the base
  rate) enter with probability `(mult - 1) / (entry_max - 1)`, where `mult = (W_ref / W_pub)^entry_wait_elast x
  exp(scarcity_beta x change in scarcity)`, bounded to [0.2, `entry_max`] (the lower bound keeps at least a fifth of
  requests entering however long the published wait; an assumption). The scarcity signal uses central demand and
  supply assumptions, and is off in the backcast. Current law has no entry screen; Sim 7's sensitivity adds one
  (`q_min_law` = 0.1, for Order 2023's readiness deposits) to both runs.
- **Transmission.** Transmission projects through the same permitting and court pipeline; each completion adds
  `tx_hosting_gw` of room in a region drawn by generation request shares. Only the bill's change in transmission
  relative to current law (same draws) moves costs; the historical pace is in `kappa`.
- **Bill.** Sec.2106 in RTOs that adopt (probability `adopt_2106`, drawn per RTO), from the rule month: a share
  `planned_share_2106` of new requests use a published location at a fixed fee (`fee_mult_2106` x the region's
  expected upgrade cost, zero-cost requests included, times the congestion multiplier; 1 = the fee recovers the
  expected cost; no cost shock, no re-study); one decision at the first result; requests whose chance of completing
  (upgrade cost below value) is below `q_min_2106` do not enter, standing for non-refundable security and withdrawal
  penalties; the post-result hold shrinks by `lag_2106`. Requests made before the rule month keep the current
  process (an assumption: new s.228 has no transition clause). `ix_rule_month` (24 / 36 / 48) is an assumption; the
  statute gives FERC 18 months for the rule and providers 2 years to file. Sec.2110: throughput x (1 + `g_2110`)
  outside ERCOT. Sec.2109: hosting room x (1 + `hosting_2109`) for projects after the rule month.

### 7.6 Construction
Agreement -> operation: LBNL measured medians by technology (2022-25). Exogenous mode for new requests: a build time
fitted to LBNL completion timing. Seeded projects past the usual time finish within a calibrated window.

### 7.7 Supply and adequacy (`baaja/supply.py`)
Existing fleet by region and group with announced retirements (share on schedule `ret_announced`) and an age hazard
for coal, gas and oil past the median retirement age (`ret_hazard_old`). On-peak accredited capacity (`firm`
in the code): dispatchable at net summer capacity; wind, solar, storage at NERC 2025 on-peak shares, declining towards
PJM's 2041/42 ELCC class ratings by `elcc_decline`, except in PJM, whose reference margin is an installed reserve
margin that already rises (18.6% to 35.1%) as the mix shifts to these resources, so its shares stay at 2026 values;
a per-region factor to NERC's existing-certain basis in 2026, applied to additions too where it is below 1 (MISO's
accredited basis); plus NERC firm transfers. Demand: NERC
net internal demand, growth scaled by `demand_growth_mult`, extended past 2035 at the 2030-35 rate. Shortfall =
max(0, (1 + reference margin) x demand - firm).

### 7.8 Calibration, validation and uncertainty
- Calibration (`baaja/calibrate.py`): EIS probabilities to CEQ counts; regional withdrawal hazards to LBNL completion;
  overdue window to EIA-860's 2024-25 additions; grid operators to request -> agreement times; grid background hazards,
  post-result hold and value scales in the 2010-25 backcast to the 12-, 36- and 60-month withdrawal shares and
  completion (24 months a check).
- Validation (`baaja/validation.py`, `results/backcast.md`): EIA-860 2018-25 additions by technology and region, LBNL
  withdrawal timing of the same cohorts, 2020-23 holdout.
- Uncertainty (`baaja/uncertainty.py`): Latin hypercube over every assumption range (drawn so the central value is
  the median), each sample a paired current law / BAAJA run with its own seed and political path; variance shares from
  rank regression.

## 8. Reproducibility

`pip install -r requirements.txt`; `python run.py --all --runs 100` recalibrates and regenerates every result and
figure; `python run.py --uncertainty 400`; `python run.py --backcast`; `python -m pytest -q`. Seeds are fixed in the
code; the same commit and inputs give the same numbers. Raw downloads are not committed (`raw/`, git-ignored); their
hashes are in `data/SOURCES.md` and the extracted JSON summaries are committed.
