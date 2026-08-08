# -*- coding: utf-8 -*-
"""Düzeltmeler: id 95 Veba Otu, 96 Göz Otu (Orobanchaceae),
98 Cadı Fındığı (kabuk/yaprak), 105 Kedi Nanesi (yan etki metni)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))

    def get(pid: int) -> dict:
        return next(x for x in d if x["id"] == pid)

    # --- 105 Kedi Nanesi / Nepeta cataria ---
    # yanEtkiler metninde yanlışlıkla "Kediotu" (Valeriana) geçmiş; Catnip ile karışmasın.
    p = get(105)
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "Kedi nanesinin idrar söktürücü özellikleri vardır ve idrar miktarını ve sıklığını "
        "artırabilir. Kedi nanesinin tütün gibi içilmesi öfori ve görsel halüsinasyonlar "
        "üretebilir. Sedasyon. Pelviste inflamatuar hastalığı olan veya hamile olan kadınlar "
        "kullanmamalıdır. Araç veya makine kullanırken dikkat edilmelidir. "
        "(Not: Valeriana officinalis / Kediotu ile karıştırılmamalıdır.)"
    )

    # --- 95 Veba Otu / Petasites hybridus (Butterbur) ---
    # Eski ad "Öksürük Kökü"; standart Türkçe ad Veba Otu. Tussilago farfara = Öksürük Otu.
    p = get(95)
    p["ad"] = "Veba Otu"
    p["temelBilgiler"]["turkceAdi"] = "Veba Otu"
    p["genelTavsiyeMetni"] = (
        "Veba Otu (Petasites hybridus; Butterbur; halk dilinde bazen Öksürük Kökü), "
        "Asteraceae familyasından yıllarca yaşayan bitkidir. Yaklaşık 1 m boya ulaşır. "
        "Doğal yayılış alanı: Avrupa (Britanya dahil), İskandinavya'dan güneye ve doğuya "
        "doğru İspanya, kuzey ve batı Asya. "
        "Not: Tussilago farfara genellikle Öksürük Otu olarak anılır; bu kayıt "
        "Petasites hybridus / Veba Otu’dur."
    )

    # --- 96 Göz Otu / Euphrasia officinalis ---
    # Modern APG: Orobanchaceae; PFAF hâlâ Scrophulariaceae gösterebilir.
    p = get(96)
    p["temelBilgiler"]["bitkiTuru"] = "bir mevsim yaşayan (Orobanchaceae)"
    p["genelTavsiyeMetni"] = (
        "Göz Otu (Euphrasia officinalis), Orobanchaceae familyasından bir mevsim yaşayan "
        "bitkidir (modern APG sınıflandırması; PFAF kaydı hâlâ eski Scrophulariaceae "
        "ailesinden gösterebilir). Yaklaşık 0.2 m boya ulaşır. Doğal yayılış alanı: "
        "Batı Avrupa (Britanya dahil), Doğu Asya."
    )

    # --- 98 Cadı Fındığı / Hamamelis virginiana ---
    # Tıbbi ana kısımlar kabuk + yaprak; tohum yenilebilirliği şüpheli/ikincil.
    p = get(98)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar (tıbbi): kabuk ve yaprak. Kullanım biçimi: kabuk/yaprak "
        "çayları, tentür ve harici özütler; damıtık cadı fındığı suyu (witch hazel water) "
        "ticari preparatlarda yaygındır. Tohum: PFAF’ta yenilebilir diye geçer ancak "
        "kaynaklar şüpheli kabul edilir; tıbbi kullanımın ana organları kabuk ve yapraktır, "
        "tohum yalnızca ikincil/şüpheli yenilebilirlik notudur."
    )

    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK fixed ids 95, 96, 98, 105")


if __name__ == "__main__":
    main()
