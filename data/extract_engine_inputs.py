"""Inputs for the v5 engine that were not yet extracted (raw files are user-supplied or public; not committed).

Usage: python data/extract_engine_inputs.py LBNL_XLSX CORPS_XLSX NEPA_CASES_CSV EIA860_DIR
Writes data/engine_inputs.json with:
  lbnl.arrivals_by_year      Generation requests per queue year (2005-2025) by technology      -> backcast arrivals
  lbnl.active_end2025        active/suspended requests at end-2025: ages (months since request, binned) and share
                             with an executed IA                                                 -> seeded pipeline
  lbnl.hybrid_storage        battery components of hybrid requests (type_2/3 = Battery): requests/month 2021-25 and
                             mean built MW (mw_2/mw_3 of operational hybrids queued 2010+)       -> storage arrivals
  lbnl.by_market             completion (2000-20 cohort) and median IR->COD by ISO vs non-ISO region -> Sim 5
  corps.standard_permit      public notice -> decision, months (Standard Permits)                  -> Corps EA duration
  cases.months_in_litigation median by court level (district / appeals)                          -> case length
  eia860.retirement_age      age at retirement of generators retired, by technology              -> Sim 4 lifetimes
"""
import json, os, sys

import numpy as np
import pandas as pd

MAP = {"Solar": "Solar", "Battery": "Storage", "Wind": "Onshore wind", "Offshore Wind": "Offshore wind",
       "Gas": "Gas", "Geothermal": "Geothermal"}
ISO = {"CAISO", "ERCOT", "ISO-NE", "MISO", "NYISO", "PJM", "SPP"}
BINS = [0, 12, 24, 36, 48, 60, 84, 120, 600]


def lbnl(path):
    q = pd.read_excel(path, sheet_name="03. Complete Queue Data", header=1)
    q = q[q.project_type == "Generation"].copy()
    q["mt"] = q.type_1.map(MAP)
    end = pd.Timestamp("2025-12-31")
    out = dict(arrivals_by_year={}, active_end2025={}, by_market={})
    g = q[q.mt.notna()]
    for t, d in g.groupby("mt"):
        out["arrivals_by_year"][t] = {int(y): int(n) for y, n in d.groupby("q_year").size().items() if 2005 <= y <= 2025}
        a = d[d.q_status.isin(["active", "suspended"]) & d.q_date.notna()]
        age = (end - a.q_date).dt.days / 30.44
        h = np.histogram(age.clip(0, 599), bins=BINS)[0]
        out["active_end2025"][t] = dict(n=int(len(a)), age_bins=BINS, age_counts=[int(x) for x in h],
                                        ia_executed_share=float((a.IA_phase_clean == "IA Executed").mean()))
        mk = {}
        for m, s in [("ISO", d[d.region.isin(ISO)]), ("non-ISO", d[~d.region.isin(ISO)])]:
            coh = s[s.q_year.between(2000, 2020)]
            mk[m] = dict(n_cohort=int(len(coh)), completion=float((coh.q_status == "operational").mean()) if len(coh) else None,
                         arrivals_share_2021_25=float(len(s[s.q_year.between(2021, 2025)]) / max(len(d[d.q_year.between(2021, 2025)]), 1)))
        out["by_market"][t] = mk
    hb = q[(q.type_2 == "Battery") | (q.type_3 == "Battery")]
    mwb = np.where(hb.type_2 == "Battery", hb.mw_2, hb.mw_3)
    hb = hb.assign(mwb=pd.to_numeric(mwb, errors="coerce"))
    built = hb[(hb.q_status == "operational") & (hb.q_year >= 2010)]
    out["hybrid_storage"] = dict(req_per_month_2021_25=float(len(hb[hb.q_year.between(2021, 2025)]) / 60),
                                 mw_built_mean=float(built.mwb.mean()), n_built=int(built.mwb.notna().sum()),
                                 parent_types=hb[hb.q_year.between(2021, 2025)].type_1.value_counts().to_dict(),
                                 arrivals_by_year={int(y): int(n) for y, n in hb.groupby("q_year").size().items() if 2005 <= y <= 2025})
    return out


def corps(path):
    c = pd.read_excel(path)
    s = c[c["Permit Type"] == "Standard Permit"]
    m = (pd.to_datetime(s["Date Issued/Denied"], errors="coerce") - pd.to_datetime(s["Public Notice Date"], format="%d-%b-%Y", errors="coerce")).dt.days / 30.44
    m = m[(m > 0) & (m < 240)]
    return dict(standard_permit=dict(n=int(len(m)), median_months=float(m.median()), p25=float(m.quantile(.25)),
                                     p75=float(m.quantile(.75)), log_sd=float(np.log(m).std()),
                                     note="public notice -> decision; excludes pre-application time"))


def cases(path):
    d = pd.read_csv(path, encoding_errors="replace", low_memory=False)
    app = d["Court Line"].fillna("").str.contains("Appeals")
    energy = d["Project Category"] == "Energy"
    f = lambda m: dict(n=int(m.sum()), median_months=float(d.days_in_litigation[m].median() / 30.44))
    return dict(months_in_litigation=dict(district=f(~app), appeals=f(app), district_energy=f(~app & energy), appeals_energy=f(app & energy)))


def eia_retire(eia_dir):
    TECH = {"Natural Gas Fired Combined Cycle": "Gas", "Natural Gas Fired Combustion Turbine": "Gas",
            "Natural Gas Steam Turbine": "Gas", "Natural Gas Internal Combustion Engine": "Gas",
            "Onshore Wind Turbine": "Onshore wind", "Solar Photovoltaic": "Solar", "Batteries": "Storage",
            "Conventional Hydroelectric": "Hydro", "Geothermal": "Geothermal", "Conventional Steam Coal": "Coal"}
    x = pd.ExcelFile(os.path.join(eia_dir, "3_1_Generator_Y2025.xlsx"))
    sh = [s for s in x.sheet_names if "Retired" in s][0]
    r = pd.read_excel(x, sh, header=1)
    r["mt"] = r.Technology.map(TECH)
    r["age"] = pd.to_numeric(r["Retirement Year"], errors="coerce") - pd.to_numeric(r["Operating Year"], errors="coerce")
    r["mw"] = pd.to_numeric(r["Nameplate Capacity (MW)"], errors="coerce")
    r = r[r.mt.notna() & r.age.between(0, 120)]
    out = {}
    for t, g in r.groupby("mt"):
        w = g.mw.fillna(0)
        out[t] = dict(n=int(len(g)), GW=float(w.sum() / 1000), median_age=float(g.age.median()),
                      mw_weighted_mean_age=float((g.age * w).sum() / max(w.sum(), 1e-9)),
                      retired_since_2015_GW=float(w[pd.to_numeric(g["Retirement Year"], errors="coerce") >= 2015].sum() / 1000))
    return dict(retirement_age=out, sheet=sh)


if __name__ == "__main__":
    lb, cx, cs, eia = sys.argv[1:5]
    out = dict(lbnl=lbnl(lb), corps=corps(cx), cases=cases(cs), eia860=eia_retire(eia))
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "engine_inputs.json"), "w"), indent=1, default=float)
    print(json.dumps({k: out["lbnl"][k] for k in ("active_end2025", "hybrid_storage")}, indent=1)[:3000])
    print(json.dumps(out["corps"], indent=1)); print(json.dumps(out["cases"], indent=1)); print(json.dumps(out["eia860"], indent=1)[:1500])
    print(json.dumps(out["lbnl"]["by_market"], indent=1)[:2000])
