"""Static charts (matplotlib). Categorical colours follow the entity (group or scenario), never the rank."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
GROUP_COLOR = {"Renewable (new)": "#1baf7a", "Fossil (gas)": "#eb6834", "Storage": "#2a78d6",
               "Renewable (retained hydro)": "#6250d6"}
SCEN_COLOR = ["#8a8984", "#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#e87ba4"]
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": .8, "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 10})


def _err(b):
    return [[max(b["mean"] - b["p5"], 0)], [max(b["p95"] - b["mean"], 0)]]


def grouped_bars(categories, series, path, title, ylabel, colors=None, fmt="{:.0f}"):
    """series: {label: [band per category]}; each band = dict(mean, p5, p95)."""
    k = len(series); w = .8 / k
    fig, ax = plt.subplots(figsize=(max(7, 1.3 * len(categories) + 2), 3.8))
    for j, (lab, bands) in enumerate(series.items()):
        c = (colors or SCEN_COLOR)[j % len(colors or SCEN_COLOR)]
        for i, b in enumerate(bands):
            x = i + (j - (k - 1) / 2) * w
            ax.bar(x, b["mean"], w * .95, yerr=_err(b), color=c, label=lab if i == 0 else None,
                   error_kw=dict(ecolor=INK2, lw=1, capsize=2))
            ax.text(x, max(b["p95"], b["mean"]) * 1.02 + 0.01, fmt.format(b["mean"]), ha="center", va="bottom", fontsize=7, color=INK2)
    ax.set_xticks(range(len(categories)), categories, fontsize=8); ax.grid(axis="x", visible=False)
    ax.set_ylabel(ylabel); ax.set_title(title, loc="left"); ax.legend(frameon=False, fontsize=8); ax.margins(y=.12)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def sweep(x, lines, path, title, xlabel, ylabel):
    """lines: {group label: [band per x]}"""
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for lab, bands in lines.items():
        c = GROUP_COLOR.get(lab, INK2)
        ax.fill_between(x, [b["p5"] for b in bands], [b["p95"] for b in bands], color=c, alpha=.15, lw=0)
        ax.plot(x, [b["mean"] for b in bands], color=c, lw=2, marker="o", ms=4, label=lab)
    ax.axhline(0, color=GRID, lw=1)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title, loc="left"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def tornado(items, central, path, title, xlabel):
    """items: [(label, value at low end, value at high end)]; sorted by swing."""
    items = sorted(items, key=lambda t: abs(t[2] - t[1]))
    fig, ax = plt.subplots(figsize=(8, 0.45 * len(items) + 1.4))
    for i, (lab, lo, hi) in enumerate(items):
        ax.barh(i, hi - central, left=central, color="#2a78d6", height=.55)
        ax.barh(i, lo - central, left=central, color="#8a8984", height=.55)
        ax.text(max(lo, hi, central) + 0.01 * (abs(central) + 1), i, f"{min(lo, hi):.1f} to {max(lo, hi):.1f}", va="center", fontsize=7, color=INK2)
    ax.axvline(central, color=INK, lw=1)
    ax.set_yticks(range(len(items)), [t[0] for t in items], fontsize=8); ax.grid(axis="y", visible=False)
    ax.set_xlabel(xlabel); ax.set_title(title + "  (grey: low end, blue: high end)", loc="left", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
