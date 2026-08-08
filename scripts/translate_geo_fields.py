# -*- coding: utf-8 -*-
"""yetistigiYerler Range kisimlarindaki Ingilizceyi Turkceye cevirir.

Yaklasim:
  1) Metni "Doğal ortamı:" oncesi (Range) ve sonrasi (Habitat TR) diye ayir.
  2) Range kisminda once uzun kalip, sonra ulke/bolge, sonra baglac cevir.
  3) Habitat kismina dokunma (zaten Turkce).
  4) Kaynak kisaltmalarini Turkce aciklamaya cevir.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"

# ---------------------------------------------------------------------------
# 1) Uzun / ozel kalıplar (IGNORECASE, once uygulanir)
# ---------------------------------------------------------------------------
PHRASES: list[tuple[str, str]] = [
    (
        r"Widely cultivated in Tropical areas,\s*it probably originated in",
        "Tropik bölgelerde yaygın olarak yetiştirilir; muhtemelen kökeni",
    ),
    (
        r"The plant has become naturalized at higher elevations in the Tropics\.?",
        "Tropiklerde yüksek rakımlarda doğallaşmıştır.",
    ),
    (
        r"Temperate regions throughout the world",
        "Dünyanın ılıman bölgeleri",
    ),
    (
        r"Throughout most of the Northern hemisphere",
        "Kuzey yarımkürenin büyük bölümü",
    ),
    (
        r"Throughout most of",
        "Büyük bölümü:",
    ),
    (
        r"A virtually cosmopolitan plant, found in most regions of the world including",
        "Neredeyse kozmopolit bir bitki; Britanya dahil dünyanın çoğu bölgesinde bulunur:",
    ),
    (
        r"A virtually cosmopolitan plant,?\s*found in most regions of the world,?\s*including",
        "Neredeyse kozmopolit bir bitki; dünyanın çoğu bölgesinde bulunur,",
    ),
    (
        r"A hybrid garden origin\.?",
        "Melez bahçe kökenlidir.",
    ),
    (
        r"A garden hybrid\.?",
        "Bahçe melezi.",
    ),
    (
        r"of hybrid origin\.?",
        "melez kökenli",
    ),
    (
        r"origin of the plant is obscure\.?",
        "bitkinin kökeni belirsizdir.",
    ),
    (
        r"Exact origin uncertain\.?",
        "Kesin kökeni belirsizdir.",
    ),
    (
        r"Original habitat is obscure\.?",
        "Asıl yetişme ortamı belirsizdir.",
    ),
    (
        r"Origin uncertain\.?",
        "Kökeni belirsizdir.",
    ),
    (
        r"Not known in the wild,?\s*probably arose as a form of\s*C\.\s*cardunculus\.?",
        "Yabani ortamda bilinmez; muhtemelen C. cardunculus'un bir formundan türemiştir.",
    ),
    (
        r"Not known wild,?\s*probably arose (?:as )?a form(?: of)?\s*C\.\s*cardunculus\.?",
        "Yabani ortamda bilinmez; muhtemelen C. cardunculus'un bir formundan türemiştir.",
    ),
    (
        r"An occasional garden escape in",
        "Ara sıra bahçeden kaçmış olarak bulunur:",
    ),
    (
        r"A garden escape in",
        "Bahçeden kaçmış olarak bulunur:",
    ),
    (
        r"An infrequent casual in",
        "Ara sıra geçici olarak bulunur:",
    ),
    (
        r"Naturalized in",
        "Doğallaştığı yerler:",
    ),
    (
        r"naturalized in",
        "doğallaştığı yerler:",
    ),
    (
        r"Possibly native of",
        "Muhtemelen anavatanı",
    ),
    (
        r"Probably native of",
        "Muhtemelen anavatanı",
    ),
    (
        r"Native of",
        "Anavatanı",
    ),
    (
        r"Native to",
        "Anavatanı",
    ),
    (
        r"south and east to",
        "güneye ve doğuya doğru",
    ),
    (
        r"north and east to",
        "kuzeye ve doğuya doğru",
    ),
    (
        r"south and west to",
        "güneye ve batıya doğru",
    ),
    (
        r"north and west to",
        "kuzeye ve batıya doğru",
    ),
    (r"east to", "doğuya doğru"),
    (r"west to", "batıya doğru"),
    (r"north to", "kuzeye doğru"),
    (r"south to", "güneye doğru"),
    (r"eastwards?\s*(?:to|-)?", "doğuya doğru "),
    (r"westwards?\s*(?:to|-)?", "batıya doğru "),
    (r"northwards?\s*(?:to|-)?", "kuzeye doğru "),
    (r"southwards?\s*(?:to|-)?", "güneye doğru "),
    # including X -> (X dahil)
    (r",\s*including\s+([^,.]+)", r" (\1 dahil)"),
    (r"\bincluding\b", "dahil"),
    # but excluding
    (r",\s*but excluding extreme north and south", ", aşırı kuzey ve güney hariç"),
    (r"but excluding extreme north and south", "aşırı kuzey ve güney hariç"),
    (r"but excluding", "hariç"),
    (r"\bexcluding\b", "hariç"),
    (r"\babsent\b", "yoktur:"),
    (r"\baround\b", "çevresinde"),
    (r"\bmany other areas\.?", "birçok başka bölge."),
    (r"\bCentral and\b", "Orta ve "),
    (r"\bC\.\s*and\b", "Orta ve "),
]

# ---------------------------------------------------------------------------
# 2) Yon / bolge kisaltmalari
# ---------------------------------------------------------------------------
ABBREVS: list[tuple[str, str]] = [
    (r"\bS\.W\.Asia\b", "Güneybatı Asya"),
    (r"\bS\.E\.Asia\b", "Güneydoğu Asya"),
    (r"\bN\.W\.Asia\b", "Kuzeybatı Asya"),
    (r"\bN\.E\.Asia\b", "Kuzeydoğu Asya"),
    (r"\bS\.W\.\s*Asia\b", "Güneybatı Asya"),
    (r"\bS\.E\.\s*Asia\b", "Güneydoğu Asya"),
    (r"\bW\.Asia\b", "Batı Asya"),
    (r"\bE\.Asia\b", "Doğu Asya"),
    (r"\bC\.Asia\b", "Orta Asya"),
    (r"\bS\.Asia\b", "Güney Asya"),
    (r"\bN\.Asia\b", "Kuzey Asya"),
    (r"\bS\.W\.\s*Europe\b", "Güneybatı Avrupa"),
    (r"\bS\.E\.\s*Europe\b", "Güneydoğu Avrupa"),
    (r"\bN\.W\.\s*Europe\b", "Kuzeybatı Avrupa"),
    (r"\bN\.E\.\s*Europe\b", "Kuzeydoğu Avrupa"),
    (r"\bS\.\s*Europe\b", "Güney Avrupa"),
    (r"\bN\.\s*Europe\b", "Kuzey Avrupa"),
    (r"\bC\.\s*Europe\b", "Orta Avrupa"),
    (r"\bW\.\s*Europe\b", "Batı Avrupa"),
    (r"\bE\.\s*Europe\b", "Doğu Avrupa"),
    (r"\bS\.W\.\s*Avrupa\b", "Güneybatı Avrupa"),
    (r"\bS\.E\.\s*Avrupa\b", "Güneydoğu Avrupa"),
    (r"\bS\.\s*Avrupa\b", "Güney Avrupa"),
    (r"\bN\.\s*Avrupa\b", "Kuzey Avrupa"),
    (r"\bC\.\s*Avrupa\b", "Orta Avrupa"),
    (r"\bW\.\s*Avrupa\b", "Batı Avrupa"),
    (r"\bE\.\s*Avrupa\b", "Doğu Avrupa"),
    (r"\bN\.\s*America\b", "Kuzey Amerika"),
    (r"\bS\.\s*America\b", "Güney Amerika"),
    (r"\bC\.\s*America\b", "Orta Amerika"),
    (r"\bN\.\s*Africa\b", "Kuzey Afrika"),
    (r"\bS\.\s*Africa\b", "Güney Afrika"),
    (r"\bE\.\s*Africa\b", "Doğu Afrika"),
    (r"\bW\.\s*Africa\b", "Batı Afrika"),
    (r"\bS\.\s*Fransa\b", "Güney Fransa"),
    (r"\bN\.\s*Fransa\b", "Kuzey Fransa"),
    (r"\bN\.\s*Yunanistan\b", "Kuzey Yunanistan"),
    (r"\bS\.W\.\s*Asya\b", "Güneybatı Asya"),
    (r"\bS\.E\.\s*Asya\b", "Güneydoğu Asya"),
]

# ---------------------------------------------------------------------------
# 3) Ulke / bolge adlari (uzun olanlar once)
# ---------------------------------------------------------------------------
PLACES: list[tuple[str, str]] = [
    (r"\bNew South Wales\b", "Yeni Güney Galler"),
    (r"\bCosta Rica\b", "Kosta Rika"),
    (r"\bSaudi Arabia\b", "Suudi Arabistan"),
    (r"\bSri Lanka\b", "Sri Lanka"),
    (r"\bNew Zealand\b", "Yeni Zelanda"),
    (r"\bUnited States\b", "Amerika Birleşik Devletleri"),
    (r"\bNorth America\b", "Kuzey Amerika"),
    (r"\bSouth America\b", "Güney Amerika"),
    (r"\bCentral America\b", "Orta Amerika"),
    (r"\bTropical Africa\b", "Tropik Afrika"),
    (r"\bTropical Asia\b", "Tropik Asya"),
    (r"\bTropical areas\b", "tropik bölgeler"),
    (r"\bCanary Islands\b", "Kanarya Adaları"),
    (r"\bBalearic Islands\b", "Balear Adaları"),
    (r"\bNorthern hemisphere\b", "Kuzey yarımküre"),
    (r"\bSouthern hemisphere\b", "Güney yarımküre"),
    (r"\bhemisphere\b", "yarımküre"),
    (r"\bMacaronesia\b", "Makaronezya"),
    (r"\bLapland\b", "Laponya"),
    (r"\bScandanavia\b", "İskandinavya"),
    (r"\bScandinavia\b", "İskandinavya"),
    (r"\bIceland\b", "İzlanda"),
    (r"\bEthiopia\b", "Etiyopya"),
    (r"\bAzores\b", "Azorlar"),
    (r"\bMadeira\b", "Madeira"),
    (r"\bCorsica\b", "Korsika"),
    (r"\bSardinia\b", "Sardinya"),
    (r"\bSicily\b", "Sicilya"),
    (r"\bCrete\b", "Girit"),
    (r"\bBalearics\b", "Balear Adaları"),
    (r"\bCanaries\b", "Kanarya Adaları"),
    (r"\bRoumania\b", "Romanya"),
    (r"\bRomania\b", "Romanya"),
    (r"\bBolivia\b", "Bolivya"),
    (r"\bColombia\b", "Kolombiya"),
    (r"\bNicaragua\b", "Nikaragua"),
    (r"\bHonduras\b", "Honduras"),
    (r"\bGuatemala\b", "Guatemala"),
    (r"\bPanama\b", "Panama"),
    (r"\bNigeria\b", "Nijerya"),
    (r"\bGabon\b", "Gabon"),
    (r"\bZaire\b", "Zaire"),
    (r"\bCongo\b", "Kongo"),
    (r"\bBhutan\b", "Bhutan"),
    (r"\bMyanmar\b", "Myanmar"),
    (r"\bBurma\b", "Myanmar"),
    (r"\bMongolia\b", "Moğolistan"),
    (r"\bVictoria\b", "Victoria"),
    (r"\bTasmania\b", "Tazmanya"),
    (r"\bQueensland\b", "Queensland"),
    (r"\bKentucky\b", "Kentucky"),
    (r"\bFlorida\b", "Florida"),
    (r"\bVirginia\b", "Virginia"),
    (r"\bOhio\b", "Ohio"),
    (r"\bMichigan\b", "Michigan"),
    (r"\bGeorgia\b", "Georgia"),
    (r"\bLouisiana\b", "Louisiana"),
    (r"\bTexas\b", "Teksas"),
    (r"\bSomalia\b", "Somali"),
    (r"\bSudan\b", "Sudan"),
    (r"\bSichuan\b", "Siçuan"),
    (r"\bSumatra\b", "Sumatra"),
    (r"\bPhilippines\b", "Filipinler"),
    (r"\bIndonesia\b", "Endonezya"),
    (r"\bMalaysia\b", "Malezya"),
    (r"\bThailand\b", "Tayland"),
    (r"\bVietnam\b", "Vietnam"),
    (r"\bPakistan\b", "Pakistan"),
    (r"\bAfghanistan\b", "Afganistan"),
    (r"\bNepal\b", "Nepal"),
    (r"\bIran\b", "İran"),
    (r"\bIraq\b", "Irak"),
    (r"\bSyria\b", "Suriye"),
    (r"\bLebanon\b", "Lübnan"),
    (r"\bIsrael\b", "İsrail"),
    (r"\bEgypt\b", "Mısır"),
    (r"\bMorocco\b", "Fas"),
    (r"\bAlgeria\b", "Cezayir"),
    (r"\bTunisia\b", "Tunus"),
    (r"\bLibya\b", "Libya"),
    (r"\bTurkey\b", "Türkiye"),
    (r"\bGreece\b", "Yunanistan"),
    (r"\bItaly\b", "İtalya"),
    (r"\bSpain\b", "İspanya"),
    (r"\bFrance\b", "Fransa"),
    (r"\bGermany\b", "Almanya"),
    (r"\bPortugal\b", "Portekiz"),
    (r"\bPoland\b", "Polonya"),
    (r"\bHungary\b", "Macaristan"),
    (r"\bBulgaria\b", "Bulgaristan"),
    (r"\bSerbia\b", "Sırbistan"),
    (r"\bCroatia\b", "Hırvatistan"),
    (r"\bAlbania\b", "Arnavutluk"),
    (r"\bUkraine\b", "Ukrayna"),
    (r"\bRussia\b", "Rusya"),
    (r"\bSweden\b", "İsveç"),
    (r"\bNorway\b", "Norveç"),
    (r"\bFinland\b", "Finlandiya"),
    (r"\bDenmark\b", "Danimarka"),
    (r"\bNetherlands\b", "Hollanda"),
    (r"\bBelgium\b", "Belçika"),
    (r"\bAustria\b", "Avusturya"),
    (r"\bSwitzerland\b", "İsviçre"),
    (r"\bCyprus\b", "Kıbrıs"),
    (r"\bBritain\b", "Britanya"),
    (r"\bEngland\b", "İngiltere"),
    (r"\bScotland\b", "İskoçya"),
    (r"\bWales\b", "Galler"),
    (r"\bIreland\b", "İrlanda"),
    (r"\bChina\b", "Çin"),
    (r"\bJapan\b", "Japonya"),
    (r"\bIndia\b", "Hindistan"),
    (r"\bKorea\b", "Kore"),
    (r"\bMexico\b", "Meksika"),
    (r"\bBrazil\b", "Brezilya"),
    (r"\bCanada\b", "Kanada"),
    (r"\bAustralia\b", "Avustralya"),
    (r"\bMediterranean\b", "Akdeniz"),
    (r"\bHimalayas\b", "Himalayalar"),
    (r"\bCaucasus\b", "Kafkasya"),
    (r"\bSiberia\b", "Sibirya"),
    (r"\bEurope\b", "Avrupa"),
    (r"\bAsia\b", "Asya"),
    (r"\bAfrica\b", "Afrika"),
    (r"\bAmerica\b", "Amerika"),
    (r"\bWestern\b", "Batı"),
    (r"\bwestern\b", "batı"),
    (r"\bEastern\b", "Doğu"),
    (r"\beastern\b", "doğu"),
    (r"\bNorthern\b", "Kuzey"),
    (r"\bnorthern\b", "kuzey"),
    (r"\bSouthern\b", "Güney"),
    (r"\bsouthern\b", "güney"),
    (r"\bCentral\b", "Orta"),
    (r"\bcentral\b", "orta"),
    (r"\bTropical\b", "Tropik"),
    (r"\btropical\b", "tropik"),
    (r"\bTemperate\b", "Ilıman"),
    (r"\btemperate\b", "ılıman"),
    (r"\bsubtropical\b", "subtropik"),
    (r"\bthe Tropics\b", "tropikler"),
    (r"\bTropics\b", "tropikler"),
]

# ---------------------------------------------------------------------------
# 4) Baglaclar / kalan Ingilizce kelimeler
# ---------------------------------------------------------------------------
WORDS: list[tuple[str, str]] = [
    (r"\band\b", "ve"),
    (r"\bor\b", "veya"),
    (r"\bfrom\b", ""),
    (r"\bto\b", "-"),
    (r"\bin\b", ""),
    (r"\bof\b", ""),
    (r"\bthe\b", ""),
    (r"\beast\b", "doğu"),
    (r"\bwest\b", "batı"),
    (r"\bnorth\b", "kuzey"),
    (r"\bsouth\b", "güney"),
    (r"\bregions?\b", "bölgeler"),
    (r"\bareas?\b", "alanlar"),
    (r"\bworld\b", "dünya"),
    (r"\bplant\b", "bitki"),
    (r"\bhabitat\b", "yetişme ortamı"),
    (r"\bnative\b", "yerel"),
    (r"\bgarden\b", "bahçe"),
    (r"\bescape\b", "kaçmış"),
    (r"\bcultivated\b", "yetiştirilen"),
    (r"\bfound\b", "bulunur"),
    (r"\bpossibly\b", "muhtemelen"),
    (r"\bprobably\b", "muhtemelen"),
    (r"\bobscure\b", "belirsiz"),
    (r"\borigin\b", "köken"),
    (r"\bOrigin\b", "Köken"),
    (r"\bhybrid\b", "melez"),
    (r"\bHybrid\b", "Melez"),
    (r"\buncertain\b", "belirsiz"),
    (r"\bExact\b", "Kesin"),
    (r"\bexact\b", "kesin"),
    (r"\bOriginal\b", "Asıl"),
    (r"\boriginal\b", "asıl"),
    (r"\bvirtually\b", "neredeyse"),
    (r"\bcosmopolitan\b", "kozmopolit"),
    (r"\binfrequent\b", "seyrek"),
    (r"\bcasual\b", "geçici"),
    (r"\bextreme\b", "aşırı"),
    (r"\bthroughout\b", "boyunca"),
    (r"\brange\b", "yayılış"),
    (r"\brare\b", "nadir"),
    (r"\balso\b", "ayrıca"),
    (r"\bmost\b", "çoğu"),
    (r"\bMany\b", "Birçok"),
    (r"\bmany\b", "birçok"),
    (r"\bother\b", "başka"),
    (r"\bis\b", ""),
    (r"\bit\b", ""),
    (r"\bthis\b", ""),
    (r"\bA\b", ""),
    (r"\ban\b", ""),
    (r"\bAn\b", ""),
    (r"\bas\b", ""),
    (r"\bform\b", "form"),
    (r"\barose\b", "türemiştir"),
    (r"\bknown\b", "bilinen"),
    (r"\bNot\b", ""),
    (r"\bnot\b", ""),
    (r"\bwild\b", "yabani"),
    (r"\bbut\b", "ancak"),
]


def clean(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,;:])(?!\s|$)", r"\1 ", text)
    text = re.sub(r"\s*-\s*", " - ", text)
    text = re.sub(r"( -\s*){2,}", " - ", text)
    text = re.sub(r"\s+\.", ".", text)
    text = re.sub(r"\.\s*\.", ".", text)
    text = re.sub(r":\s*", ": ", text)
    text = re.sub(r"\?\s*\.", "?", text)
    # Bos baglac artiklari
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"^\s*[,;:-]\s*", "", text)
    return text.strip()


def translate_range(range_text: str) -> str:
    text = range_text
    for pattern, repl in PHRASES:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    for pattern, repl in ABBREVS:
        text = re.sub(pattern, repl, text)
    for pattern, repl in PLACES:
        text = re.sub(pattern, repl, text)
    for pattern, repl in WORDS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return clean(text)


def translate_sources(text: str) -> str:
    text = re.sub(r"\(Kew POWO\)", "(Kew Bitkiler Dünyası Çevrimiçi)", text)
    text = re.sub(
        r"\(GRIN\s*/\s*Missouri Botanical Garden\)",
        "(GRIN / Missouri Botanik Bahçesi)",
        text,
    )
    text = re.sub(
        r"\(NCCIH\)",
        "(ABD Ulusal Tamamlayıcı ve Bütünleyici Sağlık Merkezi)",
        text,
    )
    text = re.sub(r"\bPlantZAfrica\b", "Güney Afrika Bitkileri", text)
    text = re.sub(r"\bSANBI\b", "Güney Afrika Ulusal Biyoçeşitlilik Enstitüsü", text)
    text = re.sub(r"\bPOWO\b", "Kew Bitkiler Dünyası Çevrimiçi", text)
    text = re.sub(r"\bMissouri Botanical Garden\b", "Missouri Botanik Bahçesi", text)
    return text


def translate_field(full: str) -> str:
    full = translate_sources(full)
    if "Doğal ortamı:" in full:
        range_part, habitat_part = full.split("Doğal ortamı:", 1)
        range_tr = translate_range(range_part)
        habitat = habitat_part.strip()
        if range_tr and not range_tr.endswith((".", "?", "!")):
            range_tr += "."
        return f"{range_tr} Doğal ortamı: {habitat}".strip()
    return translate_range(full)


# Ingilizce kalinti tespiti (yalnizca Range kismi)
EN_STOP = re.compile(
    r"\b(?:and|or|the|of|in|to|from|including|including|naturalized|"
    r"east|west|north|south|eastern|western|northern|southern|central|"
    r"temperate|tropical|tropics|regions?|areas?|world|plant|habitat|"
    r"native|garden|escape|cultivated|found|possibly|probably|obscure|"
    r"origin|hybrid|uncertain|exact|original|virtually|cosmopolitan|"
    r"infrequent|casual|extreme|throughout|range|rare|also|most|many|"
    r"other|around|absent|excluding|but|known|wild|arose|form|"
    r"hemisphere|eastwards?|westwards?|throughout)\b",
    re.I,
)


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    leftovers: list[tuple] = []

    for plant in plants:
        c = plant.get("cografyaMevsim")
        if not c:
            continue
        old = c.get("yetistigiYerler") or ""
        if not old:
            continue
        new = translate_field(old)
        if new != old:
            c["yetistigiYerler"] = new
            changed += 1

        range_part = new.split("Doğal ortamı:")[0]
        hits = EN_STOP.findall(range_part)
        if hits:
            leftovers.append((plant["id"], plant["ad"], hits, range_part[:180]))

    DATA.write_text(
        json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report = ROOT / "geo_translate_report.txt"
    lines = [
        f"Guncellenen: {changed}",
        f"Ingilizce kalinti (Range): {len(leftovers)}",
        "",
    ]
    for pid, ad, hits, sample in leftovers:
        lines.append(f"[{pid}] {ad}")
        lines.append(f"  {hits}")
        lines.append(f"  {sample}")
        lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK changed={changed} leftovers={len(leftovers)}")


if __name__ == "__main__":
    main()
