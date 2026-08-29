"""Bitki fotoğraflarını web için küçültür (assets/plants/photos/)."""
from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PHOTOS = ROOT / "assets" / "plants" / "photos"
MAX_WIDTH = 1280
JPEG_QUALITY = 82
MIN_SAVE_BYTES = 8_000  # çok küçük dosyaları atla


def optimize_file(path: Path) -> tuple[bool, int, int]:
    before = path.stat().st_size
    if before < MIN_SAVE_BYTES:
        return False, before, before

    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        w, h = im.size
        if w > MAX_WIDTH:
            nh = max(1, round(h * MAX_WIDTH / w))
            im = im.resize((MAX_WIDTH, nh), Image.Resampling.LANCZOS)

        buf = BytesIO()
        im.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        data = buf.getvalue()

    if len(data) >= before * 0.97:
        return False, before, before

    path.write_bytes(data)
    return True, before, len(data)


def main() -> int:
    if not PHOTOS.is_dir():
        print("Klasör yok:", PHOTOS)
        return 1

    changed = 0
    saved = 0
    for path in sorted(PHOTOS.glob("*.jpg")):
        try:
            ok, before, after = optimize_file(path)
            if ok:
                changed += 1
                saved += before - after
                print(f"OK {path.name}: {before // 1024}KB -> {after // 1024}KB")
        except Exception as exc:
            print(f"HATA {path.name}: {exc}", file=sys.stderr)

    print(f"\nToplam: {changed} dosya küçültüldü, ~{saved // 1024}KB kazanç")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
