"""Grid access as an agent-based system (Phase 2): grid operators, developers and transmission, by region.

simulate(p, ...) with p["grid"] == "agents" replaces the exogenous interconnection draw with this module. The
permitting, litigation and halt blocks are unchanged and keep their random numbers, so runs stay paired.

Agents, one set per LBNL region:
  Grid operator   studies requests in clusters that close every C months (C = 12: Order 2023 cluster studies; ERCOT
                  C = 1, individual studies). Serial regions study one cluster at a time: a cluster starts when the
                  previous one is finished, and takes max(d, live requests / K) months; K (requests a month) adapts to
                  the arrival rate at rate lambda a year. Fitted per region to LBNL request -> signed-agreement times
                  (fit_operators). Requests already in the queue at end-2025 without an agreement are studied first,
                  oldest first, at rate K (serial regions) or keep their exogenous draw (ERCOT).
  Developer       each request has a private value per kW, lognormal [D: LBNL cost data, P(complete | upgrade cost)].
                  At its study result it learns its network-upgrade cost (lognormal by region [D]) and stays only if
                  cost <= value. In cluster regions under current law the result comes R months before the agreement;
                  withdrawals raise the cost of those who stay (re-study, by rho x the withdrawn MW share) and they
                  decide again. New requests enter in response to the published wait and to regional scarcity.
  Transmission    projects (the model's transmission type, through permitting and courts as before) add hosting
                  room when they reach operation; upgrade costs rise with capacity signed since 2026 net of that room.
Bill provisions:
  Sec.2106        in each RTO that adopts a new process (2106(d): FERC may find existing ones compliant), from the rule
                  month: a share of requests can use published locations with a fixed per-MW fee (no cost shock, no
                  re-study); a single decision point (no re-study round); security and penalties deter requests with a
                  low chance of completing. RTO/ISO markets only, not ERCOT, Southeast or West.
  Sec.2110        study throughput x (1 + g) from the rule month (FERC-jurisdictional providers: not ERCOT).
  Sec.2109        extra hosting room per transmission project completed after the rule month.
  Titles I-II     transmission permitting and litigation provisions move transmission completion dates, and so
                  hosting room, through the existing pipeline.
Current-law transmission (same draws, levers off) is run inside each simulation, so only the bill's change in
transmission moves costs; the historical pace of transmission is already in the cost growth rate kappa [D].
"""
import json
import os

import numpy as np
from scipy.special import ndtr

from .params import REGIONS, RTO_IDX, TYPES

_D = os.path.join(os.path.dirname(__file__), "..", "data")
GT = json.load(open(os.path.join(_D, "grid_targets.json")))
FLEET = json.load(open(os.path.join(_D, "fleet_targets.json")))
END_MONTH = 215                       # Dec 2025, months since Jan 2008
FORWARD_OFFSET = 226                  # model month 0 (Nov 2026), months since Jan 2008
ERCOT = REGIONS.index("ERCOT")
NON_ISO = [REGIONS.index(r) for r in ("Southeast", "West")]
FLEET_GW = np.array([sum(FLEET["capacity"].get(r, {}).values()) / 1000 for r in REGIONS])
COST = [GT["cost"][r] for r in REGIONS]
VALUE = [GT["value"]["non-ISO" if i in NON_ISO else "ISO"] for i in range(len(REGIONS))]
D_DATA = np.array([sum(GT["arrivals"][r].get(str(y), 0) for y in range(2021, 2026)) / 60 for r in REGIONS])
from .params import GRID_BASE, GRID_LEVERS  # noqa: E402  (assumptions live in params)


# ================================================================================================================
# Grid operators: replay of the LBNL queue, fitted per region
# ================================================================================================================
def replay(q, wd, C, d, K0, lam, sig, z, serial=True, return_state=False):
    """Months from request to study result for each request, given request months q, months to withdrawal wd (-1 if
    none), cluster window C, minimum study months d, initial throughput K0 (requests/month), adaptation lam (/year),
    within-cluster log spread sig and normal draws z."""
    j = q // C; T = np.full(len(q), np.nan); Tprev = -1e9; K = K0; tprev = 0; D = 0.0
    for jj in np.unique(j):
        m = np.where(j == jj)[0]; close = (jj + 1) * C
        D = ((q >= close - 12) & (q < close)).sum() / 12
        K = K + (1 - np.exp(-lam * (close - tprev) / 12)) * (D - K); tprev = close
        start = max(close, Tprev) if serial else close
        live = ((wd[m] < 0) | (q[m] + wd[m] > start)).sum()
        Tj = max(close + d, start + live / max(K, 1e-6))
        T[m] = close + (Tj - close) * np.exp(sig * z[m]); Tprev = Tj
    if return_state:
        return T - q, dict(K=float(K), D=float(D), t=int(tprev))
    return T - q


def _arrays(r):
    R = GT["replay"][r]
    return tuple(np.array(R[k]) for k in ("q", "wd", "ia", "st"))


def score(R, t, years):
    """Censoring-consistent comparison by cohort: among requests that signed an agreement or are still active without
    withdrawing, (1) median months to agreement for those signed by Dec 2025, model vs data, (2) share signed."""
    q, wd, ia, st = R
    y = 2008 + q // 12
    elig = (ia > 0) | ((wd < 0) & (st == 0))
    msig = q + t <= END_MONTH
    err, out = [], {}
    for Y in years:
        s = (y == Y) & elig
        a, b = s & msig, s & (ia > 0)
        sm, sd = a.sum() / max(s.sum(), 1), b.sum() / max(s.sum(), 1)
        e = (sm - sd) ** 2
        if a.sum() >= 10 and b.sum() >= 10:
            ma, mb = float(np.median(t[a])), float(np.median(ia[b])); e += np.log(ma / mb) ** 2
        else:
            ma = mb = None
            e += 0.25 if b.sum() >= 10 else 0.0
        err.append(e)
        out[Y] = dict(model_median=ma, data_median=mb, model_share=float(sm), data_share=float(sd), n_signed=int(b.sum()))
    return float(np.mean(err)), out


FITTED = {"MISO": (12, True), "CAISO": (12, True), "ERCOT": (1, False)}   # IA-date coverage >= 0.84 [D]
GRID_D = range(3, 46, 3)
GRID_K = (0.05, 0.1, 0.2, 0.4, 0.7, 1.0, 1.5, 2.5)
GRID_LAM = (0, 0.1, 0.3, 1, 3, 12)
GRID_SIG = (0.15, 0.3, 0.45, 0.6)
FIT_YEARS, HOLD_YEARS = range(2010, 2020), range(2020, 2025)


def _d0(q):
    return max(((q >= 24) & (q < 84)).sum() / 60, 0.5)          # requests/month, 2010-14


def fit_operators(seed=1):
    """Fit (d, K0/D0, lambda, sigma) by grid search on 2010-19 cohorts; report 2020-24 cohorts as a holdout. Regions with
    reliable agreement dates (CAISO, ERCOT, MISO) are fitted one by one; the others take a joint fit to MISO and CAISO.
    Each region's throughput at the end of 2025 is kept as the forward starting point."""
    import itertools
    data = {r: _arrays(r) for r in REGIONS}
    Z = {r: np.random.default_rng(seed).normal(0, 1, len(data[r][0])) for r in REGIONS}
    fits = {}
    for r, (C, serial) in FITTED.items():
        q, wd = data[r][0], data[r][1]
        best = None
        for d, k, lam, sig in itertools.product(GRID_D, GRID_K, GRID_LAM, GRID_SIG):
            e, _ = score(data[r], replay(q, wd, C, d, k * _d0(q), lam, sig, Z[r], serial), FIT_YEARS)
            if best is None or e < best[0]:
                best = (e, d, k, lam, sig)
        fits[r] = dict(C=C, serial=serial, d=best[1], k0=best[2], lam=best[3], sig=best[4], fitted=True)
    pool = ("MISO", "CAISO"); best = None
    for d, k, lam, sig in itertools.product(GRID_D, GRID_K, GRID_LAM[:5], GRID_SIG[:3]):
        e = np.mean([score(data[r], replay(data[r][0], data[r][1], 12, d, k * _d0(data[r][0]), lam, sig, Z[r]), FIT_YEARS)[0]
                     for r in pool])
        if best is None or e < best[0]:
            best = (e, d, k, lam, sig)
    pooled = dict(C=12, serial=True, d=best[1], k0=best[2], lam=best[3], sig=best[4], fitted=False)
    out = {}
    for r in REGIONS:
        f = dict(fits.get(r, pooled))
        q, wd = data[r][0], data[r][1]
        t, st = replay(q, wd, f["C"], f["d"], f["k0"] * _d0(q), f["lam"], f["sig"], Z[r], f["serial"], return_state=True)
        # throughput carried to Nov 2026 at the 2025 arrival rate
        K = st["D"] + (st["K"] - st["D"]) * np.exp(-f["lam"] * (FORWARD_OFFSET - st["t"]) / 12)
        f.update(K_end=float(K), D_end=float(st["D"]), D_data=float(D_DATA[REGIONS.index(r)]))
        f["fit_error"], f["fit"] = score(data[r], t, FIT_YEARS)
        f["holdout_error"], f["holdout"] = score(data[r], t, HOLD_YEARS)
        out[r] = f
    return out


# ================================================================================================================
# Supply context for developers' scarcity signal
# ================================================================================================================
_SCARCITY = {}


WD_MONTHS = (12, 24, 36, 60)
WD_COHORTS = (2015, 2019)


def withdrawal_curve_data(months=WD_MONTHS, years=WD_COHORTS):
    """Share of a region's generation requests (cohorts `years`) withdrawn within m months of the request [D: LBNL].
    Withdrawals with no date (mostly Southeast and West) are assumed to share the dated ones' timing."""
    out = {}
    for r in REGIONS:
        R = GT["replay"][r]
        q, wd, st = np.array(R["q"]), np.array(R["wd"]), np.array(R["st"])
        c = (2008 + q // 12 >= years[0]) & (2008 + q // 12 <= years[1])
        w = c & (st == 2); wk = w & (wd >= 0)
        if c.sum() < 30 or not wk.any():
            continue
        out[r] = {m: float(w.sum() / c.sum() * (wd[wk] <= m).mean()) for m in months}
    return out


def withdrawal_curve_model(rows, months=WD_MONTHS, window=(0, 60)):
    """Same share in a model run: new requests made in `window` (months from Dec 2025), any withdrawal."""
    G = [r for r in rows if "gwd" in r]
    cat = lambda k: np.concatenate([np.broadcast_to(r[k], r["t0"].shape) for r in G])
    t0, W, gwd, reg, seeded, wait = cat("t0"), cat("W"), cat("gwd"), cat("region"), cat("seeded"), cat("wait")
    tw = np.minimum(np.where(W < wait, W, np.inf), gwd - t0)
    sel = ~seeded & (t0 >= window[0]) & (t0 < window[1])
    out = {}
    for k, r in enumerate(REGIONS):
        s = sel & (reg == k)
        if s.sum():
            out[r] = {m: float((tw[s] <= m).mean()) for m in months}
    return out


def _supply_context():
    """Existing firm capacity (with retirements), demand and reserve margin by region and model year [central]."""
    if "ctx" not in _SCARCITY:
        from . import supply as sp
        fleet = sp.existing_fleet(sp.SA)
        fac = np.array([[sp.onpeak(g, y, sp.SA) for y in sp.YEARS] for g in sp.GROUPS])
        firm = (fleet * fac[None]).sum(axis=1) * sp.FIRM_SCALE[:, None]
        nid, rml, tr = sp.demand(sp.SA)
        onpk = {t: sp.ONPEAK_2026.get(t, 1.0) for t in TYPES}
        _SCARCITY["ctx"] = dict(need=(1 + rml) * nid - tr - firm, nid=nid, onpeak=onpk, years=len(sp.YEARS))
    return _SCARCITY["ctx"]


# ================================================================================================================
# The agents
# ================================================================================================================
def _take(s, keep):
    out = dict(s)
    for k, v in s.items():
        if isinstance(v, np.ndarray) and v.shape[:1] == (s["n"],):
            out[k] = v[keep]
    out["halt_u"] = [(a[keep], b[keep]) for a, b in s["halt_u"]]
    if s.get("grid") is not None:
        out["grid"] = {k: v[keep] for k, v in s["grid"].items()}
    out["n"] = int(keep.sum())
    return out


def _cat(a, b):
    out = dict(a)
    for k, v in a.items():
        if isinstance(v, np.ndarray) and v.shape[:1] == (a["n"],):
            out[k] = np.concatenate([v, b[k]])
    out["halt_u"] = [(np.concatenate([x[0], y[0]]), np.concatenate([x[1], y[1]])) for x, y in zip(a["halt_u"], b["halt_u"])]
    out["n"] = a["n"] + b["n"]
    return out


def _law(p):
    """Same parameters with every BAAJA lever at its current-law value (current-law assumptions kept)."""
    from .params import BAAJA, BASE
    q = dict(p)
    for k in BAAJA:
        q[k] = BASE[k]
    for k in GRID_LEVERS:
        q[k] = GRID_BASE[k]
    return q


def _tx_counts(states, p, hostile_to, region_u, T_ext):
    """Transmission projects reaching operation by month and region, scenario and current law (same draws)."""
    from .model import _post
    s = next(x for x in states if x["name"] == "Transmission")
    gen = np.concatenate([x["region"][~x["seeded"]] for x in states if x["ty"]["ix"]])
    share = np.bincount(gen[gen >= 0], minlength=len(REGIONS)).astype(float)
    share = np.cumsum(share / share.sum())
    reg = np.minimum(np.searchsorted(share, region_u[: s["n"]], side="right"), len(REGIONS) - 1)
    out = {}
    for lab, pp in (("scn", p), ("law", _law(p))):
        r = _post(s, pp, hostile_to)
        on = r["done"] & (r["tCOD"] >= 0)
        cnt = np.zeros((len(REGIONS), T_ext + 1))
        m = np.clip(np.ceil(r["tCOD"][on]).astype(int), 0, T_ext)
        np.add.at(cnt, (reg[on], m), 1)
        out[lab] = np.cumsum(cnt, axis=1)
    return out


def run_agents(states, p, seed, hostile_to):
    """Agents mode: returns the states with each project's grid outcome (entered, agreement month, grid withdrawal
    month, cost) and with requests that chose not to enter removed."""
    from .model import _pre
    ops = (p.get("grid_cal") or {}).get("operators")
    if ops is None:
        raise ValueError("grid agents need fitted operators: cal['grid_cal']['operators'] (calibrate.calibrate_grid)")
    T = p["T"]; T_ext = T + 240
    gen_idx = [i for i, s in enumerate(states) if s["ty"]["ix"]]
    for s in states:
        s["cand"] = np.zeros(s["n"], bool)
    # ---- extra candidate requests (entry above the base rate), own streams ----
    if p["entry_max"] > 1:
        rx = np.random.default_rng([seed, 15485863]); sx = np.random.default_rng([seed, 15485863, 1])
        sr = np.random.default_rng([seed, 15485863, 2])
        px = dict(p, seed_queue=False, n_scale=p["n_scale"] * (p["entry_max"] - 1))
        for i in gen_idx:
            x = _pre(states[i]["name"], states[i]["ty"], px, rx, sx, sr)
            x["cand"] = np.ones(x["n"], bool)
            states[i] = _cat(states[i], x)
    g = np.random.default_rng([seed, 32452843])
    u_adopt = g.random(len(REGIONS))
    u_txreg = g.random(100000)
    # ---- flatten generation requests ----
    F = {k: np.concatenate([states[i][k] for i in gen_idx]) for k in
         ("t0", "seeded", "ia_done", "W", "Ew", "age0", "region", "tDec", "build", "IX", "cand")}
    F["typ"] = np.concatenate([np.full(states[i]["n"], i) for i in gen_idx])
    F["mw"] = np.concatenate([np.full(states[i]["n"], float(states[i]["ty"]["mw"])) for i in gen_idx])
    vm = (p.get("grid_cal") or {}).get("value_mult") or {}
    F["vmult"] = np.concatenate([np.array([vm.get(f"{states[i]['name']}|{rn}", vm.get(states[i]["name"], 1.0))
                                           for rn in REGIONS])[np.maximum(states[i]["region"], 0)] for i in gen_idx])
    n = len(F["t0"])
    Zv, Zc, Uc0, Zs, Uloc, Uacc = (g.normal(0, 1, n), g.normal(0, 1, n), g.random(n), g.normal(0, 1, n),
                                   g.random(n), g.random(n))
    ctx = _supply_context()
    onpk = np.array([ctx["onpeak"][states[i]["name"]] for i in gen_idx])[np.searchsorted(gen_idx, F["typ"])]
    tx = _tx_counts(states, p, hostile_to, u_txreg, T_ext) if p["tx_hosting_gw"] > 0 else None
    out = dict(entered=F["seeded"].copy(), tIA=np.full(n, np.inf), gwd=np.full(n, np.inf), cost=np.full(n, np.nan),
               planned=np.zeros(n, bool), W=F["W"].copy())
    h_pre = (p.get("grid_cal") or {}).get("h_pre") or {}
    backcast = p["arrivals"] is not None
    for r in range(len(REGIONS)):
        idx = np.where(F["region"] == r)[0]
        if len(idx):
            _region(r, idx, F, out, p, ops[REGIONS[r]], dict(Zv=Zv, Zc=Zc, Uc0=Uc0, Zs=Zs, Uloc=Uloc, Uacc=Uacc),
                    onpk, ctx, tx, u_adopt[r], T, T_ext, backcast, h_pre.get(REGIONS[r]))
    # ---- write back, drop non-entrants ----
    pos = 0
    for i in gen_idx:
        k = states[i]["n"]
        states[i]["grid"] = {key: v[pos:pos + k] for key, v in out.items() if key != "W"}
        states[i]["W"] = out["W"][pos:pos + k]
        pos += k
        states[i] = _take(states[i], states[i]["grid"]["entered"])
    return states


def _region(r, idx, F, out, p, op, U, onpk, ctx, tx, u_adopt, T, T_ext, backcast, h_pre=None):
    t0, seeded, ia_done = F["t0"][idx], F["seeded"][idx], F["ia_done"][idx]
    # withdrawal for reasons other than study results: a regional hazard until construction starts (the same unit draw
    # as the exogenous clock). Requests already holding an agreement at end-2025 keep the exogenous clock.
    W = F["W"][idx]
    if h_pre is not None:
        W = np.where(ia_done, W, np.ceil(F["Ew"][idx] / -np.log1p(-h_pre)) + F["age0"][idx])   # months from request
    mw, cand, tDec, build = F["mw"][idx], F["cand"][idx], F["tDec"][idx], F["build"][idx]
    n = len(idx)
    entered = seeded.copy(); started = seeded & ia_done
    tIA = np.full(n, np.inf); gwd = np.full(n, np.inf); cost = np.full(n, np.nan); planned = np.zeros(n, bool)
    fee = np.zeros(n)
    C, serial, d, lam, sig = op["C"], op["serial"], op["d"], op["lam"], op["sig"]
    cst, val = COST[r], VALUE[r]
    cmed = np.exp(cst["mu"])
    zv, zc, uc0, zs, uloc, uacc = (U[k][idx] for k in ("Zv", "Zc", "Uc0", "Zs", "Uloc", "Uacc"))
    v0 = np.exp(val["mu"] + val["sigma"] * zv) * F["vmult"][idx]   # private value, $/kW (technology x region scale)
    craw = np.where(uc0 < cst["zero_share"], 1.0, np.exp(cst["sigma"] * zc))   # cost relative to the regional median
    rule = p["ix_rule_month"]
    in_rto = r in RTO_IDX
    adopt = p["grid_2106"] and in_rto and (u_adopt < p["adopt_2106"])
    g2110 = p["grid_2110"] if r != ERCOT else 0.0
    R = p["restudy_months"] if serial else 0
    # ---- throughput: start from end-2025 (scaled to the model's request units) or, in a backcast, from 2010 ----
    base_new = ~seeded & ~cand
    if backcast:
        D0 = max((base_new & (t0 < 60)).sum() / 60, 0.5 * p["n_scale"])
        K = op["k0"] * D0
    else:
        D0 = base_new.sum() / T
        K = op["K_end"] / max(op["D_data"], 1e-9) * D0           # same throughput / arrivals ratio as end-2025
    cnt = np.zeros(T_ext + 13)
    hist = [D0] * 12                                               # trailing 12 months of entries
    # ---- scarcity: projected shortfall share of peak, `ahead` months on ----
    need, nid = ctx["need"][r], ctx["nid"][r]
    ny = ctx["years"]; ahead = p["scarcity_ahead"]
    known = np.zeros(T_ext + ahead + 600)                          # firm MW expected online by month
    ev = {}                                                         # sign month -> (COD months, firm MW)

    def scar(t):
        k = min(max((t + ahead) // 12, 0), ny - 1)
        return max(need[k] - known[: t + ahead + 1].sum(), 0.0) / nid[k]

    ia0 = seeded & ia_done
    if ia0.any():
        m = np.clip(np.maximum(tDec[ia0], 0) + build[ia0], 0, len(known) - 1).astype(int)
        np.add.at(known, m, mw[ia0] * onpk[idx][ia0])
    beta = 0.0 if backcast else p["scarcity_beta"]
    s0 = scar(0)
    A = np.zeros(T_ext + 2)                                         # GW signed since month 0, by month (increments)
    kappa = p["kappa"]

    def cong(t):
        a = A[: t + 1].sum()
        h = 0.0
        if tx is not None:
            tt = min(t, tx["scn"].shape[1] - 1)
            extra = 1 + (p["grid_2109"] if t >= rule else 0.0)
            h = p["tx_hosting_gw"] * (extra * tx["scn"][r, tt] - tx["law"][r, tt])
        return np.exp(kappa * (a - h) / FLEET_GW[r])

    def sign(sel, when):
        """Record agreements (only those alive then): GW signed and firm capacity expected online."""
        ok = sel & (W >= when - t0)
        tIA[ok] = when[ok] if np.ndim(when) else when
        w = np.broadcast_to(when, (n,))
        mi = np.clip(np.ceil(w[ok]).astype(int), 0, len(A) - 1)
        np.add.at(A, mi, mw[ok] / 1000)
        cod = np.maximum(tDec[ok], w[ok]) + build[ok]
        for sm, cm, f in zip(mi, cod, mw[ok] * onpk[idx][ok]):
            ev.setdefault(int(sm), []).append((int(min(max(cm, 0), len(known) - 1)), f))
        return ok

    def decide(sel, t_res, t_sign, c, single, tnow):
        """Study results at t_res; agreements at t_sign. Non-adopting cluster regions: one re-study round."""
        vm = v0 * np.exp(beta * (scar(tnow) - s0))
        alive1 = sel & (W >= t_res - t0)
        stay1 = alive1 & ((c <= vm) | planned)
        gwd[alive1 & ~stay1] = t_res[alive1 & ~stay1]
        if single or R == 0:
            sign(stay1, t_sign); cost[alive1] = c[alive1]; return
        tot = mw[alive1].sum()
        wsh = mw[alive1 & ~stay1].sum() / tot if tot > 0 else 0.0
        c2 = np.where(planned, c, c * (1 + p["restudy_rho"] * wsh))
        alive2 = stay1 & (W >= t_sign - t0)
        stay2 = alive2 & ((c2 <= vm) | planned)
        gwd[alive2 & ~stay2] = t_sign[alive2 & ~stay2]
        sign(stay2, t_sign); cost[alive1] = c2[alive1]

    # ---- legacy requests (in the queue at end-2025, no agreement) ----
    leg = np.where(seeded & ~ia_done)[0]
    if not serial and len(leg):                                     # individual studies: keep the exogenous draw
        tl = np.maximum(t0[leg] + F["IX"][idx][leg], 0.0)
        sel = np.zeros(n, bool); sel[leg] = True
        tt = np.zeros(n); tt[leg] = tl
        c = cmed * craw
        decide(sel, tt, tt, c, True, 0)
        started[leg] = True; leg = leg[:0]
    leg = leg[np.argsort(t0[leg], kind="stable")]                  # oldest first
    lp = 0; budget = 0.0
    # ---- clusters of new requests ----
    j = np.where(t0 >= 0, np.floor(np.maximum(t0, 0) / C), -1).astype(int)
    busy = 0.0
    nxt = 0                                                         # next cluster to study
    order = np.argsort(t0, kind="stable"); newpos = 0
    newo = order[~seeded[order]]
    Wref = None
    for t in range(T_ext):
        Keff = K * (1 + (g2110 if t >= rule else 0.0))
        for cm, f in ev.pop(t, []):
            known[cm] += f
        # published wait and scarcity -> entry this month
        pend = entered & ~started & (W >= t - t0) & (t0 < t)
        B = pend.sum()
        Wpub = (C / 2 + max(busy - t, 0.0) if serial else 0.0) + max(d, B / max(Keff, 1e-9))
        if Wref is None:
            Wref = Wpub
        if t < T:
            hi = newpos
            while hi < len(newo) and t0[newo[hi]] < t + 1:
                hi += 1
            if hi > newpos:
                ii = newo[newpos:hi]; newpos = hi
                sc = scar(t) - s0
                mult = (Wref / Wpub) ** p["entry_wait_elast"] * np.exp(beta * sc)
                mult = min(max(mult, 0.2), p["entry_max"])
                ok = np.where(cand[ii], uacc[ii] < (mult - 1) / max(p["entry_max"] - 1, 1e-9), uacc[ii] < min(mult, 1.0))
                if adopt and t >= rule:
                    cb = cmed * cong(t)
                    vm = v0[ii] * np.exp(beta * sc)
                    pl = (uloc[ii] < p["planned_share_2106"]) & (vm >= p["fee_mult_2106"] * cb)
                    qv = cst["zero_share"] + (1 - cst["zero_share"]) * ndtr((np.log(np.maximum(vm, 1e-9)) - np.log(cb)) / cst["sigma"])
                    ok &= pl | (qv >= p["q_min_2106"])
                    planned[ii] = ok & pl; fee[ii] = p["fee_mult_2106"] * cb
                entered[ii] = ok
                cnt[t] += ok.sum()
        # throughput adapts to the arrival rate
        hist.append(cnt[t] if t < T else 0.0); hist.pop(0)
        if t < T:
            K += (1 - np.exp(-lam / 12)) * (np.mean(hist) - K)
        # legacy queue, oldest first
        if lp < len(leg):
            budget += Keff
            done_now = []
            while lp < len(leg) and budget >= 1:
                i = leg[lp]; lp += 1
                if W[i] < t - t0[i]:
                    continue
                budget -= 1; done_now.append(i)
            if done_now:
                sel = np.zeros(n, bool); sel[done_now] = True; started[done_now] = True
                tt = np.full(n, t + 1.0)
                decide(sel, tt, tt, cmed * cong(t) * craw, True, t)
            if lp < len(leg):
                continue
            budget = 0.0; busy = max(busy, t + 1)
        # clusters
        while True:
            close = (nxt + 1) * C
            if close > t or (serial and t < busy):
                break
            mem = (j == nxt) & entered & ~started
            nxt += 1
            if not mem.any():
                continue
            live = (mem & (W >= t - t0)).sum()
            Tj = max(close + d, t + live / max(Keff, 1e-9))
            busy = Tj
            Ti = close + (Tj - close) * np.exp(sig * zs)
            started |= mem
            single = adopt & (t0 >= rule)                            # Sec.2106: single decision point
            tres = np.maximum(Ti - R, t + 1) if serial else Ti     # first study result
            tsig = np.maximum(Ti, tres)
            c = np.where(planned, fee, cmed * cong(t) * craw)
            if serial and adopt:
                # requests from the rule month: one decision at the first result; earlier ones: current process
                s1 = mem & single
                decide(s1, tres, tres, c, True, t)
                decide(mem & ~single, tres, tsig, c, False, t)
            else:
                decide(mem, tres, tsig, c, not serial, t)
            if serial:
                break
    out["W"][idx] = W
    out["entered"][idx] = entered; out["tIA"][idx] = tIA; out["gwd"][idx] = gwd
    out["cost"][idx] = cost; out["planned"][idx] = planned
