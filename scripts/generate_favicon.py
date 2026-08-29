"""Şifa Hanım logosundan favicon ve marka görselleri üretir."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "brand" / "sifa-hanim-logo-source.png"
PUBLIC = ROOT / "client" / "public"
BRAND_OUT = ROOT / "assets" / "brand"
MAX_LOGO_PX = 512


def main() -> None:
    BRAND_OUT.mkdir(parents=True, exist_ok=True)
    img = Image.open(SRC).convert("RGBA")

    size = max(img.size)
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    ox = (size - img.width) // 2
    oy = (size - img.height) // 2
    canvas.paste(img, (ox, oy), img)
    square = canvas.convert("RGB")
    if max(square.size) > MAX_LOGO_PX:
        square.thumbnail((MAX_LOGO_PX, MAX_LOGO_PX), Image.Resampling.LANCZOS)

    square.save(BRAND_OUT / "sifa-hanim-logo.png", optimize=True, compress_level=9)

    for px, name in [
        (512, "icon-512.png"),
        (192, "apple-touch-icon.png"),
        (48, "favicon-48x48.png"),
    ]:
        square.resize((px, px), Image.Resampling.LANCZOS).save(PUBLIC / name, optimize=True)

    square.resize((48, 48), Image.Resampling.LANCZOS).save(
        PUBLIC / "favicon.ico", format="ICO", sizes=[(48, 48)]
    )

    print("favicon hazir:", PUBLIC / "favicon.ico")


if __name__ == "__main__":
    main()
