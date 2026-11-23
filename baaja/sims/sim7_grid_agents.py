"""Simulation 7: grid access as an agent-based system (Phase 2).

Question: once queues, study capacity, network-upgrade costs and developers' choices interact, what do BAAJA's grid
sections (Sec.2106 published locations and single decision point, Sec.2110 study throughput, Sec.2109 transmission
hosting, Title I transmission permitting) add to supply by 2041, and where?

Grid operators run cluster studies (ERCOT: individual studies) at a throughput that adapts to the arrival rate;
developers enter on the published wait and regional scarcity, and withdraw at study results when the allocated
cost exceeds their value. Every scenario is paired with current law under the same agents (same seeds, draws and
political path). The validation section compares the operators and developers with LBNL data they were not fitted
to where possible (2020-24 cohorts, withdrawal timing, completion by cost).
"""
import numpy as np

from .. import experiments as ex
from .. import grid as gr
from .. import supply as sp
from ..model import simulate, summarize
from ..params import BAAJA, GRID_BILL, GRID_LAW, LEVER_KEY, REGIONS, TYPES
from . import G3, fmt, headline, save, table
from .sim6_supply import national, summarize_scenarios

AG = dict(grid="agents")
WINDOW = (0, 60)                        # requests made Dec 2025 - Nov 2030


def scenarios():
    b = dict(BAAJA, **AG)
    return {"Current law": dict(AG),
            "BAAJA": b,
            "BAAJA without Sec.2106": dict(b, grid_2106=False),
            "BAAJA without Sec.2109 hosting": dict(b, grid_2109=0.0),
            "Sec.2106 only": dict(AG, grid_2106=True),
            "BAAJA, Sec.2106 adopted by every RTO": dict(b, adopt_2106=1.0),
            f"BAAJA + Sec.2110 throughput +{100 * GRID_BILL['g_2110'][2]:.0f}%": dict(b, grid_2110=GRID_BILL["g_2110"][2])}


def grid_stats(rows, window=WINDOW):
    """Per region: new requests entered (per year), median months request -> agreement and share signed, share
    withdrawn at study results, GW online by the horizon; new requests made in `window`."""
    G = [r for r in rows if "gwd" in r]
    cat = lambda k: np.concatenate([np.broadcast_to(r[k], r["t0"].shape) for r in G])
    t0, tIA, gwd, reg, seeded, done, tCOD = (cat(k) for k in ("t0", "tIA", "gwd", "region", "seeded", "done", "tCOD"))
    mw = np.concatenate([np.full(r["t0"].shape, float(r["mw"])) for r in G])
    T = G[0]["T"]
    sel = ~seeded & (t0 >= window[0]) & (t0 < window[1])
    on = done & (tCOD <= T)
    out = {}
    for k, r in enumerate(REGIONS):
        s = sel & (reg == k)
        sig = s & np.isfinite(tIA)
        out[r] = dict(requests_per_year=float(s.sum() / ((window[1] - window[0]) / 12)),
                      months_to_IA=float(np.median(tIA[sig] - t0[sig])) if sig.any() else np.nan,
                      share_signed=float(sig.sum() / s.sum()) if s.any() else np.nan,
                      withdrawn_at_results=float(np.isfinite(gwd[s]).mean()) if s.any() else np.nan,
                      GW_online=float((mw * (on & (reg == k))).sum() / 1000))
    return out


def _bin(b):
    lo, hi = b.split("-")
    return f"{lo}+" if float(hi) >= 1e8 else b


def cost_completion(rows):
    """Completion by allocated cost bin ($/kW), new requests that received a study result, ISO regions."""
    G = [r for r in rows if "gwd" in r]
    cat = lambda k: np.concatenate([np.broadcast_to(r[k], r["t0"].shape) for r in G])
    cost, done, reg, seeded = cat("cost"), cat("done"), cat("region"), cat("seeded")
    iso = ~np.isin(reg, [REGIONS.index("Southeast"), REGIONS.index("West")])
    s = ~seeded & np.isfinite(cost) & iso
    bins = [0, 10, 50, 100, 200, 400, 1e9]
    return {f"{bins[i]}-{bins[i + 1]}": float(done[s & (cost > bins[i]) & (cost <= bins[i + 1])].mean())
            if (s & (cost > bins[i]) & (cost <= bins[i + 1])).any() else np.nan for i in range(len(bins) - 1)}


def run_set(over, n_runs, cal, extra=False):
    p = ex.params(over, cal)
    S, G, X = [], [], []
    for s in range(n_runs):
        rows = simulate(p, s, ex.politics_draw(s, len(p["turnovers"])))
        S.append(summarize(rows, p))
        if p["grid"] == "agents":
            G.append(grid_stats(rows))
            if extra:
                X.append(dict(wd=gr.withdrawal_curve_model(rows), cost=cost_completion(rows)))
    return S, G, X


def _m(G, r, k):
    return float(np.nanmean([g[r][k] for g in G]))


def run(n_runs, cal, res_dir, fig_dir, sweep_runs=None):
    if not (cal.get("grid_cal") or {}).get("operators"):
        raise ValueError("Sim 7 needs the grid calibration (run.py --all, or calibrate.calibrate_grid)")
    scen = scenarios()
    raw, gst, xtra = {}, {}, {}
    for k, o in scen.items():
        raw[k], gst[k], x = run_set(o, n_runs, cal, extra=(k == "Current law"))
        if x:
            xtra = x
    exo = {"Current law (exogenous grid)": {}, "BAAJA (exogenous grid)": dict(BAAJA)}
    raw_exo = {k: run_set(o, n_runs, cal)[0] for k, o in exo.items()}
    base = raw["Current law"]
    res = {k: ex.aggregate(r, None if k == "Current law" else base) for k, r in raw.items()}
    res_exo = {k: ex.aggregate(r, None if i == 0 else raw_exo["Current law (exogenous grid)"])
               for i, (k, r) in enumerate(raw_exo.items())}

    # ---- headline: GW by group, firm capacity and shortfall ----
    sa = sp.SA
    sups, nat = summarize_scenarios(raw, sa)
    k35, k41 = sp.YEARS.index(2035), sp.YEARS.index(2041)
    lawn = nat["Current law"]
    rows = []
    for k in list(scen)[1:]:
        d = res[k]["diff_vs_baseline"]
        z = nat[k]
        dfirm = (z["firm"] - lawn["firm"])[:, k35] / 1000
        dsh = (z["shortfall"] - lawn["shortfall"]) / 1000
        rows.append([k] + [fmt(d[f"GW {g}"], 1, True) for g in G3] + [fmt(d["GW_total"], 1, True),
                     fmt(ex.band(dfirm), 1, True), fmt(ex.band(dsh[:, k35]), 1, True), fmt(ex.band(dsh[:, k41]), 1, True)])
    t_head = table(["scenario (grid agents)", "renewable GW", "gas GW", "storage GW", "total GW", "firm GW 2035",
                    "shortfall GW 2035", "shortfall GW 2041"], rows)
    dx = res_exo["BAAJA (exogenous grid)"]["diff_vs_baseline"]
    t_cmp = table(["grid model", "current law total GW 2041", "BAAJA minus current law, total GW", "renewable GW", "gas GW", "storage GW"],
                  [["exogenous study times (Sims 1-6)", fmt(res_exo["Current law (exogenous grid)"]["totals"]["GW_total"], 0),
                    fmt(dx["GW_total"], 1, True)] + [fmt(dx[f"GW {g}"], 1, True) for g in G3],
                   ["grid agents (this simulation)", fmt(res["Current law"]["totals"]["GW_total"], 0),
                    fmt(res["BAAJA"]["diff_vs_baseline"]["GW_total"], 1, True)]
                   + [fmt(res["BAAJA"]["diff_vs_baseline"][f"GW {g}"], 1, True) for g in G3]])

    # ---- current-law adequacy: exogenous study times vs grid agents (scarcity feedback on) ----
    sups_x, nat_x = summarize_scenarios({"law": raw_exo["Current law (exogenous grid)"]}, sa)
    k27 = sp.YEARS.index(2027)
    adq = {}
    for name, sv, nv in (("exogenous study times (Sims 1-6)", sups_x["law"], nat_x["law"]),
                         ("grid agents (this simulation)", sups["Current law"], lawn)):
        adq[name] = dict(national={y: ex.band(nv["shortfall"][:, k] / 1000) for y, k in ((2027, k27), (2035, k35), (2041, k41))},
                         below_2035=ex.band(nv["regions_below_rml"][:, k35]),
                         region_2035={r: float(np.mean([x["shortfall"][i, k35] for x in sv]) / 1000) for i, r in enumerate(REGIONS)},
                         margin_2035={r: float(np.mean([x["reserve_margin"][i, k35] for x in sv])) for i, r in enumerate(REGIONS)})
    t_adq = table(["grid model", "shortfall GW 2027", "shortfall GW 2035", "shortfall GW 2041", "regions below reference margin, 2035"],
                  [[n, fmt(a["national"][2027], 0), fmt(a["national"][2035], 0), fmt(a["national"][2041], 0), fmt(a["below_2035"], 1)]
                   for n, a in adq.items()])
    ax, aa = adq["exogenous study times (Sims 1-6)"], adq["grid agents (this simulation)"]
    t_adr = table(["region", "reserve margin 2035: exogenous / agents", "shortfall GW 2035: exogenous / agents"],
                  [[r, f"{100 * ax['margin_2035'][r]:.0f}% / {100 * aa['margin_2035'][r]:.0f}%",
                    f"{ax['region_2035'][r]:.1f} / {aa['region_2035'][r]:.1f}"] for r in REGIONS])

    # ---- by region ----
    L, B = gst["Current law"], gst["BAAJA"]
    A1 = gst["BAAJA, Sec.2106 adopted by every RTO"]
    rrows = []
    for r in REGIONS:
        rrows.append([r, f"{_m(L, r, 'requests_per_year'):.0f}", f"{_m(L, r, 'months_to_IA'):.0f}", f"{_m(L, r, 'share_signed'):.2f}",
                      f"{_m(L, r, 'withdrawn_at_results'):.2f}", f"{_m(L, r, 'GW_online'):.0f}",
                      f"{_m(B, r, 'requests_per_year') - _m(L, r, 'requests_per_year'):+.0f}",
                      f"{_m(B, r, 'months_to_IA') - _m(L, r, 'months_to_IA'):+.1f}",
                      f"{_m(B, r, 'share_signed') - _m(L, r, 'share_signed'):+.3f}",
                      f"{_m(B, r, 'GW_online') - _m(L, r, 'GW_online'):+.1f}",
                      f"{_m(A1, r, 'GW_online') - _m(L, r, 'GW_online'):+.1f}"])
    t_reg = table(["region", "law: requests/yr", "law: months to agreement", "law: share signed", "law: withdrawn at results",
                   "law: GW online 2041", "BAAJA: requests/yr", "BAAJA: months", "BAAJA: share signed", "BAAJA: GW",
                   "2106 everywhere: GW"], rrows)

    # ---- validation ----
    ops = cal["grid_cal"]["operators"]
    vrows = []
    for r in REGIONS:
        o = ops[r]
        ho = "; ".join(f"{y}: {v['model_median']:.0f}/{v['data_median']:.0f}" for y, v in o["holdout"].items()
                       if v["model_median"] is not None and v["data_median"] is not None)
        fy = "; ".join(f"{y}: {v['model_median']:.0f}/{v['data_median']:.0f}" for y, v in o["fit"].items()
                       if str(y) in ("2010", "2014", "2017", "2019") and v["model_median"] is not None and v["data_median"] is not None)
        vrows.append([r, "own fit" if o["fitted"] else "pooled (MISO+CAISO)", f"{o['C']}/{'serial' if o['serial'] else 'parallel'}",
                      o["d"], f"{o['fit_error']:.2f}", f"{o['holdout_error']:.2f}", fy, ho or "-"])
    t_ops = table(["region", "operator", "cluster months / mode", "min study months", "fit error 2010-19", "holdout error 2020-24",
                   "fit cohorts: model/data median months", "holdout cohorts: model/data"], vrows)
    wdd = gr.withdrawal_curve_data()
    wrows = []
    for r in REGIONS:
        if r not in wdd:
            continue
        mm = {m: np.nanmean([x["wd"].get(r, {}).get(m, np.nan) for x in xtra]) for m in gr.WD_MONTHS}
        wrows.append([r] + [f"{mm[m]:.2f} / {wdd[r][m]:.2f}" for m in gr.WD_MONTHS])
    t_wd = table(["region"] + [f"withdrawn by {m} months: model / data" for m in gr.WD_MONTHS], wrows)
    vb = gr.GT["value"]["ISO"]["completion_by_cost_bin"]
    cc = {b: np.nanmean([x["cost"][b] for x in xtra]) for b in vb}
    t_cost = table(["allocated cost $/kW", "model: share completing", "LBNL: share completing (resolved requests)", "LBNL n"],
                   [[_bin(b), f"{cc[b]:.2f}", f"{v[0]:.2f}" if v[0] is not None else "-", v[1]] for b, v in vb.items()])
    gc = cal["grid_cal"]
    t_cod = table(["technology", "LBNL median months request -> operation (completed)", "exogenous grid (model)", "grid agents (model)"],
                  [[t, f"{TYPES[t]['cod_target']:.0f}" if TYPES[t]["cod_target"] else "-",
                    f"{res_exo['Current law (exogenous grid)']['by_type'][t]['median_months_to_COD']['mean']:.0f}",
                    f"{res['Current law']['by_type'][t]['median_months_to_COD']['mean']:.0f}"]
                   for t in ("Solar", "Onshore wind", "Gas", "Storage")])
    t_vm = table(["technology", "region", "value scale (fitted to completion)"],
                 [[*(k.split("|") if "|" in k else (k, "all (pooled)")), f"{v:.2f}"]
                  for k, v in sorted((gc.get("value_mult") or {}).items())])
    t_hz = table(["region", "pre-agreement withdrawal hazard, %/month"],
                 [[r, f"{100 * v:.2f}"] for r, v in (gc.get("h_pre") or {}).items()])

    # ---- sensitivity: grid assumptions (current law and bill design), paired ----
    ns = sweep_runs or max(n_runs // 5, 10)
    srows, sdata = [], {}
    base_s = {}
    for key, (lo, c, hi, note) in list(GRID_LAW.items()) + list(GRID_BILL.items()):
        cells = []
        for v in (lo, hi):
            lk = LEVER_KEY.get(key, key)
            if key in GRID_LAW:
                law_o, bill_o = dict(AG, **{key: v}), dict(scen["BAAJA"], **{key: v})
            else:
                law_o, bill_o = dict(AG), dict(scen["BAAJA"], **{lk: v})
            if key in GRID_LAW or "law" not in base_s:
                Ls = run_set(law_o, ns, cal)[0]
                if key not in GRID_LAW:
                    base_s["law"] = Ls
            else:
                Ls = base_s["law"]
            Bs = run_set(bill_o, ns, cal)[0]
            d = [ex.totals(b)["GW_total"] - ex.totals(a)["GW_total"] for a, b in zip(Ls, Bs)]
            lt = np.mean([ex.totals(a)["GW_total"] for a in Ls])
            cells.append((float(np.mean(d)), float(lt)))
        sdata[key] = dict(low=lo, high=hi, diff_low=cells[0][0], diff_high=cells[1][0], law_low=cells[0][1], law_high=cells[1][1])
        srows.append([key + (" (current law)" if key in GRID_LAW else " (bill)"), f"{lo} / {hi}",
                      f"{cells[0][0]:+.1f} / {cells[1][0]:+.1f}", f"{cells[0][1]:.0f} / {cells[1][1]:.0f}", note])
    t_sens = table(["assumption", "low / high", "BAAJA minus current law, total GW", "current law total GW", "what it is"], srows)

    md = "\n\n".join([
        "# Simulation 7: grid access as an agent-based system",
        "Interconnection is no longer a drawn study time. Each region's grid operator studies requests in clusters "
        "(ERCOT: one by one) at a throughput fitted to LBNL request-to-agreement times and adapting to the arrival rate; "
        "developers enter on the published wait and on their region's projected capacity shortfall, and leave at study "
        "results when the allocated network-upgrade cost exceeds their private value (both from LBNL cost data). Upgrade "
        "costs rise as capacity is signed and fall as transmission is built. Sec.2106 becomes published locations with a "
        "fixed fee and a single decision point in RTOs that change their process (drawn per RTO); Sec.2110 a throughput "
        "multiplier (0 by default: the bill does not size it); Sec.2109 extra hosting per transmission line built after "
        "the rule. Every scenario is paired with current law under the same agents. Numbers: mean [5th, 95th percentile] "
        f"across {n_runs} runs, GW online by Nov 2041.",
        "## What the grid sections add (difference from current law, grid agents)",
        t_head,
        "## Exogenous study times vs grid agents",
        "Sims 1-6 draw each request's study time; here it comes out of the queue. The agents' current law is lower "
        "because study results now remove projects whose upgrade costs exceed their value, on top of the fitted hazards.",
        t_cmp,
        "### Current law: capacity shortfall below reference margins",
        "With grid agents, developers respond to their region's projected shortfall, so surpluses and shortfalls are no "
        "longer fixed by the 2021-25 request mix, but fewer projects get through the queue overall.",
        t_adq,
        t_adr,
        "## By region (requests made 2026-30; mean across runs)",
        t_reg,
        "## Validation",
        "### Grid operators: months from request to signed agreement, by request year (LBNL)",
        "Fitted on 2010-19 cohorts; 2020-24 cohorts are a holdout. Error: mean squared log ratio of median months plus "
        "squared difference in the share signed by Dec 2025, by cohort. Regions without reliable agreement dates take "
        "the joint MISO+CAISO fit.",
        t_ops,
        "### Developers: share of requests withdrawn by months after request (2015-19 cohorts vs model 2026-30)",
        "Fitted at 24 months (one pre-agreement hazard per region); 12, 36 and 60 months are checks. Data counts still-"
        "active requests as not withdrawn.",
        t_wd,
        "The checks fail after 24 months: in the model almost every request that will withdraw has done so by 36-60 "
        "months, at its study result, while in the data a fifth to a third of 2015-19 requests were still active after "
        "five years and withdrew later, often after signing an agreement. Completion still matches (below), so the "
        "model front-loads withdrawal rather than over-counting it. This is the clearest misfit of the grid agents: the "
        "model has no late withdrawals, so it cannot show what Sec.2106(a)(3)'s single decision point and withdrawal "
        "penalties would do to them, and that part of the section is likely understated.",
        t_hz,
        "### Developers: value relative to LBNL's P(complete | cost) fit",
        "One scale per technology and region, fitted so completion of new requests matches the regional LBNL targets. "
        "Values below 1 mean fewer requests complete than LBNL's cost-completion relation alone implies.",
        t_vm,
        "### Time from request to operation, completed projects",
        "Known gap: in the agents model, waiting longer does not make a request more likely to withdraw (the background "
        "hazard is small and fitted to withdrawal timing), so completed projects are not selected for short waits as in "
        "the data and their median time to operation is longer than LBNL's. This lowers current-law GW by 2041 relative "
        "to the exogenous model; the bill's effect is a paired difference under the same agents.",
        t_cod,
        "### Developers: completion by allocated network-upgrade cost (ISO regions)",
        "LBNL counts requests resolved by 2024 (completed vs withdrawn); the model counts every 2026-41 request that "
        "received a study result, so the level differs; the gradient is the check.",
        t_cost,
        f"## Sensitivity: grid assumptions at the low and high end of their ranges ({ns} paired runs each)",
        t_sens,
    ])
    data = dict(results={k: v for k, v in res.items()}, exogenous=res_exo,
                regions={k: {r: {m: _m(v, r, m) for m in v[0][r]} for r in REGIONS} for k, v in gst.items()},
                operators={r: {k: v for k, v in o.items()} for r, o in ops.items()},
                withdrawal={"data": wdd, "model": {r: {m: float(np.nanmean([x["wd"].get(r, {}).get(m, np.nan) for x in xtra]))
                                                       for m in gr.WD_MONTHS} for r in REGIONS}},
                cost_completion={"model": cc, "data": vb}, sensitivity=sdata, adequacy_current_law=adq,
                supply={k: {"firm_2035": ex.band((nat[k]["firm"] - lawn["firm"])[:, k35] / 1000),
                            "shortfall_2035": ex.band((nat[k]["shortfall"] - lawn["shortfall"])[:, k35] / 1000)}
                        for k in list(scen)[1:]})
    save("sim7_grid_agents", data, md, res_dir)
    return md, data
