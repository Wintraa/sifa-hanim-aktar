# -*- coding: utf-8 -*-
"""Düzeltmeler: id 72, 73, 74, 75, 77, 78 (Altınbaşak–Pelin).

Her kayıt için plants.json + _pfafOrijinal okunarak PFAF ile tutarlı alanlar güncellenir.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))

    def get(pid: int) -> dict:
        return next(x for x in d if x["id"] == pid)

    # --- 72 Altınbaşak / Solidago virgaurea ---
    # PFAF: semi-shade (light woodland) or no shade; sun or semi-shade.
    p = get(72)
    assert "Solidago virgaurea" in (p.get("botanikAd") or "")
    p["temelBilgiler"] = {
        "turkceAdi": "Altınbaşak",
        "botanikAdi": "Solidago virgaurea",
        "bitkiTuru": "yıllarca yaşayan (Asteraceae)",
    }
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Tam güneşte veya yarı gölgede (açık orman altı) yetişir; her iki koşulu da tolere eder."
    )

    # --- 73 Gilaburu / Viburnum opulus ---
    # PFAF: bark = antispasmodic/astringent/sedative (ana tıbbi kısım);
    # leaves & fruits = antiscorbutic, emetic, laxative. Prefers moist or wet soil.
    p = get(73)
    assert "Viburnum opulus" in (p.get("botanikAd") or "")
    _ = p.get("_pfafOrijinal", {})
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: başlıca kabuk (antispasmodik / sakinleştirici tıbbi organ); "
        "yaprak ve meyve (daha çok laksatif ve kusturucu; C vitamini kaynağı olarak da anılır). "
        "Kullanım biçimi: sonbahar veya ilkbaharda hasat edilen kurutulmuş kabuktan çay/dekoksiyon "
        "(adet krampları, doğum sonrası spazmlar, astım/kolik tipi spazmlar); taze kabuktan "
        "homeopatik preparat. Yaprak ve meyve tıbbi kullanımda laksatif/emetik etkileri nedeniyle "
        "dikkatle değerlendirilmelidir; meyve gıda olarak pişirilerek (jöle vb.) kullanılır."
    )
    p["bakimYetistirme"]["sulamaSikligi"] = (
        "Nemli veya ıslak toprağı tercih eder; kuru konumlara uyumsuzdur. "
        "Derin, zengin, nem tutan tınlı topraklar uygundur."
    )

    # --- 74 Hünnap / Ziziphus jujuba ---
    # PFAF: fruit primary; seed hypnotic/sedative; root dyspepsia/febrifuge;
    # coffee substitute = fruit (roasted/ground); leaves famine food.
    p = get(74)
    assert "Ziziphus jujuba" in (p.get("botanikAd") or "")
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: meyve (başlıca), tohum (sedatif/hipnotik), kök "
        "(dispepsi; ateş düşürücü dekoksiyon; yara/ülser üzerine toz), yaprak "
        "(büzücü, ateş düşürücü). Kullanım biçimi: taze veya kurutulmuş meyve "
        "(çiğ/pişmiş; tonik ve sindirim destekleyici); meyve/kök dekoksiyonu; "
        "tohum preparatları (çarpıntı, uykusuzluk, sinir yorgunluğu). "
        "Kavrulup öğütülmüş meyve kahve yerine yalnızca ikincil bir kullanımdır; "
        "birincil gıda/tıbbi kullanım taze–kuru meyve ve dekoksiyonlardır."
    )

    # --- 75 Alıç / Crataegus monogyna ---
    # PFAF hazards: None known — yine de kardiyotonik/hipotansif klinik ihtiyat gerekli.
    # Roots said to stimulate arteries of the heart.
    p = get(75)
    assert "Crataegus" in (p.get("botanikAd") or "")
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: çiçek, meyve, yaprak, sürgün, kök "
        "(köklerin kalp arterlerini uyardığı söylenir). Kullanım biçimi: "
        "çiçek ve meyveden çay veya tentür (kalp toniği; uzun süreli kullanım gerekir); "
        "kavrulmuş tohum kahve yerine; kurutulmuş yapraktan çay."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "PFAF Known hazards alanında özel bir toksisite listelenmemiştir; ancak alıç "
        "kardiyotonik ve tansiyon düşürücü (hipotansif) etkilidir. Kalp yetmezliği, "
        "aritmi, yüksek/düşük tansiyon tedavisi görenler veya kalp/tansiyon ilacı "
        "(ör. beta bloker, digoksin, antihipertansifler) kullananlar hekime danışmadan "
        "tıbbi dozda kullanmamalıdır. Ameliyat öncesi kullanımda da profesyonel görüş alınmalıdır."
    )

    # --- 77 Çobançökerten / Tribulus terrestris ---
    # PFAF: ANNUAL/BIENNIAL, frost tender; often treat as frost-tender annual.
    # Seed = key medicinal (abortifacient, diuretic, tonic…). Hazards none known → yine uyarı ekle.
    p = get(77)
    assert "Tribulus terrestris" in (p.get("botanikAd") or "")
    p["temelBilgiler"]["bitkiTuru"] = (
        "tek yıllık / iki yıllık; sıklıkla dona hassas tek yıllık gibi yetiştirilir "
        "(Zygophyllaceae)"
    )
    p["genelTavsiyeMetni"] = (
        "Çobançökerten (Tribulus terrestris), Zygophyllaceae familyasından tek yıllık / "
        "iki yıllık bir bitkidir; dona hassas olup sıklıkla dona dayanıksız tek yıllık gibi "
        "yetiştirilir. Yaklaşık 0.6 m boya ulaşır. Doğal yayılış alanı: Avrupa - Kuzey "
        "Fransa ve doğuya doğru Doğu Asya."
    )
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: tohum (başlıca tıbbi organ: abortifasyan, idrar söktürücü, "
        "tonik, afrodizyak vb.), meyve, yaprak, sürgün, çiçek, gövde. Kullanım biçimi: "
        "tohum dekoksiyonu (geleneksel erkek üreme/idrar yolu kullanımları); "
        "kurutulmuş meyve preparatları; yaprak ve genç sürgünler gıda olarak pişirilerek "
        "(kıtlık gıdası)."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "PFAF Known hazards alanında özel bir toksisite listelenmemiştir; ancak tohum "
        "abortifasyan (düşük yapıcı) ve adet söktürücü olarak kaydedilmiştir. "
        "Hamilelikte ve hamilelik şüphesinde kesinlikle kullanılmamalıdır. "
        "Tıbbi dozajda uzman görüşü alınmalıdır."
    )

    # --- 78 Pelin Otu / Artemisia absinthium ---
    # PFAF: leaves occasionally flavouring; primary medicinal tea/bitter tonic;
    # Absinthe; high thujone — not ordinary culinary spice.
    p = get(78)
    assert "Artemisia absinthium" in (p.get("botanikAd") or "")
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak ve çiçekli sürgünler (hasat çiçeklenme döneminde). "
        "Kullanım biçimi: başlıca tıbbi — acı tonik çay/infüzyon (karaciğer, safra, "
        "sindirim; kısa süreli, düşük doz); harici lapa/kompres (morluk, burkulma). "
        "Yapraklar yalnızca ara sıra çeşni/aroma için kullanılır; sıradan mutfak "
        "baharatı değildir. Absinthe ve diğer alkollü içeceklerde geleneksel aroma "
        "kaynağıdır (tujon nedeniyle birçok ülkede kısıtlıdır)."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "Bitki büyük miktarlarda zehirlidir; küçük miktarlar bile sinir bozuklukları, "
        "havale, uykusuzluk yapabilir. Yalnızca kokusu bazı kişilerde baş ağrısı ve "
        "sinirliliğe yol açabilir. Yüksek tujon içerir: düşük dozda uyarıcı, aşırıda "
        "toksiktir. Nöbet yatkınlığında, hamilelikte ve emzirmede kaçınılmalıdır; "
        "çocuklara verilmemelidir. Absintizm etkileri: halüsinasyon, uykusuzluk, zeka "
        "kaybı, psikoz, tremor, nöbet. İç kullanım yalnızca kısa süreli, düşük dozda "
        "ve terciken uzman gözetiminde olmalıdır; sıradan baharat gibi serbest "
        "kullanılmamalıdır."
    )

    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated ids: 72, 73, 74, 75, 77, 78")


if __name__ == "__main__":
    main()
