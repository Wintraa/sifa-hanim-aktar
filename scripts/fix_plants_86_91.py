# -*- coding: utf-8 -*-
"""Düzeltmeler: id 86-91 (Nane, Biberiye, Kekik/Oregano, Hodan, Ashwagandha, Altın Kök)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))

    def get(pid: int) -> dict:
        return next(x for x in d if x["id"] == pid)

    # --- 86 Nane / Eau de Cologne mint ---
    p = get(86)
    p["ad"] = "Nane"
    p["botanikAd"] = "Mentha × piperita"
    p["temelBilgiler"] = {
        "turkceAdi": "Nane (Eau de Cologne / Bergamot nanesi)",
        "botanikAdi": "Mentha × piperita (Eau de Cologne mint / bergamot mint varyetesi)",
        "bitkiTuru": "yıllarca yaşayan (Lamiaceae)",
    }
    p["genelTavsiyeMetni"] = (
        "Nane — Eau de Cologne / bergamot nanesi (Mentha × piperita varyetesi), Lamiaceae "
        "familyasından yıllarca yaşayan bir bitkidir. Bu kayıt PFAF’taki Eau de Cologne mint "
        "detaylarına dayanır; aroması tipik nane (M. × piperita vulgaris) hattından daha "
        "keskin/parfümsüdür. Yaklaşık 0,5–0,6 m boya ulaşabilir."
    )
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak ve çiçekli bitki. Kullanım biçimi: taze/kuru yaprak çayı; "
        "baharat; uçucu yağ aromaterapi ve seyreltilmiş harici preparatlarda."
    )
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Uçucu yağ verimi için tam güneş en iyisidir; yarı gölgeyi de tolere eder."
    )

    # --- 87 Biberiye ---
    p = get(87)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: çiçek, yaprak, sürgün, gövde ve özellikle çiçekli sürgün uçları "
        "(flowering tops; uçucu yağ için üstün kabul edilir). Kullanım biçimi: baharat/çeşni, "
        "çay; çiçekli uçlardan damıtılan uçucu yağ haricen."
    )
    p["bakimYetistirme"]["sulamaSikligi"] = (
        "Yerleştikten sonra kuraklığa dayanabilir. Kışın aşırı nemden hoşlanmaz; "
        "çok iyi drenaj ister. Yazın kuru–orta nemli toprak uygundur."
    )
    p["bakimYetistirme"]["toprakTipi"] = (
        "Orta (tınlı), hafif (kumlu) topraklar; taşlı/kireçli ve çok iyi drene topraklar "
        "tercih edilir; pH: bazik (hafif alkali), hafif asidik, nötr. "
        "Kışın ıslak toprakta zarar görür."
    )
    p["bakimYetistirme"]["isikIhtiyaci"] = "Gölgede yetişemez; tam güneş ister."

    # --- 88 Kekik / Oregano ---
    p = get(88)
    p["temelBilgiler"]["turkceAdi"] = "Kekik (Oregano)"
    p["genelTavsiyeMetni"] = p["genelTavsiyeMetni"].replace(
        "Kekik (Origanum vulgare)",
        "Kekik / Oregano (Origanum vulgare)",
        1,
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "Hamile kadınlar tıbbi dozlarda kullanmamalıdır (küçük mutfak miktarları güvenli "
        "kabul edilir). Yüksek dozlarda güçlü sedatif (yatıştırıcı) etki gösterebilir. "
        "Tıbbi kullanımda uzman görüşü alınmalıdır."
    )
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Tam güneş tercih eder; yarı gölgeyi de tolere eder."
    )

    # --- 89 Hodan ---
    p = get(89)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak, çiçek, tohum yağı. Kullanım biçimi: taze yaprak ve "
        "çiçekler salata, çorba ve haşlama sebze (pot-herb) olarak; yapraklar içeceklere "
        "aroma için; çiçeklerden sirke vb. için renklendirici; tohum yağı; çay."
    )
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Tam güneş tercih eder; yarı gölgeyi de tolere eder."
    )

    # --- 90 Aşgabat Otu / Ashwagandha ---
    p = get(90)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: kök (başlıca tıbbi / adaptojenik organ), yaprak, meyve, tohum. "
        "Kullanım biçimi: kök tozu veya preparatları geleneksel tıbbi kullanımın merkezindedir; "
        "yaprak, meyve ve tohum da tıbbi kayıtlarda yer alır. Tohumların ikincil gıda kullanımı: "
        "bitkisel sütleri pıhtılaştırarak vejetaryen peynir yapımı (süt pıhtılaştırıcı)."
    )
    p["bakimYetistirme"]["sulamaSikligi"] = (
        "Kuru–taşlık, iyi drene toprakları tercih eder; sürekli nemli topraktan hoşlanmaz. "
        "Ilıman iklimde genellikle tek yıllık gibi yetiştirilir."
    )
    p["bakimYetistirme"]["toprakTipi"] = (
        "Kuru, taşlık, iyi drene topraklar; orta (tınlı)–hafif (kumlu); "
        "pH: bazik (hafif alkali), hafif asidik, nötr."
    )

    # --- 91 Altın Kök ---
    p = get(91)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak, kök, sürgün, gövde, çiçek. Kullanım biçimi: taze yaprak "
        "ve sürgünler salatada veya ıspanak gibi haşlanarak; turşu/lahana turşusu (sauerkraut); "
        "gövdeler kuşkonmaz gibi pişirilerek; kök adaptojen tıbbi preparatlarda; çiçek "
        "kaynatması geleneksel mide rahatsızlıklarında."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "PFAF Known hazards alanında özel bir toksisite listelenmemiştir; ancak bitki hormonal "
        "stres yanıtını düzenler ve beyin serotonin düzeylerini artırıcı etki gösterebilir "
        "(çalışmalarda %30’a varan artış bildirilmiştir). Tıbbi dozaj ve uzun süreli kullanımda "
        "uzman görüşü alınmalıdır; antidepresan veya hormonal tedavi kullananlar hekime danışmalıdır."
    )

    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK fixed 86-91")


if __name__ == "__main__":
    main()
