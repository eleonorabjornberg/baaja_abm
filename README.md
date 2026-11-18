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
| project sponsors | withdraw under a commercial attrition hazard while waiting (calibrated so ~19% of queued generation reaches operation under current law, LBNL Queued Up) |
| challengers | sue federal-nexus decisions at technology-specific rates (Bennon & Wilson 2023; RFF) |
| courts | case length, loss probability (higher for truncated reviews), vacatur or remand |
| executive | after each change of administration (2029, 2033, 2037, 2041) may halt permitted, not-yet-online projects on the side it is hostile to |

BAAJA levers and their mapping to parameters, and the full calibration table with sources, are in the docstring
of [`baaja/params.py`](baaja/params.py).

## Run
```bash
pip install -r requirements.txt
python run.py --runs 100 --sweep --plots   # ~15 s; writes results/results.json, results/summary.md, figures/*.png
python -m pytest -q
```

## Results (100 runs, mean [90% interval])
Full tables: [`results/summary.md`](results/summary.md).

**Capacity online by Nov 2041**

| | current law | BAAJA | paired change |
|---|---|---|---|
| total GW | 374 | 452 | +78 [+71, +85] |
| renewable (new) GW | 165 | 205 | +39 [+34, +45] |
| gas GW | 67 | 81 | +14 [+10, +19] |
| storage GW | 129 | 151 | +21 [+19, +24] |
| renewable share of new-build TWh | 53.8% | 54.9% | +1.2 pts [-0.9, +3.0] |

**Renewable vs fossil: what the model says so far**
1. **BAAJA grows renewables and gas roughly in proportion.** The renewable share of new generation barely
   moves (+1 pt, interval spans zero). Most of the GW gain comes from the *assumed* 10% interconnection
   speedup (Sec.2110), which is technology-neutral.
2. **The permitting provisions themselves lean renewable.** Without Sec.2110, BAAJA adds ~12 GW renewables vs ~3 GW
   gas. Renewables have more federal nexus (public land, offshore), and Sec.2213 (renewable right-of-way
   deadlines) and Sec.1401 (no halts of issued permits; matters most for offshore wind) are renewable-specific.
3. **Time to permit falls much more for renewables** (median 27 → 17 months for federal-nexus projects) than for
   gas (18 → 17). Time to commercial operation barely moves for either (49 → 47, 59 → 58 months) because
   interconnection is the binding gate.
4. **Lawsuits fall ~2/3 for both** (share of federal-nexus projects sued: renewables 18% → 6%, gas 17% → 6%).
5. **Political path matters little once Sec.1401 is in place**: the BAAJA gain is similar whether every
   administration is hostile to renewables or to fossil.
6. **Cost side:** 30-55% of federal-nexus reviews for most technologies (15% storage, 2% geothermal) are cut short by enforced deadlines, by 30-45% of their
   normal length. The harm index (below) is concentrated in transmission, hydro and wind.

Sensitivity to Sec.2110 (`figures/sweep_ix_speedup.png`): total gain ranges from +18 GW (no speedup) to +234 GW
(30%). **The interconnection assumption dominates the headline number**; treat the GW totals as a scenario,
not a forecast.

## Harm index [A]
For projects that reach operation on a truncated review: pathway weight (EIS 1.0, EA 0.3) × review months cut ×
project MW (transmission counted as 300 MW), reported in GW-review-months. A proxy for how much analysis was
skipped on things that got built, not a damage estimate.

## Changes from the uploaded v3 (`legacy/baaja_electricity_abm_v3_original.py`)
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
`baaja/experiments.py` Monte Carlo, intervals, sweeps · `baaja/plots.py` · `run.py` · `tests/` ·
`legacy/` v1 (agency-capacity queue) and original v3.
