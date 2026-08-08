# -*- coding: utf-8 -*-
"""Belirli ID araligi icin eksik bitki fotograflarini indirir."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# mevcut yardimcilari yeniden kullan
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_missing_photos import (  # noqa: E402
    DATA,
    OUT_DIR,
    download,
    find_image,
    guess_ext,
    slugify,
)

START = 204
END = 212


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    ok = 0
    fail = []

    for plant in plants:
        pid = plant["id"]
        if not (START <= pid <= END):
            continue
        ad = plant["ad"]
        botanik = plant.get("botanikAd") or ""
        slug = slugify(botanik or ad)
        # mevcut dosya adi
        current = plant.get("resimUrl") or ""
        dest_rel = current if current.startswith("assets/") else f"assets/plants/photos/{pid:03d}-{slug}.jpg"
        dest = Path(DATA).resolve().parents[1] / dest_rel
        # ROOT: DATA = root/data/plants.json -> parents[1] = root
        root = DATA.resolve().parents[1]
        dest = root / dest_rel

        if dest.exists() and dest.stat().st_size > 2500:
            print(f"SKIP {pid} (var)")
            continue

        print(f"[{pid}] {ad} ({botanik}) ...")
        found = find_image(botanik, ad, "")
        if not found:
            fail.append((pid, ad, "kaynak yok"))
            print(f"FAIL {pid}")
            continue

        source_name, image_url = found
        ext = guess_ext(image_url)
        filename = f"{pid:03d}-{slug}{ext}"
        dest = OUT_DIR / filename
        try:
            download(image_url, dest)
            plant["resimUrl"] = f"assets/plants/photos/{filename}"
            ok += 1
            print(f"OK {pid} <- {source_name}")
        except Exception as exc:
            fail.append((pid, ad, str(exc)))
            print(f"FAIL {pid}: {exc}")
            if dest.exists():
                dest.unlink(missing_ok=True)
        time.sleep(1.0)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nOK={ok} FAIL={len(fail)}")
    for item in fail:
        print(" -", item)


if __name__ == "__main__":
    main()
