"""
Her ürün fotoğrafını 4:3 kadraja oturtur.
Ürünün başı (üst) ve sonu (alt) kesilmez — her zaman contain.
Önce boş beyaz kenarları kırpar, sonra kadraja ortalar.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
AKTAR = REPO.parent / "Aktar"
PRODUCTS_JSON = REPO / "data" / "products.json"
OUT_DIR = REPO / "assets" / "products"

TARGET_W, TARGET_H = 1200, 900  # 4:3
PAD = 0.06  # %6 iç boşluk — baş/son kenara yapışmasın
WHITE_THRESH = 246

# id → Aktar dosya adı (import-aktar-images.mjs ile aynı)
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


def is_near_white(px: tuple[int, int, int], thresh: int = WHITE_THRESH) -> bool:
    r, g, b = px[:3]
    return r >= thresh and g >= thresh and b >= thresh


def trim_whitespace(im: Image.Image) -> Image.Image:
    """Boş beyaz kenarları kırp — ürün kadrajda daha büyük dursun."""
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
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

    if not found:
        return rgb

    # Kenar payı: ürün başı/sonu kesilmesin
    margin = max(4, int(min(w, h) * 0.012))
    min_x = max(0, min_x - margin)
    min_y = max(0, min_y - margin)
    max_x = min(w - 1, max_x + margin)
    max_y = min(h - 1, max_y + margin)

    # Çok agresif kırpma olmasın (görselin %40'ından fazlasını atma)
    cropped_w = max_x - min_x + 1
    cropped_h = max_y - min_y + 1
    if cropped_w < w * 0.35 or cropped_h < h * 0.35:
        return rgb

    return rgb.crop((min_x, min_y, max_x + 1, max_y + 1))


def sample_bg(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    pts = [
        im.getpixel((2, 2)),
        im.getpixel((w - 3, 2)),
        im.getpixel((2, h - 3)),
        im.getpixel((w - 3, h - 3)),
    ]
    r = sum(p[0] for p in pts) // 4
    g = sum(p[1] for p in pts) // 4
    b = sum(p[2] for p in pts) // 4
    return (r, g, b)


def fit_contain(im: Image.Image) -> Image.Image:
    """Ürünün tamamı (baş→son) 4:3 kadraja sığar — asla kırpılmaz."""
    src = trim_whitespace(im.convert("RGB"))
    bg = sample_bg(src)
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), bg)

    avail_w = TARGET_W * (1 - 2 * PAD)
    avail_h = TARGET_H * (1 - 2 * PAD)
    scale = min(avail_w / src.width, avail_h / src.height)
    new_w = max(1, int(src.width * scale))
    new_h = max(1, int(src.height * scale))
    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)

    dx = (TARGET_W - new_w) // 2
    dy = (TARGET_H - new_h) // 2
    canvas.paste(resized, (dx, dy))
    return canvas


def main() -> None:
    if not AKTAR.exists():
        raise SystemExit(f"Aktar klasörü yok: {AKTAR}")

    aktar_files = [f.name for f in AKTAR.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    products = json.loads(PRODUCTS_JSON.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ok = 0
    notes: list[str] = []

    for product in products:
        pid = int(product["id"])
        dest_name = Path(str(product.get("resimUrl", "")).split("?")[0]).name
        if not dest_name or not dest_name.endswith((".jpg", ".jpeg", ".png", ".webp")):
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
                else:
                    notes.append(f"#{pid} Aktar dosyası boş: {resolved}")
            else:
                notes.append(f"#{pid} Aktar eşleşmedi: {wanted}")

        if source is None and dest.exists() and dest.stat().st_size > 1000:
            source = dest
            notes.append(f"#{pid} mevcut dosya kullanıldı")

        if source is None:
            notes.append(f"#{pid} ATLANDI — kaynak yok")
            continue

        with Image.open(source) as im:
            fitted = fit_contain(im)
            # Geçici dosyaya yaz, sonra taşı (kilit sorunları)
            tmp = dest.with_suffix(".tmp.jpg")
            fitted.save(tmp, "JPEG", quality=90, optimize=True)
            tmp.replace(dest)

        # Cache bust
        product["resimUrl"] = f"assets/products/{dest.name}?v=fit43"
        ok += 1
        print(f"OK #{pid:02d} {dest.name}  ({source.name} -> 1200x900 contain)")

    PRODUCTS_JSON.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n{ok}/86 hazır")
    for n in notes:
        print("·", n)


if __name__ == "__main__":
    main()
