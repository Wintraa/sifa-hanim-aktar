#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eksik vaka bitkileri icin genis PubMed + Europe PMC aramasi."""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MISSING = ROOT / "data" / "missing-vaka-plants.json"
OUT = ROOT / "data" / "pubmed-gap-fill-raw.json"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
SLEEP = 0.35
TOOL = "SifaHanimAktarPlantGuide"
EMAIL = "sifahanimaktar@example.com"

# Yakin tur / es anlamli botanik adlari
ALIASES = {
    "Tilia tomentosa": ["Tilia cordata", "Tilia platyphyllos", "Tilia"],
    "Tilia cordata": ["Tilia platyphyllos", "Tilia tomentosa", "lime flower", "linden"],
    "Alchemilla xanthochlora": ["Alchemilla vulgaris", "lady's mantle"],
    "Elymus repens": ["Agropyron repens", "couch grass"],
    "Viburnum opulus": ["Viburnum", "cramp bark", "guelder rose"],
    "Mentha pulegium": ["pennyroyal", "Mentha"],
    "Cnicus benedictus": ["Centaurea benedicta", "blessed thistle"],
    "Petasites hybridus": ["Petasites", "butterbur"],
    "Euphrasia officinalis": ["Euphrasia", "eyebright"],
    "Galium aparine": ["cleavers", "Galium"],
    "Leonurus cardiaca": ["motherwort", "Leonurus"],
    "Hyssopus officinalis": ["hyssop"],
    "Syzygium aromaticum": ["clove", "Eugenia caryophyllata"],
    "Olea europaea": ["olive leaf", "olive oil", "Olea"],
    "Fragaria vesca": ["strawberry leaf", "Fragaria"],
    "Rubus idaeus": ["raspberry leaf", "Rubus"],
    "Rubus fruticosus": ["blackberry", "Rubus"],
    "Malva sylvestris": ["mallow", "Malva"],
    "Primula veris": ["cowslip", "Primula"],
    "Mentha aquatica": ["Mentha", "water mint"],
    "Mentha arvensis": ["Mentha", "corn mint"],
    "Clinopodium vulgare": ["wild basil", "Satureja vulgaris"],
    "Lamium album": ["white dead nettle", "Lamium"],
    "Galeopsis tetrahit": ["hemp nettle", "Galeopsis"],
    "Frangula alnus": ["Rhamnus frangula", "alder buckthorn"],
    "Rhamnus cathartica": ["buckthorn", "Rhamnus"],
    "Oxalis acetosella": ["wood sorrel", "Oxalis"],
    "Parietaria officinalis": ["pellitory", "Parietaria"],
    "Kaempferia galanga": ["Kaempferia", "galanga"],
    "Dittrichia viscosa": ["Inula viscosa", "Dittrichia"],
    "Styrax officinalis": ["storax", "Styrax"],
    "Simmondsia chinensis": ["jojoba"],
    "Acorus calamus": ["calamus", "sweet flag"],
    "Plantago major": ["plantain", "Plantago"],
    "Achillea millefolium": ["yarrow", "Achillea"],
}


def http_get(url: str, retries: int = 4) -> bytes:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"{TOOL}/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(str(last_err))


def esearch(term: str, retmax: int = 8) -> list[str]:
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


def efetch(pmids: list[str]) -> list[dict]:
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
    root = ET.fromstring(http_get(f"{EUTILS}/efetch.fcgi?{qs}"))
    out = []
    for art in root.findall(".//PubmedArticle"):
        pmid_el = art.find(".//MedlineCitation/PMID")
        title_el = art.find(".//ArticleTitle")
        year_el = art.find(".//PubDate/Year")
        labeled = []
        for n in art.findall(".//Abstract/AbstractText"):
            label = n.attrib.get("Label") or ""
            text = "".join(n.itertext()).strip()
            if text:
                labeled.append(f"{label}: {text}" if label else text)
        abstract = "\n".join(labeled)
        out.append(
            {
                "pmid": (pmid_el.text if pmid_el is not None else "").strip(),
                "title": "".join(title_el.itertext()).strip() if title_el is not None else "",
                "year": (year_el.text if year_el is not None else "").strip(),
                "abstract": abstract,
                "source": "PubMed",
            }
        )
    return out


def epmc_search(query: str, page_size: int = 5) -> list[dict]:
    qs = urllib.parse.urlencode(
        {
            "query": query,
            "format": "json",
            "pageSize": str(page_size),
            "resultType": "core",
        }
    )
    data = json.loads(http_get(f"{EPMC}?{qs}"))
    results = []
    for hit in data.get("resultList", {}).get("result", []) or []:
        pmid = str(hit.get("pmid") or hit.get("id") or "").strip()
        abstract = (hit.get("abstractText") or "").strip()
        if len(abstract) < 80:
            continue
        results.append(
            {
                "pmid": pmid if pmid.isdigit() else "",
                "title": (hit.get("title") or "").strip(),
                "year": str(hit.get("pubYear") or ""),
                "abstract": abstract,
                "source": "EuropePMC",
                "url": hit.get("fullTextUrlList", {})
                and None
                or (f"https://europepmc.org/article/MED/{pmid}" if pmid.isdigit() else hit.get("doi", "")),
            }
        )
    return results


def animal(blob: str) -> bool:
    return bool(re.search(r"\b(rat|rats|mice|mouse|murine|in vitro|cell line)\b", blob, re.I))


def score(article: dict, botanik: str) -> tuple:
    blob = f"{article.get('title','')} {article.get('abstract','')}".lower()
    if animal(blob) or len(article.get("abstract") or "") < 100:
        return (-99, 0, 0)
    latin = botanik.lower()
    genus = latin.split()[0] if latin else ""
    has_name = 1 if (latin in blob or genus in blob) else 0
    therapeutic = 1 if re.search(
        r"\b(improv|resolv|successful|remission|benefit|relief|recover|treatment|therapy|patient)\b",
        blob,
    ) else 0
    caseish = 1 if re.search(r"\b(case report|case study|we report|presented with|year-old)\b", blob) else 0
    adverse_only = -1 if re.search(r"\b(anaphylax|poisoning|fatal)\b", blob) and therapeutic == 0 else 0
    return (caseish, therapeutic, has_name, adverse_only, len(article.get("abstract") or ""))


def terms_for(botanik: str) -> list[str]:
    names = [botanik] + ALIASES.get(botanik, [])
    out = []
    for name in names:
        out.append(f'("{name}"[Title/Abstract]) AND Case Reports[Publication Type]')
        out.append(
            f'("{name}"[Title/Abstract]) AND (case report[Title/Abstract] OR "case study"[Title/Abstract]) '
            f"AND (patient[Title/Abstract] OR human[MeSH Terms])"
        )
        out.append(
            f'("{name}"[Title/Abstract]) AND (clinical trial[Publication Type] OR clinical study[Publication Type]) '
            f"AND (patient[Title/Abstract])"
        )
    return out


def main() -> None:
    missing = json.loads(MISSING.read_text(encoding="utf-8"))
    results = {}
    if OUT.exists():
        results = json.loads(OUT.read_text(encoding="utf-8"))
    print(f"Eksik: {len(missing)} | onceki kayit: {len(results)}")
    for i, plant in enumerate(missing, 1):
        pid = str(plant["id"])
        if pid in results and results[pid].get("status") in {"ok", "none"}:
            continue
        ad = plant["ad"]
        botanik = plant["botanikAd"]
        print(f"[{i}/{len(missing)}] {ad} ({botanik})", flush=True)
        candidates: list[dict] = []
        try:
            for term in terms_for(botanik)[:6]:
                time.sleep(SLEEP)
                ids = esearch(term, retmax=6)
                if not ids:
                    continue
                time.sleep(SLEEP)
                candidates.extend(efetch(ids))
            # Europe PMC yedek
            time.sleep(SLEEP)
            q = f'("{botanik}" OR "{ALIASES.get(botanik, [botanik])[0]}") AND ("case report" OR "case study") AND HAS_ABSTRACT:Y'
            candidates.extend(epmc_search(q, page_size=5))

            ranked = sorted(candidates, key=lambda a: score(a, botanik), reverse=True)
            best = ranked[0] if ranked and score(ranked[0], botanik)[0] > -50 else None
            if best:
                pmid = best.get("pmid") or ""
                url = (
                    f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    if pmid
                    else (best.get("url") or "https://europepmc.org/")
                )
                results[pid] = {
                    "status": "ok",
                    "plantId": plant["id"],
                    "ad": ad,
                    "botanikAd": botanik,
                    "pmid": pmid,
                    "title": best.get("title"),
                    "year": best.get("year"),
                    "abstract": best.get("abstract"),
                    "url": url,
                    "source": best.get("source", "PubMed"),
                }
                print(f"  -> {best.get('source')} {pmid or 'no-pmid'}", flush=True)
            else:
                results[pid] = {
                    "status": "none",
                    "plantId": plant["id"],
                    "ad": ad,
                    "botanikAd": botanik,
                }
                print("  -> yok", flush=True)
        except Exception as exc:  # noqa: BLE001
            results[pid] = {
                "status": "error",
                "plantId": plant["id"],
                "ad": ad,
                "botanikAd": botanik,
                "error": str(exc),
            }
            print(f"  -> HATA {exc}", flush=True)
        OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for v in results.values() if v.get("status") == "ok")
    print(f"Bitti ok={ok}/{len(missing)}")


if __name__ == "__main__":
    main()
