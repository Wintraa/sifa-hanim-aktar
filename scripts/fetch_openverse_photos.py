# -*- coding: utf-8 -*-
"""Eksik bitki gorsellerini Openverse API ile indirir."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
OUT = ROOT / "assets" / "plants" / "photos"
UA = "DogalBitkilerRehberi/1.0 (educational plant directory)"

QUERIES = {
    10: "Ocimum basilicum basil plant",
    12: "Tilia tomentosa linden flowers",
    14: "turmeric curcuma longa rhizome",
    15: "Echinacea purpurea flower",
    16: "Foeniculum vulgare fennel",
    17: "Melissa officinalis lemon balm",
    18: "Urtica dioica stinging nettle",
    19: "Achillea millefolium yarrow",
    21: "Pimpinella anisum anise",  # may already have
    23: "Rosa canina rose hips",
    25: "Hypericum perforatum St Johns wort",
    26: "Trigonella foenum-graecum fenugreek",
    29: "Laurus nobilis bay laurel leaves",
    30: "Glycyrrhiza glabra liquorice",
    32: "Helichrysum arenarium everlasting flower",
    35: "Sambucus nigra elderflower",
    36: "Lavandula stoechas french lavender",
}


def needs_local(plant: dict) -> bool:
    return not str(plant.get("resimUrl", "")).startswith("assets/plants/photos/")


def search_openverse(query: str) -> str | None:
    params = urllib.parse.urlencode({"q": query, "page_size": 5, "license_type": "commercial"})
    url = f"https://api.openverse.org/v1/images/?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    results = payload.get("results") or []
    for item in results:
        source = item.get("url") or item.get("thumbnail")
        if source and source.startswith("http"):
            return source
    return None


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as response:
        dest.write_bytes(response.read())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))

    for plant in plants:
        if not needs_local(plant):
            continue

        plant_id = plant["id"]
        query = QUERIES.get(plant_id, plant["botanikAd"])
        try:
            image_url = search_openverse(query)
            if not image_url:
                print(f"NORESULT {plant_id} {plant['ad']}")
                continue

            dest = OUT / f"{plant_id:02d}-openverse.jpg"
            download(image_url, dest)
            if dest.stat().st_size < 2000:
                dest.unlink(missing_ok=True)
                print(f"TOO_SMALL {plant_id} {plant['ad']}")
                continue

            plant["resimUrl"] = f"assets/plants/photos/{dest.name}"
            print(f"OK {plant_id} {plant['ad']} ({dest.stat().st_size})")
        except Exception as exc:
            print(f"FAIL {plant_id} {plant['ad']}: {exc}")

        time.sleep(1.2)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    local = sum(1 for plant in plants if plant["resimUrl"].startswith("assets/plants/photos/"))
    remote = sum(1 for plant in plants if plant["resimUrl"].startswith("https://"))
    print(f"Sonuc: local={local} remote={remote} total={len(plants)}")


if __name__ == "__main__":
    main()
