"""Phase 3 validation: backcast Jan 2010 - Dec 2025 under current law, with the exogenous grid (Sims 1-6) and with the
grid agents (Sim 7), against EIA-860 additions nationally and by region, plus the withdrawal timing of the same
request cohorts (2015-19) against LBNL. Requests by year come from LBNL, and in this backcast each request's region
is drawn from LBNL's requests by region in its request year [D] (forward runs use 2021-25 shares)."""
import json
import os

import numpy as np

from . import experiments as ex
from . import grid as gr
from .model import online_by_region_year, simulate, summarize
from .params import BACKCAST, ENGINE, REGIONS, _load
from .sims import table

TECH = {"Solar": ["Solar"], "Onshore wind": ["Onshore wind"], "Gas": ["Gas CC", "Gas CT", "Gas ST"], "Storage": ["Storage"]}
YEARS = range(2018, 2026)
MODES = ("exogenous", "agents")


def _arrivals():
    arr = {t: {int(y): n for y, n in d.items()} for t, d in ENGINE["lbnl"]["arrivals_by_year"].items()}
    hyb = {int(y): n for y, n in ENGINE["lbnl"]["hybrid_storage"]["arrivals_by_year"].items()}
    arr["Storage"] = {y: arr["Storage"].get(y, 0) + hyb.get(y, 0) for y in set(arr["Storage"]) | set(hyb)}
    return arr


def withdrawal_by_region(rows, window, months=gr.WD_MONTHS):
    """Share of requests made in `window` (backcast months) withdrawn within m months, by region; both grid modes."""
    G = [r for r in rows if (r["region"] >= 0).all() and r["mw"] > 0]
    cat = lambda f: np.concatenate([f(r) for r in G])
    t0, reg, W = cat(lambda r: r["t0"]), cat(lambda r: r["region"]), cat(lambda r: r["W"])
    gwd = cat(lambda r: r["gwd"] if "gwd" in r else np.full(len(r["t0"]), np.inf))
    wdn = cat(lambda r: ~r["done"] & ~r["killed"])
    tw = np.where(wdn, np.minimum(W, gwd - t0), np.inf)
    sel = (t0 >= window[0]) & (t0 < window[1])
    return {r: {m: float((tw[sel & (reg == k)] <= m).mean()) for m in months}
            for k, r in enumerate(REGIONS) if (sel & (reg == k)).sum() >= 30}


def backcast_params(cal, grid):
    return ex.params(dict(T=BACKCAST["T"], turnovers=BACKCAST["turnovers"], arrivals=_arrivals(),
                          start_year=BACKCAST["start_year"], seed_queue=False, region_by_year=True, grid=grid), cal)


def backcast(cal, grid, n_runs=10):
    p = backcast_params(cal, grid)
    y0 = BACKCAST["start_year"]
    coh = ((gr.WD_COHORTS[0] - y0) * 12, (gr.WD_COHORTS[1] + 1 - y0) * 12)
    nat, reg, wd = [], [], []
    for s in range(n_runs):
        rows = simulate(p, s, BACKCAST["politics"])
        nat.append(summarize(rows, p)["_online_by_year"])
        reg.append(online_by_region_year(rows))
        wd.append(withdrawal_by_region(rows, coh))
    yrs = [y0 + i for i in range(int(np.ceil(BACKCAST["T"] / 12)))]
    k = [yrs.index(y) for y in YEARS]
    out = dict(national={t: dict(zip(yrs, np.mean([r[t] for r in nat], axis=0).tolist())) for t in TECH},
               region={t: {REGIONS[i]: float(np.mean([np.array(r[t][i])[k].sum() for r in reg])) for i in range(len(REGIONS))}
                       for t in TECH},
               withdrawal={rg: {m: float(np.nanmean([w.get(rg, {}).get(m, np.nan) for w in wd])) for m in gr.WD_MONTHS}
                           for rg in REGIONS})
    return out


def eia():
    nat = _load("eia860_additions.json")
    add = _load("fleet_targets.json")["additions_by_year"]
    region = {t: {r: sum(add.get(r, {}).get(g, {}).get(str(y), 0.0) for g in gs for y in YEARS) / 1000 for r in REGIONS}
              for t, gs in TECH.items()}
    return dict(national={t: {y: nat[t][str(y)] / 1000 for y in YEARS} for t in TECH}, region=region)


def report(cal, res_dir, n_runs=10):
    B = {m: backcast(cal, m, n_runs) for m in MODES}
    E = eia()
    # national
    rows = []
    for t in TECH:
        x = sum(E["national"][t].values())
        cells = [t, f"{x:.1f}"]
        for m in MODES:
            v = sum(B[m]["national"][t][y] for y in YEARS)
            cells += [f"{v:.1f} ({v / x:.2f})"]
        cells.append(" ".join(f"{B['exogenous']['national'][t][y]:.0f}/{B['agents']['national'][t][y]:.0f}/"
                              f"{E['national'][t][y]:.0f}" for y in YEARS))
        rows.append(cells)
    t_nat = table(["technology", "EIA-860 GW 2018-25", "exogenous grid: model GW (ratio)", "grid agents: model GW (ratio)",
                   "by year 2018..2025 (exogenous / agents / EIA)"], rows)
    # regional
    rows, err = [], {m: [] for m in MODES}
    for r in REGIONS:
        cells = [r]
        for t in TECH:
            x = E["region"][t][r]
            cells.append(" / ".join(f"{B[m]['region'][t][r]:.1f}" for m in MODES) + f" / {x:.1f}")
        tot_e = sum(E["region"][t][r] for t in TECH)
        for m in MODES:
            tot_m = sum(B[m]["region"][t][r] for t in TECH)
            cells.append(f"{tot_m / tot_e:.2f}" if tot_e > 0 else "-")
            err[m].append(abs(np.log(max(tot_m, 1e-3) / tot_e)) * tot_e)
        rows.append(cells)
    wtot = sum(sum(E["region"][t][r] for t in TECH) for r in REGIONS)
    rerr = {m: float(np.sum(err[m]) / wtot) for m in MODES}
    t_reg = table(["region"] + [f"{t} GW (exogenous / agents / EIA)" for t in TECH] +
                  ["all four, exogenous / EIA", "all four, agents / EIA"], rows)
    # regional shares of national additions (the level is checked above)
    rows = []
    for t in TECH:
        sh = {s: {r: v[r] / max(sum(v.values()), 1e-9) for r in REGIONS}
              for s, v in (("e", E["region"][t]), ("x", B["exogenous"]["region"][t]), ("a", B["agents"]["region"][t]))}
        rows.append([t] + [f"{100 * sh['x'][r]:.0f} / {100 * sh['a'][r]:.0f} / {100 * sh['e'][r]:.0f}" for r in REGIONS])
    t_sh = table(["technology"] + REGIONS, rows)
    # withdrawal timing, same cohorts
    wdd = gr.withdrawal_curve_data()
    rows = []
    for r in REGIONS:
        if r not in wdd:
            continue
        rows.append([r] + [" / ".join(f"{B[m]['withdrawal'][r][mo]:.2f}" for m in MODES) + f" / {wdd[r][mo]:.2f}"
                           for mo in gr.WD_MONTHS])
    t_wd = table(["region"] + [f"withdrawn by {mo} months (exogenous / agents / LBNL)" for mo in gr.WD_MONTHS], rows)
    md = "\n\n".join([
        "# Backcast 2010-2025, current law, vs EIA-860 additions and LBNL withdrawal timing",
        __doc__.replace("\n", " "),
        f"Means over {n_runs} runs per grid model. The exogenous grid's study times and both models' hazards were fitted "
        "to LBNL completion and timing; nothing here is fitted to EIA-860 additions except the first forward year, which "
        "this backcast does not use.",
        "## National additions 2018-25",
        t_nat,
        "## By region, 2018-25",
        f"Weighted mean absolute log ratio of model to EIA additions across regions (all four technologies): exogenous "
        f"{rerr['exogenous']:.2f}, agents {rerr['agents']:.2f}.",
        t_reg,
        "### Each region's share of national additions, 2018-25 (%, exogenous / agents / EIA)",
        t_sh,
        "## Withdrawal timing of 2015-19 requests (same cohorts in model and data)",
        "LBNL counts requests still active at end-2025 as not withdrawn; so does the model. ERCOT's early queue data "
        "hold few withdrawn requests (under 25 solar requests a year before 2016), so its LBNL withdrawal shares are "
        "probably too low.",
        t_wd,
    ])
    open(os.path.join(res_dir, "backcast.md"), "w").write(md + "\n")
    json.dump(dict(model=B, eia=E, lbnl_withdrawal=wdd, regional_error=rerr), open(os.path.join(res_dir, "backcast.json"), "w"),
              indent=1, default=float)
    return md, B
