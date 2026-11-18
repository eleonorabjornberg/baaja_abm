"""
Trial ABM v3: BAAJA (S.5653, 119th Congress) and the US electricity build-out, by technology,
calibrated to published data where data exist.

Agents: project sponsors (withdraw under commercial attrition and delay), challengers (sue),
courts (decide, choose remedy), the executive (halts permits after a change of administration).
Each project runs two gates in parallel: federal permitting (if it has a federal nexus) and
grid interconnection (generation only). Construction starts when both are cleared.

CALIBRATION  [D] = from data, [A] = assumption
  EIS duration, current law   median 30 mo, sigma 0.74   [D] CEQ EIS Timelines 2025: median 2.4 yr NOI->FEIS
                              (2021-24), 39% within 2 yr (the sigma reproduces ~38%); IQR spread from CEQ 2020
                              (2.2-6.0 yr)
      solar / onshore wind    median 26 / 43 mo          [D] RFF (Fraas et al.): solar 26, wind 43 mo average EIS
  EA duration                 median 12 mo, sigma 0.6    [D] DOE: median EA 7-10 mo; 2015 mean 21 mo
  CE duration                 median 4 mo, sigma 1.0     [D] Roosevelt/USFS data: CE median ~112 days, mean 209
  Hydro relicensing           median 80 mo total         [D] DOE WPTO: relicensing averages 7.6 yr
  Litigation, EIS projects    solar .45 wind .45 trans .31 gas .50 geo .33   [D] Bennon & Wilson 2023 (solar ~2/3,
                              wind 38%, transmission 31%, pipelines 50%); RFF (solar ~1/3, wind ~1/2, geo 1 of 3)
      offshore wind .6, hydro .2, storage .2   [A]
  Litigation, EA / CE         .03 / .002                 [A] informed by Ruple (~0.22% of all NEPA decisions)
  Interconnection             IR->IA median 40 mo        [D] LBNL Queued Up: IR->IA well over 3 yr; IR->COD ~55 mo
  Queue completion            ~19% of projects           [D] LBNL Queued Up 2026: 19% of projects (13% of capacity)
                              requested 2000-2020 reached COD -> baseline attrition hazard calibrated to this
  Offshore wind halts         p=0.8 after a hostile turnover, ~8 mo, 25% killed   [D/A] 2025: stop-work orders on all
                              five under-construction projects, several lifted by courts; permits remanded for others
  Federal nexus shares, pathway mix, project sizes, arrival rates, construction times   [A]
  Agency staffing is NOT modelled endogenously (v1 did that); durations are drawn from the data instead.

BAAJA levers (bill section -> model)
  Sec.1106  deadlines (EA 1 yr, EIS 2 yr) made enforceable via sponsor petition + 60-day order -> durations
            capped at deadline + 4 mo; reviews cut short are flagged "truncated"
  Sec.1108  adopt other agencies' CEs -> 10% of EA -> CE
  Sec.1110  150-day limit + comment exhaustion + direct injury -> suit propensity x0.55 [A];
            remand without vacatur -> suit payoff x0.6 [A], projects keep building (pause prob .5 -> .15 [A]);
            courts of appeals original jurisdiction -> case length 24 -> 12 mo [A]; remand <= 180 days
  Sec.1202  CWA s.401 certification capped at 1 yr -> hydro non-NEPA component 48 -> 36 mo [A]
  Sec.1302  ESA s.7 consultation 90 -> 60 days
  Sec.1401  no revocation/interference with issued permits -> halt prob x0.1 (residual) [A]
  Sec.2102  CE for reconductoring in existing ROW -> 25% of transmission EA -> CE [A]
  Sec.2110  FERC interconnection rule within 1 yr -> IX 10% faster from month 24 [A]
  Sec.2213  renewable ROW application deadlines -> public-land intake 12 -> 4 mo [A]
  Sec.2229  geothermal on leases not a major Federal action -> geothermal mostly CE
"""
import numpy as np, json, sys

T = 180                      # months simulated (Nov 2026 -> Nov 2041)
TURNOVERS = [26, 74, 122, 170]   # Jan 2029, 2033, 2037, 2041

# arr: projects/month; nex: share with federal nexus; path: [CE,EA,EIS] given nexus;
# eis: EIS median months; lit: P(sued | EIS); halt: P(halted | hostile turnover, permitted & not online)
TYPES = {
  "Solar":          dict(arr=35,  mw=150, nex=.15, path=[.10,.60,.30], eis=26, lit=.45, halt=.05, build=18, ix=True,  pub=True,  nonnepa=0),
  "Storage":        dict(arr=40,  mw=120, nex=.10, path=[.50,.45,.05], eis=30, lit=.20, halt=.01, build=12, ix=True,  pub=False, nonnepa=0),
  "Onshore wind":   dict(arr=7,   mw=200, nex=.30, path=[.10,.50,.40], eis=43, lit=.45, halt=.10, build=24, ix=True,  pub=True,  nonnepa=0),
  "Offshore wind":  dict(arr=.5,  mw=800, nex=1.0, path=[0,0,1],       eis=30, lit=.60, halt=.80, build=36, ix=True,  pub=False, nonnepa=0),
  "Gas":            dict(arr=5,   mw=600, nex=.25, path=[.10,.60,.30], eis=30, lit=.50, halt=.03, build=30, ix=True,  pub=False, nonnepa=0),
  "Geothermal":     dict(arr=1,   mw=40,  nex=.90, path=[.30,.60,.10], eis=30, lit=.33, halt=.01, build=30, ix=True,  pub=True,  nonnepa=0),
  "Transmission":   dict(arr=2,   mw=0,   nex=.60, path=[.15,.45,.40], eis=36, lit=.31, halt=.03, build=36, ix=False, pub=False, nonnepa=0),
  "Hydro relicense":dict(arr=2.5, mw=50,  nex=1.0, path=[0,.40,.60],   eis=30, lit=.20, halt=.01, build=0,  ix=False, pub=False, nonnepa=48),
}
GEN = [k for k, v in TYPES.items() if v["ix"]]

BASE = dict(enforced=False, deadline={"EA": 12, "EIS": 24}, enf_lag=4, ce_shift=0.0, recond=0.0, geo_path=None,
            intake_pub=12, intake_oth=3, esa=3, esa_share=.25, nonnepa_mult=1.0,
            lit_ea=.03, lit_ce=.002, suit_mult=1.0, pause=.5, lit_med=24, p_loss=.25, trunc_loss_mult=1.6,
            vacatur=True, remand=12, p_kill_vac=.2,
            ix_med=40, ix_speedup=1.0, halt_mult=1.0, halt_len=8, p_kill_halt=.25, hazard=None, n_scale=1.0)
BAAJA = dict(enforced=True, ce_shift=.10, recond=.25, geo_path=[.85,.13,.02], intake_pub=4, esa=2, nonnepa_mult=.75,
             suit_mult=.55*.6, pause=.15, lit_med=12, vacatur=False, remand=6, ix_speedup=0.9, halt_mult=.1)
SCEN = {
  "Baseline (current law)": {},
  "BAAJA (all levers)": BAAJA,
  "BAAJA: NEPA + courts only (Div. A)": {k: v for k, v in BAAJA.items() if k not in ("recond","geo_path","intake_pub","ix_speedup","nonnepa_mult")},
  "BAAJA without Sec.1401": dict(BAAJA, halt_mult=1.0),
}


def simulate(p, seed, hostile_to):
    """hostile_to: list per turnover of 'renew' or 'fossil' (drawn per run)."""
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
        trunc = np.zeros(n, bool); cut = np.zeros(n)
        if p["enforced"]:
            cap = np.where(kind == 1, p["deadline"]["EA"], np.where(kind == 2, p["deadline"]["EIS"], np.inf)) + p["enf_lag"]
            trunc = D > cap; cut = np.where(trunc, 1 - cap / D, 0); D = np.minimum(D, cap)
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
        if p["vacatur"]:
            vac = lost & (rng.random(n) < .5)
            delay += np.where(vac, L * (~paused) + p["remand"], 0)
            killed |= vac & (rng.random(n) < p["p_kill_vac"])
        tPermit = tP + delay
        # interconnection (parallel)
        IX = np.where(ty["ix"], p["ix_med"] * rng.lognormal(0, .5, n), 0)
        if p["ix_speedup"] != 1:
            after = np.clip(np.minimum(IX, t0 + IX - 24), 0, None)   # study months falling after the rule (month 24)
            IX = IX - after * (1 - p["ix_speedup"])
        tStart = np.maximum(tPermit, t0 + IX)
        tCOD = tStart + ty["build"]
        # executive halts after hostile turnovers (permitted, not yet online)
        halted = np.zeros(n, bool)
        for k, tt in enumerate(TURNOVERS):
            hostile = (hostile_to[k] == "renew") == (name in ("Solar", "Onshore wind", "Offshore wind", "Storage", "Transmission"))
            if not hostile or name in ("Geothermal", "Hydro relicense"):
                continue
            live = (tPermit <= tt) & (tCOD > tt) & nexus & ~killed
            h = live & (rng.random(n) < ty["halt"] * p["halt_mult"])
            halted |= h
            killed |= h & (rng.random(n) < p["p_kill_halt"])
            tCOD = np.where(h, tCOD + p["halt_len"], tCOD); delay += np.where(h, p["halt_len"], 0)
        # sponsor attrition: commercial withdrawal hazard while waiting; paused months weigh double
        wait = (tStart - t0) + delay
        W = rng.geometric(p["hazard"], n) if ty["ix"] else np.full(n, 10**6)
        withdrawn = W < wait
        done = ~withdrawn & ~killed
        rows.append(dict(type=name, t0=t0, nexus=nexus, sued=sued, trunc=trunc, cut=cut, halted=halted,
                         done=done, tCOD=tCOD, mw=ty["mw"], wait=tCOD - t0))
    return rows


def summarize(rows):
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
            mean_review_cut=float(r["cut"][r["trunc"]].mean()) if r["trunc"].any() else 0.0)
    return out


def run_scenario(over, n_runs, hazard):
    p = dict(BASE); p.update(over); p["hazard"] = hazard
    acc = []
    for s in range(n_runs):
        rr = np.random.default_rng(1000 + s)
        hostile = list(rr.choice(["renew", "fossil"], len(TURNOVERS)))  # same draws across scenarios
        acc.append(summarize(simulate(p, s, hostile)))
    return {ty: {m: float(np.nanmean([a[ty][m] for a in acc])) for m in acc[0][ty]} for ty in TYPES}


def calibrate(target=0.19):
    """Attrition hazard so the current-law completion rate of queued generation ~= LBNL's 19%."""
    lo, hi = 0.001, 0.2
    for _ in range(18):
        h = (lo + hi) / 2
        p = dict(BASE, hazard=h, n_scale=0.5)
        s = summarize(simulate(p, 7, ["renew", "fossil", "renew", "fossil"]))
        n = sum(s[t]["n"] for t in GEN); c = sum(s[t]["completion_rate"] * s[t]["n"] for t in GEN) / n
        lo, hi = (h, hi) if c > target else (lo, h)
    return (lo + hi) / 2


if __name__ == "__main__":
    n_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    h = calibrate()
    res = {s: run_scenario(o, n_runs, h) for s, o in SCEN.items()}
    json.dump(dict(hazard=h, results=res), open("baaja_electricity_results.json", "w"), indent=1)
    print(f"calibrated monthly withdrawal hazard = {h:.4f}")
    for s, r in res.items():
        gw = sum(v["GW_online"] for v in r.values())
        print(f"\n== {s}: {gw:,.0f} GW online by Nov 2041; transmission projects online {r['Transmission']['projects_online']:.0f}")
        print(f"{'type':16s}{'complete%':>10s}{'GW':>9s}{'mo->COD':>9s}{'suits':>7s}{'halted':>8s}{'trunc%':>8s}{'cut%':>6s}")
        for ty, v in r.items():
            print(f"{ty:16s}{100*v['completion_rate']:10.1f}{v['GW_online']:9.1f}{v['median_months_to_COD']:9.0f}"
                  f"{v['suits']:7.0f}{v['halted']:8.1f}{100*v['truncated_share']:8.0f}{100*v['mean_review_cut']:6.0f}")
