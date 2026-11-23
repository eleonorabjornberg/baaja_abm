"""Peak demand, firm transfers and reference margins by region, from NERC's 2025 Long-Term Reliability Assessment.

Usage: python data/extract_demand.py NERC_LTRA_2025.pdf   -> data/demand_targets.json   (needs pdftotext)

Each US assessment area has a table "Demand, Resources, and Reserve Margins" for 2026-2035 (the peak season the
area plans for: summer for most, winter for WECC-Northwest). NERC assessment areas are mapped to LBNL's nine
regions; where several areas map to one region their MW are summed and the reference margin level is the
demand-weighted mean. The mapping is approximate at the edges (WECC-California includes non-CAISO utilities;
SERC-Central includes TVA, LG&E/KU and AECI).

Per region and year:
  total_internal_demand, demand_response, net_internal_demand   MW (peak, coincident within the area)
  net_firm_transfers                                            MW (imports counted as firm capacity)
  existing_certain_and_transfers, tier1_additions               MW (NERC's own resource view, for comparison)
  anticipated_reserve_margin, reference_margin_level            fractions
  growth_2030_35                                                annual growth of net internal demand, 2030-35
"""
import json, os, re, subprocess, sys

AREA_TO_REGION = {
    "MISO": "MISO", "MRO-SPP": "SPP", "NPCC-New England": "ISO-NE", "NPCC-New York": "NYISO", "PJM": "PJM",
    "Texas RE-ERCOT": "ERCOT", "WECC-California": "CAISO",
    "SERC-Central": "Southeast", "SERC-East": "Southeast", "SERC-Florida Peninsula": "Southeast",
    "SERC-Southeast": "Southeast",
    "WECC-Basin": "West", "WECC-Northwest": "West", "WECC-Rocky Mountain": "West", "WECC-Southwest": "West",
}
ROWS = {"Total Internal Demand": "total_internal_demand", "Demand Response": "demand_response",
        "Net Internal Demand": "net_internal_demand", "Additions: Tier 1": "tier1_additions",
        "Net Firm Capacity Transfers": "net_firm_transfers",
        "Existing-Certain and Net Firm Transfers": "existing_certain_and_transfers",
        "Net Capacity Transfers (WECC Model)": "net_firm_transfers",            # WECC tables
        "Existing-Certain and Net Transfers": "existing_certain_and_transfers",
        "Anticipated Reserve Margin (%)": "anticipated_reserve_margin",
        "Reference Margin Level (%)": "reference_margin_level"}
AREA_RE = re.compile(r"^(MISO|MRO-[A-Za-z ]+|NPCC-[A-Za-z ]+|PJM|SERC-[A-Za-z ]+|Texas RE-ERCOT|WECC-[A-Za-z/ ]+)$")
YEARS = list(range(2026, 2036))


def num(tok):
    tok = tok.replace(",", "").replace("–", "-").replace("−", "-")
    if tok.endswith("%"):
        return float(tok[:-1]) / 100
    return float(tok)


def parse(lines):
    areas = {}
    for i, l in enumerate(lines):
        if "Demand, Resources, and Reserve Margins" not in l:
            continue
        name = next((lines[k].strip() for k in range(i - 1, max(0, i - 60), -1) if AREA_RE.match(lines[k].strip())), None)
        if name not in AREA_TO_REGION or name in areas:
            continue
        rows = {}
        for k in range(i + 1, i + 25):
            s = lines[k].strip()
            for label, key in ROWS.items():
                if s.startswith(label) and key not in rows:
                    vals = re.findall(r"-?–?[\d,]+\.?\d*%?", s[len(label):])
                    vals = [num(v) for v in vals if re.search(r"\d", v)]
                    if len(vals) >= 10:
                        rows[key] = vals[:10]
        areas[name] = rows
    return areas


def aggregate(areas):
    out = {}
    for reg in sorted(set(AREA_TO_REGION.values())):
        members = [a for a, r in AREA_TO_REGION.items() if r == reg and a in areas]
        d = {"areas": members}
        for key in ("total_internal_demand", "demand_response", "net_internal_demand", "tier1_additions",
                    "net_firm_transfers", "existing_certain_and_transfers"):
            d[key] = [sum(areas[a].get(key, [0] * 10)[j] for a in members) for j in range(10)]
        w = [[areas[a]["net_internal_demand"][j] for a in members] for j in range(10)]
        for key in ("reference_margin_level", "anticipated_reserve_margin"):
            d[key] = [sum(areas[a][key][j] * w[j][m] for m, a in enumerate(members)) / sum(w[j]) for j in range(10)]
        nid = d["net_internal_demand"]
        d["growth_2030_35"] = (nid[9] / nid[4]) ** (1 / 5) - 1
        d["growth_2026_35"] = (nid[9] / nid[0]) ** (1 / 9) - 1
        out[reg] = d
    return out


if __name__ == "__main__":
    txt = subprocess.run(["pdftotext", "-layout", sys.argv[1], "-"], capture_output=True, text=True, check=True).stdout
    areas = parse(txt.splitlines())
    missing = [a for a in AREA_TO_REGION if a not in areas or len(areas[a]) < 6]
    reg = aggregate(areas)
    res = dict(meta=dict(source="NERC 2025 Long-Term Reliability Assessment (published Feb 2026)", years=YEARS,
                         area_to_region=AREA_TO_REGION, missing_or_partial=missing), areas=areas, regions=reg)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), "demand_targets.json"), "w"), indent=1)
    print("missing/partial:", missing)
    for r, d in reg.items():
        print(f"{r:10s} NID 2026 {d['net_internal_demand'][0]/1000:6.1f} GW 2035 {d['net_internal_demand'][9]/1000:6.1f} "
              f"growth {100*d['growth_2026_35']:.1f}%/yr  RML {100*d['reference_margin_level'][0]:.1f}%  "
              f"ARM 2026 {100*d['anticipated_reserve_margin'][0]:.1f}% 2035 {100*d['anticipated_reserve_margin'][9]:.1f}%")
