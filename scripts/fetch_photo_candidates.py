# -*- coding: utf-8 -*-
"""Hatali kart fotograflari icin ADAY gorseller indirir.

Onceki indirici ilk arama sonucunu kor sekilde aliyordu; bu yuzden
bitkiyle alakasiz gorseller (mikroskop kesiti, Cince karakter vb.) girdi.

Bu script:
  * iNaturalist taksonunu ADI BIREBIR eslesecek sekilde dogrular,
  * o taksona ait birden fazla fotografi aday olarak indirir,
  * secim gorsel kontrolle yapilsin diye _candidates/ altina yazar.

Hicbir sey plants.json'a yazilmaz; secim apply_photo_fixes.py ile uygulanir.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(__file__).resolve().parent / "_candidates"
UA = "DogalBitkilerRehberi/1.4 (educational local project; plant card photos)"

# id -> (dogrulanacak takson adi, iNaturalist arama terimi)
# Kultur melezleri iNaturalist'te "x" isaretiyle tutulur (Rosa x damascena);
# eslestirme bu isareti yok sayar.
TARGETS: dict[int, tuple[str, str]] = {
    31: ("Sambucus nigra", "Sambucus nigra"),
    34: ("Ocimum basilicum", "Ocimum basilicum"),
    44: ("Chrysanthemum morifolium", "Chrysanthemum morifolium"),
    45: ("Pelargonium hortorum", "Pelargonium hortorum"),
    60: ("Cynara cardunculus", "Cynara cardunculus"),
    90: ("Withania somnifera", "Withania somnifera"),
    93: ("Chamaemelum nobile", "Chamaemelum nobile"),
    97: ("Arnica montana", "Arnica montana"),
    160: ("Cupressus sempervirens", "Cupressus sempervirens"),
    179: ("Rosa damascena", "Rosa damascena"),
    188: ("Euphorbia pulcherrima", "Euphorbia pulcherrima"),
    202: ("Salvia miltiorrhiza", "Salvia miltiorrhiza"),
}

MAX_CANDIDATES = 6


def http_json(url: str, timeout: int = 45):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def upscale(url: str) -> str:
    """iNaturalist foto url'ini buyuk boyuta cevirir."""
    for size in ("square", "small", "thumb", "medium"):
        url = url.replace(f"/{size}.", "/large.")
    return url


def normalize(name: str) -> str:
    """Melez isaretlerini ve fazla bosluklari temizler."""
    name = name.lower().replace("\u00d7", " ").replace(" x ", " ")
    return " ".join(name.split())


def find_taxon_id(search: str, expect: str) -> int | None:
    """Adi eslesen taksonun iNaturalist id'sini bulur."""
    query = urllib.parse.urlencode({"q": search, "per_page": 15})
    payload = http_json(f"https://api.inaturalist.org/v1/taxa?{query}")
    expect_n = normalize(expect)

    for taxon in payload.get("results") or []:
        name = normalize(taxon.get("name") or "")
        if name == expect_n or name.startswith(expect_n + " "):
            return taxon.get("id")
    return None


def taxon_photo_urls(search: str, expect: str) -> list[str]:
    """Dogrulanmis taksonun hem referans hem gozlem fotograflarini toplar."""
    taxon_id = find_taxon_id(search, expect)
    if taxon_id is None:
        return []

    urls: list[str] = []

    # 1) Taksonun kuratorlu referans fotograflari
    detail = http_json(f"https://api.inaturalist.org/v1/taxa/{taxon_id}")
    for taxon in detail.get("results") or []:
        for entry in taxon.get("taxon_photos") or []:
            photo = entry.get("photo") or {}
            src = photo.get("large_url") or photo.get("medium_url") or photo.get("url")
            if src:
                urls.append(upscale(str(src)))

    # 2) Yeterli aday yoksa arastirma duzeyinde gozlem fotograflari
    if len(urls) < MAX_CANDIDATES:
        time.sleep(0.5)
        params = urllib.parse.urlencode(
            {
                "taxon_id": taxon_id,
                "quality_grade": "research",
                "photos": "true",
                "per_page": 12,
                "order_by": "votes",
            }
        )
        obs = http_json(f"https://api.inaturalist.org/v1/observations?{params}")
        for record in obs.get("results") or []:
            for photo in record.get("photos") or []:
                src = photo.get("url")
                if src:
                    urls.append(upscale(str(src)))

    seen: set[str] = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique[:MAX_CANDIDATES]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    if len(data) < 8000:
        raise RuntimeError(f"gorsel cok kucuk ({len(data)} bayt)")
    dest.write_bytes(data)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.jpg"):
        old.unlink()

    manifest: dict[str, list[dict]] = {}

    for plant_id, (expect, search) in TARGETS.items():
        print(f"[{plant_id}] {search} (beklenen takson: {expect})")
        try:
            urls = taxon_photo_urls(search, expect)
        except Exception as exc:  # noqa: BLE001
            print(f"   arama hatasi: {exc}")
            urls = []

        if not urls:
            print("   ADAY BULUNAMADI")
            manifest[str(plant_id)] = []
            time.sleep(1.0)
            continue

        entries = []
        for idx, url in enumerate(urls, start=1):
            dest = OUT_DIR / f"{plant_id:03d}-{idx}.jpg"
            try:
                download(url, dest)
                entries.append({"index": idx, "file": dest.name, "url": url})
                print(f"   aday {idx}: {dest.name}")
            except Exception as exc:  # noqa: BLE001
                print(f"   aday {idx} indirilemedi: {exc}")
            time.sleep(0.4)

        manifest[str(plant_id)] = entries
        time.sleep(1.0)

    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    total = sum(len(v) for v in manifest.values())
    print(f"\nToplam {total} aday indirildi -> {OUT_DIR}")


if __name__ == "__main__":
    main()
