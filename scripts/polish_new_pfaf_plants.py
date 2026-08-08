# -*- coding: utf-8 -*-
"""Yeni eklenen PFAF bitkilerini Turkceye cilala + Nioli'yi alternatif kaynaktan ekle."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from translate_geo_fields import translate_range  # noqa: E402
from friendly_habit_terms import friendly_habit, habit_sentence  # noqa: E402

LIVE = ROOT / "data" / "plants.json"
RAW = ROOT / "data" / "pfaf" / "raw"
TODAY = date.today().isoformat()


def ensure_period(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if text[-1] not in ".!?":
        text += "."
    return text


def capitalize(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    first = text[0]
    tr_map = {
        "i": "İ",
        "ı": "I",
        "ş": "Ş",
        "ğ": "Ğ",
        "ü": "Ü",
        "ö": "Ö",
        "ç": "Ç",
    }
    if first in tr_map:
        return tr_map[first] + text[1:]
    return first.upper() + text[1:]


def polish_geo(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if "Doğal ortamı:" in text:
        head, tail = text.split("Doğal ortamı:", 1)
        head = translate_range(head)
        # Habitat hala Ingilizce olabilir; basit ceviri sozlugu
        tail = translate_range(tail)
        tail = habitat_extra(tail)
        text = f"{ensure_period(head)} Doğal ortamı: {ensure_period(tail.lstrip())}"
    else:
        text = translate_range(text)
        text = habitat_extra(text)
    return ensure_period(text)


def habitat_extra(text: str) -> str:
    pairs = [
        (r"\bRocky ground\b", "Kayalık zemin"),
        (r"\bwaste (places|ground|areas?)\b", "boş araziler"),
        (r"\bWaste places\b", "Boş araziler"),
        (r"\bAcid soils?\b", "Asit topraklar"),
        (r"\bDry rocky slopes\b", "Kuru kayalık yamaçlar"),
        (r"\blimestone\b", "kireçtaşı"),
        (r"\bWoods?\b", "ormanlar"),
        (r"\bthickets?\b", "çalılıklar"),
        (r"\bPoor dry soils\b", "Zayıf kuru topraklar"),
        (r"\bfull sun\b", "tam güneş"),
        (r"\bWell[- ]drained desert\b", "İyi drene çöl"),
        (r"\bdesert scrub\b", "çöl çalılığı"),
        (r"\birrigated\b", "sulanmış"),
        (r"\bmetres?\b", "metre"),
        (r"\bIntroduced\b", "Sonradan getirilmiş"),
        (r"\bfew localities\b", "birkaç yerleşim"),
        (r"\bLess abundant\b", "Daha az yaygın"),
        (r"\bits range\b", "yayılış alanında"),
        (r"\bMuch\b", "Büyük kısmı"),
        (r"\bSouthwestern\b", "Güneybatı"),
        (r"\bnorthwest\b", "kuzeybatı"),
        (r"\bCalifornia\b", "Kaliforniya"),
        (r"\bArizona\b", "Arizona"),
        (r"\bPakistan\b", "Pakistan"),
        (r"\bHimachal\b", "Himaçal"),
        (r"\bAvoid during\b", "Şu dönemde kaçının:"),
    ]
    for pat, repl in pairs:
        text = re.sub(pat, repl, text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def hazard_from_raw(botanik: str) -> str | None:
    slug = botanik.lower().replace(" ", "-")
    path = RAW / f"{slug}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    raw = (data.get("knownHazards") or "").strip()
    if not raw or raw.lower().startswith("none known"):
        return "Kaynakta bilinen önemli bir uyarı belirtilmemiştir."

    # Bilinen kritik bitkiler icin elle Turkce
    special = {
        "ricinus communis": (
            "Bitkinin tüm kısımları, özellikle tohumları, rikinin toksini nedeniyle "
            "yüksek derecede zehirlidir; yenmemelidir. Hint yağı yalnızca endüstriyel/"
            "eczacılıkta arıtılmış formda kullanılır. Tohumları çocuklardan uzak tutun."
        ),
        "epilobium angustifolium": (
            "Genel olarak güvenli kabul edilir; yine de tıbbi amaçlı kullanımda "
            "doz ve süre için uzman görüşü alınmalıdır."
        ),
        "carthamus tinctorius": (
            "Gebelikte yüksek dozlarda kullanılmamalıdır. Safra yolu tıkanıklığında "
            "dikkatli olunmalıdır. Alerji öyküsü olanlar hekime danışmalıdır."
        ),
    }
    key = botanik.lower()
    if key in special:
        return special[key]

    return (
        "Kaynakta kullanım uyarıları belirtilmiştir; tıbbi amaçlı kullanımdan önce "
        "uzman görüşü alınmalıdır."
    )


def polish_plant(plant: dict) -> None:
    geo = plant.setdefault("cografyaMevsim", {})
    geo["yetistigiYerler"] = polish_geo(geo.get("yetistigiYerler", ""))
    geo["hasatMevsimi"] = ensure_period(geo.get("hasatMevsimi", ""))
    geo["ciceklenmeZamani"] = ensure_period(geo.get("ciceklenmeZamani", ""))

    health = plant.setdefault("saglikKullanim", {})
    haz = hazard_from_raw(plant.get("botanikAd", ""))
    if haz:
        health["yanEtkilerUyarilar"] = haz
    elif not (health.get("yanEtkilerUyarilar") or "").strip():
        health["yanEtkilerUyarilar"] = (
            "Kaynakta bilinen önemli bir uyarı belirtilmemiştir."
        )

    if health.get("faydalari"):
        health["faydalari"] = capitalize(ensure_period(health["faydalari"]))
    if health.get("kullanimSekli"):
        health["kullanimSekli"] = capitalize(ensure_period(health["kullanimSekli"]))

    care = plant.setdefault("bakimYetistirme", {})
    for k in ("isikIhtiyaci", "sulamaSikligi", "toprakTipi"):
        if care.get(k):
            care[k] = capitalize(ensure_period(care[k]))

    # Overview yayilisini guncel geo ile senkronla
    temel = plant.get("temelBilgiler") or {}
    habit = re.sub(r"\s*\([^)]*\)\s*$", "", temel.get("bitkiTuru", "")).strip()
    habit = friendly_habit(habit)
    family_m = re.search(r"\(([^)]+)\)\s*$", temel.get("bitkiTuru", ""))
    family = family_m.group(1) if family_m else ""
    ad = plant["ad"]
    latin = plant["botanikAd"]
    intro = f"{ad} ({latin})"
    if family and habit:
        ov = f"{intro}, {family} familyasından {habit_sentence(habit)}."
    elif family:
        ov = f"{intro}, {family} familyasından bir bitkidir."
    else:
        ov = f"{intro}."
    m = re.search(r"Yaklaşık\s+([\d.]+)\s*m", plant.get("genelTavsiyeMetni", ""))
    if m:
        ov += f" Yaklaşık {m.group(1)} m boya ulaşır."
    yer = geo.get("yetistigiYerler") or ""
    first = yer.split("Doğal ortamı:")[0].split(".")[0].strip()
    if first:
        ov += f" Doğal yayılış alanı: {first}."
    plant["genelTavsiyeMetni"] = ov


def add_nioli(plants: list[dict]) -> dict:
    next_id = max(p["id"] for p in plants) + 1
    entry = {
        "id": next_id,
        "ad": "Nioli",
        "botanikAd": "Melaleuca quinquenervia",
        "tur": "Aromatik Bitkiler",
        "resimUrl": f"assets/plants/photos/{next_id:03d}-melaleuca-quinquenervia.jpg",
        "genelTavsiyeMetni": (
            "Nioli (Melaleuca quinquenervia), Myrtaceae familyasından kışın da yeşil kalan "
            "bir ağaçtır. Yaklaşık 8–20 m boya ulaşabilir. Doğal yayılış alanı: Avustralya, "
            "Yeni Kaledonya ve çevresi."
        ),
        "temelBilgiler": {
            "turkceAdi": "Nioli",
            "botanikAdi": "Melaleuca quinquenervia",
            "bitkiTuru": "kışın da yeşil kalan ağaç (Myrtaceae)",
        },
        "saglikKullanim": {
            "faydalari": (
                "Yapraklarından elde edilen nioli (niaouli) uçucu yağı geleneksel olarak "
                "solunum yollarını rahatlatıcı, antiseptik ve aromaterapi amaçlı kullanılır."
            ),
            "kullanimSekli": (
                "Uçucu yağ formunda aromaterapide; yalnızca seyreltilmiş olarak harici "
                "kullanım için uygundur."
            ),
            "yanEtkilerUyarilar": (
                "Uçucu yağ yutulmamalıdır. Çocuklarda, gebelikte ve hassas ciltlerde "
                "dikkatli kullanılmalıdır. Seyreltilmeden cilde uygulanmamalıdır. "
                "PFAF veritabanında bu türe ait kayıt bulunamamıştır; bilgiler Kew POWO "
                "ve farmakognozi kaynaklarına dayanır."
            ),
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Avustralya doğusu, Yeni Gine ve Yeni Kaledonya; tropik–subtropik "
                "kıyı ve sulak alanlarda yetişir. Bazı bölgelerde istilacı olabilir."
            ),
            "hasatMevsimi": "Yaprak hasadı sıcak mevsimde yapılır.",
            "ciceklenmeZamani": "İlkbahar - sonbahar (iklime göre değişir).",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya yarı gölge ister.",
            "sulamaSikligi": "Nemli toprağı sever; sulak alanlara dayanıklıdır.",
            "toprakTipi": "Çeşitli topraklarda yetişebilir; nemli, iyi güneş alan konumları tercih eder.",
        },
        "kaynak": {
            "ad": "Kew POWO / farmakognozi kaynakları (PFAF'ta kayıt yok)",
            "url": "https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:598027-1",
            "cekimTarihi": TODAY,
            "eslesenAd": "Melaleuca quinquenervia",
            "not": "Niaouli / nioli uçucu yağının kaynağı; PFAF'ta tür sayfası bulunamadı.",
        },
    }
    plants.append(entry)
    return entry


def main() -> None:
    plants = json.loads(LIVE.read_text(encoding="utf-8"))
    new_ids = {204, 205, 206, 207, 208, 209, 210, 211}

    for plant in plants:
        if plant["id"] in new_ids:
            polish_plant(plant)

    if not any(p["botanikAd"] == "Melaleuca quinquenervia" for p in plants):
        nioli = add_nioli(plants)
        print("Nioli eklendi:", nioli["id"])
    else:
        print("Nioli zaten var")

    LIVE.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Toplam:", len(plants))


if __name__ == "__main__":
    main()
