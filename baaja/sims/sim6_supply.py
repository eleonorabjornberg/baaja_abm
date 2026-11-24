"""Simulation 6: electricity supply and resource adequacy by region (Phase 1).

Question: does BAAJA change whether each region has enough firm capacity to meet peak demand, 2027-2041?
Supply = existing fleet (EIA-860, end-2025) - retirements + queue additions from the model, by LBNL region.
Firm capacity and reserve margins follow NERC's 2025 Long-Term Reliability Assessment convention; demand and the
reference margin level (RML) are NERC's (2026-35, extended to 2041). See baaja/supply.py.
Every scenario is paired with current law (same seeds and political draws). Intervals: 5th-95th percentile across
runs (seed noise only; joint parameter uncertainty is Phase 3).
"""
import os

import numpy as np

from .. import experiments as ex
from .. import supply as sp
from ..params import BAAJA, IXB, REGIONS
from . import save, table

YRS = sp.YEARS
SHOW = (2030, 2035, 2041)
CEIL = round(IXB["ercot_gap_cut"], 2)


def _scen():
    return {"Current law": {}, "BAAJA (data-sized provisions)": BAAJA,
            "BAAJA + Sec.2106 10% cut": dict(BAAJA, ix_cut_rto=0.10),
            f"BAAJA + Sec.2106 ceiling ({100 * CEIL:.0f}% cut)": dict(BAAJA, ix_cut_rto=CEIL)}


def _supplies(runs, sa):
    fleet, dem = sp.existing_fleet(sa), sp.demand(sa)
    return [sp.supply(r, sa, fleet, dem) for r in runs]


def _band(x):
    x = np.asarray(x, float)
    return dict(mean=float(np.mean(x)), p5=float(np.percentile(x, 5)), p95=float(np.percentile(x, 95)))


def _f(b, d=1, sign=False, scale=1.0):
    s = "+" if sign else ""
    return f"{b['mean'] * scale:{s}.{d}f} [{b['p5'] * scale:{s}.{d}f}, {b['p95'] * scale:{s}.{d}f}]"


def national(sups):
    """National totals per run: dict of arrays [run, year]."""
    out = {k: np.array([s[k].sum(axis=0) for s in sups]) for k in ("installed", "firm", "nid", "shortfall", "twh")}
    out["reserve_margin"] = out["firm"] / out["nid"] - 1
    out["regions_below_rml"] = np.array([(s["reserve_margin"] < s["rml"]).sum(axis=0) for s in sups])
    for c in sp.CLASS:
        out[f"installed|{c}"] = np.array([s[f"installed|{c}"].sum(axis=0) for s in sups])
    return out


def summarize_scenarios(raw, sa):
    sups = {k: _supplies(r, sa) for k, r in raw.items()}
    nat = {k: national(v) for k, v in sups.items()}
    return sups, nat


def run(n_runs, cal, res_dir, fig_dir, regime=None):
    scen = _scen()
    over = (lambda o: dict(o, regime=regime)) if regime else (lambda o: o)
    raw = {k: ex.run_scenario(over(o), n_runs, cal) for k, o in scen.items()}
    sa = sp.SA
    sups, nat = summarize_scenarios(raw, sa)
    law, lawn = sups["Current law"], nat["Current law"]
    yi = {y: YRS.index(y) for y in SHOW}

    # ---- national, current law ----
    rows = []
    for y in (2027,) + SHOW:
        k = YRS.index(y)
        rows.append([y, f"{lawn['nid'][:, k].mean() / 1000:.0f}", f"{lawn['installed'][:, k].mean() / 1000:.0f}",
                     f"{lawn['installed|Renewable'][:, k].mean() / 1000:.0f} / {lawn['installed|Gas'][:, k].mean() / 1000:.0f} / "
                     f"{lawn['installed|Storage'][:, k].mean() / 1000:.0f} / {lawn['installed|Coal and oil'][:, k].mean() / 1000:.0f}",
                     f"{lawn['firm'][:, k].mean() / 1000:.0f}", _f(_band(lawn["reserve_margin"][:, k]), 1, scale=100),
                     f"{lawn['regions_below_rml'][:, k].mean():.1f}", _f(_band(lawn["shortfall"][:, k]), 1, scale=1e-3),
                     f"{lawn['twh'][:, k].mean():.0f}"])
    t_nat = table(["peak year", "peak demand GW (NERC)", "installed GW", "renewable / gas / storage / coal+oil GW",
                   "firm GW", "reserve margin %", "regions below RML (of 9)", "shortfall GW", "generation TWh"], rows)

    # ---- regional, current law ----
    rows = []
    for i, r in enumerate(REGIONS):
        rm = np.array([s["reserve_margin"][i] for s in law]); rml = law[0]["rml"][i]
        below = rm < rml[None]
        first = [YRS[int(np.argmax(b))] if b.any() else None for b in below]
        fy = [f for f in first if f]
        rows.append([r, f"{100 * rml[yi[2035]]:.1f}"] + [_f(_band(rm[:, yi[y]]), 1, scale=100) for y in SHOW]
                    + [f"{100 * below[:, yi[2035]].mean():.0f}%", (f"{int(np.median(fy))}" if len(fy) > len(first) / 2 else "-"),
                       _f(_band([s["shortfall"][i, yi[2035]] for s in law]), 1, scale=1e-3)])
    t_reg = table(["region", "RML 2035 %"] + [f"reserve margin {y} %" for y in SHOW]
                  + ["runs below RML in 2035", "median first year below RML", "shortfall 2035 GW"], rows)

    # ---- BAAJA effect ----
    eff = {}
    rows_nat, rows_reg = [], []
    for k in list(scen)[1:]:
        z = sups[k]; zn = nat[k]
        d = {m: zn[m] - lawn[m] for m in ("installed", "firm", "shortfall", "regions_below_rml", "reserve_margin", "twh")}
        eff[k] = {m: {y: _band(d[m][:, yi[y]]) for y in SHOW} for m in d}
        rows_nat.append([k] + [_f(eff[k]["firm"][y], 1, True, 1e-3) for y in SHOW]
                        + [_f(eff[k]["shortfall"][y], 1, True, 1e-3) for y in (2035, 2041)]
                        + [f"{eff[k]['regions_below_rml'][2035]['mean']:+.2f}", f"{eff[k]['twh'][2041]['mean']:+.0f}"])
        for i, r in enumerate(REGIONS):
            dfirm = [z[j]["firm"][i] - law[j]["firm"][i] for j in range(len(z))]
            dsh = [z[j]["shortfall"][i] - law[j]["shortfall"][i] for j in range(len(z))]
            drm = [z[j]["reserve_margin"][i] - law[j]["reserve_margin"][i] for j in range(len(z))]
            eff[k][r] = dict(firm={y: _band([x[yi[y]] for x in dfirm]) for y in SHOW},
                             shortfall={y: _band([x[yi[y]] for x in dsh]) for y in SHOW},
                             rm={y: _band([x[yi[y]] for x in drm]) for y in SHOW})
    t_eff_nat = table(["scenario"] + [f"firm GW {y}" for y in SHOW] + ["shortfall GW 2035", "shortfall GW 2041",
                      "regions below RML 2035", "TWh 2041"], rows_nat)
    keys = list(scen)[1:]
    for i, r in enumerate(REGIONS):
        rows_reg.append([r] + [f"{eff[k][r]['firm'][2035]['mean'] / 1000:+.1f} / {100 * eff[k][r]['rm'][2035]['mean']:+.1f} / "
                               f"{eff[k][r]['shortfall'][2035]['mean'] / 1000:+.1f}" for k in keys])
    t_eff_reg = table(["region"] + [f"{k}: firm GW / margin pts / shortfall GW (2035)" for k in keys], rows_reg)

    # ---- supply-assumption sensitivity (same runs, post-processing) ----
    srows = []
    base_k = "BAAJA + Sec.2106 10% cut"
    for key, (lo, c, hi, note) in sp.SUPPLY_ASSUMPTIONS.items():
        cells = []
        for v in (lo, hi):
            sa2 = dict(sa, **{key: v})
            L = national(_supplies(raw["Current law"], sa2)); Z1 = national(_supplies(raw["BAAJA (data-sized provisions)"], sa2))
            Z2 = national(_supplies(raw[base_k], sa2))
            cells.append((L["shortfall"][:, yi[2035]].mean() / 1000, L["regions_below_rml"][:, yi[2035]].mean(),
                          (Z1["shortfall"] - L["shortfall"])[:, yi[2035]].mean() / 1000,
                          (Z2["shortfall"] - L["shortfall"])[:, yi[2035]].mean() / 1000))
        srows.append([key, f"{lo} / {hi}", f"{cells[0][0]:.0f} / {cells[1][0]:.0f}", f"{cells[0][1]:.1f} / {cells[1][1]:.1f}",
                      f"{cells[0][2]:+.1f} / {cells[1][2]:+.1f}", f"{cells[0][3]:+.1f} / {cells[1][3]:+.1f}", note])
    t_sens = table(["assumption", "low / high", "law: shortfall 2035 GW", "law: regions below RML 2035",
                    "data-sized BAAJA: shortfall change GW", "+ 10% Sec.2106: shortfall change GW", "what it is"], srows)

    # ---- checks against NERC ----
    chk = sp.check_2026(sa)
    crow = []
    for i, r in enumerate(REGIONS):
        dn = sp.DEMAND["regions"][r]
        rm = np.array([s["reserve_margin"][i] for s in law])
        crow.append([r, f"{chk[r]['model_unscaled'] / 1000:.1f}", f"{chk[r]['nerc'] / 1000:.1f}", f"{chk[r]['scale']:.2f}",
                     f"{100 * dn['anticipated_reserve_margin'][4]:.1f} / {100 * rm[:, YRS.index(2030)].mean():.1f}",
                     f"{100 * dn['anticipated_reserve_margin'][9]:.1f} / {100 * rm[:, YRS.index(2035)].mean():.1f}"])
    t_chk = table(["region", "fleet firm GW 2026 (unscaled)", "NERC existing-certain + transfers GW", "scale applied",
                   "reserve margin 2030: NERC anticipated / model", "2035: NERC / model"], crow)

    title = "# Simulation 6: electricity supply and resource adequacy" + (f" (regime \"{regime}\")" if regime else "")
    md = "\n\n".join([
        title,
        "Supply = existing fleet (EIA-860, end-2025) minus retirements plus what the model's queue brings online, by "
        "LBNL region. On-peak accredited capacity (\"firm\" below), peak demand and the reference margin level (RML, the reserve margin a region "
        "plans to) follow NERC's 2025 Long-Term Reliability Assessment. Wind, solar and batteries count at an on-peak "
        "share that falls over time (central: halfway between NERC's 2025 national values and PJM's 2041/42 ratings), "
        "except in PJM, whose reference margin is an installed-capacity margin that already rises as accreditation falls. "
        "This simpler model has no feedback from scarcity to building, so surpluses in some regions are not "
        "self-correcting and shortfalls are not filled by new entry; the grid-agent model (Sim 7) adds an entry response.",
        "## Current law: the United States",
        t_nat,
        "## Current law: by region (reserve margin, % of peak demand; 5th-95th percentile across runs)",
        t_reg,
        "## What BAAJA changes: the United States (difference from current law, paired)",
        t_eff_nat,
        "## What BAAJA changes: by region in 2035 (mean difference from current law)",
        t_eff_reg,
        "## Sensitivity to the supply assumptions (each at its low and high end, others central; 2035)",
        t_sens,
        "## Checks against NERC",
        "Existing fleet firm capacity in 2026 vs NERC's existing-certain resources; the ratio is applied to the existing "
        "fleet so that reserve margins are on NERC's basis. NERC's anticipated reserve margin counts only Tier 1 "
        "additions (signed contracts, under construction), so it falls faster than the model's after 2028.",
        t_chk,
    ])
    data = dict(years=YRS, regions=REGIONS, effects=eff,
                law_reserve_margin={r: [_band([s["reserve_margin"][i, k] for s in law]) for k in range(len(YRS))] for i, r in enumerate(REGIONS)},
                law_rml={r: law[0]["rml"][i].tolist() for i, r in enumerate(REGIONS)},
                national_law={m: [_band(lawn[m][:, k]) for k in range(len(YRS))] for m in ("installed", "firm", "nid", "reserve_margin", "shortfall", "twh", "regions_below_rml")},
                check=chk, firm_scale=dict(zip(REGIONS, sp.FIRM_SCALE.tolist())))
    name = "sim6_supply" + (f"_{regime}" if regime else "")
    if fig_dir and not regime:
        _plot(sups, scen, os.path.join(fig_dir, "sim6_reserve_margins.png"))
    save(name, data, md, res_dir)
    return md, data


def _plot(sups, scen, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    keys = list(scen)
    col = {keys[0]: "#555555", keys[1]: "#2a78d6", keys[2]: "#eb6834"}
    fig, axs = plt.subplots(3, 3, figsize=(11, 9), sharex=True)
    for i, r in enumerate(REGIONS):
        ax = axs[i // 3, i % 3]
        for k in keys[:3]:
            rm = 100 * np.array([s["reserve_margin"][i] for s in sups[k]])
            ax.plot(YRS, rm.mean(axis=0), color=col[k], lw=1.6, label=k)
            if k == keys[0]:
                ax.fill_between(YRS, np.percentile(rm, 5, axis=0), np.percentile(rm, 95, axis=0), color=col[k], alpha=0.15, lw=0)
        ax.plot(YRS, 100 * sups[keys[0]][0]["rml"][i], color="#c0392b", ls="--", lw=1, label="NERC reference margin")
        ax.set_title(r, fontsize=10); ax.grid(alpha=0.3)
        if i % 3 == 0:
            ax.set_ylabel("reserve margin, %")
    axs[0, 0].legend(fontsize=7, loc="upper left")
    fig.suptitle("Sim 6: reserve margin by region, current law vs BAAJA", fontsize=12)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
