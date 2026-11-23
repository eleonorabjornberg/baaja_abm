"""Regional split of interconnection requests, from the LBNL queue data (CC BY 4.0).

Usage: python data/extract_regions.py LBNL_XLSX   -> data/region_targets.json

LBNL's nine regions: seven ISO/RTO markets (CAISO, ERCOT, ISO-NE, MISO, NYISO, PJM, SPP) and two non-ISO regions
(Southeast, West), assigned by LBNL. For each technology:
  new_share[mkt][region]     share of 2021-25 requests in each region, within ISO (mkt 0) and non-ISO (mkt 1)
                             markets. The model already draws ISO vs non-ISO; the region is drawn within it.
  active_share[mkt][region]  same, for requests active or suspended at end-2025 (the seeded queue)
  completion[region]         share of 2000-20 requests now operational (cells with >= 30 requests), for checks
  ia_months_median[region]   request -> signed IA, months, requests 2015-19 that reached an IA (biased short)
  since_ia_quantiles         months from signed IA to 31 Dec 2025 for active/suspended requests with an IA, at
                             quantiles 0, 0.05, ..., 1: how far into construction the seeded queue already is
  ia_to_cod_median_recent    signed IA -> commercial operation, months, projects reaching operation 2022-25
"""
import json, os, sys

import pandas as pd

MAP = {"Solar": "Solar", "Battery": "Storage", "Wind": "Onshore wind", "Offshore Wind": "Offshore wind",
       "Gas": "Gas", "Geothermal": "Geothermal"}
ISO = ["CAISO", "ERCOT", "ISO-NE", "MISO", "NYISO", "PJM", "SPP"]
NON = ["Southeast", "West"]


def shares(df):
    out = {}
    for m, regs in ((0, ISO), (1, NON)):
        sub = df[df.region.isin(regs)]
        n = len(sub)
        out[str(m)] = {r: (float((sub.region == r).sum() / n) if n else 1.0 / len(regs)) for r in regs}
        out[f"n_{m}"] = int(n)
    return out


def run(path):
    q = pd.read_excel(path, sheet_name="03. Complete Queue Data", header=1)
    q = q[q.project_type == "Generation"].copy()
    q["mt"] = q.type_1.map(MAP)
    q["mo_ia"] = (q.ia_date - q.q_date).dt.days / 30.44
    res = {}
    for t, g in q[q.mt.notna()].groupby("mt"):
        new = g[g.q_year.between(2021, 2025)]
        act = g[g.q_status.isin(["active", "suspended"])]
        coh = g[g.q_year.between(2000, 2020)]
        comp = {r: float((c.q_status == "operational").mean()) for r, c in coh.groupby("region") if len(c) >= 30}
        ia = g[g.q_year.between(2015, 2019) & (g.mo_ia > 0)]
        since = ((pd.Timestamp("2025-12-31") - act.ia_date).dt.days / 30.44).dropna()
        since = since[since >= 0]
        qs = [float(since.quantile(x)) for x in [i / 20 for i in range(21)]] if len(since) >= 20 else None
        op = g[(g.q_status == "operational") & g.on_date.dt.year.between(2022, 2025)]
        i2c = ((op.on_date - op.ia_date).dt.days / 30.44).dropna()
        i2c = i2c[i2c > -6]
        res[t] = dict(new_share=shares(new), active_share=shares(act), completion=comp,
                      ia_to_cod_median_recent=float(i2c.median()) if len(i2c) >= 20 else None, n_ia_to_cod=int(len(i2c)),
                      since_ia_quantiles=qs, n_since_ia=int(len(since)),
                      n_cohort={r: int(len(c)) for r, c in coh.groupby("region")},
                      ia_months_median={r: float(c.mo_ia.median()) for r, c in ia.groupby("region") if len(c) >= 20})
    return dict(meta=dict(source="LBNL Queued Up, interconnection queue data through 2025 (CC BY 4.0)",
                          regions_iso=ISO, regions_non_iso=NON,
                          ferc_rto=[r for r in ISO if r != "ERCOT"],
                          note="ERCOT is an ISO market but intrastate: FERC's Sec.2106 rule does not reach it"),
                types=res)


if __name__ == "__main__":
    out = run(sys.argv[1])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "region_targets.json"), "w"), indent=1)
    for t, v in out["types"].items():
        print(t, {k: round(x, 2) for k, x in v["new_share"]["0"].items()}, {k: round(x, 2) for k, x in v["new_share"]["1"].items()})
