"""Run all experiments: python run.py --runs 30 [--sweep] [--plots]"""
import argparse, json, os

from baaja import experiments as ex
from baaja.calibrate import calibrate
from baaja.params import BAAJA, BASE, CHALLENGERS, LEVER_KEYS, POLITICS, SCEN

ap = argparse.ArgumentParser()
ap.add_argument("--runs", type=int, default=30)
ap.add_argument("--sweep", action="store_true", help="Sec.2110 interconnection speedup sweep, 0-30%%")
ap.add_argument("--plots", action="store_true")
a = ap.parse_args()
os.makedirs("results", exist_ok=True); os.makedirs("figures", exist_ok=True)

h = calibrate()
raw = {s: ex.run_scenario(o, a.runs, h) for s, o in SCEN.items()}
base = raw["Baseline (current law)"]
res = {s: ex.aggregate(r, None if s == "Baseline (current law)" else base) for s, r in raw.items()}

# renewable vs fossil under fixed political paths: BAAJA gain vs current law on the same path
pol = {}
for name, path in POLITICS.items():
    b = ex.run_scenario({}, a.runs, h, path); z = ex.run_scenario(BAAJA, a.runs, h, path)
    agg = ex.aggregate(z, b)
    pol[name] = dict(agg["diff_vs_baseline"], baseline=ex.aggregate(b)["totals"], baaja=agg["totals"])

# lever decomposition: each provision alone vs current law, and full BAAJA without it
lev = {}
for name, keys in LEVER_KEYS.items():
    alone = ex.aggregate(ex.run_scenario({k: BAAJA[k] for k in keys}, a.runs, h), base)["diff_vs_baseline"]
    without = ex.aggregate(ex.run_scenario(dict(BAAJA, **{k: BASE[k] for k in keys}), a.runs, h), base)["diff_vs_baseline"]
    lev[name] = dict(alone=alone, without=without)

out = dict(hazard=h, n_runs=a.runs, scenarios=res, politics=pol, levers=lev)
if a.sweep:
    vals = [1.0, .95, .9, .85, .8, .75, .7]
    out["sweep_ix_speedup"] = ex.sweep(BAAJA, "ix_speedup", vals, a.runs, h, base)
json.dump(out, open("results/results.json", "w"), indent=1)

# console + markdown summary
L = [f"calibrated monthly withdrawal hazard = {h:.4f}, {a.runs} runs, mean [90% interval]\n"]
f = lambda b, d=0: f"{b['mean']:.{d}f} [{b['p5']:.{d}f}, {b['p95']:.{d}f}]"
L += ["| scenario | GW total | GW renewable (new) | GW gas | GW storage | renewable share of new TWh | suits | harm index |",
      "|---|---|---|---|---|---|---|---|"]
for s, r in res.items():
    t = r["totals"]
    L.append(f"| {s} | {f(t['GW_total'])} | {f(t['GW Renewable (new)'])} | {f(t['GW Fossil (gas)'])} | {f(t['GW Storage'])} "
             f"| {100*t['renewable share of new TWh']['mean']:.1f}% | {f(t['suits_total'])} | {f(t['harm_total'])} |")
L += ["\nBAAJA (all levers) minus current law, paired runs:\n", "| quantity | change |", "|---|---|"]
for k in ["GW_total", "GW Renewable (new)", "GW Fossil (gas)", "GW Storage", "TWh Renewable (new)", "TWh Fossil (gas)", "renewable share of new TWh"]:
    d = res["BAAJA (all levers)"]["diff_vs_baseline"][k]
    L.append(f"| {k} | {f(d, 3) if 'share' in k else f(d, 1)} |")
L += ["\nBAAJA gain by political path (GW vs current law on the same path):\n",
      "| path | renewable (new) | gas | storage | renewable % of new TWh, current law -> BAAJA |", "|---|---|---|---|---|"]
for n, d in pol.items():
    L.append(f"| {n} | {f(d['GW Renewable (new)'], 1)} | {f(d['GW Fossil (gas)'], 1)} | {f(d['GW Storage'], 1)} "
             f"| {100*d['baseline']['renewable share of new TWh']['mean']:.1f}% -> {100*d['baaja']['renewable share of new TWh']['mean']:.1f}% |")
L += ["\nRenewable vs fossil process outcomes (2026-31 cohort; federal-nexus projects for permits and suits):\n",
      "| scenario | group | months to permit | months to COD | permitted % | sued % |", "|---|---|---|---|---|---|"]
for s in ["Baseline (current law)", "BAAJA (all levers)"]:
    t = res[s]["totals"]
    for g in ["Renewable (new)", "Fossil (gas)", "Storage"]:
        L.append(f"| {s} | {g} | {f(t[f'median_months_to_permit | {g}'])} | {f(t[f'median_months_to_COD | {g}'])} "
                 f"| {100*t[f'permitted_share_of_nexus | {g}']['mean']:.1f} | {100*t[f'sued_share_of_nexus | {g}']['mean']:.1f} |")
L += ["\nWho sues: lawsuits over the 15 years by lead challenger, current law -> BAAJA (share of the group's suits; challenger win rate):\n",
      "| group | challenger | suits, current law | suits, BAAJA | change | share of suits, law -> BAAJA | challenger wins % |", "|---|---|---|---|---|---|---|"]
for g in ["Renewable (new)", "Fossil (gas)", "Storage", "Renewable (retained hydro)"]:
    b, z = res["Baseline (current law)"]["totals"], res["BAAJA (all levers)"]["totals"]
    tb, tz = b[f"suits | {g}"]["mean"], z[f"suits | {g}"]["mean"]
    for c in CHALLENGERS:
        sb, sz = b[f"suits: {c} | {g}"]["mean"], z[f"suits: {c} | {g}"]["mean"]
        wb = b[f"challenger wins: {c} | {g}"]["mean"]
        L.append(f"| {g} | {c} | {sb:.1f} | {sz:.1f} | {100*(sz/sb-1) if sb else 0:+.0f}% | {100*sb/tb:.0f}% -> {100*sz/tz:.0f}% "
                 f"| {100*wb/sb if sb else 0:.0f} |")
L += ["\nLever decomposition, GW vs current law (alone = only this provision; full minus = full BAAJA gain lost without it):\n",
      "| provision | renewable alone | gas alone | storage alone | renewable-share pts alone | full minus: renewable | full minus: gas |",
      "|---|---|---|---|---|---|---|"]
full = res["BAAJA (all levers)"]["diff_vs_baseline"]
for n, d in lev.items():
    al, wo = d["alone"], d["without"]
    L.append(f"| {n} | {al['GW Renewable (new)']['mean']:+.1f} | {al['GW Fossil (gas)']['mean']:+.1f} | {al['GW Storage']['mean']:+.1f} "
             f"| {100*al['renewable share of new TWh']['mean']:+.2f} | {full['GW Renewable (new)']['mean'] - wo['GW Renewable (new)']['mean']:.1f} "
             f"| {full['GW Fossil (gas)']['mean'] - wo['GW Fossil (gas)']['mean']:.1f} |")
L += ["\nPer technology, BAAJA (all levers):\n", "| type | complete % | GW | GW gain | months to COD | suits | truncated % | review cut % | harm |",
      "|---|---|---|---|---|---|---|---|---|"]
r = res["BAAJA (all levers)"]
for t, v in r["by_type"].items():
    L.append(f"| {t} | {100*v['completion_rate']['mean']:.1f} | {v['GW_online']['mean']:.1f} | {r['diff_by_type_GW'][t]['mean']:+.1f} "
             f"| {v['median_months_to_COD']['mean']:.0f} | {v['suits']['mean']:.0f} | {100*v['truncated_share']['mean']:.0f} "
             f"| {100*v['mean_review_cut']['mean']:.0f} | {v['harm']['mean']:.0f} |")
if a.sweep:
    L += ["\nSec.2110 sweep (full BAAJA, GW gain vs current law):\n", "| IX speedup | total | renewable (new) | gas | storage |", "|---|---|---|---|---|"]
    for s in out["sweep_ix_speedup"]:
        d = s["diff"]
        L.append(f"| {100*(1-s['value']):.0f}% | {f(d['GW_total'])} | {f(d['GW Renewable (new)'])} | {f(d['GW Fossil (gas)'])} | {f(d['GW Storage'])} |")
open("results/summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))

if a.plots:
    from baaja import plots
    plots.scenarios_gw(res, "figures/gw_by_scenario.png")
    plots.renew_vs_fossil(res, "figures/renewable_vs_fossil_gw.png")
    plots.renew_vs_fossil(res, "figures/renewable_vs_fossil_twh.png", unit="TWh")
    plots.gain_by_type(res, "figures/gain_by_technology.png")
    plots.politics(pol, "figures/gain_by_political_path.png")
    if a.sweep:
        plots.sweep_ix(out["sweep_ix_speedup"], res["BAAJA: NEPA + courts only (Div. A)"], "figures/sweep_ix_speedup.png")
