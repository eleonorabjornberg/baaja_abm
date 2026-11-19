"""Simulation 2: litigation - how much projects are sued, by whom, with what outcome.
Bill: Sec.1110 (NEPA claims: 150 days, comment exhaustion, direct injury, appeals-court original jurisdiction, remand
without vacatur or injunction <= 180 days), 2201 (150 days and expedited review for all federal claims on energy
authorizations), 1205, 1305. Outside the bill: state-court and administrative litigation (Sabin)."""
import json
import os

from .. import experiments as ex
from .. import plots
from ..params import A, BAAJA, CASES, CEQ, CHALLENGERS, LATE_SHARE, LEVERS, _load
from . import regime_block, G3, fmt, headline, save, sweep_table, table

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
    # fossil comparison: gas pipelines and LNG (not a generation technology in the model) vs renewables, from data
    side = []
    for g, lab in (("Renewable", "Renewables (wind, solar, geothermal)"), ("Fossil infrastructure", "Gas pipelines and LNG"),
                   ("Transmission", "Transmission")):
        v = CASES["by_group"][g]; mix = [v["lead_mix"][c] for c in CHALLENGERS]
        keep = sum(m * (1 - LATE_SHARE[j] * (1 - A["late_adapt"])) for j, m in enumerate(mix)) / sum(mix)
        keep *= A["exhaust_injury"] * A["suit_payoff"]
        side.append([lab, f"{v['cases_per_year_2012_21']:.1f}", f"{100*v['share_filed_after_150_days']:.0f}%", f"{100*v['challenger_win']:.0f}%",
                     f"{100*v['injunction_share']:.0f}%", f"{100*v['vacatur_share_of_remands']:.0f}% (n={v['n_remands']})", f"{100*keep:.0f}%"])
    pl = CEQ["types"].get("Gas pipeline/LNG (not modelled)", {})
    s = _load("permits_opposition_targets.json")["sabin"]["contested_by_type"]
    sab = [[t, v["contested"], v["litigated"], v["federal_venue"], v["state_or_admin_only"], v["canceled"]] for t, v in s.items()]
    reg_md, reg_res = regime_block(scen, n_runs, cal)
    md = "\n\n".join([
        "# Simulation 2: litigation",
        "Suits are drawn only for projects with a federal decision that are still alive at that decision. Challenger mix, win "
        "rates, injunction and vacatur rates, filing delays and case length come from 1,821 NEPA cases (2001-22).",
        "## Outcome vs current law (GW)", headline(res, scen),
        reg_md,
        "## Who sues: suits 2026-41 by lead challenger (current law / court provisions / all provisions)",
        table(["group", "challenger", "law", "courts only", "all", "challenger win rate (law)"], rows),
        "## By technology: suits per year, permits vacated, projects cancelled by courts or halts (law -> court provisions)",
        table(["technology", "suits / yr", "vacated", "cancelled"], tech),
        "## Fossil comparison: gas pipelines and LNG vs renewables (case data, 2012-21; current law)",
        f"Pipelines and LNG are not a generation technology in the model, but they carry most fossil NEPA litigation. CEQ "
        f"counts {pl.get('eis_per_year', 0):.1f} pipeline/LNG EISs a year (median {pl.get('median_months_noi_to_feis', 0):.0f} months). "
        "The last column applies the central Sec.1110 filters (150-day limit with observed filing delays and adaptation, "
        "comment exhaustion + direct injury, remand-only payoff) to each group's challenger mix. FERC certificate cases "
        "already face Natural Gas Act deadlines (30-day rehearing, 60-day petition) and appeals-court review, so for those "
        "the 150-day limit changes little; the remedy limit (no vacatur) is what binds.",
        table(["group", "NEPA cases / yr", "filed > 150 days", "challenger wins", "injunction", "vacatur of remands",
               "suits kept under BAAJA (central)"], side),
        "## Litigation BAAJA does not reach: Sabin Center contested renewable projects (2026 database)",
        table(["type", "contested", "litigated", "federal venue", "state / administrative only", "cancelled"], sab),
        "## Sensitivity (court provisions; other values central)", sweep_table(sw, SWEEP),
    ])
    plots.grouped_bars(CHALLENGERS, {g + ", law": [b[f"suits: {ch} | {g}"] for ch in CHALLENGERS] for g in ("Renewable (new)", "Fossil (gas)")}
                       | {g + ", BAAJA courts": [c[f"suits: {ch} | {g}"] for ch in CHALLENGERS] for g in ("Renewable (new)", "Fossil (gas)")},
                       os.path.join(fig_dir, "sim2_who_sues.png"), "Sim 2: suits 2026-41 by lead challenger", "suits",
                       colors=["#9ddcc4", "#f5b79c", "#1baf7a", "#eb6834"], fmt="{:.0f}")
    data = dict(regime_2025=reg_res, scenarios=res, sweep=sw, sabin=s)
    save("sim2_litigation", data, md, res_dir)
    return md, data
