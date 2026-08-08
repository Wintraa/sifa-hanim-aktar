# -*- coding: utf-8 -*-
"""Yedekten sorunlu kayitlarin orijinal metnini goster."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
backup = {
    p["id"]: p
    for p in json.loads((ROOT / "data" / "plants.backup-pre-geo-tr.json").read_text(encoding="utf-8"))
}
ids = [38, 40, 44, 49, 50, 54, 55, 57, 60, 75, 76, 79, 80, 91, 113]
lines = []
for i in ids:
    p = backup[i]
    lines.append(f"[{i}] {p['ad']}\nORIG: {p['cografyaMevsim']['yetistigiYerler']}\n")

(ROOT / "geo_orig_problem.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok")
