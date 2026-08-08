# -*- coding: utf-8 -*-
"""Kalan Unsplash URL'lerini yerel photos klasorune indirir."""

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
OUT = ROOT / "assets" / "plants" / "photos"
UA = "DogalBitkilerRehberi/1.0"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))

    for plant in plants:
        url = plant["resimUrl"]
        if not url.startswith("https://"):
            continue

        dest = OUT / f"{plant['id']:02d}-web.jpg"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                dest.write_bytes(response.read())
            plant["resimUrl"] = f"assets/plants/photos/{dest.name}"
            print(f"OK {plant['id']} {plant['ad']} ({dest.stat().st_size} byte)")
        except Exception as exc:
            print(f"FAIL {plant['id']} {plant['ad']}: {exc}")
        time.sleep(0.4)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    local = sum(1 for plant in plants if plant["resimUrl"].startswith("assets/plants/photos/"))
    print(f"Yerel gorsel sayisi: {local}/{len(plants)}")


if __name__ == "__main__":
    main()
