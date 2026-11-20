"""Right-of-way intake time on federal land, from BLM MLRS solar development grant cases with filing dates
(user export: 459 cases; filing dates observed from case action reports or estimated from serial order).

Usage: python data/extract_mlrs_filing.py FILING_DATES_CSV  -> data/mlrs_filing_targets.json
Intake = filing date -> notice date (the notice that opens the public NEPA process). Cleaning, in order:
  1. base cases only (amendments carry a suffix such as "02" or "A"; their filing date is the amendment's)
  2. notice dates shared by more than 5 cases dropped (bulk notices, e.g. 2025-12-19, later than the grants)
  3. filed <= notice, and notice <= decision / grant when those exist
Central estimate uses observed filing dates; estimated ones are reported as a robustness check.
"""
import json, os, re, sys

import numpy as np
import pandas as pd

DATES = ["filed_date", "notice_date", "decision_date", "grant_date", "rejected_withdrawn_date", "disposition_date"]


def km_median(t, event):
    o = np.argsort(t); t, e = np.asarray(t)[o], np.asarray(event)[o]; n = len(t); S = 1.0
    for i in range(n):
        if e[i]:
            S *= 1 - 1 / (n - i)
        if S <= 0.5:
            return float(t[i])
    return None


def run(path, seed=0):
    d = pd.read_csv(path, low_memory=False)
    for c in DATES:
        d[c] = pd.to_datetime(d[c], errors="coerce")
    steps = {"all cases": len(d)}
    base = d[d.legacy_serial.astype(str).str.fullmatch(r"[A-Z]+ \d{6}")].copy()
    steps["base cases"] = len(base)
    shared = base.notice_date.value_counts(); bulk = set(shared[shared > 5].index)
    base.loc[base.notice_date.isin(bulk), "notice_date"] = pd.NaT
    mo = lambda a, b: (base[b] - base[a]).dt.days / 30.44
    base["intake"] = mo("filed_date", "notice_date")
    ok = base.intake.ge(0) & ~(base.decision_date.notna() & (base.notice_date > base.decision_date)) \
         & ~(base.grant_date.notna() & (base.notice_date > base.grant_date))
    obs = base[ok & (base.filed_source == "observed")]
    steps["with a valid notice (observed filing)"] = len(obs)
    est = base[ok]
    x = obs.intake.clip(lower=0.5)
    rng = np.random.default_rng(seed)
    boot = [np.median(rng.choice(x.values, len(x))) for _ in range(5000)]
    per = {lab: dict(n=int(len(g)), median=float(g.intake.median())) for lab, g in
           (("filed 2010-18", obs[obs.filed_date.dt.year <= 2018]), ("filed 2019-26", obs[obs.filed_date.dt.year >= 2019]))}
    # time to grant, pending cases censored at their last action
    g = base[base.filed_source == "observed"].copy()
    end = g.grant_date.fillna(g.disposition_date)
    t = (end - g.filed_date).dt.days / 30.44
    ev = g.grant_date.notna()
    keep = t.ge(0)
    out = dict(cleaning_steps=steps, bulk_notice_dates=[str(b.date()) for b in sorted(bulk)],
               intake_months=dict(n=int(len(x)), median=float(x.median()), log_sd=float(np.log(x).std()),
                                  p25=float(x.quantile(.25)), p75=float(x.quantile(.75)),
                                  median_ci90=[float(np.percentile(boot, 5)), float(np.percentile(boot, 95))]),
               intake_months_incl_estimated=dict(n=int(len(est)), median=float(est.intake.median())),
               intake_by_period=per,
               filed_to_decision_months=float(mo("filed_date", "decision_date")[base.filed_source == "observed"].dropna().clip(lower=0).median()),
               filed_to_grant_km_median_months=km_median(t[keep].values, ev[keep].values),
               n_granted=int(ev[keep].sum()), n_cases_for_km=int(keep.sum()))
    return out


if __name__ == "__main__":
    out = run(sys.argv[1])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "mlrs_filing_targets.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))
