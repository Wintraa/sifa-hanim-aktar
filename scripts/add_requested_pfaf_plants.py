# -*- coding: utf-8 -*-
"""Kullanicinin istedigi bitkileri pfaf.org'dan cekip siteye ekler."""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fetch_pfaf_data import fetch_html, parse, slugify  # noqa: E402
from pfaf_terms import HABIT  # noqa: E402
from build_site_from_pfaf import (  # noqa: E402
    flowering_time,
    harvest_time,
    growing_regions,
    light_need,
    water_need,
    soil_type,
    medicinal_actions,
    edible_summary,
    overview_text,
    rating_note,
)
from translate_geo_fields import translate_range  # noqa: E402
from friendly_habit_terms import friendly_habit, habit_sentence  # noqa: E402

LIVE = ROOT / "data" / "plants.json"
OUT_DIR = ROOT / "data" / "pfaf" / "raw"
INDEX = ROOT / "data" / "pfaf" / "pfaf_index.json"
HAZARD_TR = ROOT / "data" / "pfaf" / "hazards_tr.json"
HABITAT_TR = ROOT / "data" / "pfaf" / "habitats_tr.json"

# Turkce ad -> denenecek PFAF Latin adlari (sirayla)
TARGETS: list[dict] = [
    {
        "ad": "Udi Hindi",
        "latin_candidates": ["Saussurea costus", "Saussurea lappa", "Aucklandia costus"],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Yakı Otu",
        "latin_candidates": [
            "Epilobium angustifolium",
            "Chamerion angustifolium",
            "Chamaenerion angustifolium",
        ],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Funda",
        "latin_candidates": ["Calluna vulgaris", "Erica vulgaris"],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Yapışkan Andız Otu",
        "latin_candidates": ["Dittrichia viscosa", "Inula viscosa"],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Hint Yağı Otu",
        "latin_candidates": ["Ricinus communis"],
        "tur": "Tıbbi Bitkiler",
        "aliases": ["Castor", "Hint Otu"],
    },
    {
        "ad": "Pelesenk",
        "latin_candidates": ["Styrax officinalis", "Styrax officinale"],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Aspir",
        "latin_candidates": ["Carthamus tinctorius"],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Jojoba",
        "latin_candidates": ["Simmondsia chinensis"],
        "tur": "Tıbbi Bitkiler",
    },
    {
        "ad": "Nioli",
        "latin_candidates": ["Melaleuca quinquenervia", "Melaleuca viridiflora"],
        "tur": "Aromatik Bitkiler",
    },
]

# Zaten sitede olanlar (rapor icin)
ALREADY = [
    ("Aynısefa", "Calendula officinalis"),
    ("Rezene", "Foeniculum vulgare"),
    ("Ardıç", "Juniperus communis"),
    ("Anason", "Pimpinella anisum"),
    ("Biberiye", "Salvia rosmarinus"),
    ("Kişniş", "Coriandrum sativum"),
]


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_pfaf(candidates: list[str]) -> tuple[str, dict] | None:
    for latin in candidates:
        print(f"  PFAF ara: {latin}")
        html = fetch_html(latin)
        if not html:
            print("    HTML yok")
            time.sleep(1.2)
            continue
        parsed = parse(html, latin)
        if not parsed:
            print("    bos/yok")
            time.sleep(1.2)
            continue
        # parse zaten meaningful kontrolu yapiyor
        matched = parsed.get("displayLatinName") or latin
        print(f"    OK -> {matched}")
        return latin, parsed
    return None


def hazard_tr(latin: str, pfaf: dict, hazards: dict) -> str:
    key = latin.lower()
    for k, v in hazards.items():
        if k.lower() == key or k.lower().replace(" ", "") == key.replace(" ", ""):
            return v
    # Kisa Ingilizce hazard varsa basit ceviri degil; stub birak
    raw = (pfaf.get("knownHazards") or "").strip()
    if not raw or raw.lower() in {"none known", "none known."}:
        return "Kaynakta bilinen önemli bir uyarı belirtilmemiştir."
    # Ingilizceyi oldugu gibi birakmamak icin genel uyari
    return (
        "Kaynakta uyarılar belirtilmiştir; kullanım öncesi uzman görüşü alınmalıdır. "
        f"(Orijinal kayıt: {raw[:220].rstrip('.')}.)"
    )


def habitat_tr(latin: str, pfaf: dict, habitats: dict) -> str:
    key = latin.lower()
    for k, v in habitats.items():
        if k.lower() == key:
            return v
    detail = (pfaf.get("habitatsDetail") or pfaf.get("habitats") or "").strip()
    if not detail:
        return ""
    return translate_range(detail)


def build_entry(ad: str, latin: str, tur: str, pfaf: dict, next_id: int, hazards, habitats) -> dict:
    phys = pfaf.get("physicalCharacteristics") or ""
    habitat = habitat_tr(latin, pfaf, habitats)
    region_raw = growing_regions(pfaf.get("range", ""), pfaf.get("nativeRange", ""), habitat)
    region = translate_range(region_raw) if region_raw else ""

    habit_tr = ""
    for en in sorted(HABIT, key=len, reverse=True):
        if re.search(rf"\b{re.escape(en)}\b", phys, re.I):
            habit_tr = HABIT[en]
            break
    habit_tr = friendly_habit(habit_tr)
    family = (pfaf.get("family") or "").strip()

    actions_tr, _conds, _unknown = medicinal_actions(pfaf.get("medicinalUses", ""))
    edible = edible_summary(pfaf.get("edibleUses", ""))

    flower = flowering_time(phys)
    harvest = harvest_time(phys)
    light = light_need(phys)
    water = water_need(phys)
    soil = soil_type(phys)

    # Overview: build_site fonksiyonu + dostca habit
    overview = overview_text(ad, latin, pfaf, phys, region)
    # Overview icindeki eski habit kalintilarini dostcayla degistirmek yerine
    # yeniden kur
    intro = f"{ad} ({latin})"
    if family and habit_tr:
        overview = f"{intro}, {family} familyasından {habit_sentence(habit_tr)}."
    elif family:
        overview = f"{intro}, {family} familyasından bir bitkidir."
    else:
        overview = f"{intro}, {habit_sentence(habit_tr)}."
    m = re.search(r"growing to\s+([\d.]+)\s*m\b", phys, re.I)
    if m:
        overview += f" Yaklaşık {m.group(1)} m boya ulaşır."
    if region:
        first = region.split("Doğal ortamı:")[0].split(".")[0].strip()
        if first:
            overview += f" Doğal yayılış alanı: {first}."

    fayda = actions_tr.strip()
    if fayda and not fayda.endswith((".", "!", "?")):
        fayda = fayda[0].upper() + fayda[1:] + "."
    elif fayda:
        fayda = fayda[0].upper() + fayda[1:]

    kullanim = edible.strip()
    if kullanim:
        kullanim = re.sub(r"^Kullanım biçimi:\s*", "", kullanim, flags=re.I)
        kullanim = kullanim[0].upper() + kullanim[1:]
        if not kullanim.endswith((".", "!", "?")):
            kullanim += "."

    hazard = hazard_tr(latin, pfaf, hazards)
    if hazard and hazard[0].islower():
        hazard = hazard[0].upper() + hazard[1:]
    if hazard and not hazard.endswith((".", "!", "?")):
        hazard += "."

    bitki_turu = f"{habit_tr} ({family})" if family else habit_tr

    return {
        "id": next_id,
        "ad": ad,
        "botanikAd": latin,
        "tur": tur,
        "resimUrl": f"assets/plants/photos/{next_id:03d}-{slugify(latin)}.jpg",
        "genelTavsiyeMetni": overview,
        "temelBilgiler": {
            "turkceAdi": ad,
            "botanikAdi": latin,
            "bitkiTuru": bitki_turu.strip(),
        },
        "saglikKullanim": {
            "faydalari": fayda,
            "kullanimSekli": kullanim,
            "yanEtkilerUyarilar": hazard,
        },
        "cografyaMevsim": {
            "yetistigiYerler": region if region.endswith((".", "!", "?")) else (region + "." if region else ""),
            "hasatMevsimi": (harvest + ".") if harvest and not harvest.endswith(".") else harvest,
            "ciceklenmeZamani": (flower + ".") if flower and not flower.endswith(".") else flower,
        },
        "bakimYetistirme": {
            "isikIhtiyaci": light,
            "sulamaSikligi": water,
            "toprakTipi": (soil[0].upper() + soil[1:] + ".") if soil and not soil.endswith(".") else soil,
        },
        "kaynak": {
            "ad": "Plants For A Future (pfaf.org)",
            "url": pfaf.get("sourceUrl", ""),
            "cekimTarihi": pfaf.get("fetchedAt", ""),
            "eslesenAd": pfaf.get("pfafMatchedName", latin),
            "derece": rating_note(pfaf.get("medicinalRating", ""), pfaf.get("edibilityRating", "")),
        },
    }


def main() -> None:
    plants = load_json(LIVE, [])
    index = load_json(INDEX, {})
    hazards = load_json(HAZARD_TR, {})
    habitats = load_json(HABITAT_TR, {})
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    existing_bot = {(p.get("botanikAd") or "").lower() for p in plants}
    existing_ad = {(p.get("ad") or "").casefold() for p in plants}

    print("Zaten sitede olanlar:")
    for ad, latin in ALREADY:
        print(f"  - {ad} ({latin})")

    next_id = max((p["id"] for p in plants), default=0) + 1
    added = []
    failed = []

    for target in TARGETS:
        ad = target["ad"]
        if ad.casefold() in existing_ad:
            print(f"\n[{ad}] zaten var, atlandi")
            continue

        print(f"\n[{ad}]")
        found = find_pfaf(target["latin_candidates"])
        if not found:
            failed.append(ad)
            print("  BULUNAMADI")
            continue

        latin, pfaf = found
        if latin.lower() in existing_bot:
            print(f"  Botanik ad zaten var ({latin}), atlandi")
            continue

        # Ham kayit
        slug = slugify(latin)
        raw_path = OUT_DIR / f"{slug}.json"
        save_json(raw_path, pfaf)
        index[latin] = {
            "status": "ok",
            "raw": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
            "matchedName": pfaf.get("pfafMatchedName", latin),
            "sourceUrl": pfaf.get("sourceUrl", ""),
        }

        entry = build_entry(ad, latin, target["tur"], pfaf, next_id, hazards, habitats)
        # Gorsel yoksa gecici olarak SVG/placeholder yerine bos birakma; fetch script sonra doldurur
        # Mevcut kartlar photos/ bekliyor; yoksa kirik gosterir. Once mevcut bir yedek kullan.
        fallback = ROOT / "assets" / "plants" / "photos"
        # Placeholder: ayni klasorde henuz yoksa resimUrl'i sonra guncelle
        plants.append(entry)
        added.append((next_id, ad, latin))
        existing_bot.add(latin.lower())
        existing_ad.add(ad.casefold())
        next_id += 1
        time.sleep(1.5)

    save_json(LIVE, plants)
    save_json(INDEX, index)

    print("\n=== OZET ===")
    print(f"Eklenen: {len(added)}")
    for row in added:
        print(" ", row)
    print(f"Bulunamayan: {failed}")
    print(f"Toplam bitki: {len(plants)}")


if __name__ == "__main__":
    main()
