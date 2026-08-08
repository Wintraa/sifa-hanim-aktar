# -*- coding: utf-8 -*-
"""Düzeltmeler: id 59-62, 64 (Deve Dikeni, Enginar, Şahtere, Mahlep, Eğir)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))

    def get(pid: int) -> dict:
        return next(x for x in d if x["id"] == pid)

    # --- 59 Deve Dikeni / Silybum marianum ---
    p = get(59)
    # Boy + genişlik (PFAF: grows to 1.2 m by 1 m)
    overview = p.get("genelTavsiyeMetni") or ""
    old_height = "Yaklaşık 1.2 m boya ulaşır."
    new_height = "Yaklaşık 1.2 m boya ve 1 m genişliğe ulaşır."
    if old_height in overview:
        p["genelTavsiyeMetni"] = overview.replace(old_height, new_height, 1)
    elif "1 m genişliğe" not in overview and "1.2 m" in overview:
        p["genelTavsiyeMetni"] = overview.replace(
            "Yaklaşık 1.2 m boya ulaşır",
            "Yaklaşık 1.2 m boya ve 1 m genişliğe ulaşır",
            1,
        )
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: tohum (başlıca tıbbi organ; silimarin/silibin içeren "
        "tohum ekstraktları ticari preparatların temelidir), çiçek, yaprak, yağ, kök, gövde. "
        "Kullanım biçimi: tohum ekstraktı/tıbbi preparat; kahve yerine (kavrulmuş tohum); yağ."
    )

    # --- 60 Enginar Yaprağı / Cynara scolymus ---
    p = get(60)
    p["cografyaMevsim"]["hasatMevsimi"] = (
        "Küresel enginar başları (çiçek tomurcukları) geç ilkbahardan yaza kadar hasat edilir. "
        "Tıbbi/bahçe yaprakları çiçeklenmeden hemen önce en iyidir. "
        "Tohumlar Eylül - Ekim arasında olgunlaşır (ikincil kayıt)."
    )

    # --- 61 Şahtere Otu / Fumaria officinalis ---
    p = get(61)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: çiçekli ot (taze veya kurutulmuş topraküstü bitki / flowering herb). "
        "Kullanım biçimi: çiçekli sürgünler (spreyler) süt pıhtılaştırıcı olarak; "
        "tıbbi kullanımda taze veya kuru ot. Bitki çiçeklenme başlarken hasat edilir."
    )
    hasat = p.get("cografyaMevsim", {}).get("hasatMevsimi") or ""
    note = "Çiçekli ot, çiçeklenme başladığında hasat edilir."
    if note not in hasat:
        p["cografyaMevsim"]["hasatMevsimi"] = (
            (hasat.rstrip(". ") + ". " if hasat.strip() else "") + note
        ).strip()

    # --- 62 Mahlep / Prunus mahaleb ---
    p = get(62)
    p["cografyaMevsim"]["hasatMevsimi"] = (
        "Çiçeklenme: Nisan - Mayıs. Baharat olarak kullanılan meyve/çekirdek (mahlep) "
        "geç yaz - sonbaharda hasat edilir."
    )

    # --- 64 Eğir Kökü / Acorus calamus ---
    p = get(64)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: rizom/kök (başlıca tıbbi ve çeşni organı), yaprak, gövde; "
        "ayrıca genç, yumuşak çiçek durumu (inflorescence) yenilebilir kısım olarak kaydedilir. "
        "Kullanım biçimi: rizom baharat/çeşni ve tıbbi preparat; genç çiçek durumu gıda kaydı."
    )

    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK fixed 59, 60, 61, 62, 64")


if __name__ == "__main__":
    main()
