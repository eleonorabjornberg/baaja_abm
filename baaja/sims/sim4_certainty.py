"""Simulation 4: permit certainty across administrations (and operating permits / lifetimes).
Bill: Sec.1401 (Senate-passed text: no revoking, suspending or interfering with permits in effect on/after 6 Nov 2026
for non-federal sponsors, except court order, breach, fraud, urgent new harm, sponsor request, or (new in the passed
text) action "taken pursuant to any applicable law or regulation"; agency bears a clear-and-convincing
burden; sponsor recovers delay costs and 25-50% of project costs), Sec.1402 (suits over disparate treatment of a
project type), Sec.1110(c)(6) (remanded authorizations stay in effect), Sec.1203/1204 (NPDES and nationwide permit
terms 5 -> 10 years)."""
import os

from .. import experiments as ex
from .. import plots
from ..params import BAAJA, ENGINE, POLITICS
from . import regime_block, G3, fmt, save, sweep_table, table

SWEEP = ["halt_mult_1401", "halt_mult_other", "p_kill_halt", "halt_len"]


def run(n_runs, cal, res_dir, fig_dir):
    no1401 = dict(BAAJA, halt_mult=1.0)
    rows, halted, series = [], {}, {}
    for pname, path in POLITICS.items():
        b = ex.run_scenario({}, n_runs, cal, path)
        z = ex.run_scenario(BAAJA, n_runs, cal, path); y = ex.run_scenario(no1401, n_runs, cal, path)
        az, ay, ab = ex.aggregate(z, b), ex.aggregate(y, b), ex.aggregate(b)
        gain_1401 = {g: ex.band([a[f"GW {g}"] - c[f"GW {g}"] for a, c in zip(map(ex.totals, z), map(ex.totals, y))]) for g in G3}
        rows.append([pname, f"{ab['totals']['halted_GW_total']['mean']:.1f}", f"{ay['totals']['halted_GW_total']['mean']:.1f}",
                     f"{az['totals']['halted_GW_total']['mean']:.1f}"] + [fmt(gain_1401[g], 1, True) for g in G3])
        halted[pname] = dict(law=ab["totals"]["halted_GW_total"], no1401=ay["totals"]["halted_GW_total"], baaja=az["totals"]["halted_GW_total"])
        series[pname] = (ab, ay, az)
    base = ex.run_scenario({}, n_runs, cal)
    sw = ex.assumption_sweep(BAAJA, SWEEP, n_runs, cal, base)
    ab, ay, az = series["random (default)"]
    tech = [[t, f"{ab['by_type'][t]['halted']['mean']:.1f}", f"{az['by_type'][t]['halted']['mean']:.1f}",
             f"{ab['by_type'][t]['killed_by_courts_or_halts']['mean']:.1f} -> {az['by_type'][t]['killed_by_courts_or_halts']['mean']:.1f}"]
            for t in ab["by_type"] if ab["by_type"][t]["halted"]["mean"] > 0]
    ra = ENGINE["eia860"]["retirement_age"]
    life = [[t, f"{v['median_age']:.0f}", f"{v['mw_weighted_mean_age']:.0f}", f"{v['retired_since_2015_GW']:.1f}"] for t, v in ra.items()]
    reg_md, reg_res = regime_block({"Current law": {}, "BAAJA": BAAJA, "BAAJA without Sec.1401": no1401}, n_runs, cal)
    md = "\n\n".join([
        "# Simulation 4: permit certainty across administrations",
        "Executive halts hit permitted projects that are not yet online after a change of administration hostile to their "
        "side. Offshore wind's halt probability is anchored on the 2025 stop-work orders; other technologies are ranges. "
        "Sec.1401 leaves a residual halt probability for its exceptions: central 50%, range 10-100%, because the Senate-passed "
        "text adds an exception for action 'taken pursuant to any applicable law or regulation', which could cover stop-work "
        "orders like 2025's.",
        "## Halted GW by political path, and what Sec.1401 adds (BAAJA with vs without Sec.1401)",
        table(["political path", "halted GW, law", "BAAJA w/o 1401", "BAAJA"] + [f"1401 gain: {g}" for g in G3], rows),
        reg_md,
        "## Projects halted and cancelled, by technology (random politics; law vs BAAJA)",
        table(["technology", "halted, law", "halted, BAAJA", "cancelled (courts or halts)"], tech),
        "## Plant lifetimes (EIA-860 retired generators)",
        "Plants built from 2026 do not reach retirement age before 2041, so lifetimes do not change the 2041 totals. "
        "The bill's operating-permit terms (NPDES 10 years, Sec.1203) matter for existing gas plants' renewals, which "
        "this model does not track.",
        table(["technology", "median age at retirement", "MW-weighted mean", "GW retired since 2015"], life),
        "## Sensitivity (all provisions; other values central)", sweep_table(sw, SWEEP, ("halted_GW_total", "halted GW")),
    ])
    plots.grouped_bars(list(POLITICS), {"current law": [halted[p]["law"] for p in POLITICS],
                                        "BAAJA without 1401": [halted[p]["no1401"] for p in POLITICS],
                                        "BAAJA": [halted[p]["baaja"] for p in POLITICS]},
                       os.path.join(fig_dir, "sim4_halted_GW.png"), "Sim 4: GW halted after hostile turnovers", "GW halted", fmt="{:.1f}")
    data = dict(regime_2025=reg_res, halted=halted, sweep=sw, lifetimes=ra)
    save("sim4_certainty", data, md, res_dir)
    return md, data
