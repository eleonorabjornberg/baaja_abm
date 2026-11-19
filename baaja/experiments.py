"""Monte Carlo harness: paired scenarios (same seeds and political draws), 90% intervals, sweeps, backcast."""
import numpy as np

from .model import simulate, summarize
from .params import ASSUMPTIONS, BACKCAST, BASE, CF, ENGINE, GROUPS, TYPES

METRICS = ["completion_rate", "completion_rate_nexus", "GW_online", "projects_online", "median_months_to_COD", "decisions_per_year", "EIS_per_year",
           "EA_per_year", "suits", "suits_per_year", "vacated", "halted", "halted_GW", "killed_by_courts_or_halts",
           "permitted_share", "median_months_to_permit", "truncated_share", "harm"]


def politics_draw(s, n, fixed=None):
    return list(fixed) if fixed is not None else list(np.random.default_rng(1000 + s).choice(["renew", "fossil"], n))


def params(over=None, cal=None):
    p = dict(BASE)
    if cal:
        p.update(cal)
    p.update(over or {})
    return p


def run_scenario(over, n_runs, cal, politics=None):
    p = params(over, cal)
    return [summarize(simulate(p, s, politics_draw(s, len(p["turnovers"]), politics)), p) for s in range(n_runs)]


def totals(run):
    gw = {t: run[t]["GW_online"] for t in TYPES}
    twh = {t: gw[t] * CF[t] * 8.766 for t in gw}
    out = {"GW_total": sum(gw.values()), "harm_total": sum(run[t]["harm"] for t in TYPES),
           "suits_total": sum(run[t]["suits"] for t in TYPES), "EIS_per_year_total": sum(run[t]["EIS_per_year"] for t in TYPES),
           "halted_GW_total": sum(run[t]["halted_GW"] for t in TYPES)}
    for g, members in GROUPS.items():
        out[f"GW {g}"] = sum(gw[t] for t in members)
        out[f"TWh {g}"] = sum(twh[t] for t in members)
    r, gs = out["TWh Renewable (new)"], out["TWh Fossil (gas)"]
    out["renewable share of new TWh"] = r / (r + gs) if r + gs else np.nan
    for g, v in run["_groups"].items():
        for m, x in v.items():
            out[f"{m} | {g}"] = x
    return out


def band(xs, lo=5, hi=95):
    xs = np.asarray(xs, float)
    if np.all(np.isnan(xs)):
        return dict(mean=np.nan, p5=np.nan, p95=np.nan)
    return dict(mean=float(np.nanmean(xs)), p5=float(np.nanpercentile(xs, lo)), p95=float(np.nanpercentile(xs, hi)))


def aggregate(runs, base_runs=None):
    res = {"by_type": {t: {m: band([r[t][m] for r in runs]) for m in METRICS} for t in TYPES}}
    tot = [totals(r) for r in runs]
    res["totals"] = {k: band([x[k] for x in tot]) for k in tot[0]}
    if base_runs is not None:
        bt = [totals(r) for r in base_runs]
        res["diff_vs_baseline"] = {k: band([a[k] - b[k] for a, b in zip(tot, bt)]) for k in tot[0]}
        res["diff_by_type"] = {t: {m: band([a[t][m] - b[t][m] for a, b in zip(runs, base_runs)]) for m in ("GW_online", "suits", "median_months_to_permit")}
                               for t in TYPES}
    return res


def compare(scenarios, n_runs, cal, politics=None, base_key=None):
    """{name: overrides} -> {name: aggregate}, all paired against the first (or base_key) scenario."""
    raw = {k: run_scenario(o, n_runs, cal, politics) for k, o in scenarios.items()}
    b = raw[base_key or next(iter(raw))]
    return {k: aggregate(r, None if r is b else b) for k, r in raw.items()}


LAW_KEYS = {"ea_share_nonEIS", "intake_pub", "intake_oth", "nonnepa_hydro", "lit_ea", "lit_ce", "lit_data_mult", "p_kill_vac", "remand_months",
            "delay_weight", "halt_len", "p_kill_halt", "halt_mult_other"}   # describe current law: vary in both runs


def assumption_sweep(levers, keys, n_runs, cal, base_runs, base=None):
    """For each assumption key: BAAJA (levers) at the low and high end of its range, everything else central.
    Current-law assumptions (LAW_KEYS) are changed in the baseline too, so the difference stays paired and fair.
    Returns {key: {low: {value, diff}, high: {value, diff}, note}} with diff = BAAJA - current law."""
    out = {}
    for k in keys:
        lo, _, hi, note = ASSUMPTIONS[k]
        o = {"note": note, "current_law_assumption": k in LAW_KEYS}
        for lab, v in (("low", lo), ("high", hi)):
            over = dict(base or {}); over.update(levers); over[_lever_key(k)] = v
            b = run_scenario({_lever_key(k): v, **(base or {})}, n_runs, cal) if k in LAW_KEYS else base_runs
            o[lab] = dict(value=v, diff=aggregate(run_scenario(over, n_runs, cal), b)["diff_vs_baseline"])
        out[k] = o
    return out


def _lever_key(k):
    return {"ix_2106": "ix_cut", "ix_2110": "ix_cut", "halt_mult_1401": "halt_mult", "intake_pub_baaja": "intake_pub_2213",
            "nonnepa_hydro_baaja": "nonnepa_hydro_1202", "lit_months_baaja": "lit_months"}.get(k, k)


def backcast(cal, n_runs=10):
    """Current law, Jan 2010 - Dec 2025, with LBNL requests by year, no seeded queue; GW online per year by type."""
    arr = {t: dict(v) for t, v in ((t, {int(y): n for y, n in d.items()}) for t, d in ENGINE["lbnl"]["arrivals_by_year"].items())}
    hyb = {int(y): n for y, n in ENGINE["lbnl"]["hybrid_storage"]["arrivals_by_year"].items()}
    arr["Storage"] = {y: arr["Storage"].get(y, 0) + hyb.get(y, 0) for y in set(arr["Storage"]) | set(hyb)}
    p = params(dict(T=BACKCAST["T"], turnovers=BACKCAST["turnovers"], arrivals=arr, start_year=BACKCAST["start_year"],
                    seed_queue=False), cal)
    runs = [summarize(simulate(p, s, BACKCAST["politics"]), p)["_online_by_year"] for s in range(n_runs)]
    years = list(range(BACKCAST["start_year"], BACKCAST["start_year"] + int(np.ceil(BACKCAST["T"] / 12))))
    return {t: dict(zip(years, np.mean([r[t] for r in runs], axis=0).tolist())) for t in TYPES}
