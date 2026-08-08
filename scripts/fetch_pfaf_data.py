# -*- coding: utf-8 -*-
"""pfaf.org (Plants For A Future) veritabanindan GERCEK bitki verisini ceker.

Her bitki icin kaynak URL ve cekim tarihi kaydedilir; boylece her alan
dogrulanabilir. Bulunamayan turler "not_found" olarak isaretlenir ve
asla uydurma metinle doldurulmaz.

Cikti: data/pfaf/raw/<slug>.json  +  data/pfaf/pfaf_index.json
"""

from __future__ import annotations

import html as html_lib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "plants.json"
OUT_DIR = ROOT / "data" / "pfaf" / "raw"
INDEX = ROOT / "data" / "pfaf" / "pfaf_index.json"

BASE = "https://pfaf.org/user/Plant.aspx?LatinName="
UA = "DogalBitkilerRehberi/1.0 (educational project; plant data verification)"

# PFAF HTML id -> anlamli alan adi
FIELDS = {
    "commonName": "ContentPlaceHolder1_lblCommanName",
    "family": "ContentPlaceHolder1_lblFamily",
    "usdaHardiness": "ContentPlaceHolder1_lblUSDAhardiness",
    "knownHazards": "ContentPlaceHolder1_lblKnownHazards",
    "habitats": "ContentPlaceHolder1_lblhabitats",
    "habitatsDetail": "ContentPlaceHolder1_txtHabitats",
    "range": "ContentPlaceHolder1_lblRange",
    "physicalCharacteristics": "ContentPlaceHolder1_lblPhystatment",
    "synonyms": "ContentPlaceHolder1_lblSynonyms",
    "edibleUses": "ContentPlaceHolder1_txtEdibleUses",
    "medicinalUses": "ContentPlaceHolder1_txtMediUses",
    "otherUses": "ContentPlaceHolder1_txtOtherUses",
    "cultivationDetails": "ContentPlaceHolder1_txtCultivationDetails",
    "propagation": "ContentPlaceHolder1_txtPropagation",
    "summary": "ContentPlaceHolder1_txtSummary",
    "edibilityRating": "ContentPlaceHolder1_txtEdrating",
    "medicinalRating": "ContentPlaceHolder1_txtMedRating",
    "nativeRange": "ContentPlaceHolder1_lblFoundInText",
    "weedPotential": "ContentPlaceHolder1_lblWeedPotentialText",
    "displayLatinName": "ContentPlaceHolder1_lbldisplatinname",
}

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t\r\f\v]+")


def slugify(text: str) -> str:
    value = text.lower().strip().replace(" ", "-")
    value = re.sub(r"[^a-z0-9\-]+", "", value)
    return re.sub(r"-+", "-", value).strip("-") or "plant"


def clean(raw: str) -> str:
    """HTML parcasini duz metne cevirir; PFAF referans numaralarini korur."""
    text = raw.replace("<br />", "\n").replace("<br/>", "\n").replace("<br>", "\n")
    text = TAG_RE.sub("", text)
    text = html_lib.unescape(text)
    text = WS_RE.sub(" ", text)
    lines = [ln.strip() for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln).strip()


def extract(html: str, element_id: str) -> str:
    """Belirtilen id'li elementin ic metnini yakalar (ic ice tag'lere toleransli)."""
    start_match = re.search(
        rf'id="{re.escape(element_id)}"[^>]*>', html, flags=re.IGNORECASE
    )
    if not start_match:
        return ""
    pos = start_match.end()
    # Elementin acilis tag adini bul (span/div/td ...)
    tag_match = re.search(
        rf"<(\w+)[^>]*id=\"{re.escape(element_id)}\"", html, flags=re.IGNORECASE
    )
    tag = tag_match.group(1) if tag_match else "span"

    depth = 1
    scan = pos
    pattern = re.compile(rf"</?{tag}\b", flags=re.IGNORECASE)
    while depth > 0:
        m = pattern.search(html, scan)
        if not m:
            return clean(html[pos:])
        if html[m.start() : m.start() + 2 + len(tag)].lower().startswith(f"</{tag}"):
            depth -= 1
        else:
            depth += 1
        scan = m.end()
        if depth == 0:
            return clean(html[pos : m.start()])
    return ""


def fetch_html(latin: str, retries: int = 3) -> str | None:
    url = BASE + urllib.parse.quote_plus(latin)
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 503):
                time.sleep(5 * (attempt + 1))
                continue
            if exc.code == 404:
                return None
            time.sleep(2)
        except Exception:
            time.sleep(3)
    return None


def parse(html: str, latin: str) -> dict | None:
    data = {key: extract(html, el_id) for key, el_id in FIELDS.items()}

    # PFAF, bulunmayan turlerde bos bir sablon dondurur.
    meaningful = any(
        data.get(k)
        for k in ("medicinalUses", "edibleUses", "cultivationDetails", "range", "physicalCharacteristics")
    )
    if not meaningful:
        return None

    data["botanicalName"] = latin
    data["sourceUrl"] = BASE + urllib.parse.quote_plus(latin)
    data["sourceName"] = "Plants For A Future (pfaf.org)"
    data["fetchedAt"] = date.today().isoformat()
    return data


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plants = json.loads(LIVE.read_text(encoding="utf-8"))

    only = sys.argv[1:] or None  # test icin: python fetch_pfaf_data.py "Salvia officinalis"
    targets = plants
    if only:
        wanted = {x.lower() for x in only}
        targets = [p for p in plants if p["botanikAd"].lower() in wanted]

    index: dict[str, dict] = {}
    if INDEX.exists():
        index = json.loads(INDEX.read_text(encoding="utf-8"))

    found = 0
    missing: list[tuple] = []

    for plant in targets:
        latin = (plant.get("botanikAd") or "").strip()
        if not latin:
            continue

        slug = slugify(latin)
        cache = OUT_DIR / f"{slug}.json"
        if cache.exists() and not only:
            index[latin] = {"status": "ok", "file": cache.name}
            found += 1
            continue

        print(f"[{plant['id']}] {plant['ad']} <- {latin} ...", flush=True)
        html = fetch_html(latin)
        record = parse(html, latin) if html else None

        if record:
            cache.write_text(
                json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            index[latin] = {"status": "ok", "file": cache.name}
            found += 1
            print(f"  OK  ({len(record.get('medicinalUses',''))} krk tibbi metin)")
        else:
            index[latin] = {"status": "not_found"}
            missing.append((plant["id"], plant["ad"], latin))
            print("  YOK (PFAF'ta bulunamadi)")

        time.sleep(1.3)

    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nBulundu: {found} / {len(targets)}   Bulunamadi: {len(missing)}")
    for item in missing:
        print("  -", item)


if __name__ == "__main__":
    main()
