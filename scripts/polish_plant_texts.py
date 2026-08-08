# -*- coding: utf-8 -*-
"""Bitki metinlerini sunum kalitesinde Turkceye duzenler.

- genelTavsiyeMetni: scrape sesi ('Veritabanında...') ve Ingilizce kalintilar kalkar
- Dil bilgisi: 'çalı bir bitkidir' -> 'bir çalıdır' vb.
- Noktalama / buyuk harf / 'Bilinen yok' stub'lari duzeltilir
- Isik cumleleri tekillestirilir
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
sys.path.insert(0, str(ROOT / "scripts"))

from translate_geo_fields import translate_range  # noqa: E402

HABIT_SENTENCE = {
    "tek yıllık": "tek yıllık bir bitkidir",
    "iki yıllık": "iki yıllık bir bitkidir",
    "çok yıllık": "çok yıllık bir bitkidir",
    "herdem yeşil çalı": "herdem yeşil bir çalıdır",
    "yaprak döken çalı": "yaprak döken bir çalıdır",
    "herdem yeşil ağaç": "herdem yeşil bir ağaçtır",
    "yaprak döken ağaç": "yaprak döken bir ağaçtır",
    "çalı": "bir çalıdır",
    "ağaç": "bir ağaçtır",
    "sarılıcı": "sarılıcı bir bitkidir",
    "soğanlı bitki": "soğanlı bir bitkidir",
    "eğrelti": "bir eğrelti otudur",
    "çok yıllık çalı": "çok yıllık bir çalıdır",
    "sarılıcı çalı": "sarılıcı bir çalıdır",
    "herdem yeşil": "herdem yeşil bir bitkidir",
}


def ensure_period(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if text[-1] not in ".!?…":
        text += "."
    return text


def capitalize_sentence(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return text[0].upper() + text[1:]


def split_habit_family(bitki_turu: str) -> tuple[str, str]:
    text = (bitki_turu or "").strip()
    m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text, ""


def habit_clause(habit: str) -> str:
    habit = habit.strip()
    if not habit:
        return "bir bitkidir"
    if "/" in habit:
        return f"{habit} formunda bir bitkidir"
    if habit in HABIT_SENTENCE:
        return HABIT_SENTENCE[habit]
    if habit.endswith("çalı"):
        prefix = habit[:-4].strip()
        return f"{prefix} bir çalıdır" if prefix else "bir çalıdır"
    if habit.endswith("ağaç"):
        prefix = habit[:-4].strip()
        return f"{prefix} bir ağaçtır" if prefix else "bir ağaçtır"
    if habit.endswith(("dir", "dır", "tir", "tır")):
        return habit
    return f"{habit} bir bitkidir"


def extract_height(overview: str) -> str:
    m = re.search(
        r"Yaklaşık\s+([\d.,]+)\s*m\s+boya\s+ulaşır\.?",
        overview or "",
        re.I,
    )
    if m:
        return f"Yaklaşık {m.group(1).replace(',', '.')} m boya ulaşır."
    return ""


def range_clause(yetistigi: str) -> str:
    text = (yetistigi or "").strip()
    if not text:
        return ""
    # Habitat cumlesini ayir
    if "Doğal ortamı:" in text:
        text = text.split("Doğal ortamı:", 1)[0].strip()
    text = translate_range(text)
    text = re.sub(r"^(Doğal yayılış(?: alanı)?\s*:\s*)", "", text, flags=re.I)
    text = text.rstrip(" .;")
    if not text:
        return ""
    return f"Doğal yayılış alanı: {text}."


def rebuild_overview(plant: dict) -> str:
    ad = plant.get("ad") or ""
    latin = plant.get("botanikAd") or plant.get("temelBilgiler", {}).get("botanikAdi") or ""
    habit, family = split_habit_family(
        (plant.get("temelBilgiler") or {}).get("bitkiTuru", "")
    )

    parts: list[str] = []
    intro = f"{ad} ({latin})" if latin else ad
    if family:
        parts.append(f"{intro}, {family} familyasından {habit_clause(habit)}.")
    else:
        parts.append(f"{intro}, {habit_clause(habit)}.")

    height = extract_height(plant.get("genelTavsiyeMetni") or "")
    if height:
        parts.append(height)

    region = range_clause((plant.get("cografyaMevsim") or {}).get("yetistigiYerler", ""))
    if region:
        parts.append(region)

    return " ".join(parts)


def polish_benefits(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    # Anlamsiz catch-all
    text = re.sub(r",?\s*diğer kullanımlar\b", "", text, flags=re.I)
    items = [i.strip(" ;,.") for i in re.split(r"\s*,\s*", text) if i.strip(" ;,.")]
    # Tekrarlari koru-sirali temizle
    seen: set[str] = set()
    clean = []
    for item in items:
        key = item.casefold()
        if key in seen:
            continue
        seen.add(key)
        clean.append(item)
    if not clean:
        return ""
    joined = ", ".join(clean)
    return capitalize_sentence(ensure_period(joined))


def polish_usage(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    text = re.sub(r"^Kullanım biçimi:\s*", "", text, flags=re.I)
    text = re.sub(r"^Kullanım şekli:\s*", "", text, flags=re.I)
    return capitalize_sentence(ensure_period(text))


def polish_hazards(text: str) -> str:
    text = (text or "").strip()
    if not text or text.casefold() in {
        "bilinen yok",
        "bilinen yok.",
        "bilinen risk yoktur",
        "bilinen risk yoktur.",
        "none known",
        "none known.",
        "yok",
        "yok.",
    }:
        return "Kaynakta bilinen önemli bir uyarı belirtilmemiştir."
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\(\s*", "(", text)
    text = re.sub(r"\s*\)", ")", text)
    return capitalize_sentence(ensure_period(text))


def dedupe_sentences(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text) if p.strip()]
    seen: set[str] = set()
    out = []
    for part in parts:
        key = re.sub(r"\s+", " ", part.casefold())
        if key in seen:
            continue
        seen.add(key)
        out.append(ensure_period(part) if not part.endswith((".", "!", "?")) else part)
    return " ".join(out)


def polish_soil(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    return capitalize_sentence(ensure_period(text))


def polish_geo_field(text: str, *, is_range: bool = False) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if is_range:
        # Habitat zaten TR; range kismini tekrar guvenli cevir
        if "Doğal ortamı:" in text:
            head, tail = text.split("Doğal ortamı:", 1)
            head = translate_range(head)
            text = f"{ensure_period(head)} Doğal ortamı: {tail.strip()}"
        else:
            text = translate_range(text)
    return ensure_period(text) if not text.endswith((".", "!", "?")) else text


def polish_plant(plant: dict) -> None:
    plant["genelTavsiyeMetni"] = rebuild_overview(plant)

    health = plant.setdefault("saglikKullanim", {})
    health["faydalari"] = polish_benefits(health.get("faydalari", ""))
    health["kullanimSekli"] = polish_usage(health.get("kullanimSekli", ""))
    health["yanEtkilerUyarilar"] = polish_hazards(health.get("yanEtkilerUyarilar", ""))

    geo = plant.setdefault("cografyaMevsim", {})
    geo["yetistigiYerler"] = polish_geo_field(geo.get("yetistigiYerler", ""), is_range=True)
    geo["hasatMevsimi"] = ensure_period(geo.get("hasatMevsimi", ""))
    geo["ciceklenmeZamani"] = ensure_period(geo.get("ciceklenmeZamani", ""))

    care = plant.setdefault("bakimYetistirme", {})
    care["isikIhtiyaci"] = dedupe_sentences(care.get("isikIhtiyaci", ""))
    care["sulamaSikligi"] = dedupe_sentences(care.get("sulamaSikligi", ""))
    care["toprakTipi"] = polish_soil(care.get("toprakTipi", ""))

    # Temel bilgiler: habit ifadesini duzgun birak
    temel = plant.setdefault("temelBilgiler", {})
    habit, family = split_habit_family(temel.get("bitkiTuru", ""))
    if habit or family:
        temel["bitkiTuru"] = (
            f"{habit} ({family})" if family else habit
        ).strip()


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    for plant in plants:
        polish_plant(plant)

    DATA.write_text(
        json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Hizli dogrulama ornekleri
    samples = [plants[0], plants[1], plants[10], plants[50]]
    report = []
    for p in samples:
        report.append(f"=== {p['id']} {p['ad']} ===")
        report.append(p["genelTavsiyeMetni"])
        report.append(f"fayda: {p['saglikKullanim'].get('faydalari','')[:120]}")
        report.append(f"uyarı: {p['saglikKullanim'].get('yanEtkilerUyarilar','')[:120]}")
        report.append("")
    (ROOT / "data_polish_sample.txt").write_text("\n".join(report), encoding="utf-8")
    print(f"OK {len(plants)} bitki duzenlendi")


if __name__ == "__main__":
    main()
