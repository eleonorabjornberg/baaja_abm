"""Investor-owned share of retail electricity sales by model region, EIA-861 (2025), for Sec.2109's scope.

Usage: python -I data/extract_pu_share.py EIA861_ZIP   -> data/pu_share.json

BAAJA Sec.2109 adds FPA s.232, whose subsection (d) applies "only to public utilities". The FPA's public utilities
are, for transmission, mainly investor-owned utilities; municipal, state, federal and most cooperative systems are not.
As a proxy for the share of a region's new transmission that s.232 reaches, this takes the investor-owned share of
retail sales delivered over each utility's own wires (EIA-861 Sales to Ultimate Customers, service types Bundled and
Delivery, which count each MWh once, by its wires utility; rows reported by retail marketers, as in Texas, and
behind-the-meter rows are left out because their wires utility is not given). Rows are assigned to a region by balancing authority code
(CISO, ERCO, ISNE, MISO, NYIS, PJM, SWPP); other rows go to West (western states) or Southeast (the rest).
ERCOT's utilities are intrastate and outside FERC's FPA jurisdiction over transmission, so ERCOT's share is set to 0
(my reading). Its computed share in `detail` is not meaningful: Texas retail sales are reported by retail marketers,
whose rows are left out.
"""
import io, json, os, sys, zipfile

import pandas as pd

BA = {"CISO": "CAISO", "ERCO": "ERCOT", "ISNE": "ISO-NE", "MISO": "MISO", "NYIS": "NYISO", "PJM": "PJM", "SWPP": "SPP"}
WEST = {"WA", "OR", "ID", "MT", "WY", "NV", "UT", "CO", "AZ", "NM", "CA"}
REGIONS = ["CAISO", "ERCOT", "ISO-NE", "MISO", "NYISO", "PJM", "SPP", "Southeast", "West"]


def run(path):
    z = zipfile.ZipFile(path)
    d = pd.read_excel(io.BytesIO(z.read("Sales_Ult_Cust_2025.xlsx")), sheet_name="States", header=2)
    d = d.rename(columns={"Megawatthours.4": "mwh"})
    d = d[d["Service Type"].isin(["Bundled", "Delivery"])
          & ~d["Ownership"].isin(["Retail Power Marketer", "Behind the Meter"])].copy()   # wires utility unknown
    d["mwh"] = pd.to_numeric(d["mwh"], errors="coerce").fillna(0.0)
    d["region"] = [BA.get(b, "West" if s in WEST else "Southeast") for b, s in zip(d["BA Code"], d["State"])]
    d["iou"] = d["Ownership"] == "Investor Owned"
    out = {}
    for r in REGIONS:
        g = d[d.region == r]
        out[r] = dict(iou_share=float(g.loc[g.iou, "mwh"].sum() / g.mwh.sum()), twh=float(g.mwh.sum() / 1e6))
    share = {r: (0.0 if r == "ERCOT" else round(v["iou_share"], 3)) for r, v in out.items()}
    return dict(meta=dict(source="EIA-861 2025, Sales_Ult_Cust_2025.xlsx (States), Bundled + Delivery",
                          note=__doc__.split("\n\n")[2].replace("\n", " ")),
                share=share, detail=out)


if __name__ == "__main__":
    res = run(sys.argv[1])
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pu_share.json"), "w"), indent=1)
    for r, v in res["detail"].items():
        print(f"{r:10s} IOU share {v['iou_share']:.3f}  {v['twh']:.0f} TWh  used {res['share'][r]}")
