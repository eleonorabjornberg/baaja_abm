import numpy as np
import pytest

from baaja import experiments as ex
from baaja.calibrate import calibrate, queue_completion
from baaja.model import apply_ix_rule, simulate, summarize
from baaja.params import BAAJA, BASE, GEN, TYPES

H = 0.0434
POL = ["renew", "fossil", "renew", "fossil"]


def params(over=None, **kw):
    p = dict(BASE); p.update(over or {}); p.update(kw); p.setdefault("hazard", H)
    if p["hazard"] is None:
        p["hazard"] = H
    return p


# --- Sec.2110 interconnection rule (handoff #7: speedup must count from each project's study start) ---
def test_ix_study_finished_before_rule_is_unchanged():
    assert apply_ix_rule([10.0], np.array([0.0]), 0.9, 24)[0] == pytest.approx(10.0)


def test_ix_study_starting_after_rule_is_fully_scaled():
    assert apply_ix_rule([40.0], np.array([30.0]), 0.9, 24)[0] == pytest.approx(36.0)


def test_ix_study_straddling_rule_scales_only_months_after():
    # starts at month 14, 40-month study: 10 months before the rule, 30 after -> 10 + 30*0.9
    assert apply_ix_rule([40.0], np.array([14.0]), 0.9, 24)[0] == pytest.approx(37.0)


def test_ix_no_speedup_is_identity():
    x = np.array([5.0, 50.0])
    assert np.allclose(apply_ix_rule(x, np.array([0.0, 100.0]), 1.0), x)


# --- calibration ---
def test_calibrated_baseline_completion_matches_lbnl_by_technology():
    h = calibrate()
    p = params(hazard=h)
    s = [summarize(simulate(p, seed, POL), p) for seed in range(3)]
    for t in GEN:
        c = np.mean([x[t]["completion_rate"] for x in s])
        tol = 0.02 if TYPES[t]["arr"] > 5 else 0.06       # geothermal and offshore wind: ~1-2 requests/month
        assert abs(c - TYPES[t]["completion_target"]) < tol, t


def test_build_calibration_matches_lbnl_time_to_cod():
    from baaja.calibrate import calibrate_all
    h, b = calibrate_all(rounds=2)
    p = params(hazard=h, build=b)
    s = [summarize(simulate(p, seed, POL), p) for seed in range(20, 23)]
    for t in b:
        m = np.mean([x[t]["median_months_to_COD"] for x in s])
        assert abs(m - TYPES[t]["cod_target"]) < 3, t


def test_data_calibrated_types_use_lbnl_values():
    from baaja.params import LBNL
    d = LBNL["types"]["Solar"]
    assert TYPES["Solar"]["arr"] == pytest.approx(d["arr_per_month"], abs=0.01)
    assert TYPES["Solar"]["mw"] == round(d["mw_built"])
    assert TYPES["Offshore wind"]["mw"] == 800          # too few built projects -> v3 assumption kept


# --- enforced deadlines ---
def test_baaja_caps_review_durations_and_baseline_truncates_nothing():
    p = params(BAAJA); rows = simulate(p, 1, POL)
    for r in rows:
        assert r["cut_months"][r["kind"] == 0].sum() == 0          # CEs never truncated
    b = params(); assert all(not r["trunc"].any() for r in simulate(b, 1, POL))
    s = summarize(rows, p)
    assert s["Offshore wind"]["truncated_share"] > 0.3            # EIS-only technology is hit hardest


def test_months_to_permit_respects_cap():
    # permit time for a nexus EA/EIS project without litigation <= intake + 24 + 4 + nonnepa
    p = params(BAAJA, suit_mult=0.0)
    for r in simulate(p, 2, POL):
        ty = TYPES[r["type"]]
        intake = p["intake_pub"] if ty["pub"] else p["intake_oth"]
        bound = intake + p["deadline"]["EIS"] + p["enf_lag"] + ty["nonnepa"] * p["nonnepa_mult"] + 1e-9
        dt = (r["tPermit"] - r["t0"])[r["nexus"] & (r["kind"] > 0)]   # CEs have no statutory deadline
        assert np.all(dt <= bound)


# --- Sec.1401 ---
def test_no_halts_when_halt_mult_zero_and_some_in_baseline():
    p0 = params(halt_mult=0.0)
    assert sum(summarize(simulate(p0, 3, ["renew"] * 4), p0)[t]["halted"] for t in TYPES) == 0
    p = params()
    assert summarize(simulate(p, 3, ["renew"] * 4), p)["Offshore wind"]["halted"] > 0


def test_halts_only_hit_the_side_the_administration_is_hostile_to():
    p = params()
    s = summarize(simulate(p, 3, ["fossil"] * 4), p)
    assert s["Offshore wind"]["halted"] == 0 and s["Solar"]["halted"] == 0


# --- reproducibility and common random numbers ---
def test_same_seed_same_result():
    p = params(BAAJA)
    a, b = summarize(simulate(p, 5, POL), p), summarize(simulate(p, 5, POL), p)
    assert a["Solar"] == b["Solar"]


def test_common_random_numbers_politics_does_not_shift_unaffected_types():
    # Geothermal and hydro are never halted, so their outcomes must not depend on the political path
    p = params()
    a = summarize(simulate(p, 4, ["renew"] * 4), p); b = summarize(simulate(p, 4, ["fossil"] * 4), p)
    for t in ("Geothermal", "Hydro relicense"):
        assert a[t] == b[t]


def test_common_random_numbers_vacatur_switch_keeps_stream_aligned():
    # Turning vacatur off must not change the interconnection draws of later technologies
    p1, p2 = params(), params(vacatur=False)
    r1, r2 = simulate(p1, 6, POL), simulate(p2, 6, POL)
    assert np.array_equal(r1[-1]["t0"], r2[-1]["t0"])


# --- harm index and reporting ---
def test_harm_zero_in_baseline_positive_under_baaja():
    p, q = params(), params(BAAJA)
    assert sum(summarize(simulate(p, 0, POL), p)[t]["harm"] for t in TYPES) == 0
    assert sum(summarize(simulate(q, 0, POL), q)[t]["harm"] for t in TYPES) > 0


def test_totals_group_sums_match_types():
    runs = ex.run_scenario(BAAJA, 2, H)
    t = ex.totals(runs[0])
    assert t["GW_total"] == pytest.approx(sum(runs[0][k]["GW_online"] for k in TYPES))
    assert t["GW Renewable (new)"] + t["GW Fossil (gas)"] + t["GW Storage"] + t["GW Renewable (retained hydro)"] \
        == pytest.approx(t["GW_total"])
    assert 0 < t["renewable share of new TWh"] < 1


def test_paired_difference_has_interval():
    base = ex.run_scenario({}, 4, H); z = ex.run_scenario(BAAJA, 4, H)
    d = ex.aggregate(z, base)["diff_vs_baseline"]["GW_total"]
    assert d["p5"] <= d["mean"] <= d["p95"] and d["mean"] > 0


# --- challengers ---
from baaja.params import CHALLENGER_FILTER, CHALLENGER_MIX, CHALLENGERS


def test_challenger_mixes_are_distributions():
    for t in TYPES:
        assert len(CHALLENGER_MIX[t]) == len(CHALLENGERS) and sum(CHALLENGER_MIX[t]) == pytest.approx(1.0)


def test_challenger_filter_mean_close_to_v3_factor():
    # technology-weighted mean of the Sec.1110 filter should stay near v3's single 0.55
    f = np.array(CHALLENGER_FILTER["BAAJA"])
    means = [np.dot(CHALLENGER_MIX[t], f) for t in TYPES]
    assert all(0.5 < m < 0.65 for m in means)


def test_suits_by_challenger_sum_to_total_suits():
    p = params(BAAJA); s = summarize(simulate(p, 0, POL), p)
    for t in TYPES:
        assert sum(s[t][f"suits: {c}"] for c in CHALLENGERS) == s[t]["suits"]
        assert all(s[t][f"wins: {c}"] <= s[t][f"suits: {c}"] for c in CHALLENGERS)


def test_baaja_filters_local_groups_harder_than_governments():
    base = ex.run_scenario({}, 20, H); z = ex.run_scenario(BAAJA, 20, H)
    tot = lambda runs, c: sum(r[t][f"suits: {c}"] for r in runs for t in TYPES)
    keep = {c: tot(z, c) / tot(base, c) for c in CHALLENGERS}
    assert keep["Local group / residents"] < keep["State / local government"]
