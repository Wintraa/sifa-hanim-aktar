#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zayif PubMed eslesmelerini isaretler (inceleme, yan etki, bitki yan rol)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "pubmed-vakalar-progress.json"
OUT = ROOT / "data" / "pubmed-vaka-kalite.json"


def classify(entry: dict) -> dict:
    title = (entry.get("title") or "").lower()
    abstract = (entry.get("abstract") or "").lower()
    botanik = (entry.get("botanikAd") or "").lower()
    latin = " ".join(botanik.split()[:2])
    genus = botanik.split()[0] if botanik else ""
    blob = f"{title} {abstract}"

    flags = []
    if re.search(r"\b(review|meta-analysis|systematic review)\b", blob):
        flags.append("review")
    if re.search(r"\b(anaphylax|allergic|allergy|angioedema|poisoning|toxicity|intoxication|contamination)\b", blob):
        flags.append("adverse")
    if re.search(r"\b(improv|resolv|remission|successful|benefit|relief|recover|cured|cure|maintenance treatment)\b", blob):
        flags.append("therapeutic")
    if latin and latin not in blob and genus and genus not in blob:
        flags.append("name_weak")
    # Bitki yalnizca uzun listede geciyorsa
    if abstract.count(",") > 12 and latin and blob.count(latin) <= 1:
        flags.append("peripheral")

    quality = "good"
    if "review" in flags or "peripheral" in flags or "name_weak" in flags:
        quality = "weak"
    elif "adverse" in flags and "therapeutic" not in flags:
        quality = "adverse"
    elif "therapeutic" in flags:
        quality = "good"

    return {
        "plantId": entry.get("plantId"),
        "ad": entry.get("ad"),
        "pmid": entry.get("pmid"),
        "quality": quality,
        "flags": flags,
        "title": entry.get("title"),
    }


def main() -> None:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    report = {}
    counts = {"good": 0, "adverse": 0, "weak": 0, "none": 0}
    for pid, entry in raw.items():
        if entry.get("status") != "ok":
            counts["none"] += 1
            continue
        c = classify(entry)
        report[pid] = c
        counts[c["quality"]] = counts.get(c["quality"], 0) + 1

    OUT.write_text(json.dumps({"counts": counts, "items": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(counts)


if __name__ == "__main__":
    main()
