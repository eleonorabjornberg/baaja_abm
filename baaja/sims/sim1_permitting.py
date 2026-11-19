"""Simulation 1: permitting and build-out time.
Bill: Sec.1105-1109 (level of review, deadlines, CEs), 1202 (s.401), 1204 (s.404), 1302 (ESA s.7 60 days),
1402(c) (1-year deadline for permits needing no EA/EIS), 2102 (reconductoring CE), 2213 (renewable rights-of-way),
2229 (geothermal not a major federal action)."""
import os

from .. import experiments as ex
from .. import plots
from ..params import BASE, LEVERS
from . import G3, fmt, headline, save, sweep_table, table

P = LEVERS["permitting"]
ALONE = {
    "Sec.1106 deadlines": dict(deadline_bind=P["deadline_bind"]),
    "Sec.1105/1108 CE expansion + 1402(c) CE deadline": dict(ce_shift=P["ce_shift"], ce_cap=P["ce_cap"], deadline_bind=P["deadline_bind"]),
    "Sec.2213 renewable rights-of-way": dict(intake_pub_2213=P["intake_pub_2213"]),
    "Sec.1202 s.401 clock (hydro)": dict(nonnepa_hydro_1202=P["nonnepa_hydro_1202"]),
    "Sec.1302 ESA s.7 60 days": dict(esa_months=P["esa_months"]),
    "Sec.2102 reconductoring CE": dict(recond_ce=P["recond_ce"]),
    "Sec.2229 geothermal": dict(geo_ce=P["geo_ce"]),
}
SWEEP = ["deadline_bind", "ce_shift", "intake_pub_baaja", "intake_pub", "ea_share_nonEIS", "geo_ce", "delay_weight", "gas_arr_mult"]


def run(n_runs, cal, res_dir, fig_dir):
    scen = {"Current law": {}, "Permitting provisions (central)": P}
    scen.update({f"only {k}": v for k, v in ALONE.items()})
    raw = {k: ex.run_scenario(o, n_runs, cal) for k, o in scen.items()}
    base = raw["Current law"]
    res = {k: ex.aggregate(r, None if k == "Current law" else base) for k, r in raw.items()}
    sw = ex.assumption_sweep(P, SWEEP, n_runs, cal, base)
    b, z = res["Current law"]["totals"], res["Permitting provisions (central)"]["totals"]
    proc = []
    for g in G3:
        proc.append([g, fmt(b[f"median_months_to_permit | {g}"]), fmt(z[f"median_months_to_permit | {g}"]),
                     fmt(b[f"median_months_to_COD | {g}"]), fmt(z[f"median_months_to_COD | {g}"]),
                     f"{100*b[f'permitted_share | {g}']['mean']:.1f}% -> {100*z[f'permitted_share | {g}']['mean']:.1f}%",
                     f"{b[f'decisions | {g}']['mean']:.0f} -> {z[f'decisions | {g}']['mean']:.0f}"])
    bt = res["Current law"]["by_type"]; zt = res["Permitting provisions (central)"]["by_type"]
    tech = [[t, f"{bt[t]['decisions_per_year']['mean']:.1f}", f"{bt[t]['EIS_per_year']['mean']:.1f} -> {zt[t]['EIS_per_year']['mean']:.1f}",
             f"{100*zt[t]['truncated_share']['mean']:.0f}%", fmt(res['Permitting provisions (central)']['diff_by_type'][t]['median_months_to_permit'], 1, True),
             fmt(res['Permitting provisions (central)']['diff_by_type'][t]['GW_online'], 1, True)] for t in bt]
    md = "\n\n".join([
        "# Simulation 1: permitting and build-out time",
        "Federal review applies only to projects with a federal nexus (data: land, federal balancing areas, Corps individual "
        "permits, RUS), and only projects still alive at the decision count. GW = online by Nov 2041.",
        "## Outcome vs current law (GW)", headline(res, scen),
        "## Process, renewable vs gas (projects requested 2026-31; federal-nexus projects for permits)",
        table(["group", "months to permit, law", "BAAJA", "months to COD, law", "BAAJA", "permitted (of decided)", "decisions"], proc),
        "## By technology (permitting provisions, central)",
        table(["technology", "federal decisions / yr (law)", "EIS / yr law -> BAAJA", "reviews cut by deadlines", "months to permit change", "GW change"], tech),
        "## Sensitivity: each assumption at the low and high end of its range (other values central)", sweep_table(sw, SWEEP),
    ])
    plots.grouped_bars(G3, {"current law": [b[f"median_months_to_permit | {g}"] for g in G3],
                            "BAAJA permitting": [z[f"median_months_to_permit | {g}"] for g in G3]},
                       os.path.join(fig_dir, "sim1_months_to_permit.png"), "Sim 1: median months to federal permit", "months")
    c = res["Permitting provisions (central)"]["diff_vs_baseline"]["GW Renewable (new)"]["mean"]
    plots.tornado([(k, sw[k]["low"]["diff"]["GW Renewable (new)"]["mean"], sw[k]["high"]["diff"]["GW Renewable (new)"]["mean"]) for k in SWEEP],
                  c, os.path.join(fig_dir, "sim1_tornado_renewable_GW.png"), "Sim 1: renewable GW gain vs assumption", "GW gained vs current law")
    data = dict(scenarios=res, sweep=sw)
    save("sim1_permitting", data, md, res_dir)
    return md, data
