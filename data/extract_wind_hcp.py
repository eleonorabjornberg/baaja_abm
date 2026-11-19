"""Wind habitat conservation plans (ESA s.10 incidental take permits, each with project-level NEPA) matched to
EIA-860 wind plants online 2015-2025, to add to the onshore wind federal nexus.

Usage: python data/extract_wind_hcp.py DRYAD_FILES_JSON EIA860_DIR  -> data/wind_hcp_targets.json
  DRYAD_FILES_JSON  file listing of Dryad doi:10.5061/dryad.59zw3r2kf (wind-bat HCPs through 2022), from
                    https://datadryad.org/api/v2/versions/354663/files (the CSV itself needs a login; the PDF names
                    identify the projects)
Match: the first two distinctive words of the HCP project name appear in the EIA plant name. The added share counts
only plants without another federal hook (land, federal BA, Corps, RUS; see combine_federal_hooks.py), using the
EIA plant-point definition. Eagle specific permits are not included (FWS publishes no list).
"""
import json, os, re, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from extract_federal_nexus import load_plants  # noqa: E402

STOP = {"wind", "hcp", "draft", "farm", "farms", "energy", "facility", "facilities", "project", "center", "resource", "area",
        "llc", "county", "counties", "and", "the", "ii", "iii", "iv", "of", "indiana", "ohio", "illinois", "illino", "pennsylvania"}
toks = lambda s: [w for w in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("_", " ")).split() if w not in STOP and len(w) > 2]


def run(files_json, eia_dir):
    f = json.load(open(files_json))["_embedded"]["stash:files"]
    hcp = [(x["path"][:-4], toks(x["path"][:-4])) for x in f if x["path"].lower().endswith(".pdf")]
    p, _ = load_plants(eia_dir)
    pl = pd.read_excel(os.path.join(eia_dir, "2___Plant_Y2025.xlsx"), header=1)[["Plant Code", "Plant Name"]]
    w = p[p.mt == "Onshore wind"].merge(pl, on="Plant Code", how="left")

    def match(name):
        t = set(toks(str(name)))
        return next((n for n, k in hcp if k and set(k[:2]) <= t), None)
    w["hcp"] = w["Plant Name"].map(match)
    m = w[w.hcp.notna()]
    return dict(n_hcp_documents=len(hcp), matched_plants=int(len(m)), matched_GW=float(m.mw.sum() / 1000),
                wind_GW_2015_25=float(w.mw.sum() / 1000), hcp_share_MW=float(m.mw.sum() / w.mw.sum()),
                plants=m[["Plant Name", "State", "mw", "hcp"]].to_dict("records"))


if __name__ == "__main__":
    out = run(sys.argv[1], sys.argv[2])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "wind_hcp_targets.json"), "w"), indent=1, default=float)
    print({k: v for k, v in out.items() if k != "plants"})
