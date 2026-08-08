# -*- coding: utf-8 -*-
"""Wikipedia ozet API'sinden bitkiye ozel gercek gorsel URL'lerini alir."""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "plants.json"
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "plants" / "photos"

# Botanik ad -> Wikipedia sayfa basligi (Ingilizce)
WIKI_TITLES = {
    1: "Matricaria_chamomilla",
    2: "Lavandula_angustifolia",
    3: "Aloe_vera",
    4: "Mentha_spicata",
    5: "Salvia_rosmarinus",
    6: "Rose",
    7: "Salvia_officinalis",
    8: "Jasminum_officinale",
    9: "Thymus_vulgaris",
    10: "Ocimum_basilicum",
    11: "Phalaenopsis",
    12: "Tilia_tomentosa",
    13: "Ginger",
    14: "Turmeric",
    15: "Echinacea_purpurea",
    16: "Fennel",
    17: "Melissa_officinalis",
    18: "Urtica_dioica",
    19: "Achillea_millefolium",
    20: "Althaea_officinalis",
    21: "Pimpinella_anisum",
    22: "Nigella_sativa",
    23: "Rosa_canina",
    24: "Calendula_officinalis",
    25: "Hypericum_perforatum",
    26: "Fenugreek",
    27: "Cumin",
    28: "Coriander",
    29: "Laurus_nobilis",
    30: "Liquorice",
    31: "Saffron",
    32: "Helichrysum_arenarium",
    33: "Origanum_majorana",
    34: "Garlic",
    35: "Sambucus_nigra",
    36: "Lavandula_stoechas",
    37: "Inula_helenium",
    # 38–105: yeni eklenen bitkiler
    38: "Ocimum_basilicum",
    39: "Artemisia_dracunculus",
    40: "Parsley",
    41: "Dill",
    42: "Cardamom",
    43: "Vanilla",
    44: "Cananga_odorata",
    45: "Patchouli",
    46: "Bergamot_orange",
    47: "Tulip",
    48: "Hydrangea_macrophylla",
    49: "Begonia",
    50: "Rhododendron_simsii",
    51: "Viola_odorata",
    52: "Chrysanthemum",
    53: "Pelargonium",
    54: "Paeonia_lactiflora",
    55: "Narcissus_(plant)",
    56: "Hyacinth",
    57: "Lilium_candidum",
    58: "Impatiens_walleriana",
    59: "Dracaena_trifasciata",
    60: "Monstera_deliciosa",
    61: "Spathiphyllum",
    62: "Nephrolepis_exaltata",
    63: "Poinsettia",
    64: "Ficus_elastica",
    65: "Yucca",
    66: "Kalanchoe_blossfeldiana",
    67: "Bougainvillea",
    68: "Acacia_dealbata",
    69: "Ginseng",
    70: "Ginkgo_biloba",
    71: "Taraxacum_officinale",
    72: "Capsella_bursa-pastoris",
    73: "Viscum_album",
    74: "Senna_alexandrina",
    75: "Valerian_(herb)",
    76: "Passiflora_incarnata",
    77: "Silybum_marianum",
    78: "Artichoke",
    79: "Momordica_charantia",
    80: "Fumaria_officinalis",
    81: "Alpinia_officinarum",
    82: "Prunus_mahaleb",
    83: "Peganum_harmala",
    84: "Acorus_calamus",
    85: "Plantago_major",
    86: "Arctostaphylos_uva-ursi",
    87: "Vitex_agnus-castus",
    88: "Alchemilla",
    89: "Elymus_repens",
    90: "Aesculus_hippocastanum",
    91: "Astragalus_membranaceus",
    92: "Solidago_virgaurea",
    93: "Viburnum_opulus",
    94: "Jujube",
    95: "Crataegus_monogyna",
    96: "Camellia_sinensis",
    97: "Lycium_barbarum",
    98: "Tribulus_terrestris",
    99: "Artemisia_absinthium",
    100: "Mentha_pulegium",
    101: "Cnicus_benedictus",
    102: "Tussilago_farfara",
    103: "Myrtus_communis",
    104: "Salix_alba",
    105: "Gentiana_lutea",
}

UA = "DogalBitkilerRehberi/1.0 (educational local project; contact: local-dev)"


def fetch_summary(title: str) -> dict:
    encoded = urllib.parse.quote(title)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as response:
        dest.write_bytes(response.read())


def pick_image(summary: dict) -> str | None:
    for key in ("originalimage", "thumbnail"):
        node = summary.get(key) or {}
        source = node.get("source")
        if source:
            return source
    return None


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    failures = []

    for plant in plants:
        plant_id = plant["id"]
        title = WIKI_TITLES.get(plant_id)
        if not title:
            failures.append((plant_id, plant["ad"], "title yok"))
            continue

        try:
            summary = fetch_summary(title)
            image_url = pick_image(summary)
            if not image_url:
                failures.append((plant_id, plant["ad"], "gorsel yok"))
                time.sleep(0.8)
                continue

            ext = ".jpg"
            lower = image_url.lower()
            if ".png" in lower:
                ext = ".png"
            elif ".webp" in lower:
                ext = ".webp"
            elif ".jpeg" in lower:
                ext = ".jpeg"

            filename = f"{plant_id:02d}-{title.lower().replace('_', '-')}{ext}"
            dest = OUT_DIR / filename
            download(image_url, dest)
            plant["resimUrl"] = f"assets/plants/photos/{filename}"
            print(f"OK {plant_id} {plant['ad']} <- {title}")
        except Exception as exc:
            failures.append((plant_id, plant["ad"], str(exc)))
            print(f"FAIL {plant_id} {plant['ad']}: {exc}")

        time.sleep(0.9)

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTamamlandi. Basarisiz: {len(failures)}")
    for item in failures:
        print(" -", item)


if __name__ == "__main__":
    main()
