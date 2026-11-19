"""Summaries from three user-supplied files (raw files are not committed):

  corps   USACE ORM final individual permits export (Export.xlsx; 60k Standard Permits and Letters of Permission,
          2008-2026, with coordinates). Matched to EIA-860 plants online 2015-2025: a plant "has an individual
          s.404/s.10 permit" if a permit lies within 2 km and was decided between 5 years before and 1 year after
          the plant's first operating year. Placebo: the same match with permits shifted 20 km N/S/E/W; the net
          share (real - placebo) is the estimate. Needs the EIA-860 directory (see extract_federal_nexus.py).
  doe_ea  DOE environmental assessments list (nepa_doe_environmental_assessments.csv), classified by title.
  sabin   Sabin Center 2026 contested renewable projects and local/state restrictions (CSV exports).

Usage: python data/extract_permits_opposition.py EXPORT_XLSX DOE_EA_CSV CONTESTED_CSV RESTRICTIONS_CSV EIA860_DIR
Writes data/permits_opposition_targets.json
"""
import json, os, re, sys

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from extract_federal_nexus import load_plants  # noqa: E402


def corps(path, eia_dir, R=2000, shift=20000):
    c = pd.read_excel(path)
    c["yr"] = pd.to_datetime(c["Date Issued/Denied"], errors="coerce").dt.year
    c = c.dropna(subset=["Longitude", "Latitude", "yr"])
    c = c[c.Latitude.between(17, 72) & c.Longitude.between(-180, -60)]
    p, _ = load_plants(eia_dir); p = p.reset_index(drop=True)
    P = gpd.GeoDataFrame(p, geometry=gpd.points_from_xy(p.Longitude, p.Latitude), crs=4326).to_crs(5070)
    C0 = gpd.GeoDataFrame(c[["yr"]], geometry=gpd.points_from_xy(c.Longitude, c.Latitude), crs=4326).to_crs(5070)

    def match(dx, dy):
        C = C0.copy(); C["geometry"] = C.translate(dx, dy).buffer(R)
        j = gpd.sjoin(P[["yr", "geometry"]], C, predicate="within", how="inner", lsuffix="p", rsuffix="c")
        j = j[(j.yr_c >= j.yr_p - 5) & (j.yr_c <= j.yr_p + 1)]
        return p.index.isin(j.index.unique())

    real = match(0, 0)
    plac = [match(dx, dy) for dx, dy in [(shift, 0), (-shift, 0), (0, shift), (0, -shift)]]
    out = {}
    for t, d in p.groupby("mt"):
        i = d.index; w = d.mw.values
        mw = lambda m: float((w * m[i]).sum() / w.sum())
        pm = float(np.mean([mw(m) for m in plac]))
        out[t] = dict(plants=int(len(d)), share_MW=mw(real), placebo_share_MW=pm, net_share_MW=max(mw(real) - pm, 0.0),
                      share_plants=float(real[i].mean()), placebo_share_plants=float(np.mean([m[i].mean() for m in plac])))
    return dict(n_permits=int(len(c)), years=[int(c.yr.min()), int(c.yr.max())], types=out)


def doe_ea(path):
    d = pd.read_csv(path)
    def cls(s):
        s = str(s).lower()
        if "geotherm" in s: return "Geothermal"
        if re.search(r"solar|photovoltaic", s): return "Solar"
        if "offshore wind" in s: return "Offshore wind"
        if re.search(r"\bwind\b", s): return "Onshore wind"
        if re.search(r"battery|energy storage|bess", s): return "Storage"
        if re.search(r"transmission|\bkv\b|kilovolt|substation|interconnection|power line", s): return "Transmission"
        if re.search(r"natural gas|combined.cycle|gas.fired|generating station|power plant", s): return "Gas/other generation"
        return None
    d["tech"] = d.title.map(cls)
    w = d[d.year.between(2015, 2024)]
    return dict(n=int(len(d)), years=[int(d.year.min()), int(d.year.max())],
                ea_per_year_2015_24={t: float(n / 10) for t, n in w.groupby("tech").size().items()},
                by_office={t: {o: int(n) for o, n in g.groupby("office").size().items()} for t, g in d.groupby("tech")})


def sabin(contested, restrictions):
    k = pd.read_csv(contested, encoding_errors="replace"); r = pd.read_csv(restrictions, encoding_errors="replace")
    k["T"] = k.Type.str.split("|").str[0]
    v = k["Litigation Venue"].fillna("")
    k["fed"] = v.str.contains("Federal"); k["state_admin"] = v.str.contains("State|Administrative") & ~k.fed
    out = {}
    for t, g in k.groupby("T"):
        out[t] = dict(contested=int(len(g)), litigated=int((g.Litigation == "Yes").sum()),
                      federal_venue=int(g.fed.sum()), state_or_admin_only=int(g.state_admin.sum()),
                      canceled=int((g.Status == "Canceled").sum()), pending=int((g.Status == "Pending").sum()))
    return dict(contested_by_type=out, contested_by_last_event_year={int(y): int(n) for y, n in k["Date of Last Event"].value_counts().sort_index().items()},
                restrictions=dict(n=int(len(r)), by_level=r.Level.value_counts().to_dict(), by_type=r.Type.value_counts().to_dict(),
                                  by_year_adopted={int(y): int(n) for y, n in r["Year Adopted"].dropna().value_counts().sort_index().items()}),
                note="renewables, storage and transmission only; no fossil projects in the Sabin data")


if __name__ == "__main__":
    xlsx, ea, con, res, eia = sys.argv[1:6]
    out = dict(corps_individual_permits=corps(xlsx, eia), doe_environmental_assessments=doe_ea(ea), sabin=sabin(con, res))
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "permits_opposition_targets.json"), "w"), indent=1)
    print(json.dumps(out["corps_individual_permits"]["types"], indent=1)); print(json.dumps(out["sabin"]["contested_by_type"], indent=1))
