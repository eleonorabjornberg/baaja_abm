"""Existing generating fleet by region, technology group and vintage, with retirements and capacity factors.

Usage: python data/extract_fleet.py EIA860_2025_DIR EIA860M_SEP2026_XLSX EIA923_2025_XLSX   -> data/fleet_targets.json

Fleet = EIA-860 2025 operable generators (as of end-2025, the same date as the LBNL queue snapshot the model seeds
from, so projects completed in 2026 are counted once, as model additions). Net summer capacity, MW.
Retirement year: EIA-860M Sep 2026 where it has newer information (units retired in 2026, or an updated planned
retirement year), otherwise EIA-860 2025's planned retirement year. Units without a planned retirement are listed by operating year (`unannounced_by_vintage`) for the
age-based retirement assumption in baaja/supply.py.
Region: plant balancing authority -> LBNL's nine regions (ISO BAs by code; other BAs by state: Western
Interconnection states -> West, the rest -> Southeast), the same split LBNL uses. Alaska and Hawaii excluded.
Capacity factor: EIA-923 2025 net generation / EIA-860 2025 summer capacity, by region and group (national value
where a cell has < 1 GW).
"""
import json, os, sys

import numpy as np
import pandas as pd

GROUP = {
    "Conventional Steam Coal": "Coal", "Coal Integrated Gasification Combined Cycle": "Coal", "Petroleum Coke": "Coal",
    "Natural Gas Fired Combined Cycle": "Gas CC", "Natural Gas Fired Combustion Turbine": "Gas CT",
    "Natural Gas Internal Combustion Engine": "Gas CT", "Natural Gas Steam Turbine": "Gas ST",
    "Other Natural Gas": "Gas CT", "Other Gases": "Gas CT", "Natural Gas with Compressed Air Storage": "Gas CT",
    "Petroleum Liquids": "Oil", "Nuclear": "Nuclear", "Conventional Hydroelectric": "Hydro",
    "Hydroelectric Pumped Storage": "Pumped storage", "Onshore Wind Turbine": "Onshore wind",
    "Offshore Wind Turbine": "Offshore wind", "Solar Photovoltaic": "Solar", "Solar Thermal without Energy Storage": "Solar",
    "Solar Thermal with Energy Storage": "Solar", "Batteries": "Storage", "Flywheels": "Storage",
    "Geothermal": "Geothermal",
}  # everything else (biomass, landfill gas, MSW, all other) -> "Other"
BA_REGION = {"CISO": "CAISO", "ERCO": "ERCOT", "ISNE": "ISO-NE", "MISO": "MISO", "NYIS": "NYISO", "PJM": "PJM",
             "SWPP": "SPP"}
WEST_STATES = {"WA", "OR", "CA", "ID", "NV", "UT", "AZ", "MT", "WY", "CO", "NM"}
FUEL_GROUP = {"BIT": "Coal", "SUB": "Coal", "LIG": "Coal", "RC": "Coal", "WC": "Coal", "SGC": "Coal", "PC": "Coal",
              "NG": "Gas", "OG": "Gas", "BFG": "Gas", "DFO": "Oil", "RFO": "Oil", "JF": "Oil", "KER": "Oil", "WO": "Oil",
              "NUC": "Nuclear", "WND": "Wind", "SUN": "Solar", "GEO": "Geothermal", "MWH": "Storage"}


def region(ba, state):
    if ba in BA_REGION:
        return BA_REGION[ba]
    if state in ("AK", "HI") or pd.isna(state):
        return None
    return "West" if state in WEST_STATES else "Southeast"


def run(d860, f860m, f923):
    g = pd.read_excel(os.path.join(d860, "3_1_Generator_Y2025.xlsx"), "Operable", header=1)
    pl = pd.read_excel(os.path.join(d860, "2___Plant_Y2025.xlsx"), header=1)[["Plant Code", "Balancing Authority Code", "State"]]
    g = g.merge(pl.rename(columns={"State": "pstate"}), on="Plant Code", how="left")
    g["region"] = [region(b, s) for b, s in zip(g["Balancing Authority Code"], g["pstate"])]
    g["group"] = g.Technology.map(GROUP).fillna("Other")
    g["mw"] = pd.to_numeric(g["Summer Capacity (MW)"], errors="coerce").fillna(0)
    g["ret"] = pd.to_numeric(g["Planned Retirement Year"], errors="coerce")
    g["key"] = g["Plant Code"].astype(str) + "|" + g["Generator ID"].astype(str)
    # newer retirement information from EIA-860M (Sep 2026)
    m_ret = pd.read_excel(f860m, "Retired", header=2)
    m_op = pd.read_excel(f860m, "Operating", header=2)
    for d in (m_ret, m_op):
        d["key"] = d["Plant ID"].astype(str) + "|" + d["Generator ID"].astype(str)
    retired_2026 = dict(zip(m_ret.key, pd.to_numeric(m_ret["Retirement Year"], errors="coerce")))
    planned_m = dict(zip(m_op.key, pd.to_numeric(m_op["Planned Retirement Year"], errors="coerce")))
    n_upd = 0
    for i, k in zip(g.index, g.key):
        if k in retired_2026 and retired_2026[k] >= 2026:
            g.at[i, "ret"] = retired_2026[k]; n_upd += 1
        elif k in planned_m:
            new = planned_m[k]
            if not (pd.isna(new) and pd.isna(g.at[i, "ret"])) and new != g.at[i, "ret"]:
                g.at[i, "ret"] = new; n_upd += 1
    g = g[g.region.notna()]
    regions = sorted(g.region.unique()); groups = sorted(g.group.unique())
    cap = {r: {k: float(v) for k, v in g[g.region == r].groupby("group").mw.sum().items()} for r in regions}
    # retirements by region x group x year (MW leaving at the start of that year)
    rr = g[g.ret.notna() & (g.ret >= 2026) & (g.ret <= 2045)]
    ret = {r: {k: {int(y): float(v) for y, v in d.groupby("ret").mw.sum().items()} for k, d in rr[rr.region == r].groupby("group")}
           for r in regions}
    # units with no announced retirement, by operating year: the age-based retirement assumption applies to these
    g["opy"] = pd.to_numeric(g["Operating Year"], errors="coerce")
    un = g[g.ret.isna() & g.opy.notna()]
    unannounced = {r: {k: {int(y): float(v) for y, v in d.groupby("opy").mw.sum().items()} for k, d in un[un.region == r].groupby("group")}
                   for r in regions}
    # capacity factors from EIA-923
    e = pd.read_excel(f923, "Page 1 Generation and Fuel Data", header=5)
    e.columns = [c.replace("\n", " ") for c in e.columns]
    e["region"] = [region(b, s) for b, s in zip(e["Balancing Authority Code"], e["Plant State"])]
    pm = e["Reported Prime Mover"]; fu = e["Reported Fuel Type Code"]
    grp = fu.map(FUEL_GROUP).fillna("Other")
    grp = np.where(pm == "PS", "Pumped storage", np.where(fu == "WAT", "Hydro", grp))
    grp = np.where((grp == "Wind") & (pm == "WS"), "Offshore wind", np.where(grp == "Wind", "Onshore wind", grp))
    e["g2"] = grp
    gen = e[e.region.notna()].groupby(["region", "g2"])["Net Generation (Megawatthours)"].sum()
    cap2 = g.assign(g2=g.group.replace({"Gas CC": "Gas", "Gas CT": "Gas", "Gas ST": "Gas"})).groupby(["region", "g2"]).mw.sum()
    nat = (gen.groupby(level=1).sum() / cap2.groupby(level=1).sum() / 8760).to_dict()
    cf = {}
    for (r, k), mw in cap2.items():
        v = gen.get((r, k), 0.0) / mw / 8760 if mw > 0 else np.nan
        cf.setdefault(r, {})[k] = float(v if mw >= 1000 and np.isfinite(v) else nat.get(k, 0.0))
    return dict(meta=dict(source="EIA-860 2025 (operable, end-2025); EIA-860M Sep 2026 (retirements); EIA-923 2025 "
                          "(generation)", units="MW net summer capacity", retirement_updates_from_860m=n_upd,
                          regions=regions, groups=groups,
                          national_cf={k: float(v) for k, v in nat.items()}),
                capacity=cap, retirements=ret, unannounced_by_vintage=unannounced, capacity_factor=cf)


if __name__ == "__main__":
    out = run(*sys.argv[1:4])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "fleet_targets.json"), "w"), indent=1)
    tot = {k: sum(out["capacity"][r].get(k, 0) for r in out["capacity"]) / 1000 for k in out["meta"]["groups"]}
    print("US GW:", {k: round(v, 1) for k, v in tot.items()}, "total", round(sum(tot.values()), 1))
    print("retirement updates from 860M:", out["meta"]["retirement_updates_from_860m"])
    for r in out["capacity"]:
        rt = sum(v for d in out["retirements"][r].values() for y, v in d.items() if y <= 2041) / 1000
        print(f"{r:10s} {sum(out['capacity'][r].values())/1000:6.1f} GW; announced retirements to 2041 {rt:5.1f} GW")
    print("national CF:", {k: round(v, 2) for k, v in out["meta"]["national_cf"].items()})
