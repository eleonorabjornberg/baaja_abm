"""Court parameters from a case-level NEPA litigation export (nepa-export.csv; 1,821 district and appellate cases,
filed 2001-2022, with plaintiff types, project category/type, document type, dates and remedies).
The raw file is user-supplied and not committed.

Usage: python data/extract_nepa_cases.py path/to/nepa-export.csv   -> data/nepa_case_targets.json

Mapping to the model:
  technology group  Type == Wind/Solar/Geothermal -> renewable; Hydroelectric -> hydro; Subcategory Transmission;
                    Subcategory Fossil fuel infrastructure (pipelines, LNG, compressors) -> fossil proxy (the data has
                    no gas power-plant cases; gas generation rarely has a federal nexus)
  lead challenger   first-listed plaintiff type; NGO split into national vs local/regional by the first plaintiff's
                    name (NATIONAL list below); Individual(s)/Neighborhood group/HOA/Church -> local group/residents;
                    State, Local government -> government; Company, Industry association/group, Union -> business
  outcomes          challenger win = 'Prev Agency on NEPA claim' == Challenger; vacatur share among remands;
                    injunction share; days_in_litigation; days_to_litigation_start (decision -> filing)
"""
import json, os, sys

import numpy as np
import pandas as pd

NATIONAL = ["center for biological diversity", "sierra club", "wildearth guardians", "western watersheds project",
            "natural resources defense council", "national wildlife federation", "national parks conservation association",
            "earth island institute", "greenpeace", "defenders of wildlife", "oceana", "humane society",
            "friends of the earth", "earthjustice", "environmental defense fund", "the wilderness society",
            "american bird conservancy", "food & water watch", "food and water watch", "public citizen", "wilderness watch",
            "friends of animals", "american rivers", "center for food safety", "union of concerned scientists",
            "indigenous environmental network", "american wild horse", "national audubon society", "public employees for environmental responsibility"]
CH = ["National NGO", "Local group / residents", "Tribe", "State / local government", "Business"]
LOCAL = {"Individual(s)", "Individuals", "Neighborhood group", "Neighborhood Group", "HOA", "Church", "University"}
GOV = {"State", "Local government"}
BUS = {"Company", "Industry association", "Industry group", "Union"}


def lead_type(ptype, plaintiffs):
    t = str(ptype).split(";")[0].strip(); name = str(plaintiffs).split(";")[0].strip().lower()
    if t == "NGO":
        national = any(k in name for k in NATIONAL) and "local chapter" not in name
        return "National NGO" if national else "Local group / residents"
    if t in LOCAL: return "Local group / residents"
    if t == "Tribal": return "Tribe"
    if t in GOV: return "State / local government"
    if t in BUS: return "Business"
    return None


def group(row):
    ty, sub = str(row["Type (if applicable)"]), str(row["Project Subcategory"])
    if ty in ("Wind", "Solar", "Geothermal"): return "Renewable"
    if ty == "Hydroelectric": return "Hydro"
    if sub == "Transmission": return "Transmission"
    if sub == "Fossil fuel infrastructure": return "Fossil infrastructure"
    if row["Project Category"] == "Energy": return "Other energy"
    return "Non-energy"


def stats(x):
    win = x["Prev Agency on NEPA claim"].eq("Challenger")
    vac, novac = x["Remand W/ Vacatur"].eq("Yes"), x["Remand W/O Vacatur"].eq("Yes")
    s = x.days_to_litigation_start.dropna()
    return dict(n=int(len(x)), n_district=int((~x["Court Line"].fillna("").str.contains("Appeals")).sum()),
                challenger_win=float(win[x["Prev Agency on NEPA claim"].notna()].mean()),
                injunction_share=float(x["Injunctive Relief"].eq("Yes").mean()),
                vacatur_share_of_remands=float(vac.sum() / max((vac | novac).sum(), 1)), n_remands=int((vac | novac).sum()),
                median_months_in_litigation=float(x.days_in_litigation.median() / 30.44),
                n_filing_delay=int(len(s)), share_filed_after_150_days=float((s > 150).mean()) if len(s) else None,
                median_days_decision_to_filing=float(s.median()) if len(s) else None,
                doc_share={k: float(x["Contested document type"].fillna("").str.contains(k).mean()) for k in ("CE", "EA", "EIS")},
                lead_mix={c: float((x.lead == c).mean()) for c in CH})


if __name__ == "__main__":
    d = pd.read_csv(sys.argv[1], encoding_errors="replace", low_memory=False)
    d["lead"] = [lead_type(t, p) for t, p in zip(d["Plaintiff type"], d["Plaintiffs"])]
    d["grp"] = d.apply(group, axis=1)
    win = d["Prev Agency on NEPA claim"].eq("Challenger"); known = d["Prev Agency on NEPA claim"].notna()
    by_ch = {}
    for c in CH:
        m = d.lead == c; s = d.days_to_litigation_start[m].dropna()
        by_ch[c] = dict(n=int(m.sum()), win_rate=float(win[m & known].mean()),
                        share_filed_after_150_days=float((s > 150).mean()), n_filing_delay=int(len(s)))
    allwin = float(win[known].mean())
    for c in CH:
        by_ch[c]["win_rel"] = by_ch[c]["win_rate"] / allwin
    out = dict(meta=dict(n_cases=int(len(d)), filed_years=[int(pd.to_datetime(d["Challenge Filed Date"], errors="coerce").dt.year.min()),
                                                          int(pd.to_datetime(d["Challenge Filed Date"], errors="coerce").dt.year.max())],
                         all_case_challenger_win=allwin, unmapped_lead=int(d.lead.isna().sum())),
               by_group={g: stats(x) for g, x in d.groupby("grp")}, by_lead_challenger=by_ch,
               energy=stats(d[d["Project Category"] == "Energy"]))
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "nepa_case_targets.json"), "w"), indent=1)
    print(json.dumps(out["by_lead_challenger"], indent=1))
    for g in ("Renewable", "Hydro", "Transmission", "Fossil infrastructure"):
        v = out["by_group"][g]; print(g, v["n"], {k: round(x, 2) for k, x in v["lead_mix"].items()})
