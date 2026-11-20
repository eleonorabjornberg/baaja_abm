# BAAJA ABM — handoff for Claude Code

Personal experiment, NOT thesis work. Agent-based model of the policy consequences of
S.5653, Bipartisan American Affordability and Jobs Act of 2026 (119th Congress), focused on electricity.

## Files
- `baaja_electricity_abm.py`: current model (v3). Projects by technology, two parallel gates
  (federal permitting + grid interconnection), challengers, courts, executive halts, sponsor attrition.
  Calibration table with sources sits in the module docstring ([D] = from data, [A] = assumption).
- `baaja_abm.py`: v1, generic projects with an endogenous agency-capacity queue. Kept for reference.
- Run: `python3 baaja_electricity_abm.py 30` (number of Monte Carlo runs). numpy only.

## Key modelling decision
The 2023 Fiscal Responsibility Act already set 2-yr EIS / 1-yr EA deadlines. Current law is calibrated
to CEQ's 2021-24 EIS data (median 2.4 yr, 39% within 2 yr). BAAJA's change is making the deadlines
*enforceable* (sponsor petition -> court order within 60 days), so reviews running past the deadline are
capped and flagged as truncated.

## Preliminary results (5 runs; rerun with 30+)
- GW online by Nov 2041: baseline ~372, BAAJA ~451 (+21%), Division A alone (NEPA + courts) ~389,
  BAAJA without Sec.1401 ~449.
- Lawsuits fall ~60-90% by technology; offshore wind completion rises ~9% -> ~21% (permit certainty
  + litigation limits).
- Cost side: ~30-55% of federal-nexus reviews are cut short by the enforced deadlines, by ~30-45% of
  their normal length.

## Status (Nov 2026, v5)
The model is rebuilt on data (see README data and assumption registers) and organised as five simulations
(`baaja/sims/`, map in `docs/bill_question_map.md`). Results in `results/`, charts in `figures/`.

Main findings: data-sized provisions add ~+15 GW by 2041 (renewables +11.2, gas +1.2, storage +0.4); grid access
(Sec.2106) is unsized by the bill and dominates (each 5% study-time cut ~ +35-45 GW).

## Next steps
1. Done: BLM ePlanning (EA share, durations, suit rates), FHWA/FTA limitation experiment, ERCOT interconnection bracket.
2. Done: right-of-way intake measured from BLM MLRS filing dates (median 10.5 months). Wind/geothermal cases would extend it.
3. Done: storage completion from EIA-860M (backcast 0.37 -> 0.53).
4. Partly done: wind HCPs added (+2.7 pts). Still missing: FWS specific eagle permits (no public list).
5. Sim 5: a measured link from transmission sponsorship (Sec.2105) to generator completion, if one exists.
6. Pipelines/LNG: litigation comparison in Sim 2; a full sub-model would need FERC certificate dates.
7. Done: gas arrivals sensitivity (2025 rate 2.13x). Still needed from user: list of federal actions against permitted projects 2017-26.

## History
v3 (uploaded): assumed parameters. v4: LBNL calibration, challenger agents. v5: federal nexus, EIS counts, court
parameters, seeded queue, backcast, five simulations.
