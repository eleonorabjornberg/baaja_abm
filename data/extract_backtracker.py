"""Sabin Center Climate Backtracker (2025-): federal actions aimed at wind, solar and other energy projects.

Usage: python data/extract_backtracker.py BACKTRACKER_HTML  -> data/backtracker_summary.json
The page embeds its entries as JSON (title, summary, date). The tracker records rules and orders, not actions against
individual projects (no entries for Lava Ridge, Esmeralda 7, Empire Wind or Revolution Wind), so it cannot give
per-project halt rates. It does show the mechanism used against onshore wind and solar in 2025: added reviews and
removed priority for *pending* permits, which falls under Sec.1402 (disparate treatment), not Sec.1401.
"""
import json, os, re, sys

TECH = {"wind": r"\bwind\b", "solar": r"\bsolar\b", "offshore wind": r"offshore wind|outer continental shelf",
        "oil and gas": r"oil|natural gas|lng|pipeline|methane", "coal": r"\bcoal\b"}
PERMIT = r"permit|lease|review|approv|right-of-way|stop[- ]work|halt|pause|rescind|revok"


def run(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    items = {}
    for m in re.finditer(r'\{"title":"((?:[^"\\]|\\.)*)","summary":"((?:[^"\\]|\\.)*)".*?"date":"(\d{4}-\d{2}-\d{2})"', t):
        ti = json.loads('"' + m.group(1) + '"')
        items[ti] = dict(title=ti, summary=re.sub("<[^>]+>", "", json.loads('"' + m.group(2) + '"')), date=m.group(3))
    items = sorted(items.values(), key=lambda x: x["date"])
    out = dict(n_entries=len(items), dates=[items[0]["date"], items[-1]["date"]], by_tech={})
    for k, pat in TECH.items():
        sel = [i for i in items if re.search(pat, i["title"] + " " + i["summary"], re.I) and re.search(PERMIT, i["title"], re.I)]
        out["by_tech"][k] = [dict(date=i["date"], title=i["title"]) for i in sel]
    return out


if __name__ == "__main__":
    out = run(sys.argv[1])
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "backtracker_summary.json"), "w"), indent=1)
    for k, v in out["by_tech"].items():
        print(k, len(v)); [print("   ", e["date"], e["title"][:100]) for e in v]
