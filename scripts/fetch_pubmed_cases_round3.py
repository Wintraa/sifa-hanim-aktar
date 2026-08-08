#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zayif/adverse eslesmeler icin tedavi odakli yeniden arama."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import fetch_pubmed_cases as f
import score_pubmed_cases as s

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = ROOT / "data" / "pubmed-vakalar-progress.json"
QUALITY = ROOT / "data" / "pubmed-vaka-kalite.json"


def therapeutic_terms(botanik: str) -> list[str]:
    latin = f.clean_botanical(botanik)
    return [
        (
            f'("{latin}"[Title/Abstract]) AND Case Reports[Publication Type] '
            f'AND (treatment[Title/Abstract] OR therapy[Title/Abstract]) '
            f'AND (improved[Title/Abstract] OR improvement[Title/Abstract] OR '
            f'successful[Title/Abstract] OR remission[Title/Abstract] OR '
            f'resolved[Title/Abstract] OR recovery[Title/Abstract] OR benefit[Title/Abstract]) '
            f'NOT (anaphylaxis[Title/Abstract] OR allergy[Title/Abstract] OR poisoning[Title/Abstract])'
        ),
        (
            f'("{latin}"[Title/Abstract]) AND ("case report"[Title/Abstract]) '
            f'AND (herbal[Title/Abstract] OR phytotherapy[Title/Abstract] OR extract[Title/Abstract]) '
            f'AND (patient[Title/Abstract]) '
            f'NOT (review[Publication Type])'
        ),
        (
            f'("{latin}"[Title/Abstract]) AND Case Reports[Publication Type] '
            f'AND (complementary[Title/Abstract] OR traditional[Title/Abstract] OR Ayurvedic[Title/Abstract])'
        ),
    ]


def better(new_entry: dict, old_entry: dict) -> bool:
    new_q = s.classify(new_entry)["quality"]
    old_q = s.classify(old_entry)["quality"]
    rank = {"good": 3, "adverse": 1, "weak": 0, "none": -1}
    if rank.get(new_q, 0) > rank.get(old_q, 0):
        return True
    if new_q == old_q == "good":
        # Terapotik kelime sayisi
        def tscore(e: dict) -> int:
            blob = f"{e.get('title','')} {e.get('abstract','')}".lower()
            return len(re.findall(r"improv|resolv|successful|remission|benefit|relief", blob))

        return tscore(new_entry) > tscore(old_entry)
    return False


def main() -> None:
    results = json.loads(PROGRESS.read_text(encoding="utf-8"))
    quality = json.loads(QUALITY.read_text(encoding="utf-8"))["items"]
    targets = [
        pid
        for pid, q in quality.items()
        if q.get("quality") in {"weak", "adverse"}
    ]
    # none olanlari da ekle
    targets += [pid for pid, v in results.items() if v.get("status") == "none"]
    targets = sorted(set(targets), key=lambda x: int(x))
    print(f"Yeniden arama: {len(targets)} bitki")

    improved = 0
    for i, pid in enumerate(targets, 1):
        entry = results[pid]
        ad = entry.get("ad", "")
        botanik = entry.get("botanikAd", "")
        print(f"[{i}/{len(targets)}] {ad}...", flush=True)
        best_found = None
        used = ""
        try:
            for term in therapeutic_terms(botanik):
                time.sleep(f.SLEEP_S)
                ids = f.esearch(term, retmax=10)
                if not ids:
                    continue
                time.sleep(f.SLEEP_S)
                articles = f.efetch_abstracts(ids)
                cand = f.pick_best(articles, botanik)
                if not cand:
                    continue
                candidate = {
                    "status": "ok",
                    "plantId": entry.get("plantId") or int(pid),
                    "ad": ad,
                    "botanikAd": botanik,
                    "searchTerm": term,
                    "pmid": cand["pmid"],
                    "title": cand["title"],
                    "year": cand["year"],
                    "abstract": cand["abstract"],
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{cand['pmid']}/",
                    "round": 3,
                }
                if best_found is None or better(candidate, best_found):
                    best_found = candidate
                    used = term
            if best_found and (entry.get("status") != "ok" or better(best_found, entry)):
                results[pid] = best_found
                improved += 1
                print(f"  -> guncellendi PMID {best_found['pmid']}", flush=True)
            else:
                print("  -> ayni/iyi aday yok", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"  -> HATA: {exc}", flush=True)
        PROGRESS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    (ROOT / "data" / "pubmed-vakalar-raw.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Bitti. improved={improved}")


if __name__ == "__main__":
    main()
