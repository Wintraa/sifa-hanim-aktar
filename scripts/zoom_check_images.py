# -*- coding: utf-8 -*-
"""Belirli id'lerdeki gorselleri buyuk boyutta kontrol sayfasina dizer.

Kullanim: python scripts/zoom_check_images.py 9 31 34 41
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
OUT_DIR = Path(__file__).resolve().parent / "_contact"

COLS = 3
CELL = 300
LABEL_H = 26


def main() -> None:
    ids = [int(a) for a in sys.argv[1:]]
    if not ids:
        raise SystemExit("id listesi gerekli")

    plants = {p["id"]: p for p in json.loads(LIVE.read_text(encoding="utf-8"))}
    picked = [plants[i] for i in ids if i in plants]

    rows = (len(picked) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + LABEL_H)), (250, 248, 244))
    draw = ImageDraw.Draw(sheet)

    for i, plant in enumerate(picked):
        col, row = i % COLS, i // COLS
        x, y = col * CELL, row * (CELL + LABEL_H)
        try:
            img = Image.open(ROOT / plant["resimUrl"]).convert("RGB")
            img.thumbnail((CELL - 6, CELL - 6))
            sheet.paste(img, (x + 3, y + 3))
        except Exception as exc:  # noqa: BLE001
            draw.text((x + 6, y + 40), str(exc)[:60], fill=(180, 40, 40))
        draw.rectangle(
            [x, y, x + CELL - 1, y + CELL + LABEL_H - 1], outline=(200, 190, 175)
        )
        draw.text(
            (x + 5, y + CELL + 7), f"{plant['id']} {plant['botanikAd']}"[:44],
            fill=(40, 35, 35),
        )

    out = OUT_DIR / "zoom.jpg"
    sheet.save(out, quality=92)
    print(out)


if __name__ == "__main__":
    main()
