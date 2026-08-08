# -*- coding: utf-8 -*-
"""Secilen aday fotograflari kart gorseli olarak uygular.

Onceki indirici arama sonuclarini kor sekilde aldigi icin 12 bitkide
alakasiz gorsel olusmustu (mikroskop kesiti, Cince karakter, yanlis cins,
telif filigrani vb.). Buradaki eslemeler gorsel kontrolle tek tek secildi.

  python scripts/apply_photo_fixes.py --preview   # sadece onay sayfasi uretir
  python scripts/apply_photo_fixes.py             # plants.json'a uygular
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
PHOTO_DIR = ROOT / "assets" / "plants" / "photos"
CAND_DIR = Path(__file__).resolve().parent / "_candidates"
SHEET_DIR = Path(__file__).resolve().parent / "_contact"
LOG = ROOT / "data" / "photo_fixes.json"

# id -> (aday dosyasi, yeni dosya adi, degistirme gerekcesi)
SELECTION: dict[int, tuple[str, str, str]] = {
    31: ("031-1.jpg", "031-sambucus-nigra.jpg", "mikroskobik gövde kesiti görseli"),
    34: ("034-901.jpg", "034-ocimum-basilicum-purpureum.jpg", "mor değil yeşil fesleğen"),
    44: ("044-2.jpg", "044-chrysanthemum-morifolium.jpg", "fotoğraf değil Çince 菊 karakteri"),
    45: ("045-903.jpg", "045-pelargonium-hortorum.jpg", "Pelargonium değil gerçek Geranium"),
    60: ("060-905.jpg", "060-cynara-scolymus.jpg", "enginar değil bromelya benzeri rozet"),
    90: ("090-4.jpg", "090-withania-somnifera.jpg", "üzerinde telif filigranı vardı"),
    93: ("093-2.jpg", "093-chamaemelum-nobile.jpg", "ışınsız sarı çiçek, Roma papatyası değil"),
    97: ("097-1.jpg", "097-arnica-montana.jpg", "mercan rengi pompon çiçek, Arnica değil"),
    160: ("160-4.jpg", "160-cupressus-sempervirens.jpg", "yayvan kozalaklı, sütun servi değil"),
    179: ("179-2.jpg", "179-rosa-damascena.jpg", "tek katlı yabani gül, şam gülü değil"),
    188: ("188-3.jpg", "188-euphorbia-pulcherrima.jpg", "tanınmayan yabani form"),
    202: ("202-902.jpg", "202-salvia-miltiorrhiza.jpg", "bitki seçilmeyen uzak peyzaj karesi"),
}

CELL = 300
LABEL_H = 24
COLS = 4


def preview(plants: dict[int, dict]) -> None:
    """Secilen gorselleri tek sayfada onaya sunar."""
    items = sorted(SELECTION.items())
    rows = (len(items) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + LABEL_H)), (250, 248, 244))
    draw = ImageDraw.Draw(sheet)

    for i, (plant_id, (src, _, _)) in enumerate(items):
        x, y = (i % COLS) * CELL, (i // COLS) * (CELL + LABEL_H)
        img = Image.open(CAND_DIR / src).convert("RGB")
        img.thumbnail((CELL - 6, CELL - 6))
        sheet.paste(img, (x + 3, y + 3))
        draw.rectangle(
            [x, y, x + CELL - 1, y + CELL + LABEL_H - 1], outline=(200, 190, 175)
        )
        label = f"{plant_id} {plants[plant_id]['ad']} - {plants[plant_id]['botanikAd']}"
        draw.text((x + 5, y + CELL + 7), label[:46], fill=(40, 35, 35))

    out = SHEET_DIR / "final.jpg"
    sheet.save(out, quality=92)
    print(out)


def apply(plants_list: list[dict], plants: dict[int, dict]) -> None:
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    log = []

    for plant_id, (src, new_name, reason) in sorted(SELECTION.items()):
        plant = plants[plant_id]
        old_url = plant["resimUrl"]
        shutil.copyfile(CAND_DIR / src, PHOTO_DIR / new_name)
        plant["resimUrl"] = f"assets/plants/photos/{new_name}"

        old_path = ROOT / old_url
        still_used = any(p["resimUrl"] == old_url for p in plants_list)
        if old_path.exists() and not still_used:
            old_path.unlink()

        log.append(
            {
                "id": plant_id,
                "ad": plant["ad"],
                "botanikAd": plant["botanikAd"],
                "eskiGorsel": old_url,
                "yeniGorsel": plant["resimUrl"],
                "gerekce": reason,
            }
        )
        print(f"[{plant_id}] {plant['ad']}: {old_url} -> {plant['resimUrl']}")

    DATA.write_text(
        json.dumps(plants_list, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    LOG.write_text(
        json.dumps(
            {"tarih": date.today().isoformat(), "duzeltmeler": log},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\n{len(log)} görsel güncellendi. Kayıt: {LOG.relative_to(ROOT)}")


def main() -> None:
    plants_list = json.loads(DATA.read_text(encoding="utf-8"))
    plants = {p["id"]: p for p in plants_list}

    missing = [s for _, (s, _, _) in SELECTION.items() if not (CAND_DIR / s).exists()]
    if missing:
        raise SystemExit(f"Aday dosyalari eksik: {missing}")

    if "--preview" in sys.argv:
        preview(plants)
    else:
        apply(plants_list, plants)


if __name__ == "__main__":
    main()
