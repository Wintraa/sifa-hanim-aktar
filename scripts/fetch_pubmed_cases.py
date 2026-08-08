#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tıbbi bitkiler için PubMed'den Case Report arar ve ham özetleri kaydeder.
NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANTS_PATH = ROOT / "data" / "plants.json"
OUT_PATH = ROOT / "data" / "pubmed-vakalar-raw.json"
PROGRESS_PATH = ROOT / "data" / "pubmed-vakalar-progress.json"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# Kimliksiz isteklerde saniyede ~3 isteği aşmamak için bekleme
SLEEP_S = 0.4
TOOL = "SifaHanimAktarPlantGuide"
EMAIL = "sifahanimaktar@example.com"


def http_get(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": f"{TOOL}/1.0 ({EMAIL})"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def esearch(term: str, retmax: int = 5) -> list[str]:
    qs = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": term,
            "retmax": str(retmax),
            "retmode": "json",
            "sort": "relevance",
            "tool": TOOL,
            "email": EMAIL,
        }
    )
    data = json.loads(http_get(f"{EUTILS}/esearch.fcgi?{qs}"))
    return data.get("esearchresult", {}).get("idlist", []) or []


def efetch_abstracts(pmids: list[str]) -> list[dict]:
    if not pmids:
        return []
    qs = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
            "tool": TOOL,
            "email": EMAIL,
        }
    )
    xml_bytes = http_get(f"{EUTILS}/efetch.fcgi?{qs}")
    root = ET.fromstring(xml_bytes)
    articles = []
    for art in root.findall(".//PubmedArticle"):
        pmid_el = art.find(".//MedlineCitation/PMID")
        title_el = art.find(".//ArticleTitle")
        year_el = art.find(".//PubDate/Year")
        abstract_bits = [
            (n.text or "").strip()
            for n in art.findall(".//Abstract/AbstractText")
            if (n.text or "").strip()
        ]
        # Etiketli abstract parçalarını birleştir
        labeled = []
        for n in art.findall(".//Abstract/AbstractText"):
            label = n.attrib.get("Label") or n.attrib.get("NlmCategory") or ""
            text = "".join(n.itertext()).strip()
            if not text:
                continue
            labeled.append(f"{label}: {text}" if label else text)
        abstract = "\n".join(labeled) if labeled else " ".join(abstract_bits)
        articles.append(
            {
                "pmid": (pmid_el.text if pmid_el is not None else "").strip(),
                "title": "".join(title_el.itertext()).strip() if title_el is not None else "",
                "year": (year_el.text if year_el is not None else "").strip(),
                "abstract": abstract.strip(),
            }
        )
    return articles


def clean_botanical(name: str) -> str:
    # "Genus species subsp. x" → Genus species
    parts = re.split(r"\s+", name.strip())
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1]}"
    return name.strip()


def search_terms(botanik: str, ad: str) -> list[str]:
    latin = clean_botanical(botanik)
    # Önce tedavi/iyileşme odaklı vaka raporları, sonra genel case report
    return [
        (
            f'("{latin}"[Title/Abstract]) AND Case Reports[Publication Type] '
            f'AND (treatment[Title/Abstract] OR therapy[Title/Abstract] OR '
            f'improved[Title/Abstract] OR improvement[Title/Abstract] OR '
            f'resolved[Title/Abstract] OR remission[Title/Abstract])'
        ),
        f'("{latin}"[Title/Abstract]) AND Case Reports[Publication Type]',
        (
            f'("{latin}"[Title/Abstract]) AND '
            f'(case report[Title/Abstract] OR "case study"[Title/Abstract]) '
            f'AND (human[MeSH Terms] OR patient[Title/Abstract])'
        ),
        (
            f'("{latin}"[Title/Abstract]) AND (patient[Title/Abstract]) AND '
            f'(treatment[Title/Abstract] OR therapy[Title/Abstract]) AND '
            f'(clinical[Title/Abstract] OR case[Title/Abstract])'
        ),
    ]


def pick_best(articles: list[dict], botanik: str) -> dict | None:
    usable = [a for a in articles if len((a.get("abstract") or "").strip()) >= 120]
    if not usable:
        return None

    latin = clean_botanical(botanik).lower()
    genus = latin.split()[0] if latin else ""

    def score(a: dict) -> tuple:
        blob = f"{a.get('title', '')} {a.get('abstract', '')}".lower()
        has_latin = 1 if latin and latin in blob else 0
        has_genus = 1 if genus and genus in blob else 0
        positive = 1 if re.search(
            r"\b(improv\w*|resolv\w*|remission|successful|benefit|relief|recover\w*|ameliorat\w*)\b",
            blob,
        ) else 0
        adverse = -2 if re.search(
            r"\b(anaphylax\w*|allergic contact|adverse event|poisoning|toxicity|fatal)\b",
            blob,
        ) else 0
        animal = -2 if re.search(r"\b(rat|rats|mice|mouse|in vitro|cell line|murine)\b", blob) else 0
        return (positive, has_latin, has_genus, adverse, animal, len(a.get("abstract") or ""))

    return sorted(usable, key=score, reverse=True)[0]


def load_progress() -> dict:
    if PROGRESS_PATH.exists():
        return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))
    return {}


def save_progress(data: dict) -> None:
    PROGRESS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    plants = json.loads(PLANTS_PATH.read_text(encoding="utf-8"))
    medicinal = [p for p in plants if p.get("tur") == "Tıbbi Bitkiler"]
    results = load_progress()

    print(f"Tıbbi bitki: {len(medicinal)} | Önceden kayıtlı: {len(results)}")

    for i, plant in enumerate(medicinal, 1):
        pid = str(plant["id"])
        if pid in results and results[pid].get("status") in {"ok", "none"}:
            continue

        ad = plant.get("ad", "")
        botanik = plant.get("botanikAd", "")
        print(f"[{i}/{len(medicinal)}] {ad} ({botanik})…", flush=True)

        found: list[dict] = []
        used_term = ""
        try:
            for term in search_terms(botanik, ad):
                time.sleep(SLEEP_S)
                ids = esearch(term, retmax=8)
                if not ids:
                    continue
                time.sleep(SLEEP_S)
                articles = efetch_abstracts(ids)
                best = pick_best(articles, botanik)
                if best:
                    found = [best]
                    used_term = term
                    break

            if found:
                article = found[0]
                results[pid] = {
                    "status": "ok",
                    "plantId": plant["id"],
                    "ad": ad,
                    "botanikAd": botanik,
                    "searchTerm": used_term,
                    "pmid": article["pmid"],
                    "title": article["title"],
                    "year": article["year"],
                    "abstract": article["abstract"],
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{article['pmid']}/",
                }
                print(f"  -> PMID {article['pmid']}", flush=True)
            else:
                results[pid] = {
                    "status": "none",
                    "plantId": plant["id"],
                    "ad": ad,
                    "botanikAd": botanik,
                    "pmid": None,
                    "title": None,
                    "year": None,
                    "abstract": None,
                    "url": None,
                }
                print("  -> vaka bulunamadi", flush=True)
        except Exception as exc:  # noqa: BLE001
            results[pid] = {
                "status": "error",
                "plantId": plant["id"],
                "ad": ad,
                "botanikAd": botanik,
                "error": str(exc),
            }
            print(f"  -> HATA: {exc}", flush=True)

        save_progress(results)

    OUT_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for v in results.values() if v.get("status") == "ok")
    none = sum(1 for v in results.values() if v.get("status") == "none")
    err = sum(1 for v in results.values() if v.get("status") == "error")
    print(f"Bitti. ok={ok} none={none} error={err} → {OUT_PATH}")


if __name__ == "__main__":
    main()
