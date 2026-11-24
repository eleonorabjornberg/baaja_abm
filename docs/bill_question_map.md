# Seven simulations: BAAJA sections -> model -> data

**Bill version.** The model follows the **Senate-passed text**: the amendment in the nature of a substitute to H.R. 2347
offered by Sens. Capito, Lee, Whitehouse and Heinrich (Senate file KAT26804 V62), which carries BAAJA as Divisions A and
B (S.Amdt. 6883). The Senate passed H.R. 2347 with this amendment on 19 Nov 2026, 62-33; it now goes to the House.
The engrossed Senate amendment (GovInfo, BILLS-119hr2347eas) was checked against the floor copy: every modelled
section is identical word for word.
The introduced bill was S.5653 (30 Sep 2026); section numbers below are the same in both unless noted. Scope: US
electricity, renewables vs gas. Model code: `baaja/sims/simN_*.py`; results: `results/simN_*.md`. Status: **modelled**
(with data or an assumption range), **listed** (in the bill, not simulated, reason given).

## What the substitute changed that matters for the model (S.5653 as introduced -> Senate-passed text)

| Section | Change | Model consequence |
|---|---|---|
| 2106 | applies to each **Transmission Organization** (RTO/ISO) instead of each transmission planning region; fee is "subregional" instead of "zonal"; adds storage and transmission-service locations, a co-optimization aim, and 2106(d): FERC may find existing processes compliant | Sec.2106 applies in the six FERC-jurisdictional RTOs/ISOs only (`ix_cut_rto`; Sim 7 `adopt_2106`); 2106(d) strengthens the 0% floor. The introduced text already excluded ERCOT ("transmission planning region" as defined in new s.225(a), which excludes it), so the change removes the Southeast and the non-ISO West |
| 1401 | permits in effect on/after **6 Nov 2026** (was 16 Sep); new exception (F): action "taken pursuant to any applicable law or regulation"; "materially" added to amend/alter | `halt_mult_1401` range 0.1 / 0.5 / 1.0 (was 0 / 0.1 / 0.3) |
| 2213 | unchanged: 30-day completeness, 90-day NOI if an EIS is needed, decision or deferral within 30 days; still no enforcement | `comply_2213` 0.25 / 0.5 / 1.0 |
| 2101 | offshore transmission removed from FERC backstop eligibility; "just and reasonable rates" added as a criterion | transmission permitting time; in Sim 7 finished lines add hosting room |
| 2102 | adjacent area capped at a quarter mile; grid-enhancing technologies added | transmission timing (`recond_ce`); in Sim 7 finished lines add hosting room |
| 1134 (new) | FAST-41 claims limited to 150 days (was 2 years) | with Sec.1110/2201 |
| 1501-1504 (new) | NRC licensing without hearings unless requested; uranium enrichment licensing; deadlines; NRC pay | listed (no nuclear in the model; none reaches operation by 2041 through the queue data) |
| 2115-2118 (new) | NGA civil-penalty review; RTO governance under FERC; Data Center Community Assistance Program | listed |
| 1309, 1601-1602, 2261, 3001 (new) | state wildlife plans; wildfire emissions; brownfields; DOE nuclear announcements; tax exclusion (Division C) | out of scope |

## Simulation 1: permitting and build-out time (`sim1_permitting.py`)

| Section | What it does (from the text) | Model | Data |
|---|---|---|---|
| 1106 | lead agency, joint schedule, CEQ resolves interagency disputes (30 + 14 days, then orders agencies); no waiting for new research after the NOI; alternatives limited to the sponsor's goals | modelled: share of over-deadline EA/EIS cut to deadline + 4 months (`deadline_bind`, range 0.25-1) | CEQ EIS durations by technology |
| 1105, 1108 | combine CEs; adopt other agencies' CEs; CE for actions reviewed under a state process | modelled: share of EAs -> CE (`ce_shift`, 0-0.25) | no national EA/CE count (DOE EAs only) |
| 1402(c), 1403 | 1-year deadline for permits needing no EA/EIS; applicant can sue | modelled: CE-level reviews capped at 12 months | |
| 1202 | CWA s.401 certification timeline | modelled for hydro relicensing (48 -> 36 months, ranges) | |
| 1204 | s.404: EPA veto window limited; nationwide permits 5 -> 10 years | listed: gas plants' Corps permits are in the federal nexus and EA durations (Corps 5.7-month median), but the veto-window change has no measurable delay effect | Corps individual permits x EIA-860 |
| 1302 | ESA s.7 consultation 90 -> 60 days | modelled (statute) | |
| 2102 | CE for reconductoring in existing rights-of-way | modelled (transmission EAs -> CE); in Sim 7 earlier transmission adds hosting room | |
| 2213 | renewable rights-of-way: completeness 30 days, EIS NOI within 90 days | modelled: months to start of review 12 -> 4 (both ends are ranges) | |
| 2229 | geothermal on leases not a major federal action | modelled (`geo_ce`) | NREL geothermal NEPA data |
| 1107, 2231-2233, 2251-2252 | programmatic documents; hydro conditions and maintenance; offshore "unreasonable interference" | listed | |

## Simulation 2: litigation (`sim2_litigation.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 1110 | NEPA claims within 150 days; only detailed commenters; direct injury; appeals-court original jurisdiction; remedy is remand without vacatur or injunction, <= 180 days; injunctions only on non-NEPA grounds; no NEPA review of tribal trust actions | modelled: 150-day filter from observed filing delays by challenger type x adaptation (0.39 [0.26, 1.0] from the FHWA/FTA limitation natural experiment); exhaustion/injury range; suit payoff range; no vacatur; injunctions x non-NEPA share | 1,821 NEPA cases: challenger mix, win rates, 61% filed > 150 days, injunctions 9.5%, vacatur 69% of remands, 13-month cases |
| 2201 | 150 days and expedited review for all federal claims on energy authorizations | modelled together with 1110 (the filter applies to all suits) | |
| 1205, 1305 | 150-day limits for s.404 program approvals and ESA biological opinions | listed (no separate claim type in the model) | |
| outside the bill | state-court and administrative litigation | reported, not simulated | Sabin: ~80% of litigated renewable projects in state/administrative venues |

## Simulation 3: grid access (`sim3_grid.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 2106 | FERC rule within 18 months: each RTO/ISO files consolidated interconnection + regional planning within 2 years; published locations with an upfront, fixed, subregional per-MW fee | modelled as a sweep on ISO-market projects: study-time cut 0-42% from month 36 (rule timing 24-48); floor = no measured effect of past reforms, ceiling = ERCOT's pace | LBNL request -> agreement times by region (`data/interconnection_benchmark.json`) |
| 2110 | FERC rulemaking on computing/AI queue practices; no target | central 0%, range 0-5% | |
| 2101-2103 | transmission permitting, DOE congestion study, planning | Sim 7: transmission projects that finish add hosting room to their region (lowering upgrade costs); 2103 listed | `tx_hosting_gw` (assumption 0.5-3 GW per line) |

## Simulation 7: grid access as an agent-based system (`sim7_grid_agents.py`, Phase 2)

| Section | What it does | Model (grid agents) | Data |
|---|---|---|---|
| 2106(a)(2) | published locations with an upfront, fixed per-MW fee | in RTOs that change their process (`adopt_2106`, drawn per RTO), a share of requests (`planned_share_2106`) use a published location: fixed fee, no cost shock, no re-study | LBNL network-upgrade cost by region |
| 2106(a)(3) | single decision point, non-refundable security, withdrawal penalties | one decision at the first study result; the share of new requests least likely to complete within their technology and region (`screen_2106`) do not enter; after an adverse result, developers hold their position for a shorter time (`lag_2106`, 0-1 of the current-law hold fitted in the 2010-25 backcast) | LBNL P(complete given cost) |
| 2106(d) | FERC may find existing processes compliant | `adopt_2106` 0-1 (central 0.5) | |
| 2110 | FERC rulemaking on queue automation | study throughput x (1 + `g_2110`), central 0 (not sized), high 25%; not ERCOT | |
| 2109 | advanced transmission technologies | extra hosting per line finished after the rule (`hosting_2109`, 0-30%) | |
| 2101, 2102, 2214 | transmission permitting and CEs | transmission completion dates (permitting pipeline) -> hosting room | |

## Simulation 4: permit certainty across administrations (`sim4_certainty.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 1401 | no revoking or interfering with permits in effect on/after 6 Nov 2026 (exceptions: court order, breach, fraud, urgent new harm, sponsor request, any applicable law or regulation); agency burden | modelled: residual halt probability (0.1-1.0, central 0.5) on permitted, not-yet-online projects, by political path | 2025 offshore wind stop-work orders |
| 1402(a)-(d) | suits over disparate treatment of a project type | folded into the 1401 residual | |
| 1110(c)(6) | remanded permits stay in effect | in Sim 2 (no vacatur) | |
| 1203, 1204 | NPDES and nationwide permit terms 5 -> 10 years | listed: affect existing plants' renewals; plants built 2026+ do not retire before 2041 | EIA-860 retirement ages (gas ~45 yr, wind ~21) |

## Simulation 5: utility vs merchant decision control (`sim5_decision_control.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 2106 | consolidated interconnection and planning in each Transmission Organization (RTO/ISO) | modelled through Sim 3's range, by market | LBNL completion by ISO vs non-ISO |
| 2105 | no federal right of first refusal for regional transmission | listed: changes who builds transmission; no measured link to generator completion | |
| 2104 | FERC oversight of local transmission planning on state referral | listed | |
| 2107, 2108 | transmission costs for computational loads, and 2107(b): states may condition retail service to a computational load on new generation it procures; 2108: RTOs may not block behind-the-meter aggregations (5 kW-5 MW, storage, fuel cells, generators) from wholesale markets | listed: 2107(b) acts on the demand behind the adequacy gap; 2108 is capacity outside the interconnection queue | |
| (ownership) | | gain split utility-owned vs merchant by EIA-860 ownership shares | EIA-860: 51% of new gas MW utility-owned vs 16-21% solar/wind |

## Simulation 6: supply and resource adequacy (`sim6_supply.py`, Phase 1)

No new bill sections: Sim 6 turns the queue additions that Sims 1-5 change into supply. Each project has an LBNL
region; the existing fleet (EIA-860) retires on announced dates plus an age-based rate; firm capacity and reserve
margins follow NERC's 2025 LTRA. What reaches supply from the bill:

| Section | Channel into supply | Regions reached |
|---|---|---|
| 1105-1110, 1302, 1401-1403, 2201, 2213, 2229 | more projects survive permitting, courts and halts | all nine |
| 2106 | interconnection study time (dial, Sims 3 and 6); published locations, fixed fee, single decision point (Sim 7) | FERC RTOs only: CAISO, ISO-NE, MISO, NYISO, PJM, SPP (not ERCOT, Southeast, West) |
| 2110 | interconnection study time (dial, Sims 3 and 6); study throughput (Sim 7) | all public-utility transmission providers (Sim 7: not ERCOT) |
| 2101, 2102, 2109, 2214 | transmission finished sooner adds hosting room, lowering upgrade costs (Sim 7) | regions where transmission is built |
| 1203 | NPDES permit term 5 -> 10 years for existing plants | listed: would act through retirements, which the model takes from announcements and age |
| 2107, 2114, 2117 | data-center (computational load) costs, data, assistance | listed: demand side; demand is NERC's forecast with a range |

## Renewable vs gas asymmetries in the text
- Renewable and storage: 2213 (rights-of-way for wind, solar and storage: 2213(d) adds "or store"), 2102(a) (reconductoring, mostly serves renewables), 2251-2252 (offshore wind).
- Gas-relevant: 2102(b) (interstate pipeline looping, compression and capacity enhancement in existing corridors are not a major Federal action), 1203 (NPDES term), 1204 (s.404).
- Mixed: 2108 (behind-the-meter aggregations of storage, fuel cells and generators, 5 kW-5 MW).
- Neutral on paper: 1106, 1110, 1401, 2106, 2110, 2201. They differ by technology through the data: federal nexus
  (gas ~33% via Corps permits vs wind ~5%), who sues (local groups for renewables), and interconnection time.

## Every section: status in the model

Sections as introduced; the substitute's additions and changes are in the table at the top.

**M** modelled (lever in `baaja/params.py`), **L** listed (affects electricity supply, not simulated; reason given),
**O** out of scope (no plausible effect on electricity supply by 2041, or not electricity). *Phase* = where the
course-forward plan (Nov 2026) picks it up.

| Section | Heading (short) | Status | Note |
|---|---|---|---|
| 1101-1104 | NEPA purposes, definitions, procedures, cooperation | O | 1102 adds exclusions from "major Federal action" (incl. FPA s.216A(b) transmission activities, geothermal observation tests) - folded into 2102/2229 levers |
| 1105 | Level of review | M | `ce_shift` |
| 1106 | Timely and unified reviews (deadlines, sponsor petition, court order within 120 days) | M | `deadline_bind` |
| 1107 | Programmatic documents | L | no measure of reuse |
| 1108 | CEs used by other agencies | M | `ce_shift` |
| 1109 | Applications: completeness notice within 60 days | L | candidate lever on `intake_oth` (non-federal-land nexus); Phase 0 follow-up |
| 1110 | Judicial review (150 days, remand without vacatur) | M | Sim 2 |
| 1121 | CEQ | O | |
| 1131-1133 | Permitting tracker, improvement fund | O | |
| 1201 | Water quality criteria | O | |
| 1202 | s.401 certification timeline | M | hydro relicensing only; transmission/pipeline 401 clocks listed |
| 1203 | NPDES term 5 -> 10 years | L | existing plants' renewals; Phase 1 fleet could carry it |
| 1204 | s.404 veto window, nationwide permits | L | |
| 1205 | Judicial review timeline (s.404) | L | |
| 1301-1302 | ESA s.7 consultation 90 -> 60 days | M | `esa_months` |
| 1303-1308 | ESA right-of-way, state assumption, listings, funds | O | |
| 1401 | Maintaining permits for non-Federal sponsors | M | Sim 4 |
| 1402 | Fairness for specific project types | M | folded into 1401 residual |
| 1403 | Avoiding unreasonable delays (1 year, applicant can sue) | M | `ce_cap` |
| 2101 | Transmission permitting: FERC backstop siting, >= 230 kV | M (Sim 7) | finished lines add hosting room (`tx_hosting_gw`) |
| 2102 | (a) Reconductoring in existing rights-of-way; (b) gas pipeline looping, compression and capacity enhancement in existing corridors not a major Federal action | M (a); L (b) | `recond_ce`; hosting room in Sim 7. (b) is upstream gas transport, not generation |
| 2103 | Mandatory regional and joint interregional transmission planning with cost allocation (new FPA s.225); DOE congestion study | L | the bill's main transmission-building mechanism; not modelled because transmission is not planned endogenously (lines already in the queue only) |
| 2104 | Local transmission planning oversight | L | no measured link to generation |
| 2105 | No federal ROFR | L | no measured link to generation |
| 2106 | Consolidated interconnection + planning: rule in 18 months, filings in 2 years; fixed subregional per-MW fee; single decision point; non-refundable security; withdrawal penalties | M | dial in Sims 3 and 6; structural in Sim 7 (`grid_2106`, `adopt_2106`, `planned_share_2106`, `screen_2106`, `lag_2106`, `fee_mult_2106`) |
| 2107 | Ratepayer protection: computational loads pay transmission costs | L | demand side; Phase 1 demand scenarios |
| 2108 | Behind-the-meter dispatchable resources: market access | L | outside the interconnection queue |
| 2109 | Advanced transmission technologies: public utilities must evaluate their systems and deploy on existing lines (return-on-equity penalty); not limited to RTOs | M (Sim 7), partly | `hosting_2109`: extra hosting per finished line only; the evaluate-and-deploy duty on existing lines is not modelled |
| 2110 | AI/automation in queue processing: FERC to initiate a rulemaking within 1 year; covers all public utility transmission providers | M | `ix_2110` (dial); `g_2110` throughput in Sim 7 |
| 2111 | Grid data access | L | |
| 2112-2113, 2115 | PMAs, FERC fees, conforming | O | |
| 2114 | Data on computational loads (EIA-861) | L | demand side, listed |
| 2201 | Accelerating claims: 150 days for energy authorizations | M | with 1110 |
| 2211 | Oil and gas drilling permits on non-Federal land | O | upstream gas supply, not power plants |
| 2212 | Rights-of-way across Indian land | L | |
| 2213 | Renewable rights-of-way: 30-day completeness, 90-day NOI if EIS, decision or deferral in 30 days; low-disturbance CEs | M | `intake_pub_baaja`, `comply_2213` (no enforcement mechanism in the section) |
| 2214 | CEs for grid projects and storage on disturbed land | M (Sim 7, transmission) | transmission timing -> hosting room; storage CE listed |
| 2215 | Hardrock mill sites | O | |
| 2221-2228 | Geothermal leasing, royalties, permits, pending suits | L | annual lease sales (2223) could raise geothermal requests; no data on elasticity |
| 2229 | Geothermal NEPA review | M | `geo_ce` |
| 2231-2234 | Hydropower barriers, license conditions, maintenance, micro-hydrokinetic | L | |
| 2241-2243 | FERC staffing, NW council, FERC safety | L | FERC staffing may matter for Phase 2 throughput |
| 2251 | Offshore energy: "unreasonable interference" standard | L | |
| 2252 | Offshore energy transmission | L | |
| 2301-2302 | Historic preservation | O | |
