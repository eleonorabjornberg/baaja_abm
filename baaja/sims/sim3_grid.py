"""Simulation 3: grid access - interconnection and transmission.
Bill (Senate-passed text, 19 Nov 2026): Sec.2106 (FERC rule within 18 months requiring each Transmission Organization,
i.e. RTO/ISO, to file a consolidated interconnection + regional planning process within 2 years: published interconnection
locations with an upfront, fixed, subregional per-MW fee, a single decision point, non-refundable security, withdrawal
penalties; FERC may find existing processes compliant), Sec.2110 (FERC rulemaking within 1 year on
computing/AI queue practices; no speed target), Sec.2101-2103 (transmission permitting, planning).
The text fixes no size for either effect, so this simulation is a sweep, not a point estimate."""
import os

from .. import experiments as ex
from .. import plots
from ..params import BAAJA, IXB
from . import regime_block, G3, fmt, headline, save, table

CUTS = [0.0, 0.05, 0.10, 0.20, 0.30, round(IXB["ercot_gap_cut"], 2)]   # last = ERCOT-pace ceiling [D]


def run(n_runs, cal, res_dir, fig_dir):
    base = ex.run_scenario({}, n_runs, cal)
    out, lines = [], {g: [] for g in G3}
    rule = {}
    for c in CUTS:
        a = ex.aggregate(ex.run_scenario(dict(BAAJA, ix_cut_rto=c), n_runs, cal), base)
        out.append((c, a))
        for g in G3:
            lines[g].append(a["diff_vs_baseline"][f"GW {g}"])
    for m in (24, 48):   # timing of the rules, at a 10% cut
        rule[m] = ex.aggregate(ex.run_scenario(dict(BAAJA, ix_cut_rto=0.10, ix_rule_month=m), n_runs, cal), base)["diff_vs_baseline"]
    rows = [[f"{100*c:.0f}%", fmt(a["diff_vs_baseline"]["GW_total"], 1, True)] + [fmt(a["diff_vs_baseline"][f"GW {g}"], 1, True) for g in G3]
            + [f"{100*a['diff_vs_baseline']['renewable share of new TWh']['mean']:+.2f}"] for c, a in out]
    b = ex.aggregate(base)["by_type"]
    ixrows = [[t, f"{b[t]['median_months_to_COD']['mean']:.0f}"] for t in ("Solar", "Onshore wind", "Offshore wind", "Gas", "Storage", "Geothermal")]
    reg_md, reg_res = regime_block({"Current law": {}, "BAAJA, 0% cut": BAAJA, "BAAJA, 10% cut": dict(BAAJA, ix_cut_rto=0.10)}, n_runs, cal)
    md = "\n\n".join([
        "# Simulation 3: grid access",
        "All data-based BAAJA provisions are on in every row; only the Sec.2106 study-time cut varies. In the Senate-passed "
        "text Sec.2106 applies to Transmission Organizations (RTO/ISO markets) only, so the cut applies to projects in "
        "ISO markets; non-ISO regions (Southeast, most of the West) are unaffected. ERCOT is counted as an ISO market here, "
        "although it is outside FERC's jurisdiction for these rules, so the GW below are somewhat overstated until the "
        "regional version (Phase 1) separates it. "
        "Sec.2110 applies to all public-utility transmission providers and sets no target (central 0%, range 0-5%). For Sec.2106 the data give a bracket, not a point: no measured "
        f"shortening from past queue reforms (floor 0%), and ERCOT's pace as a ceiling: ERCOT {IXB['median_months_2015_19']['ERCOT']:.0f} vs "
        f"CAISO/MISO {IXB['pooled_non_ERCOT_median']:.0f} months from request to signed agreement (2015-19 requests), a "
        f"{100*IXB['ercot_gap_cut']:.0f}% cut. Reaching it fully would also need energy-only interconnection, which the bill does not mandate. "
        "The cut applies to study months after the rules take effect (central month 36 = late 2029).",
        "## GW gained vs current law by interconnection cut",
        table(["study-time cut", "total GW", "renewable GW", "gas GW", "storage GW", "renewable share pts"], rows),
        reg_md,
        "## Timing of the rules (10% cut)",
        table(["rules affect studies from", "renewable GW", "gas GW"],
              [[f"month {m}", fmt(d["GW Renewable (new)"], 1, True), fmt(d["GW Fossil (gas)"], 1, True)] for m, d in rule.items()]),
        "## Median months from request to signed agreement by request year (regions with reliable agreement dates)",
        table(["region"] + [str(y) for y in range(2012, 2022)],
              [[r] + [f"{IXB['median_by_cohort'][r].get(str(y), float('nan')):.0f}" for y in range(2012, 2022)] for r in IXB["regions_used"]]),
        "## Why grid access dominates: current-law median months from request to operation (LBNL-calibrated)",
        table(["technology", "months"], ixrows),
    ])
    plots.sweep([100 * c for c in CUTS], lines, os.path.join(fig_dir, "sim3_grid_sweep.png"),
                "Sim 3: GW gained vs interconnection study-time cut (all other provisions on)", "study-time cut (%)", "GW vs current law")
    data = dict(regime_2025=reg_res, cuts=CUTS, results={str(c): a for c, a in out}, rule_timing={str(k): v for k, v in rule.items()})
    save("sim3_grid", data, md, res_dir)
    return md, data
