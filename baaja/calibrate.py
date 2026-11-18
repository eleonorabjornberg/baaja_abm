"""Attrition hazard calibration to LBNL Queued Up: ~19% of queued generation reaches COD under current law."""
from .model import simulate, summarize
from .params import BASE, GEN


def queue_completion(s):
    n = sum(s[t]["n"] for t in GEN)
    return sum(s[t]["completion_rate"] * s[t]["n"] for t in GEN) / n


def calibrate(target=0.19, seed=7, iters=18):
    lo, hi = 0.001, 0.2
    for _ in range(iters):
        h = (lo + hi) / 2
        p = dict(BASE, hazard=h, n_scale=0.5)
        c = queue_completion(summarize(simulate(p, seed, ["renew", "fossil", "renew", "fossil"]), p))
        lo, hi = (h, hi) if c > target else (lo, h)
    return (lo + hi) / 2
