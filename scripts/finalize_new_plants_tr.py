# -*- coding: utf-8 -*-
"""Yeni eklenen bitkilerin (204-211) kalan İngilizce metinlerini temizler ve boş faydaları doldurur."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"

# El ile düzeltilmiş Türkçe alanlar (PFAF ham metinlerinden)
FIXES = {
    204: {
        "genelTavsiyeMetni": (
            "Udi Hindi (Saussurea costus), Asteraceae familyasından yıllarca yaşayan bir bitkidir. "
            "Yaklaşık 3 m boya ulaşabilir. Doğal yayılış alanı Himalayalar (Doğu Asya)dır. "
            "Ayurveda ve Çin tıbbında kökü tonik ve baharat olarak değerlendirilir."
        ),
        "saglikKullanim": {
            "faydalari": (
                "Ağrı dindirici, antibakteriyel, kas spazmı çözücü, cinsel istek artırıcı, "
                "gaz giderici, adet söktürücü, uyarıcı, genel güçlendirici (tonik), solucan düşürücü."
            ),
            "kullanimSekli": "Kök baharat/çeşni olarak kullanılır; geleneksel preparatlarda yer alır.",
            "yanEtkilerUyarilar": "Kaynakta bilinen önemli bir uyarı belirtilmemiştir; tıbbi kullanımda uzman görüşü alınmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Doğu Asya - Himalayalar. Pakistan'dan Himachal Pradesh'e kadar 2000–3300 m yükseklikte, "
                "geçici sulanan alanlarda; Keşmir'de nemli gölgelik yerlerde, kimi zaman huş ormanı altında yetişir."
            ),
            "hasatMevsimi": "Tohumlar Ağustos - Eylül arasında olgunlaşır.",
            "ciceklenmeZamani": "Temmuz - Ağustos.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya yarı gölge ister.",
            "sulamaSikligi": "Nemli toprağı tercih eder.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu), ağır (killi) topraklar; pH: bazik (hafif alkali), hafif asidik, nötr.",
        },
    },
    205: {
        "genelTavsiyeMetni": (
            "Yakı Otu (Epilobium angustifolium), Onagraceae familyasından yıllarca yaşayan bir bitkidir. "
            "Yaklaşık 1,7 m boya ulaşır. Avrupa (Britanya dahil), ılıman Asya ve Kuzey Amerika'da yaygındır; "
            "yangın sonrası alanlarda sık görülür."
        ),
        "saglikKullanim": {
            "faydalari": (
                "İltihap giderici, kas spazmı çözücü, büzücü (astrenjan), yumuşatıcı (mukoza koruyucu), "
                "cilt yumuşatıcı, uyku getirici, müshil, lapa (harici uygulama), genel güçlendirici (tonik)."
            ),
            "kullanimSekli": "Kullanılan kısımlar: çiçek, yaprak, kök, sürgün, gövde. Kullanım biçimi: çay.",
            "yanEtkilerUyarilar": (
                "Genel olarak güvenli kabul edilir; olgun gövde ve yapraklarda tahriş edici bileşikler bulunabilir. "
                "Tıbbi kullanımda doz ve süre için uzman görüşü alınmalıdır."
            ),
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Avrupa (Britanya dahil), ılıman Asya ve Kuzey Amerika. "
                "Kayalık zeminler, boş araziler, orman kenarları ve bahçelerde yetişir."
            ),
            "hasatMevsimi": "Tohumlar Ağustos - Ekim arasında olgunlaşır.",
            "ciceklenmeZamani": "Temmuz - Eylül.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya yarı gölge ister.",
            "sulamaSikligi": "Kuru veya nemli toprağı tercih eder.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu), ağır (killi) topraklar; iyi drenaj tercih edilir; pH: bazik (hafif alkali), hafif asidik, nötr.",
        },
    },
    206: {
        "genelTavsiyeMetni": (
            "Funda (Calluna vulgaris), Ericaceae familyasından kışın da yeşil kalan bir çalıdır. "
            "Yaklaşık 0,6 m boya ulaşır. Avrupa'nın büyük bölümünde (Britanya dahil) ve kuzeybatı Fas'ta yaygındır; "
            "asitli fundalık ve bataklık alanların karakteristik bitkisidir."
        ),
        "saglikKullanim": {
            "faydalari": (
                "Kaygı giderici, romatizmaya iyi gelen, antiseptik, Bach çiçek özü, safra söktürücü, "
                "kan temizleyici, terletici, idrar söktürücü, balgam söktürücü, sakinleştirici, damar büzücü."
            ),
            "kullanimSekli": "Kullanılan kısımlar: sürgün. Kullanım biçimi: baharat/çeşni, çay.",
            "yanEtkilerUyarilar": "Kaynakta bilinen önemli bir uyarı belirtilmemiştir; tıbbi kullanımda uzman görüşü alınmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Avrupa'nın büyük bölümü (Britanya dahil) ve kuzeybatı Fas; yayılışının doğusunda daha seyrektir. "
                "Asit topraklı açık ormanlar, fundalıklar ve bataklık zeminlerde; iyi drene asit fundalıklarda baskın olabilir."
            ),
            "hasatMevsimi": "Tohumlar Ekim - Kasım arasında olgunlaşır.",
            "ciceklenmeZamani": "Temmuz - Ekim.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya yarı gölge ister.",
            "sulamaSikligi": "Kuru veya nemli toprağı tercih eder. Deniz etkisine (tuzlu rüzgâr) dayanıklıdır.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu) topraklar; besin yönünden zayıf toprakta da yetişebilir; pH: hafif asidik, çok asidik.",
        },
    },
    207: {
        "genelTavsiyeMetni": (
            "Yapışkan Andız Otu (Dittrichia viscosa), Asteraceae familyasından yıllarca yaşayan bir bitkidir. "
            "Yaklaşık 0,5 m boya ulaşır. Akdeniz Avrupası'nda yaygındır; yapışkan yapraklı, kokulu bir türdür. "
            "PFAF tıbbi kullanım derecesini 0/5 olarak kaydeder."
        ),
        "saglikKullanim": {
            "faydalari": "PFAF kaynağında bilinen tıbbi kullanım kaydı yoktur.",
            "kullanimSekli": "PFAF kaynağında yenilebilir veya tıbbi kullanım biçimi belirtilmemiştir.",
            "yanEtkilerUyarilar": "Kaynakta bilinen önemli bir uyarı belirtilmemiştir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Avrupa - Akdeniz. Britanya'da birkaç lokalitede girişim ve doğallaşma kaydı vardır. "
                "Boş arazilerde yetişir."
            ),
            "hasatMevsimi": "Belirtilmemiş.",
            "ciceklenmeZamani": "Eylül - Ekim.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Gölgede yetişemez; tam güneş ister.",
            "sulamaSikligi": "Nemli toprağı tercih eder.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu), ağır (killi) topraklar; pH: bazik (hafif alkali), hafif asidik, nötr.",
        },
    },
    208: {
        "genelTavsiyeMetni": (
            "Hint Yağı Otu / Castor (Ricinus communis), Euphorbiaceae familyasından kışın da yeşil kalan bir çalıdır. "
            "Yaklaşık 1,5 m boya ulaşabilir. Asıl yabanı belirsizdir; Afrika kökenli olduğu düşünülür. "
            "Tohumlarından elde edilen hint yağı uzun süredir müshil olarak kullanılır; bitkinin kendisi zehirlidir."
        ),
        "saglikKullanim": {
            "faydalari": (
                "Bağırsak paraziti giderici, kepek giderici, öksürük kesici, kuvvetli müshil, "
                "cilt yumuşatıcı, balgam söktürücü."
            ),
            "kullanimSekli": "Kullanılan kısımlar: arıtılmış tohum yağı. Yalnızca eczacılıkta/endüstride arıtılmış formda kullanılır.",
            "yanEtkilerUyarilar": (
                "Bitkinin tüm kısımları, özellikle tohumları, risin toksini nedeniyle yüksek derecede zehirlidir; "
                "yenmemelidir. Tek bir tohum bile çocuklarda ölümcül olabilir. "
                "Hint yağı yalnızca endüstriyel/eczacılıkta arıtılmış formda kullanılır. Tohumları çocuklardan uzak tutun."
            ),
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Asıl yabanı belirsizdir (muhtemelen Afrika). Güney ve orta-güney Avrupa'da doğallaşmıştır. "
                "Gerçek anlamda yabani popülasyon bilinmez."
            ),
            "hasatMevsimi": "Tohumlar Eylül - Kasım arasında olgunlaşır.",
            "ciceklenmeZamani": "Temmuz - Eylül.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Gölgede yetişemez; tam güneş ister.",
            "sulamaSikligi": "Nemli toprağı tercih eder.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu), ağır (killi) topraklar; iyi drenaj tercih edilir; pH: bazik (hafif alkali), hafif asidik, nötr.",
        },
    },
    209: {
        "genelTavsiyeMetni": (
            "Pelesenk (Styrax officinalis), Styracaceae familyasından kışın yapraklarını döken bir çalı/ağaççıktır. "
            "Yaklaşık 5 m boya ulaşabilir. Doğu Akdeniz Avrupası'nda yetişir; gövde ve dallarından balsamik reçine elde edilir."
        ),
        "saglikKullanim": {
            "faydalari": "Antiseptik, balgam söktürücü (gövde reçinesi).",
            "kullanimSekli": "Reçine baharat/çeşni ve geleneksel preparatlarda kullanılır.",
            "yanEtkilerUyarilar": "Kaynakta bilinen önemli bir uyarı belirtilmemiştir; tıbbi kullanımda uzman görüşü alınmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Doğu Akdeniz Avrupası. Kuru kayalık yamaçlarda (çoğunlukla kireçtaşı üzerinde) 1500 m'ye kadar; "
                "orman ve çalılıklarda, ayrıca akarsu kenarlarında yetişir."
            ),
            "hasatMevsimi": "Tohumlar Ekim ayında olgunlaşır.",
            "ciceklenmeZamani": "Haziran.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya yarı gölge ister.",
            "sulamaSikligi": "Yerleştikten sonra kuraklığa dayanabilir; nemli toprağı da tercih eder.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu) topraklar; iyi drenaj tercih edilir; pH: hafif asidik, nötr.",
        },
    },
    210: {
        "genelTavsiyeMetni": (
            "Aspir (Carthamus tinctorius), Asteraceae familyasından bir mevsim yaşayan bitkidir. "
            "Yaklaşık 1 m boya ulaşır. Kuzey Afrika (Mısır) kökenlidir; tohum yağı ve çiçek boyası için yetiştirilir."
        ),
        "saglikKullanim": {
            "faydalari": (
                "Kan dolaşımını destekleyici, ağrı dindirici, antibakteriyel, iltihap giderici; "
                "çiçekleri modern araştırmalarda kolesterol ve koroner riskle ilişkilendirilmiştir (PFAF)."
            ),
            "kullanimSekli": "Kullanılan kısımlar: sürgün, çiçek, tohum yağı. Gıda ve geleneksel tıbbi preparatlarda yer alır.",
            "yanEtkilerUyarilar": (
                "Gebelikte yüksek dozlarda kullanılmamalıdır. "
                "Bağışıklık baskılanması durumunda dikkatli olunmalıdır. Alerji öyküsü olanlar hekime danışmalıdır."
            ),
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Kuzey Afrika - Mısır. Britanya'da nadir geçici kayıtlar vardır. "
                "Zayıf, kuru topraklarda tam güneşte yetişir."
            ),
            "hasatMevsimi": "Tohumlar Eylül - Ekim arasında olgunlaşır.",
            "ciceklenmeZamani": "Ağustos - Ekim.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Gölgede yetişemez; tam güneş ister.",
            "sulamaSikligi": "Yerleştikten sonra kuraklığa dayanabilir; kuru veya nemli toprağı tercih eder.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu) topraklar; iyi drenaj; besin yönünden zayıf toprakta da yetişebilir; pH: bazik–çok alkali, hafif asidik, nötr.",
        },
    },
    211: {
        "genelTavsiyeMetni": (
            "Jojoba (Simmondsia chinensis), Simmondsiaceae familyasından kışın da yeşil kalan bir çalıdır. "
            "Yaklaşık 2 m boya ulaşır. Güneybatı Kuzey Amerika'da (Kaliforniya, Arizona) ve kuzeybatı Meksika'da yetişir; "
            "tohumlarından elde edilen mumsu yağ kozmetik ve cilt bakımında kullanılır."
        ),
        "saglikKullanim": {
            "faydalari": (
                "Tohum mumsu yağı sedef, yara ve cilt rahatsızlıklarında haricen kullanılır; "
                "geleneksel olarak böbrek rahatsızlıkları, soğuk algınlığı, idrar zorluğu ve saç dökülmesine yönelik kullanımlar kaydedilmiştir (PFAF)."
            ),
            "kullanimSekli": "Kullanılan kısımlar: tohum ve tohum yağı/mumu. Çoğunlukla harici cilt bakımı.",
            "yanEtkilerUyarilar": "Kaynakta bilinen önemli bir uyarı belirtilmemiştir; tıbbi kullanımda uzman görüşü alınmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Güneybatı Kuzey Amerika - Kaliforniya, Arizona ve kuzeybatı Meksika. "
                "İyi drene çöl topraklarında: kumlu alüvyon, iri çakıl–kil karışımları ve tınlı zeminler."
            ),
            "hasatMevsimi": "Tohum hasadı olgunlaşmaya göre yapılır (iklime bağlı).",
            "ciceklenmeZamani": "İklim bölgesine göre değişir.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Gölgede yetişemez; tam güneş ister.",
            "sulamaSikligi": "Yerleştikten sonra kuraklığa dayanabilir.",
            "toprakTipi": "Orta (tınlı), hafif (kumlu) topraklar; iyi drenaj; pH geniş aralık; tuzlu toprağa dayanabilir.",
        },
    },
}


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    for plant in plants:
        pid = plant["id"]
        if pid not in FIXES:
            continue
        fix = FIXES[pid]
        plant["genelTavsiyeMetni"] = fix["genelTavsiyeMetni"]
        plant["saglikKullanim"].update(fix["saglikKullanim"])
        plant["cografyaMevsim"].update(fix["cografyaMevsim"])
        plant["bakimYetistirme"].update(fix["bakimYetistirme"])
        changed += 1
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Guncellendi: {changed} bitki")


if __name__ == "__main__":
    main()
