# -*- coding: utf-8 -*-
"""Bitki turu ifadelerini kullanici dostu Turkceye cevirir.

'cok yillik', 'tek yillik', 'herdem yesil' gibi teknik botanik terimler
yerine gunluk dilde anlasilan karsiliklar kullanilir.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"

# Uzun ifadeler once eslesmeli
HABIT_FRIENDLY: list[tuple[str, str]] = [
    (
        "çok yıllık (ılıman iklimde yıllık gibi) otsu",
        "ılık iklimde yıllarca, soğukta bir mevsim yaşayan yumuşak gövdeli",
    ),
    (
        "tek yıllık / tropikte çok yıllık sarılıcı",
        "tırmanıcı; tropiklerde yıllarca, ılıman iklimde bir mevsim yaşayan",
    ),
    ("çok yıllık yumrulu otsu", "yumrulu, yıllarca yaşayan yumuşak gövdeli"),
    ("çok yıllık otsu süs", "yıllarca yaşayan süs"),
    ("sukulent çok yıllık", "etli yapraklı, yıllarca yaşayan"),
    ("rizomlu çok yıllık", "yeraltı gövdeli, yıllarca yaşayan"),
    ("çok yıllık otsu", "yıllarca yaşayan yumuşak gövdeli"),
    ("çok yıllık çalı", "yıllarca yaşayan çalı"),
    ("sarılıcı baklagil", "tırmanıcı baklagil"),
    ("sarılıcı çalı", "tırmanıcı çalı"),
    ("rizomlu geofit", "yeraltı gövdeli"),
    ("rizomlu otsu", "yeraltı gövdeli, yumuşak gövdeli"),
    ("epifitik orkide", "ağaç üzerinde yetişen orkide"),
    ("çalı / küçük ağaç", "çalı veya küçük ağaç"),
    ("herdem yeşil çalı", "kışın da yeşil kalan çalı"),
    ("herdem yeşil ağaç", "kışın da yeşil kalan ağaç"),
    ("yaprak döken çalı", "kışın yapraklarını döken çalı"),
    ("yaprak döken ağaç", "kışın yapraklarını döken ağaç"),
    ("soğanlı bitki", "soğanlı"),
    ("tek yıllık", "bir mevsim yaşayan"),
    ("iki yıllık", "iki yılda ömrünü tamamlayan"),
    ("çok yıllık", "yıllarca yaşayan"),
    ("herdem yeşil", "kışın da yeşil kalan"),
    ("sarılıcı", "tırmanıcı"),
    ("eğrelti", "eğrelti otu"),
]


def friendly_habit(habit: str) -> str:
    text = (habit or "").strip()
    if not text:
        return text
    # Once uzun kalıplar
    for old, new in HABIT_FRIENDLY:
        if text == old:
            return new
    # Parca parca (sirali uzunluk)
    for old, new in HABIT_FRIENDLY:
        if old in text:
            text = text.replace(old, new)
    return text


def habit_sentence(habit: str) -> str:
    """Tanitim cumlesi icin 'bir ...dir' ekini kurar."""
    h = friendly_habit(habit).strip()
    if not h:
        return "bir bitkidir"
    if h.endswith(("dir", "dır", "tir", "tır")):
        return h
    if "/" in h or ";" in h:
        return f"{h} bir bitkidir"
    if h.endswith("çalı"):
        prefix = h[: -len("çalı")].strip()
        return f"{prefix} bir çalıdır" if prefix else "bir çalıdır"
    if h.endswith("ağaç"):
        prefix = h[: -len("ağaç")].strip()
        return f"{prefix} bir ağaçtır" if prefix else "bir ağaçtır"
    if h.endswith("eğrelti otu"):
        return "bir eğrelti otudur"
    # 'yıllarca yaşayan' gibi sifatlarda ekstra 'bir' kullanma
    if any(
        h.endswith(s)
        for s in (
            "yaşayan",
            "tamamlayan",
            "gövdeli",
            "soğanlı",
            "tırmanıcı",
            "süs",
            "orkide",
            "baklagil",
        )
    ):
        return f"{h} bitkidir"
    return f"{h} bir bitkidir"


def split_habit_family(bitki_turu: str) -> tuple[str, str]:
    text = (bitki_turu or "").strip()
    m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text, ""


def extract_height(overview: str) -> str:
    m = re.search(r"Yaklaşık\s+([\d.,]+)\s*m\s+boya\s+ulaşır\.?", overview or "", re.I)
    if not m:
        return ""
    return f"Yaklaşık {m.group(1).replace(',', '.')} m boya ulaşır."


def range_clause(yetistigi: str) -> str:
    text = (yetistigi or "").strip()
    if not text:
        return ""
    if "Doğal ortamı:" in text:
        text = text.split("Doğal ortamı:", 1)[0].strip()
    text = re.sub(r"^(Doğal yayılış(?: alanı)?\s*:\s*)", "", text, flags=re.I)
    text = text.strip(" .;")
    if not text:
        return ""
    return f"Doğal yayılış alanı: {text}."


def rebuild_overview(plant: dict) -> str:
    ad = plant.get("ad") or ""
    latin = plant.get("botanikAd") or ""
    habit, family = split_habit_family(
        (plant.get("temelBilgiler") or {}).get("bitkiTuru", "")
    )
    habit = friendly_habit(habit)

    intro = f"{ad} ({latin})" if latin else ad
    parts: list[str] = []
    if family:
        parts.append(f"{intro}, {family} familyasından {habit_sentence(habit)}.")
    else:
        parts.append(f"{intro}, {habit_sentence(habit)}.")

    height = extract_height(plant.get("genelTavsiyeMetni") or "")
    if height:
        parts.append(height)

    region = range_clause((plant.get("cografyaMevsim") or {}).get("yetistigiYerler", ""))
    if region:
        parts.append(region)

    return " ".join(parts).replace("?.", "?")


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0

    for plant in plants:
        temel = plant.setdefault("temelBilgiler", {})
        habit, family = split_habit_family(temel.get("bitkiTuru", ""))
        new_habit = friendly_habit(habit)
        new_turu = f"{new_habit} ({family})" if family else new_habit
        new_turu = new_turu.strip()

        if new_turu != (temel.get("bitkiTuru") or "").strip():
            temel["bitkiTuru"] = new_turu
            changed += 1

        new_ov = rebuild_overview(plant)
        if new_ov != plant.get("genelTavsiyeMetni"):
            plant["genelTavsiyeMetni"] = new_ov
            changed += 1

    DATA.write_text(
        json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Ornek rapor
    from collections import Counter

    c = Counter()
    for p in plants:
        h, _ = split_habit_family((p.get("temelBilgiler") or {}).get("bitkiTuru", ""))
        c[h] += 1
    print(f"degisen alan guncellemesi ~{changed}")
    print("Yeni habit dagilimi:")
    for k, n in c.most_common(25):
        print(f"  {n:3}  {k}")
    print("\nOrnek tanitim:")
    print(plants[0]["genelTavsiyeMetni"])
    print(plants[1]["genelTavsiyeMetni"])


if __name__ == "__main__":
    main()
