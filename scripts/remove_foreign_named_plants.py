# -*- coding: utf-8 -*-
"""Turkce karsiligi olmayan / yabanci adli bitkileri plants.json'dan cikarir."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
REMOVED_LOG = ROOT / "data" / "removed_foreign_named_plants.json"

# Tam adi yabanci dilde kalan veya Turkce yaygin adi olmayan kayitlar
FOREIGN_NAMES = {
    "Yerba Mate",
    "Guarana",
    "Goji Berry",
    "Gotu Kola",
    "Ylang-Ylang",
    "Yucca",
    "Amla",
    "Neem",
    "Brahmi",
    "Gurmar",
    "Guduchi",
    "Guggul",
    "Damiana",
    "Jiaogulan",
    "Cascara",
    "Ginseng",
    "Sibirya Ginsengi",
    "Ginkgo Biloba",
    "Andrografis",
    "Grindelya",
    "Şizandra",
    "Şatavari",
    "Aloe Vera",
    "Acı Aloe",
    "Bellerik Hile",
    "Kara Hile",
    "Oregon Üzümü",
    "Amerikan Takke Otu",
}


def main() -> None:
    plants = json.loads(LIVE.read_text(encoding="utf-8"))
    removed = [p for p in plants if p.get("ad") in FOREIGN_NAMES]
    kept = [p for p in plants if p.get("ad") not in FOREIGN_NAMES]

    # Bulunamayan hedef adlari uyar
    found = {p["ad"] for p in removed}
    missing = sorted(FOREIGN_NAMES - found)
    if missing:
        print("Listede yok (zaten silinmis olabilir):", ", ".join(missing))

    for new_id, plant in enumerate(kept, start=1):
        plant["eskiId"] = plant.get("eskiId", plant["id"])
        plant["id"] = new_id

    LIVE.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REMOVED_LOG.write_text(
        json.dumps(
            [
                {
                    "id": p.get("eskiId", p["id"]),
                    "ad": p["ad"],
                    "botanikAd": p["botanikAd"],
                    "tur": p.get("tur"),
                }
                for p in removed
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Kaldirilan: {len(removed)}")
    print(f"Kalan: {len(kept)}")
    for p in sorted(removed, key=lambda x: x["ad"].casefold()):
        print(f"  - {p['ad']} ({p['botanikAd']})")


if __name__ == "__main__":
    main()
