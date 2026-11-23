"""Calibration to data, current law, per technology:
  hazard  monthly withdrawal hazard  -> completion of new requests = LBNL 2000-20 completion        [D]
  build   post-IA months to COD      -> median request-to-operation = LBNL 2015-18 cohort          [D]
  p_eis   P(EIS | federal review)    -> decided final EISs per year = CEQ 2015-24                   [D]
Each target depends a little on the others, so they are fitted in alternating rounds by bisection. All
technologies are fitted at once: each uses its own uniforms, so they do not interact.
"""
import numpy as np

from .model import simulate, summarize
from .params import BASE, ENGINE, GEN, TYPES

POL = ["renew", "fossil", "renew", "fossil"]


def _runs(p, seeds):
    return [summarize(simulate(p, s, POL), p) for s in seeds]


def _bisect(p0, key, targets, metric, lo, hi, seeds, iters, increasing):
    """increasing: metric rises with the parameter."""
    lo = {t: lo for t in targets}; hi = {t: hi for t in targets}
    for _ in range(iters):
        x = {t: (lo[t] + hi[t]) / 2 for t in targets}
        p = dict(p0, **{key: {**(p0.get(key) or {}), **x}})
        r = _runs(p, seeds)
        for t in targets:
            m = np.nanmean([s[t][metric] for s in r])
            if (m < targets[t]) == increasing:
                lo[t] = x[t]
            else:
                hi[t] = x[t]
    return {t: (lo[t] + hi[t]) / 2 for t in targets}


def calibrate(rounds=2, seeds=tuple(range(7, 23)), n_scale=1.0, base=None):
    p = dict(base or BASE, n_scale=n_scale, seed_queue=False)
    p["hazard"] = {t: 0.05 for t in GEN}; p["build"] = {}; p["p_eis"] = {t: 0.05 for t in TYPES}
    comp = {t: TYPES[t]["completion_target"] for t in GEN}
    cod = {t: TYPES[t]["cod_target"] for t in GEN if TYPES[t]["cod_target"]}
    eis = {t: TYPES[t]["eis_target"] for t in TYPES}
    for _ in range(rounds):
        p["hazard"] = _bisect(p, "hazard", comp, "completion_rate", 1e-4, 0.5, seeds, 18, increasing=False)
        if cod:
            p["build"] = _bisect(p, "build", cod, "median_months_to_COD", 0.0, 90.0, seeds, 14, increasing=True)
        p["p_eis"] = _bisect(p, "p_eis", eis, "EIS_per_year", 0.0, 1.0, seeds, 14, increasing=True)
    return dict(hazard=p["hazard"], build=p["build"], p_eis=p["p_eis"])


def calibrate_markets(cal, seeds=(7, 8, 9), n_scale=0.5):
    """Sim 5: separate withdrawal hazards for ISO and non-ISO regions; build and p_eis kept from the pooled calibration.
    Targets keep the ratio between markets in LBNL completion [D] (2000-20 cohort, cells with >= 30 projects), scaled
    so that, weighted by 2021-25 request shares, they equal the pooled target used by every other simulation. Without
    the scaling the 2000-20 market mix and today's differ, and Sim 5's current law would not match Sims 1-4."""
    from .params import ENGINE
    targets = {}
    for t in GEN:
        bm, pooled = ENGINE["lbnl"]["by_market"][t], TYPES[t]["completion_target"]
        ok = {m: bm[m] for m in ("ISO", "non-ISO") if bm[m]["n_cohort"] >= 30 and bm[m]["completion"] is not None}
        s_missing = sum(bm[m]["arrivals_share_2021_25"] for m in ("ISO", "non-ISO") if m not in ok)
        denom = sum(v["arrivals_share_2021_25"] * v["completion"] for v in ok.values())
        k = pooled * (1 - s_missing) / denom if denom > 0 else 1.0
        for m, v in ok.items():
            targets[f"{t}|{m}"] = min(v["completion"] * k, 0.99)
    p = dict(BASE, n_scale=n_scale, seed_queue=False, **cal)
    p["hazard"] = dict(cal["hazard"])
    lo = {k: 1e-4 for k in targets}; hi = {k: 0.5 for k in targets}
    for _ in range(18):
        x = {k: (lo[k] + hi[k]) / 2 for k in targets}
        p["hazard"] = {**cal["hazard"], **x}
        r = _runs(p, seeds)
        for k in targets:
            t, m = k.split("|")
            got = np.nanmean([s[t][f"completion_rate|{m}"] for s in r])
            if got > targets[k]:
                lo[k] = x[k]
            else:
                hi[k] = x[k]
    return dict(cal, hazard={**cal["hazard"], **{k: (lo[k] + hi[k]) / 2 for k in targets}}), targets


MIN_CELL = 50   # expected requests in a 5-year cohort below which a region keeps the pooled hazard


def regional_targets():
    """Completion targets by region [D: LBNL 2000-20 cohort, cells with >= 30 requests], scaled so that, weighted by
    each region's share of 2021-25 requests, they average to the pooled target used for the technology. Regions
    without a target keep the pooled hazard."""
    from .params import RGN
    targets = {}
    for t in GEN:
        rt = RGN["types"][t]; pooled = TYPES[t]["completion_target"]
        mk = ENGINE["lbnl"]["by_market"][t]
        w = {}
        for m, mname in ((0, "ISO"), (1, "non-ISO")):
            ms = mk[mname]["arrivals_share_2021_25"]
            for r, s in rt["new_share"][str(m)].items():
                w[r] = w.get(r, 0.0) + ms * s
        ok = {r: c for r, c in rt["completion"].items()
              if c is not None and c > 0 and w.get(r, 0.0) * TYPES[t]["arr"] * 60 >= MIN_CELL}
        miss = sum(v for r, v in w.items() if r not in ok)
        den = sum(w.get(r, 0.0) * c for r, c in ok.items())
        if den <= 0:
            continue
        k = pooled * (1 - miss) / den
        for r, c in ok.items():
            if w.get(r, 0.0) * TYPES[t]["arr"] * 60 >= MIN_CELL:   # enough projects in a 5-year cohort to fit
                targets[f"{t}|{r}"] = min(c * k, 0.95)
    return targets


def calibrate_regions(cal, seeds=tuple(range(7, 19)), n_scale=1.0, iters=18):
    """Withdrawal hazard per technology and region, fitted to regional_targets(); build and p_eis kept."""
    targets = regional_targets()
    p = dict(BASE, n_scale=n_scale, seed_queue=False, **cal)
    lo = {k: 1e-4 for k in targets}; hi = {k: 0.6 for k in targets}
    for _ in range(iters):
        x = {k: (lo[k] + hi[k]) / 2 for k in targets}
        p["hazard"] = {**cal["hazard"], **x}
        r = _runs(p, seeds)
        for k in targets:
            t, reg = k.split("|")
            got = np.nanmean([s[t][f"completion_rate|{reg}"] for s in r])
            if np.isnan(got) or got > targets[k]:
                lo[k] = x[k]
            else:
                hi[k] = x[k]
    return dict(cal, hazard={**cal["hazard"], **{k: (lo[k] + hi[k]) / 2 for k in targets}}), targets


def overdue_targets():
    """First-year additions (GW) the seeded queue should deliver: mean of EIA-860 2024 and 2025 additions [D]."""
    import json, os
    e = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "eia860_additions.json")))
    return {t: (e[t]["2024"] + e[t]["2025"]) / 2 / 1000 for t in ("Solar", "Storage", "Onshore wind", "Gas")}


def calibrate_overdue(cal, seeds=tuple(range(7, 15)), iters=14, base=None):
    """Window W (months) over which seeded projects already past the usual post-IA construction time reach operation,
    per technology, so that model year 1 (Nov 2026 - Oct 2027) matches overdue_targets(). Wider W -> fewer in year 1."""
    targets = overdue_targets()
    p = dict(BASE, **cal); p.update(base or {})
    lo = {t: 1.0 for t in targets}; hi = {t: 480.0 for t in targets}
    for _ in range(iters):
        x = {t: (lo[t] * hi[t]) ** 0.5 for t in targets}      # geometric bisection
        p["overdue"] = x
        r = [summarize(simulate(p, s, POL), p)["_online_by_year"] for s in seeds]
        for t in targets:
            got = np.mean([rr[t][0] for rr in r])
            if got > targets[t]:
                lo[t] = x[t]
            else:
                hi[t] = x[t]
    return dict(cal, overdue={t: (lo[t] * hi[t]) ** 0.5 for t in targets}), targets


def check(cal, seeds=(20, 21, 22), n_scale=1.0):
    """Fitted vs target for every calibrated quantity."""
    p = dict(BASE, n_scale=n_scale, seed_queue=False, **cal)
    r = _runs(p, seeds)
    out = {}
    for t in TYPES:
        m = lambda k: float(np.nanmean([s[t][k] for s in r]))
        out[t] = dict(completion=(m("completion_rate"), TYPES[t]["completion_target"]),
                      months_to_COD=(m("median_months_to_COD"), TYPES[t]["cod_target"]),
                      EIS_per_year=(m("EIS_per_year"), TYPES[t]["eis_target"]),
                      p_eis=cal["p_eis"].get(t), hazard=cal["hazard"].get(t), build=cal["build"].get(t))
    return out


def _completion_cells(rows, keys):
    """Completion of requests made in the first five years, by 'type|region' or 'type|*rest' (regions without a
    regional target), from simulate() rows."""
    from .params import REGIONS
    out = {}
    by = {r["type"]: r for r in rows}
    for k in keys:
        t, reg = k.split("|")
        r = by[t]; coh = ~r["seeded"] & (r["t0"] < 60)
        if reg.startswith("*"):
            excl = [REGIONS.index(x) for x in reg[1:].split(",") if x]
            sel = coh & ~np.isin(r["region"], excl)
        else:
            sel = coh & (r["region"] == REGIONS.index(reg))
        out[k] = float(r["done"][sel].mean()) if sel.any() else np.nan
    return out


def calibrate_grid(cal, seeds=tuple(range(7, 15)), iters=16, operators=None, wd_month=24):
    """Grid agents (Phase 2), current law, end-2025 queue seeded.
    (1) Grid operators fitted to LBNL request -> agreement times (grid.fit_operators).
    (2) Withdrawal in three parts: (a) before the agreement, a regional hazard h_pre fitted so the share of requests
    withdrawn within `wd_month` months matches LBNL's 2015-19 cohorts [D]; (b) at study results, when allocated cost
    exceeds the developer's value (grid agents, LBNL cost and P(complete|cost) data); (c) after the agreement, a
    hazard by technology and region fitted so completion of new requests matches calibrate_regions' targets [D].
    Regions without a regional completion target share the technology's pooled target. Both hazards are bisected at
    once, each on its own target.
    (3) First-year timing of the seeded queue refitted (calibrate_overdue) with the agents on."""
    from .grid import fit_operators, withdrawal_curve_data, withdrawal_curve_model
    from .params import REGIONS
    ops = operators or fit_operators()
    targets = regional_targets()
    for t in GEN:
        have = [k.split("|")[1] for k in targets if k.startswith(t + "|")]
        if len(have) < len(REGIONS):                            # pooled cell only if some region has no target
            targets[f"{t}|*" + ",".join(have)] = TYPES[t]["completion_target"]
    wd_t = {r: v[wd_month] for r, v in withdrawal_curve_data().items()}
    hz0 = dict(cal["hazard"])
    p = dict(BASE, **cal); p["grid"] = "agents"
    lo = {k: 1e-4 for k in targets}; hi = {k: 0.6 for k in targets}
    plo = {r: 1e-4 for r in wd_t}; phi = {r: 0.2 for r in wd_t}

    def hazard(x):
        h = dict(hz0)
        for k, v in x.items():
            t, reg = k.split("|")
            if reg.startswith("*"):
                h[t] = v
                for m in ("ISO", "non-ISO"):
                    h.pop(f"{t}|{m}", None)
            else:
                h[k] = v
        return h

    def run(gc, ss):
        got, wd = [], []
        for s in ss:
            rows = simulate(dict(p, grid_cal=gc), s, POL)
            got.append(_completion_cells(rows, targets)); wd.append(withdrawal_curve_model(rows))
        return got, wd
    for _ in range(iters):
        x = {k: (lo[k] + hi[k]) / 2 for k in targets}
        y = {r: (plo[r] + phi[r]) / 2 for r in wd_t}
        got, wd = run(dict(operators=ops, hazard=hazard(x), h_pre=y), seeds)
        for k in targets:
            m = np.nanmean([g[k] for g in got])
            if np.isnan(m) or m > targets[k]:
                lo[k] = x[k]
            else:
                hi[k] = x[k]
        for r in wd_t:
            m = np.nanmean([w.get(r, {}).get(wd_month, np.nan) for w in wd])
            if np.isnan(m) or m < wd_t[r]:
                plo[r] = y[r]
            else:
                phi[r] = y[r]
    gc = dict(operators=ops, hazard=hazard({k: (lo[k] + hi[k]) / 2 for k in targets}),
              h_pre={r: (plo[r] + phi[r]) / 2 for r in wd_t})
    got, wd = run(gc, (20, 21, 22))
    fit = {k: (float(np.nanmean([g[k] for g in got])), targets[k]) for k in targets}
    wfit = {r: (float(np.nanmean([w.get(r, {}).get(wd_month, np.nan) for w in wd])), wd_t[r]) for r in wd_t}
    od, od_t = calibrate_overdue(dict(cal, grid_cal=gc), base=dict(grid="agents"))
    gc["overdue"] = od["overdue"]
    return gc, dict(completion=fit, withdrawn_by_month=wfit, wd_month=wd_month, first_year_targets=od_t, regions=REGIONS)
