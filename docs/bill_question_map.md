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
| 1110 | NEPA claims within 150 days; only detailed commenters; direct injury; appeals-court original jurisdiction; remedy is remand without vacatur or injunction, <= 180 days; injunctions only on non-NEPA grounds; no NEPA review of tribal trust actions | modelled: 150-day filter from observed filing delays by challenger type x adaptation range; exhaustion/injury range; suit payoff range; no vacatur; injunctions x non-NEPA share | 1,821 NEPA cases: challenger mix, win rates, 61% filed > 150 days, injunctions 9.5%, vacatur 69% of remands, 13-month cases |
| 2201 | 150 days and expedited review for all federal claims on energy authorizations | modelled together with 1110 (the filter applies to all suits) | |
| 1205, 1305 | 150-day limits for s.404 program approvals and ESA biological opinions | listed (no separate claim type in the model) | |
| outside the bill | state-court and administrative litigation | reported, not simulated | Sabin: ~80% of litigated renewable projects in state/administrative venues |

## Simulation 3: grid access (`sim3_grid.py`)

| Section | What it does | Model | Data |
|---|---|---|---|
| 2106 | FERC rule within 18 months: consolidated interconnection + regional planning, published locations with fixed per-MW cost | modelled as a sweep: study-time cut 0-30% from month 36 (rule timing 24-48) | LBNL interconnection durations and completion |
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
