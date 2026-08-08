# -*- coding: utf-8 -*-
"""Kalan bozuk / Ingilizce yetistigiYerler kayitlarini elle duzeltir.

Ilk otomatik ceviri turu bazi nadir kalıplari bozmustu; burada orijinal
Ingilizce Range metnine bakilarak dogru Turkce yazilir. Habitat (Doğal
ortamı) kismi korunur.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"

# id -> sadece Range kismi (Doğal ortamı: oncesi). Habitat aynen kalir.
RANGE_FIX: dict[int, str] = {
    38: "Güney Amerika (Bolivya, Kolombiya); Orta Amerika (Kosta Rika'dan Meksika'ya); birçok başka bölgede doğallaşmıştır.",
    40: "Bitkinin kökeni belirsizdir; Güneybatı Avrupa'da doğallaşmıştır.",
    44: "Melez bahçe kökenlidir.",
    49: "Güneybatı Asya. Avrupa'da Akdeniz havzası çevresinde doğallaşmıştır.",
    50: "Batı Tropik Afrika (Nijerya'dan Gabon'a), doğuya doğru Kongo'ya (eski Zaire) kadar.",
    54: "Kuzey yarımkürenin büyük bölümü (Britanya dahil).",
    55: "Neredeyse kozmopolit bir bitki; Britanya dahil dünyanın çoğu bölgesinde bulunur.",
    57: "Avrupa (Britanya dahil, aşırı kuzey ve güney hariç), ılıman Asya'dan Japonya'ya kadar.",
    60: "Yabani ortamda bilinmez; muhtemelen C. cardunculus'un bir formundan türemiştir.",
    75: "Avrupa (Britanya dahil; İzlanda'da yoktur), güney ve batı Akdeniz havzası ile Afganistan.",
    76: "Doğu Asya - Çin? Kesin kökeni belirsizdir.",
    79: "Orta ve Güney Avrupa (Britanya dahil), Akdeniz bölgesi, Makaronezya.",
    80: "Güney Avrupa'dan Batı Asya'ya. Britanya'da seyrek ve geçici olarak bulunur.",
    91: "Avrupa, Asya ve Kuzey Amerika'nın arktik bölgeleri (Britanya dahil); dağlarda daha güneye iner.",
    113: "Berberi kıyısı (Kuzey Afrika). Britanya'da doğallaşmış veya muhtemelen yerlidir.",
}

# Genel son temizlik (tum kayitlar)
GLOBAL_REPLACEMENTS: list[tuple[str, str]] = [
    (r"\bCentraland\b", "Orta ve"),
    (r"\bGabon\b", "Gabon"),
    (r"\bZaire\b", "Zaire"),
    (r"Birçok başka ar\.", "birçok başka bölge."),
    (r",\s*-\s*", ", "),
    (r"\s{2,}", " "),
    # "Norveç güney ve doğuya doğru" -> "Norveç'ten güneye ve doğuya doğru"
    (r"\bNorveç güney ve doğuya doğru\b", "Norveç'ten güneye ve doğuya doğru"),
    (r"\bİskandinavya güney ve doğuya doğru\b", "İskandinavya'dan güneye ve doğuya doğru"),
    (r"\bArctic\b", "Arktik"),
    (r"\bfurther\b", "daha"),
    (r"\bon mountains\b", "dağlarda"),
    (r"\bmountains\b", "dağlar"),
]


def apply_range(full: str, new_range: str) -> str:
    if "Doğal ortamı:" in full:
        habitat = full.split("Doğal ortamı:", 1)[1].strip()
        return f"{new_range} Doğal ortamı: {habitat}"
    return new_range


def polish(text: str) -> str:
    for pat, repl in GLOBAL_REPLACEMENTS:
        text = re.sub(pat, repl, text)
    return text.strip()


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    fixed = 0
    polished = 0

    for plant in plants:
        c = plant.get("cografyaMevsim")
        if not c:
            continue
        old = c.get("yetistigiYerler") or ""
        if not old:
            continue

        new = old
        if plant["id"] in RANGE_FIX:
            new = apply_range(old, RANGE_FIX[plant["id"]])
            fixed += 1

        polished_text = polish(new)
        if polished_text != old:
            c["yetistigiYerler"] = polished_text
            if polished_text != new:
                polished += 1
            elif plant["id"] not in RANGE_FIX:
                polished += 1

    DATA.write_text(
        json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"elle duzeltilen={fixed}  genel cilalama={polished}")


if __name__ == "__main__":
    main()
