"""BLM ePlanning energy NEPA register (user export, 2,594 actions) -> review type mix, durations and lawsuit rates.

Usage: python data/extract_blm_eplanning.py BLM_CSV NEPA_CASES_CSV DOE_EA_CSV  -> data/blm_eplanning_targets.json

  ea_share_nonEIS   EA / (EA + CE + DNA) among non-EIS actions. "project" = actions whose description mentions
                    >= 20 MW (proxy for a project approval rather than a minor action); "all" = every energy action
  median_months     NEPA start -> decision (or completion) by technology and review type, completed actions
  decisions_per_yr  BLM decisions 2012-2021 by technology and review type
  lit_rate          P(sued | review type) for court groups Renewable and Transmission:
                    district-court NEPA suits per year 2012-2021 (case-level export) /
                    (BLM decisions per year + DOE EAs per year for EAs). Suits against other agencies' reviews are in
                    the numerator but only BLM and DOE reviews in the denominator, so rates are upper-leaning.
"""
import json, os, re, sys

import pandas as pd

DOC = {"CE": "CE", "DNA": "CE", "EA": "EA", "EIS": "EIS", "RMP Amendment - EIS": "EIS", "RMP Amendment - EA": "EA"}
TECH = {"Solar": "Solar", "Wind": "Onshore wind", "Geothermal": "Geothermal", "Storage": "Storage", "Transmission": "Transmission"}
GROUP = {"Solar": "Renewable", "Onshore wind": "Renewable", "Geothermal": "Renewable", "Storage": "Renewable", "Transmission": "Transmission"}
Y0, Y1 = 2012, 2021


def blm(path):
    d = pd.read_csv(path, low_memory=False)
    d["dt"] = d.doc_type.map(DOC); d["t"] = d.technology.map(TECH)
    d = d[d.dt.notna() & d.t.notna()].copy()
    d["start"] = pd.to_datetime(d.start_date, errors="coerce")
    d["dec"] = pd.to_datetime(d.decision_date, errors="coerce").fillna(pd.to_datetime(d.nepa_completion_date, errors="coerce"))
    d["mo"] = (d.dec - d.start).dt.days / 30.44
    d["mw"] = pd.to_numeric(d.mw_mentions.astype(str).str.extract(r"([\d.]+)")[0], errors="coerce")
    ne = d[d.dt != "EIS"]; pj = ne[ne.mw >= 20]
    out = dict(n_actions=int(len(d)),
               ea_share_nonEIS=dict(project=float((pj.dt == "EA").mean()), n_project=int(len(pj)),
                                    all=float((ne.dt == "EA").mean()), n_all=int(len(ne)),
                                    by_tech_all={t: float((g.dt == "EA").mean()) for t, g in ne.groupby("t")}),
               median_months={}, decisions_per_yr={}, cancelled_share={})
    ok = d[d.mo.between(0.1, 240)]
    for t, g in ok.groupby("t"):
        out["median_months"][t] = {k: dict(median=float(v.mo.median()), n=int(len(v))) for k, v in g.groupby("dt")}
    w = d[d.dec.dt.year.between(Y0, Y1)]
    for t, g in w.groupby("t"):
        out["decisions_per_yr"][t] = {k: float(len(v) / (Y1 - Y0 + 1)) for k, v in g.groupby("dt")}
    for t, g in d.groupby("t"):
        out["cancelled_share"][t] = float(g.nepa_status.fillna("").str.startswith("Cancelled").mean())
    return out


def lit_rates(cases_csv, doe_ea_csv, dec):
    c = pd.read_csv(cases_csv, encoding_errors="replace", low_memory=False)
    c["yr"] = pd.to_datetime(c["Challenge Filed Date"], errors="coerce").dt.year
    c = c[c.yr.between(Y0, Y1) & ~c["Court Line"].fillna("").str.contains("Appeals")]
    ty, sub = c["Type (if applicable)"].fillna(""), c["Project Subcategory"].fillna("")
    c["grp"] = None
    c.loc[ty.isin(["Wind", "Solar", "Geothermal"]), "grp"] = "Renewable"
    c.loc[sub.eq("Transmission"), "grp"] = "Transmission"
    doc = c["Contested document type"].fillna("")
    e = pd.read_csv(doe_ea_csv)
    e = e[e.year.between(Y0, Y1)]
    kw = {"Renewable": r"solar|photovoltaic|\bwind\b|geotherm|battery|energy storage", "Transmission": r"transmission|\bkv\b|kilovolt|substation|power line"}
    out = {}
    yrs = Y1 - Y0 + 1
    for g in ("Renewable", "Transmission"):
        techs = [t for t, gg in GROUP.items() if gg == g]
        den = {k: sum(dec.get(t, {}).get(k, 0) for t in techs) for k in ("CE", "EA", "EIS")}
        doe = float(e.title.str.contains(kw[g], case=False, regex=True).sum() / yrs)
        den["EA"] += doe
        sel = c.grp == g
        suits = {k: float((sel & doc.str.contains(k)).sum() / yrs) for k in ("CE", "EA")}
        out[g] = dict(suits_per_yr=suits, reviews_per_yr=den, doe_ea_per_yr=doe,
                      lit_ea=suits["EA"] / den["EA"] if den["EA"] else None,
                      lit_ce=suits["CE"] / den["CE"] if den["CE"] else None)
    return out


if __name__ == "__main__":
    b = blm(sys.argv[1])
    b["lit_rate"] = lit_rates(sys.argv[2], sys.argv[3], b["decisions_per_yr"])
    b["meta"] = dict(source="BLM ePlanning NEPA register export (Lands and Realty energy keyword + Renewable Energy program)",
                     years_for_rates=[Y0, Y1], note="NEPA start date is after the right-of-way application, so intake time is not measured")
    json.dump(b, open(os.path.join(os.path.dirname(__file__), "blm_eplanning_targets.json"), "w"), indent=1)
    print(json.dumps({k: b[k] for k in ("ea_share_nonEIS", "median_months", "lit_rate", "cancelled_share")}, indent=1))
