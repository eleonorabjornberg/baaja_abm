"""Run the five BAAJA simulations.

  python run.py --all --runs 100          # calibrate, backcast, all six simulations
  python run.py --sim 2 --runs 50         # one simulation (reuses results/calibration.json if present)
  python run.py --uncertainty 400         # joint uncertainty over all assumption ranges (reuses calibration)
Outputs: results/simN_*.md|json, results/calibration.json, results/backcast.md, figures/simN_*.png
"""
import argparse
import json
import os

from baaja import experiments as ex
from baaja.calibrate import calibrate, calibrate_overdue, calibrate_regions, check
from baaja.sims import sim1_permitting, sim2_litigation, sim3_grid, sim4_certainty, sim5_decision_control, sim6_supply
from baaja.sims import table

SIMS = {1: sim1_permitting, 2: sim2_litigation, 3: sim3_grid, 4: sim4_certainty, 5: sim5_decision_control, 6: sim6_supply}
ap = argparse.ArgumentParser()
ap.add_argument("--runs", type=int, default=50)
ap.add_argument("--sim", type=int, action="append")
ap.add_argument("--all", action="store_true")
ap.add_argument("--recalibrate", action="store_true")
ap.add_argument("--uncertainty", type=int, default=0, help="joint-uncertainty samples (0 = skip)")
a = ap.parse_args()
os.makedirs("results", exist_ok=True); os.makedirs("figures", exist_ok=True)

cal_path = "results/calibration.json"
if a.recalibrate or a.all or not os.path.exists(cal_path):
    cal = calibrate()
    cal, reg_targets = calibrate_regions(cal)       # regional withdrawal hazards (Phase 1)
    cal, od_targets = calibrate_overdue(cal)        # timing of the seeded queue's first year (Phase 1)
    fit = check(cal)
    json.dump(dict(calibration=cal, fit=fit, regional_targets=reg_targets, first_year_targets=od_targets), open(cal_path, "w"), indent=1, default=float)
    eia = json.load(open("data/eia860_additions.json"))
    b = ex.backcast(cal, 10)
    rows = []
    for t in ("Solar", "Onshore wind", "Gas", "Storage"):
        m = sum(b[t][y] for y in range(2018, 2026)); x = sum(eia[t][str(y)] for y in range(2018, 2026)) / 1000
        rows.append([t, f"{m:.1f}", f"{x:.1f}", f"{m/x:.2f}", " ".join(f"{b[t][y]:.0f}/{eia[t][str(y)]/1000:.0f}" for y in range(2018, 2026))])
    open("results/backcast.md", "w").write("# Backcast 2010-2025, current law, vs EIA-860 additions\n\n" + table(
        ["technology", "model GW 2018-25", "EIA-860 GW 2018-25", "ratio", "by year 2018..2025 (model/EIA)"], rows) + "\n")
    print(open("results/backcast.md").read())
else:
    cal = json.load(open(cal_path))["calibration"]

for k in (sorted(SIMS) if a.all else (a.sim or [])):
    md, _ = SIMS[k].run(a.runs, cal, "results", "figures")
    print(md.split("\n\n## ")[0] + "\n... written to results/")
    if k == 6:                                   # supply under the 2025 request mix as well
        SIMS[k].run(a.runs, cal, "results", "figures", regime="2025")

if a.uncertainty:
    from baaja.uncertainty import report
    md, _ = report(a.uncertainty, cal, "results")
    print(md.split("\n\n## What drives")[0])
