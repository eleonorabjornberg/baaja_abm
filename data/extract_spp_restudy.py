"""Re-study evidence from SPP's Definitive Interconnection System Impact Study (DISIS) result workbooks.

Usage: python -I data/extract_spp_restudy.py SPP_WORKBOOK_DIR [SPP_WORKBOOK_DIR ...]  -> data/spp_restudy.json

SPP posts one results workbook per cluster and posting (Phase 1, Phase 2, then Restudy 1, 2, ...), each listing the
requests still in the cluster ("Requests") and the network and interconnection cost allocated to each request, by
upgrade ("Assigned Upgrade Costs"). Comparing successive postings of the same cluster gives, for each step:

  wsh      MW share of the cluster's requests in posting k that are gone by posting k+1 (withdrawn or moved out)
  ratio    total cost allocated to the requests present in both postings, k+1 over k
  dlog     per-request change in log allocated cost ($/kW, floor $1/kW), requests present in both
  months   months between the two postings (last date in each workbook's revision history)

The model's re-study round (baaja/grid.py, decide) raises the cost of every remaining request by
restudy_rho x wsh, so rho is estimated as the slope of (ratio - 1) on wsh across steps, through the origin and with
an intercept. Requests are matched on SPP's Gen Number; affected-system entries (ASGI-) and requests from earlier
clusters modelled in a posting are excluded by keeping only requests with the cluster's own queue label (e.g.
DIS-18-1) in its first posting.
Stability-only and sensitivity workbooks are skipped.
"""
import glob, json, os, re, sys

import numpy as np
import openpyxl

LABEL = {"1602": {"DIS-16-2"}, "1701": {"DIS-17-1"}, "1702": {"DIS-17-2"}, "1801": {"DIS-18-1"},
         "1802_1901": {"DIS-18-2", "DIS-19-1"}, "2001": {"DIS-20-1"}, "2101": {"DIS-21-1"}, "2201": {"DIS-22-1"},
         "2301": {"DIS-23-1"}}
SKIP = re.compile(r"Stability-Final|Stability_SC-Final_r4|Sensitivity|DIS1601-5", re.I)


def cluster_and_stage(fn):
    n = fn.replace(" ", "_")
    m = re.search(r"(?:DIS|Workbook_)(1602|1701|1702|1801|1802_?1901|2001|2021|2101|2201|2301|2023)[-_]?((?:P[12])|(?:-?\d)|(?:Re))", n)
    if not m:
        return None, None
    c = {"18021901": "1802_1901", "2021": "2101", "2023": "2301"}.get(m.group(1).replace("_", ""), m.group(1).replace("_", ""))
    if c == "1802_1901" or c == "18021901":
        c = "1802_1901"
    s = m.group(2).lstrip("-")
    s = {"P1": "P1", "P2": "P2", "Re": "R1"}.get(s, "R" + s if s.isdigit() else s)
    if c == "1602":                     # DISIS-2016-002: only restudies 2-4 have workbooks
        s = "R" + re.search(r"1602-(\d)", n).group(1)
    return c, s


def qlabel(x):
    """'DISIS-2017-002' and 'DIS-17-2' name the same cluster."""
    s = str(x).strip()
    m = re.match(r"DISIS-20(\d\d)-00(\d)$", s)
    return f"DIS-{m.group(1)}-{m.group(2)}" if m else s


def num(x):
    if x is None:
        return 0.0
    if isinstance(x, (int, float)):
        return float(x)
    s = re.sub(r"[$,\s]", "", str(x))
    try:
        return float(s)
    except ValueError:
        return 0.0


def header(ws, keys, maxrow=6):
    for i, r in enumerate(ws.iter_rows(values_only=True, max_row=maxrow)):
        h = [str(x).strip() if x is not None else "" for x in r]
        if all(any(k.lower() == c.lower() for c in h) for k in keys):
            return i, h
    return None, None


def read_posting(f):
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    req = wb[[n for n in wb.sheetnames if n.strip().lower() == "requests"][0]]
    i, h = header(req, ["Gen Number", "MW Amount"])
    gi, mi, fi = h.index("Gen Number"), h.index("MW Amount"), h.index("Fuel Type") if "Fuel Type" in h else None
    qi = h.index("Queue")
    reqs = {}
    for r in req.iter_rows(values_only=True, min_row=i + 2):
        g = str(r[gi]).strip() if r[gi] is not None else ""
        if not g.upper().startswith("GEN-"):
            continue
        reqs[g] = dict(mw=num(r[mi]), fuel=str(r[fi]).strip() if fi is not None else "", queue=qlabel(r[qi]))
    auc = wb[[n for n in wb.sheetnames if n.strip().lower().startswith("assigned upgrade cost")][0]]
    i, h = header(auc, ["Gen Number", "Allocated Cost"])
    gi, ai, ti = h.index("Gen Number"), h.index("Allocated Cost"), h.index("Upgrade Type")
    cost = {g: dict(total=0.0, network=0.0) for g in reqs}
    for r in auc.iter_rows(values_only=True, min_row=i + 2):
        g = str(r[gi]).strip() if r[gi] is not None else ""
        if g not in cost:
            continue
        a = num(r[ai]); t = str(r[ti]).strip().lower() if r[ti] is not None else ""
        cost[g]["total"] += a
        if t != "interconnection":
            cost[g]["network"] += a
    rh = [n for n in wb.sheetnames if n.lower().startswith("revision hist")]
    dates = [c for r in wb[rh[0]].iter_rows(values_only=True) for c in r if hasattr(c, "year")] if rh else []
    m = re.search(r"(\d{2})[_]?(\d{2})[_]?(20\d{2})", os.path.basename(f))
    date = max(dates) if dates else None
    return reqs, cost, (date.strftime("%Y-%m-%d") if date else None)


def months(a, b):
    ya, ma, da = map(int, a.split("-")); yb, mb, db = map(int, b.split("-"))
    return (yb - ya) * 12 + (mb - ma) + (db - da) / 30.44


def fit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    thru0 = float((x * y).sum() / (x * x).sum()) if (x * x).sum() > 0 else float("nan")
    A = np.c_[np.ones_like(x), x]
    b, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ b
    s2 = (res ** 2).sum() / max(len(x) - 2, 1)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A))) if len(x) > 2 else [float("nan")] * 2
    return dict(slope_through_origin=thru0, intercept=float(b[0]), slope=float(b[1]), se_intercept=float(se[0]),
                se_slope=float(se[1]), n=int(len(x)))


def run(dirs):
    files = sorted(f for d in dirs for f in glob.glob(os.path.join(d, "*.xlsx")) if not SKIP.search(os.path.basename(f)))
    posts = {}
    for f in files:
        c, s = cluster_and_stage(os.path.basename(f))
        if c is None:
            print("skip (unrecognised):", os.path.basename(f), file=sys.stderr); continue
        reqs, cost, date = read_posting(f)
        if not reqs:
            print("skip (no requests):", os.path.basename(f), file=sys.stderr); continue
        posts.setdefault(c, []).append(dict(file=os.path.basename(f), stage=s, date=date, reqs=reqs, cost=cost))
    steps, clusters, pairs, posts_by = [], {}, [], {}
    for c, P in sorted(posts.items()):
        P.sort(key=lambda p: (p["date"] or "", p["file"]))
        # one posting per stage: the last one dated in that stage (later reposts supersede)
        by = {}
        for p in P:
            by[p["stage"]] = p
        order = sorted(by.values(), key=lambda p: p["date"] or "")
        posts_by[c] = {p["stage"]: p for p in order}
        base = {g for g, v in order[0]["reqs"].items() if v["queue"] in LABEL[c]}
        clusters[c] = dict(postings=[dict(stage=p["stage"], date=p["date"], file=p["file"],
                                          n=len(set(p["reqs"]) & base),
                                          mw=sum(p["reqs"][g]["mw"] for g in set(p["reqs"]) & base)) for p in order])
        for a, b in zip(order[:-1], order[1:]):
            A = set(a["reqs"]) & base; B = set(b["reqs"]) & base
            stay = A & B
            mwA = sum(a["reqs"][g]["mw"] for g in A)
            if mwA <= 0 or not stay:
                continue
            wsh = sum(a["reqs"][g]["mw"] for g in A - B) / mwA
            for kind in ("total", "network"):
                ca = sum(a["cost"][g][kind] for g in stay); cb = sum(b["cost"][g][kind] for g in stay)
                kw = np.array([a["reqs"][g]["mw"] * 1000 for g in stay])
                pa = np.array([a["cost"][g][kind] for g in stay]) / np.maximum(kw, 1)
                pb = np.array([b["cost"][g][kind] for g in stay]) / np.maximum(kw, 1)
                dl = np.log(np.maximum(pb, 1.0)) - np.log(np.maximum(pa, 1.0))
                if kind == "total":
                    pairs += [dict(cluster=c, step=f"{a['stage']}->{b['stage']}", a=float(x), b=float(y))
                              for x, y in zip(pa, pb)]
                steps.append(dict(cluster=c, step=f"{a['stage']}->{b['stage']}", date_a=a["date"], date_b=b["date"],
                                  months=months(a["date"], b["date"]) if a["date"] and b["date"] else None,
                                  kind=kind, n_a=len(A), n_stay=len(stay), mw_a=mwA, wsh=wsh,
                                  cost_a=ca, cost_b=cb, ratio=cb / ca if ca > 0 else None,
                                  usd_kw_a=ca / max(kw.sum(), 1), usd_kw_b=cb / max(kw.sum(), 1),
                                  dlog_median=float(np.median(dl)), dlog_mean=float(dl.mean()),
                                  share_up10=float((dl > np.log(1.1)).mean()),
                                  share_down10=float((dl < -np.log(1.1)).mean())))
    out = dict(meta=dict(source="SPP OpsPortal, Generator Interconnection Studies, DISIS results workbooks "
                                "(https://opsportal.spp.org/Studies/Gen)", note=__doc__.split("\n\n")[1]),
               clusters=clusters, steps=steps, fit={})
    for kind in ("total", "network"):
        S = [s for s in steps if s["kind"] == kind and s["ratio"] is not None]
        out["fit"][kind] = fit([s["wsh"] for s in S], [s["ratio"] - 1 for s in S])
        S1 = [s for s in S if s["step"].startswith("P1->")]
        out["fit"][kind + "_P1_only"] = fit([s["wsh"] for s in S1], [s["ratio"] - 1 for s in S1]) if len(S1) > 2 else None
        w = np.array([s["mw_a"] for s in S])
        out["fit"][kind]["pooled_ratio_minus_1_over_pooled_wsh"] = float(
            (sum(s["cost_b"] for s in S) / sum(s["cost_a"] for s in S) - 1) / (w @ np.array([s["wsh"] for s in S]) / w.sum()))
    # request-level spread of re-study cost changes, $/kW, stayers only
    disp = {}
    for lab, sel in (("P1->P2", lambda q: q["step"] == "P1->P2"), ("after P2", lambda q: not q["step"].startswith("P1"))):
        Q = [q for q in pairs if sel(q)]
        pos = np.array([np.log(q["b"] / q["a"]) for q in Q if q["a"] > 1 and q["b"] > 1])
        disp[lab] = dict(n=len(Q), n_pos_both=int(len(pos)),
                         share_zero_both=float(np.mean([q["a"] <= 1 and q["b"] <= 1 for q in Q])),
                         share_zero_to_pos=float(np.mean([q["a"] <= 1 < q["b"] for q in Q])),
                         share_pos_to_zero=float(np.mean([q["b"] <= 1 < q["a"] for q in Q])),
                         dlog_sd=float(pos.std()), dlog_mean=float(pos.mean()), dlog_median=float(np.median(pos)),
                         dlog_q10_q90=[float(np.quantile(pos, .1)), float(np.quantile(pos, .9))],
                         share_up10=float((pos > np.log(1.1)).mean()), share_down10=float((pos < -np.log(1.1)).mean()),
                         robust_sd=float((np.quantile(pos, .75) - np.quantile(pos, .25)) / 1.349))
    out["dispersion"] = disp
    # per cluster, first complete study (Phase 2) to the latest posting: the round a single decision point removes
    P2, cum = {}, []
    for c, v in clusters.items():
        st = [p["stage"] for p in v["postings"]]
        if "P2" in st and st.index("P2") < len(st) - 1:
            a = v["postings"][st.index("P2")]; b = v["postings"][-1]
            P2[c] = dict(months=months(a["date"], b["date"]), mw_share_withdrawn=1 - b["mw"] / a["mw"])
            pa_, pb_ = posts_by[c][a["stage"]], posts_by[c][b["stage"]]
            base = {g for g, x in pa_["reqs"].items() if x["queue"] in LABEL[c]}
            for g in base & set(pb_["reqs"]):
                kw = pa_["reqs"][g]["mw"] * 1000
                if kw > 0:
                    cum.append((pa_["cost"][g]["total"] / kw, pb_["cost"][g]["total"] / kw))
    out["after_P2"] = dict(by_cluster=P2, months_median=float(np.median([x["months"] for x in P2.values()])),
                           months_min=float(min(x["months"] for x in P2.values())),
                           months_max=float(max(x["months"] for x in P2.values())),
                           withdrawn_median=float(np.median([x["mw_share_withdrawn"] for x in P2.values()])))
    a_ = np.array([x for x, _ in cum]); b_ = np.array([y for _, y in cum])
    pos = (a_ > 1) & (b_ > 1); d = np.log(b_[pos] / a_[pos]); ch = np.abs(d) > np.log(1.01)
    out["after_P2"]["cumulative"] = dict(
        n=int(len(cum)), share_zero_both=float(((a_ <= 1) & (b_ <= 1)).mean()),
        share_zero_to_pos=float(((a_ <= 1) & (b_ > 1)).mean()), share_pos_to_zero=float(((a_ > 1) & (b_ <= 1)).mean()),
        n_pos_both=int(pos.sum()), share_changed_1pct=float(ch.mean()), dlog_sd_changed=float(d[ch].std()),
        dlog_mean_changed=float(d[ch].mean()), dlog_median_changed=float(np.median(d[ch])),
        share_up10=float((d > np.log(1.1)).mean()), share_down10=float((d < -np.log(1.1)).mean()),
        dlog_sd=float(d.std()), dlog_q=[float(np.quantile(d, q)) for q in (.1, .25, .5, .75, .9)])
    S = [s for s in steps if s["kind"] == "total"]
    first = {}
    for s in S:
        first.setdefault(s["cluster"], s)
    out["timing"] = dict(
        months_P1_to_last=dict((c, months(v["postings"][0]["date"], v["postings"][-1]["date"])) for c, v in clusters.items()
                               if len(v["postings"]) > 1 and v["postings"][0]["stage"] == "P1"),
        months_per_step_median=float(np.median([s["months"] for s in S if s["months"] is not None])),
        wsh_P1_to_P2=dict((s["cluster"], s["wsh"]) for s in S if s["step"] == "P1->P2"),
        mw_share_remaining_at_last=dict((c, v["postings"][-1]["mw"] / v["postings"][0]["mw"]) for c, v in clusters.items()
                                        if v["postings"][0]["stage"] == "P1" and v["postings"][0]["mw"] > 0))
    return out


if __name__ == "__main__":
    res = run(sys.argv[1:])
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(res, open(os.path.join(here, "spp_restudy.json"), "w"), indent=1, default=float)
    for s in res["steps"]:
        if s["kind"] == "total":
            print(f"{s['cluster']:10s} {s['step']:8s} {s['date_a']}->{s['date_b']} {s['months'] or 0:5.1f}m n={s['n_a']:3d}"
                  f" stay={s['n_stay']:3d} wsh={s['wsh']:.2f} ratio={s['ratio'] if s['ratio'] else float('nan'):.2f}"
                  f" $/kW {s['usd_kw_a']:.0f}->{s['usd_kw_b']:.0f} dlog_med={s['dlog_median']:+.2f} up10={s['share_up10']:.2f}"
                  f" down10={s['share_down10']:.2f}")
    print(json.dumps(res["fit"], indent=1, default=float))
    print(json.dumps(res["timing"], indent=1, default=float))
    print(json.dumps(res["dispersion"], indent=1, default=float))
    print(json.dumps(res["after_P2"], indent=1, default=float))
