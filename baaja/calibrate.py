"""Withdrawal-hazard calibration.

v4 (default): one monthly hazard per generation technology, so that current-law completion of the 2026-31 cohort
matches LBNL's completion rate for that technology's 2000-2020 requests [D].
v3 (calibrate_single): one hazard for all generation so pooled completion ~ 19%."""
import numpy as np

from .model import simulate, summarize
from .params import BASE, GEN, TYPES

POL = ["renew", "fossil", "renew", "fossil"]


def queue_completion(s):
    n = sum(s[t]["n"] for t in GEN)
    return sum(s[t]["completion_rate"] * s[t]["n"] for t in GEN) / n


def calibrate_single(target=0.19, seed=7, iters=18):
    lo, hi = 0.001, 0.2
    for _ in range(iters):
        h = (lo + hi) / 2
        p = dict(BASE, hazard=h, n_scale=0.5)
        c = queue_completion(summarize(simulate(p, seed, POL), p))
        lo, hi = (h, hi) if c > target else (lo, h)
    return (lo + hi) / 2


def calibrate(seeds=(7, 8, 9, 10), iters=20, n_scale=0.5, build=None):
    """Per-technology bisection of the withdrawal hazard. With one uniform per project for withdrawal, each
    technology's completion depends only on its own hazard, so all technologies are bisected simultaneously."""
    lo = {t: 1e-4 for t in GEN}; hi = {t: 0.5 for t in GEN}
    for _ in range(iters):
        h = {t: (lo[t] + hi[t]) / 2 for t in GEN}
        p = dict(BASE, hazard=h, n_scale=n_scale, build=build)
        c = {t: np.mean([summarize(simulate(p, s, POL), p)[t]["completion_rate"] for s in seeds]) for t in GEN}
        for t in GEN:
            if c[t] > TYPES[t]["completion_target"]:
                lo[t] = h[t]
            else:
                hi[t] = h[t]
    return {t: (lo[t] + hi[t]) / 2 for t in GEN}


def calibrate_build(hazard, seeds=(7, 8), iters=14, n_scale=0.5):
    """Construction months (IA -> COD, net of the parallel permitting gate) per technology so that the current-law
    median months from request to operation of completed projects matches LBNL (cod_target). Technologies without
    enough data keep their v3 value."""
    ts = [t for t in GEN if "cod_target" in TYPES[t]]
    lo = {t: 0.0 for t in ts}; hi = {t: 90.0 for t in ts}
    for _ in range(iters):
        b = {t: (lo[t] + hi[t]) / 2 for t in ts}
        p = dict(BASE, hazard=hazard, n_scale=n_scale, build=b)
        m = {t: np.mean([summarize(simulate(p, s, POL), p)[t]["median_months_to_COD"] for s in seeds]) for t in ts}
        for t in ts:
            if m[t] > TYPES[t]["cod_target"]:
                hi[t] = b[t]
            else:
                lo[t] = b[t]
    return {t: (lo[t] + hi[t]) / 2 for t in ts}


def calibrate_all(rounds=3):
    """Alternate hazard and build calibration (each shifts the other's target). Returns (hazard, build)."""
    build = None
    for _ in range(rounds):
        hazard = calibrate(build=build)
        build = calibrate_build(hazard)
    return calibrate(build=build), build
