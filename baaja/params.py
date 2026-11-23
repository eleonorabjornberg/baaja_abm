"""v5 parameters: every value is [D] (from data, source given) or an entry in ASSUMPTIONS (low, central, high).

Data files (data/*.json) are produced by the extractors in data/; see README for sources.
Time: month 0 = Nov 2026 (forward runs) or Jan 2010 (backcast). Horizon T months.
"""
import json as _json
import os as _os

_D = _os.path.join(_os.path.dirname(__file__), "..", "data")
_load = lambda f: _json.load(open(_os.path.join(_D, f)))
LBNL, ENGINE, NEXUS, CEQ, CASES = (_load("lbnl_targets.json"), _load("engine_inputs.json"),
                                   _load("federal_nexus_combined.json"), _load("ceq_eis_targets.json"),
                                   _load("nepa_case_targets.json"))
FED = _load("federal_nexus_targets.json")
LIMIT = _load("limitation_experiment.json")["late_adapt"]   # [D] highway/transit 150-180 day limit vs other NEPA suits
IXB = _load("interconnection_benchmark.json")              # [D] ERCOT vs CAISO/MISO request -> IA times
BLM = _load("blm_eplanning_targets.json")                  # [D] BLM ePlanning energy NEPA register
E860M = _load("eia860m_targets.json")                      # [D] EIA-860M late-stage completion, planned pipeline
MLRSF = _load("mlrs_filing_targets.json")["intake_months"]  # [D] BLM MLRS solar ROW filing -> notice
RGN = _load("region_targets.json")                          # [D] LBNL requests by region (Phase 1)
REGIONS = RGN["meta"]["regions_iso"] + RGN["meta"]["regions_non_iso"]
RTO_IDX = [REGIONS.index(r) for r in RGN["meta"]["ferc_rto"]]   # Sec.2106 reaches these (not ERCOT)


def _region_share(t):
    out = {}
    for kind in ("new", "active"):
        out[kind] = {}
        for m, names in ((0, RGN["meta"]["regions_iso"]), (1, RGN["meta"]["regions_non_iso"])):
            sh = RGN["types"][t][f"{kind}_share"][str(m)]
            w = [sh[r] for r in names]; tot = sum(w) or 1.0
            out[kind][m] = ([REGIONS.index(r) for r in names], list(__import__("numpy").cumsum([x / tot for x in w])))
    return out


REGION_SHARE = {t: _region_share(t) for t in RGN["types"]}
SINCE_IA = {t: v["since_ia_quantiles"] for t, v in RGN["types"].items() if v.get("since_ia_quantiles")}   # [D]
IA_TO_COD = {t: v["ia_to_cod_median_recent"] for t, v in RGN["types"].items() if v.get("ia_to_cod_median_recent")}  # [D]
_GAS2025 = ENGINE["lbnl"]["arrivals_by_year"]["Gas"]["2025"] / 12 / LBNL["types"]["Gas"]["arr_per_month"]
MIN_N = 30

T = 180
TURNOVERS = [26, 74, 122, 170]            # Jan 2029, 2033, 2037, 2041
BACKCAST = dict(T=192, start_year=2010, turnovers=[84, 132, 180], politics=["renew", "fossil", "renew"])

# ---- assumptions: (low, central, high, note). Everything not listed here is [D]. -----------------------------
ASSUMPTIONS = {
    # permitting
    "ea_share_nonEIS":   (round(BLM["ea_share_nonEIS"]["all"], 2), round(BLM["ea_share_nonEIS"]["project"], 2), 0.67,
                          "share of non-EIS federal reviews that are EAs (rest CEs/DNAs) [D: BLM ePlanning; central = actions "
                          "naming >= 20 MW (n=49), low = all energy actions, high = central + 95% binomial margin]"),
    "intake_pub":        (round(MLRSF["median_ci90"][0], 1), round(MLRSF["median"], 1), round(MLRSF["median_ci90"][1], 1),
                          "median months from federal-land right-of-way filing to the NEPA notice, current law [D: BLM "
                          "MLRS solar grants, n=60; range = 90% bootstrap CI of the median; each project draws its own "
                          "intake around this median with the observed log-sd]"),
    "intake_oth":        (1, 3, 6, "months from application to start of review, other federal nexus"),
    "nonnepa_hydro":     (36, 48, 60, "hydro relicensing months outside NEPA (s.401 certification, license terms)"),
    "lit_ea":            (0.0025, 0.005, 0.01, "P(sued | EA) for gas and hydro: all-sector case data x ~10,000 EAs/yr (CEQ estimate)"),
    "lit_ce":            (0.0001, 0.0002, 0.0005, "P(sued | CE) for gas and hydro: same method, ~100,000 CEs/yr"),
    "lit_data_mult":     (0.5, 0.75, 1.0, "scale on the energy-specific EA/CE suit rates (renewables, transmission) [D: suits / "
                          "BLM + DOE reviews, 2012-21]; < 1 because other agencies' reviews are missing from the denominator"),
    "p_kill_vac":        (0.1, 0.2, 0.4, "P(project cancelled | permit vacated)"),
    "remand_months":     (6, 12, 18, "delay after vacatur, current law"),
    "delay_weight":      (0.0, 1.0, 1.0, "weight of litigation/halt delay in the sponsor's withdrawal clock"),
    "halt_len":          (4, 8, 12, "months a halted project is stopped"),
    "p_kill_halt":       (0.1, 0.25, 0.5, "P(cancelled | halted)"),
    "halt_mult_other":   (0.5, 1.0, 2.0, "multiplier on halt probabilities for technologies other than offshore wind"),
    # BAAJA levers whose size the text does not fix
    "deadline_bind":     (0.25, 0.5, 1.0, "Sec.1106: share of over-deadline EA/EIS reviews actually cut to deadline + 4 months"),
    "ce_shift":          (0.0, 0.10, 0.25, "Sec.1105/1108: share of EAs that become CEs"),
    "recond_ce":         (0.10, 0.25, 0.50, "Sec.2102: extra share of transmission EAs that become CEs"),
    "geo_ce":            (0.5, 0.85, 1.0, "Sec.2229: share of geothermal reviews that become non-major actions"),
    "intake_pub_baaja":  (3, 4, 6, "Sec.2213: months to start of review on federal land (30-day completeness, 90-day NOI)"),
    "comply_2213":       (0.25, 0.5, 1.0, "Sec.2213: share of new federal-land applications whose intake deadlines are met. "
                          "Same range as Sec.1106 (deadline_bind); 2213 has no sponsor petition or court order to enforce it, "
                          "so its compliance is not assumed higher than 1106's"),
    "nonnepa_hydro_baaja": (30, 36, 42, "Sec.1202: hydro months outside NEPA with the s.401 clock"),
    "late_adapt":        (round(LIMIT["low"], 2), round(LIMIT["central"], 2), LIMIT["high"],
                          "Sec.1110/2201: share of would-be late filers who file within 150 days instead [D: FHWA/FTA "
                          "limitation natural experiment, data/limitation_experiment.json; high end = all late highway "
                          "suits lacked a notice]"),
    "exhaust_injury":    (0.6, 0.8, 0.95, "Sec.1110: share of timely suits that pass comment exhaustion + direct injury"),
    "suit_payoff":       (0.4, 0.6, 1.0, "Sec.1110: suits filed relative to current law when the only remedy is remand"),
    "inj_nonNEPA":       (0.0, 0.3, 0.5, "Sec.1110: share of injunctions that rest on non-NEPA laws (still allowed)"),
    "lit_months_baaja":  (8, 12, 16.4, "Sec.1110/2201: months in litigation with appeals-court original jurisdiction + expedited review"),
    "halt_mult_1401":    (0.1, 0.5, 1.0, "Sec.1401: residual halt probability relative to current law. The Senate-passed "
                          "text adds exception (F), action 'taken pursuant to any applicable law or regulation', which "
                          "could cover stop-work orders like 2025's (issued under existing regulations); high = the "
                          "exception swallows the rule, low = courts read it narrowly"),
    "ix_2110":           (0.0, 0.0, 0.05, "Sec.2110: interconnection study time cut (text sets no target)"),
    "ix_2106":           (0.0, 0.0, round(IXB["ercot_gap_cut"], 2),
                          "Sec.2106: interconnection study time cut from consolidated planning, Transmission Organizations "
                          "(RTO/ISO markets) only [floor: no measured effect of past reforms, and FERC may find existing "
                          "processes compliant (2106(d)); ceiling: ERCOT's pace, data/interconnection_benchmark.json]"),
    "ix_rule_month":     (24, 36, 48, "months until Sec.2106/2110 rules affect studies"),
    "build_months":      (None, None, None, "post-IA months to operation: calibrated to LBNL time to COD, not assumed"),
}
A = {k: v[1] for k, v in ASSUMPTIONS.items()}   # central values

# ---- technologies ---------------------------------------------------------------------------------------------
_eis_all = CEQ["meta"]["all_eis_median_months"]


def _ceq(t, key):
    v = CEQ["types"].get(t)
    return v[key] if v else None


TYPES = {}
for t, d in LBNL["types"].items():
    TYPES[t] = dict(arr=d["arr_per_month"],
                    mw=round(d["mw_built_recent"]) if d.get("n_built_recent", 0) >= MIN_N else (round(d["mw_built"]) if d["n_built"] >= MIN_N else None),
                    ix_med=d["ix_median"] if d["n_ix"] >= MIN_N else 40.0, ix_sigma=d["ix_logsd"] if d["n_ix"] >= MIN_N else 0.5,
                    completion_target=d["completion"], cod_target=d["cod_median"] if d["n_cod"] >= MIN_N else None, ix=True)
TYPES["Offshore wind"]["mw"] = 800        # [A] 3 built projects only; current BOEM projects are 700-1,100 MW
TYPES["Geothermal"]["mw"] = 40            # [A] 10 built projects
# storage includes battery components of hybrid requests [D] LBNL (54.9 requests/month, 117 MW built)
_h = ENGINE["lbnl"]["hybrid_storage"]; _s = TYPES["Storage"]
_s["mw"] = round((_s["arr"] * _s["mw"] + _h["req_per_month_2021_25"] * _h["mw_built_mean"]) / (_s["arr"] + _h["req_per_month_2021_25"]))
_s["arr"] += _h["req_per_month_2021_25"]
# storage completion: v5 raised the target from LBNL's 2000-20 cohort (9.1%) to solar's x the EIA-860M late-stage
# ratio (13.4%) because the backcast ran at 0.37-0.54 of EIA additions. That shortfall came from the 62-month
# post-IA time (below). With the measured 29 months, LBNL's own completion rate gives a backcast of 1.14 (2018-25),
# so Phase 1 returns to the direct measure [D]; the 860M-ratio value is kept for reference.
TYPES["Storage"]["completion_target_lbnl_2000_20"] = TYPES["Storage"]["completion_target"]
TYPES["Storage"]["completion_target_860m_ratio"] = TYPES["Solar"]["completion_target"] * E860M["storage_vs_solar"]
TYPES["Storage"]["completion_target"] = TYPES["Storage"]["completion_target_lbnl_2000_20"]
# storage: the 2015-18 request -> COD cohort (34 projects) predates the battery boom and implied 62 months from IA to
# COD; batteries reaching operation 2022-25 took a median 29 months [D: LBNL, n=49]. Post-IA time is set to that value
# instead of being calibrated (Phase 1).
TYPES["Storage"]["cod_target_lbnl_2015_18"] = TYPES["Storage"]["cod_target"]
TYPES["Storage"]["cod_target"] = None
# ---- demand/policy regimes: requests per technology relative to the 2021-25 mean [D] LBNL ----------------------
# "2025": each technology at its 2025 request rate. 2025 mixes data-center demand (gas x2.1, geothermal x2.2) with
# federal policy (tax-credit phase-outs, actions against wind/solar: solar x0.65, offshore wind x0.1); the data
# cannot separate the two. Transmission and hydro relicensing have no request data and stay at 1.
def _ratio2025(t):
    a = ENGINE["lbnl"]["arrivals_by_year"][t]
    return a["2025"] / (sum(a[str(y)] for y in range(2021, 2026)) / 5)
_hy = ENGINE["lbnl"]["hybrid_storage"]["arrivals_by_year"]
_st = ENGINE["lbnl"]["arrivals_by_year"]["Storage"]
REGIMES = {"2021-25": {}, "2025": {t: _ratio2025(t) for t in ("Gas", "Geothermal", "Offshore wind", "Onshore wind", "Solar")}}
REGIMES["2025"]["Storage"] = (_st["2025"] + _hy["2025"]) / (sum(_st[str(y)] + _hy[str(y)] for y in range(2021, 2026)) / 5)
TYPES["Transmission"] = dict(arr=2.0, mw=0, ix=False, completion_target=None, cod_target=None, ix_med=0, ix_sigma=.5)  # [A] arrivals
TYPES["Hydro relicense"] = dict(arr=2.5, mw=50, ix=False, completion_target=None, cod_target=None, ix_med=0, ix_sigma=.5)  # [A]

_n = NEXUS["types"]
_WHCP = _load("wind_hcp_targets.json")["hcp_share_MW"]   # [D] wind HCPs (ESA s.10 permits with NEPA), none overlap other hooks
for t, ty in TYPES.items():
    ty["nex"] = sum(_n[t]["combined_net"]) / 2 if t in _n else (0.6 if t == "Transmission" else 1.0)   # [D] / [A] transmission / statute hydro
    ty["nex_range"] = tuple(_n[t]["combined_net"]) if t in _n else ((0.4, 0.8) if t == "Transmission" else (1.0, 1.0))
    if t == "Onshore wind":
        ty["nex"] += _WHCP; ty["nex_range"] = tuple(x + _WHCP for x in ty["nex_range"])
    ty["eis_target"] = _ceq(t, "eis_per_year") or 0.0        # [D] CEQ final EISs/yr 2015-24
    m, n_all = _ceq(t, "median_months_noi_to_feis"), _ceq(t, "n_all") or 0
    ty["eis_med"] = m if (m and n_all >= 10) else _eis_all  # [D] CEQ by technology if n >= 10, else all EISs (37 mo)
    _bm = BLM["median_months"].get(t, {})                   # [D] BLM ePlanning medians where n >= 20, else DOE EA 12 / USFS CE 4
    ty["ea_med"] = _bm["EA"]["median"] if _bm.get("EA", {}).get("n", 0) >= 20 else 12.0
    ty["ce_med"] = _bm["CE"]["median"] if _bm.get("CE", {}).get("n", 0) >= 20 else 4.0
    ty["pub"] = t in ("Solar", "Onshore wind", "Geothermal")  # rights-of-way on federal land (Sec.2213 eligible)
    ty["nonnepa"] = t == "Hydro relicense"
# gas: federal nexus is mostly Corps individual permits (28 of 33 points), each with a Corps EA [D]
TYPES["Gas"]["ea_share_nonEIS"] = min(1.0, _n["Gas"]["corps_individual_net"] / TYPES["Gas"]["nex"])
for _t, _g in (("Solar", "Renewable"), ("Onshore wind", "Renewable"), ("Offshore wind", "Renewable"), ("Geothermal", "Renewable"),
               ("Storage", "Renewable"), ("Transmission", "Transmission")):   # [D] energy-specific suit rates
    TYPES[_t]["lit_ea_data"] = BLM["lit_rate"][_g]["lit_ea"]; TYPES[_t]["lit_ce_data"] = BLM["lit_rate"][_g]["lit_ce"]
TYPES["Gas"]["ea_med"] = ENGINE["corps"]["standard_permit"]["median_months"] + 2   # [D] 5.7 mo notice->decision, +2 pre-notice [A]

# EIS litigation rates [D] Bennon & Wilson 2023 / RFF (solar ~2/3, wind .38, transmission .31, pipelines .50, geo 1/3)
LIT_EIS = {"Solar": .45, "Onshore wind": .40, "Offshore wind": .60, "Gas": .50, "Geothermal": .33, "Transmission": .31,
           "Hydro relicense": .20, "Storage": .20}   # offshore wind, hydro, storage [A]
for t in TYPES:
    TYPES[t]["lit_eis"] = LIT_EIS[t]

# ---- courts [D] nepa_case_targets.json (1,821 NEPA cases 2001-22) ---------------------------------------------
CHALLENGERS = ["National NGO", "Local group / residents", "Tribe", "State / local government", "Business"]
COURT_GROUP = {"Solar": "Renewable", "Onshore wind": "Renewable", "Offshore wind": "Renewable", "Geothermal": "Renewable",
               "Storage": "Renewable", "Gas": "Fossil infrastructure", "Transmission": "Transmission", "Hydro relicense": "Hydro"}
_g = CASES["by_group"]
CHALLENGER_MIX = {t: [_g[COURT_GROUP[t]]["lead_mix"][c] for c in CHALLENGERS] for t in TYPES}
for t, m in CHALLENGER_MIX.items():          # renormalise (unmapped lead types dropped)
    s = sum(m); CHALLENGER_MIX[t] = [x / s for x in m]
WIN = {t: _g[COURT_GROUP[t]]["challenger_win"] for t in TYPES}                    # P(challenger wins NEPA claim)
WIN_REL = [CASES["by_lead_challenger"][c]["win_rel"] for c in CHALLENGERS]
LATE_SHARE = [CASES["by_lead_challenger"][c]["share_filed_after_150_days"] for c in CHALLENGERS]
INJ = CASES["energy"]["injunction_share"]                  # 9.5% of energy cases
VAC = CASES["energy"]["vacatur_share_of_remands"]          # 69% of energy remands are with vacatur
LIT_MONTHS = ENGINE["cases"]["months_in_litigation"]["district_energy"]["median_months"]   # 12.8
TRUNC_LOSS = 1.6   # [A] relative odds that a truncated review loses in court (no data)

# ---- executive halts: P(halted | hostile turnover, permitted, not online) -------------------------------------
HALT = {"Offshore wind": .8,   # [D] 2025: stop-work orders on all five projects under construction
        "Solar": .05, "Onshore wind": .10, "Storage": .01, "Gas": .03, "Transmission": .03, "Geothermal": 0, "Hydro relicense": 0}  # [A]
RENEWABLE_SIDE = ("Solar", "Onshore wind", "Offshore wind", "Storage", "Transmission")

# ---- reporting ------------------------------------------------------------------------------------------------
GROUPS = {"Renewable (new)": ["Solar", "Onshore wind", "Offshore wind", "Geothermal"],
          "Renewable (retained hydro)": ["Hydro relicense"], "Fossil (gas)": ["Gas"], "Storage": ["Storage"]}
CF = {"Solar": .24, "Onshore wind": .34, "Offshore wind": .42, "Gas": .56, "Geothermal": .70,   # [D] EIA EPM 2023-24;
      "Hydro relicense": .36, "Storage": 0.0, "Transmission": 0.0}                              # offshore [A] NREL ATB
GEN = [t for t, v in TYPES.items() if v["ix"]]
POLITICS = {"random (default)": None, "always hostile to renewables": ["renew"] * 4, "always hostile to fossil": ["fossil"] * 4}
UTILITY_OWNED = {t: FED["types"][t]["utility_owned_share_MW"] for t in GEN}   # [D] EIA-860, new MW 2015-25

# ---- scenarios -------------------------------------------------------------------------------------------------
BASE = dict(T=T, turnovers=TURNOVERS, n_scale=1.0, seed_queue=True, arrivals=None, start_year=2026,
            hazard=None, build=None, p_eis=None, nex_mult=1.0,
            ea_share_nonEIS=A["ea_share_nonEIS"], intake_pub=A["intake_pub"], intake_oth=A["intake_oth"],
            intake_pub_logsd=MLRSF["log_sd"],
            nonnepa_hydro=A["nonnepa_hydro"], esa_months=3.0, esa_share=0.25, regime="2021-25",
            intake_pub_2213=None, nonnepa_hydro_1202=None,    # BAAJA overrides (None = current-law value applies)
            comply_2213=A["comply_2213"],                     # only matters when intake_pub_2213 is set
            lit_ea=A["lit_ea"], lit_ce=A["lit_ce"], lit_data_mult=A["lit_data_mult"], p_kill_vac=A["p_kill_vac"], remand_months=A["remand_months"],
            delay_weight=A["delay_weight"], halt_len=A["halt_len"], p_kill_halt=A["p_kill_halt"],
            halt_mult_other=A["halt_mult_other"],
            # current law: no BAAJA levers
            deadline_bind=0.0, ce_shift=0.0, recond_ce=0.0, geo_ce=0.0, ce_cap=None,
            court="current", late_adapt=A["late_adapt"], exhaust_injury=A["exhaust_injury"], suit_payoff=1.0,
            inj_nonNEPA=A["inj_nonNEPA"], lit_months=LIT_MONTHS, halt_mult=1.0,
            overdue_months=12.0, overdue=None,          # overdue: calibrated per technology
            ix_cut=0.0, ix_cut_rto=0.0, ix_rule_month=A["ix_rule_month"],   # all providers / RTO-ISO only
            harm_w={"CE": 0.0, "EA": 0.3, "EIS": 1.0}, harm_mw_transmission=300)

LEVERS = {   # BAAJA, central values, grouped by simulation
    "permitting": dict(deadline_bind=A["deadline_bind"], ce_shift=A["ce_shift"], recond_ce=A["recond_ce"], geo_ce=A["geo_ce"],
                       intake_pub_2213=A["intake_pub_baaja"], nonnepa_hydro_1202=A["nonnepa_hydro_baaja"], esa_months=2.0, ce_cap=12),
    "litigation": dict(court="baaja", suit_payoff=A["suit_payoff"], lit_months=A["lit_months_baaja"]),
    "grid": dict(ix_cut=A["ix_2110"], ix_cut_rto=A["ix_2106"]),
    "certainty": dict(halt_mult=A["halt_mult_1401"]),
}
BAAJA = {k: v for d in LEVERS.values() for k, v in d.items()}
