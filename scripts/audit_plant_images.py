# -*- coding: utf-8 -*-
"""Bitki gorsellerini denetler.

Kontroller:
  1. Dosya var mi?
  2. SVG yer tutucu mu (gercek foto degil)?
  3. Ayni gorsel birden fazla bitkide kullanilmis mi?
  4. Dosya adi botanik/turkce adla uyusuyor mu?
  5. Sifir/cok kucuk dosya var mi?
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"


def ascii_slug(text: str) -> str:
    text = text.replace("ı", "i").replace("İ", "i")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def main() -> None:
    plants = json.loads(LIVE.read_text(encoding="utf-8"))

    missing: list[str] = []
    svg_placeholder: list[str] = []
    tiny: list[str] = []
    name_mismatch: list[str] = []
    usage: dict[str, list[str]] = defaultdict(list)

    for plant in plants:
        url = plant.get("resimUrl") or ""
        path = ROOT / url
        label = f"{plant['id']:3} {plant['ad']} ({plant['botanikAd']})"
        usage[url].append(label)

        if not url or not path.exists():
            missing.append(f"{label} -> {url or '(bos)'}")
            continue

        size = path.stat().st_size
        if path.suffix.lower() == ".svg":
            svg_placeholder.append(f"{label} -> {url}")
        elif size < 8000:
            tiny.append(f"{label} -> {url} ({size} bayt)")

        stem = ascii_slug(path.stem)
        stem_words = {w for w in stem.split() if len(w) > 3 and not w.isdigit()}
        cand = ascii_slug(plant["botanikAd"]) + " " + ascii_slug(plant["ad"])
        cand_words = {w for w in cand.split() if len(w) > 3}

        generic = {"openverse", "inaturalist", "wikimedia", "photo", "plant", "commons"}
        informative = stem_words - generic
        if informative and not (informative & cand_words):
            name_mismatch.append(f"{label} -> {url}")

    duplicates = {u: labels for u, labels in usage.items() if len(labels) > 1}

    def block(title: str, rows: list[str]) -> None:
        print(f"\n=== {title}: {len(rows)} ===")
        for row in rows:
            print("  ", row)

    print(f"Toplam bitki: {len(plants)}")
    block("Gorsel dosyasi YOK", missing)
    block("SVG yer tutucu (gercek foto degil)", svg_placeholder)
    block("Cok kucuk dosya (<8KB)", tiny)
    block("Dosya adi bitkiyle uyusmuyor", name_mismatch)

    print(f"\n=== Ayni gorsel birden fazla bitkide: {len(duplicates)} ===")
    for url, labels in duplicates.items():
        print(f"   {url}")
        for lab in labels:
            print(f"      {lab}")


if __name__ == "__main__":
    main()
