# -*- coding: utf-8 -*-
"""Yalnızca SVG'de kalan (fotoğrafı olmayan) bitkiler için Wikipedia görseli çeker."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from fetch_plant_photos import WIKI_TITLES, UA, fetch_summary, pick_image, download

DATA = Path(__file__).resolve().parents[1] / "data" / "plants.json"
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "plants" / "photos"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    failures = []
    ok = 0

    for plant in plants:
        if "/photos/" in plant.get("resimUrl", ""):
            continue

        plant_id = plant["id"]
        title = WIKI_TITLES.get(plant_id)
        if not title:
            failures.append((plant_id, plant["ad"], "title yok"))
            continue

        try:
            summary = fetch_summary(title)
            image_url = pick_image(summary)
            if not image_url:
                failures.append((plant_id, plant["ad"], "gorsel yok"))
                time.sleep(2.5)
                continue

            ext = ".jpg"
            lower = image_url.lower()
            if ".png" in lower:
                ext = ".png"
            elif ".webp" in lower:
                ext = ".webp"
            elif ".jpeg" in lower:
                ext = ".jpeg"

            filename = f"{plant_id:02d}-{title.lower().replace('_', '-')}{ext}"
            dest = OUT_DIR / filename
            download(image_url, dest)
            plant["resimUrl"] = f"assets/plants/photos/{filename}"
            ok += 1
            print(f"OK {plant_id} {plant['ad']} <- {title}")
        except Exception as exc:
            failures.append((plant_id, plant["ad"], str(exc)))
            print(f"FAIL {plant_id} {plant['ad']}: {exc}")
            # Rate limit'te daha uzun bekle
            if "429" in str(exc):
                time.sleep(8)
                continue

        time.sleep(2.5)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTamamlandi. OK={ok} Basarisiz={len(failures)}")
    for item in failures:
        print(" -", item)


if __name__ == "__main__":
    main()
