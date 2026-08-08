# -*- coding: utf-8 -*-
"""Belirli sorunlu kayitlari goster."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = {p["id"]: p for p in json.loads((ROOT / "data" / "plants.json").read_text(encoding="utf-8"))}

ids = [38, 40, 44, 49, 54, 55, 57, 60, 75, 76, 79, 80, 91, 113]
lines = []
for i in ids:
    p = plants[i]
    y = p["cografyaMevsim"]["yetistigiYerler"]
    lines.append(f"[{i}] {p['ad']}\n{y}\n")

(ROOT / "geo_problem_ids.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok")
