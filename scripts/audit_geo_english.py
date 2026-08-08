# -*- coding: utf-8 -*-
"""cografyaMevsim alanlarindaki Ingilizce kalintilari raporlar."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / "data" / "plants.json").read_text(encoding="utf-8"))

# Latin/Ingilizce kalinti ipuclari
EN_HINTS = re.compile(
    r"\b("
    r"Woodland|Grassland|Meadow|Hedge|Hedgerow|Coastal|Mountain|Alpine|"
    r"Cultivated|Garden|Waste|Ground|Soil|Sandy|Clay|Loam|Damp|Dry|Wet|"
    r"Shade|Sunny|Sun|Partial|Full|Moist|Rich|Poor|Nitrophilous|"
    r"Native|Range|Habitat|Found|Grows|Growing|Found in|Common|"
    r"Spring|Summer|Autumn|Fall|Winter|March|April|May|June|July|"
    r"August|September|October|November|December|January|February|"
    r"Europe|Asia|Africa|America|Mediterranean|China|India|Japan|"
    r"and|or|the|of|in|on|to|from|with|near|along|among|"
    r"forest|woods|scrub|heath|moor|bog|marsh|river|stream|bank|"
    r"roadside|field|pasture|orchard|vineyard|waste\s*places|"
    r"flowering|harvest|bloom|blooms|flowers|fruiting|"
    r"unknown|not known|N/?A|n/?a"
    r")\b",
    re.I,
)

fields = ["yetistigiYerler", "hasatMevsimi", "ciceklenmeZamani"]
hits: list[tuple] = []
word_counts: Counter = Counter()

for p in plants:
    c = p.get("cografyaMevsim") or {}
    for f in fields:
        val = (c.get(f) or "").strip()
        if not val:
            continue
        found = EN_HINTS.findall(val)
        if found:
            hits.append((p["id"], p["ad"], f, val[:180], found[:8]))
            for w in found:
                word_counts[w.lower()] += 1

print(f"Toplam bitki: {len(plants)}")
print(f"Ingilizce kalinti iceren alan: {len(hits)}")
print("\n=== En sik kelimeler ===")
for w, n in word_counts.most_common(40):
    print(f"  {n:4}  {w}")

print("\n=== Ornekler (ilk 25) ===")
for row in hits[:25]:
    print(f"[{row[0]}] {row[1]} / {row[2]}")
    print(f"    {row[3]}")
    print(f"    -> {row[4]}")
