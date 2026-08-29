# -*- coding: utf-8 -*-
"""Bitki metinlerini şifa odaklı, sade Türkçeye çevirir."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "plants.json"

JARGON = [
    (r"\bAsteraceae/Compositae\b", "papatyagiller"),
    (r"\bAsteraceae\b", "papatyagiller"),
    (r"\bCompositae\b", "papatyagiller"),
    (r"\bLamiaceae\b", "ballıbabagiller"),
    (r"\bApiaceae\b", "maydanozgiller"),
    (r"\bRosaceae\b", "gülgiller"),
    (r"\bFabaceae\b", "baklagiller"),
    (r"\binfüzyon\b", "demleme"),
    (r"\bdekoksiyon\b", "kaynatma"),
    (r"\btentür\b", "alkollü özüt"),
    (r"\bdahili\b", "içerek"),
    (r"\bharici\b", "dışarı sürerek"),
    (r"\bantiseptik\b", "mikrop temizleyici"),
    (r"\bantibakteriyel\b", "mikroplara karşı"),
    (r"\banti-inflamatuar\b", "iltihap yatıştırıcı"),
    (r"\biltihap giderici\b", "iltihabı yatıştırıcı"),
    (r"\banodyne\b", "ağrı kesici"),
    (r"\bantispazmodik\b", "kramp çözücü"),
    (r"\bkas spazmı çözücü\b", "kramp çözücü"),
    (r"\bkarminatif\b", "gaz söktürücü"),
    (r"\bgaz giderici\b", "gaz söktürücü"),
    (r"\bkolagog\b", "safraya yardımcı"),
    (r"\bsafra söktürücü\b", "safraya yardımcı"),
    (r"\bdiüretik\b", "idrar artırıcı"),
    (r"\bidrar söktürücü\b", "idrar artırıcı"),
    (r"\bemmenagog\b", "adeti uyarıcı"),
    (r"\badet söktürücü\b", "adeti uyarıcı"),
    (r"\bfebrifug\w*\b", "ateş düşürücü"),
    (r"\bdiaphoretic\b", "terletici"),
    (r"\bexpectorant\b", "balgam söktürücü"),
    (r"\bastringent\b", "büzücü"),
    (r"\bdemulcent\b", "yatıştırıcı"),
    (r"\bstomachic\b", "mideyi rahatlatıcı"),
    (r"\bnervine\b", "sinir yatıştırıcı"),
    (r"\btonik\b", "güçlendirici"),
    (r"\bgenel güçlendirici \(tonik\)\b", "vücudu destekleyici"),
    (r"\bvulnerary\b", "yara iyileştirici"),
    (r"\brubefacient\b", "cildi ısıtıcı"),
    (r"\bemetik\b", "kusturucu"),
    (r"\bpurgatif\b", "kuvvetli müshil"),
    (r"\blaksatif\b", "bağırsak yumuşatıcı"),
    (r"\bvermfij\w*\b", "bağırsak kurduna karşı"),
    (r"\bIgE\b", "alerji"),
    (r"\bPMID\s*\d+\b", ""),
]

LATIN_PAREN = re.compile(r"\s*\([A-Z][a-z]+(?:\s+[a-z\-]+){0,4}(?:\s+L\.)?[^)]*\)")
LATIN_NAME = re.compile(r"\b[A-Z][a-z]{2,}\s+[a-z]{3,}(?:\s+(?:L\.|var\.|subsp\.)[^\s,]*)?")
CITE = re.compile(r"\[\d+[a-z]?\]")
FAMILY_SENT = re.compile(
    r"[^.]*familyasından[^.]*\.",
    re.IGNORECASE,
)
RANGE_SENT = re.compile(
    r"[^.]*doğal yayılış[^.]*\.|[^.]*yetiştiği yer[^.]*\.|[^.]*doğal ortam[^.]*\.",
    re.IGNORECASE,
)
HEIGHT_SENT = re.compile(r"[^.]*yaklaşık\s+[\d.,]+\s*m[^.]*\.", re.IGNORECASE)
ANNUAL_SENT = re.compile(
    r"[^.]*bir mevsim yaşayan[^.]*\.|[^.]*çok yıllık[^.]*\.|[^.]*kışın da yeşil[^.]*\.",
    re.IGNORECASE,
)

PART_WORDS = [
    ("çiçek", "çiçek"),
    ("yaprak", "yaprak"),
    ("kök", "kök"),
    ("tohum", "tohum"),
    ("meyve", "meyve"),
    ("kabuk", "kabuk"),
    ("yağ", "yağ"),
    ("sürgün", "sürgün"),
    ("gomme", "reçine"),
    ("reçine", "reçine"),
    ("yumru", "yumru"),
    ("soğan", "soğan"),
    ("dal", "dal"),
]


def sade(text: str) -> str:
    value = str(text or "")
    value = CITE.sub("", value)
    value = LATIN_PAREN.sub("", value)
    for pat, repl in JARGON:
        value = re.sub(pat, repl, value, flags=re.IGNORECASE)
    value = re.sub(r"\s{2,}", " ", value)
    value = re.sub(r"\s+([,.;:])", r"\1", value)
    return value.strip(" .;")


def used_parts(plant: dict) -> str:
    blob = " ".join(
        [
            plant.get("ad") or "",
            (plant.get("saglikKullanim") or {}).get("kullanimSekli") or "",
            (plant.get("saglikKullanim") or {}).get("faydalari") or "",
        ]
    ).lower()
    found = []
    for key, label in PART_WORDS:
        if key in blob and label not in found:
            found.append(label)
    if "tohum" in (plant.get("ad") or "").lower() and "tohum" not in found:
        found.insert(0, "tohum")
    if not found:
        if plant.get("tur") == "Süs Bitkileri":
            return "süs için bakılır, şifa için içilmez"
        return "kuru ot / droğ"
    if len(found) == 1:
        return found[0]
    return ", ".join(found[:-1]) + " ve " + found[-1]


def how_to_use(plant: dict, part: str) -> str:
    raw = sade((plant.get("saglikKullanim") or {}).get("kullanimSekli") or "")
    low = raw.lower()
    ad = plant.get("ad") or "Bu bitki"
    lines = []

    if plant.get("tur") == "Süs Bitkileri" and ("süs" in low or not raw):
        return (
            f"{ad} evde bakılan bir süs bitkisidir. Çayı yapılmaz, yenmez, ilaç gibi içilmez. "
            "Çocukların ve ev hayvanlarının yaprağını koparıp yutmasına izin vermeyin."
        )

    if "çay" in low or "demleme" in low or "infüzyon" in low:
        lines.append(
            "Çay için: Bir su bardağı (yaklaşık 150 ml) kaynar suya 1 tatlı kaşığı kuru droğ konur. "
            "Kapağı kapatılır, 8–10 dakika demlenir, süzülüp ılık içilir. Günde 2–3 fincanı geçmeyin. "
            "Acı gelirse bal eklenebilir; şekerle abartmayın."
        )
    if "kaynat" in low or "dekoksiyon" in low or "kök" in part or "kabuk" in part:
        lines.append(
            "Kök veya kabuk kullanılıyorsa çay gibi demlemek yetmez: bir kase soğuk suya bir parça droğ konur, "
            "hafif ateşte 10–15 dakika kaynatılır, süzülür. Bu daha sert bir içecektir; az başlanır."
        )
    if any(w in low for w in ["lapa", "yıkama", "sürme", "harici", "dışarı", "cilt", "kompres", "yağ"]):
        lines.append(
            "Dışarı sürmek için: Demlenmiş su soğuduktan sonra temiz beze emdirilip ilgili yere konur, "
            "veya aktardan aldığınız hazır merhem/yağ ince bir tabaka sürülür. Açık, irinli, derin yaraya "
            "kendi başınıza sürmeyin. Göze kaçırmayın."
        )
    if "baharat" in low or "çeşni" in low or "yemek" in low:
        lines.append(
            "Mutfakta: Yemeğe az miktarda çeşni olarak katılır. Şifa niyetiyle avuç avuç yenmez; "
            "yemekteki koku yeterlidir."
        )
    if "gargara" in low or "ağız" in low or "boğaz" in low:
        lines.append(
            "Gargara: Ilık demleme ile ağız çalkalanır veya gargara yapılır, tükürülür. Yutmak zorunda değilsiniz."
        )
    if "buhar" in low or "inhal" in low:
        lines.append(
            "Buhar: Demlemenin buharı dikkatle solunur. Yüze çok yaklaşmayın, göze kaçmasın, çocukta bu usul kullanılmasın."
        )
    if not lines:
        if raw:
            lines.append(f"Aktardaki kullanım: {raw}. Az miktarla başlayın, kutu üzerindeki tarife bakın.")
        else:
            lines.append(
                "Aktardan nasıl satıldığını sorun (çaylık ot, toz, yağ, kapsül). "
                "Her şeklin dozu ayrıdır; poşet çay ile kuvvetli özüt aynı şey değildir."
            )
    lines.append(
        "Hazır çay poşeti, kapsül veya şurup aldıysanız kutunun arkasındaki tarife uyun. "
        "Şikayet bir haftada geçmezse ürünü değiştirmek yerine doktora görünün."
    )
    return " ".join(lines)


def benefits(plant: dict) -> str:
    raw = sade((plant.get("saglikKullanim") or {}).get("faydalari") or "")
    ad = plant.get("ad") or "Bu bitki"
    if plant.get("tur") == "Süs Bitkileri" and not raw:
        return (
            f"{ad} şifa bitkisi değildir. Ev güzelliği içindir. "
            "İçmek, kaynatmak veya çocuğa vermek doğru olmaz."
        )
    if not raw:
        return (
            f"{ad} aktar raflarında bulunur. Şikayetinize uygun olup olmadığını aktara ve eczacıya sorun; "
            "her ot her derde iyi gelmez."
        )
    # Split long comma lists into readable sentence
    cleaned = raw.replace(";", ".").strip()
    if len(cleaned) > 40 and "," in cleaned and "." not in cleaned[:80]:
        parts = [p.strip(" .") for p in re.split(r",| ve ", cleaned) if p.strip()]
        parts = [p for p in parts if len(p) > 2][:12]
        if parts:
            cleaned = (
                f"{ad} geleneksel olarak şu şikayetlerde kullanılır: "
                + ", ".join(parts)
                + ". Bunlar halk ve aktar kullanımına göredir; herkeste aynı sonucu vermez."
            )
    if not cleaned.startswith(ad):
        cleaned = f"{ad} şu işler için tutulur: {cleaned}"
    if "kanser" in cleaned.lower():
        cleaned += " Kanser tedavisi olduğu anlamına gelmez."
    return cleaned


def warnings(plant: dict) -> str:
    raw = sade((plant.get("saglikKullanim") or {}).get("yanEtkilerUyarilar") or "")
    ad = plant.get("ad") or "Bu bitki"
    bits = []
    if raw:
        bits.append(raw)
    else:
        bits.append(f"{ad} ‘zararsız çay’ diye sınırsız içilmez. Fazlası mideyi bozabilir, alerji yapabilir.")
    low = (raw + " " + ((plant.get("saglikKullanim") or {}).get("faydalari") or "")).lower()
    if any(w in low for w in ["adet", "rahim", "gebelik", "hamile", "düşük"]):
        bits.append("Hamilelikte, emzirirken ve çocuklarda hekime sormadan kullanılmaz.")
    if any(w in low for w in ["karaciğer", "böbrek", "kalp", "tansiyon", "kan sulandır"]):
        bits.append("Kronik hastalığı veya düzenli ilacı olanlar (tansiyon, şeker, kan sulandırıcı, tiroid) mutlaka hekime sorsun.")
    if any(w in low for w in ["alerji", "kaşıntı", "şişme", "anafilaksi"]):
        bits.append(
            "Kaşıntı, dil-dudak şişmesi, nefes darlığı olursa bırakın, acile gidin. "
            "Papatyagiller alerjisi olanlar bu familyadan otlara da dikkat etsin."
        )
    bits.append(
        "Bu bilgiler teşhis ve tedavi değildir. Ağrı, ateş, kanama, nefes darlığı, şiddetli kusma olursa bitkiyle vakit kaybetmeyin, doktora gidin."
    )
    # de-dupe similar
    out = []
    seen = set()
    for b in bits:
        key = b[:48]
        if key not in seen:
            seen.add(key)
            out.append(b)
    return " ".join(out)


def intro(plant: dict, part: str) -> str:
    ad = plant.get("ad") or "Bu bitki"
    tur = plant.get("tur") or ""
    if tur == "Süs Bitkileri":
        return (
            f"{ad} şifalı ot diye içilecek bir bitki değildir; evde bakılan süs bitkisidir. "
            "Aşağıdaki uyarıları çocuklar ve ev hayvanları için okuyun."
        )
    if tur == "Aromatik Bitkiler":
        return (
            f"{ad} hem kokusu hem şifa niyetiyle kullanılan bir ottur. Aktarda en çok {part} satılır. "
            "Koku için de, çay için de doz kaçmamalıdır."
        )
    return (
        f"{ad} Şifa Hanım Aktar’da şifa niyetiyle tutulan bir ottur. En çok {part} kullanılır. "
        "Aşağıda neye iyi geldiği, evde nasıl hazırlandığı ve kimlerin dikkat etmesi gerektiği anlatılır. "
        "Komşu tavsiyesiyle avuç avuç içilmez."
    )


def genel(plant: dict, part: str, fayda: str, kullanim: str, uyari: str) -> str:
    ad = plant.get("ad") or "Bu bitki"
    return "\n\n".join(
        [
            intro(plant, part),
            f"Ne işe yarar?\n{fayda}",
            f"Nasıl kullanılır?\n{kullanim}",
            f"Nelere dikkat edilir?\n{uyari}",
            f"Kısaca: {ad} şifa dolabının bir parçası olabilir ama ilaç kutusunun yerini tutmaz. "
            "Emin değilseniz aktara ve eczacıya sorun, ağır işi doktora bırakın.",
        ]
    )


def rewrite_one(plant: dict) -> dict:
    part = used_parts(plant)
    fayda = benefits(plant)
    kullanim = how_to_use(plant, part)
    uyari = warnings(plant)
    plant = dict(plant)
    plant["genelTavsiyeMetni"] = genel(plant, part, fayda, kullanim, uyari)
    tb = dict(plant.get("temelBilgiler") or {})
    tb["turkceAdi"] = plant.get("ad") or tb.get("turkceAdi")
    tb["bitkiTuru"] = f"Kullanılan kısım: {part}"
    plant["temelBilgiler"] = tb
    sk = dict(plant.get("saglikKullanim") or {})
    sk["faydalari"] = fayda
    sk["kullanimSekli"] = kullanim
    sk["yanEtkilerUyarilar"] = uyari
    plant["saglikKullanim"] = sk
    # Coğrafya/bakım: şifa dışı metni boşaltma; UI gizlenecek. Kısa şifa notu bırak.
    plant["cografyaMevsim"] = {
        "yetistigiYerler": "Aktardan alınır; nerede yetiştiği şifa için önemli değildir.",
        "hasatMevsimi": "Kuru droğ serin, karanlık ve kapalı kavanozda saklanır; nemlenirse atılır.",
        "ciceklenmeZamani": "Taze ot yoksa kurusu yıl boyu kullanılır.",
    }
    return plant


def main() -> None:
    plants = json.loads(SRC.read_text(encoding="utf-8"))
    out = [rewrite_one(p) for p in plants]
    SRC.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"yazıldı: {len(out)} bitki -> {SRC}")


if __name__ == "__main__":
    main()
