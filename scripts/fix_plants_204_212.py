# -*- coding: utf-8 -*-
"""Düzeltmeler: id 204 (Udi Hindi) ve 212 (Nioli) — güvenlik uyarıları."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))

    def get(pid: int) -> dict:
        return next(x for x in d if x["id"] == pid)

    # --- 204 Udi Hindi / Saussurea costus ---
    p = get(204)
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "CITES Ek I (Appendix I) kapsamında nesli tehlike altındaki bir türdür; "
        "uluslararası ticareti sıkı şekilde kısıtlanmış/denetlenmiştir — yasal ve "
        "sertifikalı kaynak dışında alım-satım yapılmamalıdır. Bitkisel ticaret "
        "ürünlerinde Aristolochic asit içeren toksik bitkilerle (ör. Aristolochia "
        "türleri) tağşiş/kontaminasyon riski yüksektir; bu bileşikler böbrek "
        "toksisitesi (aristolochic asit nefropatisi) ve kanser riskiyle "
        "ilişkilendirilir (FDA tarzı güvenlik uyarısı). İç kullanım ve yüksek doz "
        "önerilmez; tıbbi kullanımda mutlaka uzman görüşü alınmalıdır."
    )

    # --- 212 Nioli / Melaleuca quinquenervia ---
    p = get(212)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Yaprak ve uç sürgünlerden buhar damıtımıyla elde edilen nioli (niaouli / "
        "gomenol) uçucu yağı; yalnızca iyi seyreltilmiş harici uygulama veya "
        "aromaterapi/inhalasyon için uygundur. Bebek ve küçük çocukların yüz/burun "
        "bölgesine uygulanmamalıdır. İç kullanım önerilmez."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "Gomenol / nioli (niaouli) uçucu yağı yutulmamalıdır; iç kullanım "
        "risklidir ve önerilmez. Seyreltilmeden cilde uygulanmamalıdır. Özellikle "
        "bebek ve küçük çocuklarda yüz/burun çevresine uygulama kontrendikedir: "
        "1,8-sineol içeren uçucu yağlarda larengospazm ve solunum durması riski "
        "bildirilmiştir. Çocuklarda, gebelikte ve hassas ciltlerde yalnızca "
        "uzman rehberliğinde, seyreltilmiş harici/aromaterapi kullanımı düşünülmelidir. "
        "1,8-sineol chemotipi baskındır; yüksek sineollü okaliptüs yağı ile "
        "karıştırma/tağşiş riski vardır. Florida’da çiçek salgıları hassas kişilerde "
        "solunum tahrişi bildirilmiştir. Bazı bölgelerde istilacı olabilir."
    )

    DATA.write_text(
        json.dumps(d, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Doğrulama özeti
    for pid in (204, 212):
        sk = get(pid)["saglikKullanim"]
        print(f"=== id {pid} {get(pid)['ad']} ===")
        print(f"kullanimSekli: {sk['kullanimSekli'][:120]}...")
        print(f"yanEtkilerUyarilar: {sk['yanEtkilerUyarilar'][:160]}...")
        print()


if __name__ == "__main__":
    main()
