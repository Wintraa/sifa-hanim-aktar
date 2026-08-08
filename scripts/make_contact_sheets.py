# -*- coding: utf-8 -*-
"""Tum bitki gorsellerinden numarali kontak sayfalari uretir.

Boylece her gorsel tek tek acilmadan toplu olarak gozden gecirilebilir.
Cikti: scripts/_contact/sheet_<n>.jpg
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
OUT_DIR = Path(__file__).resolve().parent / "_contact"

COLS = 6
ROWS = 6
CELL = 190
LABEL_H = 26


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("sheet_*.jpg"):
        old.unlink()

    plants = json.loads(LIVE.read_text(encoding="utf-8"))
    per_sheet = COLS * ROWS

    for sheet_idx in range((len(plants) + per_sheet - 1) // per_sheet):
        chunk = plants[sheet_idx * per_sheet : (sheet_idx + 1) * per_sheet]
        sheet = Image.new(
            "RGB", (COLS * CELL, ROWS * (CELL + LABEL_H)), (250, 248, 244)
        )
        draw = ImageDraw.Draw(sheet)

        for i, plant in enumerate(chunk):
            col, row = i % COLS, i // COLS
            x, y = col * CELL, row * (CELL + LABEL_H)

            path = ROOT / plant["resimUrl"]
            try:
                img = Image.open(path).convert("RGB")
                img.thumbnail((CELL - 6, CELL - 6))
                sheet.paste(img, (x + 3, y + 3))
            except Exception as exc:  # noqa: BLE001
                draw.text((x + 6, y + 40), f"HATA\n{exc}"[:60], fill=(180, 40, 40))

            draw.rectangle(
                [x, y, x + CELL - 1, y + CELL + LABEL_H - 1], outline=(200, 190, 175)
            )
            # Kimlik: id + botanik ad (ASCII'ye zorlamadan, PIL varsayilan fontu)
            label = f"{plant['id']} {plant['botanikAd']}"
            draw.text((x + 5, y + CELL + 6), label[:34], fill=(40, 35, 35))

        out = OUT_DIR / f"sheet_{sheet_idx + 1}.jpg"
        sheet.save(out, quality=88)
        print(f"{out}  ({len(chunk)} gorsel, id {chunk[0]['id']}-{chunk[-1]['id']})")


if __name__ == "__main__":
    main()
