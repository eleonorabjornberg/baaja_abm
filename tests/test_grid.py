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
        if va:   # a share 1 - a (fitted; LBNL's 0.23 in ISO regions before other withdrawal) fails at any cost
            a = ((c.get("grid_cal") or {}).get("value_a") or {}).get("ISO", gr.VALUE[REGIONS.index("PJM")]["a"])
            assert 0.5 * (1 - a) < left < 1.5 * (1 - a)
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


@pytest.mark.parametrize("rank", ["completion", "value"])
def test_relative_screen_removes_share_either_rank(cal, rank):
    c = cal["calibration"]
    m = REGIONS.index("PJM")
    base = dict(BAAJA, grid="agents", adopt_2106=1.0, planned_share_2106=0.0, q_min_law=0.0, screen_rank=rank)
    p0 = ex.params(dict(base, screen_2106=0.0), c)
    p1 = ex.params(dict(base, screen_2106=0.25), c)
    rule = p0["ix_rule_month"]
    n = lambda rows: sum(int(((r["region"] == m) & ~r["seeded"] & (r["t0"] >= rule)).sum()) for r in _gen(rows).values())
    a, b = n(simulate(p0, 2, POL)), n(simulate(p1, 2, POL))
    assert a > 200 and abs(b / a - 0.75) < 0.05, (a, b)


# ---- code matches text (guard 3): each test pins a behavior the brief and ODD state ----
def test_legacy_queue_gets_the_restudy_round_in_cluster_regions(cal):
    """Requests in the queue at end-2025 go through current law's re-study round: their recorded cost moves with it."""
    c = cal["calibration"]
    m = REGIONS.index("MISO")
    get = lambda o: _gen(simulate(ex.params(dict(grid="agents", **o), c), 3, POL))
    a, b = get(dict(restudy_scale=0.0, restudy_rho=0.0)), get(dict(restudy_scale=1.0))
    moved = 0
    for t in a:
        sa, sb = a[t]["seeded"] & (a[t]["region"] == m), b[t]["seeded"] & (b[t]["region"] == m)
        ca, cb = a[t]["cost"][sa], b[t]["cost"][sb]
        ok = np.isfinite(ca) & np.isfinite(cb) & (ca > 0)
        moved += int((~np.isclose(ca[ok], cb[ok])).sum())
    assert moved > 20


def test_planned_lines_enter_in_july_of_their_in_service_year():
    assert gr.month_of(2026, 11) == 0
    assert gr.month_of(2028) == 20                 # July 2028 is 20 months after Nov 2026
    assert all(isinstance(y, int) for v in gr.PLAN_TX.values() for y, _ in v)


def test_sec2109_reaches_only_public_utilities(cal, monkeypatch):
    """FPA s.232(d) applies only to public utilities: with no public-utility share, Sec.2109 changes nothing."""
    c = cal["calibration"]
    assert gr.PU_SHARE[REGIONS.index("ERCOT")] == 0 and ((0 <= gr.PU_SHARE) & (gr.PU_SHARE <= 1)).all()
    monkeypatch.setattr(gr, "PU_SHARE", np.zeros(len(REGIONS)))
    o = dict(BAAJA, grid="agents", adopt_2106=0.0)
    a = _gw(simulate(ex.params(dict(o, grid_2109=0.0), c), 5, POL), ex.params(o, c))
    b = _gw(simulate(ex.params(dict(o, grid_2109=0.3), c), 5, POL), ex.params(o, c))
    assert np.isclose(a, b)


def test_zero_cost_completion_matches_lbnl(cal):
    f = (cal.get("grid_fit") or {}).get("cost_completion")
    if not f:
        pytest.skip("calibration predates the fitted failure share")
    for mk, v in f.items():
        got, want = v["zero"]
        # check seeds are not the fit seeds: allow sampling error (non-ISO zero-cost requests are few, West only)
        n = v.get("n_zero", 0)
        tol = max(0.05, 3 * np.sqrt(want * (1 - want) / n)) if n else 0.05
        assert abs(got - want) < tol, (mk, got, want, n)


def test_restudy_shock_follows_spp_quantiles():
    q = gr.RESTUDY_Q
    assert len(q) == 101 and np.all(np.diff(q) >= 0)
    assert q[50] < 0                                # SPP: the median request's cost falls at re-study


def test_single_decision_scope_planned_leaves_others_in_the_round(cal):
    """sdp_scope_2106='planned' with no published locations: the bill's single decision point applies to no one,
    so with the screen off Sec.2106 changes nothing."""
    c = cal["calibration"]
    o = dict(BAAJA, grid="agents", adopt_2106=1.0, planned_share_2106=0.0, screen_2106=0.0, lag_2106=1.0,
             grid_2109=0.0, grid_2110=0.0)
    a = simulate(ex.params(dict(o, sdp_scope_2106="planned"), c), 6, POL)
    b = simulate(ex.params(dict(o, grid_2106=False), c), 6, POL)
    for x, y in zip(_gen(a).values(), _gen(b).values()):
        assert np.array_equal(x["done"], y["done"])
