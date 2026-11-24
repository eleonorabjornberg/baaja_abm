"""Joint uncertainty (Phase 3 harness): every assumption range sampled at once, crossed with seeds.

Each sample draws all [A] assumptions in params.ASSUMPTIONS and supply.SUPPLY_ASSUMPTIONS by Latin hypercube. A value
is drawn uniformly between low and central with probability 1/2 and between central and high otherwise, so the
central value is the median. Current law and BAAJA are run with the same draws, seed and political path (paired);
assumptions that describe current law move both runs. Sec.2106's study-time cut is reported two ways: held at its
central value (0) and drawn across its range (0 to ERCOT's pace), together with Sec.2110's (0-5%). A third sample
(grid="agents", Phase 2) replaces both dials with the grid agents and draws their assumptions: GRID_LAW (current law,
both runs) and GRID_BILL (bill design, BAAJA only).

Output: intervals that include parameter uncertainty, and each assumption's share of the variance of the result
(squared standardized regression coefficients on the rank-transformed sample; they sum to at most the R^2), with
bootstrap 90% intervals on the shares. In the grid-agents sample the share of RTO capacity whose operator actually
adopts a new Sec.2106 process (drawn per RTO with probability adopt_2106) is added as a regressor: adopt_2106 only sets
the odds, and which RTOs adopt is the largest single source of spread.
"""
import numpy as np

from . import supply as sp
from .experiments import LAW_KEYS, _lever_key, params, politics_draw
from .model import simulate, summarize
from .params import ASSUMPTIONS, BAAJA, CF, GRID_BILL, GRID_LAW, GROUPS, LEVER_KEY, REGIONS, RTO_IDX, TYPES

ADOPT_KEY = "adoption realised (share of RTO capacity)"


def adoption_share(seed, adopt):
    """Share of RTO fleet capacity whose operator adopts Sec.2106 in run `seed` (same draw as grid.run_agents)."""
    from .grid import FLEET_GW
    u = np.random.default_rng([seed, 32452843]).random(len(REGIONS))
    w = np.array([FLEET_GW[r] for r in RTO_IDX])
    return float((w * (u[list(RTO_IDX)] < adopt)).sum() / w.sum())

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
        out["GW new"] = out["GW total"] - out["GW Renewable (retained hydro)"]      # relicensed hydro is not new
        if agents:
            out[ADOPT_KEY] = adoption_share(s, bill.get("adopt_2106", GRID_BILL["adopt_2106"][1]))
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


def shares_boot(X, y, n_boot=200, seed=7):
    """Variance shares with bootstrap 5th-95th percentile intervals (rows resampled)."""
    sh, r2 = variance_shares(X, y)
    rng = np.random.default_rng(seed)
    B = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        B.append([variance_shares(X[i], y[i])[0][j] for j in range(X.shape[1])])
    B = np.array(B)
    ci = {j: (float(np.percentile(B[:, j], 5)), float(np.percentile(B[:, j], 95))) for j in range(X.shape[1])}
    return sh, r2, ci


def band(x):
    x = np.asarray(x, float)
    return dict(mean=float(x.mean()), p5=float(np.percentile(x, 5)), p50=float(np.median(x)), p95=float(np.percentile(x, 95)))


METRICS = ["GW new", "GW Renewable (new)", "GW Fossil (gas)", "GW Storage", "suits",
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
        kx, XX = list(keys), X
        if grid == "agents":                                   # realised adoption as a regressor
            kx = kx + [ADOPT_KEY]; XX = np.column_stack([X, [r[ADOPT_KEY] for r in res]])
        for m in ("GW new", "shortfall change GW 2035"):
            y = np.array([r[m] for r in res])
            sh, r2, ci = shares_boot(XX, y)
            shares[m] = dict(r2=r2, top=[(kx[i], v, ci[i]) for i, v in sorted(sh.items(), key=lambda x: -x[1])[:8]])
            if grid == "agents":
                shares[m]["r2_without_realised_adoption"] = variance_shares(X, y)[1]
                shares[m]["r2_realised_adoption_alone"] = variance_shares(XX[:, -1:], y)[1]
        out[lab] = dict(bands=o, variance=shares, keys=kx)
        if grid == "agents":
            ad = np.array([r[ADOPT_KEY] for r in res]); gn = np.array([r["GW new"] for r in res])
            out[lab]["by_adoption"] = {lab2: band(gn[sel]) for lab2, sel in
                                       (("no RTO adopts", ad == 0), ("some adopt", (ad > 0) & (ad < 1)), ("every RTO adopts", ad == 1))
                                       if sel.sum() >= 5}
        f = lambda b, d=1: f"{b['p50']:+.{d}f} [{b['p5']:+.{d}f}, {b['p95']:+.{d}f}]"
        rows.append([lab] + [f(o[m]) for m in METRICS[:-1]] + [f"{o['law shortfall GW 2035']['p50']:.0f} [{o['law shortfall GW 2035']['p5']:.0f}, {o['law shortfall GW 2035']['p95']:.0f}]"])
    md += ["## Median [5th, 95th percentile] of BAAJA minus current law, by 2041 unless noted",
           "New GW excludes relicensed hydro (existing plants kept in service).",
           table(["sample", "new GW", "renewable GW", "gas GW", "storage GW", "suits 2026-41", "firm GW 2035",
                  "shortfall GW 2035", "shortfall GW 2041", "current-law shortfall GW 2035"], rows)]
    for lab, v in out.items():
        md.append(f"## What drives the result ({lab})")
        md.append(table(["result", "R^2 (rank regression)", "largest shares of variance [bootstrap 90%]"],
                        [[m, f"{s['r2']:.2f}" + (f" (without realised adoption {s['r2_without_realised_adoption']:.2f}; "
                                                 f"realised adoption alone {s['r2_realised_adoption_alone']:.2f})"
                                                 if "r2_without_realised_adoption" in s else ""),
                          "; ".join(f"{k} {100 * x:.0f}% [{100 * c[0]:.0f}, {100 * c[1]:.0f}]" for k, x, c in s["top"])]
                         for m, s in v["variance"].items()]))
        if "by_adoption" in v:
            md.append(table(["realised Sec.2106 adoption", "new GW, BAAJA minus current law: median [5th, 95th]"],
                            [[k, f"{b['p50']:+.1f} [{b['p5']:+.1f}, {b['p95']:+.1f}]"] for k, b in v["by_adoption"].items()]))
    os.makedirs(res_dir, exist_ok=True)
    json.dump(out, open(os.path.join(res_dir, "uncertainty.json"), "w"), indent=1, default=float)
    open(os.path.join(res_dir, "uncertainty.md"), "w").write("\n\n".join(md) + "\n")
    return "\n\n".join(md), out
