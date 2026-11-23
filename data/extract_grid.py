"""Inputs for the grid-access agents (Phase 2), from LBNL queue and interconnection-cost data (CC BY 4.0).

Usage: python data/extract_grid.py LBNL_QUEUE_XLSX LBNL_COST_DIR FLEET_JSON   -> data/grid_targets.json

replay[region]       every generation request 2008-25: request month (months since Jan 2008), months to withdrawal
                     (-1 if not withdrawn), months to signed IA (-1 if none), status (0 active or suspended,
                     1 operational, 2 withdrawn, 3 unknown) and MW. Replayed through the operator model to
                     fit study capacity (baaja/grid.py, fit_operators).
ia_coverage[region]  share of operational projects with an IA date; regions >= 0.8 are used to fit study capacity
arrivals[region]     requests per year 2008-25
cost[region]         network + POI upgrade cost, $/kW (2022-24 $), latest study, requests queued 2018 or later, all
                     statuses: lognormal (mu, sigma) of positive costs, share at or near zero, n. CAISO has no LBNL cost
                     file and takes the pooled ISO fit; ERCOT allocates no network upgrades to generators and takes the
                     pooled ISO POI-only fit; Southeast and West come from LBNL's sample of non-ISO balancing authorities.
value                P(complete | cost) = a (1 - Phi((ln c - mu) / sigma)) fitted by maximum likelihood on resolved
                     requests (complete vs withdrawn), ISO and non-ISO: a developer stays if the allocated cost is below its
                     private value, lognormal(mu, sigma); a = share that would complete at zero cost.
kappa                growth of upgrade cost with capacity connected: ln(median cost, requests 2018+ / 2010-17) divided by
                     GW reaching operation 2014-21 as a share of the region's 2025 fleet. Net of the transmission built
                     over the same years.
"""
import glob, json, os, sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

ISO = ["CAISO", "ERCOT", "ISO-NE", "MISO", "NYISO", "PJM", "SPP"]
REG = ISO + ["Southeast", "West"]
T0 = pd.Timestamp("2008-01-01")
END = pd.Timestamp("2025-12-31")
FILES = {"MISO": ("miso_costs_2021", "data", "Real Total/kW", "Real POI/kW"),
         "PJM": ("pjm_costs_2022", "data", "$2022 Total Cost/kW", "$2022 POI Cost/kW"),
         "SPP": ("spp_costs_2023", "data", "$2022 Total Cost/kW", "$2022 POI Cost/kW"),
         "NYISO": ("nyiso_2022", "data", "$2022 Total Cost/kW", "$2022 POI Cost/kW"),
         "ISO-NE": ("isone_interconnection", "data", "$2022 Total Cost/kW", "$2022 POI Cost/kW"),
         "BA": ("ba_costs_2024", "Project Cost Data", "$2024 Total Cost/kW", "$2024 POI Cost/kW")}


def months(a, b):
    return ((b - a).dt.days / 30.44)


def lognorm_fit(x, floor=1.0):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    pos = x[x > floor]
    return dict(mu=float(np.log(pos).mean()), sigma=float(np.log(pos).std()), zero_share=float((x <= floor).mean()),
                median=float(np.median(x)), n=int(len(x)))


def value_fit(c, done):
    c = np.maximum(np.asarray(c, float), 1.0); y = np.asarray(done, bool)
    lc = np.log(c)

    def nll(th):
        a = 1 / (1 + np.exp(-th[0])); mu, s = th[1], np.exp(th[2])
        p = np.clip(a * (1 - norm.cdf((lc - mu) / s)), 1e-9, 1 - 1e-9)
        return -(y * np.log(p) + (~y) * np.log(1 - p)).sum()
    r = minimize(nll, [1.0, np.log(150), 0.0], method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-6, fatol=1e-8))
    a, mu, s = 1 / (1 + np.exp(-r.x[0])), r.x[1], np.exp(r.x[2])
    bins = [0, 10, 50, 100, 200, 400, 1e9]
    obs = {f"{bins[i]}-{bins[i+1]}": [float(y[(c > bins[i]) & (c <= bins[i + 1])].mean()) if ((c > bins[i]) & (c <= bins[i + 1])).any() else None,
                                       int(((c > bins[i]) & (c <= bins[i + 1])).sum())] for i in range(len(bins) - 1)}
    return dict(a=float(a), mu=float(mu), sigma=float(s), median_value=float(np.exp(mu)), n=int(len(c)),
                completion_by_cost_bin=obs)


def load_costs(cost_dir, q):
    out = {}
    for reg, (stem, sheet, col, poi) in FILES.items():
        f = glob.glob(os.path.join(cost_dir, stem + "*.xlsx"))[0]
        d = pd.read_excel(f, sheet_name=sheet)
        d["status"] = d["Request Status"].replace({"Operational": "Complete"})
        d["c"] = pd.to_numeric(d[col], errors="coerce"); d["poi"] = pd.to_numeric(d[poi], errors="coerce")
        qd = d["Queue Date"]
        d["qy"] = pd.to_numeric(qd, errors="coerce") if reg == "SPP" else pd.to_datetime(qd, errors="coerce").dt.year
        if reg == "BA":                                     # link to LBNL regions through the Queued Up project id
            m = q[q.region.isin(["Southeast", "West"])].drop_duplicates("q_id").set_index("q_id").region
            d["region"] = d["Project # in Queued Up"].map(m)
            for r in ("Southeast", "West"):
                out[r] = d[d.region == r].copy()
            out["BA"] = d
        else:
            d["region"] = reg; out[reg] = d
    return out


def run(qpath, cost_dir, fleet_path):
    q = pd.read_excel(qpath, sheet_name="03. Complete Queue Data", header=1)
    q = q[q.project_type == "Generation"].copy()
    fleet = json.load(open(fleet_path))["capacity"]
    res = dict(meta=dict(source="LBNL Queued Up (through 2025) and LBNL interconnection cost studies (CC BY 4.0)",
                         month0="2008-01", regions=REG))
    # ---- replay arrays and IA coverage ----
    g = q[(q.q_date >= T0) & (q.q_date <= END)].copy()
    g["qm"] = np.floor(months(pd.Series(T0, index=g.index), g.q_date)).astype(int)
    g["wd"] = np.where(g.q_status == "withdrawn", np.round(months(g.q_date, g.wd_date)), np.nan)
    g["ia"] = np.round(months(g.q_date, g.ia_date))
    g.loc[g.ia <= 0, "ia"] = np.nan
    g.loc[(g.q_status == "withdrawn") & g.wd_date.isna(), "wd"] = np.nan
    res["replay"], res["ia_coverage"], res["arrivals"] = {}, {}, {}
    for r in REG:
        s = g[g.region == r].sort_values("qm")
        st = s.q_status.map({"active": 0, "suspended": 0, "operational": 1, "withdrawn": 2}).fillna(3).astype(int)
        res["replay"][r] = dict(q=s.qm.tolist(), wd=s.wd.fillna(-1).clip(lower=-1).astype(int).tolist(),
                                ia=s.ia.fillna(-1).astype(int).tolist(), st=st.tolist(),
                                mw=s.mw_1.fillna(0).round().astype(int).tolist())
        op = q[(q.region == r) & (q.q_status == "operational") & (q.q_year >= 2010)]
        res["ia_coverage"][r] = float(op.ia_date.notna().mean()) if len(op) else 0.0
        res["arrivals"][r] = {int(y): int(n) for y, n in s.groupby(s.q_date.dt.year).size().items()}
    # ---- costs ----
    C = load_costs(cost_dir, q)
    res["cost"], res["cost_old"] = {}, {}
    iso_new = pd.concat([C[r][C[r].qy >= 2018] for r in ("MISO", "PJM", "SPP", "NYISO", "ISO-NE")])
    for r in ("MISO", "PJM", "SPP", "NYISO", "ISO-NE", "Southeast", "West"):
        d = C[r]
        res["cost"][r] = lognorm_fit(d[d.qy >= 2018].c)
        res["cost_old"][r] = lognorm_fit(d[d.qy.between(2010, 2017)].c)
    res["cost"]["CAISO"] = dict(lognorm_fit(iso_new.c), note="pooled ISO (no LBNL CAISO cost file)")
    res["cost"]["ERCOT"] = dict(lognorm_fit(iso_new.poi), note="pooled ISO POI-only cost: ERCOT does not allocate network upgrades to generators")
    # ---- value distribution ----
    res["value"] = {}
    for lab, regs in (("ISO", ("MISO", "PJM", "SPP", "NYISO", "ISO-NE")), ("non-ISO", ("BA",))):
        d = pd.concat([C[r] for r in regs])
        d = d[d.status.isin(["Complete", "Withdrawn"]) & d.c.notna()]
        res["value"][lab] = value_fit(d.c, d.status == "Complete")
    # ---- kappa: cost growth per share of fleet connected ----
    kap = {}
    for r in ("MISO", "PJM", "SPP", "NYISO", "ISO-NE", "Southeast", "West"):
        new, old = res["cost"][r]["median"], res["cost_old"][r]["median"]
        op = q[(q.region == r) & (q.q_status == "operational") & q.on_date.dt.year.between(2014, 2021)]
        gw = float(op.mw_1.fillna(0).sum()) / 1000
        fl = sum(fleet.get(r, {}).values()) / 1000
        if old > 0 and new > 0 and gw > 0 and fl > 0 and res["cost_old"][r]["n"] >= 30:
            kap[r] = dict(ln_ratio=float(np.log(new / old)), gw_connected=gw, fleet_gw=fl, kappa=float(np.log(new / old) / (gw / fl)))
    ks = [v["kappa"] for v in kap.values() if v["kappa"] > 0]
    res["kappa"] = dict(by_region=kap, median=float(np.median(ks)) if ks else 0.0)
    return res


if __name__ == "__main__":
    out = run(*sys.argv[1:4])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "grid_targets.json"), "w"), separators=(",", ":"))
    print("coverage", {k: round(v, 2) for k, v in out["ia_coverage"].items()})
    print("cost", {k: (round(np.exp(v["mu"])), round(v["sigma"], 2), v["n"]) for k, v in out["cost"].items()})
    print("value", {k: {x: (round(y, 3) if isinstance(y, float) else y) for x, y in v.items() if x != "completion_by_cost_bin"} for k, v in out["value"].items()})
    print("kappa", json.dumps(out["kappa"], indent=0)[:900])
