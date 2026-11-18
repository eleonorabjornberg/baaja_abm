"""
Trial agent-based model: policy consequences of S.5653, the Bipartisan American
Affordability and Jobs Act of 2026 (BAAJA), 119th Congress.

STATUS: trial / illustrative. The BAAJA levers below are taken from the bill
text; every behavioural parameter (agency capacity, review workloads, litigation
propensities, sponsor patience) is an assumption, not an estimate.

Agents (monthly time step, 15-year horizon):
  Project sponsors  - arrive, wait for review, abandon if total delay exceeds patience
  Lead agency       - fixed staff capacity; serves the review queue; under BAAJA it
                      must meet statutory deadlines, cutting review effort if short of time
  Challengers       - decide whether to sue on expected benefit vs cost, subject to
                      the statute of limitations, comment exhaustion and standing filters
  Court             - finds defects with probability tied to review quality; picks remedy
  Executive         - after political turnover, may revoke issued permits (baseline only)

BAAJA levers modelled (bill section -> model parameter):
  NEPA s.107 as amended (Sec.1106): EA within 1 yr, EIS within 2 yr   -> deadline_months
  Sec.1108: agencies may adopt other agencies' categorical exclusions -> ce_share boost
  NEPA judicial review (Sec.1110): 150-day limitation, comment
     exhaustion, direct-injury standing, courts of appeals original
     jurisdiction, remand WITHOUT vacatur, remand capped at 180 days  -> litigation block
  Sec.1302: ESA s.7 consultation 90 -> 60 days (150 -> 100 extended)  -> esa_months
  Sec.1401: no revocation of issued permits for non-Federal sponsors  -> revocation off
"""
import numpy as np, json, sys

BASE = dict(
    months=180, arrivals_per_month=20,
    # share of new projects by review pathway [CE, EA, EIS]
    pathway_share=[0.60, 0.33, 0.07],
    work_units={"CE": 0.5, "EA": 6.0, "EIS": 40.0},   # staff-months of review work
    agency_capacity=110.0,
    # minimum elapsed months per review (comment periods, interagency coordination)
    floor_months={"CE": 1, "EA": 14, "EIS": 45},                            # staff-months available per month
    deadline_months=None,                             # None = no binding deadline
    ce_boost=0.0,                                     # extra share moved EA -> CE
    esa_months=3.0, esa_share=0.25,                   # share of EA/EIS needing s.7 consult
    # litigation
    sue_base={"CE": 0.01, "EA": 0.05, "EIS": 0.25},   # propensity to sue a decision
    sol_months=72,                                    # APA default 6-year limitation
    standing_filter=1.0,                              # share of would-be suers who qualify
    litigation_months=30,                             # district court + appeal
    remedy="vacatur",                                 # 'vacatur' or 'remand'
    p_vacatur_given_defect=0.6, remand_months=12,
    # review quality -> defects
    base_defect=0.10, rush_defect_slope=0.8,          # defect prob rises as effort is cut
    # sponsors
    patience_median_months=60, patience_sigma=0.5,
    # executive turnover / revocation risk on issued permits
    revocation_on=True, turnover_every=48, p_revoke_after_turnover=0.03,
)

BAAJA = dict(
    deadline_months={"CE": 3, "EA": 12, "EIS": 24},
    floor_months={"CE": 1, "EA": 9, "EIS": 20},   # lead-agency schedule, 21/30-day coordination clocks
    ce_boost=0.10, esa_months=2.0,
    sol_months=5,                       # 150 days
    standing_filter=0.55,               # must have commented + direct injury
    litigation_months=14,               # court of appeals original jurisdiction
    remedy="remand", remand_months=6,   # remand without vacatur, max 180 days
    revocation_on=False,                # Sec.1401
)

LEVERS = {
    "Deadlines + CEs + ESA (Sec.1106/1108/1302)": ["deadline_months", "floor_months", "ce_boost", "esa_months"],
    "Judicial review only (Sec.1110)": ["sol_months", "standing_filter", "litigation_months", "remedy", "remand_months"],
    "Permit certainty only (Sec.1401)": ["revocation_on"],
}


def run(p, seed):
    rng = np.random.default_rng(seed)
    share = np.array(p["pathway_share"], float)
    share[0] += p["ce_boost"]; share[1] -= p["ce_boost"]
    kinds = np.array(["CE", "EA", "EIS"])
    queue, active = [], []   # queue: dicts under review; active: permitted projects
    out = dict(decided=0, abandoned=0, built=0, suits=0, defects_unremedied=0,
               vacated=0, revoked=0, decision_months=[], defects=0)
    for t in range(p["months"]):
        # arrivals
        for _ in range(rng.poisson(p["arrivals_per_month"])):
            k = rng.choice(kinds, p=share)
            esa = p["esa_months"] if (k != "CE" and rng.random() < p["esa_share"]) else 0.0
            queue.append(dict(k=k, t0=t, done=0.0, need=p["work_units"][k] * rng.lognormal(0, 0.3),
                              esa=esa, patience=p["patience_median_months"] * rng.lognormal(0, p["patience_sigma"]),
                              delay=0.0, floor=p["floor_months"][k] * rng.lognormal(0, 0.35)))
        # agency: deadline-driven priority (earliest deadline first) under BAAJA, FIFO otherwise
        if p["deadline_months"]:
            queue.sort(key=lambda q: q["t0"] + p["deadline_months"][q["k"]])
        cap = p["agency_capacity"]
        finished = []
        for q in queue:
            age = t - q["t0"]
            if age > q["patience"]:
                finished.append((q, "abandon")); continue
            rate = q["need"] / max(q["floor"], 1.0)           # work can't be compressed below floor
            give = min(cap, rate, q["need"] - q["done"]); cap -= give; q["done"] += give
            if q["done"] >= q["need"] - 1e-9 and age >= max(q["esa"], q["floor"]):
                finished.append((q, "full"))
            elif p["deadline_months"] and age >= p["deadline_months"][q["k"]]:
                finished.append((q, "rushed"))   # statutory deadline forces a decision
        for q, how in finished:
            queue.remove(q)
            if how == "abandon":
                out["abandoned"] += 1; continue
            quality = min(1.0, q["done"] / q["need"])
            defect = rng.random() < p["base_defect"] + p["rush_defect_slope"] * (1 - quality)
            out["defects"] += defect
            out["decided"] += 1
            if q["k"] == "EIS": out["decision_months"].append(t - q["t0"])
            active.append(dict(q, t_dec=t, defect=defect, status="permitted", resume=None))
        # challengers: each newly decided project may be sued once, within the limitation window
        for a in active:
            if a["status"] == "permitted" and t == a["t_dec"] + 1:
                expected_gain = 1.0 if p["remedy"] == "vacatur" else 0.35   # remand-only lowers payoff
                if rng.random() < p["sue_base"][a["k"]] * expected_gain * 2 * p["standing_filter"] \
                        and p["sol_months"] >= 1:
                    out["suits"] += 1
                    a["status"] = "litigation"; a["resume"] = t + p["litigation_months"]
            if a["status"] == "litigation" and t >= a["resume"]:
                if a["defect"] and rng.random() < 0.7:   # court finds the defect
                    if p["remedy"] == "vacatur" and rng.random() < p["p_vacatur_given_defect"]:
                        out["vacated"] += 1; a["delay"] += p["litigation_months"] + p["remand_months"]
                        a["status"] = "remand"; a["resume"] = t + p["remand_months"]
                    else:
                        a["status"] = "remand"; a["resume"] = t + p["remand_months"]
                        a["delay"] += p["remand_months"]
                else:
                    a["status"] = "permitted"; a["delay"] += p["litigation_months"]
            if a["status"] == "remand" and t >= a["resume"]:
                a["defect"] = False; a["status"] = "permitted"
        # executive turnover -> revocation risk
        if p["revocation_on"] and t > 0 and t % p["turnover_every"] == 0:
            for a in active:
                if a["status"] == "permitted" and rng.random() < p["p_revoke_after_turnover"]:
                    a["status"] = "revoked"; out["revoked"] += 1
        # sponsors: build 24 months after a clean permit unless total delay exhausted patience
        keep = []
        for a in active:
            total_wait = (a["t_dec"] - a["t0"]) + a["delay"]
            if a["status"] == "revoked":
                continue
            if total_wait > a["patience"] and a["status"] != "permitted":
                out["abandoned"] += 1; continue
            if a["status"] == "permitted" and t >= a["t_dec"] + 24 + a["delay"]:
                out["built"] += 1
                out["defects_unremedied"] += a["defect"]   # built on a defective review
                continue
            keep.append(a)
        active = keep
    dm = out.pop("decision_months")
    out["EIS_median_months"] = float(np.median(dm)) if dm else np.nan
    return out


def scenario(over, n=40):
    p = dict(BASE); p.update(over)
    rs = [run(p, s) for s in range(n)]
    return {k: (float(np.mean([r[k] for r in rs])), float(np.std([r[k] for r in rs]))) for k in rs[0]}


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    scen = {"Baseline (current law)": {}, "BAAJA (all levers)": BAAJA}
    for name, keys in LEVERS.items():
        scen[name] = {k: BAAJA[k] for k in keys}
    # stress test: BAAJA deadlines with 25% less agency staff
    scen["BAAJA, agency capacity -25%"] = dict(BAAJA, agency_capacity=BASE["agency_capacity"] * 0.75)
    res = {name: scenario(o, n) for name, o in scen.items()}
    json.dump(res, open("baaja_results.json", "w"), indent=1)
    cols = ["built", "abandoned", "EIS_median_months", "suits", "vacated", "revoked", "defects", "defects_unremedied"]
    print(f"{'scenario':46s}" + "".join(f"{c[:12]:>13s}" for c in cols))
    for name, r in res.items():
        print(f"{name:46s}" + "".join(f"{r[c][0]:13.1f}" for c in cols))
