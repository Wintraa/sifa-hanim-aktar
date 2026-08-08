#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PubMed ham vaka özetlerini plants.json içindeki ornekVaka alanına işler.
Türkçe anlatımlar data/pubmed-vaka-ozetleri.json dosyasından okunur;
yoksa güvenli bir iskelet (PMID + makale başlığı) bırakılır.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANTS_PATH = ROOT / "data" / "plants.json"
RAW_PATH = ROOT / "data" / "pubmed-vakalar-progress.json"
OZET_PATH = ROOT / "data" / "pubmed-vaka-ozetleri.json"


def main() -> None:
    plants = json.loads(PLANTS_PATH.read_text(encoding="utf-8"))
    raw = json.loads(RAW_PATH.read_text(encoding="utf-8")) if RAW_PATH.exists() else {}
    ozetler = json.loads(OZET_PATH.read_text(encoding="utf-8")) if OZET_PATH.exists() else {}

    updated = 0
    cleared = 0

    for plant in plants:
        pid = str(plant.get("id"))
        entry = raw.get(pid)
        ozet = ozetler.get(pid) or ozetler.get(plant.get("id"))

        if plant.get("tur") != "Tıbbi Bitkiler":
            if "ornekVaka" in plant:
                del plant["ornekVaka"]
                cleared += 1
            continue

        if not entry or entry.get("status") != "ok" or not entry.get("pmid"):
            if "ornekVaka" in plant:
                del plant["ornekVaka"]
                cleared += 1
            continue

        vaka = {
            "baslik": (ozet or {}).get("baslik")
            or f"{plant.get('ad')} — PubMed klinik vaka deneyimi",
            "sorun": (ozet or {}).get("sorun") or "Klinik vaka raporunda tanımlanan sağlık sorunu.",
            "yaklasim": (ozet or {}).get("yaklasim")
            or f"{plant.get('ad')} ({plant.get('botanikAd')}) içeren bitkisel yaklaşım klinik olarak belgelenmiştir.",
            "sonuc": (ozet or {}).get("sonuc") or "Ayrıntılar PubMed vaka raporunda yer almaktadır.",
            "anlatim": (ozet or {}).get("anlatim")
            or (
                f"PubMed’de yayımlanan gerçek bir klinik vaka raporuna göre {plant.get('ad')} "
                f"ile ilişkili bir hasta deneyimi belgelenmiştir. Makale: “{entry.get('title') or 'Klinik vaka'}”. "
                f"Tam metin ve bağlam için kaynak bağlantısını inceleyebilirsiniz."
            ),
            "pubmedId": str(entry["pmid"]),
            "pubmedUrl": entry.get("url") or f"https://pubmed.ncbi.nlm.nih.gov/{entry['pmid']}/",
            "makaleBasligi": entry.get("title") or "",
            "yil": entry.get("year") or "",
        }

        plant["ornekVaka"] = vaka
        updated += 1

    PLANTS_PATH.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Guncellendi: {updated} | temizlenen: {cleared}")


if __name__ == "__main__":
    main()
