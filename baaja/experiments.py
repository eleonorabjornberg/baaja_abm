"""Monte Carlo experiments: scenarios with intervals, paired differences, sweeps, renewable/fossil split."""
import numpy as np

from .model import simulate, summarize
from .params import BASE, CF, GROUPS, TURNOVERS, TYPES

METRICS = ["completion_rate", "GW_online", "projects_online", "median_months_to_COD", "suits", "halted",
           "truncated_share", "mean_review_cut", "harm"]


def politics_draw(s, fixed=None):
    if fixed is not None:
        return list(fixed)
    return list(np.random.default_rng(1000 + s).choice(["renew", "fossil"], len(TURNOVERS)))


def run_scenario(over, n_runs, hazard, politics=None):
    """List of per-run summaries. Seeds and political draws are shared across scenarios (paired runs)."""
    p = dict(BASE); p.update(over); p["hazard"] = hazard
    return [summarize(simulate(p, s, politics_draw(s, politics)), p) for s in range(n_runs)]


def totals(run):
    """Per-run headline numbers, including the renewable vs fossil split."""
    gw = {t: run[t]["GW_online"] for t in TYPES}
    twh = {t: gw[t] * CF[t] * 8.766 for t in gw}                      # GW x CF x 8766 h / 1000
    out = {"GW_total": sum(gw.values()),
           "harm_total": sum(run[t]["harm"] for t in TYPES),
           "suits_total": sum(run[t]["suits"] for t in TYPES),
           "transmission_online": run["Transmission"]["projects_online"]}
    for g, members in GROUPS.items():
        out[f"GW {g}"] = sum(gw[t] for t in members)
        out[f"TWh {g}"] = sum(twh[t] for t in members)
    new_ren, gas = out["TWh Renewable (new)"], out["TWh Fossil (gas)"]
    out["renewable share of new TWh"] = new_ren / (new_ren + gas)
    for g, v in run["_groups"].items():
        for m, x in v.items():
            out[f"{m} | {g}"] = x
    return out


def band(xs, lo=5, hi=95):
    xs = np.asarray(xs, float)
    return dict(mean=float(np.nanmean(xs)), p5=float(np.nanpercentile(xs, lo)), p95=float(np.nanpercentile(xs, hi)))


def aggregate(runs, base_runs=None):
    """Mean and 90% interval for every per-technology metric and every total; if base_runs is given, also the
    paired difference vs that scenario (same seeds, so the interval reflects the policy, not seed noise)."""
    res = {"by_type": {t: {m: band([r[t][m] for r in runs]) for m in METRICS} for t in TYPES}}
    tot = [totals(r) for r in runs]
    res["totals"] = {k: band([x[k] for x in tot]) for k in tot[0]}
    if base_runs is not None:
        bt = [totals(r) for r in base_runs]
        res["diff_vs_baseline"] = {k: band([a[k] - b[k] for a, b in zip(tot, bt)]) for k in tot[0]}
        res["diff_by_type_GW"] = {t: band([a[t]["GW_online"] - b[t]["GW_online"] for a, b in zip(runs, base_runs)])
                                  for t in TYPES}
    return res


def sweep(base_over, key, values, n_runs, hazard, base_runs):
    """Re-run `base_over` with `key` set to each value; return headline totals and paired gain vs baseline."""
    out = []
    for v in values:
        runs = run_scenario(dict(base_over, **{key: v}), n_runs, hazard)
        a = aggregate(runs, base_runs)
        out.append(dict(value=v, totals=a["totals"], diff=a["diff_vs_baseline"]))
    return out
