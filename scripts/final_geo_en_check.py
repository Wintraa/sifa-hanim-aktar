# -*- coding: utf-8 -*-
"""Son kontrol: cografyaMevsim alanlarinda acik Ingilizce kelime var mi?"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / "data" / "plants.json").read_text(encoding="utf-8"))

# Bilinen Ingilizce baglac/yon/kalip kelimeleri (ozel ad DEGIL)
EN = re.compile(
    r"\b(?:"
    r"and|or|the|of|to|from|in|on|at|by|with|for|as|an|a|"
    r"including|naturalized|native|origin|obscure|uncertain|exact|"
    r"hybrid|garden|escape|cultivated|found|possibly|probably|"
    r"throughout|hemisphere|cosmopolitan|virtually|infrequent|casual|"
    r"east|west|north|south|eastern|western|northern|southern|central|"
    r"temperate|tropical|tropics|regions?|areas?|world|plant|habitat|"
    r"around|absent|excluding|eastwards|westwards|further|mountains|"
    r"arctic|barberry|coast|most|many|other|known|wild|arose|form|"
    r"centraland|scandanavia"
    r")\b",
    re.I,
)

# Latin bilimsel ad (C. cardunculus) kabul edilir
SCI = re.compile(r"\b[A-Z]\.\s*[a-z]+\b")

hits = []
for p in plants:
    c = p.get("cografyaMevsim") or {}
    for field in ("yetistigiYerler", "hasatMevsimi", "ciceklenmeZamani"):
        val = c.get(field) or ""
        # bilimsel adlari gecici maskele
        masked = SCI.sub("XX", val)
        found = EN.findall(masked)
        if found:
            hits.append((p["id"], p["ad"], field, found, val[:200]))

out = []
out.append(f"kalan={len(hits)}\n")
for row in hits:
    out.append(f"[{row[0]}] {row[1]} / {row[2]}\n  {row[3]}\n  {row[4]}\n")

(ROOT / "geo_final_check.txt").write_text("\n".join(out), encoding="utf-8")
print(f"kalan={len(hits)}")
