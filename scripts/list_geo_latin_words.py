# -*- coding: utf-8 -*-
"""yetistigiYerler alanlarindaki benzersiz Ingilizce kalintilari listeler."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plants = json.loads((ROOT / "data" / "plants.json").read_text(encoding="utf-8"))

# Latin harflerle baslayan / iceren Ingilizce kelime gruplarini yakala
LATIN = re.compile(r"[A-Za-z][A-Za-z.'\-]{1,}")

skip = {
    # Zaten Turkceye gecmis / ozel adlar (latin yazimi kabul edilebilir olanlar yok;
    # hepsini raporla, sonra karar ver)
}

for field in ("yetistigiYerler", "hasatMevsimi", "ciceklenmeZamani"):
    words = {}
    for p in plants:
        val = (p.get("cografyaMevsim") or {}).get(field) or ""
        for w in LATIN.findall(val):
            # Turkce karakter iceren kelimeleri atla (ornegin "Avrupa" zaten TR)
            # Ama "Avrupa" tamamen Latin harf - hepsini sayacagiz
            key = w
            words[key] = words.get(key, 0) + 1

    # Sadece birden fazla gecen veya acik Ingilizce olanlar
    print(f"\n===== {field} ({len(words)} benzersiz latin kelime) =====")
    for w, n in sorted(words.items(), key=lambda x: (-x[1], x[0].lower())):
        print(f"  {n:4}  {w}")
