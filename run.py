"""Run the BAAJA simulations.

  python run.py --all --runs 100          # calibrate, backcast, all seven simulations
  python run.py --backcast                # backcast 2010-25 by region (reuses results/calibration.json)
  python run.py --recalibrate-grid --sim 7 # refit only the grid agents (Phase 2), then Sim 7
  python run.py --sim 2 --runs 50         # one simulation (reuses results/calibration.json if present)
  python run.py --uncertainty 400         # joint uncertainty over all assumption ranges (reuses calibration)
Outputs: results/simN_*.md|json, results/calibration.json, results/backcast.md, figures/simN_*.png
"""
import argparse
import json
import os

from baaja import validation
from baaja.calibrate import calibrate, calibrate_grid, calibrate_overdue, calibrate_regions, check
from baaja.sims import sim1_permitting, sim2_litigation, sim3_grid, sim4_certainty, sim5_decision_control, sim6_supply
from baaja.sims import sim7_grid_agents
from baaja.sims import table

SIMS = {1: sim1_permitting, 2: sim2_litigation, 3: sim3_grid, 4: sim4_certainty, 5: sim5_decision_control, 6: sim6_supply,
        7: sim7_grid_agents}
ap = argparse.ArgumentParser()
ap.add_argument("--runs", type=int, default=50)
ap.add_argument("--sim", type=int, action="append")
ap.add_argument("--all", action="store_true")
ap.add_argument("--recalibrate", action="store_true")
ap.add_argument("--recalibrate-grid", action="store_true", help="refit only the grid agents (keeps the rest)")
ap.add_argument("--uncertainty", type=int, default=0, help="joint-uncertainty samples (0 = skip)")
ap.add_argument("--backcast", action="store_true", help="backcast 2010-25 by region, both grid models (in --all)")
a = ap.parse_args()
os.makedirs("results", exist_ok=True); os.makedirs("figures", exist_ok=True)

cal_path = "results/calibration.json"
if a.recalibrate or a.all or not os.path.exists(cal_path):
    cal = calibrate()
    cal, reg_targets = calibrate_regions(cal)       # regional withdrawal hazards (Phase 1)
    cal, od_targets = calibrate_overdue(cal)        # timing of the seeded queue's first year (Phase 1)
    fit = check(cal)
    cal["grid_cal"], grid_fit = calibrate_grid(cal)  # grid agents (Phase 2)
    json.dump(dict(calibration=cal, fit=fit, regional_targets=reg_targets, first_year_targets=od_targets, grid_fit=grid_fit),
              open(cal_path, "w"), indent=1, default=float)
    md, _ = validation.report(cal, "results", 10)     # backcast 2010-25, both grid models, vs EIA-860 and LBNL
    print(md.split("\n## By region")[0])
else:
    saved = json.load(open(cal_path)); cal = saved["calibration"]
    if a.recalibrate_grid or not (cal.get("grid_cal") or {}).get("operators"):
        cal.pop("grid_cal", None)
        cal["grid_cal"], saved["grid_fit"] = calibrate_grid(cal)
        saved["calibration"] = cal
        json.dump(saved, open(cal_path, "w"), indent=1, default=float)

if a.backcast and not a.all:
    md, _ = validation.report(cal, "results", 10)
    print(md.split("\n## By region")[0])

for k in (sorted(SIMS) if a.all else (a.sim or [])):
    md, _ = SIMS[k].run(a.runs, cal, "results", "figures")
    print(md.split("\n\n## ")[0] + "\n... written to results/")
    if k == 6:                                   # supply under the 2025 request mix as well
        SIMS[k].run(a.runs, cal, "results", "figures", regime="2025")

if a.uncertainty:
    from baaja.uncertainty import report
    md, _ = report(a.uncertainty, cal, "results")
    print(md.split("\n\n## What drives")[0])
