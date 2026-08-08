# -*- coding: utf-8 -*-
"""Eksik kart fotograflarini Wikipedia/Wikimedia olmadan doldurur.

Kaynaklar: iNaturalist -> Openverse (CC)
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
OUT_DIR = ROOT / "assets" / "plants" / "photos"
UA = "DogalBitkilerRehberi/1.3 (educational local project; plant card photos)"


def http_get_json(url: str, timeout: int = 45) -> dict | list:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, dest: Path) -> None:
    # Wikimedia hostlarini bilinçli atla
    host = urllib.parse.urlparse(url).netloc.lower()
    if any(x in host for x in ("wikimedia", "wikipedia", "wikidata")):
        raise RuntimeError(f"wikimedia atlandi: {host}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    if len(data) < 2500:
        raise RuntimeError("gorsel cok kucuk")
    dest.write_bytes(data)


def slugify(text: str) -> str:
    text = text.lower().replace(" ", "-")
    text = re.sub(r"[^a-z0-9\-]+", "", text)
    return text[:60] or "plant"


def guess_ext(url: str) -> str:
    lower = url.lower().split("?")[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if lower.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def from_inaturalist(query: str) -> str | None:
    url = (
        "https://api.inaturalist.org/v1/taxa?"
        + urllib.parse.urlencode({"q": query, "rank": "species,genus", "per_page": 8})
    )
    payload = http_get_json(url)
    for taxon in payload.get("results") or []:
        photo = taxon.get("default_photo") or {}
        for key in ("medium_url", "large_url", "url", "square_url"):
            src = photo.get(key)
            if not src or not str(src).startswith("http"):
                continue
            src = str(src).replace("http://", "https://")
            host = urllib.parse.urlparse(src).netloc.lower()
            if "wikimedia" in host or "wikipedia" in host:
                continue
            return src
    return None


def from_openverse(query: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "page_size": 12,
            "license": "cc0,pdm,by,by-sa",
            "category": "photograph",
        }
    )
    url = f"https://api.openverse.org/v1/images/?{params}"
    payload = http_get_json(url)
    for item in payload.get("results") or []:
        src = item.get("url") or item.get("thumbnail")
        if not src or not str(src).startswith("http"):
            continue
        host = urllib.parse.urlparse(str(src)).netloc.lower()
        if any(x in host for x in ("wikimedia", "wikipedia", "wikidata")):
            continue
        return str(src)
    return None


SOURCES = (
    ("inaturalist", from_inaturalist),
    ("openverse", from_openverse),
)


def find_image(botanik: str, ad: str, en_hint: str = "") -> tuple[str, str] | None:
    queries: list[str] = []
    for q in (botanik, en_hint, ad):
        q = (q or "").strip()
        if q and q.lower() not in {x.lower() for x in queries}:
            queries.append(q)

    for source_name, source_fn in SOURCES:
        for query in queries:
            try:
                url = source_fn(query)
            except urllib.error.HTTPError as exc:
                print(f"  {source_name} HTTP {exc.code} ({query})")
                if exc.code == 429:
                    time.sleep(10)
                continue
            except Exception as exc:
                print(f"  {source_name} hata: {exc}")
                continue
            if url:
                return source_name, url
            time.sleep(0.4)
        time.sleep(0.5)
    return None


def english_hint(plant: dict) -> str:
    """temelBilgiler.bitkiTuru icindeki (English Name) ipucunu cek."""
    bitki = plant.get("temelBilgiler", {}).get("bitkiTuru") or ""
    m = re.search(r"\(([^)]+)\)\s*$", bitki)
    return m.group(1).strip() if m else ""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    targets = [p for p in plants if "/photos/" not in str(p.get("resimUrl", ""))]
    print(f"Foto bekleyen: {len(targets)} (kaynak: iNaturalist + Openverse)\n")

    ok = 0
    failures: list[tuple] = []

    for plant in targets:
        plant_id = plant["id"]
        ad = plant["ad"]
        botanik = plant.get("botanikAd") or ""
        hint = english_hint(plant)
        print(f"[{plant_id}] {ad} ({botanik}) ...")

        found = find_image(botanik, ad, hint)
        if not found:
            failures.append((plant_id, ad, "kaynak yok"))
            print(f"FAIL {plant_id}")
            time.sleep(0.8)
            continue

        source_name, image_url = found
        slug = slugify(botanik or ad)
        ext = guess_ext(image_url)
        filename = f"{plant_id:03d}-{slug}{ext}"
        dest = OUT_DIR / filename

        try:
            download(image_url, dest)
            plant["resimUrl"] = f"assets/plants/photos/{filename}"
            ok += 1
            print(f"OK {plant_id} <- {source_name}")
        except Exception as exc:
            # Indirme basarisizsa ayni kaynak zincirinde sonraki deneme icin
            # Openverse'e dusmek uzere bir kez daha dene (farkli query)
            retry = None
            for q in (botanik, hint, f"{botanik} plant", ad):
                if not q:
                    continue
                try:
                    alt = from_openverse(q)
                    if alt:
                        retry = alt
                        break
                except Exception:
                    continue
            if retry:
                try:
                    download(retry, dest)
                    plant["resimUrl"] = f"assets/plants/photos/{filename}"
                    ok += 1
                    print(f"OK {plant_id} <- openverse-retry")
                except Exception as exc2:
                    failures.append((plant_id, ad, str(exc2)))
                    print(f"FAIL {plant_id}: {exc2}")
                    if dest.exists():
                        dest.unlink(missing_ok=True)
            else:
                failures.append((plant_id, ad, str(exc)))
                print(f"FAIL {plant_id}: {exc}")
                if dest.exists():
                    dest.unlink(missing_ok=True)

        if ok and ok % 8 == 0:
            DATA.write_text(
                json.dumps(plants, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        time.sleep(1.1)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTamamlandi. OK={ok} Basarisiz={len(failures)}")
    for item in failures:
        print(" -", item)


if __name__ == "__main__":
    main()
