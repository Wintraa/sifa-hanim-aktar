# -*- coding: utf-8 -*-
"""Ornek yetistigiYerler degerlerini UTF-8 dosyaya yazar."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / "data" / "plants.json").read_text(encoding="utf-8"))

out = []
for p in plants[:40]:
    c = p.get("cografyaMevsim") or {}
    out.append(f"=== [{p['id']}] {p['ad']} ===")
    out.append(f"YER: {c.get('yetistigiYerler', '')}")
    out.append(f"HASAT: {c.get('hasatMevsimi', '')}")
    out.append(f"CICEK: {c.get('ciceklenmeZamani', '')}")
    out.append("")

# Ayrica 25 dogrulanmis-alternatif kaynakli bitki (id buyuk olanlar)
for p in plants:
    if p["id"] >= 181:
        c = p.get("cografyaMevsim") or {}
        out.append(f"=== [{p['id']}] {p['ad']} ===")
        out.append(f"YER: {c.get('yetistigiYerler', '')}")
        out.append(f"HASAT: {c.get('hasatMevsimi', '')}")
        out.append(f"CICEK: {c.get('ciceklenmeZamani', '')}")
        out.append("")

(ROOT / "geo_samples.txt").write_text("\n".join(out), encoding="utf-8")
print("yazildi", len(out))
