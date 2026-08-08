# -*- coding: utf-8 -*-
"""plants.json alanlarini GERCEK PFAF verisinden yeniden kurar.

Ilke: hicbir alan uydurulmaz. Her Turkce deger, PFAF metnindeki bir
ifadeden deterministik olarak turetilir veya birebir cevrilir.
Kaynakta bilgi yoksa alan bos kalir ve arayuz "belirtilmemis" gosterir.

PFAF'ta bulunmayan bitkiler siteden cikarilip
data/unverified_plants.json dosyasina tasinir (geri alinabilir).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pfaf_terms import (  # noqa: E402
    ACTIONS,
    CONDITIONS,
    EDIBLE_PARTS,
    EDIBLE_USES,
    HABIT,
    LIGHT_RULES,
    MONTHS,
    MOISTURE_RULES,
    REGIONS,
    SOIL_PH,
    SOIL_TEXTURE,
)

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
# Kaynak liste: PFAF oncesi tam yedek. Boylece script tekrar tekrar
# calistirilabilir ve id/eskiId alanlari bozulmaz.
SOURCE = ROOT / "data" / "plants.backup-pre-pfaf.json"
RAW_DIR = ROOT / "data" / "pfaf" / "raw"
INDEX = ROOT / "data" / "pfaf" / "pfaf_index.json"
QUARANTINE = ROOT / "data" / "unverified_plants.json"
HAZARD_TR = ROOT / "data" / "pfaf" / "hazards_tr.json"
HABITAT_TR = ROOT / "data" / "pfaf" / "habitats_tr.json"

SOURCE_NAME = "Plants For A Future (pfaf.org)"


def slugify(text: str) -> str:
    value = text.lower().strip().replace(" ", "-")
    value = re.sub(r"[^a-z0-9\-]+", "", value)
    return re.sub(r"-+", "-", value).strip("-") or "plant"


def tr_month(word: str) -> str:
    return MONTHS.get(word.strip().lower(), "")


# ---------------------------------------------------------------- mevsim

def flowering_time(phys: str) -> str:
    """PFAF 'in flower from June to August' -> 'Haziran - Agustos'."""
    m = re.search(r"in flower\s+from\s+(\w+)\s+to\s+(\w+)", phys, re.I)
    if m:
        a, b = tr_month(m.group(1)), tr_month(m.group(2))
        if a and b:
            return f"{a} - {b}"
    m = re.search(r"in flower\s+in\s+(\w+)", phys, re.I)
    if m and tr_month(m.group(1)):
        return tr_month(m.group(1))
    if re.search(r"in flower all year", phys, re.I):
        return "Yıl boyu çiçekli"
    m = re.search(r"in flower\s+from\s+(\w+)", phys, re.I)
    if m and tr_month(m.group(1)):
        return f"{tr_month(m.group(1))} ayından itibaren"
    return ""


def harvest_time(phys: str) -> str:
    """Tohum olgunlasma donemi (PFAF'in verdigi tek hasat gostergesi)."""
    m = re.search(r"seeds? ripen\s+from\s+(\w+)\s+to\s+(\w+)", phys, re.I)
    if m:
        a, b = tr_month(m.group(1)), tr_month(m.group(2))
        if a and b:
            return f"Tohumlar {a} - {b} arasında olgunlaşır"
    m = re.search(r"seeds? ripen\s+in\s+(\w+)", phys, re.I)
    if m and tr_month(m.group(1)):
        return f"Tohumlar {tr_month(m.group(1))} ayında olgunlaşır"
    m = re.search(r"seeds? ripen\s+from\s+(\w+)", phys, re.I)
    if m and tr_month(m.group(1)):
        return f"Tohumlar {tr_month(m.group(1))} ayından itibaren olgunlaşır"
    return ""


# ---------------------------------------------------------------- cografya

def growing_regions(rng: str, native: str, habitat_tr: str) -> str:
    """PFAF Range/Native Range alanlarini Turkce bolge adlarina cevirir.

    habitat_tr: dogal ortam metninin hazir Turkce cevirisi. Ingilizce metin
    asla dogrudan aktarilmaz. Range kismindaki baglaclar (and/to/from...)
    translate_geo_fields.translate_range ile tamamen Turkceye cevrilir.
    """
    # Cevrim sozlugunu lazy import et (dongusel bagimlilik olmasin)
    from translate_geo_fields import translate_range

    parts: list[str] = []

    source = (rng or "").strip().rstrip(".")
    if source:
        translated = source
        # Uzun ifadeleri once cevir ki parca eslesme olmasin
        for en in sorted(REGIONS, key=len, reverse=True):
            translated = re.sub(
                rf"(?<![\w.]){re.escape(en)}(?![\w])",
                REGIONS[en],
                translated,
                flags=re.I,
            )
        parts.append(translate_range(translated))

    if not parts and native:
        caps = re.findall(r"\b([A-Z][A-Z\s]{3,})\s*:", native)
        regions = []
        for c in caps:
            key = c.strip().lower()
            regions.append(REGIONS.get(key, c.strip().title()))
        if regions:
            parts.append(", ".join(dict.fromkeys(regions)))

    text = "; ".join(p for p in parts if p).strip()
    if text and not text.endswith("."):
        text += "."

    habitat = (habitat_tr or "").strip().rstrip(".")
    if habitat:
        sentence = f"Doğal ortamı: {habitat}."
        text = f"{text} {sentence}".strip() if text else sentence

    return text.strip()


# ---------------------------------------------------------------- bakim

def light_need(phys: str) -> str:
    found = [tr for en, tr in LIGHT_RULES if en in phys.lower()]
    return " ".join(dict.fromkeys(found))


def water_need(phys: str) -> str:
    found = [tr for en, tr in MOISTURE_RULES if en in phys.lower()]
    return " ".join(dict.fromkeys(found))


def _match_longest_first(text: str, table: dict[str, str]) -> list[str]:
    """Ic ice gecen ifadelerde en uzun eslesmeyi alir.

    Ornek: "can grow in very alkaline soils" hem "very alkaline" hem
    "alkaline" ile eslesir; sadece uzun olani sayilmalidir.
    """
    remaining = text
    found: list[str] = []
    for en in sorted(table, key=len, reverse=True):
        if en in remaining:
            found.append(table[en])
            remaining = remaining.replace(en, " ")
    return list(dict.fromkeys(found))


def soil_type(phys: str) -> str:
    out: list[str] = []

    m = re.search(r"Suitable for:\s*(.*?)\s*soils?\b(.*?)(?:\.|$)", phys, re.I | re.S)
    if m:
        textures = m.group(1).lower()
        found = _match_longest_first(textures, SOIL_TEXTURE)
        if found:
            out.append(f"{', '.join(found)} topraklar")
        tail = (m.group(2) or "").lower()
        if "well-drained" in tail or "well drained" in tail:
            out.append("iyi drene olması tercih edilir")
        if "nutritionally poor" in tail:
            out.append("besin yönünden zayıf toprakta da yetişebilir")
        if "heavy clay" in tail:
            out.append("ağır killi toprakta da yetişebilir")

    m = re.search(r"Suitable pH:\s*(.*?)(?:\.|$)", phys, re.I | re.S)
    if m:
        ph_text = m.group(1).lower()
        found = _match_longest_first(ph_text, SOIL_PH)
        if found:
            out.append(f"pH: {', '.join(found)}")
        if "saline" in ph_text:
            out.append("tuzlu toprağa dayanabilir")

    return "; ".join(out).strip()


# ---------------------------------------------------------------- saglik

def _split_terms(chunk: str) -> list[str]:
    """PFAF etki listesi bosluk/satirla ayrilmis terimlerdir."""
    chunk = chunk.replace("\n", "  ")
    return [t.strip() for t in re.split(r"\s{2,}", chunk) if t.strip()]


def medicinal_actions(med: str) -> tuple[str, str, list[str]]:
    """PFAF etki/kullanim etiketlerini Turkceye cevirir.

    PFAF bu listede iki farkli sey barindirir: farmakolojik etkiler
    (ornek: antiseptic) ve geleneksel kullanim alani olan hastalik adlari
    (ornek: Cancer). Ikincisini "fayda" gibi sunmak yanlis olur; bu yuzden
    ayri dondurulur.

    Donen: (etkiler_tr, kullanim_alanlari_tr, sozlukte_olmayanlar)
    """
    text = med
    # PFAF'in kendi feragat cumlesini at (bizim kendi feragatnamemiz var)
    text = re.sub(
        r"Plants For A Future can not take any responsibility.*?medicinally\.",
        "",
        text,
        flags=re.I | re.S,
    ).strip()

    lines = [ln for ln in text.split("\n") if ln.strip()]
    terms: list[str] = []
    for line in lines[:3]:
        # Etki satiri: kisa terimler, cumle noktalamasi yok
        if len(line) > 400 or line.count(".") > 1:
            break
        candidates = _split_terms(line)
        if not candidates:
            continue
        known = [
            c
            for c in candidates
            if c.lower().strip() in ACTIONS or c.lower().strip() in CONDITIONS
        ]
        if known and len(known) >= max(1, len(candidates) // 2):
            terms.extend(candidates)

    actions: list[str] = []
    conditions: list[str] = []
    unknown: list[str] = []
    for term in dict.fromkeys(terms):
        key = term.lower().strip()
        if key in ACTIONS:
            actions.append(ACTIONS[key])
        elif key in CONDITIONS:
            conditions.append(CONDITIONS[key])
        else:
            unknown.append(term)

    return (
        ", ".join(dict.fromkeys(actions)),
        ", ".join(dict.fromkeys(conditions)),
        unknown,
    )


def edible_summary(edible: str) -> str:
    """'Edible Parts: Flowers Leaves / Edible Uses: Condiment Tea' -> Turkce."""
    out: list[str] = []

    m = re.search(r"Edible Parts?:\s*(.*?)(?:\n|Edible Uses:|$)", edible, re.I | re.S)
    if m:
        terms = _split_terms(m.group(1))
        tr = [EDIBLE_PARTS.get(t.lower().strip(), "") for t in terms]
        tr = [t for t in tr if t]
        if tr:
            out.append(f"Kullanılan kısımlar: {', '.join(dict.fromkeys(tr))}")

    m = re.search(r"Edible Uses?:\s*(.*?)(?:\n|$)", edible, re.I | re.S)
    if m:
        terms = _split_terms(m.group(1))
        tr = [EDIBLE_USES.get(t.lower().strip(), "") for t in terms]
        tr = [t for t in tr if t]
        if tr:
            out.append(f"Kullanım biçimi: {', '.join(dict.fromkeys(tr))}")

    return ". ".join(out).strip()


def _habit_clause(habit_tr: str) -> str:
    """Habit ifadesini dil bilgisine uygun cumle ekine cevirir."""
    h = (habit_tr or "").strip()
    if not h:
        return "bir bitkidir"
    if "/" in h or ";" in h:
        return f"{h} bir bitkidir"
    if h.endswith(("dir", "dır", "tir", "tır")):
        return h
    if h.endswith("çalı"):
        prefix = h[: -len("çalı")].strip()
        return f"{prefix} bir çalıdır" if prefix else "bir çalıdır"
    if h.endswith("ağaç"):
        prefix = h[: -len("ağaç")].strip()
        return f"{prefix} bir ağaçtır" if prefix else "bir ağaçtır"
    if h.endswith("eğrelti otu"):
        return "bir eğrelti otudur"
    return f"{h} bir bitkidir"


def overview_text(plant_name: str, latin: str, pfaf: dict, phys: str, region: str) -> str:
    """Tanitim paragrafini dogrulanmis PFAF alanlarindan, akademik Turkceyle kurar.

    Derece/skor cumleleri arayuz metnine yazilmaz; bunlar plant['kaynak'] icinde kalir.
    """
    family = (pfaf.get("family") or "").strip()
    habit_tr = ""
    for en in sorted(HABIT, key=len, reverse=True):
        if re.search(rf"\b{re.escape(en)}\b", phys, re.I):
            habit_tr = HABIT[en]
            break

    sentences: list[str] = []
    intro = f"{plant_name} ({latin})"
    if family:
        sentences.append(f"{intro}, {family} familyasından {_habit_clause(habit_tr)}.")
    else:
        sentences.append(f"{intro}, {_habit_clause(habit_tr)}.")

    m = re.search(r"growing to\s+([\d.]+)\s*m\b", phys, re.I)
    if m:
        sentences.append(f"Yaklaşık {m.group(1)} m boya ulaşır.")

    if region:
        # Habitat cumlesini ayir; yalnizca yayilis ozetini kullan
        first = region.split("Doğal ortamı:")[0].split(".")[0].strip()
        if first:
            sentences.append(f"Doğal yayılış alanı: {first}.")

    return " ".join(sentences)


def rating_note(med_rating: str, ed_rating: str) -> str:
    def num(text: str) -> str:
        m = re.search(r"\((\d)\s*of\s*5\)", text or "")
        return m.group(1) if m else ""

    med, ed = num(med_rating), num(ed_rating)
    bits = []
    if med:
        bits.append(f"tıbbi kullanım derecesi {med}/5")
    if ed:
        bits.append(f"yenilebilirlik derecesi {ed}/5")
    return ", ".join(bits)


# ---------------------------------------------------------------- ana akis

def build() -> None:
    source_path = SOURCE if SOURCE.exists() else LIVE
    plants = json.loads(source_path.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}
    hazards_tr = json.loads(HAZARD_TR.read_text(encoding="utf-8")) if HAZARD_TR.exists() else {}
    habitats_tr = json.loads(HABITAT_TR.read_text(encoding="utf-8")) if HABITAT_TR.exists() else {}

    kept: list[dict] = []
    removed: list[dict] = []
    unknown_actions: dict[str, int] = {}
    stats = {"flower": 0, "harvest": 0, "soil": 0, "light": 0, "water": 0, "region": 0, "actions": 0, "hazard_tr": 0}

    for plant in plants:
        latin = (plant.get("botanikAd") or "").strip()
        entry = index.get(latin, {})

        if entry.get("status") != "ok":
            plant["dogrulanmadi"] = True
            removed.append(plant)
            continue

        raw_path = RAW_DIR / (entry.get("file") or f"{slugify(latin)}.json")
        if not raw_path.exists():
            plant["dogrulanmadi"] = True
            removed.append(plant)
            continue

        pfaf = json.loads(raw_path.read_text(encoding="utf-8"))
        phys = pfaf.get("physicalCharacteristics", "") or ""

        # --- Cografya & Mevsim (PFAF Range / Physical Characteristics)
        region = growing_regions(
            pfaf.get("range", ""),
            pfaf.get("nativeRange", ""),
            habitats_tr.get(latin, ""),
        )
        flower = flowering_time(phys)
        harvest = harvest_time(phys)

        plant["cografyaMevsim"] = {
            "yetistigiYerler": region,
            "hasatMevsimi": harvest,
            "ciceklenmeZamani": flower,
        }

        # --- Bakim & Yetistirme (PFAF Physical Characteristics)
        light = light_need(phys)
        water = water_need(phys)
        soil = soil_type(phys)

        plant["bakimYetistirme"] = {
            "isikIhtiyaci": light,
            "sulamaSikligi": water,
            "toprakTipi": soil,
        }

        # --- Saglik & Kullanim
        actions_tr, conditions_tr, unknown = medicinal_actions(
            pfaf.get("medicinalUses", "") or ""
        )
        for u in unknown:
            unknown_actions[u] = unknown_actions.get(u, 0) + 1

        hazard = hazards_tr.get(latin, "")

        faydalari = actions_tr
        if conditions_tr:
            faydalari = (
                f"{actions_tr}. Geleneksel kullanım alanları: {conditions_tr}."
                if actions_tr
                else f"Geleneksel kullanım alanları: {conditions_tr}."
            )

        plant["saglikKullanim"] = {
            "faydalari": faydalari,
            "kullanimSekli": edible_summary(pfaf.get("edibleUses", "") or ""),
            "yanEtkilerUyarilar": hazard,
        }

        # --- Tanitim metni (yalnizca dogrulanmis alanlardan uretilir)
        plant["genelTavsiyeMetni"] = overview_text(
            plant["ad"], latin, pfaf, phys, region
        )

        # --- Temel bilgiler (PFAF Common Name / Family)
        family = (pfaf.get("family") or "").strip()
        habit_tr = ""
        for en in sorted(HABIT, key=len, reverse=True):
            if re.search(rf"\b{re.escape(en)}\b", phys, re.I):
                habit_tr = HABIT[en]
                break

        plant["temelBilgiler"] = {
            "turkceAdi": plant["ad"],
            "botanikAdi": latin,
            "bitkiTuru": " ".join(
                x for x in [habit_tr, f"({family})" if family else ""] if x
            ).strip() or plant["temelBilgiler"].get("bitkiTuru", ""),
        }

        # --- Kaynak / denetim bilgisi
        plant["kaynak"] = {
            "ad": SOURCE_NAME,
            "url": pfaf.get("sourceUrl", ""),
            "cekimTarihi": pfaf.get("fetchedAt", ""),
            "eslesenAd": pfaf.get("pfafMatchedName", latin),
            "derece": rating_note(pfaf.get("medicinalRating", ""), pfaf.get("edibilityRating", "")),
        }

        # --- Ingilizce orijinal (denetim icin saklanir, arayuzde gosterilmez)
        plant["_pfafOrijinal"] = {
            "knownHazards": pfaf.get("knownHazards", ""),
            "medicinalUses": pfaf.get("medicinalUses", ""),
            "edibleUses": pfaf.get("edibleUses", ""),
            "physicalCharacteristics": phys,
            "range": pfaf.get("range", ""),
            "cultivationDetails": pfaf.get("cultivationDetails", ""),
        }

        plant.pop("kaynakMedicinalId", None)
        plant.pop("dogrulanmadi", None)

        stats["flower"] += bool(flower)
        stats["harvest"] += bool(harvest)
        stats["soil"] += bool(soil)
        stats["light"] += bool(light)
        stats["water"] += bool(water)
        stats["region"] += bool(region)
        stats["actions"] += bool(actions_tr)
        stats["hazard_tr"] += bool(hazard)

        kept.append(plant)

    # id'leri yeniden sirala (1..n) ve eski id'yi koru
    for new_id, plant in enumerate(kept, start=1):
        plant["eskiId"] = plant["id"]
        plant["id"] = new_id

    LIVE.write_text(json.dumps(kept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUARANTINE.write_text(
        json.dumps(removed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Sitede kalan (PFAF dogrulamali): {len(kept)}")
    print(f"Karantinaya alinan (PFAF'ta yok): {len(removed)}")
    print("\nAlan doluluk orani (kalan kayitlar icinde):")
    for key, value in stats.items():
        print(f"  {key:10} {value:3}/{len(kept)}")

    if unknown_actions:
        top = sorted(unknown_actions.items(), key=lambda kv: -kv[1])[:40]
        print(f"\nSozlukte olmayan etki terimi ({len(unknown_actions)} farkli):")
        for term, count in top:
            print(f"  {count:3}x {term}")


if __name__ == "__main__":
    build()
