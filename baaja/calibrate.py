"""Calibration to data, current law, per technology:
  hazard  monthly withdrawal hazard  -> completion of new requests = LBNL 2000-20 completion        [D]
  build   post-IA months to COD      -> median request-to-operation = LBNL 2015-18 cohort          [D]
  p_eis   P(EIS | federal review)    -> decided final EISs per year = CEQ 2015-24                   [D]
Each target depends a little on the others, so they are fitted in alternating rounds by bisection. All
technologies are fitted at once: each uses its own uniforms, so they do not interact.
"""
import numpy as np

from .model import simulate, summarize
from .params import BASE, GEN, TYPES

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
