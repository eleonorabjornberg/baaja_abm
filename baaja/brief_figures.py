"""Figures for the brief (docs/brief.md), drawn from the committed results/*.json: python run.py --brief-figures."""
import json
import os

import numpy as np

from .plots import INK, INK2, GRID, plt

C_EXO, C_AGT, C_ALL, C_EIA = "#8a8984", "#2a78d6", "#1baf7a", "#eb6834"


def _j(res_dir, name):
    return json.load(open(os.path.join(res_dir, name)))


def headline(res_dir, path):
    """BAAJA minus current law by 2041 under each way of modelling grid access, with intervals."""
    s7, un = _j(res_dir, "sim7_grid_agents.json"), _j(res_dir, "uncertainty.json")
    exo = s7["exogenous"]["BAAJA (exogenous grid)"]["diff_vs_baseline"]["GW_total"]
    U = {k: v["bands"]["GW total"] for k, v in un.items()}
    r = s7["results"]
    rows = [
        ("Data-sized provisions, exogenous grid (central values)", exo, C_EXO, "runs"),
        ("   same, all assumption ranges", U["grid dials at 0 (data-sized provisions)"], C_EXO, "joint"),
        ("Grid agents: BAAJA (central values)", r["BAAJA"]["diff_vs_baseline"]["GW_total"], C_AGT, "runs"),
        ("   same, all assumption ranges", U["grid agents (Phase 2), their assumptions drawn"], C_AGT, "joint"),
        ("Grid agents: every RTO adopts Sec.2106", r["BAAJA, Sec.2106 adopted by every RTO"]["diff_vs_baseline"]["GW_total"], C_ALL, "runs"),
        ("Study-time dial 0 to ERCOT pace (all ranges)", U["grid dials across their ranges"], "#c9c8c3", "joint"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    for i, (lab, b, c, kind) in enumerate(rows[::-1]):
        mid = b.get("p50", b["mean"])
        ax.plot([b["p5"], b["p95"]], [i, i], color=c, lw=6 if kind == "joint" else 3, solid_capstyle="butt", alpha=.9)
        ax.plot(mid, i, "o", color=INK, ms=5)
        ax.text(b["p95"] + 2, i, f"{mid:+.0f} [{b['p5']:+.0f}, {b['p95']:+.0f}]", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows[::-1]], fontsize=8)
    ax.axvline(0, color=INK2, lw=.8)
    ax.set_xlim(-5, 235); ax.grid(axis="y", visible=False)
    ax.set_xlabel("GW online by Nov 2041, BAAJA minus current law (dot: central, bar: 5th-95th percentile)", fontsize=9)
    ax.set_title("BAAJA by 2041: +10 to +50 GW, depending on Sec.2106 (current law builds ~910 GW)", loc="left", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def regions(res_dir, path):
    s7 = _j(res_dir, "sim7_grid_agents.json")["regions"]
    law = s7["Current law"]; regs = list(law)
    sc = {"BAAJA (central: each RTO adopts with p = 0.5)": ("BAAJA", C_AGT),
          "BAAJA, every RTO adopts Sec.2106": ("BAAJA, Sec.2106 adopted by every RTO", C_ALL)}
    fig, ax = plt.subplots(figsize=(8.6, 3.4)); w = .38
    for j, (lab, (k, c)) in enumerate(sc.items()):
        v = [s7[k][r]["GW_online"] - law[r]["GW_online"] for r in regs]
        x = np.arange(len(regs)) + (j - .5) * w
        ax.bar(x, v, w * .95, color=c, label=lab)
        for xi, vi in zip(x, v):
            ax.text(xi, vi + .3, f"{vi:.0f}", ha="center", fontsize=7, color=INK2)
    ax.set_xticks(range(len(regs)), regs, fontsize=8); ax.grid(axis="x", visible=False)
    ax.set_ylabel("GW by 2041 vs current law")
    ax.set_title("Grid agents: the gain is in RTO markets, most of it in MISO and PJM (ERCOT, Southeast, West: permitting only)",
                 loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def shortfall(res_dir, path):
    s6, s7 = _j(res_dir, "sim6_supply.json"), _j(res_dir, "sim7_grid_agents.json")
    yrs = s6["years"]; sh = s6["national_law"]["shortfall"]
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    ax.fill_between(yrs, [b["p5"] / 1000 for b in sh], [b["p95"] / 1000 for b in sh], color=C_EXO, alpha=.2, lw=0)
    ax.plot(yrs, [b["mean"] / 1000 for b in sh], color=INK2, lw=2, label="current law, exogenous grid (Sim 6)")
    ag = s7["adequacy_current_law"]["grid agents (this simulation)"]["national"]
    ax.plot([int(y) for y in ag], [ag[y]["mean"] for y in ag], "o", color=C_AGT, ms=6, label="current law, grid agents (Sim 7)")
    sup = s7["supply"]["BAAJA"]["shortfall_2035"]
    base35 = ag["2035"]["mean"]
    ax.errorbar([2035.25], [base35 + sup["mean"]], yerr=[[sup["mean"] - sup["p5"] if sup["mean"] > sup["p5"] else 0],
                [sup["p95"] - sup["mean"] if sup["p95"] > sup["mean"] else 0]], fmt="s", color=C_ALL, ms=5,
                label=f"BAAJA, grid agents, 2035 ({sup['mean']:+.1f} GW)")
    ax.set_ylabel("GW below reference margins"); ax.set_ylim(bottom=0)
    ax.set_title("Current law falls short of NERC reference margins, mostly in PJM; BAAJA closes a few percent of the gap",
                 loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=8, loc="upper left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def drivers(res_dir, path):
    un = _j(res_dir, "uncertainty.json")
    panels = [("grid dials at 0 (data-sized provisions)", "Data-sized provisions"),
              ("grid agents (Phase 2), their assumptions drawn", "Grid agents")]
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.0))
    for ax, (k, t) in zip(axes, panels):
        v = un[k]["variance"]["GW total"]
        top = v["top"][:6][::-1]
        ax.barh(range(len(top)), [100 * x[1] for x in top], color=C_AGT if "agents" in k else C_EXO)
        ax.set_yticks(range(len(top)), [x[0] for x in top], fontsize=8); ax.grid(axis="y", visible=False)
        ax.set_xlabel("% of variance in GW (rank regression)", fontsize=8)
        ax.set_title(f"{t} (R² {v['r2']:.2f})", loc="left", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def backcast(res_dir, path):
    b = _j(res_dir, "backcast.json")
    tech = list(b["eia"]["national"])
    yrs = [str(y) for y in range(2018, 2026)]
    fig, ax = plt.subplots(figsize=(8.6, 3.0)); w = .38
    for j, (m, c, lab) in enumerate((("exogenous", C_EXO, "exogenous grid (Sims 1-6)"), ("agents", C_AGT, "grid agents (Sim 7)"))):
        v = [sum(b["model"][m]["national"][t][y] for y in yrs) / sum(b["eia"]["national"][t][y] for y in yrs) for t in tech]
        x = np.arange(len(tech)) + (j - .5) * w
        ax.bar(x, v, w * .95, color=c, label=lab)
        for xi, vi in zip(x, v):
            ax.text(xi, vi + .02, f"{vi:.2f}", ha="center", fontsize=7, color=INK2)
    ax.axhline(1, color=C_EIA, lw=1.2, label="EIA-860")
    ax.set_xticks(range(len(tech)), tech); ax.grid(axis="x", visible=False); ax.set_ylim(0, 1.3)
    ax.set_ylabel("model / EIA-860, 2018-25 additions")
    ax.set_title("Backcast 2010-25 under current law (not fitted to EIA): national fit, storage too low with agents",
                 loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def run(res_dir="results", fig_dir="figures"):
    out = []
    for f, name in ((headline, "brief_1_headline.png"), (regions, "brief_2_regions.png"), (shortfall, "brief_3_shortfall.png"),
                    (drivers, "brief_4_drivers.png"), (backcast, "brief_5_backcast.png")):
        p = os.path.join(fig_dir, name); f(res_dir, p); out.append(p)
    return out
