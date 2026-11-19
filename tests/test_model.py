import json
import os

import numpy as np
import pytest

from baaja import experiments as ex
from baaja.calibrate import calibrate, check
from baaja.model import ix_cut, simulate, summarize
from baaja.params import BAAJA, BASE, CHALLENGER_MIX, CHALLENGERS, ENGINE, GEN, NEXUS, TYPES

POL = ["renew", "fossil", "renew", "fossil"]


@pytest.fixture(scope="module")
def cal():
    return calibrate(rounds=2)


def P(cal, over=None, **kw):
    p = ex.params(over, cal); p.update(kw); return p


# --- interconnection rule timing -----------------------------------------------------------------------------
def test_ix_cut_only_after_rule_month():
    assert ix_cut([10.0], np.array([0.0]), .1, 24)[0] == pytest.approx(10.0)
    assert ix_cut([40.0], np.array([30.0]), .1, 24)[0] == pytest.approx(36.0)
    assert ix_cut([40.0], np.array([14.0]), .1, 24)[0] == pytest.approx(37.0)


# --- calibration fits the data -------------------------------------------------------------------------------
def test_calibration_matches_targets(cal):
    c = check(cal)
    for t in GEN:
        got, want = c[t]["completion"]
        assert abs(got - want) < (0.02 if TYPES[t]["arr"] > 5 else 0.05), t
        if TYPES[t]["cod_target"]:
            got, want = c[t]["months_to_COD"]
            assert abs(got - want) < 3, t
    for t in ("Solar", "Transmission", "Hydro relicense"):
        got, want = c[t]["EIS_per_year"]
        assert abs(got - want) < 0.6 * want + 0.3, t


def test_nexus_shares_come_from_data():
    for t in ("Gas", "Solar", "Onshore wind", "Storage", "Geothermal"):
        lo, hi = NEXUS["types"][t]["combined_net"]
        assert TYPES[t]["nex"] == pytest.approx((lo + hi) / 2)
    assert TYPES["Offshore wind"]["nex"] == 1.0


# --- structural rules ----------------------------------------------------------------------------------------
def test_no_review_or_suit_after_withdrawal(cal):
    p = P(cal)
    for r in simulate(p, 3, POL):
        assert not (r["sued"] & ~r["decided"]).any()
        assert not (r["decided"] & ~r["nexus"]).any()


def test_seeded_queue_matches_lbnl_active_counts(cal):
    p = P(cal)
    rows = {r["type"]: r for r in simulate(p, 4, POL)}
    for t in ("Solar", "Gas", "Onshore wind"):
        assert rows[t]["seeded"].sum() == pytest.approx(ENGINE["lbnl"]["active_end2025"][t]["n"], rel=0.1)
        assert (rows[t]["t0"][rows[t]["seeded"]] < 0).all()


def test_deadlines_apply_only_to_reviews_starting_after_enactment(cal):
    p = P(cal, BAAJA, deadline_bind=1.0)
    rows = simulate(p, 5, POL)
    assert sum(r["trunc"].sum() for r in rows) > 0
    for r in rows:
        intake = p["intake_pub_2213"] if TYPES[r["type"]]["pub"] else p["intake_oth"]
        assert not (r["trunc"] & (r["t0"] + intake < 0)).any(), r["type"]


def test_no_vacatur_or_halts_when_turned_off(cal):
    p = P(cal, BAAJA, halt_mult=0.0)
    rows = simulate(p, 6, ["renew"] * 4)
    assert sum(r["vacated"].sum() for r in rows) == 0
    assert sum(r["halted"].sum() for r in rows) == 0


def test_common_random_numbers_politics_does_not_move_gas_on_renewable_hostility(cal):
    p = P(cal, halt_mult=0.0)
    a = summarize(simulate(p, 7, ["renew"] * 4), p); b = summarize(simulate(p, 7, ["fossil"] * 4), p)
    assert a["Gas"]["GW_online"] == b["Gas"]["GW_online"]


def test_challenger_mix_and_suit_accounting(cal):
    for t in TYPES:
        assert sum(CHALLENGER_MIX[t]) == pytest.approx(1.0)
    p = P(cal); s = summarize(simulate(p, 8, POL), p)
    for t in TYPES:
        assert sum(s[t][f"suits: {c}"] for c in CHALLENGERS) == s[t]["suits"]


def test_baaja_reduces_suits_and_paired_interval(cal):
    base = ex.run_scenario({}, 4, cal); z = ex.run_scenario(BAAJA, 4, cal)
    d = ex.aggregate(z, base)["diff_vs_baseline"]
    assert d["suits_total"]["mean"] < 0
    assert d["GW_total"]["p5"] <= d["GW_total"]["mean"] <= d["GW_total"]["p95"]


def test_backcast_within_tolerance_of_eia(cal):
    b = ex.backcast(cal, 3)
    e = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "eia860_additions.json")))
    for t in ("Solar", "Onshore wind", "Gas"):
        m = sum(b[t][y] for y in range(2018, 2026)); x = sum(e[t][str(y)] for y in range(2018, 2026)) / 1000
        assert 0.6 < m / x < 1.4, t


def test_harm_zero_under_current_law(cal):
    p = P(cal); s = summarize(simulate(p, 9, POL), p)
    assert sum(s[t]["harm"] for t in TYPES) == 0


# --- the five simulations run end to end -------------------------------------------------------------------
@pytest.mark.parametrize("mod", ["sim1_permitting", "sim2_litigation", "sim3_grid", "sim4_certainty", "sim5_decision_control"])
def test_simulation_runs(mod, cal, tmp_path):
    import importlib
    m = importlib.import_module(f"baaja.sims.{mod}")
    md, data = m.run(2, cal, str(tmp_path), str(tmp_path))
    assert md.startswith("# Simulation") and (tmp_path / f"{mod}.md").exists()


def test_late_adapt_comes_from_limitation_experiment():
    from baaja.params import ASSUMPTIONS, LIMIT
    lo, c, hi, _ = ASSUMPTIONS["late_adapt"]
    assert lo == pytest.approx(LIMIT["low"], abs=0.01) and c == pytest.approx(LIMIT["central"], abs=0.01) and lo < c < hi


def test_blm_review_parameters_come_from_eplanning():
    from baaja.params import ASSUMPTIONS, BLM
    assert ASSUMPTIONS["ea_share_nonEIS"][1] == pytest.approx(BLM["ea_share_nonEIS"]["project"], abs=0.01)
    assert TYPES["Solar"]["ea_med"] == pytest.approx(BLM["median_months"]["Solar"]["EA"]["median"])
    assert TYPES["Solar"]["lit_ea_data"] == pytest.approx(BLM["lit_rate"]["Renewable"]["lit_ea"])
    assert "lit_ea_data" not in TYPES["Gas"]          # gas keeps the generic all-sector rate
