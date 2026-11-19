# Research questions -> BAAJA sections -> model -> data

Scope: US electricity, renewables vs fossil (gas generation; pipelines/LNG only as the fossil litigation comparison).
Bill text: S.5653 as introduced (GovInfo BILLS-119s5653is). Section numbers below are the bill's. Status: **in model**,
**partial**, or **not yet**.

## 1. How long do renewable vs fossil build-outs take?

| Section | What it does (from the text) | Model | Data |
|---|---|---|---|
| 1106 | NEPA s.107 rewrite: lead agency, joint schedule, CEQ resolves interagency disputes (30 + 14 days, then orders agencies); agencies may not wait for new research after the NOI; alternatives limited to those meeting the sponsor's goals; EIS scoping comment 60-75 days | in model as a hard cap on EA/EIS duration at deadline + 4 months (an assumption about how binding the deadlines become) | CEQ EIS durations by technology (`data/ceq_eis_targets.json`) |
| 1105, 1108 | combine categorical exclusions; adopt other agencies' CEs; CE for actions already reviewed under a state process | in model as 10% of EAs -> CE [A] | DOE EA list (`data/permits_opposition_targets.json`); no national EA/CE count |
| 1107 | programmatic documents | not yet | |
| 1202 | CWA s.401 certification timeline | in model only for hydro (48 -> 36 months) [A] | |
| 1204 | s.404: EPA veto window limited to application -> issuance; nationwide permits 5 -> 10 years | not yet; matters for **gas** (~28% of new gas MW has a Corps individual permit) | Corps individual permits x EIA-860 |
| 1302 | ESA s.7 consultation 90 -> 60 days | in model (3 -> 2 months) | |
| 1402(c), 1403 | 1-year deadline for federal permits that need no EA/EIS; applicant can sue in district court | not yet | |
| 2101, 2102 | transmission permitting (FPA s.216); CE for reconductoring in existing right-of-way | in model as 25% of transmission EAs -> CE [A] | CEQ transmission EISs |
| 2106 | FERC rule within 18 months: consolidated interconnection + regional planning, published interconnection locations with fixed zonal per-MW cost, streamlined interconnection | not yet; **this, not 2110, is the substantive interconnection lever** | LBNL queue (interconnection durations, completion) |
| 2110 | FERC rulemaking within 1 year to make transmission providers share/use computing, AI and automation queue practices; revisit every 4 years | in model as a 10% interconnection speedup [A]; **the text sets no speed target, so 10% has no basis in the bill** | |
| 2213 | renewable rights-of-way on federal land: completeness in 30 days, EIS notice of intent within 90 days, cost recovery within 30 days | in model as intake 12 -> 4 months [A] | |
| 2223-2229 | geothermal leasing; 2225 no federal permit on certain land; 2229 geothermal (with oil/gas) on leases not a major federal action | in model as geothermal mostly CE | NREL geothermal NEPA data |
| 2231-2233 | hydro: license conditions limited to project effects; maintenance without prior approval | partly (hydro relicensing) | |
| 2251-2252 | offshore wind: "unreasonable interference" standard; offshore transmission | not yet | |

## 2. How many projects get permitted?

| Section | What it does | Model | Data |
|---|---|---|---|
| 1106, 1402(c), 1403 | deadlines and petition rights (above) | permitted share is reported but currently counts projects that already withdrew (to fix) | CEQ EIS counts; federal nexus shares (`data/federal_nexus_targets.json`) |
| 1402(a)-(d) | applicants may sue over a "pattern of disparate treatment" of a project type vs the prior 5 years | not yet; relevant to renewable vs fossil because either side can be the disfavored type under a given administration | |

## 3. How much are projects sued, and by whom?

| Section | What it does | Model | Data |
|---|---|---|---|
| 1110 | NEPA claims: filed within 150 days; only by parties that submitted a detailed comment; direct-harm injury; courts of appeals original jurisdiction; only remedy is remand **without vacatur or injunction**, at most 180 days; authorization stays in effect; preliminary injunctions only for non-NEPA laws; no NEPA review of actions using tribal trust resources (with exceptions) | in model: suit filter by challenger type [A], payoff x0.6 [A], pause 0.5 -> 0.15 [A], case length 24 -> 12 months [A], no vacatur | case-level NEPA litigation (`data/nepa_case_targets.json`): 61% of energy suits filed > 150 days after decision; injunctions in 5-8%; vacatur in 62-72% of remands; median 13-17 months in litigation |
| 2201 | **all** federal-law claims against energy authorizations (federal-land rights-of-way, OCS, geothermal, ESA s.7/s.10): 150-day limit, expedited review, remand <= 180 days | not yet (model treats only NEPA claims) | |
| 1205, 1305 | 150-day limits for s.404 program approvals and ESA biological opinions (D.C. Circuit) | not yet | |
| — (outside the bill) | state-court and administrative litigation | not in model | Sabin: ~80% of litigated renewable projects were in state/administrative venues, which BAAJA does not reach |

## 4. Do vertically integrated utilities shift decision control?

| Section | What it does | Model | Data |
|---|---|---|---|
| 2105 | prohibits a federal right of first refusal for regional/interregional transmission selected for cost allocation (incumbent utilities lose priority) | not yet | |
| 2104 | FERC oversight of local transmission planning on state referral | not yet | |
| 2103, 2106 | DOE transmission study every 3 years; consolidated generation + transmission planning | not yet | |
| 2107 | transmission costs assigned to computational (data-center) loads | not yet | |
| 2108 | market access for dispatchable behind-the-meter systems (storage, generators, fuel cells) | not yet | |
| 2112 | power marketing administration staffing | not yet | |
|  |  |  | EIA-860 ownership: 51% of new gas MW utility-owned vs 16-21% solar/wind |

## 5. How long do plants stay in use?

| Section | What it does | Model | Data |
|---|---|---|---|
| 1203 | NPDES permit term 5 -> 10 years (affects thermal plants with discharges, i.e. gas) | not yet | |
| 1204 | nationwide permit term 5 -> 10 years | not yet | |
| 1401 | protects "operation at full capacity" of permitted projects | not yet for operations | |
| 2233 | hydro maintenance without prior approval | not yet | EIA-860 retirements (not yet extracted) |

The bill has no direct retirement provision; lifetime effects would come through permit terms and operating-permit certainty. This question may have a small answer.

## 6. How many permits are reconsidered?

| Section | What it does | Model | Data |
|---|---|---|---|
| 1401 | agencies may not revoke, suspend, amend or otherwise interfere with permits in effect on/after 16 Sep 2026 for non-federal sponsors, except court order, breach, fraud, urgent new harm, or sponsor request; burden on agency (clear and convincing); sponsor can recover delay costs and 25-50% of project costs | in model as executive halt probability x0.1 [A]; halts only on permitted, not-yet-online projects | 2025 offshore wind stop-work orders |
| 1110(c)(6)-(7), 2201(e)-(f) | remanded authorizations stay in effect; supplemental documents are separate actions with their own 150-day clock | partly (remand without vacatur) | |
| 2226 | pending civil actions don't stop geothermal lease processing | not yet | |

## Renewable vs fossil asymmetries in the text

- Renewable-only: 2213 (rights-of-way deadlines), 2102 (reconductoring, mostly serves renewables), 2251-2252 (offshore wind).
- Fossil-relevant: 1203 (NPDES term, thermal plants), 1204 (s.404, gas plants), 2108 (dispatchable market access, partly gas).
- Neutral on paper: 1106, 1110, 1401, 2106, 2110, 2201. Their effect differs by technology through the data: federal nexus, who sues, and where (federal vs state court).
