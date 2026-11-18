"""Parameters, calibration notes and scenarios (moved unchanged from v3).

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
            ix_med=40, ix_speedup=1.0, ix_rule_month=24, halt_mult=1.0, halt_len=8, p_kill_halt=.25, hazard=None, n_scale=1.0,
            delay_weight=1.0,                       # weight of litigation/halt delay in the attrition wait (see README)
            harm_w={"CE": 0.0, "EA": 0.3, "EIS": 1.0}, harm_mw_transmission=300)   # harm index weights [A]
BAAJA = dict(enforced=True, ce_shift=.10, recond=.25, geo_path=[.85,.13,.02], intake_pub=4, esa=2, nonnepa_mult=.75,
             suit_mult=.55*.6, pause=.15, lit_med=12, vacatur=False, remand=6, ix_speedup=0.9, halt_mult=.1)
SCEN = {
  "Baseline (current law)": {},
  "BAAJA (all levers)": BAAJA,
  "BAAJA: NEPA + courts only (Div. A)": {k: v for k, v in BAAJA.items() if k not in ("recond","geo_path","intake_pub","ix_speedup","nonnepa_mult")},
  "BAAJA without Sec.1401": dict(BAAJA, halt_mult=1.0),
}


# ---- renewable vs fossil reporting -------------------------------------------------------------------
# Groups. Hydro relicensing keeps existing capacity online rather than adding new capacity, so it is
# reported as "renewable (retained)" and kept out of new-build totals. Storage shifts energy, it does not
# generate it, so it has no TWh.
GROUPS = {
    "Renewable (new)": ["Solar", "Onshore wind", "Offshore wind", "Geothermal"],
    "Renewable (retained hydro)": ["Hydro relicense"],
    "Fossil (gas)": ["Gas"],
    "Storage": ["Storage"],
}
# Annual capacity factors, for turning GW into TWh/yr of new generation.
#   solar .24, onshore wind .34, gas .56, geothermal .70, hydro .36   [D] EIA Electric Power Monthly,
#   2023-24 US fleet averages (gas = combined cycle, matching the 600 MW project size)
#   offshore wind .42                                                  [A] NREL ATB, no mature US fleet yet
CF = {"Solar": .24, "Onshore wind": .34, "Offshore wind": .42, "Gas": .56, "Geothermal": .70,
      "Hydro relicense": .36, "Storage": 0.0, "Transmission": 0.0}

# Political paths for the executive-halt agent (which side each of the 4 administrations is hostile to).
POLITICS = {
    "random (default)": None,                       # drawn per run, same draws across scenarios
    "always hostile to renewables": ["renew"] * 4,
    "always hostile to fossil": ["fossil"] * 4,
}

# Lever decomposition for the renewable vs fossil question: each provision alone, and full BAAJA minus each.
LEVER_KEYS = {
    "Sec.1106 enforceable deadlines": ["enforced"],
    "Sec.1108/2102 CE adoption + reconductoring": ["ce_shift", "recond"],
    "Sec.1110 judicial review": ["suit_mult", "pause", "lit_med", "vacatur", "remand"],
    "Sec.1202/1302 CWA 401 + ESA clocks": ["nonnepa_mult", "esa"],
    "Sec.1401 permit certainty": ["halt_mult"],
    "Sec.2110 interconnection rule": ["ix_speedup"],
    "Sec.2213 renewable ROW deadlines": ["intake_pub"],
    "Sec.2229 geothermal CE": ["geo_path"],
}
