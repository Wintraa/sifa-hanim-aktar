# -*- coding: utf-8 -*-
"""Her bitki icin ozel SVG uretir ve plants.json resimUrl alanlarini gunceller."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
OUT = ROOT / "assets" / "plants"

PALETTES = [
    ("#F5EFE6", "#8D7B68", "#C8B6A6", "#A8A196"),
    ("#F3EDE4", "#6B8F71", "#A084E8", "#C8B6A6"),
    ("#F7F1E8", "#8D7B68", "#D4A373", "#A8A196"),
    ("#F2EBE3", "#7A6A5A", "#A084E8", "#9AAE8E"),
    ("#F6F0E7", "#5C7A63", "#C8B6A6", "#8D7B68"),
    ("#F4EEE5", "#8D6A5A", "#B8A4D8", "#A8A196"),
    ("#F8F2E9", "#6E7B63", "#C8B6A6", "#A084E8"),
    ("#F1EAE1", "#7B6B58", "#9CB89A", "#C8B6A6"),
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
        }
    )
    value = name.translate(table).lower()
    value = re.sub(r"[^a-z0-9\-]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "bitki"


def motif(plant_id: int, accent: str, leaf: str, petal: str) -> str:
    kind = plant_id % 5
    if kind == 0:
        # Papatya / cicek
        return f"""
  <path d="M600 640 C600 640 595 430 600 330" stroke="{accent}" stroke-width="16" stroke-linecap="round"/>
  <path d="M600 420 C520 360 430 390 390 470 C470 500 550 490 600 420Z" fill="{leaf}"/>
  <path d="M600 460 C690 390 810 420 850 510 C760 530 660 520 600 460Z" fill="{leaf}"/>
  <circle cx="600" cy="300" r="58" fill="{petal}"/>
  <circle cx="545" cy="255" r="42" fill="#fffaf4"/>
  <circle cx="655" cy="255" r="42" fill="#fffaf4"/>
  <circle cx="545" cy="345" r="42" fill="#fffaf4"/>
  <circle cx="655" cy="345" r="42" fill="#fffaf4"/>
  <circle cx="600" cy="220" r="42" fill="#fffaf4"/>
  <circle cx="600" cy="380" r="42" fill="#fffaf4"/>
  <circle cx="600" cy="300" r="28" fill="{accent}"/>
"""
    if kind == 1:
        # Lavanta / basak
        return f"""
  <path d="M600 700 V280" stroke="{accent}" stroke-width="14" stroke-linecap="round"/>
  <ellipse cx="560" cy="340" rx="28" ry="42" fill="{petal}"/>
  <ellipse cx="640" cy="340" rx="28" ry="42" fill="{petal}"/>
  <ellipse cx="560" cy="420" rx="28" ry="42" fill="{petal}"/>
  <ellipse cx="640" cy="420" rx="28" ry="42" fill="{petal}"/>
  <ellipse cx="560" cy="500" rx="28" ry="42" fill="{petal}"/>
  <ellipse cx="640" cy="500" rx="28" ry="42" fill="{petal}"/>
  <ellipse cx="600" cy="280" rx="34" ry="48" fill="{accent}"/>
  <path d="M600 520 C520 560 470 620 450 680" stroke="{leaf}" stroke-width="18" fill="none" stroke-linecap="round"/>
  <path d="M600 560 C680 590 740 640 760 690" stroke="{leaf}" stroke-width="18" fill="none" stroke-linecap="round"/>
"""
    if kind == 2:
        # Sukulent / aloe
        return f"""
  <path d="M600 680 C560 520 520 360 500 250" stroke="{leaf}" stroke-width="34" stroke-linecap="round" fill="none"/>
  <path d="M600 680 C640 520 680 360 700 250" stroke="{accent}" stroke-width="34" stroke-linecap="round" fill="none"/>
  <path d="M600 680 C580 540 540 420 480 340" stroke="{petal}" stroke-width="28" stroke-linecap="round" fill="none"/>
  <path d="M600 680 C620 540 660 420 720 340" stroke="{leaf}" stroke-width="28" stroke-linecap="round" fill="none"/>
  <path d="M600 680 C600 560 600 460 600 360" stroke="{accent}" stroke-width="30" stroke-linecap="round" fill="none"/>
"""
    if kind == 3:
        # Yaprak / nane
        return f"""
  <path d="M600 690 V300" stroke="{accent}" stroke-width="14" stroke-linecap="round"/>
  <path d="M600 380 C480 300 390 360 360 470 C470 510 560 480 600 380Z" fill="{leaf}"/>
  <path d="M600 450 C720 360 820 410 850 520 C740 560 640 530 600 450Z" fill="{petal}"/>
  <path d="M600 540 C500 500 410 560 390 650 C500 670 570 620 600 540Z" fill="{leaf}"/>
  <path d="M600 590 C690 550 790 600 810 680 C710 700 640 660 600 590Z" fill="{accent}"/>
"""
    # Agac / meyve
    return f"""
  <path d="M600 720 V430" stroke="{accent}" stroke-width="28" stroke-linecap="round"/>
  <circle cx="600" cy="340" r="140" fill="{leaf}"/>
  <circle cx="500" cy="390" r="100" fill="{petal}"/>
  <circle cx="700" cy="390" r="100" fill="{petal}"/>
  <circle cx="560" cy="300" r="28" fill="{accent}"/>
  <circle cx="640" cy="320" r="24" fill="{accent}"/>
  <circle cx="600" cy="380" r="26" fill="{accent}"/>
"""


def make_svg(name: str, plant_id: int) -> str:
    bg, accent, petal, leaf = PALETTES[plant_id % len(PALETTES)]
    safe_name = name.replace("&", "&amp;")
    return f"""<svg width="1200" height="900" viewBox="0 0 1200 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="900" rx="48" fill="{bg}"/>
  <rect x="52" y="52" width="1096" height="796" rx="36" fill="#FDFBF7" stroke="{petal}" stroke-width="6"/>
  <circle cx="220" cy="180" r="70" fill="{petal}" opacity="0.35"/>
  <circle cx="980" cy="220" r="110" fill="{leaf}" opacity="0.28"/>
  {motif(plant_id, accent, leaf, petal)}
  <text x="600" y="790" text-anchor="middle" fill="#4A3E3D" font-family="Arial, sans-serif" font-size="48" font-weight="700">{safe_name}</text>
</svg>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plants = json.loads(DATA.read_text(encoding="utf-8"))

    for plant in plants:
        slug = slugify(plant["ad"])
        filename = f"{plant['id']:02d}-{slug}.svg"
        path = OUT / filename
        path.write_text(make_svg(plant["ad"], plant["id"]), encoding="utf-8")
        plant["resimUrl"] = f"assets/plants/{filename}"

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(plants)} ozel SVG olusturuldu.")


if __name__ == "__main__":
    main()
