"""Federal nexus of recently built plants: EIA-860 plant locations x BLM Surface Management Agency (SMA) layer.

Usage: python data/extract_federal_nexus.py EIA860_DIR SMA_GDB
  EIA860_DIR  unzipped https://www.eia.gov/electricity/data/eia860/xls/eia8602025.zip (2___Plant, 3_1_Generator)
  SMA_GDB     SMA_WM.gdb from BLM National SMA Surface Management Agency Area Polygons
              (https://gbp-blm-egis.hub.arcgis.com/datasets/BLM-EGIS::blm-national-sma-surface-management-agency-area-polygons)
Writes data/federal_nexus_targets.json and data/eia860_additions.json (annual MW added 2015-2025 by technology).

Federal nexus (lower bound) = plant point (or 1 km buffer) on federal surface land (BLM, USFS, NPS, FWS, DOD, BOR,
other federal, BIA trust land) OR inside a federal balancing authority (WAPA, BPA, TVA, SPA). Not observed: Army
Corps s.404 individual permits, FWS incidental/eagle take permits, DOE/RUS financing, so true nexus is higher.
Offshore wind is federal by statute (OCS Lands Act) and is set to 1.
"""
import json, os, sys

import geopandas as gpd
import pandas as pd
import pyogrio

TECH = {"Solar Photovoltaic": "Solar", "Solar Thermal without Energy Storage": "Solar",
        "Solar Thermal with Energy Storage": "Solar", "Onshore Wind Turbine": "Onshore wind",
        "Offshore Wind Turbine": "Offshore wind", "Batteries": "Storage", "Geothermal": "Geothermal",
        "Natural Gas Fired Combustion Turbine": "Gas", "Natural Gas Fired Combined Cycle": "Gas",
        "Natural Gas Internal Combustion Engine": "Gas"}
FED_LAYERS = ["BLM", "USFS", "NPS", "FWS", "DOD", "BOR", "OTHFED", "BIA"]
FED_BA = {"WACM", "WALC", "WAUW", "WAUE", "BPAT", "TVA", "SPA"}


def load_plants(d, y0=2015, y1=2025):
    pl = pd.read_excel(os.path.join(d, "2___Plant_Y2025.xlsx"), header=1)
    g = pd.read_excel(os.path.join(d, "3_1_Generator_Y2025.xlsx"), sheet_name=0, header=1)
    g["mt"] = g.Technology.map(TECH); g = g[g.mt.notna()].copy()
    g["yr"] = pd.to_numeric(g["Operating Year"], errors="coerce")
    g["mw"] = pd.to_numeric(g["Nameplate Capacity (MW)"], errors="coerce")
    adds = g[g.yr.between(y0, y1)].groupby(["mt", "yr"]).mw.sum().unstack(0).fillna(0)
    g = g[g.yr.between(y0, y1)]
    p = g.groupby(["Plant Code", "mt"]).agg(mw=("mw", "sum"), yr=("yr", "min")).reset_index()
    p = p.merge(pl[["Plant Code", "Latitude", "Longitude", "State", "Regulatory Status",
                    "Balancing Authority Code"]], on="Plant Code", how="left")
    for c in ("Latitude", "Longitude"):
        p[c] = pd.to_numeric(p[c], errors="coerce")
    return p.dropna(subset=["Latitude", "Longitude"]), adds


def nexus(p, gdb, buffers=(0, 1000)):
    pts = gpd.GeoDataFrame(p, geometry=gpd.points_from_xy(p.Longitude, p.Latitude), crs=4326).to_crs(3857)
    on = {b: pd.Series(False, index=p.index) for b in buffers}
    for lyr in FED_LAYERS:
        g = pyogrio.read_dataframe(gdb, layer=f"SurfaceMgtAgy_{lyr}", columns=["ADMIN_AGENCY_CODE"])
        g = g[g.geometry.notna()][["geometry"]]
        for b in buffers:
            q = pts[["geometry"]].copy()
            if b:
                q["geometry"] = q.buffer(b)
            hit = gpd.sjoin(q, g, predicate="intersects", how="inner").index.unique()
            on[b] |= p.index.isin(hit)
    pma = p["Balancing Authority Code"].isin(FED_BA)
    out = {}
    for t, d in p.groupby("mt"):
        r = dict(plants=int(len(d)), GW=float(d.mw.sum() / 1000), federal_BA_share_MW=float((d.mw * pma[d.index]).sum() / d.mw.sum()),
                 utility_owned_share_MW=float((d.mw * (d["Regulatory Status"] == "RE")).sum() / d.mw.sum()))
        for b in buffers:
            nx = on[b][d.index] | pma[d.index]
            r[f"federal_land_share_MW_buf{b}"] = float((d.mw * on[b][d.index]).sum() / d.mw.sum())
            r[f"nexus_share_MW_buf{b}"] = float((d.mw * nx).sum() / d.mw.sum())
            r[f"nexus_share_plants_buf{b}"] = float(nx.mean())
        if t == "Offshore wind":
            for k in list(r):
                if k.startswith("nexus_share"):
                    r[k] = 1.0
            r["note"] = "federal by statute (OCS); SMA does not cover the OCS"
        out[t] = r
    return out


if __name__ == "__main__":
    p, adds = load_plants(sys.argv[1])
    res = dict(meta=dict(source="EIA-860 2025 (plants with generators online 2015-2025) x BLM National SMA",
                         federal_layers=FED_LAYERS, federal_BAs=sorted(FED_BA),
                         caveat="lower bound: s.404, ESA/eagle take, federal financing not observed"),
               types=nexus(p, sys.argv[2]))
    here = os.path.dirname(__file__)
    json.dump(res, open(os.path.join(here, "federal_nexus_targets.json"), "w"), indent=1)
    json.dump({t: {int(y): float(v) for y, v in adds[t].items()} for t in adds}, open(os.path.join(here, "eia860_additions.json"), "w"), indent=1)
    for t, r in res["types"].items():
        print(f"{t:14s} nexus MW {100*r['nexus_share_MW_buf0']:5.1f}-{100*r['nexus_share_MW_buf1000']:5.1f}%  utility-owned {100*r['utility_owned_share_MW']:4.0f}%  GW {r['GW']:.0f}")
    print((adds / 1000).round(1))
