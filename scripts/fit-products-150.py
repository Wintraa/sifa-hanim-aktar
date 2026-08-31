"""
Profesyonel urun thumbnail — Aktar orijinalinden.
- Acik/gri kenarlar kirpilir
- Sabit krem zemin (#FDFBF7)
- Urun basi ve tabani KESILMEZ (contain)
- Cikti: 400x400 (150px grid icin retina)
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parents[1]
AKTAR = REPO.parent / "Aktar"
PRODUCTS_JSON = REPO / "data" / "products.json"
OUT_DIR = REPO / "assets" / "products"

TARGET = 400
PAD = 0.035
BG = (253, 251, 247)  # --bg site kremi

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


def is_background(r: int, g: int, b: int) -> bool:
    """Beyaz, acik gri, krem kenarlar."""
    mx, mn = max(r, g, b), min(r, g, b)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    if lum >= 248:
        return True
    if lum >= 215 and (mx - mn) <= 22:
        return True
    return False


def trim_content(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    step = 1 if max(w, h) < 1200 else 2

    min_x, min_y = w, h
    max_x, max_y = 0, 0
    found = False

    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            if not is_background(r, g, b):
                found = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if not found:
        return rgb

    # Urun basi/sonu icin ince kenar payi
    margin = max(3, int(min(w, h) * 0.008))
    min_x = max(0, min_x - margin)
    min_y = max(0, min_y - margin)
    max_x = min(w - 1, max_x + margin)
    max_y = min(h - 1, max_y + margin)

    cw = max_x - min_x + 1
    ch = max_y - min_y + 1
    if cw < w * 0.25 or ch < h * 0.25:
        return rgb

    return rgb.crop((min_x, min_y, max_x + 1, max_y + 1))


def fit_thumb(im: Image.Image) -> Image.Image:
    src = trim_content(im)
    # Hafif keskinlestir
    src = ImageEnhance.Sharpness(src).enhance(1.08)
    src = ImageEnhance.Contrast(src).enhance(1.04)

    canvas = Image.new("RGB", (TARGET, TARGET), BG)
    avail = TARGET * (1 - 2 * PAD)
    scale = min(avail / src.width, avail / src.height)
    nw = max(1, int(src.width * scale))
    nh = max(1, int(src.height * scale))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)

    dx = (TARGET - nw) // 2
    dy = (TARGET - nh) // 2
    canvas.paste(resized, (dx, dy))
    return canvas


def main() -> None:
    if not AKTAR.exists():
        raise SystemExit(f"Aktar klasoru yok: {AKTAR}")

    aktar_files = [
        f.name
        for f in AKTAR.iterdir()
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} and f.stat().st_size > 500
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
                source = AKTAR / resolved

        if source is None and dest.exists() and dest.stat().st_size > 1000:
            source = dest
            print(f"WARN #{pid:02d} mevcut dosyadan")

        if source is None:
            print(f"SKIP #{pid:02d} kaynak yok")
            continue

        with Image.open(source) as im:
            out = fit_thumb(im)
            tmp = dest.with_suffix(".tmp.jpg")
            out.save(tmp, "JPEG", quality=92, optimize=True, progressive=True)
            tmp.replace(dest)

        product["resimUrl"] = f"assets/products/{dest.name}?v=pro-v2"
        ok += 1
        print(f"OK #{pid:02d} <- {source.name}")

    PRODUCTS_JSON.write_text(
        json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\n{ok}/86 hazir")


if __name__ == "__main__":
    main()
