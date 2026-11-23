"""Simulation 5: utility vs merchant decision control.
Bill: Sec.2105 (no federal right of first refusal for regional/interregional transmission selected for cost allocation),
Sec.2104 (FERC oversight of local transmission planning on state referral), Sec.2106 (consolidated planning in every
transmission planning region), Sec.2107 (transmission costs for computational loads), Sec.2108 (market access for
dispatchable behind-the-meter resources).
What the data support: projects split by market (ISO/RTO, mostly merchant vs non-ISO West/Southeast, where vertically
integrated utilities plan), with completion by market from LBNL; ownership shares by technology from EIA-860.
What they do not: any measured effect of ROFR removal or consolidated planning on generation; those enter only through
the Sec.2106 interconnection range of Simulation 3, applied to each market."""
import os

from .. import experiments as ex
from .. import plots
from ..calibrate import calibrate_markets
from ..params import BAAJA, ENGINE, GEN, REGIONS, UTILITY_OWNED
from . import regime_block, fmt, save, table

MK = ("ISO", "non-ISO")


def _by_market(agg, t, m, key="by_type"):
    return agg[key][t].get(f"GW_online|{m}")


def run(n_runs, cal, res_dir, fig_dir):
    # regional hazards (calibrate_regions) already give ISO / non-ISO completion; fit by market only if absent
    has_regions = any(k.split("|")[-1] in REGIONS for k in cal["hazard"] if "|" in k)
    calm, targets = (cal, {}) if has_regions else calibrate_markets(cal)
    base = ex.run_scenario({}, n_runs, calm)
    scen = {"BAAJA (data-based)": BAAJA, "BAAJA + Sec.2106 at 15%": dict(BAAJA, ix_cut_rto=0.15)}
    res = {}
    for k, o in scen.items():
        z = ex.run_scenario(o, n_runs, calm)
        res[k] = {t: {m: ex.band([a[t][f"GW_online|{m}"] - b[t][f"GW_online|{m}"] for a, b in zip(z, base)]) for m in MK} for t in GEN}
    lvl = {t: {m: ex.band([b[t][f"GW_online|{m}"] for b in base]) for m in MK} for t in GEN}
    rows = []
    for t in GEN:
        bm = ENGINE["lbnl"]["by_market"][t]
        rows.append([t, f"{100*bm['non-ISO']['arrivals_share_2021_25']:.0f}%",
                     f"{100*(bm['ISO']['completion'] or 0):.0f}% / {100*(bm['non-ISO']['completion'] or 0):.0f}%" if bm['non-ISO']['completion'] is not None else f"{100*(bm['ISO']['completion'] or 0):.0f}% / -",
                     f"{100*UTILITY_OWNED[t]:.0f}%", f"{lvl[t]['ISO']['mean']:.0f} / {lvl[t]['non-ISO']['mean']:.0f}"]
                    + [f"{res[k][t]['ISO']['mean']:+.1f} / {res[k][t]['non-ISO']['mean']:+.1f}" for k in scen])
    own = []
    for k in scen:
        u = sum(UTILITY_OWNED[t] * (res[k][t]["ISO"]["mean"] + res[k][t]["non-ISO"]["mean"]) for t in GEN)
        tot = sum(res[k][t]["ISO"]["mean"] + res[k][t]["non-ISO"]["mean"] for t in GEN)
        own.append([k, f"{tot:+.1f}", f"{u:+.1f}", f"{tot - u:+.1f}"])
    reg_md, reg_res = regime_block({"Current law": {}, "BAAJA (data-based)": BAAJA}, n_runs, calm)
    md = "\n\n".join([
        "# Simulation 5: utility vs merchant decision control",
        "Each project is in an ISO/RTO market (mostly merchant developers) or a non-ISO region (West, Southeast: vertically "
        "integrated utilities plan and own more). Withdrawal hazards are fitted to LBNL completion by region (and so by market), scaled to each technology's national target.",
        "## By technology: market split, completion, utility ownership, GW online by 2041 and BAAJA gain (ISO / non-ISO)",
        table(["technology", "non-ISO share of requests", "completion ISO / non-ISO", "utility-owned share of new MW (EIA-860)",
               "GW 2041, law"] + [f"gain: {k}" for k in scen], rows),
        reg_md,
        "## Who gets the gain: utility-owned vs merchant (EIA-860 ownership shares applied to each technology's gain)",
        table(["scenario", "total GW gain", "utility-owned", "merchant / other"], own),
        "## Not modelled with data",
        "Sec.2105 (no ROFR) and Sec.2104 change who builds transmission, not when generation connects; the model has no "
        "measured link from transmission sponsorship to generator completion. Sec.2108 concerns behind-the-meter resources, "
        "outside the interconnection queue. Sec.2107 assigns transmission costs to computational loads (data centers) and "
        "Sec.2114 requires data collection on them: they change who pays and what is reported, not generator timing. "
        "These are listed, not simulated; the data-center build-out enters only through the 2025 request regime.",
    ])
    cats = [t for t in GEN if t != "Geothermal"]
    plots.grouped_bars(cats, {f"{k}: {m}": [res[k][t][m] for t in cats] for k in scen for m in MK},
                       os.path.join(fig_dir, "sim5_gain_by_market.png"), "Sim 5: GW gained by market type", "GW vs current law",
                       colors=["#9ec5f0", "#2a78d6", "#f5b79c", "#eb6834"], fmt="{:.1f}")
    data = dict(regime_2025=reg_res, market_targets=targets, hazard_by_market={k: v for k, v in calm["hazard"].items() if "|" in k},
                gain_by_market=res, level_by_market=lvl)
    save("sim5_decision_control", data, md, res_dir)
    return md, data
