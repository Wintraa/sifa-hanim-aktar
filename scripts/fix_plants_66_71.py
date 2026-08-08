# -*- coding: utf-8 -*-
"""Düzeltmeler: id 66-71 (Ayı Üzümü, Hayıt Otu, Aslanpençesi, Ayrık Otu, At Kestanesi, Geven Otu).

Her kayıt için Türkçe alanlar ve _pfafOrijinal PFAF metinleriyle hizalanır.
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

    # --- 66 Ayı Üzümü / Arctostaphylos uva-ursi ---
    p = get(66)
    # botanikAd / temelBilgiler.botanikAdi tek ve tutarlı kalsın (UI her ikisini de gösterir)
    p["botanikAd"] = "Arctostaphylos uva-ursi"
    p["temelBilgiler"]["botanikAdi"] = "Arctostaphylos uva-ursi"
    p["saglikKullanim"]["kullanimSekli"] = (
        "Tıbbi kullanılan kısım: yaprak (meyve değil). Kullanım biçimi: erken sonbaharda "
        "toplanan yeşil yapraklar kurutulur; kuru yaprak çayı idrar yolu antiseptiği / "
        "antibakteriyel amaçla (tercihen uzman gözetiminde); yaprak infüzyonu haricen lapa, "
        "göz/ağız yıkama vb. Gıda kategorisi (yenilebilirlik): meyve — çiğ veya pişmiş, "
        "reçel/marmelat; tadı kuru ve büzücüdür. Not: tıbbi çay yapraktan yapılır; meyve "
        "gıda kullanımıdır."
    )
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Tam gölgeden (yoğun orman altı) tam güneşe kadar yetişebilir; yarı gölgeyi "
        "(açık orman) da tolere eder. Gölgede meyve verimi azalabilir."
    )

    # --- 67 Hayıt Otu / Vitex agnus-castus ---
    p = get(67)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Birincil tıbbi kullanım (PFAF tıbbi derece 5/5): tohum ve meyve (berry) — kadın "
        "hormonal sistemini dengelemek için tentür veya tohum/meyve preparatları "
        "(adet düzensizliği, PMS, menopoz şikayetleri vb.; uzman görüşüyle). İkincil gıda/"
        "mutfak: meyve baharat/çeşni (biber ikamesi); aromatik yaprak da baharat olarak; "
        "ras el hanout karışımlarında kullanılır."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "Baş ağrısı, karın krampları ve ishal, artmış adet kanaması, döküntüler, kaşıntı. "
        "Aşırı dozda formikasyon (ciltte böcek geziyormuş hissi) ile seyreden nörolojik "
        "rahatsızlık bildirilmiştir — yüksek dozdan kaçının. Hamilelikte önerilmez; süt "
        "üretimini baskılayabilir. Tıbbi dozajda hekim/eczacıya danışın."
    )

    # --- 68 Aslanpençesi / Alchemilla xanthochlora (vulgaris agg.) ---
    p = get(68)
    p["botanikAd"] = "Alchemilla xanthochlora"
    p["temelBilgiler"]["botanikAdi"] = "Alchemilla xanthochlora"
    p["temelBilgiler"]["turkceAdi"] = "Aslanpençesi"
    p["kaynak"]["eslesenAd"] = "Alchemilla xanthochlora"
    # Taksonomi notu: vulgaris adı yaygın; PFAF eşleşmesi xanthochlora
    p["genelTavsiyeMetni"] = (
        "Aslanpençesi (Alchemilla xanthochlora; sıklıkla A. vulgaris agregatı / eski adıyla "
        "A. vulgaris olarak anılır), Rosaceae familyasından yıllarca yaşayan bitkidir. "
        "Yaklaşık 0,3 m boya ulaşır. Flora Europaea’da A. xanthochlora Rothm. olarak "
        "listelenir; halk ve bazı kaynaklarda ‘A. vulgaris’ adı bu grup için kullanılır "
        "(taksonomi belirsizliği). Doğal yayılış alanı: Avrupa (Britanya dahil), Norveç – "
        "İspanya ve doğuya doğru Polonya."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "Bitki tanen bakımından zengindir (büzücü / astrenjan etki). Aşırı veya uygunsuz "
        "kullanım, yüksek tanen içeriği nedeniyle mide hassasiyetine / mide rahatsızlığına "
        "yol açabilir. PFAF Known hazards alanında ayrı bir toksin listelenmemiştir; yine "
        "de uzun süreli veya yüksek dozda kullanımda dikkatli olunmalı, tıbbi kullanımda "
        "uzman görüşü alınmalıdır."
    )
    p["bakimYetistirme"]["toprakTipi"] = (
        "Orta (tınlı), hafif (kumlu), ağır (killi) topraklar; iyi drene olması tercih "
        "edilir; ağır killi toprakta da yetişebilir; pH: nötr ve bazik (hafif alkali) — "
        "PFAF: neutral and basic (mildly alkaline)."
    )
    p["bakimYetistirme"]["isikIhtiyaci"] = (
        "Yarı gölgede (açık orman) veya gölgesiz / tam güneşte yetişebilir."
    )

    # --- 69 Ayrık Otu / Elymus repens ---
    p = get(69)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısımlar: rizom/kök (başlıca), genç yaprak/sürgün, tohum. Kullanım "
        "biçimi: rizom çayı (idrar yolu / böbrek destekleyici tıbbi kullanım); kavrulmuş "
        "rizom kahve ikamesi; kurutulup un haline getirilerek ekmek ununa katılır; uzun "
        "kaynatmayla şurup ve bazen bira yapımı; genç sürgünler ilkbahar salatasında "
        "(lifli). Tohum tahıl lapası olarak (küçük ve kabuklu)."
    )
    p["bakimYetistirme"]["sulamaSikligi"] = (
        "Kuru, nemli veya yaş toprakları tercih eder."
    )

    # --- 70 At Kestanesi / Aesculus hippocastanum ---
    p = get(70)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Tıbbi kullanılan kısımlar: kabuk (ilkbaharda hasat; çay, damar toniği), yaprak "
        "(ateş / boğmaca vb. için çay), tohum (romatisma, hemoroid vb.; harici yağ/jel "
        "dahil), ayrıca kök tozu analjezik kayıtlarda. Gıda kullanımı (dikkat): kavrulmuş "
        "tohum yalnızca saponinler uzaklaştırıldıktan sonra kahve ikamesi / un olarak "
        "anılır — doğrudan güvenli gıda/kahve değildir. Tohum veya un akan suda uzun "
        "yıkama (liç) ve iyice pişirme gerekir; işlem mineralleri de azaltır. Dahili tıbbi "
        "kullanım potansiyel olarak toksiktir; profesyonel gözetim olmadan içilmemelidir."
    )
    p["saglikKullanim"]["yanEtkilerUyarilar"] = (
        "UYARI: Tohum toksik saponinler içerir; çiğ veya işlenmemiş tohum yenmemeli / "
        "doğrudan kahve gibi tüketilmemelidir. Saponinler zayıf emilse de acıdır; büyük "
        "miktarlarda tüketim önerilmez. Gıda için mutlaka akan suda dikkatli liç/yıkama "
        "ve iyice pişirme (gerekirse pişirme suyunu değiştirme) gerekir. Bitki dahili "
        "alınırsa potansiyel olarak toksiktir — profesyonel gözetim olmadan dahili "
        "kullanmayın. Böbrek veya karaciğer hastalığında kaçının. Varfarin / antikoagülan "
        "tedaviyle etkileşebilir; bu ilaçları kullananlar kaçınmalıdır. Saponinler balık "
        "gibi bazı canlılar için çok daha toksiktir."
    )

    # --- 71 Geven Otu / Astragalus membranaceus ---
    p = get(71)
    p["saglikKullanim"]["kullanimSekli"] = (
        "Kullanılan kısım: kök (Huang Qi; geleneksel Çin tıbbında temel bitkilerden). "
        "Kullanım biçimi: kök kaynatması / çay (dekoksiyon); çorba ve yemeklere katılan "
        "tıbbi gıda yardımcısı; tentür / özüt. PFAF yenilebilirlik derecesi 0/5 ve "
        "yenilebilir kullanım alanı boş/mutfak gıdası olarak listelenmez — bu alan "
        "mutfak yenilebilirliğini değil, tıbbi kök kullanımını ifade eder. Kök genellikle "
        "4 yaşındaki bitkilerden sonbaharda hasat edilip kurutulur. Tıbbi dozajda uzman "
        "görüşü alınmalıdır."
    )

    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("OK: id 66-71 düzeltildi ->", DATA)


if __name__ == "__main__":
    main()
