"""Combined federal nexus of plants online 2015-2025, by technology (union of hooks that trigger project-level NEPA):
  land / federal BA   EIA-860 plant point (or 1 km buffer) on federal surface land, or in WAPA/BPA/TVA/SPA
  Corps individual    USACE individual permit within 2 km, decided -5..+1 years around first operation;
                      net of a placebo (permits shifted 20 km)
  RUS                 plant owned by a co-op that received USDA Rural Utilities Service electric loans/grants
                      (USAspending export; lenders NRUCFC/CoBank excluded); co-op name match, so a lower bound
  offshore wind       federal by statute
Also counts DOE EISs by topic (DOE EIS list export).

Usage: python data/combine_federal_hooks.py EIA860_DIR SMA_GDB CORPS_XLSX RUS_CSV DOE_EIS_CSV
Writes data/federal_nexus_combined.json. Raw inputs are not committed.
"""
import json, os, re, sys

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from extract_federal_nexus import FED_BA, FED_LAYERS, load_plants  # noqa: E402
import pyogrio  # noqa: E402

LEGAL = {"INC", "CORP", "CORPORATION", "CO", "LLC", "THE", "INCORPORATED", "A", "AN", "OF", "AND"}
SYN = {"COOPERATIVE": "COOP", "ASSOCIATION": "ASSN", "ELECTRIC": "ELEC", "ELECTRICAL": "ELEC"}
COOP = r"\bCOOP|\bEMC\b|\bASSN\b|ELECTRIFICATION|\bG ?& ?T\b|POWER SUPPLY|MEMBERSHIP|TODAY S POWER"
norm = lambda s: " ".join(x for x in (SYN.get(w, w) for w in re.sub(r"[^A-Z0-9 ]", " ", str(s).upper()).split()) if x not in LEGAL)
k2 = lambda s: " ".join(s.split()[:2])


def land_flags(p, gdb, buffers=(0, 1000)):
    pts = gpd.GeoDataFrame(p, geometry=gpd.points_from_xy(p.Longitude, p.Latitude), crs=4326).to_crs(3857)
    on = {b: np.zeros(len(p), bool) for b in buffers}
    for lyr in FED_LAYERS:
        g = pyogrio.read_dataframe(gdb, layer=f"SurfaceMgtAgy_{lyr}", columns=["ADMIN_AGENCY_CODE"])
        g = g[g.geometry.notna()][["geometry"]]
        for b in buffers:
            q = pts[["geometry"]].copy()
            if b:
                q["geometry"] = q.buffer(b)
            on[b] |= p.index.isin(gpd.sjoin(q, g, predicate="intersects", how="inner").index.unique())
    ba = p["Balancing Authority Code"].isin(FED_BA).values
    return {b: on[b] | ba for b in buffers}


def corps_flags(p, xlsx, R=2000, shift=20000):
    c = pd.read_excel(xlsx)
    c["yr"] = pd.to_datetime(c["Date Issued/Denied"], errors="coerce").dt.year
    c = c.dropna(subset=["Longitude", "Latitude", "yr"])
    c = c[c.Latitude.between(17, 72) & c.Longitude.between(-180, -60)]
    P = gpd.GeoDataFrame(p[["yr"]], geometry=gpd.points_from_xy(p.Longitude, p.Latitude), crs=4326).to_crs(5070)
    C0 = gpd.GeoDataFrame(c[["yr"]], geometry=gpd.points_from_xy(c.Longitude, c.Latitude), crs=4326).to_crs(5070)

    def match(dx, dy):
        C = C0.copy(); C["geometry"] = C.translate(dx, dy).buffer(R)
        j = gpd.sjoin(P, C, predicate="within", how="inner", lsuffix="p", rsuffix="c")
        j = j[(j.yr_c >= j.yr_p - 5) & (j.yr_c <= j.yr_p + 1)]
        return p.index.isin(j.index.unique())
    return match(0, 0), [match(dx, dy) for dx, dy in [(shift, 0), (-shift, 0), (0, shift), (0, -shift)]]


def rus_flags(p, eia_dir, rus_csv):
    r = pd.read_csv(rus_csv)
    r = r[~r.recipient.str.upper().str.contains("NATIONAL RURAL UTILITIES|NRUCFC|COBANK")]
    rn = set(r.recipient.map(norm)); rk = {k2(x) for x in rn}
    pl = pd.read_excel(os.path.join(eia_dir, "2___Plant_Y2025.xlsx"), header=1)[["Plant Code", "Utility Name"]]
    n = p[["Plant Code"]].merge(pl, on="Plant Code", how="left")["Utility Name"].map(norm)
    return (n.str.contains(COOP, regex=True) & (n.isin(rn) | n.map(k2).isin(rk))).values, dict(
        n_awards=int(len(r)), years=[str(pd.to_datetime(r.date).min().date()), str(pd.to_datetime(r.date).max().date())])


if __name__ == "__main__":
    eia, gdb, xlsx, rus_csv, eis_csv = sys.argv[1:6]
    p, _ = load_plants(eia); p = p.reset_index(drop=True)
    land = land_flags(p, gdb); ip, plac = corps_flags(p, xlsx); rus, rmeta = rus_flags(p, eia, rus_csv)
    out = {}
    for t, d in p.groupby("mt"):
        i = d.index.values; w = d.mw.values; s = lambda m: float((w * m[i]).sum() / w.sum())
        ip_placebo = float(np.mean([s(m) for m in plac]))
        r = dict(plants=int(len(d)), GW=float(w.sum() / 1000),
                 land_or_federal_BA=[s(land[0]), s(land[1000])], corps_individual_raw=s(ip), corps_placebo=ip_placebo,
                 corps_individual_net=max(s(ip) - ip_placebo, 0.0), rus_owned=s(rus))
        r["combined_net"] = [max(s(land[b] | ip | rus) - ip_placebo, s(land[b])) for b in (0, 1000)]
        if t == "Offshore wind":
            r["combined_net"] = [1.0, 1.0]; r["note"] = "federal by statute (OCS)"
        out[t] = r
    e = pd.read_csv(eis_csv)
    eis = {t: int(n) for t, n in e[e.year >= 2015].topic.value_counts().items()}
    res = dict(meta=dict(definition=__doc__.split("Usage")[0].strip(), rus=rmeta,
                         note="combined_net = share of MW with any hook, minus the Corps placebo rate; range = point vs 1 km buffer"),
               types=out, doe_eis_since_2015_by_topic=eis)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), "federal_nexus_combined.json"), "w"), indent=1)
    for t, r in out.items():
        print(f"{t:14s} combined {100*r['combined_net'][0]:5.1f}-{100*r['combined_net'][1]:5.1f}%  land/BA {100*r['land_or_federal_BA'][0]:4.1f}  Corps net {100*r['corps_individual_net']:4.1f}  RUS {100*r['rus_owned']:4.1f}")
