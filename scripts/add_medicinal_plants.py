# -*- coding: utf-8 -*-
"""Sifali bitki kayitlarini plants.json dosyasina ekler."""

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "data" / "plants.json"


def ascii_tr(text: str) -> str:
    replacements = {
        "ı": "i",
        "İ": "I",
        "ğ": "g",
        "Ğ": "G",
        "ü": "u",
        "Ü": "U",
        "ş": "s",
        "Ş": "S",
        "ö": "o",
        "Ö": "O",
        "ç": "c",
        "Ç": "C",
        "â": "a",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def normalize(value):
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, str):
        return ascii_tr(value)
    return value


NEW_PLANTS = [
    {
        "id": 13,
        "ad": "Zencefil",
        "botanikAd": "Zingiber officinale",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Zencefil, tropikal kokenli rizomlu bir bitkidir ve geleneksel mutfak ile bitkisel demlemelerde sik kullanilir. Sicak cay olarak tuketildiginde ferahlik hissi verebilir; mide rahatsizliklari ve soguk havalarda destekleyici bir secenek olarak anilir.",
        "temelBilgiler": {
            "turkceAdi": "Zencefil",
            "botanikAdi": "Zingiber officinale",
            "bitkiTuru": "Cok yillik rizomlu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Mide bulantisini hafifletmeye yardimci olabilir, sindirimi destekleyebilir ve soguk alginligi semptomlarinda sicak demleme olarak tercih edilir.",
            "kullanimSekli": "Taze rizom dilimleri sicak suda demlenir; kurutulmus zencefil tozu cay veya yemeklerde kullanilir.",
            "yanEtkilerUyarilar": "Yuksek dozda mide tahrisi yapabilir. Kan sulandirici ilac kullananlar ve safra tasi olanlar uzman gorusu almalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Guney Asya kokenli; tropikal ve sicak nemli iklimlerde, seralarda yetistirilir.",
            "hasatMevsimi": "Dikimden 8-10 ay sonra rizom hasadi",
            "ciceklenmeZamani": "Uygun tropikal kosullarda yaz donemi",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Parlak dolayli isik veya yari gunes",
            "sulamaSikligi": "Toprak nemli tutulmali, su birikimi olmamali",
            "toprakTipi": "Humuslu, gevsek ve iyi drene olan toprak",
        },
    },
    {
        "id": 14,
        "ad": "Zerdecal",
        "botanikAd": "Curcuma longa",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Zerdecal, parlak sari rizomuyla bilinen ve mutfakta baharat olarak yaygin kullanilan sifali bir bitkidir. Kurkumin icerigi nedeniyle antioksidan ve antienflamatuvar ozellikleriyle anilir; sicak sut veya yemek karisimlarinda degerlendirilir.",
        "temelBilgiler": {
            "turkceAdi": "Zerdecal",
            "botanikAdi": "Curcuma longa",
            "bitkiTuru": "Cok yillik rizomlu baharat ve tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Eklem rahatsizliklarinda destekleyici kullanimi yaygindir; antioksidan etkisiyle bilinir ve sindirim destekleyici demlemelerde yer alir.",
            "kullanimSekli": "Kurutulmus toz formunda baharat veya sicak icecek olarak; yag ve karabiber ile birlikte emilimi artabilir.",
            "yanEtkilerUyarilar": "Safra kesesi sorunu olanlarda dikkatli kullanilmalidir. Hamilelikte yuksek doz onerilmez; ilac etkilesimi icin uzmana danisilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Hindistan ve Guneydogu Asya baslica uretim bolgeleridir; sicak nemli iklim ister.",
            "hasatMevsimi": "Yapraklar kurudugunda rizom hasadi (yaklasik 7-10 ay)",
            "ciceklenmeZamani": "Sicak mevsimlerde",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Bol gunes veya yari gunes",
            "sulamaSikligi": "Buyume doneminde duzenli nem; kislik dinlenmede azaltilir",
            "toprakTipi": "Organik maddece zengin, nemli ama drenajli toprak",
        },
    },
    {
        "id": 15,
        "ad": "Ekinezya",
        "botanikAd": "Echinacea purpurea",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Ekinezya, Kuzey Amerika kokenli cicekli bir tibbi bitkidir ve bagisiklik destegi amaciyla geleneksel kullanimi yaygindir. Bahcelerde sus degeri yuksek pembe-mor cicekleriyle de tercih edilir.",
        "temelBilgiler": {
            "turkceAdi": "Ekinezya",
            "botanikAdi": "Echinacea purpurea",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Bagisiklik sistemini destekleyici etkisiyle anilir; soguk alginligi donemlerinde bitki cayi veya ekstrakt olarak kullanilabilir.",
            "kullanimSekli": "Kurutulmus cicek ve kokleri demlenerek cay yapilir; standartlastirilmis ekstrakt formlari da bulunur.",
            "yanEtkilerUyarilar": "Aster familyasina alerjisi olanlarda risk vardir. Otoimmun hastaligi olanlar ve surekli ilac kullananlar uzman kontrolunde kullanmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Kuzey Amerika kokenli; Turkiye ve Avrupa bahcelerinde kultur bitkisi olarak yetisir.",
            "hasatMevsimi": "Cicekler yaz ortasinda, kokler sonbaharda",
            "ciceklenmeZamani": "Haziran - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Yerlesik bitkide orta duzey; asiri sulamadan kacinilir",
            "toprakTipi": "Iyi drene, hafif kumlu veya tinli toprak",
        },
    },
    {
        "id": 16,
        "ad": "Rezene",
        "botanikAd": "Foeniculum vulgare",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Rezene, anason benzeri tatli aromasiyla bilinen maydanozgiller familyasindan sifali bir bitkidir. Tohumlari demlenerek gaz ve sindirim rahatsizliklarinda geleneksel olarak kullanilir.",
        "temelBilgiler": {
            "turkceAdi": "Rezene",
            "botanikAdi": "Foeniculum vulgare",
            "bitkiTuru": "Cok yillik otsu aromatik tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Sindirim sistemini rahatlatmaya, gaz ve siskinligi azaltmaya yardimci olabilir; tatlamsı aromasiyla demlemelerde tercih edilir.",
            "kullanimSekli": "Olgun tohumlar ezilerek sicak suda demlenir; taze yapraklari salata ve yemeklerde kullanilabilir.",
            "yanEtkilerUyarilar": "Hamilelikte yogun kullanimda dikkat edilmelidir. Ostrojen benzeri etki potansiyeli nedeniyle hormon duyarli durumlarda uzmana danisilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz havzasi, Anadolu ve iliman iklimli bircok bolge",
            "hasatMevsimi": "Yaz sonu tohum hasadi",
            "ciceklenmeZamani": "Temmuz - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Olculu; kurakliga oldukca dayanikli",
            "toprakTipi": "Gevsek, kumlu-tinli ve drenajli toprak",
        },
    },
    {
        "id": 17,
        "ad": "Melisa",
        "botanikAd": "Melissa officinalis",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Melisa (Ogulotu), limonumsu ferah kokusuyla bilinen ballibabagiller familyasindan yatistirici bir sifali bitkidir. Aksam demlemelerinde rahatlama amaciyla sik tercih edilir.",
        "temelBilgiler": {
            "turkceAdi": "Melisa (Ogulotu)",
            "botanikAdi": "Melissa officinalis",
            "bitkiTuru": "Cok yillik otsu tibbi ve aromatik bitki",
        },
        "saglikKullanim": {
            "faydalari": "Stres hissini azaltmaya ve uyku kalitesini desteklemeye yardimci olabilir; hafif sindirim rahatligi da saglayabilir.",
            "kullanimSekli": "Taze veya kurutulmus yapraklar sicak suda demlenerek cay yapilir.",
            "yanEtkilerUyarilar": "Tiroid ilaci kullananlar dikkatli olmalidir. Asiri tuketimden kacinilmali; hamilelikte uzmana danisilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Guney Avrupa, Akdeniz ve Anadolu bahcelerinde yaygin",
            "hasatMevsimi": "Ilkbahar sonundan sonbahara yaprak hasadi",
            "ciceklenmeZamani": "Haziran - Agustos",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Yari gunes veya aydinlik golge",
            "sulamaSikligi": "Toprak hafif nemli tutulacak sekilde duzenli sulama",
            "toprakTipi": "Humuslu, nem tutan ve drenajli bahce topragi",
        },
    },
    {
        "id": 18,
        "ad": "Isirgan Otu",
        "botanikAd": "Urtica dioica",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Isirgan otu, yakici tuyleriyle bilinen ancak kurutulup demlendiginde geleneksel sifali kullanimi genis bir bitkidir. Mineral zenginligi nedeniyle bahar demlemelerinde ve destekleyici bitki caylarinda yer alir.",
        "temelBilgiler": {
            "turkceAdi": "Isirgan Otu",
            "botanikAdi": "Urtica dioica",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Mineral destegi sunabilir, eklem rahatsizliklarinda geleneksel kullanimi vardir ve sac-cilt bakiminda haricen degerlendirilebilir.",
            "kullanimSekli": "Genc yapraklar kaynatilarak cay veya corba yapilir; kurutulmus yaprak demlenir.",
            "yanEtkilerUyarilar": "Taze bitki cilde temasinda yakici etki yapar. Bobrek veya ilac kullananlar uzman gorusu almalidir; asiri tuketimden kacinilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Nemli tarla kenarlari, orman acikliklari ve Anadolu genelinde yaygin",
            "hasatMevsimi": "Ilkbahar ve yaz basi taze yaprak",
            "ciceklenmeZamani": "Haziran - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Yari gunes veya golge",
            "sulamaSikligi": "Nemli toprak; kurakliga hassas",
            "toprakTipi": "Azotca zengin, nemli ve humuslu toprak",
        },
    },
    {
        "id": 19,
        "ad": "Civanpercemi",
        "botanikAd": "Achillea millefolium",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Civanpercemi, ince yapraklari ve semsiye seklinde cicekleriyle bilinen geleneksel bir sifali bitkidir. Halk hekimliginde yara bakimi ve adet donemi rahatsizliklarinda adi gecen bitkiler arasindadir.",
        "temelBilgiler": {
            "turkceAdi": "Civanpercemi",
            "botanikAdi": "Achillea millefolium",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Yara iyilesmesini destekleyici harici kullanimlari vardir; sindirim ve adet rahatsizliklarinda geleneksel demleme olarak kullanilabilir.",
            "kullanimSekli": "Cicekli ust kisimler kurutularak cay yapilir; haricen kompres uygulanabilir.",
            "yanEtkilerUyarilar": "Papatyagiller alerjisi olanlarda reaksiyon riski vardir. Hamilelikte ic kullanimi onerilmez.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Cayirlar, yol kenarlari ve iliman iklimli Anadolu yaylalari",
            "hasatMevsimi": "Ciceklenme doneminde ust kisimlar",
            "ciceklenmeZamani": "Haziran - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Kurakliga dayanikli; seyrek sulama",
            "toprakTipi": "Zayif, tasli veya kumlu iyi drene toprak",
        },
    },
    {
        "id": 20,
        "ad": "Hatmi Cicegi",
        "botanikAd": "Althaea officinalis",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Hatmi cicegi, yuksek musilaj icerigiyle bilinen yumusatici bir sifali bitkidir. Bogaz ve solunum yolu rahatsizliklarinda demleme olarak geleneksel kullanimi yaygindir.",
        "temelBilgiler": {
            "turkceAdi": "Hatmi Cicegi",
            "botanikAdi": "Althaea officinalis",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Bogaz tahrisini yumusatmaya yardimci olabilir; kuru oksuruk ve solunum yolu konforunda destekleyici demleme olarak kullanilir.",
            "kullanimSekli": "Cicek veya kok soguk/ilik suda bekletilerek veya demlenerek tuketilir.",
            "yanEtkilerUyarilar": "Ilac emilimini geciktirebilecegi icin diger ilaclarla ayni anda alinmamalidir. Diabet hastalari uzmana danismalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Nemli cayirlar, nehir kenarlari ve iliman Avrupa-Anadolu bolgeleri",
            "hasatMevsimi": "Yaz aylarinda cicek, sonbaharda kok",
            "ciceklenmeZamani": "Temmuz - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes veya yari gunes",
            "sulamaSikligi": "Duzenli; nemli toprak sever",
            "toprakTipi": "Nemli, verimli ve derin bahce topragi",
        },
    },
    {
        "id": 21,
        "ad": "Anason",
        "botanikAd": "Pimpinella anisum",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Anason, Gudul Sifali Bitkiler Rehberi ve Anadolu tariminda bilinen maydanozgiller familyasindan aromatik bir bitkidir. Meyveleri cay olarak demlendiginde gaz sancilarina ve soguk alginligina iyi geldigi geleneksel olarak belirtilir.",
        "temelBilgiler": {
            "turkceAdi": "Anason",
            "botanikAdi": "Pimpinella anisum",
            "bitkiTuru": "Tek yillik aromatik tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Gaz sancilarini hafifletmeye, sindirimi desteklemeye ve sakinlestirici demleme deneyimi sunmaya yardimci olabilir.",
            "kullanimSekli": "Olgun meyveler (tohumlar) demlenerek bitki cayi yapilir; baharat olarak da kullanilir.",
            "yanEtkilerUyarilar": "Yuksek dozda alerjik reaksiyon nadiren gorulebilir. Hamilelikte olculu kullanilmali; uzmana danisilmasi uygundur.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Turkiye'de Burdur, Ege, Bati Akdeniz ve Goller yoresi baslica uretim alanlaridir.",
            "hasatMevsimi": "Temmuz - Agustos",
            "ciceklenmeZamani": "Haziran - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Cikis ve ciceklenmeye kadar duzenli; olgunlasmada kuru hava tercih edilir",
            "toprakTipi": "Iyi drene, tinli ve orta verimli toprak",
        },
    },
    {
        "id": 22,
        "ad": "Corekotu",
        "botanikAd": "Nigella sativa",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Corekotu, siyah tohumlariyla bilinen ve Anadolu mutfagi ile geleneksel sifada onemli yeri olan bir bitkidir. Tohum yagi ve baharat formu yaygin kullanilir.",
        "temelBilgiler": {
            "turkceAdi": "Corekotu",
            "botanikAdi": "Nigella sativa",
            "bitkiTuru": "Tek yillik otsu tibbi ve baharat bitkisi",
        },
        "saglikKullanim": {
            "faydalari": "Bagisiklik destegi ve solunum yolu rahatsizliklarinda geleneksel kullanimi vardir; antioksidan ozellikleriyle anilir.",
            "kullanimSekli": "Tohumlar baharat olarak veya yag formunda olculu miktarda tuketilir.",
            "yanEtkilerUyarilar": "Yuksek doz yag tuketimi rahatsizlik verebilir. Hamilelikte ve kronik hastalarda uzman gorusu alinmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Guneybati Asya, Akdeniz ve Anadolu tarim alanlari",
            "hasatMevsimi": "Yaz ortasi tohum hasadi",
            "ciceklenmeZamani": "Mayis - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Orta duzey; asiri nemden kacinilir",
            "toprakTipi": "Hafif, kumlu-tinli ve drenajli toprak",
        },
    },
    {
        "id": 23,
        "ad": "Kusburnu",
        "botanikAd": "Rosa canina",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Kusburnu, yabani gulun C vitamini zengin meyveleridir. Kurutularak cay yapiminda kullanilir; kis aylarinda bagisiklik destegi amaciyla geleneksel demlemelerde yer alir.",
        "temelBilgiler": {
            "turkceAdi": "Kusburnu",
            "botanikAdi": "Rosa canina",
            "bitkiTuru": "Cok yillik cali; tibbi meyve",
        },
        "saglikKullanim": {
            "faydalari": "Yuksek C vitamini icerigiyle bagisiklik destekleyici olarak anilir; antioksidan demleme olarak tercih edilir.",
            "kullanimSekli": "Kurutulmus meyveler kirilarak veya butun halde sicak suda demlenir.",
            "yanEtkilerUyarilar": "Asiri tuketim mide hassasiyeti yapabilir. Tohum killari bogaz tahrisine yol acabilecegi icin suzulerek icilmelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Avrupa ve Anadolu orman kenarlari, yamaclar ve kirsal alanlar",
            "hasatMevsimi": "Sonbahar (Eylul - Kasim)",
            "ciceklenmeZamani": "Mayis - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes veya yari gunes",
            "sulamaSikligi": "Yerlesik bitkide orta; kurakliga dayanikli",
            "toprakTipi": "Cogu toprakta yetisir; drenajli bahce topragi",
        },
    },
    {
        "id": 24,
        "ad": "Aynisafa",
        "botanikAd": "Calendula officinalis",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Aynisafa (portakal nergisi), Gudul Sifa Yolu rehberinde de yer alan, sari-turuncu cicekleriyle bilinen sifali bir bitkidir. Cilt bakiminda merhem ve yara iyilesmesini destekleyici harici kullanimlari yaygindir.",
        "temelBilgiler": {
            "turkceAdi": "Aynisafa",
            "botanikAdi": "Calendula officinalis",
            "bitkiTuru": "Tek yillik otsu tibbi ve sus bitkisi",
        },
        "saglikKullanim": {
            "faydalari": "Cilt tahrislerinde rahatlatici etki gosterebilir; yara iyilesmesini destekleyici harici kullanimi ve sindirim rahatligi icin demleme olarak anilir.",
            "kullanimSekli": "Ciceklerden cay, yag veya merhem hazirlanir; haricen kompres uygulanabilir.",
            "yanEtkilerUyarilar": "Papatyagiller alerjisi olanlarda dikkatli kullanilmalidir. Ic kullanimda hamilelikte uzman gorusu alinmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz kokenli; bahcelerde ve tarla kenarlarinda kultur bitkisi olarak yetisir.",
            "hasatMevsimi": "Ciceklenme boyunca haftalik cicek hasadi",
            "ciceklenmeZamani": "Mayis - Ekim",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Duzenli; ciceklenme doneminde nem destegi",
            "toprakTipi": "Iyi drene, secici olmayan bahce topragi (pH 4.5-8.5)",
        },
    },
    {
        "id": 25,
        "ad": "Sari Kantaron",
        "botanikAd": "Hypericum perforatum",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Sari kantaron, yaz aylarinda acan sari cicekleriyle bilinen ve ruh hali destegi amaciyla geleneksel kullanimi olan bir sifali bitkidir. Ilac etkilesimleri nedeniyle dikkatli kullanimi sarttir.",
        "temelBilgiler": {
            "turkceAdi": "Sari Kantaron",
            "botanikAdi": "Hypericum perforatum",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Hafif ruh hali dusuklugunde destekleyici kullanimi arastirilmistir; haricen yag olarak kas ve cilt bakiminda da degerlendirilir.",
            "kullanimSekli": "Cicekli ust kisimler demlenerek cay veya yag maserasyonu yapilir.",
            "yanEtkilerUyarilar": "Cok sayida ilacla etkilesime girer (antidepresan, dogum kontrol, kan sulandirici vb.). Mutlaka hekim onayi ile kullanilmalidir; gunes hassasiyeti artabilir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Avrupa, Anadolu cayir ve yol kenarlari",
            "hasatMevsimi": "Ciceklenme donemi (Haziran - Temmuz)",
            "ciceklenmeZamani": "Haziran - Agustos",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Kurakliga dayanikli; seyrek sulama",
            "toprakTipi": "Kumlu, tasli ve iyi drene toprak",
        },
    },
    {
        "id": 26,
        "ad": "Cemen",
        "botanikAd": "Trigonella foenum-graecum",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Cemen, baklagiller familyasindan tohumlari baharat ve geleneksel sifada kullanilan bir bitkidir. Anadolu mutfaginda cemen pasta ve baharat karisimlarinda yer alir.",
        "temelBilgiler": {
            "turkceAdi": "Cemen",
            "botanikAdi": "Trigonella foenum-graecum",
            "bitkiTuru": "Tek yillik baklagil tibbi ve baharat bitkisi",
        },
        "saglikKullanim": {
            "faydalari": "Sindirim destegi ve ishtah acici etkisiyle anilir; geleneksel olarak kan sekeri yonetiminde de adi gecer.",
            "kullanimSekli": "Tohumlar baharat olarak ogutulur veya demlenerek cay yapilir.",
            "yanEtkilerUyarilar": "Hamilelikte yuksek doz onerilmez. Diabet ilaci kullananlar hekim kontrolunde kullanmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz, On Asya ve Anadolu tarim alanlari; kuraga dayanikli",
            "hasatMevsimi": "Yaz ortasi bakla ve tohum hasadi",
            "ciceklenmeZamani": "Nisan - Haziran",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Orta; kurakliga dayanikli",
            "toprakTipi": "Iyi drene, hafif alkali veya notr toprak",
        },
    },
    {
        "id": 27,
        "ad": "Kimyon",
        "botanikAd": "Cuminum cyminum",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Kimyon, maydanozgiller familyasindan tohumlari baharat olarak kullanilan aromatik bir bitkidir. Anadolu ve Ortadogu mutfaginda sindirim destekleyici baharat olarak yaygindir.",
        "temelBilgiler": {
            "turkceAdi": "Kimyon",
            "botanikAdi": "Cuminum cyminum",
            "bitkiTuru": "Tek yillik aromatik baharat bitkisi",
        },
        "saglikKullanim": {
            "faydalari": "Sindirimi kolaylastirmaya ve gaz rahatsizliklarini azaltmaya yardimci olabilir; yemeklere aroma katar.",
            "kullanimSekli": "Kurutulmus tohumlar baharat olarak veya demlenerek kullanilir.",
            "yanEtkilerUyarilar": "Yuksek miktarda tuketim mide hassasiyeti yapabilir. Alerji oykusu olanlar dikkatli olmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz, Ortadogu ve sicak kurak iklimli tarim bolgeleri",
            "hasatMevsimi": "Yaz ortasi tohum hasadi",
            "ciceklenmeZamani": "Haziran - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Olculu; asiri sudan kacinilir",
            "toprakTipi": "Kumlu-tinli, iyi drene toprak",
        },
    },
    {
        "id": 28,
        "ad": "Kisnis",
        "botanikAd": "Coriandrum sativum",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Kisnis, hem taze yapraklari (kisnis yesilligi) hem de kuru tohumlariyla mutfakta ve geleneksel sifada kullanilan aromatik bir bitkidir.",
        "temelBilgiler": {
            "turkceAdi": "Kisnis",
            "botanikAdi": "Coriandrum sativum",
            "bitkiTuru": "Tek yillik aromatik bitki",
        },
        "saglikKullanim": {
            "faydalari": "Sindirim rahatligi, ishtah destegi ve yemeklerde ferah aroma saglar.",
            "kullanimSekli": "Taze yapraklar salata ve yemeklerde; tohumlar baharat veya cay olarak kullanilir.",
            "yanEtkilerUyarilar": "Nadiren alerjik reaksiyon gorulebilir. Olculu tuketim tercih edilmelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz, Ortadogu ve iliman iklimli bahceler",
            "hasatMevsimi": "Yapraklar surekli; tohumlar yaz ortasi",
            "ciceklenmeZamani": "Haziran - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes veya yari gunes",
            "sulamaSikligi": "Duzenli; toprak tamamen kurumamali",
            "toprakTipi": "Gevsek, verimli ve drenajli toprak",
        },
    },
    {
        "id": 29,
        "ad": "Defne",
        "botanikAd": "Laurus nobilis",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Defne, Akdeniz ikliminin klasik yaprak dokmeyen aromatik agaci/calisidir. Yapraklari yemeklerde aroma icin kullanilir; geleneksel demlemelerde de adi gecer.",
        "temelBilgiler": {
            "turkceAdi": "Defne",
            "botanikAdi": "Laurus nobilis",
            "bitkiTuru": "Yaprak dokmeyen aromatik agac/cali",
        },
        "saglikKullanim": {
            "faydalari": "Sindirim destekleyici yemek aromasi sunar; geleneksel olarak metabolizma ve solunum rahatligiyla iliskilendirilir.",
            "kullanimSekli": "Kurutulmus yapraklar yemeklerde veya sinirli sayida demlenerek kullanilir.",
            "yanEtkilerUyarilar": "Buyuk miktarda yaprak tuketimi uygun degildir. Hamilelikte yogun demlemeden kacinilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz kiyilari, Ege ve Guney Anadolu",
            "hasatMevsimi": "Yil boyu yaprak; en aromatik donem yaz",
            "ciceklenmeZamani": "Mart - Mayis",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes veya yari gunes",
            "sulamaSikligi": "Yerlesik bitkide orta; kurakliga dayanikli",
            "toprakTipi": "Iyi drene, hafif kirecli toprak",
        },
    },
    {
        "id": 30,
        "ad": "Meyan Koku",
        "botanikAd": "Glycyrrhiza glabra",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Meyan koku, tatlamsı aromasiyla bilinen ve bogaz rahatligi icin geleneksel demlemelerde kullanilan guclu bir sifali bitkidir. Uzun sureli yuksek doz kullanimi risklidir.",
        "temelBilgiler": {
            "turkceAdi": "Meyan Koku",
            "botanikAdi": "Glycyrrhiza glabra",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Bogaz ve mide mukozasini yumusatmaya yardimci olabilir; kisa sureli demlemelerde tercih edilir.",
            "kullanimSekli": "Kurutulmus kok dilimleri kisa sure demlenerek cay yapilir.",
            "yanEtkilerUyarilar": "Uzun sure veya yuksek doz tansiyonu yukseltebilir ve potasyum dusuklugune yol acabilir. Hipertansiyon, bobrek ve kalp hastalarinda kullanilmamalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz, Guney Avrupa ve Guneybati Asya",
            "hasatMevsimi": "Sonbahar kok hasadi (3-4 yasindan sonra)",
            "ciceklenmeZamani": "Haziran - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Orta duzey nem",
            "toprakTipi": "Derin, kumlu-tinli ve iyi drene toprak",
        },
    },
    {
        "id": 31,
        "ad": "Safran",
        "botanikAd": "Crocus sativus",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Safran, Crocus sativus ciceginin kirmizi stigma tellerinden elde edilen degerli bir baharat ve geleneksel sifali urundur. Anadolu'da ozellikle Safranbolu yoresiyle bilinir.",
        "temelBilgiler": {
            "turkceAdi": "Safran",
            "botanikAdi": "Crocus sativus",
            "bitkiTuru": "Cok yillik soganli tibbi ve baharat bitkisi",
        },
        "saglikKullanim": {
            "faydalari": "Ruh hali destegi ve antioksidan ozellikleriyle arastirilmistir; mutfakta aroma ve renk verici olarak kullanilir.",
            "kullanimSekli": "Kucuk miktarda stigma telleri sicak suda bekletilerek yemek veya iceceklere eklenir.",
            "yanEtkilerUyarilar": "Yuksek doz zehirli olabilir. Hamilelikte farmakolojik dozlar tehlikelidir; yalnizca mutfak miktarlarinda kullanilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Iran, Ispanya, Yunanistan ve Turkiye (Safranbolu vb.)",
            "hasatMevsimi": "Sonbahar ciceklenme donemi (Ekim - Kasim)",
            "ciceklenmeZamani": "Ekim - Kasim",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Dinlenme doneminde az; buyume doneminde olculu",
            "toprakTipi": "Iyi drene, hafif kirecli ve kumlu toprak",
        },
    },
    {
        "id": 32,
        "ad": "Altin Otu",
        "botanikAd": "Helichrysum arenarium",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Altin otu (olmez cicek), sari cicek basaklariyla bilinen ve geleneksel olarak safra ve sindirim destegi amaciyla kullanilan bir sifali bitkidir. Gudul rehberinde de yer alir.",
        "temelBilgiler": {
            "turkceAdi": "Altin Otu",
            "botanikAdi": "Helichrysum arenarium",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Karaciger ve safra yollari icin geleneksel demleme olarak anilir; sindirim rahatligina destek olabilir.",
            "kullanimSekli": "Kurutulmus cicekler demlenerek cay yapilir.",
            "yanEtkilerUyarilar": "Safra tasi olanlar hekim kontrolunde kullanmalidir. Papatyagiller alerjisinde dikkat edilmelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Kumlu step ve kurak Anadolu-Avrupa bolgeleri",
            "hasatMevsimi": "Ciceklenme donemi",
            "ciceklenmeZamani": "Temmuz - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Az; kurakliga dayanikli",
            "toprakTipi": "Kumlu, zayif ve cok iyi drene toprak",
        },
    },
    {
        "id": 33,
        "ad": "Mercankosk",
        "botanikAd": "Origanum majorana",
        "tur": "Aromatik Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Mercankosk, kekige benzer aromasiyla bilinen ballibabagiller familyasindan sifali ve mutfak bitkisidir. Gudul rehberinde kekik ile birlikte anilir.",
        "temelBilgiler": {
            "turkceAdi": "Mercankosk",
            "botanikAdi": "Origanum majorana",
            "bitkiTuru": "Cok yillik aromatik tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Sindirim rahatligi, hafif yatistirici etki ve solunum yolu demlemelerinde destekleyici kullanimi vardir.",
            "kullanimSekli": "Kurutulmus yapraklar baharat veya cay olarak kullanilir.",
            "yanEtkilerUyarilar": "Hamilelikte yogun ucucu yag formundan kacinilmalidir. Olculu baharat kullanimi genelde guvenlidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz iklimi ve gunesli bahceler",
            "hasatMevsimi": "Ciceklenme oncesi yaprak hasadi",
            "ciceklenmeZamani": "Haziran - Agustos",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Az-orta; asiri sudan kacinilir",
            "toprakTipi": "Kumlu, kirecli ve iyi drene toprak",
        },
    },
    {
        "id": 34,
        "ad": "Sarimsak",
        "botanikAd": "Allium sativum",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Sarimsak, mutfagin temel aromatiklerinden olmanin yani sira geleneksel sifada bagisiklik ve kalp-damar destegi amaciyla en cok anilan bitkilerden biridir.",
        "temelBilgiler": {
            "turkceAdi": "Sarimsak",
            "botanikAdi": "Allium sativum",
            "bitkiTuru": "Cok yillik soganli tibbi ve mutfak bitkisi",
        },
        "saglikKullanim": {
            "faydalari": "Bagisiklik destegi, antimikrobiyal ozellikleri ve kardiyovaskuler saglikla iliskili geleneksel kullanimi vardir.",
            "kullanimSekli": "Cig veya pisirilmis dis olarak yemeklerde; olculu miktarda tuketilir.",
            "yanEtkilerUyarilar": "Kan sulandirici ilaclarla etkilesebilir. Ameliyat oncesi birakilmasi onerilebilir; mide hassasiyeti yapabilir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Dunya genelinde kultur bitkisi; Anadolu'da yaygin tarimi vardir.",
            "hasatMevsimi": "Yaz basi sogan hasadi",
            "ciceklenmeZamani": "Cogu kultur cesidi nadiren ciceklenir",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Buyume doneminde duzenli; hasada yakin azaltilir",
            "toprakTipi": "Gevsek, verimli ve iyi drene toprak",
        },
    },
    {
        "id": 35,
        "ad": "Kara Murver",
        "botanikAd": "Sambucus nigra",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Kara murver, cicek ve olgun meyveleriyle bilinen geleneksel bir sifali calidir. Cicekleri demleme, meyveleri ise surup formunda soguk mevsim desteklerinde kullanilir.",
        "temelBilgiler": {
            "turkceAdi": "Kara Murver",
            "botanikAdi": "Sambucus nigra",
            "bitkiTuru": "Cok yillik cali; tibbi cicek ve meyve",
        },
        "saglikKullanim": {
            "faydalari": "Soguk alginligi donemlerinde bagisiklik destegi amaciyla anilir; cicek cayi terletici ve yumusatici etkiyle bilinir.",
            "kullanimSekli": "Kurutulmus cicekler demlenir; olgun meyveler pisirilerek surup veya recel yapilir.",
            "yanEtkilerUyarilar": "Cig meyve, yaprak ve tohumlar toksik olabilir. Yalnizca olgun meyve pisirilerek veya guvenilir urunler kullanilmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Avrupa ve Anadolu nemli orman kenarlari, bahceler",
            "hasatMevsimi": "Cicek: yaz basi; meyve: yaz sonu-sonbahar",
            "ciceklenmeZamani": "Mayis - Temmuz",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes veya yari gunes",
            "sulamaSikligi": "Duzenli nem sever",
            "toprakTipi": "Nemli, humuslu ve verimli toprak",
        },
    },
    {
        "id": 36,
        "ad": "Karabas Otu",
        "botanikAd": "Lavandula stoechas",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Karabas otu, Akdeniz'e ozgu lavanta turlerinden biridir ve Anadolu'da geleneksel sifali demlemelerde adi gecer. Solunum yolu rahatsizliklarinda halk arasinda tercih edilir.",
        "temelBilgiler": {
            "turkceAdi": "Karabas Otu",
            "botanikAdi": "Lavandula stoechas",
            "bitkiTuru": "Cok yillik aromatik tibbi cali",
        },
        "saglikKullanim": {
            "faydalari": "Solunum yolu demlemelerinde destekleyici kullanimi vardir; aromatik rahatlatici etkisiyle bilinir.",
            "kullanimSekli": "Cicekli ust kisimler demlenerek cay yapilir; buhar inhalasyonunda da kullanilabilir.",
            "yanEtkilerUyarilar": "Hamilelikte ve epilepsi oykusunda dikkatli kullanilmalidir. Ucucu yag seyreltilmeden cilde surulmemelidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Akdeniz maki alanlari, Ege ve Guney Anadolu",
            "hasatMevsimi": "Ilkbahar sonu - yaz basi",
            "ciceklenmeZamani": "Mart - Haziran",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes",
            "sulamaSikligi": "Az; kurakliga dayanikli",
            "toprakTipi": "Kirecli, tasli ve iyi drene toprak",
        },
    },
    {
        "id": 37,
        "ad": "Andiz Otu",
        "botanikAd": "Inula helenium",
        "tur": "Tibbi Bitkiler",
        "resimUrl": "assets/plants/bitki-kart.svg",
        "genelTavsiyeMetni": "Andiz otu, buyuk sari cicekleri ve aromatik kokuyle bilinen geleneksel bir sifali bitkidir. Solunum yolu rahatsizliklarinda kok kullanimi halk hekimliginde yer alir.",
        "temelBilgiler": {
            "turkceAdi": "Andiz Otu",
            "botanikAdi": "Inula helenium",
            "bitkiTuru": "Cok yillik otsu tibbi bitki",
        },
        "saglikKullanim": {
            "faydalari": "Solunum yolu ve oksuruk rahatsizliklarinda geleneksel demleme olarak anilir; sindirim destegi de soylenir.",
            "kullanimSekli": "Kurutulmus kok dilimleri demlenerek veya kaynatilarak kullanilir.",
            "yanEtkilerUyarilar": "Yuksek doz mide tahrisi yapabilir. Hamilelikte ve alerji oykusunda uzman gorusu alinmalidir.",
        },
        "cografyaMevsim": {
            "yetistigiYerler": "Avrupa ve Bati Asya; nemli cayir ve bahce kenarlari",
            "hasatMevsimi": "Sonbahar kok hasadi",
            "ciceklenmeZamani": "Temmuz - Eylul",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam gunes veya yari gunes",
            "sulamaSikligi": "Duzenli; nemli toprak sever",
            "toprakTipi": "Derin, verimli ve nem tutan toprak",
        },
    },
]


def main() -> None:
    plants = json.loads(PATH.read_text(encoding="utf-8"))
    existing_ids = {plant["id"] for plant in plants}
    existing_names = {plant["ad"].lower() for plant in plants}

    added = []
    for plant in normalize(NEW_PLANTS):
        if plant["id"] in existing_ids or plant["ad"].lower() in existing_names:
            continue
        plants.append(plant)
        added.append(plant["ad"])

    PATH.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Toplam bitki: {len(plants)}")
    print(f"Yeni eklenen: {len(added)}")
    print("Yeni adlar:", ", ".join(added))


if __name__ == "__main__":
    main()
