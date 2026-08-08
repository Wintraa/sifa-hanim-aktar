# -*- coding: utf-8 -*-
"""Kalan habit dil bilgisi ve uyari stub duzeltmeleri."""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "plants.json"


def habit_clause(habit: str) -> str:
    habit = (habit or "").strip()
    if not habit:
        return "bir bitkidir"
    if "/" in habit:
        return f"{habit} formunda bir bitkidir"
    mapping = {
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
    if habit in mapping:
        return mapping[habit]
    if habit.endswith("çalı"):
        prefix = habit[:-4].strip()
        return f"{prefix} bir çalıdır" if prefix else "bir çalıdır"
    if habit.endswith("ağaç"):
        prefix = habit[:-4].strip()
        return f"{prefix} bir ağaçtır" if prefix else "bir ağaçtır"
    if habit.endswith(("dir", "dır", "tir", "tır")):
        return habit
    return f"{habit} bir bitkidir"


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


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    fixed = 0

    for plant in plants:
        habit, family = split_habit_family(
            (plant.get("temelBilgiler") or {}).get("bitkiTuru", "")
        )
        ad = plant.get("ad") or ""
        latin = plant.get("botanikAd") or ""
        intro = f"{ad} ({latin})" if latin else ad
        parts = []
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

        new_overview = " ".join(parts)
        if new_overview != plant.get("genelTavsiyeMetni"):
            plant["genelTavsiyeMetni"] = new_overview
            fixed += 1

        health = plant.setdefault("saglikKullanim", {})
        haz = (health.get("yanEtkilerUyarilar") or "").strip()
        if haz.casefold() in {
            "bilinen risk yoktur.",
            "bilinen risk yoktur",
            "bilinen yok",
            "bilinen yok.",
        }:
            health["yanEtkilerUyarilar"] = (
                "Kaynakta bilinen önemli bir uyarı belirtilmemiştir."
            )
            fixed += 1

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    leftovers = [
        (p["id"], p["ad"])
        for p in plants
        if "çalı bir bitki" in p["genelTavsiyeMetni"]
        or "ağaç bir bitki" in p["genelTavsiyeMetni"]
    ]
    print(f"fixed={fixed} leftovers={leftovers}")


if __name__ == "__main__":
    main()
