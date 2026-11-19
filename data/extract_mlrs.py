"""BLM MLRS solar development grant cases (user export, 770 cases): outcomes of solar right-of-way applications.

Usage: python data/extract_mlrs.py MLRS_CSV  -> data/mlrs_targets.json
The export has no filing/receipt date, so it cannot measure intake time (params `intake_pub`); serial numbers are
not a usable proxy (amendment suffixes, state formats). It gives outcomes: authorized / (authorized + closed) is the
share of resolved BLM solar applications that were granted. "Closed" mixes withdrawn, rejected and relinquished.
"""
import json, os, sys

import pandas as pd


def run(path):
    d = pd.read_csv(path, low_memory=False)
    d = d[d.commodity == "SOLAR ENERGY FACILITIES"].copy()
    d["yr"] = pd.to_datetime(d.disposition_date, errors="coerce").dt.year
    share = lambda g: {k: float(v) for k, v in g.disposition.value_counts(normalize=True).items()}
    res = lambda g: float((g.disposition == "AUTHORIZED").sum() / g.disposition.isin(["AUTHORIZED", "CLOSED"]).sum())
    return dict(n=int(len(d)), status_share=share(d), granted_share_of_resolved=res(d),
                by_state={s: dict(n=int(len(g)), granted_share_of_resolved=res(g) if g.disposition.isin(["AUTHORIZED", "CLOSED"]).any() else None)
                          for s, g in d.groupby("state")},
                median_acres={k: float(v) for k, v in d.groupby("disposition").acres.median().items()},
                authorized_by_year={int(y): int(n) for y, n in d[d.disposition == "AUTHORIZED"].groupby("yr").size().items()},
                note="no filing date in this export; request the case action history for intake time")


if __name__ == "__main__":
    out = run(sys.argv[1])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "mlrs_targets.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n", "status_share", "granted_share_of_resolved", "by_state", "median_acres")}, indent=1))
