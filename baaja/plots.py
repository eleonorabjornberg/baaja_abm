"""Static PNG charts (matplotlib). Palette: reference categorical slots, assigned per entity, never cycled."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
COLOR = {"Renewable (new)": "#1baf7a", "Fossil (gas)": "#eb6834", "Storage": "#2a78d6",
         "Renewable (retained hydro)": "#6250d6", "Baseline": "#8a8984", "BAAJA": "#2a78d6"}
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": .8, "axes.axisbelow": True,
                     "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})


def _err(b):
    return [[b["mean"] - b["p5"]], [b["p95"] - b["mean"]]]


def scenarios_gw(res, path):
    names = list(res); fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, n in enumerate(names):
        b = res[n]["totals"]["GW_total"]
        ax.barh(i, b["mean"], xerr=_err(b), color=COLOR["Baseline" if i == 0 else "BAAJA"], height=.55,
                error_kw=dict(ecolor=INK2, lw=1.2, capsize=3))
        ax.text(b["p95"] + 5, i, f"{b['mean']:.0f} GW", va="center", color=INK2)
    ax.set_yticks(range(len(names)), names); ax.invert_yaxis(); ax.grid(axis="y", visible=False)
    ax.set_xlabel("GW online by Nov 2041 (bars: mean, whiskers: 90% interval across runs)")
    ax.set_title("Capacity online by 2041, by scenario", loc="left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def renew_vs_fossil(res, path, scen=("Baseline (current law)", "BAAJA (all levers)"), unit="GW"):
    groups = ["Renewable (new)", "Fossil (gas)", "Storage"] + (["Renewable (retained hydro)"] if unit == "GW" else [])
    if unit == "TWh":
        groups = [g for g in groups if g != "Storage"]
    fig, ax = plt.subplots(figsize=(8, 3.8)); w = .38
    for j, s in enumerate(scen):
        for i, g in enumerate(groups):
            b = res[s]["totals"][f"{unit} {g}"]
            ax.bar(i + (j - .5) * w * 1.05, b["mean"], w, yerr=_err(b), color=COLOR[g], alpha=1 if j else .45,
                   error_kw=dict(ecolor=INK2, lw=1, capsize=2))
            ax.text(i + (j - .5) * w * 1.05, b["p95"] * 1.02, f"{b['mean']:.0f}", ha="center", va="bottom", fontsize=8, color=INK2)
    ax.set_xticks(range(len(groups)), groups); ax.grid(axis="x", visible=False)
    ax.set_ylabel(f"{unit}{'/yr' if unit == 'TWh' else ''} from projects online by 2041")
    ax.set_title(f"Renewable vs fossil, {unit}: pale = current law, solid = BAAJA", loc="left")
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def gain_by_type(res, path, scen="BAAJA (all levers)"):
    d = res[scen]["diff_by_type_GW"]; types = [t for t in d if t != "Transmission"]
    grp = {"Solar": "Renewable (new)", "Onshore wind": "Renewable (new)", "Offshore wind": "Renewable (new)",
           "Geothermal": "Renewable (new)", "Gas": "Fossil (gas)", "Storage": "Storage", "Hydro relicense": "Renewable (retained hydro)"}
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for i, t in enumerate(types):
        b = d[t]; ax.barh(i, b["mean"], xerr=_err(b), color=COLOR[grp[t]], height=.55, error_kw=dict(ecolor=INK2, lw=1, capsize=2))
        ax.text(max(b["p95"], 0) + .5, i, f"+{b['mean']:.1f}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(types)), types); ax.invert_yaxis(); ax.grid(axis="y", visible=False)
    ax.set_xlabel("GW added by BAAJA vs current law (paired runs, 90% interval)")
    ax.set_title("Where the BAAJA gain lands, by technology", loc="left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def politics(pol, path):
    names = list(pol); fig, ax = plt.subplots(figsize=(8, 3.4)); w = .38
    for i, n in enumerate(names):
        for j, g in enumerate(["Renewable (new)", "Fossil (gas)"]):
            b = pol[n][f"GW {g}"]
            ax.bar(i + (j - .5) * w * 1.05, b["mean"], w, yerr=_err(b), color=COLOR[g], error_kw=dict(ecolor=INK2, lw=1, capsize=2))
            ax.text(i + (j - .5) * w * 1.05, b["p95"] + .3, f"+{b['mean']:.1f}", ha="center", va="bottom", fontsize=8, color=INK2)
    ax.set_xticks(range(len(names)), names); ax.grid(axis="x", visible=False)
    ax.set_ylabel("GW gained from BAAJA vs current law")
    ax.set_title("BAAJA gain by political path (green = renewable, orange = gas)", loc="left")
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def sweep_ix(sw, divA, path):
    x = [round(100 * (1 - s["value"])) for s in sw]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for key, g in [("GW Renewable (new)", "Renewable (new)"), ("GW Fossil (gas)", "Fossil (gas)"), ("GW Storage", "Storage")]:
        m = [s["diff"][key]["mean"] for s in sw]
        ax.fill_between(x, [s["diff"][key]["p5"] for s in sw], [s["diff"][key]["p95"] for s in sw], color=COLOR[g], alpha=.15, lw=0)
        ax.plot(x, m, color=COLOR[g], lw=2, marker="o", ms=4, label=g)
        ax.axhline(divA["diff_vs_baseline"][key]["mean"], color=COLOR[g], lw=1, ls=":")
    ax.set_xlabel("Assumed Sec.2110 interconnection speedup (%)"); ax.set_ylabel("GW gained vs current law")
    ax.set_title("Sensitivity to the Sec.2110 assumption (dotted: Division A alone)", loc="left")
    ax.legend(frameon=False, loc="upper left"); fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def who_sues(res, challengers, path):
    """Small multiples: lawsuits by lead challenger, current law (pale) vs BAAJA (solid), renewable vs gas."""
    b, z = res["Baseline (current law)"]["totals"], res["BAAJA (all levers)"]["totals"]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), sharey=False); w = .38
    for ax, g in zip(axes, ["Renewable (new)", "Fossil (gas)"]):
        for i, c in enumerate(challengers):
            for j, (src, a) in enumerate([(b, .45), (z, 1)]):
                v = src[f"suits: {c} | {g}"]
                ax.bar(i + (j - .5) * w * 1.05, v["mean"], w, yerr=_err(v), color=COLOR[g], alpha=a,
                       error_kw=dict(ecolor=INK2, lw=1, capsize=2))
            sb, sz = b[f"suits: {c} | {g}"]["mean"], z[f"suits: {c} | {g}"]["mean"]
            top = max(b[f"suits: {c} | {g}"]["p95"], z[f"suits: {c} | {g}"]["p95"])
            ax.text(i, top * 1.04, f"{100*(sz/sb-1):+.0f}%", ha="center", va="bottom", fontsize=8, color=INK2)
        ax.margins(y=.12)
        ax.set_xticks(range(len(challengers)), [c.replace(" / ", "/\n") for c in challengers], fontsize=8)
        ax.grid(axis="x", visible=False); ax.set_title(g, loc="left")
    axes[0].set_ylabel("lawsuits, 2026-41")
    fig.suptitle("Who sues: pale = current law, solid = BAAJA (label: change)", x=.01, ha="left")
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
