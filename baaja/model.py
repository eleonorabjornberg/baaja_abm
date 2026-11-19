"""v5 engine: projects by technology through federal review (if they have a federal nexus) and interconnection,
sued only if they are still alive when their permit decision is made.

Common random numbers: every random draw is made for every project in every scenario, in the same order, and each
decision uses its own uniform, so scenarios with the same seed differ only through the policy.
"""
from statistics import NormalDist

import numpy as np

from .params import (REGIMES, CHALLENGER_MIX, CHALLENGERS, COURT_GROUP, ENGINE, GROUPS, HALT, INJ, LATE_SHARE,
                     RENEWABLE_SIDE, TRUNC_LOSS, TYPES, VAC, WIN, WIN_REL)

KIND = np.array(["CE", "EA", "EIS"])
_N01 = NormalDist()
_erf = np.vectorize(lambda z: _N01.cdf(z))
_inv = np.vectorize(lambda u: _N01.inv_cdf(min(max(u, 1e-12), 1 - 1e-12)))
MONTHS_BEFORE_START = 10          # end-2025 queue snapshot -> Nov 2026 start


def ix_cut(IX, t0, cut, rule_month):
    """Interconnection rules (Sec.2106/2110) shorten only the study months that fall after `rule_month`, counted
    from each project's own request date t0."""
    IX = np.asarray(IX, float)
    if cut == 0:
        return IX
    after = np.clip(np.minimum(IX, t0 + IX - rule_month), 0, None)
    return IX - after * cut


def seeded_queue(name, rng, n_scale):
    """Projects active in the LBNL queue at end-2025 [D]: request age drawn within the observed age bins."""
    a = ENGINE["lbnl"]["active_end2025"].get(name)
    if not a:
        return np.zeros(0), np.zeros(0, bool)
    counts = rng.poisson(np.array(a["age_counts"]) * n_scale)
    b = a["age_bins"]
    age = np.concatenate([rng.uniform(b[i], b[i + 1], c) for i, c in enumerate(counts)]) if counts.sum() else np.zeros(0)
    ia_done = rng.random(len(age)) < a["ia_executed_share"]
    return -(age + MONTHS_BEFORE_START), ia_done


def arrival_times(name, ty, p, rng):
    if p["arrivals"] is None:
        n = rng.poisson(ty["arr"] * REGIMES[p["regime"]].get(name, 1.0) * p["T"] * p["n_scale"])
        return rng.uniform(0, p["T"], n)
    per_year = p["arrivals"].get(name, {})                     # backcast: requests by calendar year
    out = []
    for k in range(int(np.ceil(p["T"] / 12))):
        n = rng.poisson(per_year.get(p["start_year"] + k, 0) * p["n_scale"])
        out.append(rng.uniform(12 * k, min(12 * (k + 1), p["T"]), n))
    return np.concatenate(out) if out else np.zeros(0)


def simulate(p, seed, hostile_to):
    rng = np.random.default_rng(seed)
    T = p["T"]
    rows = []
    for name, ty in TYPES.items():
        t_new = arrival_times(name, ty, p, rng)
        if p["seed_queue"] and ty["ix"]:
            t_old, ia_done = seeded_queue(name, rng, p["n_scale"])
        else:
            t_old, ia_done = np.zeros(0), np.zeros(0, bool)
        t0 = np.concatenate([t_old, t_new]); n = len(t0)
        seeded = np.arange(n) < len(t_old); ia_done = np.concatenate([ia_done, np.zeros(len(t_new), bool)])
        age0 = np.where(seeded, -t0, 0.0)                       # months already in the queue at month 0
        # ---- draws (all unconditional) ----
        u_nex, u_kind, z_D, u_esa, u_trunc = (rng.random(n), rng.random(n), rng.normal(0, 1, n), rng.random(n), rng.random(n))
        who = rng.choice(len(CHALLENGERS), n, p=CHALLENGER_MIX[name])
        u_sue, u_late, u_ex, z_L, u_inj, u_lose, u_vac, u_kill = (rng.random(n) for _ in range(8))
        u_ix, u_w, u_mkt = rng.random(n), rng.random(n), rng.random(n)
        mk = ENGINE["lbnl"]["by_market"].get(name)
        mkt = (u_mkt < mk["non-ISO"]["arrivals_share_2021_25"]).astype(int) if mk else np.zeros(n, int)   # 1 = non-ISO
        # ---- federal review ----
        nexus = u_nex < min(1.0, ty["nex"] * p["nex_mult"])
        p_eis = (p["p_eis"] or {}).get(name, 0.0)
        ea_sh = ty.get("ea_share_nonEIS", p["ea_share_nonEIS"])
        p_ea = (1 - p_eis) * ea_sh * (1 - p["ce_shift"] - (p["recond_ce"] if name == "Transmission" else 0))
        kind = np.where(u_kind < p_eis, 2, np.where(u_kind < p_eis + max(p_ea, 0), 1, 0))
        if name == "Geothermal" and p["geo_ce"] > 0:            # Sec.2229: lease activities not a major federal action
            kind = np.where(u_kind < p["geo_ce"], 0, kind)
        med = np.where(kind == 0, ty["ce_med"], np.where(kind == 1, ty["ea_med"], ty["eis_med"]))
        sig = np.where(kind == 0, 1.0, np.where(kind == 1, .6, .74))
        D = med * np.exp(sig * z_D)
        D = D + np.where((kind > 0) & (u_esa < p["esa_share"]), p["esa_months"], 0)
        intake = (p["intake_pub_2213"] if p["intake_pub_2213"] is not None else p["intake_pub"]) if ty["pub"] else p["intake_oth"]
        review_start = t0 + intake
        cap = np.where(kind == 1, 12 + 4, np.where(kind == 2, 24 + 4, np.inf))
        if p["ce_cap"]:
            cap = np.where(kind == 0, p["ce_cap"], cap)          # Sec.1402(c): 1 year for permits needing no EA/EIS
        applies = nexus & (review_start >= 0) & (u_trunc < p["deadline_bind"])   # prospective only
        trunc = applies & (D > cap) & (kind > 0)
        cut_months = np.where(applies & (D > cap), D - cap, 0.0)
        D = np.where(applies, np.minimum(D, cap), D)
        nonnepa = (p["nonnepa_hydro_1202"] if p["nonnepa_hydro_1202"] is not None else p["nonnepa_hydro"]) if ty["nonnepa"] else 0.0
        tDec = t0 + intake + D + nonnepa                         # permit decision, absent litigation
        # ---- sponsor withdrawal clock (drawn now; seeded projects are alive at month 0, memoryless) ----
        hz = p["hazard"] or {}
        h = np.where(mkt == 1, hz.get(f"{name}|non-ISO", hz.get(name, 0.02)), hz.get(f"{name}|ISO", hz.get(name, 0.02)))
        W = (np.ceil(np.log1p(-u_w) / np.log1p(-h)) + age0) if ty["ix"] else np.full(n, 1e9)
        decided = nexus & (W >= tDec - t0) & (tDec >= 0) & (tDec <= T)
        # ---- litigation on decided projects ----
        l_ea = ty["lit_ea_data"] * p["lit_data_mult"] if "lit_ea_data" in ty else p["lit_ea"]
        l_ce = ty["lit_ce_data"] * p["lit_data_mult"] if "lit_ce_data" in ty else p["lit_ce"]
        lit_p = np.where(kind == 2, ty["lit_eis"], np.where(kind == 1, l_ea, l_ce))
        if p["court"] == "baaja":
            timely = u_late >= np.array(LATE_SHARE)[who] * (1 - p["late_adapt"])
            passes = timely & (u_ex < p["exhaust_injury"])
            sued = decided & (u_sue < lit_p * p["suit_payoff"]) & passes
            inj = INJ * p["inj_nonNEPA"]; vac_share = 0.0
        else:
            sued = decided & (u_sue < lit_p)
            inj = INJ; vac_share = VAC
        L = p["lit_months"] * np.exp(.5 * z_L)
        paused = sued & (u_inj < inj)
        p_win = WIN[name] * np.array(WIN_REL)[who] * np.where(trunc, TRUNC_LOSS, 1.0)
        lost = sued & (u_lose < np.minimum(p_win, 1))
        vacated = lost & (u_vac < vac_share)
        delay = np.where(paused, L, 0.0) + np.where(vacated, p["remand_months"], 0.0)
        killed = vacated & (u_kill < p["p_kill_vac"])
        tPermit = np.where(nexus, tDec + delay, t0)
        # ---- interconnection (parallel gate) ----
        if ty["ix"]:
            mu, s = np.log(ty["ix_med"]), ty["ix_sigma"]
            lo = _erf((np.log(np.maximum(age0, 1e-9)) - mu) / s)   # seeded, IA not yet signed: study longer than age
            u = np.where(seeded & ~ia_done, lo + u_ix * (1 - lo), u_ix)
            IX = np.exp(mu + s * _inv(u))
            IX = np.where(ia_done, age0, IX)
            IX = ix_cut(IX, t0, p["ix_cut"], p["ix_rule_month"])
        else:
            IX = np.zeros(n)
        tStart = np.maximum(tPermit, t0 + IX)
        build = (p["build"] or {}).get(name, 24.0 if ty["ix"] else (36.0 if name == "Transmission" else 0.0))
        tCOD = tStart + build
        # ---- executive halts after hostile turnovers (permitted, not yet online) ----
        halted = np.zeros(n, bool)
        for k, tt in enumerate(p["turnovers"]):
            u_h, u_hk = rng.random(n), rng.random(n)
            hostile = (hostile_to[k] == "renew") == (name in RENEWABLE_SIDE)
            ph = HALT[name] * (1.0 if name == "Offshore wind" else p["halt_mult_other"]) * p["halt_mult"]
            if not hostile or ph == 0:
                continue
            live = (tPermit <= tt) & (tCOD > tt) & nexus & ~killed & (W >= tt - t0)
            hh = live & (u_h < ph)
            halted |= hh
            killed |= hh & (u_hk < p["p_kill_halt"])
            tCOD = np.where(hh, tCOD + p["halt_len"], tCOD); delay = delay + np.where(hh, p["halt_len"], 0)
        wait = (tStart - t0) + p["delay_weight"] * delay
        withdrawn = W < wait
        done = ~withdrawn & ~killed
        rows.append(dict(type=name, t0=t0, seeded=seeded, nexus=nexus, kind=kind, decided=decided, tDec=tDec,
                         sued=sued, who=np.where(sued, who, -1), lost=lost, vacated=vacated, paused=paused,
                         trunc=trunc, cut_months=cut_months, halted=halted, killed=killed, done=done,
                         tPermit=tPermit, tCOD=tCOD, wait=tCOD - t0, mw=ty["mw"], T=T, mkt=mkt))
    return rows


def harm_index(r, p):
    """GW-review-months cut on projects that reach operation [A weights]: not a damage estimate."""
    online = r["done"] & (r["tCOD"] <= r["T"])
    w = np.array([p["harm_w"][k] for k in KIND])[r["kind"]]
    mw = r["mw"] if r["mw"] > 0 else p["harm_mw_transmission"]
    return float((w * r["cut_months"] * online).sum() * mw / 1000)


def summarize(rows, p):
    out = {}
    for r in rows:
        T = r["T"]; new = ~r["seeded"]
        coh = new & (r["t0"] < 60)                              # projects requested in the first 5 years
        online = r["done"] & (r["tCOD"] <= T)
        dec = r["decided"]
        yrs = T / 12 * p["n_scale"]                         # per-year counts are per full-size population
        s = dict(n=float(new.sum()), n_seeded=float(r["seeded"].sum()),
                 completion_rate=float(r["done"][coh].mean()) if coh.any() else np.nan,
                 completion_rate_nexus=float(r["done"][coh & r["nexus"]].mean()) if (coh & r["nexus"]).any() else np.nan,
                 GW_online=float(online.sum() * r["mw"] / 1000), projects_online=float(online.sum()),
                 median_months_to_COD=float(np.median(r["wait"][r["done"] & coh])) if (r["done"] & coh).any() else np.nan,
                 decisions_per_year=float(dec.sum() / yrs),
                 EIS_per_year=float((dec & (r["kind"] == 2)).sum() / yrs),
                 EA_per_year=float((dec & (r["kind"] == 1)).sum() / yrs),
                 suits=float(r["sued"].sum()), suits_per_year=float(r["sued"].sum() / yrs),
                 vacated=float(r["vacated"].sum()), halted=float(r["halted"].sum()),
                 halted_GW=float((r["halted"]).sum() * r["mw"] / 1000),
                 killed_by_courts_or_halts=float(r["killed"].sum()),
                 permitted_share=float((dec & ~r["killed"]).sum() / dec.sum()) if dec.any() else np.nan,
                 median_months_to_permit=float(np.median((r["tPermit"] - r["t0"])[dec & coh])) if (dec & coh).any() else np.nan,
                 truncated_share=float(r["trunc"][dec].mean()) if dec.any() else 0.0,
                 harm=harm_index(r, p))
        for m, lab in ((0, "ISO"), (1, "non-ISO")):
            sel = r["mkt"] == m
            s[f"GW_online|{lab}"] = float((online & sel).sum() * r["mw"] / 1000)
            s[f"completion_rate|{lab}"] = float(r["done"][coh & sel].mean()) if (coh & sel).any() else np.nan
        for j, c in enumerate(CHALLENGERS):
            s[f"suits: {c}"] = float((r["who"] == j).sum())
            s[f"wins: {c}"] = float(((r["who"] == j) & r["lost"]).sum())
        out[r["type"]] = s
    out["_groups"] = summarize_groups(rows)
    out["_online_by_year"] = online_by_year(rows)
    return out


def online_by_year(rows):
    """GW reaching operation in each model year, by technology."""
    out = {}
    for r in rows:
        yrs = int(np.ceil(r["T"] / 12))
        on = r["done"] & (r["tCOD"] <= r["T"]) & (r["tCOD"] >= 0)
        out[r["type"]] = (np.histogram(r["tCOD"][on], bins=yrs, range=(0, 12 * yrs))[0] * r["mw"] / 1000).tolist()
    return out


def summarize_groups(rows):
    by = {r["type"]: r for r in rows}
    out = {}
    for g, members in GROUPS.items():
        cat = lambda k: np.concatenate([by[t][k] for t in members])
        t0, seeded, dec, sued, killed, done = cat("t0"), cat("seeded"), cat("decided"), cat("sued"), cat("killed"), cat("done")
        wait, tPermit, who, lost = cat("wait"), cat("tPermit"), cat("who"), cat("lost")
        coh = ~seeded & (t0 < 60)
        med = lambda x: float(np.median(x)) if len(x) else np.nan
        o = dict(median_months_to_COD=med(wait[coh & done]), median_months_to_permit=med((tPermit - t0)[dec & coh]),
                 permitted_share=float((dec & ~killed).sum() / dec.sum()) if dec.any() else np.nan,
                 sued_share_of_decided=float(sued[dec].mean()) if dec.any() else np.nan,
                 decisions=float(dec.sum()), suits=float(sued.sum()))
        for j, c in enumerate(CHALLENGERS):
            o[f"suits: {c}"] = float((who == j).sum())
            o[f"challenger wins: {c}"] = float(((who == j) & lost).sum())
        out[g] = o
    return out
