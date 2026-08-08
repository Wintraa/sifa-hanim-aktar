# -*- coding: utf-8 -*-
"""SVG kalan bitkiler icin Wikipedia disi kaynaklardan foto ceker.

Kaynaklar (sirayla):
1) iNaturalist taxa API (bitki fotograflari)
2) Openverse (Creative Commons gorseller)
3) Wikimedia Commons MediaSearch (yedek; yavas)
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "plants.json"
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "plants" / "photos"
UA = "DogalBitkilerRehberi/1.1 (educational local project; photo fill for plant cards)"

# Botanik / arama ifadeleri (SVG kalanlar icin)
SEARCH_QUERIES: dict[int, list[str]] = {
    40: ["Petroselinum crispum", "parsley plant"],
    41: ["Anethum graveolens", "dill herb"],
    44: ["Cananga odorata", "ylang ylang flower"],
    45: ["Pogostemon cablin", "patchouli plant"],
    50: ["Rhododendron simsii", "azalea flower"],
    53: ["Pelargonium hortorum", "geranium flower"],
    55: ["Narcissus poeticus", "daffodil narcissus"],
    56: ["Hyacinthus orientalis", "hyacinth flower"],
    57: ["Lilium candidum", "madonna lily"],
    58: ["Impatiens walleriana", "busy lizzie impatiens"],
    62: ["Nephrolepis exaltata", "boston fern"],
    63: ["Euphorbia pulcherrima", "poinsettia"],
    64: ["Ficus elastica", "rubber plant"],
    65: ["Yucca elephantipes", "yucca plant"],
    68: ["Acacia dealbata", "mimosa acacia"],
    69: ["Panax ginseng", "ginseng plant"],
    71: ["Taraxacum officinale", "dandelion flower"],
    72: ["Capsella bursa-pastoris", "shepherd's purse"],
    74: ["Senna alexandrina", "senna plant"],
    76: ["Passiflora incarnata", "passionflower"],
    77: ["Silybum marianum", "milk thistle"],
    78: ["Cynara scolymus", "artichoke plant"],
    79: ["Momordica charantia", "bitter melon"],
    85: ["Plantago major", "plantain weed"],
    86: ["Arctostaphylos uva-ursi", "bearberry"],
    87: ["Vitex agnus-castus", "chaste tree"],
    88: ["Alchemilla vulgaris", "lady's mantle"],
    90: ["Aesculus hippocastanum", "horse chestnut"],
    92: ["Solidago virgaurea", "goldenrod"],
    94: ["Ziziphus jujuba", "jujube fruit"],
    95: ["Crataegus monogyna", "hawthorn"],
    96: ["Camellia sinensis", "tea plant"],
    97: ["Lycium barbarum", "goji berry"],
    98: ["Tribulus terrestris", "puncture vine"],
    102: ["Tussilago farfara", "coltsfoot"],
    103: ["Myrtus communis", "myrtle plant"],
    104: ["Salix alba", "white willow"],
}


def http_get_json(url: str, timeout: int = 45) -> dict | list:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, dest: Path) -> None:
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
    """iNaturalist taxa aramasindan default_photo al."""
    url = (
        "https://api.inaturalist.org/v1/taxa?"
        + urllib.parse.urlencode({"q": query, "rank": "species,genus", "per_page": 5})
    )
    payload = http_get_json(url)
    results = payload.get("results") or []
    for taxon in results:
        photo = taxon.get("default_photo") or {}
        # tercihen orta/buyuk
        for key in ("medium_url", "large_url", "square_url", "url"):
            src = photo.get(key)
            if src and src.startswith("http"):
                return src.replace("http://", "https://")
    return None


def from_openverse(query: str) -> str | None:
    """Openverse CC gorsel aramasi."""
    params = {
        "q": query,
        "page_size": 8,
        "license": "cc0,pdm,by,by-sa",
        "category": "photograph",
    }
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params)
    payload = http_get_json(url)
    results = payload.get("results") or []
    for item in results:
        # dogrudan indirme URL
        src = item.get("url") or item.get("thumbnail")
        if not src:
            continue
        title = (item.get("title") or "").lower()
        # cok alakasiz sonuclari biraz ele
        if any(bad in title for bad in ("logo", "icon", "map", "diagram", "clipart")):
            continue
        return src
    return None


def from_commons(query: str) -> str | None:
    """Wikimedia Commons MediaSearch (Wikipedia ozet API degil)."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6,
        "gsrlimit": 5,
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "iiurlwidth": 1200,
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    payload = http_get_json(url)
    pages = (payload.get("query") or {}).get("pages") or {}
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = (info.get("mime") or "").lower()
        if not mime.startswith("image/"):
            continue
        if "svg" in mime:
            continue
        src = info.get("thumburl") or info.get("url")
        if src:
            return src
    return None


SOURCES = (
    ("inaturalist", from_inaturalist),
    ("openverse", from_openverse),
    ("commons", from_commons),
)


def find_image(plant_id: int, botanik: str, ad: str) -> tuple[str, str] | None:
    queries = SEARCH_QUERIES.get(plant_id) or [botanik, ad]
    # botanik adi her zaman denensin
    if botanik and botanik not in queries:
        queries = [botanik, *queries]

    for source_name, source_fn in SOURCES:
        for query in queries:
            try:
                url = source_fn(query)
            except urllib.error.HTTPError as exc:
                print(f"  {source_name} HTTP {exc.code} ({query})")
                if exc.code == 429:
                    time.sleep(6)
                continue
            except Exception as exc:
                print(f"  {source_name} hata: {exc}")
                continue
            if url:
                return source_name, url
            time.sleep(0.4)
        time.sleep(0.6)
    return None


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    ok = 0
    failures: list[tuple] = []

    targets = [p for p in plants if "/photos/" not in p.get("resimUrl", "")]
    print(f"SVG kalan: {len(targets)}\n")

    for plant in targets:
        plant_id = plant["id"]
        ad = plant["ad"]
        botanik = plant.get("botanikAd") or ""
        print(f"[{plant_id}] {ad} ...")

        found = find_image(plant_id, botanik, ad)
        if not found:
            failures.append((plant_id, ad, "kaynak bulunamadi"))
            print(f"FAIL {plant_id} {ad}: kaynak yok")
            time.sleep(1.0)
            continue

        source_name, image_url = found
        slug = slugify(botanik or ad)
        ext = guess_ext(image_url)
        filename = f"{plant_id:02d}-{slug}{ext}"
        dest = OUT_DIR / filename

        try:
            download(image_url, dest)
            plant["resimUrl"] = f"assets/plants/photos/{filename}"
            ok += 1
            print(f"OK {plant_id} {ad} <- {source_name}")
        except Exception as exc:
            failures.append((plant_id, ad, str(exc)))
            print(f"FAIL {plant_id} {ad}: indirme {exc}")
            if dest.exists():
                dest.unlink(missing_ok=True)

        time.sleep(1.2)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTamamlandi. OK={ok} Basarisiz={len(failures)}")
    for item in failures:
        print(" -", item)


if __name__ == "__main__":
    main()
