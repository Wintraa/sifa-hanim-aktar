#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hayvan modeli / zayif eslesmeleri ornekVaka'dan cikarir."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANTS = ROOT / "data" / "plants.json"
RAW = ROOT / "data" / "pubmed-vakalar-progress.json"
OZET = ROOT / "data" / "pubmed-vaka-ozetleri.json"


def is_animal(blob: str) -> bool:
    return bool(
        re.search(
            r"\b(rat|rats|mice|mouse|murine|in vitro|cell line|sıçan|fare modeli|hayvan modeli)\b",
            blob,
            re.I,
        )
    )


def main() -> None:
    plants = json.loads(PLANTS.read_text(encoding="utf-8"))
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    removed = 0

    for plant in plants:
        vaka = plant.get("ornekVaka")
        if not vaka:
            continue
        pid = str(plant["id"])
        entry = raw.get(pid, {})
        blob = " ".join(
            [
                vaka.get("baslik", ""),
                vaka.get("anlatim", ""),
                vaka.get("makaleBasligi", ""),
                entry.get("title", "") or "",
                entry.get("abstract", "") or "",
            ]
        )
        if is_animal(blob):
            del plant["ornekVaka"]
            removed += 1

    PLANTS.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = sum(1 for p in plants if p.get("ornekVaka"))
    print(f"removed_animal={removed} remaining={n}")


if __name__ == "__main__":
    main()
