"""Extract calibration targets from LBNL 'Queued Up' interconnection queue data (CC BY 4.0).

Usage: python data/extract_lbnl.py path/to/LBNL_Ix_Queue_Data_File_thru2025.xlsx
Writes data/lbnl_targets.json (committed; the raw workbook is not).

Definitions (Generation requests only; resource type = type_1, so hybrids count under their first type):
  arr_per_month    requests per month, 2021-2025 queue years
  completion       share of 2000-2020 requests now operational (LBNL's own completion metric)
  mw_built         mean mw_1 of operational projects queued 2010 or later (projects that complete are much smaller
                   than the average request, so GW = completed count x built size)
  mw_built_recent  mean mw_1 of projects that reached operation 2022-2025 (sizes have grown; used for forward runs)
  ix_median, ix_logsd   interconnection request -> signed IA, months, requests queued 2015+ (median, sd of log)
  cod_median       interconnection request -> commercial operation, months, operational projects queued 2015-2018
                   (a cohort with >= 7 years to finish, which limits the bias toward fast projects)
"""
import json, os, sys

import numpy as np
import pandas as pd

MAP = {"Solar": "Solar", "Battery": "Storage", "Wind": "Onshore wind", "Offshore Wind": "Offshore wind",
       "Gas": "Gas", "Geothermal": "Geothermal"}


def extract(path):
    q = pd.read_excel(path, sheet_name="03. Complete Queue Data", header=1)
    q = q[q.project_type == "Generation"].copy()
    q["mt"] = q.type_1.map(MAP)
    mo = lambda a, b: (b - a).dt.days / 30.44
    out = {}
    for t, g in q[q.mt.notna()].groupby("mt"):
        rec, coh = g[g.q_year.between(2021, 2025)], g[g.q_year.between(2000, 2020)]
        op = g[(g.q_status == "operational") & (g.q_year >= 2010)]
        ia = g[g.ia_date.notna() & g.q_date.notna() & (g.q_year >= 2015)]
        d = mo(ia.q_date, ia.ia_date); d = d[d > 0]
        c = g[(g.q_status == "operational") & g.on_date.notna() & g.q_date.notna() & g.q_year.between(2015, 2018)]
        dc = mo(c.q_date, c.on_date); dc = dc[dc > 0]
        recent = g[(g.q_status == "operational") & g.on_date.dt.year.between(2022, 2025)]
        out[t] = dict(arr_per_month=len(rec) / 60, mw_built_recent=float(recent.mw_1.mean()) if len(recent) else None,
                      n_built_recent=int(len(recent)), completion=float((coh.q_status == "operational").mean()),
                      n_cohort=int(len(coh)), mw_built=float(op.mw_1.mean()), n_built=int(len(op)),
                      mw_requested_median=float(rec.mw_1.median()),
                      ix_median=float(d.median()), ix_logsd=float(np.log(d).std()), n_ix=int(len(d)),
                      cod_median=float(dc.median()) if len(dc) else None, n_cod=int(len(dc)),
                      arr_by_year={int(y): int(n) for y, n in g.groupby("q_year").size().loc[2019:2025].items()})
    allg = q[q.q_year.between(2000, 2020)]
    meta = dict(source="LBNL Queued Up, interconnection queue data through 2025 (CC BY 4.0)",
                all_generation_completion_2000_2020=float((allg.q_status == "operational").mean()))
    return dict(meta=meta, types=out)


if __name__ == "__main__":
    res = extract(sys.argv[1])
    dst = os.path.join(os.path.dirname(__file__), "lbnl_targets.json")
    json.dump(res, open(dst, "w"), indent=1)
    print(json.dumps(res, indent=1))
