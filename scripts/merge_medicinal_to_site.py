# -*- coding: utf-8 -*-
"""Medicinal veri setindeki benzersiz bitkileri site plants.json semasina ekler.

- Botanik adi zaten sitesinde olanlari atlar
- Yeni kayitlar id=106+ ile eklenir
- Gecici SVG kart gorseli uretir (sonra foto scripti gercek fotoyla degistirir)
- plants.json uzerine yazar; medicinal dosyalarina dokunmaz
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
MEDICINAL = ROOT / "data" / "medicinal" / "plants_all.json"
SVG_DIR = ROOT / "assets" / "plants"

CATEGORY_TO_TUR = {
    "Tıbbi Bitki": "Tıbbi Bitkiler",
    "Baharat": "Aromatik Bitkiler",
    "Çay": "Tıbbi Bitkiler",
    "Uçucu Yağ": "Aromatik Bitkiler",
}

BITKI_TURU = {
    "Tıbbi Bitkiler": "Tıbbi / şifalı bitki",
    "Aromatik Bitkiler": "Aromatik bitki veya baharat",
    "Süs Bitkileri": "Süs bitkisi",
}

PALETTES = [
    ("#F5EFE6", "#8D7B68", "#C8B6A6", "#A8A196"),
    ("#F3EDE4", "#6B8F71", "#A084E8", "#C8B6A6"),
    ("#F7F1E8", "#8D7B68", "#D4A373", "#A8A196"),
    ("#F2EBE3", "#7A6A5A", "#A084E8", "#9AAE8E"),
]


def slugify(name: str) -> str:
    table = str.maketrans(
        {
            "ı": "i",
            "İ": "i",
            "ğ": "g",
            "Ğ": "g",
            "ü": "u",
            "Ü": "u",
            "ş": "s",
            "Ş": "s",
            "ö": "o",
            "Ö": "o",
            "ç": "c",
            "Ç": "c",
            " ": "-",
            "'": "",
            "’": "",
        }
    )
    value = name.translate(table).lower()
    value = re.sub(r"[^a-z0-9\-]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "bitki"


def make_svg(name: str, plant_id: int) -> str:
    bg, accent, petal, leaf = PALETTES[plant_id % len(PALETTES)]
    safe = name.replace("&", "&amp;")
    return f"""<svg width="1200" height="900" viewBox="0 0 1200 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="900" rx="48" fill="{bg}"/>
  <rect x="52" y="52" width="1096" height="796" rx="36" fill="#FDFBF7" stroke="{petal}" stroke-width="6"/>
  <circle cx="220" cy="180" r="70" fill="{petal}" opacity="0.35"/>
  <circle cx="980" cy="220" r="110" fill="{leaf}" opacity="0.28"/>
  <path d="M600 690 V300" stroke="{accent}" stroke-width="14" stroke-linecap="round"/>
  <path d="M600 380 C480 300 390 360 360 470 C470 510 560 480 600 380Z" fill="{leaf}"/>
  <path d="M600 450 C720 360 820 410 850 520 C740 560 640 530 600 450Z" fill="{petal}"/>
  <circle cx="600" cy="280" r="48" fill="{accent}"/>
  <text x="600" y="790" text-anchor="middle" fill="#4A3E3D" font-family="Georgia, serif" font-size="44" font-weight="700">{safe}</text>
</svg>
"""


def map_plant(src: dict, new_id: int) -> dict:
    tur = CATEGORY_TO_TUR.get(src["category"], "Tıbbi Bitkiler")
    ad = src["commonNameTr"].strip()
    botanik = src["botanicalName"].strip()
    edible = (src.get("edibleParts") or "").strip()
    compounds = (src.get("activeCompounds") or "").strip()
    uses = (src.get("medicinalUses") or "").strip()
    warnings = (src.get("warnings") or "").strip()
    summary = (src.get("summary") or "").strip()
    en = (src.get("commonNameEn") or "").strip()

    kullanim = edible
    if compounds:
        kullanim = (
            f"{edible.rstrip('.')}. Etkin bileşenler arasında {compounds} sayılır."
            if edible
            else f"Etkin bileşenler: {compounds}."
        )

    slug = slugify(botanik or ad)
    svg_name = f"{new_id:03d}-{slug}.svg"
    svg_path = SVG_DIR / svg_name
    svg_path.write_text(make_svg(ad, new_id), encoding="utf-8")

    return {
        "id": new_id,
        "ad": ad,
        "botanikAd": botanik,
        "tur": tur,
        "resimUrl": f"assets/plants/{svg_name}",
        "genelTavsiyeMetni": summary or uses,
        "temelBilgiler": {
            "turkceAdi": ad,
            "botanikAdi": botanik,
            "bitkiTuru": f"{BITKI_TURU.get(tur, 'Şifalı bitki')}"
            + (f" ({en})" if en else ""),
        },
        "saglikKullanim": {
            "faydalari": uses,
            "kullanimSekli": kullanim or "Geleneksel demleme, ekstrakt veya baharat formunda değerlendirilir.",
            "yanEtkilerUyarilar": warnings,
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Türüne göre ılıman, Akdeniz veya tropik bölgelerde doğal veya kültüre alınmış olarak bulunur.",
            "hasatMevsimi": "Kullanılan kısma (yaprak, çiçek, kök, meyve) göre değişir; genelde çiçeklenme veya olgunlaşma döneminde.",
            "ciceklenmeZamani": "İklime ve türe bağlı olarak ilkbahar–yaz arası yaygındır.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Çoğu tür için güneşli veya yarı gölge konum uygundur.",
            "sulamaSikligi": "Toprak yüzeyinin kurumasına göre ölçülü sulama; tür spesifik ihtiyaçlara göre ayarlanır.",
            "toprakTipi": "İyi drene olan, orta verimli bahçe toprağı tercih edilir.",
        },
        "kaynakMedicinalId": src.get("id"),
    }


def main() -> None:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    live = json.loads(LIVE.read_text(encoding="utf-8"))
    medicinal = json.loads(MEDICINAL.read_text(encoding="utf-8"))

    existing_bots = {p["botanikAd"].lower().strip() for p in live}
    existing_names = {p["ad"].lower().strip() for p in live}
    next_id = max(p["id"] for p in live) + 1

    added = []
    skipped = 0
    for src in medicinal:
        bot = src["botanicalName"].lower().strip()
        if bot in existing_bots:
            skipped += 1
            continue
        # Ayni Turkce ad + farkli botanik nadir; yine de ad carpismasinda botanik oncelikli (yukarida)
        plant = map_plant(src, next_id)
        live.append(plant)
        existing_bots.add(bot)
        existing_names.add(plant["ad"].lower().strip())
        added.append(plant["id"])
        next_id += 1

    LIVE.write_text(json.dumps(live, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Eklendi: {len(added)} (id {added[0] if added else '-'}–{added[-1] if added else '-'})")
    print(f"Atlandi (botanik cakisma): {skipped}")
    print(f"Toplam site bitkisi: {len(live)}")


if __name__ == "__main__":
    main()
