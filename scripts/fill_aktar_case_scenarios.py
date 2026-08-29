# PubMed vakasi olmayan bitkilere aktar tezgahi senaryosu ekler.
# Kaynak: aktar-senaryo -- klinik uydurma degil; kullanim ozetinden turetilmis ornek.
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANTS = ROOT / "data" / "plants.json"


def first_sentence(text: str, max_len: int = 160) -> str:
    t = re.sub(r"\s+", " ", (text or "").strip())
    if not t:
        return ""
    for sep in (". ", "! ", "? "):
        if sep in t:
            t = t.split(sep, 1)[0] + "."
            break
    return t[:max_len].rstrip(".") + ("." if t else "")


def build_case(plant: dict) -> dict:
    ad = plant.get("ad") or "Bu bitki"
    fayda = first_sentence(plant.get("saglikKullanim", {}).get("faydalari", ""))
    kullanim = first_sentence(plant.get("saglikKullanim", {}).get("kullanimSekli", ""))
    uyari = first_sentence(plant.get("saglikKullanim", {}).get("yanEtkilerUyarilar", ""))

    sorun = fayda or f"{ad} ile ilgili gunluk bir sikayet icin danisildi."
    yaklasim = kullanim or f"Aktar yonlendirmesiyle {ad} uygun sekilde kullanildi."
    sonuc = (
        "Sikayet hafifledi; herkeste ayni sonuc cikmayabilir. "
        + (f"Uyari: {uyari}" if uyari else "Kullanmadan once hekime danisilmali.")
    )
    anlatim = (
        f"Tezgâhta sik sorulan bir ornek: {ad} icin basvuruldu. "
        f"{sorun} {yaklasim} "
        "Bu bir klinik calisma ozeti degildir; aktar kullanimina dayali ornek senaryodur."
    )

    return {
        "baslik": f"{ad} — tezgah ornegi",
        "sorun": sorun,
        "yaklasim": yaklasim,
        "sonuc": sonuc,
        "anlatim": anlatim,
        "kaynak": "aktar-senaryo",
    }


def has_case(plant: dict) -> bool:
    v = plant.get("ornekVaka") or {}
    return bool(v.get("anlatim") or v.get("sorun"))


def main() -> None:
    plants = json.loads(PLANTS.read_text(encoding="utf-8"))
    filled = 0
    for plant in plants:
        if has_case(plant):
            continue
        plant["ornekVaka"] = build_case(plant)
        filled += 1

    PLANTS.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"aktar senaryosu eklendi: {filled} / toplam {len(plants)}")


if __name__ == "__main__":
    main()
