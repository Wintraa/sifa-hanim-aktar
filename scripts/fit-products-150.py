"""
Ürün fotoğraflarını 150x150 (retina: 300x300) kare kadraja oturtur.
Ürünün başı ve tabanı kesilmez — contain + beyaz kenar kırpma.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
AKTAR = REPO.parent / "Aktar"
PRODUCTS_JSON = REPO / "data" / "products.json"
OUT_DIR = REPO / "assets" / "products"

# CSS 150px; 2x retina
TARGET = 300
PAD = 0.07
WHITE_THRESH = 246

EXACT = {
    1: "Esila Kuyruk.jpg",
    2: "adnız.jpg",
    4: "Radian Masaj.jpg",
    5: "çörek otu.jpg",
    9: "coconut.jpeg",
    10: "coconut.jpeg",
    11: "PulBiber.jpeg",
    12: "PulBiber.jpeg",
    13: "Toz Biber.jpeg",
    14: "Toz Biber.jpeg",
    15: "İsot.jpeg",
    16: "kimyon.jpeg",
    17: "Kekik.jpeg",
    18: "Toz Tarçın.jpeg",
    19: "Kara Biber.jpeg",
    20: "Sumak.jpeg",
    21: "Çubuk Tarçın.jpeg",
    22: "Zencefil.jpeg",
    23: "Zerdeçal.jpeg",
    24: "beyaz susam.jpeg",
    25: "Kavruk Susam.jpeg",
    26: "karanfil.jpeg",
    27: "çörek otu.jpg",
    28: "Keten Tohum.jpeg",
    29: "Rezene.jpeg",
    30: "Kına.jpeg",
    31: "Kış Çay.jpeg",
    32: "Atom Çay.jpeg",
    33: "Form Çay.jpeg",
    34: "Beyaz Çay.jpeg",
    35: "Yeşil Çay.jpeg",
    36: "yeşil Çay dökme.jpeg",
    37: "Seylan Çay.jpg",
    38: "Kayısılı Biberiyeli.jpeg",
    39: "Bromelain.jpeg",
    40: "KekreMekre.jpeg",
    41: "momoridca kokonat.jpg",
    42: "detox.jpeg",
    43: "Elmalı bişey sirke.jpeg",
    44: "Aserola.jpeg",
    45: "Matcha Detox.jpeg",
    46: "Matcha Bromelain.jpeg",
    47: "Matcha Yeşil Çay.jpeg",
    48: "Dorm Diyet Kahjvesi.jpeg",
    49: "Şifa HAnım Kahve.jpeg",
    50: "Adıyaman Kervan.jpeg",
    51: "Sütlü Menengiç.jpeg",
    52: "Dolma Biber.jpeg",
    53: "Patlıcan Kuru Askı.jpeg",
    54: "Domates kuru.jpeg",
    55: "incir kuru.jpeg",
    56: "Dut Kuru.jpeg",
    57: "Hayıt Tohumlu Macun.jpeg",
    58: "Ballı Polenli Ginsengli.jpeg",
    59: "andız Pekmezli.jpeg",
    60: "Yakı Otlu Prvoit.jpeg",
    61: "45+ Performans.jpeg",
    62: "Mandalina.jpeg",
    63: "Zühre Ana Kids.jpg",
    64: "Zühre Ana Kozalak.jpg",
    65: "Propolis.jpg",
    66: "Sultan Macun.jpg",
    67: "Stevia.jpg",
    68: "Tropikal.jpg",
    69: "Zühre Ana Yaban Mersini.jpeg",
    70: "vişne.jpg",
    71: "karadut.jpg",
    72: "adnız.jpg",
    73: "hurma.jpg",
    74: "harnup.jpg",
    75: "dut.jpg",
    76: "kızılcık.jpg",
    77: "elma.jpg",
    78: "Kozalak urubu.jpeg",
    79: "Alıç Sireksi.jpeg",
    80: "ananas.jpg",
    81: "enginar.jpg",
    82: "üzüm.jpg",
    83: "Gül Sirkesi.jpeg",
    84: "Sultan.jpeg",
    85: "Çakşır.jpg",
    86: "Enginat.jpg",
}


def norm(s: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFD", s.casefold())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    for ext in (".jpeg", ".jpg", ".png", ".webp"):
        if s.endswith(ext):
            s = s[: -len(ext)]
    return "".join(ch for ch in s if ch.isalnum() or ch in " +").strip()


def resolve_aktar(wanted: str, files: list[str]) -> str | None:
    if wanted in files:
        return wanted
    wl = wanted.casefold()
    for f in files:
        if f.casefold() == wl:
            return f
    wn = norm(wanted)
    for f in files:
        if norm(f) == wn:
            return f
    for f in files:
        if wn and wn in norm(f):
            return f
    return None


def is_near_white(px, thresh: int = WHITE_THRESH) -> bool:
    r, g, b = px[:3]
    return r >= thresh and g >= thresh and b >= thresh


def trim_whitespace(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    step = 2 if max(w, h) > 800 else 1

    min_x, min_y = w, h
    max_x, max_y = 0, 0
    found = False
    for y in range(0, h, step):
        for x in range(0, w, step):
            if not is_near_white(px[x, y]):
                found = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if not found:
        return rgb

    margin = max(4, int(min(w, h) * 0.015))
    min_x = max(0, min_x - margin)
    min_y = max(0, min_y - margin)
    max_x = min(w - 1, max_x + margin)
    max_y = min(h - 1, max_y + margin)

    cropped_w = max_x - min_x + 1
    cropped_h = max_y - min_y + 1
    if cropped_w < w * 0.3 or cropped_h < h * 0.3:
        return rgb

    return rgb.crop((min_x, min_y, max_x + 1, max_y + 1))


def sample_bg(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    pts = [
        im.getpixel((min(2, w - 1), min(2, h - 1))),
        im.getpixel((max(0, w - 3), min(2, h - 1))),
        im.getpixel((min(2, w - 1), max(0, h - 3))),
        im.getpixel((max(0, w - 3), max(0, h - 3))),
    ]
    return (
        sum(p[0] for p in pts) // 4,
        sum(p[1] for p in pts) // 4,
        sum(p[2] for p in pts) // 4,
    )


def fit_square(im: Image.Image) -> Image.Image:
    """Kare kadraj — ürün tamamen sığar (baş ve taban kesilmez)."""
    src = trim_whitespace(im.convert("RGB"))
    bg = sample_bg(src)
    canvas = Image.new("RGB", (TARGET, TARGET), bg)

    avail = TARGET * (1 - 2 * PAD)
    scale = min(avail / src.width, avail / src.height)
    new_w = max(1, int(src.width * scale))
    new_h = max(1, int(src.height * scale))
    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)

    dx = (TARGET - new_w) // 2
    dy = (TARGET - new_h) // 2
    canvas.paste(resized, (dx, dy))
    return canvas


def main() -> None:
    if not AKTAR.exists():
        raise SystemExit(f"Aktar klasoru yok: {AKTAR}")

    aktar_files = [
        f.name
        for f in AKTAR.iterdir()
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    products = json.loads(PRODUCTS_JSON.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ok = 0
    for product in products:
        pid = int(product["id"])
        dest_name = Path(str(product.get("resimUrl", "")).split("?")[0]).name
        if not dest_name.endswith((".jpg", ".jpeg", ".png", ".webp")):
            dest_name = f"{pid:02d}-product.jpg"
        dest = OUT_DIR / dest_name

        source: Path | None = None
        wanted = EXACT.get(pid)
        if wanted:
            resolved = resolve_aktar(wanted, aktar_files)
            if resolved:
                src_path = AKTAR / resolved
                if src_path.stat().st_size > 0:
                    source = src_path

        if source is None and dest.exists() and dest.stat().st_size > 1000:
            source = dest

        if source is None:
            print(f"SKIP #{pid:02d} kaynak yok")
            continue

        with Image.open(source) as im:
            fitted = fit_square(im)
            tmp = dest.with_suffix(".tmp.jpg")
            fitted.save(tmp, "JPEG", quality=88, optimize=True)
            tmp.replace(dest)

        product["resimUrl"] = f"assets/products/{dest.name}?v=sq150"
        ok += 1
        print(f"OK #{pid:02d} {dest.name}")

    PRODUCTS_JSON.write_text(
        json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\n{ok}/86 kare kadraj hazir")


if __name__ == "__main__":
    main()
