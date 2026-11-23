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


def _completion_cells(rows, keys, window=(0, 60)):
    """Completion of requests made in `window` (months; default the first five years), by 'type|region' or 'type|*rest' (regions without a
    regional target), from simulate() rows."""
    from .params import REGIONS
    out = {}
    by = {r["type"]: r for r in rows}
    for k in keys:
        t, reg = k.split("|")
        r = by[t]; coh = ~r["seeded"] & (r["t0"] >= window[0]) & (r["t0"] < window[1])
        if reg.startswith("*"):
            excl = [REGIONS.index(x) for x in reg[1:].split(",") if x]
            sel = coh & ~np.isin(r["region"], excl)
        else:
            sel = coh & (r["region"] == REGIONS.index(reg))
        out[k] = float(r["done"][sel].mean()) if sel.any() else np.nan
    return out


def calibrate_grid(cal, seeds=tuple(range(7, 15)), iters=14, passes=3, operators=None):
    """Grid agents, current law, fitted in the 2010-25 backcast so that model and data cohorts share an era (the
    Phase 2 fit used 2026-30 model cohorts against 2015-19 data and missed the timing; Phase 3 backcast).
    (1) Grid operators fitted to LBNL request -> agreement times (grid.fit_operators).
    (2) Withdrawal in two parts. (a) Background: a regional hazard from request to construction start, one rate for a
    request's first 12 months and one after. (b) At study results: a developer is done when the allocated cost exceeds
    its value, and withdraws after holding its position a while (exponential, regional mean). By region, the
    first-year hazard, the later hazard and the mean hold are fitted so the shares of 2015-19 requests withdrawn
    within 12, 36 and 60 months match LBNL [D] (24 months is left out of the fit as a check). Value is LBNL's
    P(complete | cost) fit [D] scaled by a factor per technology and region, fitted so completion of 2010-19
    requests by end-2025 matches calibrate_regions' targets [D] (LBNL 2000-20 cohorts, still-active requests counted
    as not complete in both). Regions without a regional completion target share the technology's pooled target.
    Timing and values are fitted in alternating passes.
    (3) P(EIS | federal review) refitted in forward runs so decided EISs per year match CEQ 2015-24 [D] with the
    agents on: the agents withdraw later than the exogenous model's constant hazard, so more requests survive to a
    federal decision, and the exogenous fit would overcount EISs.
    (4) First-year timing of the seeded queue refitted (calibrate_overdue) with the agents on.
    EIA-860 additions are not used anywhere in the fit (validation.report compares them)."""
    from .grid import H_SPLIT, WD_COHORTS, fit_operators, withdrawal_curve_data
    from .params import BACKCAST, REGIONS
    from .validation import backcast_params, withdrawal_by_region
    ops = operators or fit_operators()
    targets = regional_targets()
    for t in GEN:
        have = [k.split("|")[1] for k in targets if k.startswith(t + "|")]
        if len(have) < len(REGIONS):                            # pooled cell only if some region has no target
            targets[f"{t}|*" + ",".join(have)] = TYPES[t]["completion_target"]
    wdd = withdrawal_curve_data()
    m1, m2, m3 = H_SPLIT, 60, 36
    w1, w2, w3 = ({r: v[m] for r, v in wdd.items()} for m in (m1, m2, m3))
    pb = backcast_params(cal, "agents")
    y0 = BACKCAST["start_year"]
    coh = ((WD_COHORTS[0] - y0) * 12, (WD_COHORTS[1] + 1 - y0) * 12)
    comp_win = (0, (WD_COHORTS[1] + 1 - y0) * 12)              # 2010-19 requests, completion by end-2025
    pf = dict(BASE, **cal); pf["grid"] = "agents"               # forward runs (EIS refit)

    def vmult(x):
        v = {}
        for k, val in x.items():
            t, reg = k.split("|")
            v[t if reg.startswith("*") else k] = float(np.exp(val))
        return v

    def run(gc, ss):
        got, wd = [], []
        for s in ss:
            rows = simulate(dict(pb, grid_cal=gc), s, BACKCAST["politics"])
            got.append(_completion_cells(rows, targets, comp_win)); wd.append(withdrawal_by_region(rows, coh))
        return got, wd

    def wdm(wd, r, m):
        return np.nanmean([w.get(r, {}).get(m, np.nan) for w in wd])
    eis_t = {t: TYPES[t]["eis_target"] for t in GEN if TYPES[t]["ix"]}
    pe = {t: cal["p_eis"].get(t, 0.0) for t in eis_t}

    def fit_eis(gc):
        lo = {t: 0.0 for t in eis_t}; hi = {t: 1.0 for t in eis_t}
        for _ in range(iters):
            z = {t: (lo[t] + hi[t]) / 2 for t in eis_t}
            r = [summarize(simulate(dict(pf, grid_cal=dict(gc, p_eis=z)), s, POL), pf) for s in seeds]
            for t in eis_t:
                if np.nanmean([q[t]["EIS_per_year"] for q in r]) < eis_t[t]:
                    lo[t] = z[t]
                else:
                    hi[t] = z[t]
        return {t: (lo[t] + hi[t]) / 2 for t in eis_t}
    x = {k: 0.0 for k in targets}; h1 = {r: 0.02 for r in wdd}; h2 = {r: 0.0 for r in wdd}; lg = {r: 0.0 for r in wdd}
    hp = lambda: {r: [h1[r], h2[r]] for r in wdd}
    cur = lambda: dict(operators=ops, value_mult=vmult(x), h_pre=hp(), exit_lag=dict(lg))
    # each piece is bisected toward its target: (name, dict, LBNL target, month, upper bound, raising it raises the share)
    pieces = (("first-year hazard", h1, w1, m1, 0.2, True), ("hold after an adverse result", lg, w2, m2, 240.0, False),
              ("later hazard", h2, w3, m3, 0.05, True))
    for rnd in range(passes):                      # alternate: withdrawal timing, then values (each bisected afresh)
        for _, d, tgt, m, top, up in pieces:
            lo = {r: 0.0 for r in wdd}; hi = {r: top for r in wdd}
            for _ in range(iters):
                d.update({r: (lo[r] + hi[r]) / 2 for r in wdd})
                _, wd = run(cur(), seeds)
                for r in wdd:
                    v = wdm(wd, r, m)
                    if np.isnan(v) or (v < tgt[r]) == up:
                        lo[r] = d[r]
                    else:
                        hi[r] = d[r]
            d.update({r: (lo[r] + hi[r]) / 2 for r in wdd})
        lo = {k: -5.0 for k in targets}; hi = {k: 5.0 for k in targets}
        for _ in range(iters):
            x = {k: (lo[k] + hi[k]) / 2 for k in targets}
            got, _ = run(cur(), seeds)
            for k in targets:
                m = np.nanmean([g[k] for g in got])
                if np.isnan(m) or m > targets[k]:
                    hi[k] = x[k]
                else:
                    lo[k] = x[k]
        x = {k: (lo[k] + hi[k]) / 2 for k in targets}
    gc = cur()
    gc["p_eis"] = fit_eis(gc)
    got, wd = run(gc, tuple(range(20, 30)))                 # check on 10 seeds not used in the fit
    chk = [summarize(simulate(dict(pf, grid_cal=gc), s, POL), pf) for s in range(20, 30)]
    eis_fit = {t: (float(np.nanmean([q[t]["EIS_per_year"] for q in chk])), eis_t[t]) for t in eis_t}
    fit = {k: (float(np.nanmean([g[k] for g in got])), targets[k]) for k in targets}
    wfit = {r: {m: (float(wdm(wd, r, m)), v[m]) for m in v} for r, v in wdd.items()}
    od, od_t = calibrate_overdue(dict(cal, grid_cal=gc), base=dict(grid="agents"))
    gc["overdue"] = od["overdue"]
    return gc, dict(completion=fit, withdrawn_by_month=wfit, fitted_months=[m1, m3, m2], eis_per_year=eis_fit,
                    first_year_targets=od_t, regions=REGIONS, setting="backcast 2010-25")
