# baaja_abm

Trial agent-based model of how **S.5653, the Bipartisan American Affordability and Jobs Act of 2026 (BAAJA,
119th Congress)** would change the US electricity build-out, with a focus on **renewable vs fossil** outcomes.
Personal experiment, not peer reviewed. Every number below is conditional on the assumptions marked [A].

## What the model does
Monthly cohorts of projects (solar, storage, onshore and offshore wind, gas, geothermal, transmission, hydro
relicensing) arrive over Nov 2026 to Nov 2041. Each project runs two gates in parallel: federal permitting (if it
has a federal nexus: CE / EA / EIS review, ESA consultation, litigation) and grid interconnection. Agents:

| agent | behaviour |
|---|---|
| project sponsors | withdraw under a technology-specific attrition hazard while waiting (calibrated to LBNL completion rates) |
| challengers | five types (national NGO, local group / residents, tribe, state / local government, business) sue federal-nexus decisions; the lead challenger is drawn from a technology-specific mix |
| courts | case length, loss probability (by challenger type; higher for truncated reviews), vacatur or remand |
| executive | after each change of administration (2029, 2033, 2037, 2041) may halt permitted, not-yet-online projects on the side it is hostile to |

BAAJA levers, their mapping to parameters, and every source are in [`baaja/params.py`](baaja/params.py)
([D] = from data, [A] = assumption).

## Data
| what | source | used for |
|---|---|---|
| interconnection queue, 38,201 requests through 2025 | LBNL Queued Up data file (CC BY 4.0) via [`data/extract_lbnl.py`](data/extract_lbnl.py) -> [`data/lbnl_targets.json`](data/lbnl_targets.json) | arrivals by technology (2021-25 requests/month), built project size (mean MW of operational projects), interconnection duration (IR -> IA median and spread), completion rates (2000-20 cohort) and time to operation (2015-18 cohort), which calibrate per-technology withdrawal hazards and post-IA build times |
| EIS / EA / CE durations | CEQ EIS Timelines 2020, 2025; RFF (Fraas et al.); DOE NEPA metrics; USFS | review durations |
| litigation rates by sector | Bennon & Wilson 2023 (53 ELR 10836); RFF | P(sued) for EIS projects |
| who sues | CEQ NEPA Litigation Surveys 2001-13 (n = 3,650 plaintiff entries); Breakthrough Institute, *Understanding NEPA Litigation* (2024, 387 appeals 2013-22) | challenger mix anchors, win rates by challenger type |
| capacity factors | EIA Electric Power Monthly; NREL ATB (offshore wind) | GW -> TWh |

Values that rest on fewer than 30 projects keep the v3 assumption (offshore wind size: 3 built; geothermal
interconnection: 3 IAs). The raw LBNL workbook is not committed; rerun the extractor on it to refresh the targets.

## Run
```bash
pip install -r requirements.txt pandas openpyxl
python run.py --runs 100 --sweep --plots   # ~75 s; writes results/results.json, results/summary.md, figures/*.png
python -m pytest -q
```

## Results (data-calibrated, 100 runs, mean [90% interval])
Full tables: [`results/summary.md`](results/summary.md).

**Capacity online by Nov 2041**

| | current law | BAAJA | paired change |
|---|---|---|---|
| total GW | 355 | 428 | +74 [+68, +80] |
| renewable (new) GW | 204 | 256 | +52 [+48, +58] |
| gas GW | 88 | 98 | +10 [+8, +13] |
| storage GW | 50 | 58 | +8 [+7, +9] |
| renewable share of new-build TWh | 53.0% | 56.3% | +3.3 pts [+2.4, +4.2] |

**Renewable vs fossil**
1. **BAAJA tilts the build-out toward renewables**: +52 GW renewables vs +10 GW gas; renewable share of new
   generation +3.3 points (interval excludes zero). With the data calibration the tilt is clearer than in v3:
   gas clears interconnection much faster (median 21 vs ~33 months for solar and wind, LBNL), so the
   interconnection gate, and Sec.2110's speedup of it, matters more for renewables.
2. **Provisions that lean renewable**: Sec.2213 renewable right-of-way deadlines (+6 GW renewables alone, nothing
   for gas), Sec.1401 permit certainty (offshore wind), and the enforced NEPA deadlines (renewables have more
   federal nexus). Sec.2110 remains the largest single lever and is an assumption (sweep: +25 GW at 0% speedup to
   +204 GW at 30%).
3. **Time to permit** (federal-nexus projects): renewables 28 -> 18 months, gas 18 -> 17. **Time to operation**
   barely moves (renewables 61 -> 60, gas 36 -> 36 months): interconnection and post-IA development dominate.
4. **Permitted**: 97-98% of federal-nexus projects get their permit under current law, ~100% under BAAJA.
5. **Political path** matters little once Sec.1401 is in place.

**Who sues** (`figures/who_sues.png`)
- Renewables are sued mostly by **local groups and residents** (44% of suits), then national NGOs (22%) and
  businesses (15%; offshore-wind fishing interests). Gas is sued mostly by **national NGOs** (45%), then local
  groups (30%).
- BAAJA cuts suits ~2/3 overall, but unevenly: **local groups and residents -73%, national NGOs -68%, businesses
  -70%, tribes -58%, state and local governments -53%**. The 150-day clock and comment-exhaustion rule hit
  challengers without legal staff hardest; sovereign and proprietary plaintiffs keep standing.
- Tribes have the highest win rate (BTI: 31% of appeals), so they are a growing share of the remaining, more
  successful suits.

**Cost side**: 30-55% of federal-nexus reviews for most technologies (15% storage, 2% geothermal) are cut short by
enforced deadlines, by 30-45% of their normal length. The harm index (below) is concentrated in transmission,
onshore wind, hydro and offshore wind.

**Absolute level caveat**: the baseline (~24 GW/yr) is below recent US additions because hybrid storage
components are not counted separately and completion rates come from the 2000-20 queue cohort. Read the
differences between scenarios, not the levels.

## Harm index [A]
For projects that reach operation on a truncated review: pathway weight (EIS 1.0, EA 0.3) × review months cut ×
project MW (transmission counted as 300 MW), reported in GW-review-months. A proxy for how much analysis was
skipped on things that got built, not a damage estimate.

## Changes from the uploaded v3 (`legacy/baaja_electricity_abm_v3_original.py`)
- **v4 data calibration** from LBNL Queued Up (arrivals, sizes, interconnection durations, per-technology
  withdrawal hazards and post-IA build times); v3 values kept as `TYPES_V3`.
- **Challenger agents** (who sues) replace the single standing/exhaustion factor of 0.55 with type-specific
  filters whose technology-weighted mean is ~0.55.
- **Common random numbers:** v3 skipped random draws when vacatur was off or an administration was not hostile, so
  scenarios with the same seed drifted onto different random streams. All draws are now made in every scenario.
  Distributions are unchanged; paired intervals are ~3× tighter.
- `mean_review_cut` now averages only over federal-nexus projects (v3 included projects with no federal review).
- Attrition wait: v3 adds litigation/halt delay on top of time to construction start, which already contains
  litigation delay when permitting binds, so that delay counts double. Kept as `delay_weight=1` (v3 behaviour);
  set 0 to test.
- New outputs: uncertainty intervals, paired differences, renewable/fossil/storage groups (GW, TWh via EIA capacity
  factors), months to permit, permitted and sued shares, lever decomposition, political-path experiment,
  Sec.2110 sweep, harm index, charts, tests.

## Layout
`baaja/params.py` parameters and scenarios · `baaja/model.py` simulation · `baaja/calibrate.py` ·
`baaja/experiments.py` Monte Carlo, intervals, sweeps · `baaja/plots.py` · `run.py` · `tests/` · `data/` LBNL extractor and targets ·
`legacy/` v1 (agency-capacity queue) and original v3.
