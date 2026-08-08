#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PubMed'de vaka bulunamayan bitkiler icin daha genis arama (ikinci tur)."""

from __future__ import annotations

import json
import time
from pathlib import Path

# Mevcut fetch modulunu yeniden kullan
import fetch_pubmed_cases as f

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "data" / "pubmed-vakalar-progress.json"


def broader_terms(botanik: str) -> list[str]:
    latin = f.clean_botanical(botanik)
    genus = latin.split()[0] if latin else botanik
    return [
        f'("{genus}"[Title/Abstract]) AND Case Reports[Publication Type] AND herbal[Title/Abstract]',
        f'("{latin}"[Title/Abstract]) AND ("case report"[Title/Abstract] OR Case Reports[Publication Type])',
        f'("{genus}"[Title/Abstract]) AND phytotherapy[Title/Abstract] AND patient[Title/Abstract]',
        f'("{latin}"[MeSH Terms] OR "{latin}"[Title/Abstract]) AND Case Reports[Publication Type]',
    ]


def main() -> None:
    results = json.loads(PROGRESS.read_text(encoding="utf-8"))
    none_ids = [k for k, v in results.items() if v.get("status") == "none"]
    print(f"Ikinci tur: {len(none_ids)} bitki")

    for i, pid in enumerate(none_ids, 1):
        entry = results[pid]
        ad = entry.get("ad", "")
        botanik = entry.get("botanikAd", "")
        print(f"[{i}/{len(none_ids)}] {ad} ({botanik})...", flush=True)
        found = None
        used = ""
        try:
            for term in broader_terms(botanik):
                time.sleep(f.SLEEP_S)
                ids = f.esearch(term, retmax=8)
                if not ids:
                    continue
                time.sleep(f.SLEEP_S)
                articles = f.efetch_abstracts(ids)
                best = f.pick_best(articles, botanik)
                if best:
                    found = best
                    used = term
                    break
            if found:
                results[pid] = {
                    "status": "ok",
                    "plantId": entry.get("plantId") or int(pid),
                    "ad": ad,
                    "botanikAd": botanik,
                    "searchTerm": used,
                    "pmid": found["pmid"],
                    "title": found["title"],
                    "year": found["year"],
                    "abstract": found["abstract"],
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{found['pmid']}/",
                    "round": 2,
                }
                print(f"  -> PMID {found['pmid']}", flush=True)
            else:
                print("  -> hala yok", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"  -> HATA: {exc}", flush=True)
        PROGRESS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for v in results.values() if v.get("status") == "ok")
    none = sum(1 for v in results.values() if v.get("status") == "none")
    print(f"Bitti. ok={ok} none={none}")
    (ROOT / "data" / "pubmed-vakalar-raw.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
