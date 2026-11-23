"""Phase 3: two-piece background hazard, region by request year, court baseline, backcast, joint uncertainty."""
import json
import os

import numpy as np
import pytest

from baaja import experiments as ex
from baaja import grid as gr
from baaja import uncertainty as un
from baaja import validation as va
from baaja.model import draw_region_by_year, simulate, summarize
from baaja.params import BAAJA, LEVERS, REGION_BY_YEAR, REGIONS, TYPES

POL = ["renew", "fossil", "renew", "fossil"]
CAL = os.path.join(os.path.dirname(__file__), "..", "results", "calibration.json")


@pytest.fixture(scope="module")
def cal():
    if not os.path.exists(CAL):
        pytest.skip("no results/calibration.json (run.py --all)")
    return json.load(open(CAL))["calibration"]


def _gw(p, seed):
    s = summarize(simulate(p, seed, POL), p)
    return sum(s[t]["GW_online"] for t in TYPES)


# ---- background withdrawal clock --------------------------------------------------------------------------------
def test_pre_clock_two_piece():
    Ew = np.random.default_rng(0).exponential(size=200_000)
    one = gr.pre_clock(Ew, 0.02)
    assert np.array_equal(one, gr.pre_clock(Ew, [0.02, 0.02]))          # equal pieces = one hazard
    two = gr.pre_clock(Ew, [0.04, 0.005])
    assert abs((two <= 12).mean() - (1 - 0.96 ** 12)) < 0.005             # first-year piece
    late = two[two > 12] - 12                                             # memoryless after the split
    assert abs(np.mean(late <= 12) - (1 - 0.995 ** 12)) < 0.01
    assert np.all(np.diff(gr.pre_clock(np.sort(Ew), [0.04, 0.005])) >= 0)  # monotone in the draw (paired runs)


# ---- regions by request year ------------------------------------------------------------------------------------
def test_region_by_year_follows_that_years_shares():
    t = "Solar"
    years = sorted(REGION_BY_YEAR[t])
    y = years[len(years) // 2]
    u = np.random.default_rng(1).random(50_000)
    reg = draw_region_by_year(t, np.full(u.size, y), u)
    idx, cum = REGION_BY_YEAR[t][y]
    want = np.diff([0.0] + cum)
    got = np.array([(reg == i).mean() for i in idx])
    assert np.allclose(got, want, atol=0.01)
    far = draw_region_by_year(t, np.full(u.size, years[-1] + 5), u)      # beyond the data: nearest year
    assert np.array_equal(far, draw_region_by_year(t, np.full(u.size, years[-1]), u))


# ---- court baseline after Seven County ----------------------------------------------------------------------------
def test_court_baseline_central_is_unchanged_and_scales_both_runs(cal):
    p0 = ex.params({}, cal)
    p1 = ex.params(dict(nepa_win_mult=1.0, nepa_suit_mult=1.0), cal)
    a, b = simulate(p0, 4, POL), simulate(p1, 4, POL)
    for x, y in zip(a, b):
        assert np.array_equal(x["sued"], y["sued"]) and np.array_equal(x["lost"], y["lost"])
    low = ex.params(dict(nepa_win_mult=0.5, nepa_suit_mult=0.6), cal)
    sl = sum(r["sued"].sum() for r in simulate(low, 4, POL))
    assert sl < sum(r["sued"].sum() for r in a)
    lw = sum(r["lost"].sum() for r in simulate(low, 4, POL))
    assert lw <= sum(r["lost"].sum() for r in a)
    # BAAJA's court provisions are worth less against a more deferential baseline (paired, same seeds)
    gain = lambda o: np.mean([_gw(ex.params({**o, **LEVERS["litigation"]}, cal), s) - _gw(ex.params(o, cal), s)
                              for s in range(6)])
    assert gain(dict(nepa_win_mult=0.5, nepa_suit_mult=0.6)) <= gain({}) + 1e-9


# ---- backcast ----------------------------------------------------------------------------------------------------
def test_backcast_report_shapes(cal, tmp_path):
    md, B = va.report(cal, str(tmp_path), n_runs=1)
    assert os.path.exists(tmp_path / "backcast.md") and os.path.exists(tmp_path / "backcast.json")
    for m in va.MODES:
        for t in va.TECH:
            nat = sum(B[m]["national"][t][y] for y in va.YEARS)
            reg = sum(B[m]["region"][t].values())
            assert abs(nat - reg) < 1e-6 * max(nat, 1) + 1e-6, (m, t)   # regions sum to the nation
    e = va.eia()
    for t in va.TECH:                                                     # EIA regions sum to EIA national (within 2%)
        assert abs(sum(e["region"][t].values()) / sum(e["national"][t].values()) - 1) < 0.02, t


def test_backcast_exogenous_mode_unchanged_by_grid_settings(cal):
    p = va.backcast_params(cal, "exogenous")
    a = simulate(p, 2, ["renew", "fossil", "renew"])
    b = simulate(dict(p, grid_cal=None, kappa=7.0), 2, ["renew", "fossil", "renew"])
    for x, y in zip(a, b):
        assert np.array_equal(x["done"], y["done"])


# ---- joint uncertainty -------------------------------------------------------------------------------------------
def test_joint_sample_reproducible(cal):
    k1, X1, r1 = un.sample(4, cal, seed=11, supply_on=False)
    k2, X2, r2 = un.sample(4, cal, seed=11, supply_on=False)
    assert k1 == k2 and np.array_equal(X1, X2) and r1 == r2
    _, X3, _ = un.sample(4, cal, seed=12, supply_on=False)
    assert not np.array_equal(X1, X3)


def test_joint_interval_no_narrower_than_seed_only(cal):
    n = 16
    keys, X, res = un.sample(n, cal, seed=5, supply_on=False)
    joint = np.array([r["GW total"] for r in res])
    seed_only = []
    for j in range(n):
        s = 10_000 + j; pol = ex.politics_draw(s, 4)
        pl, pb = ex.params({}, cal), ex.params(BAAJA, cal)
        seed_only.append(sum(summarize(simulate(pb, s, pol), pb)[t]["GW_online"] for t in TYPES)
                         - sum(summarize(simulate(pl, s, pol), pl)[t]["GW_online"] for t in TYPES))
    assert np.ptp(joint) >= np.ptp(seed_only)
    assert "nepa_win_mult" in keys and "nepa_suit_mult" in keys
