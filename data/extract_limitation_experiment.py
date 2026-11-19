"""Natural experiment for BAAJA's 150-day filing limit (Sec.1110, 2201): do challengers file sooner when a short
statute of limitations applies?

Highway and transit approvals (FHWA/FTA) have had a short limit since SAFETEA-LU (2005: 180 days after a Federal
Register notice), cut to 150 days by MAP-21 (from Oct 2012). Other NEPA approvals fall under the APA's 6-year default.
Using the case-level NEPA export (district courts, days from decision to filing), compare the two filing-delay
distributions.

Adaptation estimate: late_adapt = 1 - (share of highway suits filed after cutoff) / (share of other suits filed after
cutoff), where the cutoff allows for the gap between the decision and the Federal Register notice that starts the
clock. Central cutoff 240 days (150-180 day limit + 60-90 day notice lag); range from cutoffs 210-300 days. Highway
suits filed late include approvals with no published notice (6-year limit), so the estimate is a lower bound; the
upper end of the range is set to 1.0.

Usage: python data/extract_limitation_experiment.py path/to/nepa-export.csv  -> data/limitation_experiment.json
"""
import json, os, sys

import numpy as np
import pandas as pd

BINS = [0, 60, 120, 150, 180, 210, 240, 300, 365, 730, 100000]


def run(path):
    d = pd.read_csv(path, encoding_errors="replace", low_memory=False)
    ag = d["Agency whose document is being challenged"].fillna(""); sub = d["Project Subcategory"].fillna("")
    d["hwy"] = sub.isin(["Highway/bridge", "Transit"]) | ag.str.contains(r"FHWA|FTA", regex=True)
    k = d[d.days_to_litigation_start.notna() & ~d["Court Line"].fillna("").str.contains("Appeals") & (d.days_to_litigation_start >= 0)]
    v_h, v_o = k.days_to_litigation_start[k.hwy], k.days_to_litigation_start[~k.hwy]
    late = lambda v, c: float((v > c).mean())
    est = {c: 1 - late(v_h, c) / late(v_o, c) for c in (210, 240, 300)}
    hist = {f"{a}-{b}": dict(other=float(((v_o > a) & (v_o <= b)).mean()), highway=float(((v_h > a) & (v_h <= b)).mean()))
            for a, b in zip(BINS[:-1], BINS[1:])}
    return dict(n_highway=int(len(v_h)), n_other=int(len(v_o)), histogram_days=hist,
                share_filed_after={c: dict(other=late(v_o, c), highway=late(v_h, c)) for c in (150, 210, 240, 300, 365)},
                late_adapt_by_cutoff=est,
                late_adapt=dict(low=float(min(est.values())), central=float(est[240]), high=1.0),
                note="lower-bound estimate: late highway suits include approvals without a published notice")


if __name__ == "__main__":
    out = run(sys.argv[1])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "limitation_experiment.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_highway", "n_other", "share_filed_after", "late_adapt_by_cutoff", "late_adapt")}, indent=1))
