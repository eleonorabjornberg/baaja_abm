"""The brief's model numbers are generated from the results (baaja/brief_numbers.py)."""
import os

import pytest

from baaja import brief_numbers as bn


@pytest.fixture(scope="module")
def rendered():
    if not os.path.exists(bn.SRC):
        pytest.skip("no docs/brief_src.md")
    missing = [f for f in bn.FILES.values() if not os.path.exists(os.path.join(bn.ROOT, f))]
    if missing:
        pytest.skip(f"results missing: {missing}")
    return bn.render()


def test_every_placeholder_resolves(rendered):
    out, nums = rendered
    assert nums and "{{" not in out


def test_brief_is_the_rendering_of_the_template_on_current_results(rendered):
    out, _ = rendered
    assert open(bn.OUT).read() == out, "docs/brief.md is stale: run python -m baaja.brief_numbers"


def test_no_signed_gw_number_typed_by_hand(rendered):
    assert bn.typed_numbers() == []


def test_expression_arithmetic(tmp_path):
    p = tmp_path / "t.md"
    p.write_text("x {{sim7:results/BAAJA/totals/GW_new/mean - sim7:results/Current law/totals/GW_new/mean ; +.1f}} y")
    if not os.path.exists(os.path.join(bn.ROOT, bn.FILES["sim7"])):
        pytest.skip("no sim7 results")
    out, nums = bn.render(str(p))
    v = list(nums.values())[0]["value"]
    assert out == f"x {v:+.1f} y"


def test_range_sum():
    if not os.path.exists(os.path.join(bn.ROOT, bn.FILES["back"])):
        pytest.skip("no backcast results")
    bn._cache.clear()
    d = bn._load("back")["eia"]["national"]["Solar"]
    want = sum(v for k, v in d.items() if 2018 <= int(k) <= 2025)
    assert abs(bn.lookup("back:eia/national/Solar/2018..2025") - want) < 1e-9


def test_variance_ranks_match_the_names_the_brief_gives_them():
    """The brief names the assumptions behind variance shares it quotes by rank: a reorder must fail here, not
    mislabel the text."""
    import json
    p = os.path.join(bn.ROOT, bn.FILES["unc"])
    if not os.path.exists(p):
        pytest.skip("no uncertainty results")
    u = json.load(open(p))
    top = lambda k: [n for n, *_ in u[k]["variance"]["GW new"]["top"]]
    g = top("grid agents (Phase 2), their assumptions drawn")
    assert g[0] == "g_2110" and g[1].startswith("adoption realised") and g[2] == "restudy_scale", g[:3]
    assert top("grid dials at 0 (data-sized provisions)")[0] == "comply_2213"
    assert top("grid dials across their ranges")[0] == "ix_2106"
