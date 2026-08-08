# -*- coding: utf-8 -*-
"""Indirilen aday fotograflari gorsel secim icin sayfalara dizer."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

CAND_DIR = Path(__file__).resolve().parent / "_candidates"
OUT_DIR = Path(__file__).resolve().parent / "_contact"
ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"

CELL = 235
LABEL_H = 24
COLS = 6

# Yalnizca belirli kaynagi gostermek icin: 0 = hepsi, 900 = Openverse adaylari
MIN_INDEX = int(__import__("os").environ.get("MIN_INDEX", "0"))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("cand_*.jpg"):
        old.unlink()

    manifest = json.loads((CAND_DIR / "manifest.json").read_text(encoding="utf-8"))
    plants = {p["id"]: p for p in json.loads(LIVE.read_text(encoding="utf-8"))}

    rows = []
    for pid, entries in manifest.items():
        picked = [e for e in entries if e["index"] >= MIN_INDEX]
        if picked:
            rows.append((int(pid), picked))
    rows.sort()

    # her sayfada 3 bitki (3 satir)
    per_page = 3
    for page in range((len(rows) + per_page - 1) // per_page):
        chunk = rows[page * per_page : (page + 1) * per_page]
        sheet = Image.new(
            "RGB", (COLS * CELL, len(chunk) * (CELL + LABEL_H)), (250, 248, 244)
        )
        draw = ImageDraw.Draw(sheet)

        for r, (pid, entries) in enumerate(chunk):
            y = r * (CELL + LABEL_H)
            for c, entry in enumerate(entries[:COLS]):
                x = c * CELL
                try:
                    img = Image.open(CAND_DIR / entry["file"]).convert("RGB")
                    img.thumbnail((CELL - 6, CELL - 6))
                    sheet.paste(img, (x + 3, y + 3))
                except Exception as exc:  # noqa: BLE001
                    draw.text((x + 6, y + 40), str(exc)[:50], fill=(180, 40, 40))
                draw.rectangle(
                    [x, y, x + CELL - 1, y + CELL + LABEL_H - 1],
                    outline=(200, 190, 175),
                )
                tag = f"{pid} #{entry['index']}  {plants[pid]['botanikAd']}"
                draw.text((x + 5, y + CELL + 6), tag[:38], fill=(40, 35, 35))

        out = OUT_DIR / f"cand_{page + 1}.jpg"
        sheet.save(out, quality=90)
        print(f"{out}  -> {[pid for pid, _ in chunk]}")


if __name__ == "__main__":
    main()
