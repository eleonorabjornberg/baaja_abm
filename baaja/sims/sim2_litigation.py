"""Simulation 2: litigation - how much projects are sued, by whom, with what outcome.
Bill: Sec.1110 (NEPA claims: 150 days, comment exhaustion, direct injury, appeals-court original jurisdiction, remand
without vacatur or injunction <= 180 days), 2201 (150 days and expedited review for all federal claims on energy
authorizations), 1205, 1305. Outside the bill: state-court and administrative litigation (Sabin)."""
import json
import os

from .. import experiments as ex
from .. import plots
from ..params import BAAJA, CHALLENGERS, LEVERS, _load
from . import G3, fmt, headline, save, sweep_table, table

L = LEVERS["litigation"]
SWEEP = ["late_adapt", "exhaust_injury", "suit_payoff", "inj_nonNEPA", "lit_months_baaja", "lit_data_mult", "lit_ea", "p_kill_vac", "remand_months"]


def run(n_runs, cal, res_dir, fig_dir):
    scen = {"Current law": {}, "Court provisions only (Sec.1110/2201)": L, "All data-based provisions": BAAJA}
    raw = {k: ex.run_scenario(o, n_runs, cal) for k, o in scen.items()}
    base = raw["Current law"]
    res = {k: ex.aggregate(r, None if k == "Current law" else base) for k, r in raw.items()}
    sw = ex.assumption_sweep(L, SWEEP, n_runs, cal, base)
    b, c, a = (res[k]["totals"] for k in scen)
    rows = []
    for g in G3:
        for ch in CHALLENGERS:
            sb, sc, sa = b[f"suits: {ch} | {g}"]["mean"], c[f"suits: {ch} | {g}"]["mean"], a[f"suits: {ch} | {g}"]["mean"]
            wb = b[f"challenger wins: {ch} | {g}"]["mean"]
            rows.append([g, ch, f"{sb:.1f}", f"{sc:.1f}", f"{sa:.1f}", f"{100*wb/sb:.0f}%" if sb else "-"])
    bt, ct = res["Current law"]["by_type"], res["Court provisions only (Sec.1110/2201)"]["by_type"]
    tech = [[t, f"{bt[t]['suits_per_year']['mean']:.2f} -> {ct[t]['suits_per_year']['mean']:.2f}",
             f"{bt[t]['vacated']['mean']:.1f} -> {ct[t]['vacated']['mean']:.1f}",
             f"{bt[t]['killed_by_courts_or_halts']['mean']:.1f} -> {ct[t]['killed_by_courts_or_halts']['mean']:.1f}"] for t in bt]
    s = _load("permits_opposition_targets.json")["sabin"]["contested_by_type"]
    sab = [[t, v["contested"], v["litigated"], v["federal_venue"], v["state_or_admin_only"], v["canceled"]] for t, v in s.items()]
    md = "\n\n".join([
        "# Simulation 2: litigation",
        "Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win "
        "rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).",
        "## Outcome vs current law (GW)", headline(res, scen),
        "## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)",
        table(["group", "challenger", "law", "courts only", "all", "challenger win rate (law)"], rows),
        "## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)",
        table(["technology", "suits / yr", "vacated", "cancelled"], tech),
        "## Litigation BAAJA does not reach: Sabin Center contested renewable projects (2026 database)",
        table(["type", "contested", "litigated", "federal venue", "state / administrative only", "cancelled"], sab),
        "## Sensitivity (court provisions; other values central)", sweep_table(sw, SWEEP),
    ])
    plots.grouped_bars(CHALLENGERS, {g + ", law": [b[f"suits: {ch} | {g}"] for ch in CHALLENGERS] for g in ("Renewable (new)", "Fossil (gas)")}
                       | {g + ", BAAJA courts": [c[f"suits: {ch} | {g}"] for ch in CHALLENGERS] for g in ("Renewable (new)", "Fossil (gas)")},
                       os.path.join(fig_dir, "sim2_who_sues.png"), "Sim 2: suits 2026-41 by lead challenger", "suits",
                       colors=["#9ddcc4", "#f5b79c", "#1baf7a", "#eb6834"], fmt="{:.0f}")
    data = dict(scenarios=res, sweep=sw, sabin=s)
    save("sim2_litigation", data, md, res_dir)
    return md, data
