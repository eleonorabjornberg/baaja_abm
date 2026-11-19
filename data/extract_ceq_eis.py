"""Electricity EISs per year and EIS durations by technology from CEQ's EIS timeline data (public domain).

Usage: python data/extract_ceq_eis.py path/to/CEQ_EIS_Timeline_Data_2024_1_13_2025.xlsx
       (https://nepa.gov/sites/default/files/documents/CEQ_EIS_Timeline_Data_2024_1_13_2025.xlsx)
Writes data/ceq_eis_targets.json and data/ceq_electricity_eis.csv (the classified subset, for checking).

Classification is by keywords in the project title (and lead agency for BOEM / FERC); cooperating-agency
duplicates are dropped (same title prefix, same FEIS year). This is a keyword classifier: check the CSV.
"""
import json, os, re, sys

import pandas as pd


def classify(title, agency):
    s = str(title).lower(); a = str(agency)
    if "geotherm" in s: return "Geothermal"
    if "solar" in s: return "Solar"
    if re.search(r"offshore wind|wind energy area", s) or (a == "BOEM" and "wind" in s): return "Offshore wind"
    if re.search(r"\bwind\b", s) and not re.search(r"wind river|windy|wind cave", s): return "Onshore wind"
    if re.search(r"battery", s): return "Storage"
    if re.search(r"hydroelectric|hydro project|hydropower|pumped storage|energy storage project|relicens", s):
        return "Hydro relicense"
    if re.search(r"transmission|\bkv\b|kilovolt|power line|powerline|intertie", s): return "Transmission"
    if re.search(r"natural gas|combined.cycle|peaking|gas.fired", s) and re.search(r"generat|power plant|energy center|station", s):
        return "Gas"
    if re.search(r"lng|pipeline|natural gas|compressor", s): return "Gas pipeline/LNG (not modelled)"
    return None


def extract(path, y0=2015, y1=2024):
    d = pd.read_excel(path)
    d["yr"] = pd.to_datetime(d["FEIS NOA Date"]).dt.year
    d["tech"] = [classify(t, a) for t, a in zip(d["Project Title"], d["Lead Agency"])]
    e = d[d.tech.notna()].copy()
    e["key"] = e["Project Title"].str.lower().str.replace(r"[^a-z0-9 ]", "", regex=True).str.slice(0, 40)
    e = e.sort_values("FEIS NOA Date").drop_duplicates(["key", "yr"])
    w = e[e.yr.between(y0, y1)]
    out = {}
    for t, g in e.groupby("tech"):
        gw = w[w.tech == t]
        out[t] = dict(eis_per_year=len(gw) / (y1 - y0 + 1), n_window=int(len(gw)), n_all=int(len(g)),
                      median_months_noi_to_feis=float(g["Years from NOI to FEIS"].median() * 12),
                      by_year={int(k): int(v) for k, v in g.groupby("yr").size().items()})
    allm = float(d["Years from NOI to FEIS"].median() * 12)
    return e, dict(meta=dict(source="CEQ EIS Timeline Data 2010-2024 (released 2025-01-13)", window=[y0, y1],
                             all_eis_median_months=allm, n_all_eis=int(len(d))), types=out)


if __name__ == "__main__":
    e, res = extract(sys.argv[1])
    here = os.path.dirname(__file__)
    e.drop(columns=["key"]).to_csv(os.path.join(here, "ceq_electricity_eis.csv"), index=False)
    json.dump(res, open(os.path.join(here, "ceq_eis_targets.json"), "w"), indent=1)
    for t, v in res["types"].items():
        print(f"{t:34s} EIS/yr {v['eis_per_year']:.1f} (n={v['n_window']}, all {v['n_all']})  median NOI->FEIS {v['median_months_noi_to_feis']:.0f} mo")
    print("all EISs median months", round(res["meta"]["all_eis_median_months"]), "n", res["meta"]["n_all_eis"])
