"""The five simulations. Each module exposes run(n_runs, cal, res_dir, fig_dir) -> (markdown, data dict).

Shared conventions: every scenario is paired against current law with the same seeds and political draws;
numbers are mean [5th, 95th percentile] across runs; GW are capacity online by Nov 2041 from requests already
in the queue at end-2025 plus new requests; renewable vs gas is the comparison in every table.
"""
import json
import os

import numpy as np

from .. import experiments as ex
from ..params import ASSUMPTIONS, BAAJA, GROUPS

G3 = ["Renewable (new)", "Fossil (gas)", "Storage"]


def fmt(b, d=1, sign=False):
    if b is None or b.get("mean") is None or np.isnan(b["mean"]):
        return "n/a"
    s = "+" if sign else ""
    return f"{b['mean']:{s}.{d}f} [{b['p5']:{s}.{d}f}, {b['p95']:{s}.{d}f}]"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def headline(res, scen):
    """Standard renewable vs gas outcome table for a set of scenarios (diff vs current law)."""
    rows = []
    for s in scen:
        t = res[s]["totals"]; d = res[s].get("diff_vs_baseline")
        if d is None:
            rows.append([s] + [fmt(t[f"GW {g}"], 0) for g in G3] + [f"{100*t['renewable share of new TWh']['mean']:.1f}%"])
        else:
            rows.append([s] + [fmt(d[f"GW {g}"], 1, True) for g in G3] + [f"{100*d['renewable share of new TWh']['mean']:+.2f} pts"])
    return table(["scenario", "renewable GW", "gas GW", "storage GW", "renewable share of new TWh"], rows)


def regime_block(scen, n_runs, cal, title="Same comparison if 2025's request mix continues (regime \"2025\")"):
    """Re-run `scen` (first entry = current law) with every technology at its 2025 request rate, paired within that
    regime, so the bill's effect is shown separately from the regime change."""
    res = ex.compare({k: dict(v, regime="2025") for k, v in scen.items()}, n_runs, cal)
    return f"## {title}\n\n" + headline(res, list(scen)), res


def sweep_table(sw, keys, extra=("suits_total", "suits")):
    """Each assumption at the low / high end: renewable and gas GW gain, plus one extra total (default: suits)."""
    rows = []
    for k in keys:
        v = sw[k]; g = lambda lab, m: v[lab]["diff"][m]["mean"]
        rows.append([k + (" (current law)" if v.get("current_law_assumption") else ""), f"{v['low']['value']} / {v['high']['value']}",
                     f"{g('low', 'GW Renewable (new)'):+.1f} / {g('high', 'GW Renewable (new)'):+.1f}",
                     f"{g('low', 'GW Fossil (gas)'):+.1f} / {g('high', 'GW Fossil (gas)'):+.1f}",
                     f"{g('low', extra[0]):+.1f} / {g('high', extra[0]):+.1f}", v["note"]])
    return table(["assumption", "low / high", "renewable GW gain", "gas GW gain", f"{extra[1]} change", "what it is"], rows)


def save(name, data, md, res_dir):
    os.makedirs(res_dir, exist_ok=True)
    json.dump(data, open(os.path.join(res_dir, f"{name}.json"), "w"), indent=1, default=float)
    open(os.path.join(res_dir, f"{name}.md"), "w").write(md + "\n")
