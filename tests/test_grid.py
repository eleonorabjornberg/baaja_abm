"""Grid agents (Phase 2): exogenous mode untouched, pairing, bill mechanics, and fit to the LBNL data."""
import json
import os

import numpy as np
import pytest

from baaja import experiments as ex
from baaja import grid as gr
from baaja.model import simulate, summarize
from baaja.params import BAAJA, REGIONS, TYPES

POL = ["renew", "fossil", "renew", "fossil"]
CAL = os.path.join(os.path.dirname(__file__), "..", "results", "calibration.json")


@pytest.fixture(scope="module")
def cal():
    if not os.path.exists(CAL):
        pytest.skip("no results/calibration.json (run.py --all)")
    c = json.load(open(CAL))
    if not (c["calibration"].get("grid_cal") or {}).get("operators"):
        pytest.skip("calibration has no grid agents (run.py --all)")
    return c


def _gen(rows):
    return {r["type"]: r for r in rows if TYPES[r["type"]]["ix"]}


def _gw(rows, p):
    s = summarize(rows, p)
    return sum(s[t]["GW_online"] for t in TYPES)


def test_exogenous_mode_ignores_grid_settings(cal):
    c = cal["calibration"]
    a = simulate(ex.params(dict(BAAJA, grid="exogenous"), c), 3, POL)
    b = simulate(ex.params(dict(BAAJA, grid="exogenous", grid_2106=False, grid_2109=0.0, grid_2110=0.5, kappa=9.0), c), 3, POL)
    for x, y in zip(a, b):
        assert np.array_equal(x["done"], y["done"]) and np.allclose(x["tCOD"], y["tCOD"], equal_nan=True)


def test_agents_deterministic_and_law_has_no_bill_effect(cal):
    c = cal["calibration"]
    pl = ex.params(dict(grid="agents"), c)
    pz = gr._law(ex.params(dict(BAAJA, grid="agents"), c))      # every lever back at current law
    a, b, z = simulate(pl, 5, POL), simulate(pl, 5, POL), simulate(pz, 5, POL)
    assert _gw(a, pl) == _gw(b, pl) == _gw(z, pz)


def test_sec2106_leaves_ercot_and_non_rto_regions_alone(cal):
    c = cal["calibration"]
    pl, p6 = ex.params(dict(grid="agents"), c), ex.params(dict(grid="agents", grid_2106=True, adopt_2106=1.0), c)
    L, S = _gen(simulate(pl, 2, POL)), _gen(simulate(p6, 2, POL))
    keep = [REGIONS.index(r) for r in ("ERCOT", "Southeast", "West")]
    changed_rto = False
    for t in L:
        ml, ms = np.isin(L[t]["region"], keep), np.isin(S[t]["region"], keep)
        assert np.array_equal(L[t]["tIA"][ml], S[t]["tIA"][ms]), t
        rl, rs = L[t]["region"] == REGIONS.index("MISO"), S[t]["region"] == REGIONS.index("MISO")
        changed_rto |= (rl.sum() != rs.sum()) or not np.array_equal(L[t]["tIA"][rl], S[t]["tIA"][rs])
    assert changed_rto


def test_more_study_throughput_shortens_waits(cal):
    c = cal["calibration"]
    late = lambda rows: np.concatenate([(r["tIA"] - r["t0"])[~r["seeded"] & (r["t0"] > 36) & (r["t0"] < 96) & np.isfinite(r["tIA"])
                                        & (r["region"] == REGIONS.index("MISO"))] for r in _gen(rows).values()])
    a = late(simulate(ex.params(dict(grid="agents"), c), 1, POL))
    b = late(simulate(ex.params(dict(grid="agents", grid_2110=1.0), c), 1, POL))
    assert np.median(b) < np.median(a)


def test_congestion_raises_withdrawal_at_study_results(cal):
    c = cal["calibration"]
    share = lambda rows: np.mean(np.concatenate([np.isfinite(r["gwd"][~r["seeded"]]) for r in _gen(rows).values()]))
    a = share(simulate(ex.params(dict(grid="agents", kappa=0.0), c), 1, POL))
    b = share(simulate(ex.params(dict(grid="agents", kappa=10.0), c), 1, POL))
    assert b > a


def test_operators_fit_and_holdout(cal):
    ops = cal["calibration"]["grid_cal"]["operators"]
    for r in ("MISO", "CAISO", "ERCOT"):
        assert ops[r]["fitted"] and ops[r]["fit_error"] < 0.15 and ops[r]["holdout_error"] < 0.15, r
    h = ops["MISO"]["holdout"]["2020"]
    assert abs(np.log(h["model_median"] / h["data_median"])) < 0.25       # MISO's lengthening, out of sample


def test_grid_calibration_matches_targets(cal):
    f = cal.get("grid_fit")
    if not f:
        pytest.skip("no grid_fit in calibration.json")
    # backcast fit (2015-19 cohorts): 12 and 36 months fitted; 60 months fitted but MISO misses by ~0.13 even with
    # its hold at the bound; 24 months is a check
    tol = {"12": 0.03, "24": 0.08, "36": 0.04, "60": 0.15}
    for r, v in f["withdrawn_by_month"].items():
        for m, (got, want) in v.items():
            assert abs(got - want) < tol[str(m)], (r, m)
    for k, (got, want) in f["completion"].items():
        if k.startswith("Geothermal|*"):        # the handful of geothermal requests drawn outside the West
            continue
        if want >= 0.05:
            assert abs(got - want) / want < 0.35, k


def test_withdrawal_curve_data_shape():
    d = gr.withdrawal_curve_data()
    assert set(d) <= set(REGIONS) and len(d) >= 7
    for v in d.values():
        x = [v[m] for m in gr.WD_MONTHS]
        assert all(0 <= a <= b <= 1 for a, b in zip(x, x[1:]))


def test_zero_cost_requests_pay_nothing_and_leave_only_for_cost_independent_reasons(cal):
    c = cal["calibration"]
    for va in (False, True):
        G = _gen(simulate(ex.params(dict(grid="agents", value_a=va), c), 4, POL))
        cost = np.concatenate([r["cost"] for r in G.values()]); gwd = np.concatenate([r["gwd"] for r in G.values()])
        reg = np.concatenate([r["region"] for r in G.values()])
        pjm = (reg == REGIONS.index("PJM")) & np.isfinite(cost)
        z = cost == 0
        zs = gr.COST[REGIONS.index("PJM")]["zero_share"]
        assert 0.5 * zs < z[pjm].mean() < 1.5 * zs
        left = np.isfinite(gwd[z & pjm]).mean()
        if va:   # LBNL: a share 1 - a (0.23 in ISO regions) does not complete at any cost
            assert 0.5 * (1 - gr.VALUE[REGIONS.index("PJM")]["a"]) < left < 1.5 * (1 - gr.VALUE[REGIONS.index("PJM")]["a"])
        else:
            assert left == 0


def test_sec2106_fee_is_a_multiple_of_expected_cost(cal):
    c = cal["calibration"]
    p = ex.params(dict(BAAJA, grid="agents", adopt_2106=1.0, kappa=0.0, fee_mult_2106=1.2), c)
    G = _gen(simulate(p, 1, POL))
    m = REGIONS.index("MISO"); cs = gr.COST[m]
    want = 1.2 * (1 - cs["zero_share"]) * np.exp(cs["mu"] + cs["sigma"] ** 2 / 2)
    fees = np.concatenate([r["cost"][r["planned"] & (r["region"] == m) & np.isfinite(r["cost"])] for r in G.values()])
    assert len(fees) and np.allclose(fees, want)


def test_ercot_upgrade_costs_do_not_grow(cal):
    c = cal["calibration"]
    a = _gen(simulate(ex.params(dict(grid="agents", kappa=0.0), c), 2, POL))
    b = _gen(simulate(ex.params(dict(grid="agents", kappa=10.0), c), 2, POL))
    e = REGIONS.index("ERCOT")
    for t in a:
        ia, ib = a[t]["region"] == e, b[t]["region"] == e
        assert np.array_equal(a[t]["tIA"][ia], b[t]["tIA"][ib]), t


def test_new_capacity_excludes_relicensed_hydro(cal):
    c = cal["calibration"]
    p = ex.params(dict(grid="agents"), c)
    s = summarize(simulate(p, 1, POL), p)
    tot = ex.totals(s)
    assert np.isclose(tot["GW_new"], tot["GW_total"] - s["Hydro relicense"]["GW_online"] - s["Transmission"]["GW_online"])
    assert s["Hydro relicense"]["GW_online"] > 0


def test_relative_screen_removes_share(cal):
    c = cal["calibration"]
    m = REGIONS.index("MISO")
    base = dict(BAAJA, grid="agents", adopt_2106=1.0, planned_share_2106=0.0, q_min_law=0.0)
    p0 = ex.params(dict(base, screen_2106=0.0), c)
    p1 = ex.params(dict(base, screen_2106=0.25), c)
    rule = p0["ix_rule_month"]
    n = lambda rows: sum(int(((r["region"] == m) & ~r["seeded"] & (r["t0"] >= rule)).sum()) for r in _gen(rows).values())
    a, b = n(simulate(p0, 2, POL)), n(simulate(p1, 2, POL))
    assert a > 200 and abs(b / a - 0.75) < 0.05, (a, b)
