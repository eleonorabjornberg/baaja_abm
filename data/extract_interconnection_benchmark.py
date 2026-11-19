"""Interconnection benchmark for Sec.2106/2110 (Simulation 3), from the LBNL queue data.

No study measures what past queue reforms did to study times, so the data give a bracket rather than a point:
  floor    0: within-region trends show no shortening of request -> IA times in the regions with reliable IA dates
             (MISO, CAISO) across the reform years, as volumes surged.
  ceiling  the ERCOT gap: 1 - ERCOT median / median of CAISO + MISO, request -> signed IA, requests 2015-2019 that
           reached an IA. ERCOT's connect-and-manage, proactive-planning process is the closest US analogue to
           Sec.2106's planned interconnection locations with fixed per-MW costs; reaching it fully would also require
           energy-only interconnection, which the bill does not mandate.
Only regions where >= 80% of operational projects have an IA date are used (CAISO, ERCOT, MISO).

Usage: python data/extract_interconnection_benchmark.py LBNL_XLSX  -> data/interconnection_benchmark.json
"""
import json, os, sys

import numpy as np
import pandas as pd


def run(path):
    q = pd.read_excel(path, sheet_name="03. Complete Queue Data", header=1)
    q = q[(q.project_type == "Generation") & q.q_date.notna()].copy()
    q["mo_ia"] = (q.ia_date - q.q_date).dt.days / 30.44
    op = q[q.q_status == "operational"]
    coverage = op.groupby("region").ia_date.apply(lambda s: float(s.notna().mean())).to_dict()
    reliable = sorted(r for r, c in coverage.items() if c >= 0.8)
    done = q[q.mo_ia.notna() & (q.mo_ia > 0)]
    coh = done[done.q_year.between(2015, 2019)]
    med = {r: float(coh[coh.region == r].mo_ia.median()) for r in reliable}
    n = {r: int((coh.region == r).sum()) for r in reliable}
    others = [r for r in reliable if r != "ERCOT"]
    pooled = float(coh[coh.region.isin(others)].mo_ia.median())
    trend = {r: {int(y): float(v) for y, v in done[done.region == r].groupby("q_year").mo_ia.median().loc[2012:2022].items()}
             for r in reliable}
    return dict(ia_date_coverage=coverage, regions_used=reliable, median_months_2015_19=med, n_2015_19=n,
                pooled_non_ERCOT_median=pooled, ercot_gap_cut=float(1 - med["ERCOT"] / pooled),
                median_by_cohort=trend,
                note="trend medians for cohorts after ~2020 are biased short: only fast projects have IAs yet")


if __name__ == "__main__":
    out = run(sys.argv[1])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "interconnection_benchmark.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("regions_used", "median_months_2015_19", "n_2015_19", "pooled_non_ERCOT_median", "ercot_gap_cut")}, indent=1))
    for r, t in out["median_by_cohort"].items():
        print(r, {y: round(v) for y, v in t.items()})
