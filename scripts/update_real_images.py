# -*- coding: utf-8 -*-
"""Bitki gorsellerini Wikimedia Commons gercek fotograflariyla gunceller."""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "plants.json"

# Wikimedia Commons - turune ozel, serbest lisansli gercek fotograflar
IMAGE_MAP = {
    1: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Matricaria_recutita_002.JPG/960px-Matricaria_recutita_002.JPG",
    2: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Lavandula_angustifolia_001.JPG/960px-Lavandula_angustifolia_001.JPG",
    3: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Aloe_Vera.jpg/960px-Aloe_Vera.jpg",
    4: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Mentha_spicata1.jpg/960px-Mentha_spicata1.jpg",
    5: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rosmarinus_officinalis1.jpg/960px-Rosmarinus_officinalis1.jpg",
    6: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Rosa_red_flower.jpg/960px-Rosa_red_flower.jpg",
    7: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Salvia_officinalis0.jpg/960px-Salvia_officinalis0.jpg",
    8: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Jasminum_officinale1.jpg/960px-Jasminum_officinale1.jpg",
    9: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Thymus_vulgaris_1.jpg/960px-Thymus_vulgaris_1.jpg",
    10: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Basil-Basilico-Ocimum_basilicum-albahaca.jpg/960px-Basil-Basilico-Ocimum_basilicum-albahaca.jpg",
    11: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Phalaenopsis_%28aka%29.jpg/960px-Phalaenopsis_%28aka%29.jpg",
    12: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Tilia_tomentosa_flowers.jpg/960px-Tilia_tomentosa_flowers.jpg",
    13: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Zingiber_officinale_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-030.jpg/960px-Zingiber_officinale_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-030.jpg",
    14: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Curcuma_longa_roots.jpg/960px-Curcuma_longa_roots.jpg",
    15: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/EchinaceaPurpurea.jpg/960px-EchinaceaPurpurea.jpg",
    16: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Foeniculum_vulgare1.jpg/960px-Foeniculum_vulgare1.jpg",
    17: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Melissa_officinalis_002.JPG/960px-Melissa_officinalis_002.JPG",
    18: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Urtica_dioica_004.JPG/960px-Urtica_dioica_004.JPG",
    19: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Achillea_millefolium_2009.jpg/960px-Achillea_millefolium_2009.jpg",
    20: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Althaea_officinalis_002.JPG/960px-Althaea_officinalis_002.JPG",
    21: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Pimpinella_anisum_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-108.jpg/960px-Pimpinella_anisum_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-108.jpg",
    22: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Nigella_sativa_001.JPG/960px-Nigella_sativa_001.JPG",
    23: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Rosa_canina_hips.jpg/960px-Rosa_canina_hips.jpg",
    24: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Calendula_officinalis01.jpg/960px-Calendula_officinalis01.jpg",
    25: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Hypericum_perforatum_002.JPG/960px-Hypericum_perforatum_002.JPG",
    26: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Trigonella_foenum-graecum_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-136.jpg/960px-Trigonella_foenum-graecum_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-136.jpg",
    27: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Cuminum_cyminum_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-198.jpg/960px-Cuminum_cyminum_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-198.jpg",
    28: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Coriandrum_sativum_003.JPG/960px-Coriandrum_sativum_003.JPG",
    29: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Laurus_nobilis_001.JPG/960px-Laurus_nobilis_001.JPG",
    30: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Glycyrrhiza_glabra_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-061.jpg/960px-Glycyrrhiza_glabra_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-061.jpg",
    31: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Saffron_%28Crocus_sativus%29.jpg/960px-Saffron_%28Crocus_sativus%29.jpg",
    32: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Helichrysum_arenarium_kz03.jpg/960px-Helichrysum_arenarium_kz03.jpg",
    33: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Origanum_majorana0.jpg/960px-Origanum_majorana0.jpg",
    34: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Garlic_-_Allium_sativum_-_white_background.jpg/960px-Garlic_-_Allium_sativum_-_white_background.jpg",
    35: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Sambucus_nigra_003.JPG/960px-Sambucus_nigra_003.JPG",
    36: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Lavandula_stoechas_1.jpg/960px-Lavandula_stoechas_1.jpg",
    37: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Inula_helenium_002.JPG/960px-Inula_helenium_002.JPG",
}


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))

    for plant in plants:
        plant_id = plant["id"]
        if plant_id not in IMAGE_MAP:
            raise SystemExit(f"Eksik gorsel eslemesi: id={plant_id}")
        plant["resimUrl"] = IMAGE_MAP[plant_id]

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(plants)} bitki gorseli Wikimedia Commons ile guncellendi.")


if __name__ == "__main__":
    main()
