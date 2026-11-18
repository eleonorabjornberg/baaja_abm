"""Project-level simulation (v3 logic).

Difference from v3: every random draw is made in every scenario, whether or not the branch uses it (common
random numbers). In v3, turning vacatur off or a non-hostile turnover skipped draws, so BAAJA and baseline runs
with the same seed drifted onto different random streams and paired differences were noisier than necessary.
Distributions are unchanged; individual seeds no longer match v3 exactly."""
import numpy as np

from .params import T, TURNOVERS, TYPES

KIND = np.array(["CE", "EA", "EIS"])
RENEWABLE_SIDE = ("Solar", "Onshore wind", "Offshore wind", "Storage", "Transmission")


def apply_ix_rule(IX, t0, speedup, rule_month=24):
    """Sec.2110: FERC interconnection rule takes effect at `rule_month`. Only study months that fall after
    the rule are shortened by `speedup` (0.9 = 10% faster). Months are counted from each project's own
    study start t0, not from the start of the simulation."""
    IX = np.asarray(IX, float)
    if speedup == 1:
        return IX
    after = np.clip(np.minimum(IX, t0 + IX - rule_month), 0, None)
    return IX - after * (1 - speedup)


def simulate(p, seed, hostile_to):
    """hostile_to: list per turnover of 'renew' or 'fossil' (the side the new administration is hostile to)."""
    rng = np.random.default_rng(seed)
    rows = []
    for name, ty in TYPES.items():
        n = rng.poisson(ty["arr"] * T * p["n_scale"])
        t0 = rng.uniform(0, T, n)
        nexus = rng.random(n) < ty["nex"]
        path = np.array(p["geo_path"] if (name == "Geothermal" and p["geo_path"]) else ty["path"], float)
        sh = min(path[1], p["ce_shift"] + (p["recond"] if name == "Transmission" else 0)); path[0] += sh; path[1] -= sh
        kind = rng.choice(3, n, p=path / path.sum())
        med = np.where(kind == 0, 4, np.where(kind == 1, 12, ty["eis"]))
        sig = np.where(kind == 0, 1.0, np.where(kind == 1, .6, .74))
        D = med * rng.lognormal(0, 1, n) ** sig
        D += np.where((kind > 0) & (rng.random(n) < p["esa_share"]), p["esa"], 0)
        trunc = np.zeros(n, bool); cut = np.zeros(n); cut_months = np.zeros(n)
        if p["enforced"]:
            cap = np.where(kind == 1, p["deadline"]["EA"], np.where(kind == 2, p["deadline"]["EIS"], np.inf)) + p["enf_lag"]
            trunc = D > cap; cut = np.where(trunc, 1 - cap / D, 0)
            cut_months = np.where(trunc, D - cap, 0)
            D = np.minimum(D, cap)
        trunc &= nexus; cut = np.where(nexus, cut, 0); cut_months = np.where(nexus, cut_months, 0)
        intake = p["intake_pub"] if ty["pub"] else p["intake_oth"]
        tP = t0 + np.where(nexus, intake + D + ty["nonnepa"] * p["nonnepa_mult"], 0)
        # challengers
        lit_p = np.where(kind == 2, ty["lit"], np.where(kind == 1, p["lit_ea"], p["lit_ce"])) * p["suit_mult"]
        sued = nexus & (rng.random(n) < lit_p)
        L = p["lit_med"] * rng.lognormal(0, .5, n)
        paused = sued & (rng.random(n) < p["pause"])
        lost = sued & (rng.random(n) < p["p_loss"] * np.where(trunc, p["trunc_loss_mult"], 1))
        delay = np.where(paused, L, 0.0)
        killed = np.zeros(n, bool)
        u_vac, u_kill = rng.random(n), rng.random(n)     # drawn in every scenario (common random numbers)
        if p["vacatur"]:
            vac = lost & (u_vac < .5)
            delay += np.where(vac, L * (~paused) + p["remand"], 0)
            killed |= vac & (u_kill < p["p_kill_vac"])
        tPermit = tP + delay
        # interconnection (parallel gate)
        IX = np.where(ty["ix"], p["ix_med"] * rng.lognormal(0, .5, n), 0)
        IX = apply_ix_rule(IX, t0, p["ix_speedup"], p["ix_rule_month"])
        tStart = np.maximum(tPermit, t0 + IX)
        tCOD = tStart + ty["build"]
        # executive halts after hostile turnovers (permitted, not yet online)
        halted = np.zeros(n, bool)
        for k, tt in enumerate(TURNOVERS):
            u_h, u_hk = rng.random(n), rng.random(n)     # drawn whatever the politics (common random numbers)
            hostile = (hostile_to[k] == "renew") == (name in RENEWABLE_SIDE)
            if not hostile or name in ("Geothermal", "Hydro relicense"):
                continue
            live = (tPermit <= tt) & (tCOD > tt) & nexus & ~killed
            h = live & (u_h < ty["halt"] * p["halt_mult"])
            halted |= h
            killed |= h & (u_hk < p["p_kill_halt"])
            tCOD = np.where(h, tCOD + p["halt_len"], tCOD); delay += np.where(h, p["halt_len"], 0)
        # sponsor attrition: commercial withdrawal hazard while waiting. As in v3, delay is added on top of
        # (tStart - t0), which already contains litigation delay when permitting is the binding gate, so
        # delay counts double there. delay_weight=1 keeps v3; set 0 for a pure time-in-queue hazard.
        wait = (tStart - t0) + p["delay_weight"] * delay
        W = rng.geometric(p["hazard"], n) if ty["ix"] else np.full(n, 10**6)
        withdrawn = W < wait
        done = ~withdrawn & ~killed
        rows.append(dict(type=name, t0=t0, nexus=nexus, kind=kind, sued=sued, trunc=trunc, cut=cut,
                         cut_months=cut_months, halted=halted, done=done, tCOD=tCOD, mw=ty["mw"], wait=tCOD - t0,
                         tPermit=np.where(nexus, tPermit, np.nan), killed=killed))
    return rows


def harm_index(r, p):
    """Truncated-review harm proxy [A] for one technology: sum over projects that reach COD by the horizon of
    pathway weight x review-months cut x project MW, in GW-review-months. Transmission (mw=0) is weighted as a
    project of `harm_mw_transmission` MW. Not a damage estimate: it scores how much analysis was skipped on
    things that actually got built."""
    online = r["done"] & (r["tCOD"] <= T)
    w = np.array([p["harm_w"][k] for k in KIND])[r["kind"]]
    mw = r["mw"] if r["mw"] > 0 else p["harm_mw_transmission"]
    return float((w * r["cut_months"] * online).sum() * mw / 1000)


def summarize(rows, p):
    out = {}
    for r in rows:
        coh = r["t0"] < 60                                   # 2026-31 cohort: followed >= 10 yrs
        online = r["done"] & (r["tCOD"] <= T)
        out[r["type"]] = dict(
            n=float(len(r["t0"])), completion_rate=float(r["done"][coh].mean()) if coh.any() else np.nan,
            GW_online=float(online.sum() * r["mw"] / 1000), projects_online=float(online.sum()),
            median_months_to_COD=float(np.median(r["wait"][r["done"] & coh])) if (r["done"] & coh).any() else np.nan,
            suits=float(r["sued"].sum()), halted=float(r["halted"].sum()),
            truncated_share=float(r["trunc"][r["nexus"]].mean()) if r["nexus"].any() else 0.0,
            mean_review_cut=float(r["cut"][r["trunc"]].mean()) if r["trunc"].any() else 0.0,
            harm=harm_index(r, p))
    out["_groups"] = summarize_groups(rows)
    return out


def summarize_groups(rows):
    """Renewable vs fossil (and storage) outcomes pooled over the technologies in each group, 2026-31 cohort for
    durations and shares. 'permitted' = federal-nexus project whose permit issued by the horizon and was not
    killed by vacatur or a halt; 'sued' is counted per federal-nexus project."""
    from .params import GROUPS
    by = {r["type"]: r for r in rows}
    out = {}
    for g, members in GROUPS.items():
        cat = lambda k: np.concatenate([by[t][k] for t in members])
        t0, nexus, done, sued, killed = cat("t0"), cat("nexus"), cat("done"), cat("sued"), cat("killed")
        wait, tPermit = cat("wait"), cat("tPermit")
        coh = t0 < 60; nx = coh & nexus
        permitted = nx & (tPermit <= T) & ~killed
        med = lambda x: float(np.median(x)) if len(x) else np.nan
        out[g] = dict(
            median_months_to_COD=med(wait[coh & done]),
            median_months_to_permit=med((tPermit - t0)[permitted]),
            permitted_share_of_nexus=float(permitted.sum() / nx.sum()) if nx.any() else np.nan,
            sued_share_of_nexus=float(sued[nx].mean()) if nx.any() else np.nan,
            suits=float(sued.sum()))
    return out
