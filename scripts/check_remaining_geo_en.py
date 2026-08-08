# -*- coding: utf-8 -*-
"""Kalan sorunlu yetistigiYerler kayitlarini listeler."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / "data" / "plants.json").read_text(encoding="utf-8"))

EN = re.compile(
    r"\b(?:and|or|the|of|to|from|in|including|Naturalized|naturalized|"
    r"east|west|north|south|origin|hybrid|garden|escape|cultivated|"
    r"obscure|uncertain|hemisphere|cosmopolitan|virtually|throughout|"
    r"absent|excluding|eastwards|around|infrequent|casual|form|"
    r"Barberry|Coast|Most|Centraland|arose|known|wild|Exact|"
    r"Bolivia|Colombia|Costa|Rica|Nigeria|Gabon|Zaire|Mongolia|"
    r"Wales|Scotland|Ireland|Britain|America|Tropical|Temperate|"
    r"many|other|areas|regions|plant|habitat|Native|Original)\b",
    re.I,
)

out = []
for p in plants:
    val = (p.get("cografyaMevsim") or {}).get("yetistigiYerler") or ""
    range_part = val.split("Doğal ortamı:")[0]
    hits = EN.findall(range_part)
    if hits:
        out.append(f"[{p['id']}] {p['ad']}\n  hits={hits}\n  {range_part.strip()}\n")

(ROOT / "geo_remaining.txt").write_text("\n".join(out) or "TEMİZ\n", encoding="utf-8")
print(f"kalan={len(out)}")
