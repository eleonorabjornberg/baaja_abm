"""EIA-860M (monthly generator inventory): late-stage completion by technology and the growth of the gas pipeline.

Usage: python data/extract_eia860m.py DEC2021_XLSX LATEST_XLSX  -> data/eia860m_targets.json
  late_stage_completion  generators on the "Planned" sheet in Dec 2021, by status in the latest file
                         (operating or retired = completed; canceled/postponed; still planned; dropped)
  storage_vs_solar       storage / solar late-stage completion (by count). Used to correct storage's LBNL completion
                         target, which comes from the 2000-20 request cohort when few batteries finished.
  planned_GW             planned capacity by technology in each file (gas pipeline growth)
"""
import json, os, sys

import pandas as pd

M = {"Batteries": "Storage", "Solar Photovoltaic": "Solar", "Onshore Wind Turbine": "Onshore wind",
     "Offshore Wind Turbine": "Offshore wind", "Natural Gas Fired Combined Cycle": "Gas",
     "Natural Gas Internal Combustion Engine": "Gas", "Natural Gas Fired Combustion Turbine": "Gas"}


def load(f, sheet):
    raw = pd.read_excel(f, sheet, header=None, nrows=6)
    h = [i for i in range(6) if raw.iloc[i].astype(str).str.contains("Plant ID").any()][0]
    d = pd.read_excel(f, sheet, header=h)
    d = d[pd.to_numeric(d["Plant ID"], errors="coerce").notna()].copy()
    d["key"] = d["Plant ID"].astype(int).astype(str) + "|" + d["Generator ID"].astype(str)
    d["mt"] = d.Technology.map(M); d["mw"] = pd.to_numeric(d["Nameplate Capacity (MW)"], errors="coerce")
    return d


def run(old, new):
    p = load(old, "Planned")
    st = {s: set(load(new, s).key) for s in ("Operating", "Planned", "Retired", "Canceled or Postponed")}
    p = p[p.mt.notna()].copy()
    p["now"] = p.key.map(lambda k: "completed" if k in st["Operating"] or k in st["Retired"] else
                         "cancelled" if k in st["Canceled or Postponed"] else "still planned" if k in st["Planned"] else "dropped")
    comp = {t: dict(n=int(len(g)), **{s: float((g.now == s).mean()) for s in ("completed", "cancelled", "still planned", "dropped")},
                    completed_MW_share=float(g.mw[g.now == "completed"].sum() / g.mw.sum())) for t, g in p.groupby("mt")}
    newp = load(new, "Planned")
    return dict(late_stage_completion=comp,
                storage_vs_solar=comp["Storage"]["completed"] / comp["Solar"]["completed"],
                planned_GW={"Dec 2021": (p.groupby("mt").mw.sum() / 1000).to_dict(),
                            "latest": (newp[newp.mt.notna()].groupby("mt").mw.sum() / 1000).to_dict()},
                gas_planned_GW_by_year={int(y): float(v / 1000) for y, v in newp[newp.mt == "Gas"].groupby("Planned Operation Year").mw.sum().items()},
                files=[os.path.basename(old), os.path.basename(new)])


if __name__ == "__main__":
    out = run(sys.argv[1], sys.argv[2])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "eia860m_targets.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("storage_vs_solar", "planned_GW")}, indent=1))
