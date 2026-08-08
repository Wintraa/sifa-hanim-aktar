# -*- coding: utf-8 -*-
"""Safran kaydini ve 'bir ... bir bitkidir' tekrarini duzeltir."""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "plants.json"

NO_EXTRA_BIR = (
    "yaşayan",
    "tamamlayan",
    "gövdeli",
    "soğanlı",
    "tırmanıcı",
    "süs",
    "orkide",
    "baklagil",
)


def habit_sentence(habit: str) -> str:
    h = (habit or "").strip()
    if not h:
        return "bir bitkidir"
    if "/" in h or ";" in h:
        return f"{h} bir bitkidir"
    if h.endswith(("dir", "dır", "tir", "tır")):
        return h
    if h.endswith("çalı"):
        prefix = h[: -len("çalı")].strip()
        return f"{prefix} bir çalıdır" if prefix else "bir çalıdır"
    if h.endswith("ağaç"):
        prefix = h[: -len("ağaç")].strip()
        return f"{prefix} bir ağaçtır" if prefix else "bir ağaçtır"
    if h.endswith("eğrelti otu"):
        return "bir eğrelti otudur"
    if any(h.endswith(s) for s in NO_EXTRA_BIR):
        return f"{h} bitkidir"
    return f"{h} bir bitkidir"


def split_hf(text: str) -> tuple[str, str]:
    text = (text or "").strip()
    m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text, ""


def height(overview: str) -> str:
    m = re.search(r"Yaklaşık\s+([\d.,]+)\s*m\s+boya\s+ulaşır\.?", overview or "", re.I)
    if not m:
        return ""
    return f"Yaklaşık {m.group(1).replace(',', '.')} m boya ulaşır."


def region(yetistigi: str) -> str:
    text = (yetistigi or "").strip()
    if not text:
        return ""
    if "Doğal ortamı:" in text:
        text = text.split("Doğal ortamı:", 1)[0].strip()
    text = re.sub(r"^(Doğal yayılış(?: alanı)?\s*:\s*)", "", text, flags=re.I)
    text = text.strip(" .;")
    return f"Doğal yayılış alanı: {text}." if text else ""


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))

    for plant in plants:
        if plant["id"] == 27:
            plant["temelBilgiler"]["bitkiTuru"] = "soğanlı (Iridaceae)"

        habit, family = split_hf((plant.get("temelBilgiler") or {}).get("bitkiTuru", ""))
        ad = plant.get("ad") or ""
        latin = plant.get("botanikAd") or ""
        intro = f"{ad} ({latin})" if latin else ad
        parts = []
        if family:
            parts.append(f"{intro}, {family} familyasından {habit_sentence(habit)}.")
        else:
            parts.append(f"{intro}, {habit_sentence(habit)}.")

        h = height(plant.get("genelTavsiyeMetni") or "")
        if h:
            parts.append(h)
        r = region((plant.get("cografyaMevsim") or {}).get("yetistigiYerler", ""))
        if r:
            parts.append(r)

        plant["genelTavsiyeMetni"] = " ".join(parts).replace("?.", "?")

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    samples = [p for p in plants if p["id"] in (1, 2, 27)]
    for p in samples:
        print(p["id"], p["temelBilgiler"]["bitkiTuru"])
        print(" ", p["genelTavsiyeMetni"])


if __name__ == "__main__":
    main()
