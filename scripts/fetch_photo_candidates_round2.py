# -*- coding: utf-8 -*-
"""Ilk turda cozulemeyen bitkiler icin hedefli aday indirme.

Sorunlar:
  45  Pelargonium x hortorum  -> takson adi melez isaretli, bulunamadi
  60  Cynara ... var. scolymus -> yabani kardon geldi, enginar basi gerek
  90  Withania somnifera      -> gecici SSL hatasi
  202 Salvia miltiorrhiza     -> adaylarda filigran var
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

CAND_DIR = Path(__file__).resolve().parent / "_candidates"
UA = "DogalBitkilerRehberi/1.4 (educational local project; plant card photos)"

# id -> denenecek iNaturalist arama terimleri (sirayla)
TARGETS: dict[int, list[str]] = {
    60: ["Cynara cardunculus scolymus"],
}

MAX_CANDIDATES = 6


def http_json(url: str, timeout: int = 45, retries: int = 3):
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(2 + attempt * 3)
    raise last  # type: ignore[misc]


def upscale(url: str) -> str:
    for size in ("square", "small", "thumb", "medium"):
        url = url.replace(f"/{size}.", "/large.")
    return url


def normalize(name: str) -> str:
    name = name.lower().replace("\u00d7", " ").replace(" x ", " ")
    name = name.replace(" var. ", " ").replace(" subsp. ", " ")
    return " ".join(name.split())


def search_taxa(term: str) -> list[dict]:
    query = urllib.parse.urlencode({"q": term, "per_page": 15})
    payload = http_json(f"https://api.inaturalist.org/v1/taxa?{query}")
    return payload.get("results") or []


def photos_for(term: str) -> list[str]:
    target = normalize(term)
    taxon_id = None
    for taxon in search_taxa(term):
        if normalize(taxon.get("name") or "") == target:
            taxon_id = taxon.get("id")
            break
    if taxon_id is None:
        return []

    urls: list[str] = []
    detail = http_json(f"https://api.inaturalist.org/v1/taxa/{taxon_id}")
    for taxon in detail.get("results") or []:
        for entry in taxon.get("taxon_photos") or []:
            photo = entry.get("photo") or {}
            src = photo.get("large_url") or photo.get("medium_url") or photo.get("url")
            if src:
                urls.append(upscale(str(src)))

    if len(urls) < MAX_CANDIDATES:
        time.sleep(0.6)
        params = urllib.parse.urlencode(
            {
                "taxon_id": taxon_id,
                "quality_grade": "research",
                "photos": "true",
                "per_page": 15,
                "order_by": "votes",
            }
        )
        obs = http_json(f"https://api.inaturalist.org/v1/observations?{params}")
        for record in obs.get("results") or []:
            for photo in record.get("photos") or []:
                if photo.get("url"):
                    urls.append(upscale(str(photo["url"])))

    seen: set[str] = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique


def download(url: str, dest: Path) -> None:
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as response:
                data = response.read()
            if len(data) < 8000:
                raise RuntimeError(f"cok kucuk ({len(data)})")
            dest.write_bytes(data)
            return
        except Exception:  # noqa: BLE001
            if attempt == 2:
                raise
            time.sleep(2 + attempt * 2)


def main() -> None:
    manifest_path = CAND_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for plant_id, terms in TARGETS.items():
        for old in CAND_DIR.glob(f"{plant_id:03d}-*.jpg"):
            old.unlink()

        urls: list[str] = []
        for term in terms:
            print(f"[{plant_id}] arama: {term}")
            try:
                urls = photos_for(term)
            except Exception as exc:  # noqa: BLE001
                print(f"   hata: {exc}")
                continue
            if urls:
                print(f"   {len(urls)} foto bulundu")
                break
            print("   eslesme yok")
            time.sleep(1.0)

        entries = []
        for idx, url in enumerate(urls[:MAX_CANDIDATES], start=1):
            dest = CAND_DIR / f"{plant_id:03d}-{idx}.jpg"
            try:
                download(url, dest)
                entries.append({"index": idx, "file": dest.name, "url": url})
                print(f"   aday {idx}: {dest.name}")
            except Exception as exc:  # noqa: BLE001
                print(f"   aday {idx} indirilemedi: {exc}")
            time.sleep(0.5)

        manifest[str(plant_id)] = entries
        time.sleep(1.0)

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("\nBitti.")


if __name__ == "__main__":
    main()
