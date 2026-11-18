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

## Status (Nov 2026 build-out)
Done: package layout, tests, 90% intervals with paired runs (common random numbers), Sec.2110 sweep (#1),
renewable vs fossil reporting, harm index (#3), charts and per-technology split (#6), Sec.2110 test (#7).
See README for results and changes from v3.

## Known issues / next steps (original list)
1. Energy-title gain (~60 GW over Division A) is driven mostly by the ASSUMED 10% interconnection speedup
   (Sec.2110). Run a sensitivity sweep (0-30%).
2. Federal-nexus shares, pathway mixes, arrival rates and project sizes are assumptions. Candidate
   data: LBNL Queued Up data file (CC BY 4.0) for arrivals/sizes by technology; BLM/BOEM project lists for nexus.
3. "Truncated review" has no quality/harm consequence beyond a higher court-loss probability. Decide what
   harm metric (if any) to model.
4. Agency staffing isn't endogenous in v3 (it was in v1). Consider merging v1's capacity queue back in.
5. Sec.1401 effect is small in GW terms because halts only hit permitted-not-yet-online projects; check
   whether it should also cover lease pauses.
6. Add confidence intervals and a chart; split results by technology.
7. A bug was fixed in the Sec.2110 speedup (it was measured from simulation start, not study start).
   Write a test for it.

## Sources used
CEQ EIS Timelines reports (2020, 2025); RFF (Fraas et al.) on solar/wind NEPA timelines and litigation;
Bennon & Wilson, NEPA Litigation Over Large Energy and Transport Infrastructure Projects, 53 ELR 10836 (2023);
DOE NEPA metrics (EA durations); DOE WPTO hydropower licensing (7.6-yr relicensing); LBNL Queued Up
2025/2026; 2025 offshore wind stop-work order coverage (CRS LSB11402, Axios, E&E News).

## Next phase (requested)
Base parameters on data and add: who sues (challenger types), vertically integrated utility vs merchant
decision control, asset lifetimes / retirements, permit reconsideration. LBNL Queued Up is behind a bot check from
the cloud session; EIA-860M is reachable.
