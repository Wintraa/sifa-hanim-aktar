# -*- coding: utf-8 -*-
"""PFAF'ta ilk denemede bulunamayan turleri esanlamli/alternatif adlarla arar.

Silme karari oncesi son kontrol: bir tur PFAF'ta baska bir kabul gormus
adla kayitli olabilir. Bulunursa gercek veri cekilir ve hangi ad ile
eslendigi kayda yazilir (pfafMatchedName).
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_pfaf_data import INDEX, OUT_DIR, fetch_html, parse, slugify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"

# Bilinen esanlamli / PFAF'in kullandigi ad
KNOWN_SYNONYMS: dict[str, list[str]] = {
    "Aloe barbadensis Miller": ["Aloe vera"],
    "Salvia rosmarinus": ["Rosmarinus officinalis"],
    "Ocimum basilicum var. purpureum": ["Ocimum basilicum"],
    "Mentha piperita": ["Mentha x piperita", "Mentha × piperita"],
    "Pelargonium hortorum": ["Pelargonium x hortorum", "Pelargonium zonale"],
    "Senna alexandrina": ["Cassia senna", "Cassia angustifolia", "Senna alexandrina"],
    "Alpinia officinarum": ["Alpinia officinarum", "Alpinia galanga"],
    "Euphorbia pulcherrima": ["Euphorbia pulcherrima"],
    "Yucca elephantipes": ["Yucca gigantea", "Yucca elephantipes"],
    "Bougainvillea glabra": ["Bougainvillea glabra", "Bougainvillea spectabilis"],
    "Begonia semperflorens": ["Begonia cucullata", "Begonia semperflorens"],
    "Rhododendron simsii": ["Rhododendron simsii", "Rhododendron indicum"],
    "Chrysanthemum morifolium": ["Chrysanthemum x morifolium", "Chrysanthemum indicum"],
    "Impatiens walleriana": ["Impatiens walleriana"],
    "Spathiphyllum wallisii": ["Spathiphyllum wallisii"],
    "Nephrolepis exaltata": ["Nephrolepis exaltata"],
    "Kalanchoe blossfeldiana": ["Kalanchoe blossfeldiana"],
    "Alchemilla vulgaris": ["Alchemilla vulgaris", "Alchemilla xanthochlora"],
    "Curcuma zedoaria": ["Curcuma zedoaria"],
    "Zingiber zerumbet": ["Zingiber zerumbet"],
    "Alpinia galanga": ["Alpinia galanga"],
    "Kaempferia galanga": ["Kaempferia galanga"],
    "Piper longum": ["Piper longum"],
    "Mucuna pruriens": ["Mucuna pruriens"],
    "Commiphora mukul": ["Commiphora wightii", "Commiphora mukul"],
    "Boswellia serrata": ["Boswellia serrata"],
    "Styrax benzoin": ["Styrax benzoin"],
    "Salvia miltiorrhiza": ["Salvia miltiorrhiza"],
    "Harpagophytum procumbens": ["Harpagophytum procumbens"],
    "Curcuma longa": ["Curcuma longa", "Curcuma domestica"],
    "Elettaria cardamomum": ["Elettaria cardamomum"],
    "Pogostemon cablin": ["Pogostemon cablin", "Pogostemon patchouli"],
    "Citrus bergamia": ["Citrus bergamia", "Citrus aurantium"],
    "Momordica charantia": ["Momordica charantia"],
}


def variants(latin: str) -> list[str]:
    """Ad varyantlari uretir: yetkili adi at, var./spp. temizle, hibrit dene."""
    out: list[str] = []

    def add(v: str) -> None:
        v = re.sub(r"\s+", " ", v).strip()
        if v and v not in out:
            out.append(v)

    for known in KNOWN_SYNONYMS.get(latin, []):
        add(known)

    add(latin)

    # "Aloe barbadensis Miller" -> "Aloe barbadensis"
    add(re.sub(r"\s+(Miller|Mill\.|L\.|DC\.|Linn\.?)$", "", latin))

    # "var." / "ssp." / "subsp." sonrasini at
    add(re.split(r"\s+(?:var\.|ssp\.|subsp\.|cv\.)\s+", latin)[0])

    # "spp." iceren jenerik adlar -> cinsi tek basina denemek anlamsiz, atla
    without_spp = latin.replace(" spp.", "").replace(" sp.", "").strip()
    if without_spp != latin and " " in without_spp:
        add(without_spp)

    # Ilk iki kelime (cins + tur)
    parts = latin.split()
    if len(parts) >= 2:
        add(f"{parts[0]} {parts[1]}")
        add(f"{parts[0]} x {parts[1]}")

    return out


def main() -> None:
    plants = json.loads(LIVE.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}

    failed = [
        p
        for p in plants
        if index.get((p.get("botanikAd") or "").strip(), {}).get("status") != "ok"
    ]
    print(f"Yeniden denenecek: {len(failed)}\n")

    resolved = 0
    still_missing: list[tuple] = []

    for plant in failed:
        latin = (plant.get("botanikAd") or "").strip()
        if not latin:
            continue

        print(f"[{plant['id']}] {plant['ad']} ({latin})", flush=True)
        hit = None

        for candidate in variants(latin):
            if candidate.lower() == latin.lower() and index.get(latin, {}).get("status") == "not_found":
                # ilk turda zaten denendi
                continue
            html = fetch_html(candidate)
            record = parse(html, candidate) if html else None
            if record:
                hit = (candidate, record)
                break
            time.sleep(1.0)

        if hit:
            candidate, record = hit
            record["pfafMatchedName"] = candidate
            record["siteBotanicalName"] = latin
            slug = slugify(latin)
            (OUT_DIR / f"{slug}.json").write_text(
                json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            index[latin] = {
                "status": "ok",
                "file": f"{slug}.json",
                "matchedName": candidate,
            }
            resolved += 1
            print(f"  COZULDU -> {candidate}")
        else:
            index[latin] = {"status": "not_found"}
            still_missing.append((plant["id"], plant["ad"], latin))
            print("  HALA YOK")

        time.sleep(1.0)

    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nCozuldu: {resolved}   Hala bulunamadi: {len(still_missing)}")
    for item in still_missing:
        print("  -", item)


if __name__ == "__main__":
    main()
