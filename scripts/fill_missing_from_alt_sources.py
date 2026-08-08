# -*- coding: utf-8 -*-
"""PFAF'ta eksik veya siteye yansımamış tıbbi bilgileri tamamlar.

1) Ham PFAF metninden etki etiketlerini yeniden çıkarır (çeviri kaçmış kayıtlar).
2) PFAF'ta 'None known' olanlar için güvenilir alternatif kaynaklar kullanır
   (hakemli dergi, PROSEA/Pl@ntUse, Kew, Merck Manual vb.).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
RAW = ROOT / "data" / "pfaf" / "raw"

sys.path.insert(0, str(ROOT / "scripts"))
from build_site_from_pfaf import edible_summary, medicinal_actions  # noqa: E402
from pfaf_terms import ACTIONS  # noqa: E402


def slugify(latin: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", latin.lower()).strip("-")


def capitalize_tr(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    first = text[0]
    tr_map = {"i": "İ", "ı": "I", "ş": "Ş", "ğ": "Ğ", "ü": "Ü", "ö": "Ö", "ç": "Ç"}
    if first in tr_map:
        return tr_map[first] + text[1:]
    return first.upper() + text[1:]


def ensure_period(text: str) -> str:
    text = (text or "").strip()
    if text and not text.endswith((".", "!", "?")):
        text += "."
    return text


def prose_actions(med: str) -> str:
    """Cümle içindeki virgüllü etki listelerini yakala (PFAF düzyazı formatı)."""
    text = re.sub(
        r"Plants For A Future can not take any responsibility.*?medicinally\.",
        "",
        med or "",
        flags=re.I | re.S,
    )
    found: list[str] = []
    # "as an anodyne, anti-inflammatory, ..." veya "are anodyne, antiseptic, ..."
    for m in re.finditer(
        r"(?:as an?|are|being)\s+([a-z][a-z\-\s,]{10,220}?)(?:\.|\[|$)",
        text,
        flags=re.I,
    ):
        chunk = m.group(1)
        chunk = re.sub(r"\band\b", ",", chunk, flags=re.I)
        for part in re.split(r"[,;/]+", chunk):
            key = part.strip().lower()
            key = re.sub(r"\s+", " ", key)
            if key in ACTIONS and ACTIONS[key] not in found:
                found.append(ACTIONS[key])
    # Ayrıca bilinen tekil etiketleri metinde ara
    for key, tr in ACTIONS.items():
        if re.search(rf"\b{re.escape(key)}\b", text, re.I) and tr not in found:
            # Çok kısa genel kelimeleri atla (skin vb. ACTIONS'ta olabilir)
            if len(key) < 5:
                continue
            found.append(tr)
        if len(found) >= 14:
            break
    return ", ".join(found)


def load_raw(latin: str) -> dict | None:
    path = RAW / f"{slugify(latin)}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


# PFAF tıbbi kaydı yok / yetersiz → alternatif güvenilir kaynaklar
ALT_FILL = {
    207: {  # Dittrichia viscosa — J Ethnopharmacol / JTCME / MDPI derlemeleri
        "saglikKullanim": {
            "faydalari": (
                "Akdeniz ethnobotanik kayıtlarında iltihap giderici, ateş düşürücü, antiseptik, "
                "antimikrobiyal, romatizma ağrılarında destekleyici, yara ve cilt apselerinde harici "
                "kullanılan; solunum (bronşit vb.) ve sindirim şikayetlerinde geleneksel olarak "
                "değerlendirilen bir bitkidir. Yaprak özütlerinde antioksidan ve antibakteriyel "
                "etkiler laboratuvar çalışmalarında gösterilmiştir."
            ),
            "kullanimSekli": (
                "Geleneksel olarak yaprak, kök veya çiçekli dallar; kaynatma (dekoksiyon), "
                "lapa/kataplasma veya yağlı harici preparat biçiminde kullanılır. "
                "Yenilebilir gıda kullanımı için güvenilir kayıt sınırlıdır."
            ),
            "yanEtkilerUyarilar": (
                "İç kullanımda doz ve süre için uzman görüşü alınmalıdır. "
                "Ciltte tahriş veya alerji olursa kullanım kesilmelidir. "
                "Gebelikte ve çocuklarda doktor kontrolü olmadan kullanılmamalıdır."
            ),
        },
        "cografyaMevsim": {
            "hasatMevsimi": "Yaprak ve çiçekli sürgünler genellikle yaz sonu–sonbahar çiçeklenme döneminde toplanır.",
        },
        "kaynak_ek": {
            "ad": (
                "Plants For A Future (pfaf.org) + JTCME 2024 derleme / MDPI Molecules 2022 "
                "(Dittrichia viscosa ethnomedikal ve farmakolojik çalışmalar)"
            ),
            "altUrl": "https://doi.org/10.1016/j.jtcme.2024.03.012",
            "not": (
                "PFAF tıbbi etki listesi boştur (0/5); ethnomedikal ve farmakolojik bilgiler "
                "hakemli derlemelerden tamamlanmıştır."
            ),
        },
    },
    212: {  # Nioli — PROSEA / Pl@ntUse
        "saglikKullanim": {
            "faydalari": (
                "Yapraklarından damıtılan nioli (niaouli / gomen) uçucu yağı antiseptik, "
                "balgam söktürücü ve solunum yolu rahatlatıcı olarak bilinir; Fransa farmasötik "
                "geleneğinde öksürük, boğmaca, romatizma, nevralji ve kronik bronşiyal "
                "katarrda kajeput/okaliptüs yağına alternatif olarak kullanılmıştır. "
                "Aromaterapide sinüzit, boğaz ve bronşit şikayetlerinde destekleyici "
                "inhalasyon/harici kullanımı yaygındır."
            ),
            "kullanimSekli": (
                "Yaprak ve uç sürgünlerden buhar damıtımıyla elde edilen uçucu yağ; "
                "öksürük pastilleri, gargara, diş macunu aroması ve seyreltilmiş harici/"
                "inhalasyon preparatlarında kullanılır."
            ),
            "yanEtkilerUyarilar": (
                "Uçucu yağ yutulmamalıdır; seyreltilmeden cilde uygulanmamalıdır. "
                "Çocuklarda, gebelikte ve hassas ciltlerde dikkatli kullanılmalıdır. "
                "1,8-sineol chemotipi baskındır; yüksek sineollü okaliptüs yağı ile karıştırma/"
                "tağşiş riski vardır. Florida’da çiçek salgıları hassas kişilerde solunum "
                "tahrişi bildirilmiştir. Bazı bölgelerde istilacı olabilir."
            ),
        },
        "cografyaMevsim": {
            "yetistigiYerler": (
                "Doğu Avustralya kıyıları (Yeni Güney Galler–Queensland), güney Yeni Gine ve "
                "Yeni Kaledonya; tropik–subtropik kıyı ovaları, tatlı su bataklıkları ve "
                "estuar kenarlarında yetişir. Florida vb. yerlerde istilacı olabilir."
            ),
            "hasatMevsimi": (
                "Nioli yağı için yapraklar doğal meşcerelerden dal budanarak toplanır; "
                "çiçeklenme Avustralya’da genellikle sonbahar–kıştır."
            ),
            "ciceklenmeZamani": "Sonbahar - kış (Avustralya); iklime göre yıl boyu çiçek görülebilir.",
        },
        "bakimYetistirme": {
            "isikIhtiyaci": "Tam güneş veya açık yarı gölge ister.",
            "sulamaSikligi": "Nemli–bataklık alanlara uyarlıdır; mevsimsel su baskınını tolere eder.",
            "toprakTipi": (
                "Humuslu, genelde yüzeyde kumlu altta siltli/killi, organik maddece zengin "
                "ve sık ıslak topraklar; tuzlu rüzgâra kısmen dayanıklıdır."
            ),
        },
        "kaynak_ek": {
            "ad": "PROSEA / Pl@ntUse (Melaleuca quinquenervia) — PFAF'ta tür sayfası yok",
            "url": "https://plantuse.plantnet.org/en/Melaleuca_quinquenervia_(PROSEA)",
            "altUrl": "https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:598027-1",
            "not": "Niaouli yağı ve ekoloji bilgisi PROSEA monografından; taksonomi Kew POWO ile doğrulanmıştır.",
        },
    },
    135: {  # Helichrysum italicum — PubMed / PMC derlemeleri
        "saglikKullanim": {
            "faydalari": (
                "Akdeniz geleneksel tıbbında alerji, soğuk algınlığı, öksürük, cilt, karaciğer/"
                "safra ve iltihaplı durumlar için kullanılır. Uçucu yağı ve özütleri antimikrobiyal, "
                "iltihap giderici, yara ve hematom/çürük iyileşmesini destekleyici etkileriyle "
                "aromaterapi ve cilt bakımında değerlendirilir."
            ),
            "kullanimSekli": (
                "Çiçek ve yapraklar çay/baharat olarak; uçucu yağ ise seyreltilmiş harici "
                "uygulama ve aromaterapide kullanılır."
            ),
            "yanEtkilerUyarilar": (
                "Uçucu yağ yutulmamalıdır. Seyreltilmeden cilde uygulanması önerilmez "
                "(özel uygulamalar hariç, uzman rehberliğinde). Alerjik reaksiyon bildirilmiştir; "
                "hassas ciltlerde yama testi yapılmalıdır."
            ),
        },
        "cografyaMevsim": {
            "hasatMevsimi": "Çiçekli sürgünler yaz çiçeklenme döneminde hasat edilir.",
        },
        "kaynak_ek": {
            "ad": (
                "Plants For A Future (pfaf.org) + PubMed/PMC derlemeleri "
                "(Helichrysum italicum traditional use & pharmacology)"
            ),
            "altUrl": "https://pubmed.ncbi.nlm.nih.gov/24239849/",
            "not": (
                "PFAF tıbbi etki listesi boştur (0/5); ethnomedikal ve farmakolojik bilgiler "
                "hakemli derlemelerden tamamlanmıştır."
            ),
        },
    },
}

# PFAF düzyazısından Türkçe özet (etiket çıkarma yetersiz kaldığında)
PROSE_TR = {
    1: {  # Matricaria chamomilla
        "faydalari": (
            "Sindirim bozuklukları, sinir gerginliği ve huzursuzlukta dahili; cilt sorunlarında "
            "harici kullanılır. Çiçek demlemesi ağrı dindirici, iltihap giderici, antiseptik, "
            "kas spazmı çözücü, gaz giderici, safra söktürücü, terletici, adet söktürücü, "
            "ateş düşürücü, sakinleştirici, mideyi güçlendirici, tonik ve damar genişletici "
            "etkileriyle anılır."
        ),
        "kullanimSekli": "Çiçeklerin demlenmesi (infüzyon); dahili çay ve harici yıkama/lapa.",
    },
    86: {  # Mentha piperita
        "faydalari": (
            "Antiseptik ve sindirim destekleyici; ateş, baş ağrısı ve hafif rahatsızlıklarda "
            "geleneksel çay olarak kullanılır. Yaprak ve çiçekli bitki ağrı dindirici, "
            "antiseptik, kas spazmı çözücü, gaz giderici, safra söktürücü, terletici, "
            "serinletici, mideyi güçlendirici, tonik ve damar genişletici etkileriyle kaydedilmiştir."
        ),
        "kullanimSekli": "Yapraklardan çay; uçucu yağ aromaterapi ve harici preparatlarda (seyreltilmiş).",
        "yanEtkilerUyarilar": (
            "Gebelerde yüksek dozda kullanılmamalıdır (PFAF uyarısı). "
            "Uçucu yağ yutulmamalı ve seyreltilmeden cilde uygulanmamalıdır."
        ),
    },
    116: {  # Ocimum tenuiflorum — PFAF + Merck / PMC
        "faydalari": (
            "Ayurveda’da önemli adaptogen bitkidir: antiseptik, terletici, ateş düşürücü, "
            "kas spazmı çözücü, ağrı dindirici, antibakteriyel, bağışıklık ve sinir sistemini "
            "destekleyici, iltihap giderici ve sindirim dostudur. Araştırma kayıtlarında kan "
            "şekeri düşürücü etki ve yaprak uçucu yağında antibakteriyel/antifungal aktivite "
            "bildirilmiştir; stres ve uyku destekleyici klinik çalışmalar mevcuttur."
        ),
        "kullanimSekli": "Çiçek, yaprak ve tohum; çay, demleme veya geleneksel preparatlar.",
        "yanEtkilerUyarilar": (
            "Gebelikte ve ilaç kullananlarda (özellikle diyabet ilaçları) hekime danışılmalıdır. "
            "Tıbbi amaçlı kullanımda doz için uzman görüşü alınmalıdır."
        ),
    },
    150: {  # Atropa belladonna
        "faydalari": (
            "Çok zehirli olmakla birlikte tıbbi geçmişi uzundur: göz ameliyatlarında pupil "
            "genişletici, bağırsak koliği ve peptik ülser semptomlarında, Parkinson "
            "tremor/rijiditesinde ve bazı mantar zehirlenmelerinde antidot olarak "
            "(yalnızca hekim kontrolünde) kullanılmıştır."
        ),
        "kullanimSekli": (
            "Yalnızca kalifiye hekim/eczacı denetiminde farmasötik preparat olarak. "
            "Evde demleme veya kendi kendine kullanım kesinlikle uygun değildir."
        ),
        "yanEtkilerUyarilar": (
            "Bitkinin tüm kısımları yüksek derecede zehirlidir. Amatör toplama ve kullanım "
            "ölümcül olabilir. Yalnızca uzman denetiminde kullanılır."
        ),
    },
    166: {  # Frangula alnus
        "faydalari": (
            "Orta Çağ’dan beri bilinen yumuşak müshildir. Kabuktaki antrakinonlar (yaklaşık "
            "%3–7) kolon duvarını uyararak yaklaşık 8–12 saat sonra bağırsak hareketi sağlar."
        ),
        "kullanimSekli": (
            "İyi kurutulmuş ve yeterli süre saklanmış kabuk (taze kabuk kusmaya yol açabilir). "
            "Standartlaştırılmış eczacılık preparatları tercih edilmelidir."
        ),
        "yanEtkilerUyarilar": (
            "Uzun süreli veya yüksek dozda kullanımda sıvı–elektrolit kaybı riski vardır. "
            "Bağırsak tıkanıklığı, iltihabi bağırsak hastalığı ve karın ağrısı durumunda "
            "kullanılmamalıdır. Gebelikte ve çocuklarda hekime danışılmalıdır."
        ),
    },
}


def fill_from_pfaf_raw(plant: dict) -> bool:
    """Boş fayda/kullanım alanlarını ham PFAF'tan doldur."""
    latin = plant.get("botanikAd") or ""
    raw = load_raw(latin)
    if not raw:
        return False

    health = plant.setdefault("saglikKullanim", {})
    changed = False

    fayda = (health.get("faydalari") or "").strip()
    if not fayda or fayda.startswith("PFAF kaynağında bilinen"):
        actions, _conds, _unk = medicinal_actions(raw.get("medicinalUses") or "")
        if not actions:
            actions = prose_actions(raw.get("medicinalUses") or "")
        # PROSE_TR öncelikli özet varsa onu kullan
        prose = PROSE_TR.get(plant["id"])
        if prose and prose.get("faydalari"):
            health["faydalari"] = ensure_period(prose["faydalari"])
            changed = True
        elif actions:
            health["faydalari"] = ensure_period(capitalize_tr(actions))
            changed = True

    kul = (health.get("kullanimSekli") or "").strip()
    if not kul or kul.startswith("PFAF kaynağında yenilebilir"):
        prose = PROSE_TR.get(plant["id"])
        if prose and prose.get("kullanimSekli"):
            health["kullanimSekli"] = ensure_period(prose["kullanimSekli"])
            changed = True
        else:
            edible = edible_summary(raw.get("edibleUses") or "")
            if edible:
                health["kullanimSekli"] = ensure_period(capitalize_tr(edible))
                changed = True

    uyar = (health.get("yanEtkilerUyarilar") or "").strip()
    prose = PROSE_TR.get(plant["id"])
    if prose and prose.get("yanEtkilerUyarilar"):
        if (not uyar) or uyar.startswith("Kaynakta bilinen"):
            health["yanEtkilerUyarilar"] = ensure_period(prose["yanEtkilerUyarilar"])
            changed = True

    return changed


def apply_alt(plant: dict) -> bool:
    pid = plant["id"]
    if pid not in ALT_FILL:
        return False
    fix = ALT_FILL[pid]
    if "saglikKullanim" in fix:
        plant.setdefault("saglikKullanim", {}).update(
            {k: ensure_period(v) if isinstance(v, str) else v for k, v in fix["saglikKullanim"].items()}
        )
    if "cografyaMevsim" in fix:
        plant.setdefault("cografyaMevsim", {}).update(fix["cografyaMevsim"])
    if "bakimYetistirme" in fix:
        plant.setdefault("bakimYetistirme", {}).update(fix["bakimYetistirme"])
    if "kaynak_ek" in fix:
        kaynak = plant.setdefault("kaynak", {})
        ek = fix["kaynak_ek"]
        kaynak["ad"] = ek.get("ad", kaynak.get("ad", ""))
        if ek.get("url"):
            kaynak["url"] = ek["url"]
        if ek.get("altUrl"):
            kaynak["altUrl"] = ek["altUrl"]
        if ek.get("not"):
            kaynak["not"] = ek["not"]
        kaynak["cekimTarihi"] = "2026-08-01"
    # genel tavsiye: Nioli için hafif güncelle
    if pid == 212:
        plant["genelTavsiyeMetni"] = (
            "Nioli (Melaleuca quinquenervia), Myrtaceae familyasından kışın da yeşil kalan, "
            "kalın kâğıtsı kabuklu bir ağaçtır (genelde 8–12 m, bazen 25 m). "
            "Doğu Avustralya, Yeni Gine ve Yeni Kaledonya kökenlidir; yapraklarından "
            "cineol bakımından zengin nioli (niaouli) uçucu yağı elde edilir."
        )
    if pid == 207:
        plant["genelTavsiyeMetni"] = (
            "Yapışkan Andız Otu (Dittrichia viscosa, eşanlam: Inula viscosa), Asteraceae "
            "familyasından yıllarca yaşayan, yapışkan ve kokulu bir Akdeniz bitkisidir. "
            "Yaklaşık 0,5 m boya ulaşır. PFAF tıbbi derece kaydı düşük olsa da Akdeniz "
            "ethnobotaniğinde cilt, romatizma ve solunum şikayetlerinde geleneksel kullanımı "
            "hakemli derlemelerde belgelenmiştir."
        )
    if pid == 135:
        # mevcut genel metni bozma; yalnızca sağlık alanları
        pass
    return True


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    pfaf_fixed = 0
    alt_fixed = 0

    for plant in plants:
        health = plant.get("saglikKullanim") or {}
        fayda = (health.get("faydalari") or "").strip()
        needs = (not fayda) or fayda.startswith("PFAF kaynağında")
        kul = (health.get("kullanimSekli") or "").strip()
        needs_kul = (not kul) or kul.startswith("PFAF kaynağında")

        if plant["id"] in ALT_FILL:
            if apply_alt(plant):
                alt_fixed += 1
            continue

        if needs or needs_kul or plant["id"] in PROSE_TR:
            if fill_from_pfaf_raw(plant):
                pfaf_fixed += 1

    DATA.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PFAF ham veriden tamamlanan: {pfaf_fixed}")
    print(f"Alternatif kaynaktan tamamlanan: {alt_fixed}")

    # Kontrol: hâlâ boş tıbbi fayda (dekoratifler hariç kısmi)
    empty = []
    for p in plants:
        f = (p.get("saglikKullanim") or {}).get("faydalari") or ""
        if not f.strip():
            empty.append((p["id"], p["ad"]))
    print(f"Hâlâ boş fayda alanı: {len(empty)}")
    for item in empty[:25]:
        print(" -", item)


if __name__ == "__main__":
    main()
