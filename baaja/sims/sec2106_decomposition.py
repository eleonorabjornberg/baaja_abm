"""Where the Sec.2106 gain in the grid-agent model comes from: python run.py --decomposition --runs 40.

Answers the second methods review (Nov 2026). Every case is paired with current law under the same seeds, political
draws and assumption changes. Writes results/sec2106_decomposition.md|json.

  A. Sec.2106 by component (every RTO adopts): single decision point (the re-study round removed), published locations,
     entry screen (relative, absolute, none); and the same screens with each RTO adopting with p = 0.5.
  B. The current-law re-study round turned down in law and bill alike (restudy_rho, restudy_months).
  C. PJM's upgrade-cost distribution given MISO's zero-cost share or MISO's spread; MISO given PJM's study throughput.
  D. Permitting and courts only (Sec.2106 and Sec.2109 off) with grid agents.
  E. More or sooner: RTO capacity online by Nov 2041 against capacity that ever completes.
  F. The calibration before the Nov 2026 refit (commit b6c291c), relative against absolute screen.
"""
import copy
import json
import os
import subprocess
from multiprocessing import Pool

import numpy as np

from .. import experiments as ex
from .. import grid as gr
from ..model import simulate, summarize
from ..params import BAAJA, REGIONS, RTO_IDX, TYPES
from . import save, table

AG = dict(grid="agents")
B = dict(BAAJA, **AG)
EV = dict(B, adopt_2106=1.0)
RTO = [REGIONS[i] for i in RTO_IDX]
PRE_REFIT = "b6c291c"
_CAL = {}


def _stats(rows, p):
    """National new GW (relicensed hydro excluded), GW online by region (interconnecting types), and for new
    requests in RTO regions: GW online by the horizon, GW that ever complete, and zero-cost shares of signers."""
    out = dict(GW_new=ex.totals(summarize(rows, p))["GW_new"])
    reg = {r: 0.0 for r in REGIONS}
    on_rto = ever_rto = coh_on = coh_ever = 0.0
    zc = {}
    for r in rows:
        if not TYPES[r["type"]]["ix"]:
            continue
        on = r["done"] & (r["tCOD"] <= r["T"])
        for k, g in enumerate(REGIONS):
            reg[g] += r["mw"] * (on & (r["region"] == k)).sum() / 1000
        new = ~r["seeded"] & np.isin(r["region"], RTO_IDX)
        on_rto += r["mw"] * (new & on).sum() / 1000
        ever_rto += r["mw"] * (new & r["done"]).sum() / 1000
        coh = new & (r["t0"] >= p["ix_rule_month"]) & (r["t0"] < p["ix_rule_month"] + 72)   # first six years under the rule
        coh_on += r["mw"] * (coh & on).sum() / 1000
        coh_ever += r["mw"] * (coh & r["done"]).sum() / 1000
        post = ~r["seeded"] & (r["t0"] >= p["ix_rule_month"]) & np.isfinite(r["tIA"])
        for g in ("PJM", "MISO"):
            s = post & (r["region"] == REGIONS.index(g))
            zc[f"{g}|{r['type']}"] = [int(s.sum()), int((s & (r["cost"] == 0)).sum())]
    out.update(region=reg, RTO=sum(reg[g] for g in RTO), new_rto_online=on_rto, new_rto_ever=ever_rto, cohort_online=coh_on,
               cohort_ever=coh_ever, zero_cost=zc)
    return out


def _one(job):
    key, over, cal_key, cost_patch, seed = job
    cal = _CAL[cal_key]
    orig = copy.deepcopy(gr.COST)
    try:
        for g, kv in (cost_patch or {}).items():
            gr.COST[REGIONS.index(g)] = dict(gr.COST[REGIONS.index(g)], **kv)
        p = ex.params(over, cal)
        return key, seed, _stats(simulate(p, seed, ex.politics_draw(seed, len(p["turnovers"]))), p)
    finally:
        gr.COST[:] = orig


def _init(cals):
    _CAL.update(cals)


def _cases(cal):
    """(key, overrides, calibration key, cost patch). Every bill case names the current-law case it is paired with."""
    c = []
    law = lambda tag, x=None, ck="now", cp=None: c.append((f"{tag}|law", dict(AG, **(x or {})), ck, cp))
    bill = lambda tag, name, o, ck="now", cp=None: c.append((f"{tag}|{name}", o, ck, cp))
    # A. components
    law("A")
    for name, o in (("without Sec.2106", dict(EV, grid_2106=False)),
                    ("single decision point only", dict(EV, screen_2106=0.0, planned_share_2106=0.0)),
                    ("+ published locations (no screen)", dict(EV, screen_2106=0.0)),
                    ("+ relative screen (central)", EV),
                    ("+ absolute screen instead", dict(EV, screen_2106=0.0, q_abs_2106=0.25)),
                    ("relative screen, no published locations", dict(EV, planned_share_2106=0.0)),
                    ("p=0.5: no screen", dict(B, screen_2106=0.0)),
                    ("p=0.5: relative screen (central)", B),
                    ("p=0.5: absolute screen", dict(B, screen_2106=0.0, q_abs_2106=0.25))):
        bill("A", name, o)
    # B. re-study round
    for tag, x in (("B rho=0", dict(restudy_rho=0.0)), ("B months=1", dict(restudy_months=1)),
                   ("B rho=0, months=1", dict(restudy_rho=0.0, restudy_months=1)),
                   ("B months=0", dict(restudy_months=0))):
        law(tag, x)
        for name, o in (("without Sec.2106", dict(EV, grid_2106=False)),
                        ("single decision point only", dict(EV, screen_2106=0.0, planned_share_2106=0.0)),
                        ("full Sec.2106", EV), ("p=0.5", B)):
            bill(tag, name, dict(o, **x))
    # C. PJM cost shape, MISO throughput
    iP, iM = REGIONS.index("PJM"), REGIONS.index("MISO")
    for tag, cp, ck in (("C PJM zero-cost share = MISO's", {"PJM": dict(zero_share=gr.COST[iM]["zero_share"])}, "now"),
                        ("C PJM cost spread = MISO's", {"PJM": dict(sigma=gr.COST[iM]["sigma"])}, "now"),
                        ("C MISO throughput = PJM's", None, "miso_tp")):
        law(tag, ck=ck, cp=cp)
        for name, o in (("full Sec.2106", EV), ("no screen", dict(EV, screen_2106=0.0))):
            bill(tag, name, o, ck, cp)
    # D. permitting and courts only
    bill("A", "Titles I-II only (no Sec.2106, no Sec.2109)", dict(B, grid_2106=False, grid_2109=0.0))
    bill("A", "p=0.5 without Sec.2109", dict(B, grid_2109=0.0))
    # F. calibration before the refit
    if "pre" in _CAL:
        law("F", ck="pre")
        for name, o in (("without Sec.2106", dict(EV, grid_2106=False)), ("relative screen (central)", EV),
                        ("no screen", dict(EV, screen_2106=0.0)), ("absolute screen", dict(EV, screen_2106=0.0, q_abs_2106=0.25))):
            bill("F", name, o, "pre")
    return c


def _band(x):
    x = np.asarray(x, float)
    return dict(mean=float(x.mean()), p5=float(np.percentile(x, 5)), p95=float(np.percentile(x, 95)))


def run(n_runs, cal, res_dir, procs=None):
    cals = {"now": cal}
    cm = copy.deepcopy(cal); o = cm["grid_cal"]["operators"]
    o["MISO"]["K_end"] = o["PJM"]["K_end"] / o["PJM"]["D_data"] * o["MISO"]["D_data"]
    cals["miso_tp"] = cm
    try:
        cals["pre"] = json.loads(subprocess.run(["git", "show", f"{PRE_REFIT}:results/calibration.json"], capture_output=True,
                                                check=True, text=True).stdout)["calibration"]
    except Exception:          # noqa: BLE001  (no git history: section F is skipped)
        pass
    _CAL.update(cals)
    cases = _cases(cal)
    jobs = [(k, o, ck, cp, s) for k, o, ck, cp in cases for s in range(n_runs)]
    with Pool(procs or os.cpu_count(), initializer=_init, initargs=(cals,)) as pool:
        out = pool.map(_one, jobs, chunksize=4)
    R = {}
    for k, s, st in out:
        R.setdefault(k, {})[s] = st
    seeds = range(n_runs)
    res = {}
    for k in R:
        tag, name = k.split("|", 1)
        L = R[f"{tag}|law"]
        d = lambda f: [f(R[k][s]) - f(L[s]) for s in seeds]
        res[k] = dict(GW_new=_band([R[k][s]["GW_new"] for s in seeds]),
                      diff_GW_new=_band(d(lambda x: x["GW_new"])),
                      diff_RTO=_band(d(lambda x: x["RTO"])),
                      diff_region={g: float(np.mean(d(lambda x, g=g: x["region"][g]))) for g in REGIONS},
                      diff_new_rto_online=float(np.mean(d(lambda x: x["new_rto_online"]))),
                      diff_new_rto_ever=float(np.mean(d(lambda x: x["new_rto_ever"]))),
                      diff_cohort_online=float(np.mean(d(lambda x: x["cohort_online"]))),
                      diff_cohort_ever=float(np.mean(d(lambda x: x["cohort_ever"]))),
                      zero_cost={z: [float(np.mean([R[k][s]["zero_cost"].get(z, [0, 0])[i] for s in seeds])) for i in (0, 1)]
                                 for z in R[k][seeds[0]]["zero_cost"]})
    res["_meta"] = dict(n_runs=n_runs, pre_refit_commit=PRE_REFIT if "pre" in cals else None,
                        throughput_over_arrivals={g: o2["K_end"] / o2["D_data"] for g, o2 in cal["grid_cal"]["operators"].items()},
                        cost={g: dict(zero_share=gr.COST[REGIONS.index(g)]["zero_share"], sigma=gr.COST[REGIONS.index(g)]["sigma"])
                              for g in RTO})
    md = report(res)
    save("sec2106_decomposition", res, md, res_dir)
    return md, res


def _f(b):
    return f"{b['mean']:+.1f} [{b['p5']:+.1f}, {b['p95']:+.1f}]"


def report(res):
    n = res["_meta"]["n_runs"]
    A = lambda name: res[f"A|{name}"]
    law = res["A|law"]["GW_new"]["mean"]
    rows_a = [[name, _f(A(name)["diff_GW_new"]), f"{A(name)['diff_GW_new']['mean'] - A('without Sec.2106')['diff_GW_new']['mean']:+.1f}"
               if name != "without Sec.2106" else "", _f(A(name)["diff_RTO"])]
              for name in ("without Sec.2106", "single decision point only", "+ published locations (no screen)",
                           "+ relative screen (central)", "+ absolute screen instead", "relative screen, no published locations",
                           "p=0.5: no screen", "p=0.5: relative screen (central)", "p=0.5: absolute screen",
                           "Titles I-II only (no Sec.2106, no Sec.2109)", "p=0.5 without Sec.2109")]
    t_a = table(["case (every RTO adopts unless p=0.5)", "BAAJA minus current law, new GW", "of which Sec.2106",
                 "RTO regions, GW"], rows_a)
    rows_b = []
    for tag in ("B rho=0", "B months=1", "B rho=0, months=1", "B months=0"):
        L = res[f"{tag}|law"]["GW_new"]["mean"]
        g = lambda nm: res[f"{tag}|{nm}"]["diff_GW_new"]["mean"]
        rows_b.append([tag[2:], f"{L:.0f}", f"{g('without Sec.2106'):+.1f}", f"{g('single decision point only'):+.1f}",
                       f"{g('full Sec.2106'):+.1f}", f"{g('p=0.5'):+.1f}"])
    g0 = lambda nm: A(nm)["diff_GW_new"]["mean"]
    rows_b.insert(0, ["central (rho 0.3, 6 months)", f"{law:.0f}", f"{g0('without Sec.2106'):+.1f}",
                      f"{g0('single decision point only'):+.1f}", f"{g0('+ relative screen (central)'):+.1f}",
                      f"{g0('p=0.5: relative screen (central)'):+.1f}"])
    t_b = table(["current-law re-study round (law and bill)", "current law new GW", "without Sec.2106",
                 "single decision point only", "every RTO, full Sec.2106", "p=0.5, full Sec.2106"], rows_b)
    reg = [g for g in RTO]
    scr = [[g, f"{A('+ published locations (no screen)')['diff_region'][g]:+.1f}", f"{A('+ relative screen (central)')['diff_region'][g]:+.1f}",
            f"{A('+ relative screen (central)')['diff_region'][g] - A('+ published locations (no screen)')['diff_region'][g]:+.1f}",
            f"{A('+ absolute screen instead')['diff_region'][g]:+.1f}", f"{res['_meta']['throughput_over_arrivals'][g]:.2f}",
            f"{res['_meta']['cost'][g]['zero_share']:.3f}", f"{res['_meta']['cost'][g]['sigma']:.2f}"] for g in reg]
    t_r = table(["region (every RTO adopts)", "no screen", "relative screen", "screen effect", "absolute screen",
                 "throughput / arrivals", "zero-cost share", "cost spread (sigma)"], scr)
    rows_c = []
    for tag, lab in (("A", "as calibrated"), ("C PJM zero-cost share = MISO's", "PJM zero-cost share = MISO's"),
                     ("C PJM cost spread = MISO's", "PJM cost spread = MISO's"), ("C MISO throughput = PJM's", "MISO throughput = PJM's")):
        full = res[f"{tag}|+ relative screen (central)" if tag == "A" else f"{tag}|full Sec.2106"]["diff_region"]
        nos = res[f"{tag}|+ published locations (no screen)" if tag == "A" else f"{tag}|no screen"]["diff_region"]
        rows_c.append([lab, f"{full['PJM']:+.1f}", f"{nos['PJM']:+.1f}", f"{full['MISO']:+.1f}", f"{nos['MISO']:+.1f}"])
    t_c = table(["counterfactual (every RTO adopts)", "PJM, full Sec.2106", "PJM, no screen", "MISO, full Sec.2106",
                 "MISO, no screen"], rows_c)
    zc = res["A|+ relative screen (central)"]["zero_cost"]
    zrows = [[k.replace("|", ", "), f"{v[1]:.0f} of {v[0]:.0f}"] for k, v in zc.items() if v[0] >= 1]
    t_z = table(["post-rule requests that sign (every RTO adopts, mean per run)", "with zero upgrade cost"], zrows)
    rows_e = [[name, f"{A(name)['diff_new_rto_online']:+.1f}", f"{A(name)['diff_new_rto_ever']:+.1f}",
               f"{A(name)['diff_new_rto_online'] - A(name)['diff_new_rto_ever']:+.1f}",
               f"{A(name)['diff_cohort_online']:+.1f}", f"{A(name)['diff_cohort_ever']:+.1f}"]
              for name in ("without Sec.2106", "+ published locations (no screen)", "+ relative screen (central)",
                           "p=0.5: relative screen (central)")]
    t_e = table(["case", "new RTO requests online by Nov 2041, GW", "that ever complete, GW", "sooner, not more",
                 "requests made in the rule's first six years: online by Nov 2041", "that ever complete"], rows_e)
    parts = [
        "# Where the Sec.2106 gain comes from (grid agents)",
        f"Mean [5th, 95th percentile] across {n} paired runs; every case is paired with current law under the same seeds, "
        "political draws and assumption changes. New capacity excludes relicensed hydro. GW online by Nov 2041.",
        "## A. Sec.2106 by component",
        "The single decision point removes the current-law re-study round (withdrawals raise the cost of those who stay, "
        "restudy_rho, and add restudy_months before agreement). Published locations add a share of requests at sites "
        "the provider has studied, at a fixed fee. The entry screen keeps out the requests least likely to complete.",
        t_a,
        "## B. The current-law re-study round",
        "Both current law and the bill change. With no re-study penalty under current law, Sec.2106's single decision "
        "point has little to remove.",
        t_b,
        "## By region: the entry screen",
        t_r,
        "## C. PJM and MISO counterfactuals",
        t_c, t_z,
        "## E. More or sooner",
        "Capacity from new requests in RTO regions. 'Ever complete' counts requests that reach operation after Nov "
        "2041 too; the difference is capacity the bill brings forward rather than adds.",
        t_e,
    ]
    if res["_meta"]["pre_refit_commit"]:
        F = lambda nm: res[f"F|{nm}"]["diff_GW_new"]
        t_f = table(["calibration before the Nov 2026 refit (commit " + res["_meta"]["pre_refit_commit"] + "), every RTO adopts",
                     "BAAJA minus current law, new GW"],
                    [[nm, _f(F(nm))] for nm in ("without Sec.2106", "relative screen (central)", "no screen", "absolute screen")])
        parts += ["## F. Screen specification under the earlier calibration", t_f]
    return "\n\n".join(parts) + "\n"
