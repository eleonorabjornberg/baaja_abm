"""Numbers in the brief come from the results files, not from typing (guard against stale numbers).

docs/brief_src.md is the brief with each model number written as a placeholder that names where it comes from:

    {{sim7:results/BAAJA/diff_vs_baseline/GW_new/mean ; +.1f}}
    {{dec:A|+ relative screen (central)/diff_GW_new/mean - dec:A|without Sec.2106/diff_GW_new/mean ; +.1f}}

A placeholder is one or more paths joined by " - " or " + ", then " ; " and a Python format spec. A path is
`file:key/key/...`; list items are addressed by index. Files:

    sim7 results/sim7_grid_agents.json      dec  results/sec2106_decomposition.json
    unc  results/uncertainty.json           cal  results/calibration.json
    back results/backcast.json

`python -m baaja.brief_numbers` writes docs/brief.md from the template and results/brief_numbers.json (every
placeholder and its value). tests/test_brief_numbers.py fails if docs/brief.md is not the rendering of the template
on the current results, if a placeholder does not resolve, or if the template types a signed GW number by hand.
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
FILES = dict(sim7="results/sim7_grid_agents.json", dec="results/sec2106_decomposition.json",
             unc="results/uncertainty.json", cal="results/calibration.json", back="results/backcast.json")
SRC = os.path.join(ROOT, "docs", "brief_src.md")
OUT = os.path.join(ROOT, "docs", "brief.md")
NUMS = os.path.join(ROOT, "results", "brief_numbers.json")
PH = re.compile(r"\{\{(.+?)\}\}")
TERM = re.compile(r"\s+([-+])\s+(?=(?:%s):)" % "|".join(FILES))
# a signed GW (or percentage-point) number typed in the template outside a placeholder
TYPED = re.compile(r"(?<![\w.])[+−-]\d+(?:\.\d+)?\s?GW\b")

_cache = {}


def _load(alias):
    if alias not in _cache:
        _cache[alias] = json.load(open(os.path.join(ROOT, FILES[alias])))
    return _cache[alias]


def lookup(path):
    alias, rest = path.split(":", 1)
    x = _load(alias.strip())
    for k in rest.strip().split("/"):
        x = x[int(k)] if isinstance(x, list) else x[k]
    return float(x)


def value(expr):
    """Evaluate `path (+|-) path ...`."""
    parts = TERM.split(" " + expr.strip())
    v = lookup(parts[0])
    for op, p in zip(parts[1::2], parts[2::2]):
        v = v + lookup(p) if op == "+" else v - lookup(p)
    return v


def placeholder(body):
    expr, fmt = body.rsplit(";", 1)
    v = value(expr)
    fmt = fmt.strip()
    if fmt.startswith("abs"):
        v, fmt = abs(v), fmt[3:]
    s = format(v, fmt)
    return s, v


def render(src=None):
    """Return (rendered text, {placeholder: value})."""
    _cache.clear()
    text = open(src or SRC).read()
    nums = {}

    def sub(m):
        s, v = placeholder(m.group(1))
        nums[m.group(1).strip()] = dict(value=v, text=s)
        return s
    return PH.sub(sub, text), nums


def typed_numbers(src=None):
    """Signed GW numbers typed in the template outside placeholders (should be none)."""
    text = PH.sub("", open(src or SRC).read())
    return TYPED.findall(text)


def main():
    out, nums = render()
    open(OUT, "w").write(out)
    json.dump(nums, open(NUMS, "w"), indent=1)
    print(f"docs/brief.md: {len(nums)} numbers from results")
    left = typed_numbers()
    if left:
        print("typed by hand (use placeholders):", left)


if __name__ == "__main__":
    main()
