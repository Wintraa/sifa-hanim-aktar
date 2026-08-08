# -*- coding: utf-8 -*-
"""Eksik bitkileri güvenle ekler ve yalnızca yeni kayıtlar için SVG üretir."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
SVG_DIR = ROOT / "assets" / "plants"

# ad, botanik ad, tür, kısa kullanım/özellik notu
PLANTS = [
("Reyhan", "Ocimum basilicum var. purpureum", "Aromatik Bitkiler", "kendine özgü kokusu ve yemeklere verdiği renk"),
("Tarhun", "Artemisia dracunculus", "Aromatik Bitkiler", "anasonu andıran aroması ve mutfaktaki kullanımı"),
("Maydanoz", "Petroselinum crispum", "Aromatik Bitkiler", "taze yaprakları ve ferah aroması"),
("Dereotu", "Anethum graveolens", "Aromatik Bitkiler", "ince yaprakları ve belirgin aroması"),
("Kakule", "Elettaria cardamomum", "Aromatik Bitkiler", "tohum kapsüllerinin yoğun kokusu"),
("Vanilya", "Vanilla planifolia", "Aromatik Bitkiler", "fermente kapsüllerinden elde edilen tatlı aroması"),
("Ylang-Ylang", "Cananga odorata", "Aromatik Bitkiler", "çiçeklerinin yoğun ve çiçeksi kokusu"),
("Paçuli", "Pogostemon cablin", "Aromatik Bitkiler", "yapraklarının topraksı ve kalıcı kokusu"),
("Bergamot", "Citrus bergamia", "Aromatik Bitkiler", "kabuk yağının narenciye karakteri"),
("Lale", "Tulipa gesneriana", "Süs Bitkileri", "ilkbaharda açan gösterişli çiçekleri"),
("Ortanca", "Hydrangea macrophylla", "Süs Bitkileri", "büyük çiçek kümeleri ve bahçe görünümü"),
("Begonya", "Begonia semperflorens", "Süs Bitkileri", "uzun süre çiçekli kalabilen yapısı"),
("Açelya", "Rhododendron simsii", "Süs Bitkileri", "canlı renkli çiçekleri ve çalı formu"),
("Menekşe", "Viola odorata", "Süs Bitkileri", "zarif çiçekleri ve hoş kokusu"),
("Kasımpatı", "Chrysanthemum morifolium", "Süs Bitkileri", "sonbahar renkleri ve dayanıklı çiçekleri"),
("Sardunya", "Pelargonium hortorum", "Süs Bitkileri", "balkonlara uygun çiçekli yapısı"),
("Şakayık", "Paeonia lactiflora", "Süs Bitkileri", "katmerli çiçekleri ve kuvvetli görünümü"),
("Nergis", "Narcissus poeticus", "Süs Bitkileri", "ilkbahar başındaki kokulu çiçekleri"),
("Sümbül", "Hyacinthus orientalis", "Süs Bitkileri", "salkım çiçekleri ve belirgin kokusu"),
("Zambak", "Lilium candidum", "Süs Bitkileri", "iri çiçekleri ve zarif duruşu"),
("Camgüzeli", "Impatiens walleriana", "Süs Bitkileri", "yarı gölgede açan renkli çiçekleri"),
("Paşa Kılıcı", "Sansevieria trifasciata", "Süs Bitkileri", "dikey, dayanıklı yaprakları"),
("Deve Tabanı", "Monstera deliciosa", "Süs Bitkileri", "delikli büyük yaprakları"),
("Barış Çiçeği", "Spathiphyllum wallisii", "Süs Bitkileri", "parlak yaprakları ve beyaz çiçek örtüleri"),
("Aşk Merdiveni", "Nephrolepis exaltata", "Süs Bitkileri", "sarkık ve gür yaprakları"),
("Atatürk Çiçeği", "Euphorbia pulcherrima", "Süs Bitkileri", "kış dönemindeki kırmızı brahteleri"),
("Kauçuk Bitkisi", "Ficus elastica", "Süs Bitkileri", "iri, parlak yaprakları"),
("Yucca", "Yucca elephantipes", "Süs Bitkileri", "gövde üzerinde yükselen kılıç biçimli yaprakları"),
("Kalanşo", "Kalanchoe blossfeldiana", "Süs Bitkileri", "etli yaprakları ve uzun ömürlü çiçekleri"),
("Begonvil", "Bougainvillea glabra", "Süs Bitkileri", "renkli brahteleri ve sarılıcı gelişimi"),
("Mimoza", "Acacia dealbata", "Süs Bitkileri", "sarı püskül çiçekleri ve hafif kokusu"),
("Ginseng", "Panax ginseng", "Tıbbi Bitkiler", "geleneksel olarak enerji ve dayanıklılık desteği"),
("Ginkgo Biloba", "Ginkgo biloba", "Tıbbi Bitkiler", "geleneksel olarak bilişsel işlevlere destek amacı"),
("Karahindiba", "Taraxacum officinale", "Tıbbi Bitkiler", "geleneksel sindirim ve sıvı dengesi desteği"),
("Çoban Çantası", "Capsella bursa-pastoris", "Tıbbi Bitkiler", "geleneksel bitkisel çay uygulamaları"),
("Ökse Otu", "Viscum album", "Tıbbi Bitkiler", "yalnızca uzman gözetiminde değerlendirilen geleneksel kullanım"),
("Sinameki", "Senna alexandrina", "Tıbbi Bitkiler", "kısa süreli bağırsak hareketi desteği"),
("Kedi Otu", "Valeriana officinalis", "Tıbbi Bitkiler", "geleneksel rahatlama ve uyku rutini desteği"),
("Çarkıfelek", "Passiflora incarnata", "Tıbbi Bitkiler", "rahatlama amaçlı geleneksel kullanım"),
("Deve Dikeni", "Silybum marianum", "Tıbbi Bitkiler", "geleneksel karaciğer fonksiyonu desteği"),
("Enginar Yaprağı", "Cynara scolymus", "Tıbbi Bitkiler", "geleneksel sindirim desteği"),
("Kudret Narı", "Momordica charantia", "Tıbbi Bitkiler", "geleneksel beslenme ve bitkisel uygulamalar"),
("Şahtere Otu", "Fumaria officinalis", "Tıbbi Bitkiler", "geleneksel sindirim rahatlığı desteği"),
("Havlıcan", "Alpinia officinarum", "Tıbbi Bitkiler", "baharatlı köksapı ile geleneksel kullanım"),
("Mahlep", "Prunus mahaleb", "Tıbbi Bitkiler", "aromatik çekirdeğiyle geleneksel mutfak kullanımı"),
("Üzerlik Otu", "Peganum harmala", "Tıbbi Bitkiler", "geleneksel kullanım geçmişi bulunan tohumları"),
("Eğir Kökü", "Acorus calamus", "Tıbbi Bitkiler", "aromatik köksapıyla geleneksel uygulamalar"),
("Sinir Otu", "Plantago major", "Tıbbi Bitkiler", "geleneksel cilt ve solunum rahatlığı desteği"),
("Ayı Üzümü", "Arctostaphylos uva-ursi", "Tıbbi Bitkiler", "geleneksel idrar yolu desteği"),
("Hayıt Otu", "Vitex agnus-castus", "Tıbbi Bitkiler", "geleneksel kadın sağlığı rutinleri desteği"),
("Aslanpençesi", "Alchemilla vulgaris", "Tıbbi Bitkiler", "geleneksel kadın sağlığı uygulamaları"),
("Ayrık Otu", "Elymus repens", "Tıbbi Bitkiler", "geleneksel sıvı dengesi desteği"),
("At Kestanesi", "Aesculus hippocastanum", "Tıbbi Bitkiler", "haricen bacak konforu için geleneksel kullanım"),
("Geven Otu", "Astragalus membranaceus", "Tıbbi Bitkiler", "geleneksel bağışıklık desteği"),
("Altınbaşak", "Solidago virgaurea", "Tıbbi Bitkiler", "geleneksel sıvı dengesi desteği"),
("Gilaburu", "Viburnum opulus", "Tıbbi Bitkiler", "meyvesiyle geleneksel içecek kullanımı"),
("Hünnap", "Ziziphus jujuba", "Tıbbi Bitkiler", "meyvesiyle geleneksel beslenme desteği"),
("Alıç", "Crataegus monogyna", "Tıbbi Bitkiler", "geleneksel kalp-damar rutini desteği"),
("Yeşil Çay Bitkisi", "Camellia sinensis", "Tıbbi Bitkiler", "antioksidan içeren yaprakları"),
("Goji Berry", "Lycium barbarum", "Tıbbi Bitkiler", "meyvesiyle geleneksel beslenme desteği"),
("Çobançökerten", "Tribulus terrestris", "Tıbbi Bitkiler", "geleneksel canlılık desteği"),
("Pelin Otu", "Artemisia absinthium", "Tıbbi Bitkiler", "acı aromasıyla geleneksel sindirim kullanımı"),
("Yarpuz", "Mentha pulegium", "Tıbbi Bitkiler", "nane benzeri kokusuyla geleneksel kullanım"),
("Şevketi Bostan", "Cnicus benedictus", "Tıbbi Bitkiler", "geleneksel sindirim uygulamaları"),
("Öksürük Otu", "Tussilago farfara", "Tıbbi Bitkiler", "geleneksel solunum yolu rahatlığı desteği"),
("Mersin Bitkisi", "Myrtus communis", "Tıbbi Bitkiler", "aromatik yapraklarıyla geleneksel kullanım"),
("Söğüt Kabuğu", "Salix alba", "Tıbbi Bitkiler", "geleneksel ağrı konforu desteği"),
("Centiyane", "Gentiana lutea", "Tıbbi Bitkiler", "acı köküyle geleneksel sindirim kullanımı"),
]

PALETTES = [("#F5EFE6", "#8D7B68", "#C8B6A6", "#A8A196"), ("#F3EDE4", "#6B8F71", "#A084E8", "#C8B6A6"), ("#F7F1E8", "#8D7B68", "#D4A373", "#A8A196"), ("#F2EBE3", "#7A6A5A", "#A084E8", "#9AAE8E")]

def normalise(value):
    value = value.casefold().replace("ı", "i")
    return "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c) and c.isalnum())

def slugify(value):
    value = normalise(value)
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "bitki"

def make_svg(name, plant_id):
    bg, accent, petal, leaf = PALETTES[plant_id % len(PALETTES)]
    safe = name.replace("&", "&amp;")
    return f'''<svg width="1200" height="900" viewBox="0 0 1200 900" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="900" rx="48" fill="{bg}"/><rect x="52" y="52" width="1096" height="796" rx="36" fill="#FDFBF7" stroke="{petal}" stroke-width="6"/>
  <circle cx="220" cy="180" r="70" fill="{petal}" opacity=".35"/><circle cx="980" cy="220" r="110" fill="{leaf}" opacity=".28"/>
  <path d="M600 700V300" stroke="{accent}" stroke-width="16" stroke-linecap="round"/><path d="M600 480C485 360 390 430 360 530C480 550 565 530 600 480Z" fill="{leaf}"/><path d="M600 520C720 390 825 450 850 550C730 570 640 555 600 520Z" fill="{petal}"/>
  <circle cx="600" cy="285" r="82" fill="{petal}"/><circle cx="545" cy="245" r="36" fill="#FDFBF7"/><circle cx="655" cy="245" r="36" fill="#FDFBF7"/><circle cx="600" cy="335" r="32" fill="{accent}"/>
  <text x="600" y="790" text-anchor="middle" fill="#4A3E3D" font-family="Arial, sans-serif" font-size="48" font-weight="700">{safe}</text>
</svg>\n'''

def fields(ad, botanik, tur, note):
    if tur == "Süs Bitkileri":
        return {
            "genelTavsiyeMetni": f"{ad}, {note} sayesinde ev, balkon ve bahçelerde öne çıkan bir süs bitkisidir. Uygun ışık ve dengeli sulama ile bulunduğu alana uzun süre canlılık katabilir.",
            "temelBilgiler": {"turkceAdi": ad, "botanikAdi": botanik, "bitkiTuru": "Süs ve peyzaj bitkisi"},
            "saglikKullanim": {"faydalari": "Dekoratif görünümüyle yaşam alanlarında sakin ve yeşil bir atmosfer oluşturmaya yardımcı olabilir.", "kullanimSekli": "Saksıda, balkonda veya iklime uygun bahçelerde dekoratif amaçla yetiştirilir.", "yanEtkilerUyarilar": "Bazı süs bitkileri yenildiğinde evcil hayvanlar ve çocuklar için zararlı olabilir; bitki özsuyu ile temas sonrası eller yıkanmalıdır."},
            "cografyaMevsim": {"yetistigiYerler": "Türüne uygun ılıman, korunaklı dış mekânlar ile aydınlık iç mekânlar", "hasatMevsimi": "Dekoratif yetiştiricilikte hasat uygulanmaz", "ciceklenmeZamani": "Tür ve yetiştirme koşullarına göre değişir"},
            "bakimYetistirme": {"isikIhtiyaci": "Aydınlık ortam; türüne göre doğrudan veya filtrelenmiş güneş", "sulamaSikligi": "Toprağın üst kısmı kurudukça kontrollü sulama", "toprakTipi": "Organik maddeli, havadar ve iyi drene olan saksı toprağı"},
        }
    if tur == "Aromatik Bitkiler":
        return {
            "genelTavsiyeMetni": f"{ad}, {note} ile öne çıkan aromatik bir bitkidir. Taze ya da uygun şekilde kurutulmuş kısımları mutfak ve koku uygulamalarına ölçülü biçimde eşlik edebilir.",
            "temelBilgiler": {"turkceAdi": ad, "botanikAdi": botanik, "bitkiTuru": "Aromatik bitki"},
            "saglikKullanim": {"faydalari": "Kokusu ve aroması rahatlatıcı bir ritüele veya dengeli beslenmeye destek olabilir.", "kullanimSekli": "Türüne uygun kısmı taze, kurutulmuş, baharat veya kontrollü demleme biçiminde kullanılabilir.", "yanEtkilerUyarilar": "Uçucu yağlar ağızdan gelişigüzel alınmamalı ve cilde seyreltilmeden sürülmemelidir. Hamilelikte, emzirmede ve düzenli ilaç kullanımında uzmana danışılmalıdır."},
            "cografyaMevsim": {"yetistigiYerler": "İklimine uygun bahçeler, saksılar ve kontrollü üretim alanları", "hasatMevsimi": "Aromanın yoğun olduğu büyüme döneminde", "ciceklenmeZamani": "Tür ve yetiştirme koşullarına göre değişir"},
            "bakimYetistirme": {"isikIhtiyaci": "Çoğunlukla bol ışık veya yarı güneş", "sulamaSikligi": "Toprak hafif kurudukça; köklerde su biriktirmeden", "toprakTipi": "Gevşek, besince dengeli ve iyi drene olan toprak"},
        }
    return {
        "genelTavsiyeMetni": f"{ad}, {note} için geleneksel uygulamalarda değerlendirilen bir bitkidir. Bitkisel kullanım kişiden kişiye değişebilir; tıbbi tanı ve tedavinin yerine geçmez.",
        "temelBilgiler": {"turkceAdi": ad, "botanikAdi": botanik, "bitkiTuru": "Tıbbi bitki"},
        "saglikKullanim": {"faydalari": "Geleneksel kullanımı günlük iyi oluşa destek olabilir; etkileri için bilimsel kanıtın düzeyi bitkiye ve kullanım biçimine göre değişir.", "kullanimSekli": "Uygun bitki kısmı, güvenilir üründen ve önerilen miktarda çay, baharat veya harici uygulama şeklinde kullanılabilir.", "yanEtkilerUyarilar": "Hamilelik, emzirme, kronik hastalık ve düzenli ilaç kullanımında hekime veya eczacıya danışılmalıdır. Alerji, beklenmeyen belirti veya etkileşim riskinde kullanım bırakılmalıdır."},
        "cografyaMevsim": {"yetistigiYerler": "Türüne göre ılıman bölgeler, kültür alanları veya doğal habitatlar", "hasatMevsimi": "Kullanılan kök, yaprak, çiçek veya meyve kısmına göre değişir", "ciceklenmeZamani": "Tür ve iklim koşullarına göre değişir"},
        "bakimYetistirme": {"isikIhtiyaci": "Türüne göre güneşli veya yarı gölgeli alan", "sulamaSikligi": "Toprak nemi gözlenerek düzenli fakat aşırıya kaçmadan", "toprakTipi": "İyi drene olan, türün doğal isteğine uygun toprak"},
    }

def main():
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    existing_names = {normalise(p["ad"]) for p in plants}
    existing_botanical = {normalise(p.get("botanikAd", "")) for p in plants}
    aliases = {"altinotu": "altinotu", "aynisafa": "aynisefa"}
    added, skipped = [], []
    next_id = max((p["id"] for p in plants), default=37) + 1
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    for ad, botanik, tur, note in PLANTS:
        name_key = aliases.get(normalise(ad), normalise(ad))
        bot_key = normalise(botanik)
        if name_key in existing_names or bot_key in existing_botanical:
            skipped.append(ad)
            continue
        record = {"id": next_id, "ad": ad, "botanikAd": botanik, "tur": tur, "resimUrl": f"assets/plants/{next_id:02d}-{slugify(ad)}.svg"}
        record.update(fields(ad, botanik, tur, note))
        plants.append(record)
        (SVG_DIR / f"{next_id:02d}-{slugify(ad)}.svg").write_text(make_svg(ad, next_id), encoding="utf-8")
        existing_names.add(name_key); existing_botanical.add(bot_key)
        added.append((next_id, ad)); next_id += 1
    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Atlanan: {len(skipped)}")
    print(f"Eklenen: {len(added)}")
    print(f"Yeni toplam: {len(plants)}")
    print("Eklenen kayıtlar:", ", ".join(f"{i} {ad}" for i, ad in added))

# Kullanıcının 100 bitkilik kaynağında yer alıp ilk veri setinde zaten bulunanlar.
# Bunlar da aynı eşleştirme yolundan geçirilir; bu sayede betik tekrarlı çalıştırmada güvenlidir.
SOURCE_DUPLICATES = [
    (ad, "", "", "") for ad in [
        "Biberiye", "Kekik", "Nane", "Fesleğen", "Lavanta", "Adaçayı", "Defne", "Melisa",
        "Kişniş", "Zencefil", "Zerdeçal", "Kimyon", "Rezene", "Anason", "Çörek Otu", "Safran",
        "Gül", "Orkide", "Yasemin",
        "Sarı Kantaron", "Papatya", "Ekinezya", "Ihlamur", "Kuşburnu", "Aloe Vera", "Isırgan Otu",
        "Civanperçemi", "Hatmi Çiçeği", "Meyan Kökü", "Altınotu", "Aynısafa", "Kara Mürver",
    ]
]
PLANTS = SOURCE_DUPLICATES + PLANTS


if __name__ == "__main__":
    main()




