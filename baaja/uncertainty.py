"""Joint uncertainty (Phase 3 harness): every assumption range sampled at once, crossed with seeds.

Each sample draws all [A] assumptions in params.ASSUMPTIONS and supply.SUPPLY_ASSUMPTIONS by Latin hypercube. A value
is drawn uniformly between low and central with probability 1/2 and between central and high otherwise, so the
central value is the median. Current law and BAAJA are run with the same draws, seed and political path (paired);
assumptions that describe current law move both runs. Sec.2106's study-time cut is reported two ways: held at its
central value (0) and drawn across its range (0 to ERCOT's pace), together with Sec.2110's (0-5%). A third sample
(grid="agents", Phase 2) replaces both dials with the grid agents and draws their assumptions: GRID_LAW (current law,
both runs) and GRID_BILL (bill design, BAAJA only).

Output: intervals that include parameter uncertainty, and each assumption's share of the variance of the result
(squared standardized regression coefficients on the rank-transformed sample, normalised to sum to the R^2).
"""
import numpy as np

from . import supply as sp
from .experiments import LAW_KEYS, _lever_key, params, politics_draw
from .model import simulate, summarize
from .params import ASSUMPTIONS, BAAJA, CF, GRID_BILL, GRID_LAW, GROUPS, LEVER_KEY, TYPES

GRID_KEYS = ["ix_2110", "ix_2106"]                            # interconnection dials the bill does not size
MODEL_KEYS = [k for k, v in ASSUMPTIONS.items() if v[0] is not None and k not in GRID_KEYS]
SUPPLY_KEYS = list(sp.SUPPLY_ASSUMPTIONS)
AGENT_KEYS = list(GRID_LAW) + list(GRID_BILL)


def lhs(n, k, rng):
    u = (np.argsort(rng.random((k, n)), axis=1).T + rng.random((n, k))) / n
    return u                                                     # [n, k] in (0, 1), one stratum per sample


def value(lo, c, hi, u):
    return lo + (c - lo) * (u / 0.5) if u < 0.5 else c + (hi - c) * ((u - 0.5) / 0.5)


def _gw(run):
    gw = {t: run[t]["GW_online"] for t in TYPES}
    return {g: sum(gw[t] for t in m) for g, m in GROUPS.items()}


def sample(n, cal, seed=2026, grid="central", supply_on=True):
    rng = np.random.default_rng(seed)
    agents = grid == "agents"
    keys = (MODEL_KEYS + (GRID_KEYS if grid == "range" else []) + (AGENT_KEYS if agents else [])
            + (SUPPLY_KEYS if supply_on else []))
    U = lhs(n, len(keys), rng)
    X = np.zeros_like(U); rows = []
    for j in range(n):
        law, bill, sa = {}, dict(BAAJA), dict(sp.SA)
        if agents:
            law["grid"] = bill["grid"] = "agents"
        for i, k in enumerate(keys):
            if k in sp.SUPPLY_ASSUMPTIONS:
                lo, c, hi, _ = sp.SUPPLY_ASSUMPTIONS[k]; v = value(lo, c, hi, U[j, i]); sa[k] = v
            elif k in GRID_LAW:
                lo, c, hi, _ = GRID_LAW[k]; v = value(lo, c, hi, U[j, i]); law[k] = v; bill[k] = v
            elif k in GRID_BILL:
                lo, c, hi, _ = GRID_BILL[k]; v = value(lo, c, hi, U[j, i]); bill[LEVER_KEY.get(k, k)] = v
            else:
                lo, c, hi, _ = ASSUMPTIONS[k]; v = value(lo, c, hi, U[j, i])
                if k in LAW_KEYS:
                    law[k] = v; bill[k] = v
                else:
                    bill[_lever_key(k)] = v
            X[j, i] = v
        s = 10_000 + j
        pol = politics_draw(s, 4)
        pl, pb = params(law, cal), params(bill, cal)
        rl, rb = summarize(simulate(pl, s, pol), pl), summarize(simulate(pb, s, pol), pb)
        gl, gb = _gw(rl), _gw(rb)
        out = {f"GW {g}": gb[g] - gl[g] for g in gl}
        out["GW total"] = sum(out.values())
        out["suits"] = sum(rb[t]["suits"] for t in TYPES) - sum(rl[t]["suits"] for t in TYPES)
        if supply_on:
            sl, sb = sp.supply(rl, sa), sp.supply(rb, sa)
            k35 = sp.YEARS.index(2035); k41 = sp.YEARS.index(2041)
            out["law shortfall GW 2035"] = sl["shortfall"][:, k35].sum() / 1000
            out["shortfall change GW 2035"] = (sb["shortfall"][:, k35].sum() - sl["shortfall"][:, k35].sum()) / 1000
            out["shortfall change GW 2041"] = (sb["shortfall"][:, k41].sum() - sl["shortfall"][:, k41].sum()) / 1000
            out["firm change GW 2035"] = (sb["firm"][:, k35].sum() - sl["firm"][:, k35].sum()) / 1000
        rows.append(out)
    return keys, X, rows


def variance_shares(X, y):
    """Squared standardized coefficients of a regression of rank(y) on rank(X); sum <= R^2."""
    from scipy.stats import rankdata
    R = np.column_stack([rankdata(X[:, i]) for i in range(X.shape[1])])
    ry = rankdata(y)
    Z = (R - R.mean(0)) / np.where(R.std(0) > 0, R.std(0), 1); zy = (ry - ry.mean()) / (ry.std() or 1)
    beta, *_ = np.linalg.lstsq(np.column_stack([Z, np.ones(len(zy))]), zy, rcond=None)
    pred = np.column_stack([Z, np.ones(len(zy))]) @ beta
    r2 = 1 - ((zy - pred) ** 2).sum() / (zy ** 2).sum()
    return dict(zip(range(X.shape[1]), (beta[:-1] ** 2).tolist())), float(r2)


def band(x):
    x = np.asarray(x, float)
    return dict(mean=float(x.mean()), p5=float(np.percentile(x, 5)), p50=float(np.median(x)), p95=float(np.percentile(x, 95)))


METRICS = ["GW total", "GW Renewable (new)", "GW Fossil (gas)", "GW Storage", "suits",
           "firm change GW 2035", "shortfall change GW 2035", "shortfall change GW 2041", "law shortfall GW 2035"]


def report(n, cal, res_dir, agents=None):
    """Joint samples (grid dials central / across their ranges / grid agents) -> results/uncertainty.md|json."""
    if agents is None:
        agents = bool((cal.get("grid_cal") or {}).get("operators"))
    import json, os
    from .sims import table
    out, md = {}, ["# Joint uncertainty: all assumption ranges at once",
                   f"{n} Latin-hypercube samples per row, each paired current law vs BAAJA with its own seed and political "
                   "path. Every [A] assumption (permitting, courts, halts, supply) is drawn from its range; values are drawn "
                   "so the central value is the median. 'Grid dials' are the interconnection study-time cuts the bill does "
                   "not size: Sec.2110 (0-5%) and Sec.2106 (0 to ERCOT's pace, RTO/ISO markets only). The grid-agents row replaces "
                   "the dials with Phase 2's queue model and also draws its assumptions (entry, scarcity response, cost growth, "
                   "re-study, transmission hosting; Sec.2106 adoption, published-location share, fee, Sec.2110 throughput, "
                   "Sec.2109 hosting)."]
    rows = []
    labs = [("grid dials at 0 (data-sized provisions)", "central"), ("grid dials across their ranges", "range")]
    if agents:
        labs.append(("grid agents (Phase 2), their assumptions drawn", "agents"))
    for lab, grid in labs:
        keys, X, res = sample(n, cal, grid=grid)
        o = {m: band([r[m] for r in res]) for m in METRICS}
        shares = {}
        for m in ("GW total", "shortfall change GW 2035"):
            sh, r2 = variance_shares(X, np.array([r[m] for r in res]))
            shares[m] = dict(r2=r2, top=[(keys[i], v) for i, v in sorted(sh.items(), key=lambda x: -x[1])[:6]])
        out[lab] = dict(bands=o, variance=shares, keys=keys)
        f = lambda b, d=1: f"{b['p50']:+.{d}f} [{b['p5']:+.{d}f}, {b['p95']:+.{d}f}]"
        rows.append([lab] + [f(o[m]) for m in METRICS[:-1]] + [f"{o['law shortfall GW 2035']['p50']:.0f} [{o['law shortfall GW 2035']['p5']:.0f}, {o['law shortfall GW 2035']['p95']:.0f}]"])
    md += ["## Median [5th, 95th percentile] of BAAJA minus current law, by 2041 unless noted",
           table(["sample", "total GW", "renewable GW", "gas GW", "storage GW", "suits 2026-41", "firm GW 2035",
                  "shortfall GW 2035", "shortfall GW 2041", "current-law shortfall GW 2035"], rows)]
    for lab, v in out.items():
        md.append(f"## What drives the result ({lab})")
        md.append(table(["result", "R^2 (rank regression)", "largest shares of variance"],
                        [[m, f"{s['r2']:.2f}", "; ".join(f"{k} {100 * x:.0f}%" for k, x in s["top"])] for m, s in v["variance"].items()]))
    os.makedirs(res_dir, exist_ok=True)
    json.dump(out, open(os.path.join(res_dir, "uncertainty.json"), "w"), indent=1, default=float)
    open(os.path.join(res_dir, "uncertainty.md"), "w").write("\n\n".join(md) + "\n")
    return "\n\n".join(md), out
