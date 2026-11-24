"""Figures for the brief (docs/brief.md), drawn from the committed results/*.json: python run.py --brief-figures."""
import json
import os

import numpy as np

from .plots import INK, INK2, GRID, plt

C_EXO, C_AGT, C_ALL, C_EIA = "#8a8984", "#2a78d6", "#1baf7a", "#eb6834"


def _j(res_dir, name):
    return json.load(open(os.path.join(res_dir, name)))


def headline(res_dir, path):
    """BAAJA minus current law by 2041 (new capacity, relicensed hydro excluded), by model and scenario."""
    s7, un = _j(res_dir, "sim7_grid_agents.json"), _j(res_dir, "uncertainty.json")
    G = "GW_new"
    exo = s7["exogenous"]["BAAJA (exogenous grid)"]["diff_vs_baseline"][G]
    U = {k: v["bands"]["GW new"] for k, v in un.items()}
    r = s7["results"]
    d = lambda k: r[k]["diff_vs_baseline"][G]
    rows = [
        ("Simpler model, data-sized provisions", exo, C_EXO, "runs"),
        ("   same, all assumption ranges drawn", U["grid dials at 0 (data-sized provisions)"], C_EXO, "joint"),
        ("Grid agents: no RTO adopts Sec.2106", d("BAAJA without Sec.2106"), C_AGT, "runs"),
        ("Grid agents: each RTO adopts with p = 0.5", d("BAAJA"), C_AGT, "runs"),
        ("Grid agents: every RTO adopts Sec.2106", d("BAAJA, Sec.2106 adopted by every RTO"), C_ALL, "runs"),
        ("Grid agents, all assumption ranges drawn", U["grid agents (Phase 2), their assumptions drawn"], C_AGT, "joint"),
        ("Simpler model, study-time cut 0 to ERCOT pace", U["grid dials across their ranges"], "#c9c8c3", "joint"),
    ]
    lo = min(b["p5"] for _, b, _, _ in rows); hi = max(b["p95"] for _, b, _, _ in rows)
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    for i, (lab, b, c, kind) in enumerate(rows[::-1]):
        mid = b.get("p50", b["mean"])
        ax.plot([b["p5"], b["p95"]], [i, i], color=c, lw=6 if kind == "joint" else 3, solid_capstyle="butt", alpha=.9)
        ax.plot(mid, i, "o", color=INK, ms=5)
        ax.text(b["p95"] + (hi - lo) * .01, i, f"{mid:+.0f} [{b['p5']:+.0f}, {b['p95']:+.0f}]", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(rows)), [x[0] for x in rows[::-1]], fontsize=8)
    ax.axvline(0, color=INK2, lw=.8)
    ax.set_xlim(min(lo, 0) - (hi - lo) * .03, hi + (hi - lo) * .22); ax.grid(axis="y", visible=False)
    ax.set_xlabel("new GW online by Nov 2041, BAAJA minus current law\nthin bars: 5th-95th percentile across 100 paired "
                  "runs, dot = mean; thick bars: 400 joint samples\nof all assumption ranges, dot = median",
                  fontsize=8)
    law = r["Current law"]["totals"][G]["mean"]
    ax.set_title(f"BAAJA by 2041: {d('BAAJA without Sec.2106')['mean']:+.0f} GW if no RTO adopts Sec.2106, "
                 f"{d('BAAJA, Sec.2106 adopted by every RTO')['mean']:+.0f} GW if all do (current law: ~{law:,.0f} GW new)",
                 loc="left", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def regions(res_dir, path):
    s7 = _j(res_dir, "sim7_grid_agents.json")["regions"]
    law = s7["Current law"]; regs = list(law)
    sc = {"no RTO adopts Sec.2106": ("BAAJA without Sec.2106", C_EXO),
          "each RTO adopts with p = 0.5": ("BAAJA", C_AGT),
          "every RTO adopts Sec.2106": ("BAAJA, Sec.2106 adopted by every RTO", C_ALL)}
    fig, ax = plt.subplots(figsize=(8.6, 3.4)); w = .27
    for j, (lab, (k, c)) in enumerate(sc.items()):
        v = [s7[k][r]["GW_online"] - law[r]["GW_online"] for r in regs]
        x = np.arange(len(regs)) + (j - 1) * w
        ax.bar(x, v, w * .95, color=c, label=lab)
        for xi, vi in zip(x, v):
            ax.text(xi, vi + (.3 if vi >= 0 else -1.2), f"{vi:.0f}", ha="center", fontsize=6.5, color=INK2)
    ax.set_xticks(range(len(regs)), regs, fontsize=8); ax.grid(axis="x", visible=False); ax.axhline(0, color=INK2, lw=.8)
    ax.set_ylabel("new GW by 2041 vs current law")
    ax.set_title("Grid agents, by region (Sec.2106 applies only in RTO/ISO markets, not ERCOT, the Southeast or the West)",
                 loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=8); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def shortfall(res_dir, path):
    s7 = _j(res_dir, "sim7_grid_agents.json")
    ag = s7["adequacy_current_law"]["grid agents (this simulation)"]["national"]
    ex_ = s7["adequacy_current_law"]["exogenous study times (Sims 1-6)"]["national"]
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    for off, a, c, lab in ((-.15, ex_, C_EXO, "current law, simpler model"), (0, ag, INK2, "current law, grid agents")):
        ys = sorted(int(y) for y in a)
        ax.errorbar([y + off for y in ys], [a[str(y)]["mean"] for y in ys],
                    yerr=[[a[str(y)]["mean"] - a[str(y)]["p5"] for y in ys], [a[str(y)]["p95"] - a[str(y)]["mean"] for y in ys]],
                    fmt="o", color=c, ms=5, capsize=3, label=lab)
    sup = s7["supply"]
    for key, c, lab in (("BAAJA", C_AGT, "BAAJA (p = 0.5)"), ("BAAJA, Sec.2106 adopted by every RTO", C_ALL, "BAAJA, every RTO")):
        pts = [(2035, sup[key]["shortfall_2035"]), (2041, sup[key]["shortfall_2041"])]
        ax.plot([y + .15 for y, _ in pts], [ag[str(y)]["mean"] + b["mean"] for y, b in pts], "s", color=c, ms=5,
                label=f"{lab}: {pts[0][1]['mean']:+.1f} GW in 2035, {pts[1][1]['mean']:+.1f} in 2041")
    ax.set_xticks([2027, 2035, 2041]); ax.set_ylabel("GW below NERC reference margin levels"); ax.set_ylim(bottom=0)
    ax.set_title("Shortfall below NERC reference margin levels (a benchmark, mostly PJM's rising margin); bars: 5th-95th "
                 "percentile across runs", loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def drivers(res_dir, path):
    un = _j(res_dir, "uncertainty.json")
    panels = [("grid dials at 0 (data-sized provisions)", "Simpler model, data-sized provisions"),
              ("grid agents (Phase 2), their assumptions drawn", "Grid agents")]
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.2))
    for ax, (k, t) in zip(axes, panels):
        v = un[k]["variance"]["GW new"]
        top = v["top"][:6][::-1]
        x = [100 * e[1] for e in top]
        err = [[100 * (e[1] - e[2][0]) for e in top], [100 * (e[2][1] - e[1]) for e in top]]
        err = [[max(a, 0) for a in err[0]], [max(a, 0) for a in err[1]]]
        ax.barh(range(len(top)), x, xerr=err, color=C_AGT if "agents" in k else C_EXO, ecolor=INK2, capsize=2)
        ax.set_yticks(range(len(top)), [e[0].replace(" (share of RTO capacity)", "") for e in top], fontsize=7.5)
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("% of variance in new GW (rank regression; bars: bootstrap 90%)", fontsize=7.5)
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
    ax.set_title("Backcast 2010-25 under current law (EIA-860 additions not used in fitting), national",
                 loc="left", fontsize=9)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def run(res_dir="results", fig_dir="figures"):
    out = []
    for f, name in ((headline, "brief_1_headline.png"), (regions, "brief_2_regions.png"), (shortfall, "brief_3_shortfall.png"),
                    (drivers, "brief_4_drivers.png"), (backcast, "brief_5_backcast.png")):
        p = os.path.join(fig_dir, name); f(res_dir, p); out.append(p)
    return out
