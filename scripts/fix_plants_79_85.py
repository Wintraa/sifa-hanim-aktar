# -*- coding: utf-8 -*-
"""Düzeltmeler: id 79–85 (Yarpuz, Şevketi Bostan, Öksürük Otu, Mersin, Söğüt, Centiyane, Ihlamur).

Her kayıt için plants.json + _pfafOrijinal okunarak PFAF ile uyumlu Türkçe alanlar güncellenir.
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

    # --- 79 Yarpuz / Mentha pulegium ---
    p = get(79)
    # temelBilgiler / botanikAd yapısal olarak ayrı tutulur; tutarlı bırakılır
    p["temelBilgiler"] = {
        "turkceAdi": "Yarpuz",
        "botanikAdi": "Mentha pulegium",
        "bitkiTuru": "yıllarca yaşayan (Lamiaceae)",
    }
    p["botanikAd"] = "Mentha pulegium"
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Tam güneş tercih eder; yarı gölgeyi tolere eder "
        "(uçucu yağ verimi için güneşli konum daha uygundur)."
    )
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak; taze veya kurutulmuş çiçekli ot / toprak üstü "
        "aksam (flowering herb / whole aerial plant); yapraklardan damıtılan uçucu yağ. "
        "Kullanım biçimi: baharat/çeşni; taze veya kuru yaprak çayı; tıbbi özütler "
        "çoğunlukla çiçeklenme döneminde hasat edilen toprak üstü aksamdan; uçucu yağ "
        "haricen/kontrollü preparatlarda (yüksek toksisite — uyarılar bölümüne bakın)."
    )
    # Uyarılar zaten yağ toksisitesini kapsıyor; çiçekli ot/özüt odağını netleştir
    yan = (p["saglikKullanim"].get("yanEtkilerUyarilar") or "").strip()
    if "çiçekli ot" not in yan.lower() and "toprak üstü" not in yan.lower():
        p["saglikKullanim"]["yanEtkilerUyarilar"] = (
            yan
            + " Uçucu yağ ve yüksek dozlu özütler (özellikle çiçekli toprak üstü "
            "aksamdan elde edilenler) toksisite ve düşük riskinin merkezindedir; "
            "tıbbi dozajda uzman görüşü şarttır."
        ).strip()

    # --- 80 Şevketi Bostan / Cnicus benedictus (PFAF kaydı; kök+çiçek başı kullanımları) ---
    p = get(80)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak, çiçek (çiçek başları), kök, tohum yağı; "
        "tıbbi kullanımda çoğunlukla çiçeklenme dönemindeki bütün bitki. "
        "Kullanım biçimi: genç yapraklar çiğ; açılmamış çiçek başları enginar "
        "(Cynara) benzeri sebze olarak (küçük ve zahmetli); kök haşlanarak "
        "pot-herb/haşlama sebze; baharat/çeşni ve tohum yağı. "
        "Tıbbi olarak asıl roller iştah açıcı, acı tonik ve sindirim "
        "(anoreksi, dispepsi, karaciğer/safra) içindir — sıcak veya soğuk "
        "infüzyon/çay. Geleneksel soğuk infüzyonun gebelik önleyici olarak "
        "kullanıldığı da kaydedilmiştir; bu ikincil/tarihsel bir uygulamadır ve "
        "sindirim–iştah kullanımlarının yerine geçmez. Emzirenlerde süt artırıcı "
        "ılık infüzyon da gelenekseldir; yüksek dozlar kusturucudur."
    )

    # --- 81 Öksürük Otu / Tussilago farfara ---
    p = get(81)
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Tam güneş tercih eder; yarı gölgeyi de tolere eder."
    )
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak, çiçek (çiçek sapları), kök/rizom (kök gövdesi), "
        "yağ. Kullanım biçimi: yaprak ve çiçek çayı veya kaynatma (öksürük/solunum); "
        "çiçek tomurcuğu ve genç çiçekler çiğ/pişmiş; yaprak salata, çorba veya sebze; "
        "kurutulmuş yakılmış yaprak tuz yerine; ince kök gövdesi (rootstock) şeker "
        "şurubunda şekerleme (candied); kökten acı tonik/terletici preparat. "
        "Tıbbi olarak yapraklar Avrupa’da yaygındır; kök bazen kullanılır. "
        "Çiçekler pirolizidin alkaloitleri açısından daha yüksektir — uyarılar bölümüne bakın."
    )

    # --- 82 Mersin Bitkisi / Myrtus communis ---
    p = get(82)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: yaprak ve sürgün/dalcık (twigs) — başlıca buruk "
        "(astrenjan), antiseptik ve kanama durdurucu kaynak; çiçek; meyve; "
        "yaprak ve dalcıklardan uçucu yağ. "
        "Kullanım biçimi: yaprak taze veya kuru (iç/dış tıbbi kullanım, baharat); "
        "meyve taze/kuru çeşni veya ekşi içecek; çiçek tomurcuğu ve çiçek salata/"
        "çeşni; uçucu yağ (myrtol içeren) lokal antiseptik preparatlarda."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "PFAF “Known hazards” alanında özel bir liste yoktur; ancak uçucu yağ ve "
        "içindeki myrtol yüksek dozlarda toksik olabilir — damıtılmış yağı ağızdan "
        "yüksek dozda kullanmayın. Etken maddeler hızla sistemik emilir; alımdan "
        "kısa süre sonra idrara menekşe benzeri koku verebilir (PFAF). "
        "Tıbbi dozaj ve uçucu yağ kullanımında uzman görüşü alınmalıdır; "
        "hamilelik/emzirme ve çocuklarda özellikle dikkatli olun."
    )

    # --- 83 Söğüt Kabuğu / Salix alba ---
    p = get(83)
    p["bakimYetistirme"]["sulamaSikligi"] = (
        "Nemli veya ıslak toprağı tercih eder (dere/nehir kenarı, sulak alanlar; "
        "aralıklı taşkınlı veya kötü drene topraklarda da yetişebilir). "
        "Deniz etkisine (tuzlu rüzgâr) dayanıklıdır."
    )
    p["bakimYetistirme"]["toprakTipi"] = (
        "Orta (tınlı), hafif (kumlu), ağır (killi) topraklar; ağır killi toprakta "
        "da yetişebilir; nemli–ağır toprakları sever. "
        "pH: hafif asidik ve nötr. Kireçli/tebeşirli (chalky) ve alkali topraklarda "
        "genelde zayıf gelişir; ince–yoksul topraklardan hoşlanmaz."
    )

    # --- 84 Centiyane / Gentiana lutea ---
    p = get(84)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: kök (başlıca tıbbi organ; tıbbi derece 5/5 acı tonik). "
        "Kullanım biçimi: sonbaharda hasat edilip kurutulan kök; kaynatma (decoction) "
        "veya çay/özüt olarak sindirim toniği (iştahsızlık, dispepsi, karaciğer/"
        "safra, genel güçsüzlük). Gıda/çeşni: gentian bitters (acin) üretiminde; "
        "şerbetçiotu yaygınlaşmadan önce birada aroma olarak. "
        "Çiçek açmamış bitkilerin köklerinin tıbbi açıdan daha zengin olabileceği "
        "kaydedilmiştir. Mide/duodenum ülserinde kullanılmaz — uyarılar bölümüne bakın."
    )

    # --- 85 Ihlamur / Tilia cordata ---
    p = get(85)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: çiçek (lime flowers — başlıca tıbbi ve çay organı); "
        "yaprak; özsu (sap); odun kömürü (tıbbi); tomurcuk/olgunlaşmamış meyve "
        "(gıda pastası). "
        "Kullanım biçimi: taze veya kuru çiçek çayı (soğuk algınlığı, terletici, "
        "sakinleştirici, tansiyon vb.); genç yapraklar salata/sandviç; ilkbahar "
        "özsuyu içecek veya şurup; öğütülmüş çiçek ve olgunlaşmamış meyveden "
        "çikolata benzeri pasta (kolay bozulur); odundan yapılan kömür mide/"
        "dispeptik rahatsızlıklarda içsel, yanık ve yaralarda toz olarak haricen. "
        "Çiçekler taze açmışken hasat edilmelidir — yaşlı çiçekler narkotik etki "
        "gösterebilir (uyarılar)."
    )

    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated plants.json for ids 79–85")
    for pid in (79, 80, 81, 82, 83, 84, 85):
        pl = get(pid)
        sk = pl["saglikKullanim"]
        by = pl["bakimYetistirme"]
        print(f"\n--- id {pid} {pl['ad']} ---")
        print("isik:", by.get("isikIhtiyaci"))
        print("sulama:", by.get("sulamaSikligi"))
        print("toprak:", (by.get("toprakTipi") or "")[:180])
        print("kullanim:", (sk.get("kullanimSekli") or "")[:220])
        print("yan:", (sk.get("yanEtkilerUyarilar") or "")[:180])


if __name__ == "__main__":
    main()
