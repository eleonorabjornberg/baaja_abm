# Five simulations: BAAJA sections -> model -> data

Scope: US electricity, renewables vs gas. "Section" always means a section of S.5653 as introduced (GovInfo
BILLS-119s5653is). Model code: `baaja/sims/simN_*.py`; results: `results/simN_*.md`. Status: **modelled** (with data
or an assumption range), **listed** (in the bill, not simulated, reason given).

## Simulation 1: permitting and build-out time (`sim1_permitting.py`)

| Section | What it does (from the text) | Model | Data |
|---|---|---|---|
| 1106 | lead agency, joint schedule, CEQ resolves interagency disputes (30 + 14 days, then orders agencies); no waiting for new research after the NOI; alternatives limited to the sponsor's goals | modelled: share of over-deadline EA/EIS cut to deadline + 4 months (`deadline_bind`, range 0.25-1) | CEQ EIS durations by technology |
| 1105, 1108 | combine CEs; adopt other agencies' CEs; CE for actions reviewed under a state process | modelled: share of EAs -> CE (`ce_shift`, 0-0.25) | no national EA/CE count (DOE EAs only) |
| 1402(c), 1403 | 1-year deadline for permits needing no EA/EIS; applicant can sue | modelled: CE-level reviews capped at 12 months | |
| 1202 | CWA s.401 certification timeline | modelled for hydro relicensing (48 -> 36 months, ranges) | |
| 1204 | s.404: EPA veto window limited; nationwide permits 5 -> 10 years | listed: gas plants' Corps permits are in the federal nexus and EA durations (Corps 5.7-month median), but the veto-window change has no measurable delay effect | Corps individual permits x EIA-860 |
| 1302 | ESA s.7 consultation 90 -> 60 days | modelled (statute) | |
| 2102 | CE for reconductoring in existing rights-of-way | modelled (transmission EAs -> CE); transmission has no MW in the model, so no GW effect | |
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
| 2106 | FERC rule within 18 months: consolidated interconnection + regional planning, published locations with fixed per-MW cost | modelled as a sweep: study-time cut 0-42% from month 36 (rule timing 24-48); floor = no measured effect of past reforms, ceiling = ERCOT's pace | LBNL request -> agreement times by region (`data/interconnection_benchmark.json`) |
| 2110 | FERC rulemaking on computing/AI queue practices; no target | central 0%, range 0-5% | |
| 2101-2103 | transmission permitting, DOE congestion study, planning | listed | |

## Simulation 4: permit certainty across administrations (`sim4_certainty.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 1401 | no revoking or interfering with permits in effect on/after 16 Sep 2026 (exceptions: court order, breach, fraud, urgent new harm, sponsor request); agency burden; sponsor recovers 25-50% of costs | modelled: residual halt probability (0-0.3) on permitted, not-yet-online projects, by political path | 2025 offshore wind stop-work orders |
| 1402(a)-(d) | suits over disparate treatment of a project type | folded into the 1401 residual | |
| 1110(c)(6) | remanded permits stay in effect | in Sim 2 (no vacatur) | |
| 1203, 1204 | NPDES and nationwide permit terms 5 -> 10 years | listed: affect existing plants' renewals; plants built 2026+ do not retire before 2041 | EIA-860 retirement ages (gas ~45 yr, wind ~21) |

## Simulation 5: utility vs merchant decision control (`sim5_decision_control.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 2106 | consolidated planning in every transmission planning region | modelled through Sim 3's range, by market | LBNL completion by ISO vs non-ISO |
| 2105 | no federal right of first refusal for regional transmission | listed: changes who builds transmission; no measured link to generator completion | |
| 2104 | FERC oversight of local transmission planning on state referral | listed | |
| 2107, 2108 | transmission costs for computational loads; behind-the-meter dispatchable access | listed (outside the interconnection queue) | |
| (ownership) | | gain split utility-owned vs merchant by EIA-860 ownership shares | EIA-860: 51% of new gas MW utility-owned vs 16-21% solar/wind |

## Renewable vs gas asymmetries in the text
- Renewable-only: 2213 (rights-of-way), 2102 (reconductoring, mostly serves renewables), 2251-2252 (offshore wind).
- Gas-relevant: 1203 (NPDES term), 1204 (s.404), 2108 (dispatchable access).
- Neutral on paper: 1106, 1110, 1401, 2106, 2110, 2201. They differ by technology through the data: federal nexus
  (gas ~33% via Corps permits vs wind ~5%), who sues (local groups for renewables), and interconnection time.

## Every section of S.5653 (introduced text, 30 Sep 2026): status in the model

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
| 2101 | Transmission permitting: FERC backstop siting, >= 230 kV | L -> Phase 2 | transmission gets MW and hosting room in Phase 2 |
| 2102 | Reconductoring in existing rights-of-way | M (timing only) | `recond_ce`; MW effect in Phase 2 |
| 2103 | DOE congestion study; regional/interregional planning | L -> Phase 2 | planning ahead of requests |
| 2104 | Local transmission planning oversight | L | no measured link to generation |
| 2105 | No federal ROFR | L | no measured link to generation |
| 2106 | Consolidated interconnection + planning: rule in 18 months, filings in 2 years; fixed zonal per-MW cost; single decision point; non-refundable security; withdrawal penalties | M (dial) -> Phase 2 | Sim 3 sweep now; structural in Phase 2 |
| 2107 | Ratepayer protection: computational loads pay transmission costs | L | demand side; Phase 1 demand scenarios |
| 2108 | Behind-the-meter dispatchable resources: market access | L | outside the interconnection queue |
| 2109 | Advanced transmission technologies (presumption of prudence) | L -> Phase 2 | hosting room per transmission project |
| 2110 | AI/automation in queue processing: rulemaking within 1 year | M | `ix_2110`; Phase 2 throughput |
| 2111 | Grid data access | L | |
| 2112-2113, 2115 | PMAs, FERC fees, conforming | O | |
| 2114 | Data on computational loads (EIA-861) | O | |
| 2201 | Accelerating claims: 150 days for energy authorizations | M | with 1110 |
| 2211 | Oil and gas drilling permits on non-Federal land | O | upstream gas supply, not power plants |
| 2212 | Rights-of-way across Indian land | L | |
| 2213 | Renewable rights-of-way: 30-day completeness, 90-day NOI if EIS, decision or deferral in 30 days; low-disturbance CEs | M | `intake_pub_baaja`, `comply_2213` (no enforcement mechanism in the section) |
| 2214 | CEs for grid projects and storage on disturbed land | L -> Phase 2 | storage CE; transmission timing |
| 2215 | Hardrock mill sites | O | |
| 2221-2228 | Geothermal leasing, royalties, permits, pending suits | L | annual lease sales (2223) could raise geothermal requests; no data on elasticity |
| 2229 | Geothermal NEPA review | M | `geo_ce` |
| 2231-2234 | Hydropower barriers, license conditions, maintenance, micro-hydrokinetic | L | |
| 2241-2243 | FERC staffing, NW council, FERC safety | L | FERC staffing may matter for Phase 2 throughput |
| 2251 | Offshore energy: "unreasonable interference" standard | L | |
| 2252 | Offshore energy transmission | L | |
| 2301-2302 | Historic preservation | O | |
