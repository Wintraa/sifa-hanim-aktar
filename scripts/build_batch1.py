# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "vaka-rewrite-batch1-raw.json"
OUT = ROOT / "data" / "vaka-rewrite-batch1.json"

REWRITES = {
    "1": {
        "baslik": "Papatya çayı sonrası ağır alerjik şok",
        "sorun": "Saman nezlesi ve astımı olan 8 yaşındaki çocuk, hayatında ilk kez papatya çayı içtikten sonra ağır alerjik şok (anafilaksi) geçirdi.",
        "yaklasim": "Papatya çayı özütüne deri testi, pasif transfer testi ve ELISA ile IgE antikorları incelendi; pelin ve diğer polenlerle çapraz alerji testleri yapıldı.",
        "sonuc": "Tepkinin IgE aracılı alerji olduğu doğrulandı; pelin polenine daha önce duyarlı olan çocuğun papatyadaki polenlerle çapraz reaksiyon verdiği gösterildi.",
        "anlatim": "Polen alerjisi olan bir çocuk ilk papatya çayını içtikten sonra ağır alerjik şoka girdi. Testler papatyaya karşı IgE antikorları ve pelin ile çapraz duyarlılığı ortaya koydu. Yazarlar tepkinin tip I IgE aracılı mekanizmayla açıklandığını belirtti. Bu olgu ciddi alerji riskini belgeler. Bu metin tıbbi tavsiye değildir.",
    },
    "5": {
        "baslik": "Adaçayı çayı sonrası yüzde şişlik",
        "sorun": "13 yaşındaki erkek çocukta, kekik içeren yemekten ve ardından adaçayı çayından sonra yüzde ve vücutta ani şişlik (anjiyoödem) gelişti; daha önce bilinen alerji öyküsü yoktu.",
        "yaklasim": "Et, peynir, adaçayı, kekik ve nane ayrı ayrı ağızdan deneme (OFC) ve deri testleriyle değerlendirildi.",
        "sonuc": "Adaçayı, kekik ve nane denemelerinde şişlik tekrarladı; ballıbabagiller (Lamiaceae) alerjisi tanısı kondu. Deri testi yalnızca nanede pozitifti; tanı çoğunlukla ağızdan denemeye dayandı.",
        "anlatim": "Çocuğun ilk şişliği yemekteki kekikten, ikincisi adaçayı çayından kaynaklandı. Nane ile de benzer reaksiyon görüldü. Aynı bitki ailesindeki baharatlar alerji tetikleyici olabilir. Bu metin tıbbi tavsiye değildir.",
    },
    "7": {
        "baslik": "Yenidoğanda kekik suyu sonrası ağır kriz",
        "sorun": "14 günlük bebek, gaz sancısı (infantil kolik) için şekerli kekik suyu içirildikten iki saat sonra ağır nefes darlığıyla acile geldi. Kan şekeri düşük, kanda asit birikimi (laktik asidoz) vardı.",
        "yaklasim": "Acil değerlendirme yapıldı; altta yatan fruktoz 1-6 difosfataz eksikliği araştırılıp doğrulandı.",
        "sonuc": "Nadir metabolik hastalık tanısı kondu. Asidozun kekik suyuna eklenen şeker/fruktoz veya kekikteki fenolik bileşenlerle tetiklenmiş olabileceği düşünüldü.",
        "anlatim": "Gaz için verilen şekerli kekik suyu sonrası yenidoğan ağır solunum sıkıntısıyla hastaneye getirildi. İnceleme altta yatan enzim eksikliğini ortaya çıkardı. Yazarlar tatlandırıcı veya kekik bileşenlerinin krizi tetiklemiş olabileceğini belirtti. Bu metin tıbbi tavsiye değildir.",
    },
    "10": {
        "baslik": "Kas hastalığında Ayurveda bakımı",
        "sorun": "Dokuz yaşındaki erkek çocukta Duchenne kas distrofisi vardı: altı yaşından beri yardım olmadan ayakta duramıyor ve yürüyemiyordu. Alt ekstremite güçsüzlüğü, iştahsızlık, düzensiz bağırsak hareketleri ve huzursuzluk eşlik ediyordu.",
        "yaklasim": "Dört ay boyunca altı seans Ayurveda uygulandı: dış ve iç Swedana, Basti, ağızdan bitkisel ilaçlar (Zingiber officinale dahil) ve diyet düzenlemesi; fizyoterapi sürdürüldü.",
        "sonuc": "Üçüncü seans sonrası yatak kenarından destekle ayakta durma ve taş tutup atma görüldü. Bir ay sonunda iştah ve bağırsak alışkanlıklarında iyileşme bildirildi; kabızlık azaldı, üst ekstremite kas tonusunda ince değişiklikler ve yaşam kalitesinde artış kaydedildi.",
        "anlatim": "Ağır kas hastalığı olan çocuğa Ayurveda temelli çok bileşenli bakım uygulandı; zencefil ağızdan verilen bitkiler arasındaydı. Takipte ayakta durma kapasitesi ve genel şikayetlerde iyileşme bildirildi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "11": {
        "baslik": "COVID-19'da ekinezya fayda-risk değerlendirmesi",
        "sorun": "Hafif, grip benzeri COVID-19 şikayetlerinde birçok kişinin bitkisel destek eklemesi bekleniyordu; hangisinin güvenli veya yararlı olduğu net değildi.",
        "yaklasim": "DSÖ ve EMA listelerindeki 39 bitki için klinik ve laboratuvar verileri derlendi; fayda-risk dengesi paracetamol, ibuprofen ve kodein referans alınarak sınıflandırıldı.",
        "sonuc": "Echinacea purpurea dahil 12 bitki umut verici (promising) olarak sınıflandırıldı. Derleme, erken/hafif gripte destek tedavisi olarak klinik tartışmaya değer olabilecek bitkileri öne çıkardı.",
        "anlatim": "Bu derleme COVID-19 döneminde solunum şikayetlerinde kullanılan bitkilerin fayda-risk dengesini değerlendirir. Ekinezya umut verici grupta yer alır. Metin tek hasta öyküsü değil, bilimsel kanıt özetidir. Bu metin tıbbi tavsiye değildir.",
    },
    "12": {
        "baslik": "Deri sertleşmesinde Ayurveda bakımı",
        "sorun": "45 yaşındaki kadında üç yıldır yaygın deri sertleşmesi, renk açılması, eklem katılığı, eklem ağrısı, iştahsızlık, kabızlık ve göğüs yanması vardı. Yaygın sistemik skleroz tanısı konmuştu.",
        "yaklasim": "Ayurveda protokolü uygulandı: pippali rasayan, svedana, virechan, basti ve ağızdan bitkisel ilaçlar; rezene (Foeniculum vulgare) arka da dahildi.",
        "sonuc": "Sekiz hafta sonra renk açılması azaldı, yeni saç çıkışı görüldü, hafif deri yumuşaması oldu; göğüs yanması, iştahsızlık ve uykusuzluk azaldı, ruhsal iyilik hali arttı.",
        "anlatim": "Uzun süredir sistemik skleroz yaşayan kadına Ayurveda bakımı verildi; rezene ağızdan preparatların parçasıydı. Sekiz haftada deri ve şikayetlerde kısmi düzelme kaydedildi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "13": {
        "baslik": "Kontrolsüz hipertiroidide melisa çayı",
        "sorun": "27 yaşındaki kadında kronik hipertiroidi vardı: düşük TSH, yüksek T3-T4, ekzoftalmus, çarpıntı, kaygı, uyku sorunu, saç dökülmesi ve kuru cilt. Bir yıl prednizolon ve metimazol sonrası yeterli düzelme olmamıştı.",
        "yaklasim": "Geleneksel Fars tıbbı paketi verildi: yaşam tarzı düzenlemesi, melisa bitki çayı ve Fars arpa suyu; bir yıl izlendi.",
        "sonuc": "İki ayda TSH arttı, T3-T4 düştü; ekzoftalmus, çarpıntı, kaygı, uyku bozukluğu ve cilt kuruluğu belirgin düzeldi. Üç ayda tiroid kan değerleri normal aralığa girdi; bir yıllık izlemde durum stabil kaldı.",
        "anlatim": "İlaçlara rağmen kontrolsüz hipertiroidisi olan kadın melisa çayı içeren geleneksel bakım aldı. Takipte hem laboratuvar hem şikayetlerde iyileşme kaydedildi. Bu tek olgu sunumudur. Bu metin tıbbi tavsiye değildir.",
    },
    "14": {
        "baslik": "Yenidoğanda ısırgan suyuyla kurdeşen",
        "sorun": "17 günlük bebekte yaygın kurdeşen (ürtiker) çıktı. Anne, meme çatlakları için emzirmeden önce ve sonra ısırgan otu kaynatma suyunu meme ucuna sürmüştü.",
        "yaklasim": "Bebek ve annede kanda ısırgana özel IgE düzeyleri ölçüldü; bebekte ısırgan suyuyla deri çizik testi yapıldı.",
        "sonuc": "Bebekte yüksek IgE ve pozitif deri testi saptandı. Döküntüler ilaç verilmeden birinci günde geriledi, ikinci günde kayboldu.",
        "anlatim": "Emziren annenin ısırgan kaynatmasıyla temastan sonra bebekte kurdeşen görüldü. Testler bebekte duyarlılığı destekledi. Döküntü kısa sürede kendiliğinden geçti. Bu metin tıbbi tavsiye değildir.",
    },
    "15": {
        "baslik": "Civanperçemi alerjisi ve bağışıklık hücreleri",
        "sorun": "38 yaşındaki alerjisi olmayan erkek oduncuda mevsimsel hava yoluyla temas dermatiti vardı; ışığa maruz cilt bölgelerinde kızarık-skalöz lezyonlar ve kabarcıklar görülüyordu.",
        "yaklasim": "Civanperçemi dahil birkaç Compositae (bileşikgiller) özütüne yama testi yapıldı; kanından alınan T hücreleri laboratuvar ortamında incelendi.",
        "sonuc": "Civanperçemi dahil birçok Compositae özütüne pozitif yama testi elde edildi. T hücre klonları Th0 fenotipi gösterdi; IFN-gamma ve IL-4 yüksek düzeyde üretildi.",
        "anlatim": "Oduncunun mevsimsel cilt döküntüsünde civanperçemi yama testinde pozitifti. Bağışıklık hücrelerinin sitokin profili incelendi; IL-4'ün de rol oynayabileceği belirtildi. Bu immunoloji çalışmasıdır, tedavi sonucu raporu değildir. Bu metin tıbbi tavsiye değildir.",
    },
    "16": {
        "baslik": "Kirlenmiş hatmi köküyle zehirlenme",
        "sorun": "27 yaşındaki erkek ve 28 yaşındaki gebe kadın, soğuk algınlığı için hatmi kökü karışımını sıcak çikolataya ekledikten sonra ağır antikolinerjik sendromla (ağız kuruluğu, bilinç değişikliği vb.) acile geldi.",
        "yaklasim": "Kısa süre yoğun bakımda destek tedavi verildi. Bitki örneğinde yüksek miktarda atropin bulundu; muhtemelen güzelavrat otundan (Atropa belladonna) bulaşmıştı.",
        "sonuc": "Semptomlar geriledi ve hastalar taburcu edildi. Maruz kalınan atropin dozu 2 mg'lık hafif toksik dozun çok üzerindeydi (20-200 mg).",
        "anlatim": "Hatmi kökü ürününün zehirli bir bitkiyle karışmış olduğu anlaşıldı. İki kişi ağır zehirlendi ama destek tedaviyle düzeldi. Bu istenmeyen olay belgesidir. Bu metin tıbbi tavsiye değildir.",
    },
    "17": {
        "baslik": "Bebekte anason karışımıyla karaciğer yetmezliği",
        "sorun": "4 aylık bebekte karaciğer enzimleri çok yükseldi, kan pıhtılaşması bozuldu, kan şekeri düştü, nöbet ve gözlerde istemsiz hareketler (nistagmus) gelişti.",
        "yaklasim": "Enfeksiyon, metabolik ve bağışıklık hastalıkları dışlandı. Aile, iki aydır her gün yıldız anason ve yeşil anason kaynatması verdiğini söyledi.",
        "sonuc": "Ev yapımı anason ürününe bağlı karaciğer yetmezliği olarak değerlendirildi. Bebeklere evde bitki çayı vermenin ciddi riski vurgulandı.",
        "anlatim": "Gaz için verilen anason karışımı sonrası bebekte ağır karaciğer ve sinir sistemi tablosu belgelendi. Başka nedenler ekarte edildi. Bu olumsuz olgu sunumudur. Bu metin tıbbi tavsiye değildir.",
    },
    "18": {
        "baslik": "COVID-19'da çörek otu içeren ev desteği",
        "sorun": "44 yaşındaki erkek hekimde hastaneden kapılan COVID-19 doğrulandı. Sonra kuru öksürük ve nefes alma zorluğu gelişti.",
        "yaklasim": "Evde izolasyon ve öksürük ilacı sonrası TaibUVID karışımı (çörek otu, papatya ve bal) hem buhar hem ağızdan günde beş kez dört gün kullanıldı.",
        "sonuc": "Ertesi gün belirtiler hafifledi. İki gün sonra burun-boğaz sürüntüsü PCR negatif oldu; diğer hastalar hâlâ pozitifti. Birkaç gün sonra semptomlar kayboldu ve işe döndü.",
        "anlatim": "COVID-19'lu bir hekim çörek otu içeren ev yapımı destek kullandı. Kısa sürede rahatlama hissetti ve PCR negatife döndü. Bu tek kişi deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "19": {
        "baslik": "Romatoid artritte kuşburnu tozu çalışması",
        "sorun": "Romatoid artritli 89 hastada (ortalama yaş 56,6; ortalama hastalık süresi 12,8 yıl) günlük işlev kaybı ve hastalık aktivitesi vardı.",
        "yaklasim": "Çift kör plasebo kontrollü çalışmada altı ay boyunca günde 5 gram kapsüllü kuşburnu tozu veya plasebo verildi. HAQ, DAS-28 ve yaşam kalitesi skorları izlendi.",
        "sonuc": "Kuşburnu grubunda HAQ-DI 0,105 iyileşti, plasebo grubunda 0,039 kötüleşti (p=0,032). DAS-28'de kuşburnu lehine eğilim (p=0,056) ve hekim global skorunda anlamlı üstünlük (p=0,012) görüldü.",
        "anlatim": "Romatoid artritli katılımcılar altı ay kuşburnu tozu aldı. Günlük işlev skorlarında plaseboya göre iyileşme bildirildi. Bu klinik araştırma özetidir. Bu metin tıbbi tavsiye değildir.",
    },
    "20": {
        "baslik": "Bacak yarası ve selülitte aynısefa bakımı",
        "sorun": "Kadın hastada sol alt bacakta sivilce benzeri lezyondan ağrılı yara (ülser) gelişti. Kızarıklık, şişlik, sıcaklık ve hassasiyet selülit (deri altı iltihabı) ile uyumluydu.",
        "yaklasim": "Kişiye özel homeopati yaklaşımında Pyrogenium, aynısefa (Calendula) ve Myristica sırayla verildi; antiseptik yara bakımı ve aynısefa merhemi uygulandı.",
        "sonuc": "Takipte ağrı, iltihap ve yara boyutlarında kademeli azalma görüldü; yara iyileşmesi tatmin edici bulundu, advers olay bildirilmedi.",
        "anlatim": "Bacak ülseri ve selüliti olan hastaya aynısefa içeren bireyselleştirilmiş bakım uygulandı. Seri fotoğraflarla iyileşme izlendi. MONARCH ölçeğinde olumlu ilişki skoru elde edildi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "21": {
        "baslik": "Diyabetik ayak enfeksiyonunda sarı kantaronlu ışık tedavisi",
        "sorun": "Diyabetli iki hastada ayak yarası ve kemik enfeksiyonu (osteomiyelit) vardı; ampütasyon riski taşıyorlardı.",
        "yaklasim": "Fotodinamik antimikrobiyal bakım (PACT) uygulandı: yara içine fenotiyazin boyaları ve sarı kantaron (Hypericum) özütü enjekte edilip ışık verildi. Seanslar başlangıçta günlük, iyileşme başlayınca haftalık yapıldı.",
        "sonuc": "Her iki hasta da ampütasyon öncesinde iyileşti. Röntgenlerde kemik iyileşmesi ve doku yapısında düzelme görüldü.",
        "anlatim": "Osteomiyelitli diyabetik iki hastaya sarı kantaron özütü içeren PACT protokolü uygulandı. Ampütasyon planlanan hastalar iyileşti. Bu klinik deneyim raporudur. Bu metin tıbbi tavsiye değildir.",
    },
    "22": {
        "baslik": "Çemen tozuyla ani ağır alerji",
        "sorun": "İki kişide çemen tohumu tozunun solunması, yutulması veya saça sürülmesi sonrası ani alerji gelişti. Birinde burun akıntısı, hırıltı ve bayılma; diğerinde baş uyuşması, yüzde şişlik ve hırıltı vardı.",
        "yaklasim": "Deri çizik testleri, çift kör plasebo kontrollü ağızdan deneme ve immunoblot ile IgE bağlanması incelendi.",
        "sonuc": "Her iki hastada çemen ve nohuta duyarlılık doğrulandı; ağızdan denemede solunum akımında %20'den fazla düşüş görüldü. Çemen gıda alerjenleri listesine eklendi.",
        "anlatim": "Çemen baharatı ciddi solunum ve deri reaksiyonlarına yol açtı. Testler alerjiyi objektif olarak doğruladı. Bu olumsuz alerji olgularıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "26": {
        "baslik": "Lynch sendromunda meyan kökü Ayurveda bakımı",
        "sorun": "28 yaşındaki erkekte Lynch sendromu vardı. Üç ameliyat ve kemoterapi sonrası 2019'da adenokanser tanısı aldı; yeni ameliyat yerine Ayurveda danışmanlığı istedi.",
        "yaklasim": "15 gün meyan kökü (Glycyrrhiza glabra) sütlü kalpa preparatı verildi.",
        "sonuc": "15 günde yaşam kalitesi skorunda anlamlı iyileşme (P<0,001) ve karın BT'de bağırsak duvarı kalınlığında 2,8 cm'den 1,5 cm'ye düşüş (~%50) görüldü; komplikasyon kötüleşmedi.",
        "anlatim": "Kalıtsal bağırsak kanseri yatkınlığı olan genç erkek meyan kökü içeren Ayurveda bakımı aldı. Kısa sürede yaşam kalitesi ve görüntülemede düzelme bildirildi. Bu tek olgu sunumudur. Bu metin tıbbi tavsiye değildir.",
    },
    "27": {
        "baslik": "Tekrarlayan divertikülitte safran içeren destek",
        "sorun": "72 yaşındaki emekli hekimde yedi yıldır tekrarlayan divertikülit vardı. İlk altı yılda yılda 3-4 antibiyotik gerektiren atak, 2013'te yaklaşık iki ayda bir atak olmaya başladı.",
        "yaklasim": "Mart 2013'te Carpellum Mali comp. (ağızdan) ve safran (Crocus) içeren Kalium aceticum comp. (cilt altı) eklendi.",
        "sonuc": "Dört ayda semptomsuz iyileşme görüldü. Sonraki 28 ayda 4 hafif atak, ardından 11 ay ataksız geçti; 41 aylık izlemde yan etki bildirilmedi.",
        "anlatim": "Sık divertikülit atakları yaşayan hekim safran içeren entegratif preparatlar aldı. Atak sıklığı belirgin azaldı. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "28": {
        "baslik": "Altın otu paketlemede akar kaynaklı döküntü salgını",
        "sorun": "Bitkisel ilaç üreten işyerinde altın otu tartıp paketleyen 18 çalışanda kaşıntılı, sulu kabarcıklı döküntü gelişti; bazılarında grip benzeri hastalık da vardı.",
        "yaklasim": "Meslek hastalıkları merkezinde değerlendirme yapıldı. Bitki örneklerinde Pyemotes ventricosus adlı akar doğrulandı.",
        "sonuc": "İlk 16 çalışanda lezyonlar görüldü; 44 gün sonra iki yeni olgu eklendi. Etken bitkinin kendisi değil, bitkiye bulaşan akarlardı.",
        "anlatim": "Altın otu işleyen işçilerde kaşıntılı döküntü salgını bildirildi. İnceleme kontamine akar kaynaklı olduğunu gösterdi. Bu mesleki maruziyet belgesidir. Bu metin tıbbi tavsiye değildir.",
    },
    "30": {
        "baslik": "Hepatopulmoner sendromda yüksek doz sarımsak",
        "sorun": "Ağır hepatopulmoner sendromlu hastada kanda oksijen düşüklüğü (hipoksi) vardı. Somatostatin yanıt vermedi; karaciğer naklini reddetti.",
        "yaklasim": "Hasta kendi girişimiyle 18 ay boyunca yüksek doz toz sarımsak aldı.",
        "sonuc": "18 aylık kullanımda semptomlarda kısmi hafifleme ve bazı objektif iyileşme bulguları bildirildi.",
        "anlatim": "Karaciğer-akciğer sendromu olan hasta nakli reddedip yüksek doz sarımsak kullandı. Takipte kısmi rahatlama kaydedildi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "31": {
        "baslik": "Prion hastalığında mürver lektiniyle doku boyaması",
        "sorun": "Nadir Gerstmann-Sträussler-Scheinker (GSS) prion hastalığında beyinde anormal prion proteini birikimleri vardı.",
        "yaklasim": "Kara mürverden elde edilen lektin (SNA) dahil çeşitli lektinlerle doku boyaması yapıldı; prion antikoru ile eşleştirme incelendi.",
        "sonuc": "SNA, prion birikimlerinin çekirdeğinde sialil (açılı şeker) yapıları boyadı. Glikozilasyon (şeker ekleme) değişikliklerinin nöron hasarında erken olay olabileceği gösterildi.",
        "anlatim": "GSS hastalığı beyin dokusunda mürver kaynaklı lektin boyaması kullanıldı. Kara mürver burada ilaç değil, laboratuvar aracıdır. Bu patoloji çalışmasıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "32": {
        "baslik": "Depresyonda lavanta dahil bitki derlemesi",
        "sorun": "Depresyon dünya çapında yaygın ve ciddi bir ruhsal hastalıktır; klasik ilaçların yan etkileri nedeniyle doğal tedavi arayışı artmaktadır.",
        "yaklasim": "2015-2024 arası PubMed, ClinicalKey ve MedNar tarandı; 13 rastgele kontrollü çalışma ve 1 meta-analiz derlemeye alındı. Lavandula angustifolia dahil bitkiler değerlendirildi.",
        "sonuc": "Safran, lavanta, sarı kantaron ve zerdeçalın insan çalışmalarında depresyon belirtilerini hafiflettiği bildirildi. Bitkisel ürünler klasik farmakoterapiyi destekleyebilir.",
        "anlatim": "Sistematik derleme depresyonda fitoterapinin klinik çalışmalardaki yerini özetler. Lavanta etkili bitkiler arasında sayılır. Bu bireysel vaka değil, derlemedir. Bu metin tıbbi tavsiye değildir.",
    },
    "33": {
        "baslik": "Göz altı koyuluğunda andız içeren krem",
        "sorun": "35-60 yaş arası 40 kadında orta-ağır göz altı koyuluğu, şişlik ve ince çizgiler vardı.",
        "yaklasim": "12 haftalık açık etiketli çalışmada andız otu (Inula helenium) prebiyotiği, C vitamini türevi, peptidler, krizın ve kafein içeren göz kremi kullanıldı.",
        "sonuc": "37 katılımcı tamamladı. Krem kısa ve uzun vadede objektif ve öznel ölçümlerde iyileşme gösterdi; mikrodamar tıkanıklığı, melanin ve hemoglobin kaynaklı renk koyulaşmasında azalma bildirildi.",
        "anlatim": "Göz altı koyuluğu olan kadınlara andız içeren topikal krem uygulandı. Görünümde anlamlı iyileşme kaydedildi. Bu kozmetik klinik çalışmasıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "54": {
        "baslik": "Bahçe otlarıyla temastan hedef tahtası döküntüsü",
        "sorun": "52 yaşındaki kadın, ev bahçesinde otlarla temastan sonra 13 yıldır hedef tahtası benzeri deri döküntüsü (eritema multiforme) atakları yaşıyordu.",
        "yaklasim": "Taze bitkilerle yama ve ışıkla yama testleri yapıldı. Karahindiba dahil birkaç ottta egzama tipi pozitiflik ve ışıkla artma görüldü.",
        "sonuc": "Testin dördüncü gününde tipik döküntü yeniden başladı; yama testi komplikasyonu olarak eritema multiforme tekrarladı.",
        "anlatim": "Bahçe otlarıyla teması olan kadında eritema multiforme tekrarladı. Karahindiba yama testinde pozitifti. Test sırasında döküntü yeniden alevlendi. Bu olumsuz temas olgusudur. Bu metin tıbbi tavsiye değildir.",
    },
    "55": {
        "baslik": "Domuzlarda çoban çantası nitrit zehirlenmesi",
        "sorun": "18 domuzdan 4'ü öldü. Otopside kanın tipik kahverengi renk değişimi görüldü.",
        "yaklasim": "Hayvanların yediği bahçe artığı ve otlar incelendi. Yalnızca çoban çantası otunda nitrit bulundu.",
        "sonuc": "Çoban çantası kaynaklı şüpheli nitrit zehirlenmesi olarak bildirildi; literatürde ilk rapor olarak sunuldu.",
        "anlatim": "Bahçe artığı yiyen domuzlarda ölüm ve nitrit zehirlenmesini düşündüren otopsi bulguları vardı. Nitrit yalnızca çoban çantası otunda saptandı. Bu veteriner olgusudur. Bu metin tıbbi tavsiye değildir.",
    },
    "56": {
        "baslik": "Melanom sonrası ökse otu özütü deneyimi",
        "sorun": "68 yaşındaki erkekte 1992'de kolda, 1999'da omuzda melanom vardı; omuz tümörü evre IIA (pT3, pN0, M0) olarak çıkarıldı.",
        "yaklasim": "Ameliyat sonrası tek destek olarak standardize ökse otu özütü (Iscador M) başlandı. 2001'de karaciğerde tek metastaz saptandı; kemoterapi veya radyoterapi verilmedi, ökse otu dozu ayarlandı.",
        "sonuc": "Haziran 2002'de karaciğer metastazında tam remisyon tanısı kondu. Mayıs 2006'ya kadar yeni metastaz saptanmadı; hasta stabil kaldı.",
        "anlatim": "İki kez melanom geçiren hastaya ameliyat sonrası ökse otu özütü verildi. Karaciğer metastazı tamamen geriledi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "57": {
        "baslik": "Lorazepam ile kedi otu etkileşimi",
        "sorun": "Yaygın kaygı bozukluğu için lorazepam kullanan hasta, kendi kendine kedi otu ve çarkıfelek de aldı. 32 saat içinde el titremesi, baş dönmesi, çarpıntı ve kas yorgunluğu gelişti.",
        "yaklasim": "Aile öyküsü ve muayene ile esansiyel tremor, Parkinson ve Wilson hastalığı dışlandı. Bitki-ilaç etkileşimi değerlendirildi.",
        "sonuc": "Kedi otu ve çarkıfeleğin lorazepam etkisini artırarak GABA reseptörlerinde güçlendirici etki yapmış olabileceği düşünüldü.",
        "anlatim": "Lorazepam kullanan hasta kedi otu ve çarkıfeleği birlikte alınca titreme, baş dönmesi ve çarpıntı yaşadı. Nörolojik hastalıklar elendi. Bu etkileşim uyarısıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "58": {
        "baslik": "Lorazepam ile çarkıfelek etkileşimi",
        "sorun": "Lorazepam kullanırken çarkıfelek ve kedi otu alan hastada el titremesi, baş dönmesi, çarpıntı ve kas yorgunluğu ortaya çıktı.",
        "yaklasim": "Nörolojik hastalıklar dışlandı. Bitkisel ürün ile reçeteli ilaç etkileşimi klinik olarak değerlendirildi.",
        "sonuc": "Çarkıfelek ve kedi otunun lorazepam ile birlikte alındığında belirtilere yol açmış olabileceği; etkinin birbirine eklenmiş olabileceği düşünüldü.",
        "anlatim": "Çarkıfelek ve kedi otunun lorazepam ile birlikte kullanımı sonrası istenmeyen belirtiler belgelendi. Etkinin birbirine eklenmiş olabileceği düşünüldü. Bu etkileşim uyarısıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "59": {
        "baslik": "Lösemi kemoterapisinde deve dikeni desteği",
        "sorun": "Akut miyeloid lösemi için yeniden indüksiyon kemoterapisi sırasında karaciğer enzimleri yükseldi; destek bakıyla düzelmedi.",
        "yaklasim": "Deve dikeni (Silybum marianum / milk thistle) eklendi; karaciğer testleri izlendi.",
        "sonuc": "Karaciğer testlerinde hızlı düşüş görüldü; sonraki kemoterapilerde daha az yükselme bildirildi.",
        "anlatim": "Lösemi kemoterapisi sırasında karaciğer enzimleri yükselen hastaya deve dikeni eklendi. Enzimler hızla düştü ve sonraki kürlerde daha az yükseldi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "60": {
        "baslik": "Enginar tozuyla mesleki burun ve astım alerjisi",
        "sorun": "İki sebze deposu işçisinde enginar duyarlanmasıyla mesleki burun alerjisi (rinit) ve bronşiyal astım gelişti.",
        "yaklasim": "Deri çizik testi, bitkiye özel IgE, protein analizi, burun denemesi ve bir hastada işyeri solunum ölçümü yapıldı.",
        "sonuc": "Her iki hastada enginar deri testi pozitif; bitkiye özel IgE saptandı. Burun denemesinde solunum akımı %81-85 düştü. Parietaria poleni ile çapraz reaktivite gösterildi.",
        "anlatim": "Sebze deposunda çalışan iki kişide enginar tozuna bağlı burun ve astım alerjisi belgelendi. Testler duyarlılığı doğruladı. Bu mesleki alerji olgusudur. Bu metin tıbbi tavsiye değildir.",
    },
    "61": {
        "baslik": "Huzursuz bağırsakta şahtere çalışması",
        "sorun": "Huzursuz bağırsak sendromlu 106 hastada karın ağrısı ve şişkinlik vardı.",
        "yaklasim": "Çift kör plasebo kontrollü çalışmada şahtere (günde 1500 mg), zerdeçal türü veya plasebo 18 hafta verildi.",
        "sonuc": "Ağrı ve şişkinlikte gruplar arasında anlamlı fark gösterilmedi (p=0,81 ve p=0,48). Şahtere veya zerdeçal plaseboya üstünlük kanıtlanmadı.",
        "anlatim": "Huzursuz bağırsak yakınması olan kişilere şahtere veya zerdeçal verildi. Plaseboya göre anlamlı üstünlük bulunmadı. Bu nötr sonuçlu araştırma özetidir. Bu metin tıbbi tavsiye değildir.",
    },
    "62": {
        "baslik": "Mahlep baharatına alerjik tepki",
        "sorun": "40 yaşındaki kadın, badem ve ağaç yemişi alerjisi öyküsüyle mahlep çekirdeği yedikten kısa süre sonra orta şiddette kaşıntı ve ağız-boğaz şişliği yaşadı.",
        "yaklasim": "Antep fıstığı, badem ve mahlep özütleriyle deri çizik testleri ve ELISA/Western blot analizi yapıldı.",
        "sonuc": "Mahlep deri testinde 7 mm wheal; bademle antijenik benzerlik ve çapraz reaktivite gösterildi. Mahlebe akut alerji ilk kez belgelendi.",
        "anlatim": "Ağaç yemişi alerjisi olan kadın mahlep yedikten sonra ağız-boğaz şişliği yaşadı. Testler mahlep duyarlılığını ve bademle çapraz reaksiyonu destekledi. Bu alerji uyarısıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "63": {
        "baslik": "Aşırı üzerlik çayıyla ağır zehirlenme",
        "sorun": "41 yaşındaki kadın, sakinleşmek için önerilen dozun 10-20 katı (~100 g) üzerlik tohumunu kaynatarak içtikten sonra bilinç kaybı, yüksek tansiyon, hızlı nabız ve hızlı solunum gelişti.",
        "yaklasim": "Solunum tüpü takılması (entübasyon) ve beş gün destek tedavi uygulandı; karaciğer ve böbrek değerleri izlendi.",
        "sonuc": "Bilinç, böbrek ve karaciğer değerleri kademeli normale döndü. Yüksek dozda yaşamı tehdit edebilen zehirlenme olgusudur; destek tedaviyle iyileşme bildirildi.",
        "anlatim": "Çok yüksek doz üzerlik çayı sonrası kadın ağır bilinç kaybı ve solunum sorunu yaşadı. Yoğun bakım desteğiyle düzeldi. Bu zehirlenme olgusudur. Bu metin tıbbi tavsiye değildir.",
    },
    "64": {
        "baslik": "Sıçanlarda radyasyon yarasında eğir kökü",
        "sorun": "Kanser radyoterapisinde sık görülen radyasyon kaynaklı cilt yarası iyileşmeyi geciktirir; önleme ve tedavi için az ilaç vardır.",
        "yaklasim": "Sıçanlara 45 Gy radyasyon uygulandı; 10%, 20% ve 40% eğir kökü (Acorus calamus) özütü 45 gün verildi. Yara iyileşmesi, iltihap, hücre ölümü ve damar oluşumu ölçüldü.",
        "sonuc": "Orta doz grupta 45. günde %88,97 iyileşme oranı en yüksekti. İltihap azaldı, IL-1β/IL-6/TNF-α düştü, damar oluşumu arttı.",
        "anlatim": "Radyasyon yarası olan sıçanlarda eğir kökü özütü yara iyileşmesini hızlandırdı. Bu hayvan modeli çalışmasıdır, insan olgusu değildir. Bu metin tıbbi tavsiye değildir.",
    },
    "65": {
        "baslik": "Sıçanlarda ağız yarasında sinir otu",
        "sorun": "Ağız yaraları çeşitli nedenlerle oluşur; ağız ortamı sürekli değiştiği için kesin tedavi zordur.",
        "yaklasim": "72 Wistar sıçanına damakta 2 mm yara açıldı; farklı dozlarda nano-emülsifiye sinir otu (Plantago major) özütü uygulandı.",
        "sonuc": "%5 sinir otu nano-emülsiyonunda yara yeniden kaplanma oranı %66,7 ile en yüksekti; diğer formlar belirgin fayda göstermedi. Dört doz sonrası gruplar arasında anlamlı fark bulunmadı.",
        "anlatim": "Sıçan ağız yaralarında sinir otu nano-emülsiyonu yeniden kaplanmayı artırdı; diğer formlar belirgin fayda göstermedi. Bu hayvan çalışmasıdır. Bu metin tıbbi tavsiye değildir.",
    },
    "66": {
        "baslik": "Kadın hastalıklarında ayı üzümü kullanımı",
        "sorun": "Kadınlar adet, menopoz yakınmaları ve basit idrar yolu enfeksiyonları için bitkisel ürün kullanıyordu.",
        "yaklasim": "PhytoVIS veri tabanından 1658 kadının kendi bildirdiği bitkisel kullanımları analiz edildi.",
        "sonuc": "Basit idrar yolu enfeksiyonunda ayı üzümü (Arctostaphylos uva-ursi) en çok kullanılan bitkilerden biriydi. Algılanan etkinlik ve tolerabilite çok iyi puanlandı.",
        "anlatim": "Gerçek yaşam verisinde kadınların bitkisel ürün tercihleri incelendi. Ayı üzümü idrar yolu şikayetlerinde öne çıktı. Bu gözlemsel analizdir. Bu metin tıbbi tavsiye değildir.",
    },
    "67": {
        "baslik": "Hafif prolaktin yüksekliğinde hayıt deneyimi",
        "sorun": "Hafif prolaktin yüksekliği ve seyrek adet (oligomenore) olan hastada göreli östrojen düşüklüğü vardı; hipofiz tümörü yoktu. Bromokriptin ilacını tolere edemedi.",
        "yaklasim": "Hayıt (Vitex agnus-castus) özütü başlandı.",
        "sonuc": "Şikayetlerde rahatlama ve hormonal testlerde düzelme bildirildi.",
        "anlatim": "İlacı tolere edemeyen hastaya hayıt özütü verildi. Şikayet ve hormon testlerinde düzelme kaydedildi. Bu tek olgu sunumudur. Bu metin tıbbi tavsiye değildir.",
    },
    "68": {
        "baslik": "Zayıflama takviyesiyle kalp ritmi duraklaması",
        "sorun": "37 yaşındaki sağlıklı erkek, 10 gün Hydroxycut Hardcore zayıflama takviyesi aldıktan sonra bayılma (senkop) yaşadı. Telemetride tekrarlayan sinüs düğüm duraklamaları ve 24 saniyelik duraklama görüldü.",
        "yaklasim": "Ürün kesildi; kardiyak izlem yapıldı.",
        "sonuc": "İlaç bırakılınca semptomlar tamamen geçti. Hydroxycut'a bağlı bradiaritmi (yavaş kalp ritmi) ve senkop ilk kez raporlandı.",
        "anlatim": "Zayıflama takviyesi kullanan erkekte bayılma ve kalp ritmi duraklamaları görüldü. Ürün kesilince düzeldi. Özet Hydroxycut Hardcore takviyesini anlatır; aslanpençesi bu yayında geçmez. Bu metin tıbbi tavsiye değildir.",
    },
    "70": {
        "baslik": "At kestanesi içeren saç takviyesiyle morarma",
        "sorun": "23 yaşındaki kadın, doğum kontrol hapı başladıktan kısa sonra bacaklarda ağrılı morarmalarla acile geldi. Hap kesilince morarma geçti.",
        "yaklasim": "Sonradan aynı dönemde at kestanesi özütü içeren oral saç takviyesi de aldığı anlaşıldı. Hap tek başına yeniden denendi.",
        "sonuc": "Yalnızca hapla reaksiyon olmadı; at kestanesi içeren takviyenin kan sulandırıcı etkisi daha olası neden sayıldı.",
        "anlatim": "Morarmalar önce doğum kontrol hapına bağlandı. Sonra aynı dönemde at kestanesi içeren saç takviyesi aldığı anlaşıldı; yalnız hapla tepki yeniden olmadı. Bu istenmeyen olay belgesidir. Bu metin tıbbi tavsiye değildir.",
    },
    "71": {
        "baslik": "İleri karaciğer kanserinde geven içeren macun",
        "sorun": "55 yaşındaki kadında yaygın karaciğer kanseri, portal ven pıhtısı ve idrar söktürücülere dirençli karın suyu (asit) vardı. Genel durumu kötüydü (ECOG skoru 3).",
        "yaklasim": "Göbek çevresindeki bir noktaya geven (Astragalus) içeren bitkisel macun ve günde bir saat bitkisel ısıtma (moksibüstyon) uygulandı.",
        "sonuc": "Bir ayda bel çevresi 86 cm'den 71 cm'ye düştü, genel durum skorunda iyileşme oldu; istenmeyen etki gözlenmedi.",
        "anlatim": "İleri karaciğer kanserli ve karın suyu biriken kadına geven içeren dışarıdan macun ve ısıtma uygulandı. Bir ayda bel çevresi ve genel durumda düzelme bildirildi. Bu tek olgu deneyimidir. Bu metin tıbbi tavsiye değildir.",
    },
    "72": {
        "baslik": "Üreter stenti şikayetlerinde altınbaşak kompleksi",
        "sorun": "İdrar yoluna double-J stent takılan 60 hastada idrar yakınmaları, ağrı ve yaşam kalitesi bozulması vardı.",
        "yaklasim": "Açık etiketli rastgele çalışmada altınbaşak (Solidago) içeren bitkisel kompleks veya tamsulosin bir ay verildi; USSQ skorları izlendi.",
        "sonuc": "Her iki tedavide skorlar başlangıca göre iyileşti; idrar semptomlarında 7. ve 21. günlerde tamsulosin lehine anlamlı fark vardı. Ağrı ve diğer alanlarda anlamlı fark bildirilmedi.",
        "anlatim": "Stent şikâyeti olan hastalara altınbaşak içeren kompleks veya tamsulosin verildi. İkisinde de skorlar düzeldi; bazı idrar yakınmalarında ilaç kolu biraz öndeydi. Bu araştırma özetidir. Bu metin tıbbi tavsiye değildir.",
    },
    "74": {
        "baslik": "Köpekte hünnap çekirdeği yabancı cisim",
        "sorun": "15 yaşındaki kısırlaştırılmış erkek Maltese köpek, bütün hünnap yedikten beş gün sonra iştahsızlık ve halsizlik yaşadı.",
        "yaklasim": "Röntgenlerde karakteristik çizgili opak cisimler görüldü. Ameliyatla mideden altı sivri uçlu çekirdek çıkarıldı.",
        "sonuc": "Köpek sorunsuz iyileşti. Veteriner literatürde hünnap çekirdeği yutma ilk kez bu şekilde raporlandı.",
        "anlatim": "Bütün hünnap yiyen köpeğin midesinden sivri çekirdekler ameliyatla çıkarıldı. Köpek iyileşti. Bu veteriner olgusudur, insan şifa deneyimi değildir. Bu metin tıbbi tavsiye değildir.",
    },
    "75": {
        "baslik": "Alıç kökü tabletiyle yavaş nabız",
        "sorun": "Hasta kilo vermek için internetten alıç kökü (Crataegus mexicana) tableti aldıktan sonra yaygın kas ağrıları, baş dönmesi ve dakikada 52 atımlık yavaş nabızla (bradikardi) acile geldi.",
        "yaklasim": "Tekrar sorulunca bitkisel ürün öyküsü alındı. Kanda digoksin benzeri düzey ölçüldü; gözlem yapıldı.",
        "sonuc": "Şikayetler gözlemle düzeldi, kalp hızı normale döndü. Alıç kökünün kalp glikozidi benzeri etkisine bağlı toksisite olarak değerlendirildi.",
        "anlatim": "İnternetten alınan alıç kökü tableti sonrası yavaş nabız ve kas ağrıları belgelendi. Gözlemle düzeldi. Bu zehirlenme olgusudur. Bu metin tıbbi tavsiye değildir.",
    },
    "76": {
        "baslik": "Yeşil çay özütüyle ağır karaciğer yetmezliği",
        "sorun": "Kişi, zayıflama için satılan yeşil çay hidroalkolik özütünü (Exolise) kendi kendine kullanırken ani ve ağır karaciğer yetmezliği (fulminan hepatit) geliştirdi.",
        "yaklasim": "Klinik değerlendirme yapıldı; karaciğer nakli gerekti.",
        "sonuc": "Fulminan hepatit nedeniyle karaciğer nakli yapıldığı bildirildi.",
        "anlatim": "Zayıflama için satılan yeşil çay özütünü kendi kendine kullanan kişide ani ve ağır karaciğer yetmezliği gelişti. Karaciğer nakli gerekti. Bu toksisite uyarısıdır. Bu metin tıbbi tavsiye değildir.",
    },
}


def main():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    out = {}
    missing = []
    for item in raw:
        sid = str(item["id"])
        if sid not in REWRITES:
            missing.append(sid)
            continue
        r = REWRITES[sid]
        out[sid] = {
            **r,
            "pubmedId": item["pmid"],
            "pubmedUrl": item["url"],
            "makaleBasligi": item["title"],
            "yil": item["year"],
            "kaynakAdi": item["kaynakAdi"],
        }
    if missing:
        raise SystemExit(f"Missing rewrites for ids: {missing}")
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)} items to {OUT}")


if __name__ == "__main__":
    main()
