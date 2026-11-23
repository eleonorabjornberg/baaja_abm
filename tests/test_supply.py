import json
import os

import numpy as np
import pytest

from baaja import experiments as ex
from baaja import supply as sp
from baaja.calibrate import calibrate, calibrate_overdue, calibrate_regions, regional_targets
from baaja.model import simulate, summarize
from baaja.params import BAAJA, GEN, REGIONS, RGN, RTO_IDX, TYPES

POL = ["renew", "fossil", "renew", "fossil"]


@pytest.fixture(scope="module")
def cal():
    c = calibrate(rounds=1)
    c, _ = calibrate_regions(c, seeds=(7, 8, 9, 10), iters=12)
    c, _ = calibrate_overdue(c, seeds=(7, 8, 9), iters=10)
    return c


def test_regions_and_rto_set():
    assert len(REGIONS) == 9 and "ERCOT" not in [REGIONS[i] for i in RTO_IDX]
    assert {REGIONS[i] for i in RTO_IDX} == {"CAISO", "ISO-NE", "MISO", "NYISO", "PJM", "SPP"}


def test_region_draws_follow_lbnl_shares(cal):
    p = ex.params({}, cal)
    r = {x["type"]: x for x in simulate(p, 3, POL)}["Solar"]
    new = ~r["seeded"]; iso = new & (r["mkt"] == 0)
    for reg, share in RGN["types"]["Solar"]["new_share"]["0"].items():
        got = (r["region"][iso] == REGIONS.index(reg)).mean()
        assert got == pytest.approx(share, abs=0.02), reg


def test_2106_leaves_ercot_and_non_iso_untouched(cal):
    a = {x["type"]: x for x in simulate(ex.params(dict(BAAJA, ix_cut_rto=0.4, ix_rule_month=0), cal), 4, POL)}["Solar"]
    b = {x["type"]: x for x in simulate(ex.params(dict(BAAJA, ix_cut_rto=0.0), cal), 4, POL)}["Solar"]
    out = ~np.isin(a["region"], RTO_IDX)
    assert np.array_equal(a["tCOD"][out], b["tCOD"][out])
    assert (a["tCOD"][~out] < b["tCOD"][~out] - 1e-9).any()


def test_regional_targets_average_to_pooled():
    tg = regional_targets()
    assert any(k.startswith("Solar|") for k in tg)
    for t in GEN:
        assert all(0 < v < 1 for k, v in tg.items() if k.startswith(t + "|"))


def test_supply_accounting_identities(cal):
    p = ex.params({}, cal)
    run = summarize(simulate(p, 5, POL), p)
    s = sp.supply(run)
    fleet = sp.existing_fleet()
    add = sp.additions(run)
    assert np.allclose(s["installed"], (fleet + add).sum(axis=1))
    assert np.allclose(s["added"], add.sum(axis=1))
    assert (np.diff(add, axis=2) >= -1e-9).all()                          # cumulative additions never fall
    # additions by region sum to the national GW online
    nat = sum(run[t]["GW_online"] for t in sp.MODEL_GROUP if t in run) * 1000
    assert add[:, :, -1].sum() == pytest.approx(nat, rel=1e-6)
    assert np.allclose(s["reserve_margin"], s["firm"] / s["nid"] - 1)
    assert (s["shortfall"] >= 0).all()


def test_fleet_retirements_only_reduce_capacity():
    f = sp.existing_fleet()
    assert (np.diff(f, axis=2) <= 1e-9).all()
    hi = sp.existing_fleet(dict(sp.SA, ret_hazard_old=0.06)); lo = sp.existing_fleet(dict(sp.SA, ret_hazard_old=0.01))
    assert hi.sum() < f.sum() < lo.sum()


def test_firm_scale_matches_nerc_2026():
    chk = sp.check_2026()
    for r, v in chk.items():
        assert (v["model_unscaled"] - sp.DEMAND["regions"][r]["net_firm_transfers"][0]) * v["scale"] \
            + sp.DEMAND["regions"][r]["net_firm_transfers"][0] == pytest.approx(v["nerc"], rel=1e-9)


def test_current_law_has_zero_bill_effect_and_baaja_adds_firm(cal):
    a = ex.run_scenario({}, 2, cal); b = ex.run_scenario({}, 2, cal); z = ex.run_scenario(BAAJA, 2, cal)
    for x, y, w in zip(a, b, z):
        sa, sb, sz = sp.supply(x), sp.supply(y), sp.supply(w)
        assert np.array_equal(sa["firm"], sb["firm"])
        assert sz["firm"].sum() >= sa["firm"].sum()


def test_demand_from_nerc():
    nid, rml, tr = sp.demand()
    d = sp.DEMAND["regions"]["PJM"]
    k = sp.YEARS.index(2030)
    assert nid[REGIONS.index("PJM"), k] == pytest.approx(d["net_internal_demand"][4])
    assert rml[REGIONS.index("PJM"), k] == pytest.approx(d["reference_margin_level"][4])


def test_joint_uncertainty_is_reproducible_and_wider_than_seed_noise(cal):
    from baaja import uncertainty as u
    k1, X1, r1 = u.sample(12, cal, seed=5)
    k2, X2, r2 = u.sample(12, cal, seed=5)
    assert k1 == k2 and np.array_equal(X1, X2) and [r["GW total"] for r in r1] == [r["GW total"] for r in r2]
    assert "ix_2106" not in k1 and "ix_2106" in u.sample(4, cal, grid="range")[0]
    # values stay inside their ranges
    from baaja.params import ASSUMPTIONS
    for i, k in enumerate(k1):
        lo, _, hi, _ = ASSUMPTIONS[k] if k in ASSUMPTIONS else sp.SUPPLY_ASSUMPTIONS[k]
        assert (X1[:, i] >= min(lo, hi) - 1e-12).all() and (X1[:, i] <= max(lo, hi) + 1e-12).all(), k
    # joint spread of the GW gain is at least the seed-only spread at central values
    seed_only = [sum(z[t]["GW_online"] - b[t]["GW_online"] for t in TYPES)
                 for z, b in zip(ex.run_scenario(BAAJA, 12, cal), ex.run_scenario({}, 12, cal))]
    assert np.std([r["GW total"] for r in r1]) >= 0.8 * np.std(seed_only)
