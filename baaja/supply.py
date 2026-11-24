"""Supply and resource adequacy by region and year (Phase 1).

Installed capacity = existing fleet (EIA-860, end-2025) - retirements + model additions (projects reaching operation
from the interconnection queue, by region). On-peak accredited capacity ('firm' in the code) follows NERC's reserve-margin convention: dispatchable
resources at net summer capacity; wind, solar and batteries at an on-peak share; plus NERC's net firm transfers.
Reserve margin = firm / net internal demand - 1, compared with NERC's reference margin level (RML).

Model year k (months 12k..12k+11 from Nov 2026) is labelled peak year 2027 + k: capacity online by October counts
for the next summer peak. Projects built from 2026 do not retire before 2041.

Data [D]: data/fleet_targets.json (EIA-860/860M/923), data/demand_targets.json (NERC 2025 LTRA),
data/engine_inputs.json (age at retirement). Assumptions [A]: SUPPLY_ASSUMPTIONS below, each with a range.
"""
import numpy as np

from .params import ENGINE, REGIONS, _load

FLEET = _load("fleet_targets.json")
DEMAND = _load("demand_targets.json")
YEARS = list(range(2027, 2042))                      # peak years covered by the 15-year run
NERC_YEARS = DEMAND["meta"]["years"]                 # 2026-2035

# (low, central, high, note) - post-processing assumptions; they do not change the queue simulation
SUPPLY_ASSUMPTIONS = {
    "ret_hazard_old":   (0.01, 0.03, 0.06, "annual retirement probability of coal, gas and oil units with no announced "
                         "retirement once past the median age at retirement (coal 56, gas/oil 45 years) [A; ages D: EIA-860]"),
    "ret_announced":    (0.6, 1.0, 1.0, "share of announced retirements (EIA-860/860M) that happen on schedule; low = "
                         "delays such as the 2025 DOE 202(c) orders keeping coal units open"),
    "elcc_decline":     (0.0, 0.5, 1.0, "how far on-peak shares of wind, solar and batteries fall by 2041: 0 = NERC 2025 "
                         "national values throughout, 1 = PJM's 2041/42 preliminary ELCC class ratings, linear in time "
                         "(not in PJM, whose installed reserve margin already rises with the mix)"),
    "demand_growth_mult": (0.5, 1.0, 1.5, "multiplier on NERC's forecast growth in net internal demand (2026-35 path, "
                           "extended to 2041 at the 2030-35 rate)"),
}
SA = {k: v[1] for k, v in SUPPLY_ASSUMPTIONS.items()}

DISPATCHABLE = ["Coal", "Gas CC", "Gas CT", "Gas ST", "Oil", "Nuclear", "Hydro", "Pumped storage", "Geothermal", "Other"]
VARIABLE = ["Onshore wind", "Offshore wind", "Solar", "Storage"]
# on-peak share of capacity. 2026: NERC 2025 LTRA, existing + Tier 1, North America, on-peak / nameplate (Figure 16):
# solar 101/194, wind 37/200, battery and hybrid 32/54. Offshore wind: onshore value x PJM offshore/onshore ratio
# (60%/34%, DY2028/29). 2041: PJM preliminary ELCC class ratings for DY2041/42 (solar = mean of fixed and tracking,
# storage = 4-hour).
ONPEAK_2026 = {"Solar": 101 / 194, "Onshore wind": 37 / 200, "Offshore wind": 37 / 200 * 60 / 34, "Storage": 32 / 54}
ONPEAK_2041_PJM = {"Solar": 0.075, "Onshore wind": 0.18, "Offshore wind": 0.26, "Storage": 0.20}
RET_AGE = {"Coal": ENGINE["eia860"]["retirement_age"]["Coal"]["median_age"],
           **{g: ENGINE["eia860"]["retirement_age"]["Gas"]["median_age"] for g in ("Gas CC", "Gas CT", "Gas ST", "Oil")}}
# model technology -> fleet group (new gas is counted with combined cycles)
MODEL_GROUP = {"Solar": "Solar", "Onshore wind": "Onshore wind", "Offshore wind": "Offshore wind", "Storage": "Storage",
               "Gas": "Gas CC", "Geothermal": "Geothermal"}
GROUPS = DISPATCHABLE + VARIABLE
CLASS = {"Renewable": ["Solar", "Onshore wind", "Offshore wind", "Geothermal", "Hydro"],
         "Gas": ["Gas CC", "Gas CT", "Gas ST"], "Storage": ["Storage", "Pumped storage"],
         "Coal and oil": ["Coal", "Oil"], "Nuclear": ["Nuclear"], "Other": ["Other"]}


# PJM's NERC reference margin is an installed reserve margin (LTRA 2025, RML summary table) that rises from 18.6% to
# 35.1% (2026-34) as the mix shifts to resources with low accredited value, and NERC counts PJM's solar and wind near
# installed capacity rights (11.3 and 5.3 GW in 2026 vs EIA nameplate 18.0 and 11.7). The falling value of those
# resources is therefore already in PJM's RML: in PJM the on-peak shares are held at their 2026 values, so the
# decline is not counted twice. Elsewhere the RML is flat and on-peak shares carry the decline (elcc_decline).
INSTALLED_RML = ("PJM",)


def onpeak(group, year, sa, region=None):
    if group not in ONPEAK_2026:
        return 1.0
    f = (year - 2026) / 15
    dec = 0.0 if region in INSTALLED_RML else sa["elcc_decline"]
    c41 = ONPEAK_2026[group] + dec * (ONPEAK_2041_PJM[group] - ONPEAK_2026[group])
    return ONPEAK_2026[group] + min(max(f, 0), 1) * (c41 - ONPEAK_2026[group])


def existing_fleet(sa=SA):
    """MW by region, group, year (array [region, group, year]) after retirements."""
    out = np.zeros((len(REGIONS), len(GROUPS), len(YEARS)))
    for i, r in enumerate(REGIONS):
        cap = FLEET["capacity"].get(r, {})
        for j, g in enumerate(GROUPS):
            base = cap.get(g, 0.0)
            ann = FLEET["retirements"].get(r, {}).get(g, {})
            vint = FLEET["unannounced_by_vintage"].get(r, {}).get(g, {})
            for k, y in enumerate(YEARS):
                gone = sa["ret_announced"] * sum(v for yy, v in ann.items() if int(yy) <= y)
                if g in RET_AGE:
                    for oy, mw in vint.items():
                        n = max(0, y - max(2026, int(oy) + RET_AGE[g]))
                        gone += mw * (1 - np.exp(-sa["ret_hazard_old"] * n))
                out[i, j, k] = max(base - gone, 0.0)
    return out


def demand(sa=SA):
    """Net internal demand (MW) and RML by region and year [region, year]."""
    nid = np.zeros((len(REGIONS), len(YEARS))); rml = np.zeros_like(nid); tr = np.zeros_like(nid)
    for i, r in enumerate(REGIONS):
        d = DEMAND["regions"][r]
        path = np.array(d["net_internal_demand"], float)
        g_tail = d["growth_2030_35"]
        for k, y in enumerate(YEARS):
            if y <= NERC_YEARS[-1]:
                v = path[y - NERC_YEARS[0]]; j = y - NERC_YEARS[0]
            else:
                v = path[-1] * (1 + g_tail) ** (y - NERC_YEARS[-1]); j = len(NERC_YEARS) - 1
            nid[i, k] = path[0] * (v / path[0]) ** sa["demand_growth_mult"]
            rml[i, k] = d["reference_margin_level"][j]
            tr[i, k] = d["net_firm_transfers"][j]
    return nid, rml, tr


def additions(run):
    """Cumulative MW added by the model, [region, group, year], from summarize()['_online_region_year']."""
    out = np.zeros((len(REGIONS), len(GROUPS), len(YEARS)))
    for t, per_region in run["_online_region_year"].items():
        if t not in MODEL_GROUP:
            continue
        j = GROUPS.index(MODEL_GROUP[t])
        for i in range(len(REGIONS)):
            out[i, j, :] += np.cumsum(np.array(per_region[i][:len(YEARS)])) * 1000   # GW -> MW
    return out


def supply(run, sa=SA, fleet=None, dem=None):
    """One model run -> dict of arrays by region and year (MW unless noted)."""
    fleet = existing_fleet(sa) if fleet is None else fleet
    nid, rml, tr = demand(sa) if dem is None else dem
    add = additions(run)
    inst = fleet + add
    fac = np.array([[[onpeak(g, y, sa, r) for y in YEARS] for g in GROUPS] for r in REGIONS])   # [region, group, year]
    # existing fleet scaled to NERC's existing-certain basis (FIRM_SCALE). Additions take the same scale where it is
    # below 1 (MISO counts accredited capacity, and the derating applies to new units too), but are not scaled up
    # where it is above 1 (CAISO, SPP: area boundaries and imports, which do not apply to new units).
    firm = ((fleet * fac).sum(axis=1) * FIRM_SCALE[:, None] + (add * fac).sum(axis=1) * np.minimum(FIRM_SCALE, 1.0)[:, None]
            + tr)
    cf = np.array([[FLEET["capacity_factor"].get(r, {}).get(_cfkey(g), FLEET["meta"]["national_cf"].get(_cfkey(g), 0.0))
                    for g in GROUPS] for r in REGIONS]).clip(min=0)
    twh = (inst * cf[:, :, None]).sum(axis=1) * 8.766 / 1e3
    rm = firm / nid - 1
    out = dict(installed=inst.sum(axis=1), firm=firm, nid=nid, rml=rml, reserve_margin=rm,
               shortfall=np.maximum((1 + rml) * nid - firm, 0.0), twh=twh, added=add.sum(axis=1))
    for c, members in CLASS.items():
        out[f"installed|{c}"] = inst[:, [GROUPS.index(g) for g in members], :].sum(axis=1)
    return out


def _fleet_firm_2026(sa=SA):
    return np.array([sum(FLEET["capacity"].get(r, {}).get(g, 0.0) * onpeak(g, 2026, sa, r) for g in GROUPS) for r in REGIONS])


# [D] per-region factor putting the existing fleet on NERC's 2026 "existing-certain" basis (NERC excludes uncommitted
# merchant capacity, MISO counts accredited capacity, and NERC areas differ slightly from LBNL regions)
FIRM_SCALE = np.array([(DEMAND["regions"][r]["existing_certain_and_transfers"][0] - DEMAND["regions"][r]["net_firm_transfers"][0])
                       for r in REGIONS]) / _fleet_firm_2026()


def _cfkey(g):
    return "Gas" if g.startswith("Gas") else g


def check_2026(sa=SA):
    """Fleet firm capacity at end-2025 + NERC transfers vs NERC's 2026 existing-certain + transfers (MW)."""
    out = {}
    raw = _fleet_firm_2026(sa)
    for i, r in enumerate(REGIONS):
        tr = DEMAND["regions"][r]["net_firm_transfers"][0]
        out[r] = dict(model_unscaled=raw[i] + tr, nerc=DEMAND["regions"][r]["existing_certain_and_transfers"][0],
                      scale=float(FIRM_SCALE[i]))
    return out
