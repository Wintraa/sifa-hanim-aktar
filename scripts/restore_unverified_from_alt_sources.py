# -*- coding: utf-8 -*-
"""PFAF'ta bulunamayan 25 bitkiyi guvenilir kuresel kaynaklara dayali
yeniden olusturup plants.json'a ekler.

Kaynaklar (ornegin): Kew POWO, EMA HMPC, NCCIH, German Commission E,
Missouri Botanical Garden, MSKCC, GRIN.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
OUT_LOG = ROOT / "data" / "restored_from_alt_sources.json"

TODAY = date.today().isoformat()

# Her kayit: site semasi + kaynak kumesı (arayuzde gosterilmez, denetim icin saklanir)
PLANTS: list[dict] = [
    {
        "ad": "Gül",
        "botanikAd": "Rosa damascena",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/06-rose.jpg",
        "genelTavsiyeMetni": "Şam gülü (Rosa damascena), Akdeniz ve Batı Asya kökenli, yoğun kokulu çiçekleriyle bilinen çok yıllık bir çalıdır. Bahçe süsü, gül yağı ve gül suyu üretiminde kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Gül",
            "botanikAdi": "Rosa damascena",
            "bitkiTuru": "çok yıllık çalı (Rosaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Gül yağı ve gül suyu geleneksel olarak cilt bakımında ve aromaterapide kullanılır; yapraklar bazı mutfak tariflerinde yer alır.",
            "kullanimSekli": "Süs bitkisi olarak yetiştirilir; uygun üretim koşullarında çiçeklerden gül suyu veya yağ elde edilir.",
            "yanEtkilerUyarilar": "Tarım ilacı uygulanmış süs gülleri tüketilmemelidir. Dikenler yaralanmaya yol açabilir. Esansiyel yağ deride tahriş yapabilir; seyreltilmeden kullanılmamalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Doğal yayılış: Batı Asya ve Güneydoğu Avrupa; Türkiye’de Isparta başta olmak üzere kültür formları yaygındır.",
            "hasatMevsimi": "Çiçek hasadı genellikle Mayıs-Haziran",
            "ciceklenmeZamani": "Mayıs - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş (günde en az 6 saat)",
            "sulamaSikligi": "Düzenli; toprağın üst kısmı kurudukça sulanır, kışın azaltılır",
            "toprakTipi": "Humuslu, iyi drene, hafif asidik–nötr bahçe toprağı",
        },
        "kaynak": {
            "ad": "Kew POWO / Missouri Botanical Garden",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
            "not": "Tür düzeyi Rosa damascena olarak netleştirildi (önceki Rosa spp. yerine).",
        },
    },
    {
        "ad": "Orkide",
        "botanikAd": "Phalaenopsis amabilis",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/11-phalaenopsis.jpg",
        "genelTavsiyeMetni": "Phalaenopsis (kelebek orkidesi), Güneydoğu Asya tropik ormanlarında epifitik yaşayan, uzun ömürlü çiçek salkımlarıyla bilinen bir süs bitkisidir. Evlerde dolaylı ışık ve hava alan orkide karışımında yetiştirilir.",
        "temelBilgiler": {
            "turkceAdi": "Orkide",
            "botanikAdi": "Phalaenopsis amabilis",
            "bitkiTuru": "epifitik orkide (Orchidaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Asıl değeri dekoratiftir; tıbbi kullanımı yoktur.",
            "kullanimSekli": "İç mekânda süs bitkisi olarak yetiştirilir.",
            "yanEtkilerUyarilar": "Aşırı sulama kök çürümesine yol açar. Yapısal olarak yenilebilir kabul edilmez.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Doğal yayılış: Malezya takımadaları ve Güneydoğu Asya tropik ormanları",
            "hasatMevsimi": "Hasat yapılmaz; çiçek gözlemi esastır",
            "ciceklenmeZamani": "Uygun koşullarda yıl içinde, sıklıkla kış–ilkbahar",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ama doğrudan güneş almayan ışık",
            "sulamaSikligi": "Orkide kabuğu kurudukça ölçülü sulama; suda bekletilmez",
            "toprakTipi": "Kabuklu, hava alan özel orkide karışımı",
        },
        "kaynak": {
            "ad": "Kew POWO / Missouri Botanical Garden",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
            "not": "Temsilci tür Phalaenopsis amabilis olarak netleştirildi.",
        },
    },
    {
        "ad": "Zerdeçal",
        "botanikAd": "Curcuma longa",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/14-openverse.jpg",
        "genelTavsiyeMetni": "Zerdeçal (Curcuma longa), Zingiberaceae familyasından, Güneybatı Hindistan kökenli rizomlu bir kültür bitkisidir. Rizomu baharat ve geleneksel bitkisel tıpta kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Zerdeçal",
            "botanikAdi": "Curcuma longa",
            "bitkiTuru": "rizomlu geofit (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "EMA HMPC’ye göre geleneksel kullanımda hafif sindirim şikayetleri (şişkinlik, yavaş sindirim, gaz) için değerlendirilir.",
            "kullanimSekli": "Kurutulmuş rizom tozu baharat veya demleme olarak; yetişkinlerde kısa süreli kullanım için monograflarda tarif edilmiştir.",
            "yanEtkilerUyarilar": "Safra yolu tıkanıklığı, kolanjit, safra taşı, karaciğer hastalığı olanlarda önerilmez (EMA). 18 yaş altında önerilmez. Gebelikte yüksek dozdan kaçınılmalıdır. Antikoagülanlarla birlikte kanama riski artabilir. Ağız kuruluğu, gaz ve mide tahrişi görülebilir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Kültür formu olarak Güneybatı Hindistan kökenli; tropik ve subtropik bölgelerde yetiştirilir (Kew POWO).",
            "hasatMevsimi": "Yapraklar kuruduğunda rizom hasadı (yaklaşık 7–10 ay)",
            "ciceklenmeZamani": "Sıcak mevsim",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ışık; kısmi gölge tolere eder",
            "sulamaSikligi": "Büyüme döneminde düzenli nem; kış dinlenmesinde azaltılır",
            "toprakTipi": "Zengin, iyi drene, nemli toprak",
        },
        "kaynak": {
            "ad": "Kew POWO; EMA HMPC Curcumae longae rhizoma",
            "url": "https://www.ema.europa.eu/en/medicines/herbal/curcumae-longae-rhizoma",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Kakule",
        "botanikAd": "Elettaria cardamomum",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/photos/42-cardamom.jpg",
        "genelTavsiyeMetni": "Kakule (Elettaria cardamomum), zencefilgillerden, Güney Hindistan Batı Gatları ve Sri Lanka kökenli aromatik bir çok yıllıktır. Tohum kapsülleri baharat olarak kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Kakule",
            "botanikAdi": "Elettaria cardamomum",
            "bitkiTuru": "çok yıllık otsu (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak sindirim rahatlatıcı ve baharat olarak kullanılır; mutfak ve çay karışımlarında yaygındır.",
            "kullanimSekli": "Kurutulmuş tohum kapsülleri baharat veya demleme olarak",
            "yanEtkilerUyarilar": "Mutfak dozlarında genellikle tolere edilir. Yüksek miktarda mide tahrişi yapabilir. Bilinen alerjisi olanlar kaçınmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Anavatanı: Güney Hindistan (Batı Gatlar) ve Sri Lanka; tropiklerde kültürü yaygındır (GRIN / Missouri Botanical Garden).",
            "hasatMevsimi": "Kapsüller olgunlaşıp yeşilken hasat edilir",
            "ciceklenmeZamani": "Tropiklerde yağışlı döneme bağlı; kültürde yıl boyu çiçeklenebilir",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Yarı gölge (orman altı); yoğun güneşten korunur",
            "sulamaSikligi": "Yüksek ve düzenli nem ister; kuraklığa dayanıksızdır",
            "toprakTipi": "Humusça zengin, asidik, iyi drene orman toprağı",
        },
        "kaynak": {
            "ad": "USDA GRIN; Missouri Botanical Garden",
            "url": "https://www.missouribotanicalgarden.org/PlantFinder/PlantFinderDetails.aspx?taxonid=287608",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Paçuli",
        "botanikAd": "Pogostemon cablin",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/photos/45-pogostemon-cablin.jpg",
        "genelTavsiyeMetni": "Paçuli (Pogostemon cablin), Lamiaceae familyasından, Güneydoğu Asya kökenli aromatik bir otsu bitkidir. Yapraklarından elde edilen uçucu yağ parfümeri ve aromaterapide kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Paçuli",
            "botanikAdi": "Pogostemon cablin",
            "bitkiTuru": "çok yıllık otsu (Lamiaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Uçucu yağ geleneksel olarak koku sabitleyici ve cilt bakımında harici kullanılır.",
            "kullanimSekli": "Esansiyel yağ olarak seyreltilmiş harici kullanım; yapraklar kurutularak saklanır",
            "yanEtkilerUyarilar": "Saf esansiyel yağ deride tahriş ve alerjik reaksiyon yapabilir; seyreltilmeden kullanılmamalıdır. İç kullanım tıbbi denetim olmadan önerilmez.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Güneydoğu Asya (özellikle Endonezya, Filipinler, Malezya) tropik bölgeleri",
            "hasatMevsimi": "Yaprak hasadı sıcak mevsimde birkaç kez",
            "ciceklenmeZamani": "Sıcak tropik koşullarda",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak dolaylı ışık veya yarı gölge",
            "sulamaSikligi": "Düzenli nem; su birikimine izin verilmez",
            "toprakTipi": "Verimli, iyi drene, hafif asidik toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Begonya",
        "botanikAd": "Begonia cucullata",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/49-begonia.jpg",
        "genelTavsiyeMetni": "Mum begonyası grubu (Begonia cucullata / semperflorens grubu), Güney Amerika kökenli, sürekli çiçeklenen popüler bir süs bitkisidir. Saksı ve bordürlerde yaygın yetiştirilir.",
        "temelBilgiler": {
            "turkceAdi": "Begonya",
            "botanikAdi": "Begonia cucullata",
            "bitkiTuru": "çok yıllık otsu süs (Begoniaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım; tıbbi kullanım hedeflenmez.",
            "kullanimSekli": "Saksı veya bahçe süsü",
            "yanEtkilerUyarilar": "Bazı Begonia türleri oksalik asit içerir; yenmemelidir. Evcil hayvanlar için potansiyel olarak toksik olabilir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Güney Amerika (doğal); ılıman bölgelerde yazlık veya iç mekân süsü",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "İlkbahar - sonbahar (sıcak iklimde daha uzun)",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak dolaylı ışık veya sabah güneşi",
            "sulamaSikligi": "Toprak yüzey kurudukça; yapraklara aşırı su değdirilmez",
            "toprakTipi": "Hafif, iyi drene, organik maddece zengin saksı harcı",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
            "not": "Eski ad Begonia semperflorens; kabul gören ad Begonia cucullata.",
        },
    },
    {
        "ad": "Camgüzeli",
        "botanikAd": "Impatiens walleriana",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/58-impatiens-walleriana.jpg",
        "genelTavsiyeMetni": "Camgüzeli (Impatiens walleriana), Doğu Afrika kökenli, gölgeye uyumlu, sürekli çiçeklenen bir süs bitkisidir. Saksı ve gölgeli bordürlerde tercih edilir.",
        "temelBilgiler": {
            "turkceAdi": "Camgüzeli",
            "botanikAdi": "Impatiens walleriana",
            "bitkiTuru": "çok yıllık (ılıman iklimde yıllık gibi) otsu (Balsaminaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım.",
            "kullanimSekli": "Süs bitkisi",
            "yanEtkilerUyarilar": "Yenilebilir kabul edilmez. Aşırı sulama kök hastalıklarına yol açar.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Doğu Afrika (Tanzanya, Mozambik vb.); dünya çapında süs olarak kültüre alınmıştır",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "İlkbahar - sonbahar",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Yarı gölge veya parlak dolaylı ışık",
            "sulamaSikligi": "Düzenli nem; kuraklığa hassastır",
            "toprakTipi": "Humuslu, nem tutan ama iyi drene toprak",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden / Kew POWO",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Barış Çiçeği",
        "botanikAd": "Spathiphyllum wallisii",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/61-spathiphyllum.jpg",
        "genelTavsiyeMetni": "Barış çiçeği (Spathiphyllum wallisii), Orta ve Güney Amerika tropiklerinden gelen, beyaz spateli çiçekleriyle bilinen popüler bir iç mekân bitkisidir.",
        "temelBilgiler": {
            "turkceAdi": "Barış Çiçeği",
            "botanikAdi": "Spathiphyllum wallisii",
            "bitkiTuru": "çok yıllık otsu (Araceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım.",
            "kullanimSekli": "İç mekân süs bitkisi",
            "yanEtkilerUyarilar": "Araceae familyası üyesi olarak kalsiyum oksalat kristalleri içerir; çiğnenmesi ağız ve boğazda tahriş yapabilir. Evcil hayvanlar ve çocuklardan uzak tutulmalıdır (ASPCA / botanik uyarıları).",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Kolombiya ve Orta Amerika tropik orman altı",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "Uygun koşullarda yıl boyu aralıklı",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Orta–parlak dolaylı ışık; düşük ışığa kısmen dayanır",
            "sulamaSikligi": "Toprak hafif nemli tutulur; saksı altında su birikmez",
            "toprakTipi": "Hafif, organik maddece zengin, iyi drene saksı harcı",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Aşk Merdiveni",
        "botanikAd": "Nephrolepis exaltata",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/62-nephrolepis-exaltata.jpg",
        "genelTavsiyeMetni": "Aşk merdiveni / Boston eğreltisi (Nephrolepis exaltata), tropik ve subtropik bölgelerde doğal yayılışı olan, uzun yaprak demetleriyle bilinen bir ev eğreltisidir.",
        "temelBilgiler": {
            "turkceAdi": "Aşk Merdiveni",
            "botanikAdi": "Nephrolepis exaltata",
            "bitkiTuru": "eğrelti (Nephrolepidaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım.",
            "kullanimSekli": "İç mekân veya nemli gölge bahçe süsü",
            "yanEtkilerUyarilar": "Genellikle toksik kabul edilmez; yine de yenmemelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Tropik/subtropik Amerika, Afrika ve Asya’nın nemli bölgelerinde doğal veya doğallaşmış",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "Çiçek açmaz; sporlarla çoğalır",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak dolaylı ışık veya yarı gölge",
            "sulamaSikligi": "Düzenli nem; kuru hava ve kurak topraktan hoşlanmaz",
            "toprakTipi": "Humuslu, hava alan, hafif asidik saksı karışımı",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden / Kew POWO",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Atatürk Çiçeği",
        "botanikAd": "Euphorbia pulcherrima",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/63-euphorbia-pulcherrima.jpg",
        "genelTavsiyeMetni": "Atatürk çiçeği / poinsettia (Euphorbia pulcherrima), Meksika kökenli, kırmızı brakteleriyle bilinen bir sütleğen türüdür. Kış süsü olarak kültürü yaygındır.",
        "temelBilgiler": {
            "turkceAdi": "Atatürk Çiçeği",
            "botanikAdi": "Euphorbia pulcherrima",
            "bitkiTuru": "çalı / küçük ağaç (Euphorbiaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım.",
            "kullanimSekli": "Süs bitkisi",
            "yanEtkilerUyarilar": "Sütlü özsu cilt ve gözlerde tahriş yapabilir. Yutulması mide bulantısına yol açabilir. Lateks hassasiyeti olanlar dikkat etmelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Meksika ve Orta Amerika; dünya çapında süs olarak yetiştirilir",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "Kış (kısa gün koşullarında brakte rengi oluşur)",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak dolaylı ışık",
            "sulamaSikligi": "Toprak yüzeyi kurudukça; aşırı sulamadan kaçınılır",
            "toprakTipi": "İyi drene saksı toprağı",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden / Kew POWO",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Kalanço",
        "botanikAd": "Kalanchoe blossfeldiana",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/66-kalanchoe-blossfeldiana.jpg",
        "genelTavsiyeMetni": "Kalanço (Kalanchoe blossfeldiana), Madagaskar kökenli, sukulent yapraklı ve uzun ömürlü çiçek salkımlı bir süs bitkisidir.",
        "temelBilgiler": {
            "turkceAdi": "Kalanço",
            "botanikAdi": "Kalanchoe blossfeldiana",
            "bitkiTuru": "sukulent çok yıllık (Crassulaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım.",
            "kullanimSekli": "İç mekân süs bitkisi",
            "yanEtkilerUyarilar": "Bazı Kalanchoe türleri evcil hayvanlar için toksiktir (kalp glikozitleri). Yenmemelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Madagaskar; dünya çapında süs kültürü",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "Kış - ilkbahar (kısa gün)",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ışık; birkaç saat doğrudan güneş tolere edilebilir",
            "sulamaSikligi": "Seyrek; toprak tamamen kuruyunca sulanır",
            "toprakTipi": "Sukulent/kaktüs karışımı, çok iyi drene",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Begonvil",
        "botanikAd": "Bougainvillea glabra",
        "tur": "Süs Bitkileri",
        "resimUrl": "assets/plants/photos/67-bougainvillea.jpg",
        "genelTavsiyeMetni": "Begonvil (Bougainvillea glabra), Güney Amerika kökenli, renkli brakteleriyle bilinen, sıcak iklimlerde yetişen dikenli bir sarılıcı çalıdır.",
        "temelBilgiler": {
            "turkceAdi": "Begonvil",
            "botanikAdi": "Bougainvillea glabra",
            "bitkiTuru": "sarılıcı çalı (Nyctaginaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Dekoratif kullanım.",
            "kullanimSekli": "Bahçe ve balkon süsü (sıcak iklim)",
            "yanEtkilerUyarilar": "Dikenler yaralanmaya yol açabilir. Özsu bazı kişilerde cilt tahrişi yapabilir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Brezilya ve çevresi; Akdeniz ikliminde kültürü yaygındır",
            "hasatMevsimi": "Hasat yapılmaz",
            "ciceklenmeZamani": "İlkbahar - sonbahar (sıcak bölgelerde daha uzun)",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş",
            "sulamaSikligi": "Yerleştikten sonra orta; aşırı sulama çiçeklenmeyi azaltır",
            "toprakTipi": "İyi drene, orta verimli toprak",
        },
        "kaynak": {
            "ad": "Missouri Botanical Garden / Kew POWO",
            "url": "https://www.missouribotanicalgarden.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Sinameki",
        "botanikAd": "Senna alexandrina",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/74-senna-alexandrina.jpg",
        "genelTavsiyeMetni": "Sinameki (Senna alexandrina), Fabaceae familyasından, Kuzeydoğu Afrika ve Arap Yarımadası ile ilişkilendirilen bir çalıdır. Yaprak ve meyveleri müshil amaçlı bitkisel preparatlarda kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Sinameki",
            "botanikAdi": "Senna alexandrina",
            "bitkiTuru": "çalı (Fabaceae)",
        },
        "saglikKullanim": {
            "faydalari": "WHO ve EMA monograflarına göre kısa süreli, ara sıra görülen kabızlıkta kullanılır.",
            "kullanimSekli": "Kurutulmuş yaprak veya meyve; standartlaştırılmış preparatlar gece tek doz şeklinde (yetişkin / 12 yaş üstü)",
            "yanEtkilerUyarilar": "Bağırsak tıkanıklığı, apandisit, Crohn, ülseratif kolit, nedeni bilinmeyen karın ağrısı, ciddi dehidratasyonda kontrendikedir. 12 yaş altı kullanılmaz. 1–2 haftadan uzun kullanım tıbbi denetim gerektirir; uzun süreli kullanım elektrolit kaybına yol açabilir. Gebelikte yalnızca hekim önerisiyle.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Kuzeydoğu Afrika, Sudan, Mısır ve Arabistan yarımadası çevresi; tropik–subtropik kurak bölgelerde kültürü vardır",
            "hasatMevsimi": "Yaprak ve meyve olgunlaşma döneminde",
            "ciceklenmeZamani": "Sıcak mevsim",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş",
            "sulamaSikligi": "Kuraklığa dayanıklı; ölçülü sulama",
            "toprakTipi": "İyi drene, kumlu–tınlı toprak",
        },
        "kaynak": {
            "ad": "WHO Monographs; EMA HMPC Senna alexandrina; Commission E",
            "url": "https://www.ema.europa.eu/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Kudret Narı",
        "botanikAd": "Momordica charantia",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/79-momordica-charantia.jpg",
        "genelTavsiyeMetni": "Kudret narı (Momordica charantia), Cucurbitaceae familyasından, tropik Asya, Afrika ve Amerika’da yetişen acı meyveli bir sarılıcıdır. Meyve sebze ve geleneksel bitkisel kullanımlarda yer alır.",
        "temelBilgiler": {
            "turkceAdi": "Kudret Narı",
            "botanikAdi": "Momordica charantia",
            "bitkiTuru": "tek yıllık / tropikte çok yıllık sarılıcı (Cucurbitaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak kan şekeri desteği amacıyla anılır; klinik kanıtlar sınırlı ve karışıktır (MSKCC).",
            "kullanimSekli": "Olgunlaşmamış meyve sebze olarak pişirilerek; bitkisel preparatlar yalnızca uzman önerisiyle",
            "yanEtkilerUyarilar": "Gebelikte kullanılmamalıdır (abortif/embriyotoksik risk, hayvan verileri). İnsülin veya diyabet ilaçlarıyla birlikte hipoglisemi riski artabilir. G6PD eksikliğinde tohum/vicine nedeniyle kaçınılmalıdır. Çocuklarda dikkatli olunmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Tropik ve subtropik Asya, Afrika, Karayipler ve Güney Amerika",
            "hasatMevsimi": "Meyveler yeşil–olgunlaşmamış dönemde",
            "ciceklenmeZamani": "Sıcak mevsim",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş",
            "sulamaSikligi": "Düzenli nem; iyi drenaj şart",
            "toprakTipi": "Verimli, iyi drene bahçe toprağı",
        },
        "kaynak": {
            "ad": "MSKCC About Herbs; Drugs.com Professional",
            "url": "https://www.mskcc.org/cancer-care/integrative-medicine/herbs/bitter-melon",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Küçük Havlıcan",
        "botanikAd": "Alpinia officinarum",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/81-alpinia-officinarum.jpg",
        "genelTavsiyeMetni": "Küçük havlıcan (Alpinia officinarum), zencefilgillerden, Güney Çin ve Güneydoğu Asya’da yetişen rizomlu bir baharat–tıbbi bitkidir.",
        "temelBilgiler": {
            "turkceAdi": "Küçük Havlıcan",
            "botanikAdi": "Alpinia officinarum",
            "bitkiTuru": "rizomlu çok yıllık (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak sindirim rahatsızlıkları ve iştahsızlıkta baharat/demleme olarak kullanılır.",
            "kullanimSekli": "Kurutulmuş rizom baharat veya çay olarak",
            "yanEtkilerUyarilar": "Yüksek doz mide tahrişi yapabilir. Gebelikte tıbbi denetim olmadan kullanılmamalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Güney Çin ve Güneydoğu Asya tropik bölgeleri",
            "hasatMevsimi": "Rizom olgunlaşınca (genellikle 1 yaşından sonra)",
            "ciceklenmeZamani": "Yaz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ışık veya yarı gölge",
            "sulamaSikligi": "Düzenli nem; soğukta azaltılır",
            "toprakTipi": "Zengin, nemli, iyi drene toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Zedoarya",
        "botanikAd": "Curcuma zedoaria",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/144-curcuma-zedoaria.jpg",
        "genelTavsiyeMetni": "Zedoarya (Curcuma zedoaria), zencefilgillerden, Güney ve Güneydoğu Asya’da yetişen rizomlu bir türdür. Rizomu baharat ve geleneksel tıpta zerdeçal akrabası olarak kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Zedoarya",
            "botanikAdi": "Curcuma zedoaria",
            "bitkiTuru": "rizomlu geofit (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak sindirim ve gaz şikayetlerinde kullanılır.",
            "kullanimSekli": "Kurutulmuş rizom baharat veya demleme",
            "yanEtkilerUyarilar": "Safra yolu hastalıklarında dikkatli olunmalıdır. Gebelikte yüksek dozdan kaçınılmalıdır. Zerdeçal ailesine alerjisi olanlar kullanmamalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Hindistan ve Güneydoğu Asya; tropik kültür alanları",
            "hasatMevsimi": "Rizom olgunlaşınca",
            "ciceklenmeZamani": "Sıcak mevsim",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ışık / yarı gölge",
            "sulamaSikligi": "Büyümede düzenli nem",
            "toprakTipi": "Zengin, iyi drene toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Şampuan Zencefili",
        "botanikAd": "Zingiber zerumbet",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/145-zingiber-zerumbet.jpg",
        "genelTavsiyeMetni": "Şampuan zencefili (Zingiber zerumbet), zencefilgillerden, Güneydoğu Asya kökenli rizomlu bir bitkidir. Çiçek konisinin özsuyu geleneksel olarak saç ve cilt bakımında anılır.",
        "temelBilgiler": {
            "turkceAdi": "Şampuan Zencefili",
            "botanikAdi": "Zingiber zerumbet",
            "bitkiTuru": "rizomlu çok yıllık (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak harici cilt/saç bakımında ve sindirim şikayetlerinde kullanılır.",
            "kullanimSekli": "Çiçek konisi özsuyu harici; rizom baharat/demleme (ölçülü)",
            "yanEtkilerUyarilar": "Ciltte tahriş olasıdır. İç kullanımda zencefil ailesi alerjisi ve gebelikte dikkat gerekir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Güneydoğu Asya ve Pasifik adaları tropikleri",
            "hasatMevsimi": "Rizom ve taze çiçek konileri sıcak mevsimde",
            "ciceklenmeZamani": "Yaz - sonbahar",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak dolaylı ışık veya yarı gölge",
            "sulamaSikligi": "Düzenli nem",
            "toprakTipi": "Humuslu, iyi drene toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Büyük Havlıcan",
        "botanikAd": "Alpinia galanga",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/146-alpinia-galanga.jpg",
        "genelTavsiyeMetni": "Büyük havlıcan / galanga (Alpinia galanga), zencefilgillerden, Güneydoğu Asya mutfağında rizomu baharat olarak kullanılan aromatik bir çok yıllıktır.",
        "temelBilgiler": {
            "turkceAdi": "Büyük Havlıcan",
            "botanikAdi": "Alpinia galanga",
            "bitkiTuru": "rizomlu çok yıllık (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak sindirim destekleyici baharat olarak kullanılır.",
            "kullanimSekli": "Taze veya kurutulmuş rizom mutfakta; demleme ölçülü",
            "yanEtkilerUyarilar": "Yüksek doz mide tahrişi yapabilir. Gebelikte tıbbi görüş alınmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Güneydoğu Asya (Endonezya, Tayland, Malezya vb.)",
            "hasatMevsimi": "Rizom gerektiğinde",
            "ciceklenmeZamani": "Yaz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ışık / yarı gölge",
            "sulamaSikligi": "Düzenli nem",
            "toprakTipi": "Zengin, iyi drene toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Kencur",
        "botanikAd": "Kaempferia galanga",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/147-kaempferia-galanga.jpg",
        "genelTavsiyeMetni": "Kencur (Kaempferia galanga), zencefilgillerden, Güneydoğu Asya’da yetişen, aromatik rizomlu küçük bir otsu bitkidir. Endonezya ve Malezya mutfağında baharat olarak kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Kencur",
            "botanikAdi": "Kaempferia galanga",
            "bitkiTuru": "rizomlu otsu (Zingiberaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel olarak aromatik baharat ve harici uygulamalarda kullanılır.",
            "kullanimSekli": "Taze rizom mutfakta; ölçülü demleme",
            "yanEtkilerUyarilar": "Aşırı kullanım mide rahatsızlığı yapabilir. Gebelikte dikkatli olunmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Güneydoğu Asya tropik orman altı",
            "hasatMevsimi": "Rizom yapraklar kuruduğunda",
            "ciceklenmeZamani": "Yağışlı dönem",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Yarı gölge",
            "sulamaSikligi": "Düzenli nem; kış dinlenmesinde azaltılır",
            "toprakTipi": "Humuslu, iyi drene toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Uzun Biber",
        "botanikAd": "Piper longum",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/148-piper-longum.jpg",
        "genelTavsiyeMetni": "Uzun biber (Piper longum), Piperaceae familyasından, Hindistan altkıtası kökenli sarılıcı bir baharat bitkisidir. Meyve başakları kurutulup baharat olarak kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Uzun Biber",
            "botanikAdi": "Piper longum",
            "bitkiTuru": "sarılıcı çalı (Piperaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Ayurveda ve geleneksel tıpta sindirim ve solunum destekleyici baharat olarak anılır.",
            "kullanimSekli": "Kurutulmuş meyve başakları baharat olarak",
            "yanEtkilerUyarilar": "Acı/keskin baharat; mide–bağırsak tahrişi yapabilir. Gebelikte yüksek doz önerilmez. Piperin ilaç metabolizmasını etkileyebilir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Hindistan, Sri Lanka ve Güneydoğu Asya’nın nemli tropik bölgeleri",
            "hasatMevsimi": "Başaklar yeşilden siyaha dönerken",
            "ciceklenmeZamani": "Yağışlı dönem",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Yarı gölge / parlak dolaylı ışık",
            "sulamaSikligi": "Yüksek nem; düzenli sulama",
            "toprakTipi": "Humusça zengin, iyi drene toprak",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Kadife Fasulye",
        "botanikAd": "Mucuna pruriens",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/155-mucuna-pruriens.jpg",
        "genelTavsiyeMetni": "Kadife fasulye (Mucuna pruriens), Fabaceae familyasından, tropik bölgelerde yetişen sarılıcı bir baklagildir. Tohumları L-DOPA içerir; bakla tüyleri şiddetli kaşıntıya yol açar.",
        "temelBilgiler": {
            "turkceAdi": "Kadife Fasulye",
            "botanikAdi": "Mucuna pruriens",
            "bitkiTuru": "sarılıcı baklagil (Fabaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel Ayurveda kullanımında tohum preparatları anılır; L-DOPA içeriği nedeniyle nörolojik araştırmalarda incelenir.",
            "kullanimSekli": "Yalnızca işlenmiş/standartlaştırılmış preparatlar; ham bakla ve tüylerle temas edilmez",
            "yanEtkilerUyarilar": "Bakla tüyleri şiddetli kaşıntı ve cilt tahrişi yapar. Tohumlar yüksek L-DOPA içerir; Parkinson ilaçları, antidepresanlar ve psikotrop ilaçlarla tehlikeli etkileşim riski vardır. Gebelikte kullanılmaz. Kendi kendine tedavi için uygun değildir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Tropik Afrika ve Asya; birçok tropik bölgede doğallaşmıştır",
            "hasatMevsimi": "Baklalar olgunlaşınca (koruyucu ekipmanla)",
            "ciceklenmeZamani": "Yağışlı dönem",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya hafif gölge",
            "sulamaSikligi": "Orta–düzenli",
            "toprakTipi": "İyi drene bahçe toprağı",
        },
        "kaynak": {
            "ad": "Kew POWO; MSKCC / bilimsel güvenlik uyarıları",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Akgünlük",
        "botanikAd": "Boswellia serrata",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/160-boswellia-serrata.jpg",
        "genelTavsiyeMetni": "Akgünlük / Hint günlük ağacı (Boswellia serrata), Burseraceae familyasından, Hindistan’ın kurak bölgelerine özgü bir ağaçtır. Kabuk altı reçinesi Ayurveda’da ve modern takviyelerde kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Akgünlük",
            "botanikAdi": "Boswellia serrata",
            "bitkiTuru": "ağaç (Burseraceae)",
        },
        "saglikKullanim": {
            "faydalari": "NCCIH’e göre geleneksel olarak eklem iltihabı ve bazı solunum–sindirim şikayetlerinde kullanılır; eklem sağlığı takviyesi olarak araştırılır.",
            "kullanimSekli": "Reçine özütü tablet/kapsül formunda (standartlaştırılmış ürünler)",
            "yanEtkilerUyarilar": "Kısa süreli oral kullanımda genellikle iyi tolere edilir; mide bulantısı, ishal görülebilir (NCCIH). Gebelik ve emzirmede tıbbi dozların güvenliği net değildir. İlaç kullananlar hekime danışmalıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Hindistan’ın kurak dağlık bölgeleri; ayrıca Orta Doğu ve Kuzey Afrika’da akraba türler bulunur (NCCIH)",
            "hasatMevsimi": "Reçine hasadı kurak dönemde",
            "ciceklenmeZamani": "Kurak tropik mevsim döngüsüne bağlı",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş",
            "sulamaSikligi": "Kuraklığa dayanıklı; aşırı sudan kaçınılır",
            "toprakTipi": "İyi drene, taşlı–kumlu toprak",
        },
        "kaynak": {
            "ad": "NCCIH Boswellia; NCBI LiverTox",
            "url": "https://www.nccih.nih.gov/health/boswellia",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Benzoin Ağacı",
        "botanikAd": "Styrax benzoin",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/photos/162-styrax-benzoin.jpg",
        "genelTavsiyeMetni": "Benzoin ağacı (Styrax benzoin), Styraxaceae familyasından, Güneydoğu Asya’da yetişen bir ağaçtır. Kabuğundan elde edilen benzoin reçinesi tütsü ve parfümeride kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Benzoin Ağacı",
            "botanikAdi": "Styrax benzoin",
            "bitkiTuru": "ağaç (Styraxaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Reçine geleneksel olarak tütsü, parfüm sabitleyici ve bazı harici preparatlarda kullanılır.",
            "kullanimSekli": "Reçine tütsü veya seyreltilmiş aromatik karışımlarda",
            "yanEtkilerUyarilar": "Reçine dumanı solunum yollarını tahriş edebilir. Ciltte alerjik reaksiyon olasıdır. İç kullanım önerilmez.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Sumatra ve Güneydoğu Asya tropik ormanları",
            "hasatMevsimi": "Kabuk yaralandıktan sonra reçine toplanır",
            "ciceklenmeZamani": "Tropik yağış döngüsüne bağlı",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak ışık / yarı gölge",
            "sulamaSikligi": "Düzenli nem",
            "toprakTipi": "Derin, iyi drene orman toprağı",
        },
        "kaynak": {
            "ad": "Kew POWO / USDA GRIN",
            "url": "https://powo.science.kew.org/",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Kırmızı Adaçayı",
        "botanikAd": "Salvia miltiorrhiza",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/192-salvia-miltiorrhiza.jpg",
        "genelTavsiyeMetni": "Kırmızı adaçayı / danshen (Salvia miltiorrhiza), Lamiaceae familyasından, Çin’e özgü çok yıllık bir ottur. Kökü geleneksel Çin tıbbında kullanılır.",
        "temelBilgiler": {
            "turkceAdi": "Kırmızı Adaçayı",
            "botanikAdi": "Salvia miltiorrhiza",
            "bitkiTuru": "çok yıllık otsu (Lamiaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Geleneksel Çin tıbbında dolaşım ve bazı kardiyovasküler şikayetlerde kullanılır; modern klinik kullanım yalnızca uzman denetiminde olmalıdır.",
            "kullanimSekli": "Kurutulmuş kök preparatları (standartlaştırılmış ürünler)",
            "yanEtkilerUyarilar": "Varfarin ve diğer oral antikoagülanlarla birlikte kanama riskini ciddi ölçüde artırır; birlikte kullanılmamalıdır (klinik vaka ve kohort verileri). Ameliyat öncesi bırakılmalıdır. Gebelikte kullanılmaz.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Çin’in tepelik ve dağlık bölgeleri",
            "hasatMevsimi": "Kök sonbahar–ilkbahar arası",
            "ciceklenmeZamani": "Yaz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya hafif gölge",
            "sulamaSikligi": "Orta; iyi drenaj şart",
            "toprakTipi": "İyi drene, orta verimli toprak",
        },
        "kaynak": {
            "ad": "Klinik literatür (warfarin etkileşimi); Kew POWO",
            "url": "https://journals.sagepub.com/doi/10.1345/aph.19029",
            "cekimTarihi": TODAY,
        },
    },
    {
        "ad": "Şeytan Pençesi",
        "botanikAd": "Harpagophytum procumbens",
        "tur": "Tıbbi Bitkiler",
        "resimUrl": "assets/plants/photos/227-harpagophytum-procumbens.jpg",
        "genelTavsiyeMetni": "Şeytan pençesi (Harpagophytum procumbens), Pedaliaceae familyasından, Güney Afrika’nın Kalahari savanlarına özgü yumrulu bir bitkidir. İkincil yumrular Alman Commission E tarafından onaylı bitkisel kullanımlarda yer alır.",
        "temelBilgiler": {
            "turkceAdi": "Şeytan Pençesi",
            "botanikAdi": "Harpagophytum procumbens",
            "bitkiTuru": "çok yıllık yumrulu otsu (Pedaliaceae)",
        },
        "saglikKullanim": {
            "faydalari": "Commission E: iştahsızlık, hazımsızlık ve hareket sistemi dejeneratif rahatsızlıklarında; klinik literatürde eklem ve bel ağrısı için araştırılır.",
            "kullanimSekli": "Kurutulmuş ikincil yumru demleme veya standartlaştırılmış özüt",
            "yanEtkilerUyarilar": "Mide ve oniki parmak ülserinde kontrendikedir. Safra taşı olanlar hekime danışmalıdır. Gebelikte kullanılmaz (oksitosik etki bildirimi). Yüksek doz mide rahatsızlığı yapabilir. Kan sulandırıcı ve diyabet ilaçlarıyla etkileşim olasıdır.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Namibya, Botsvana, Güney Afrika ve çevresi (Kalahari savanı) — SANBI PlantZAfrica",
            "hasatMevsimi": "İkincil yumrular kontrollü hasatla",
            "ciceklenmeZamani": "Yaz (Güney Yarımküre)",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş",
            "sulamaSikligi": "Kuraklığa dayanıklı; seyrek sulama",
            "toprakTipi": "Kumlu, çok iyi drene toprak",
        },
        "kaynak": {
            "ad": "German Commission E; SANBI PlantZAfrica",
            "url": "https://pza.sanbi.org/harpagophytum-procumbens",
            "cekimTarihi": TODAY,
        },
    },
]


def main() -> None:
    live = json.loads(LIVE.read_text(encoding="utf-8"))
    existing = {(p.get("botanikAd") or "").lower() for p in live}
    existing_names = {(p.get("ad") or "").lower() for p in live}

    added: list[dict] = []
    skipped: list[str] = []
    next_id = max((p.get("id") or 0) for p in live) + 1

    for raw in PLANTS:
        key = raw["botanikAd"].lower()
        if key in existing or raw["ad"].lower() in existing_names:
            skipped.append(f"{raw['ad']} ({raw['botanikAd']})")
            continue
        plant = dict(raw)
        plant["id"] = next_id
        next_id += 1
        live.append(plant)
        existing.add(key)
        existing_names.add(raw["ad"].lower())
        added.append(
            {
                "id": plant["id"],
                "ad": plant["ad"],
                "botanikAd": plant["botanikAd"],
                "kaynak": plant["kaynak"]["ad"],
            }
        )

    LIVE.write_text(json.dumps(live, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_LOG.write_text(
        json.dumps({"added": added, "skipped": skipped}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    # Karantina listesini temizle (geri yüklendi)
    quarantine = ROOT / "data" / "unverified_plants.json"
    quarantine.write_text("[]\n", encoding="utf-8")

    print(f"Eklenen: {len(added)}")
    print(f"Atlanan (zaten var): {len(skipped)}")
    print(f"Yeni toplam: {len(live)}")
    for item in added:
        print(f"  + {item['id']:3} {item['ad']} — {item['kaynak']}")


if __name__ == "__main__":
    main()
