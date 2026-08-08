# -*- coding: utf-8 -*-
"""PFAF 'Habitats' (dogal ortam) metinlerini ceviri icin parcalara ayirir."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "pfaf" / "raw"
INDEX = ROOT / "data" / "pfaf" / "pfaf_index.json"
OUT_DIR = ROOT / "data" / "pfaf"
CHUNKS = 3


def main() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    items: list[tuple[str, str]] = []

    for latin, entry in sorted(index.items()):
        if entry.get("status") != "ok":
            continue
        path = RAW_DIR / entry["file"]
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        habitat = (data.get("habitatsDetail") or "").strip()
        if not habitat:
            continue
        habitat = re.sub(r"\s*\[[\d,\s\-K]+\]", "", habitat).strip()
        items.append((latin, habitat))

    print(f"Cevrilecek habitat metni: {len(items)}")
    size = (len(items) + CHUNKS - 1) // CHUNKS

    for i in range(CHUNKS):
        chunk = dict(items[i * size : (i + 1) * size])
        if not chunk:
            continue
        out = OUT_DIR / f"habitats_todo_{i + 1}.json"
        out.write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        chars = sum(len(v) for v in chunk.values())
        print(f"  {out.name}: {len(chunk)} kayit, {chars} karakter")


if __name__ == "__main__":
    main()
