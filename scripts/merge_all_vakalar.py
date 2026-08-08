#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pubmed-vaka-ozetleri.json + gap-vaka-ozetleri.json -> plants.json ornekVaka
Metinleri sade tutar; hayvan modeli / bos kayitlari atlar.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANTS = ROOT / "data" / "plants.json"
OZET = ROOT / "data" / "pubmed-vaka-ozetleri.json"
GAP = ROOT / "data" / "gap-vaka-ozetleri.json"
RAW = ROOT / "data" / "pubmed-vakalar-progress.json"
GAP_RAW = ROOT / "data" / "pubmed-gap-fill-raw.json"


def is_animal(blob: str) -> bool:
    return bool(
        re.search(
            r"\b(rat|rats|mice|mouse|murine|in vitro|cell line|sıçan|fare modeli)\b",
            blob,
            re.I,
        )
    )


def main() -> None:
    plants = json.loads(PLANTS.read_text(encoding="utf-8"))
    ozet = json.loads(OZET.read_text(encoding="utf-8")) if OZET.exists() else {}
    gap = json.loads(GAP.read_text(encoding="utf-8")) if GAP.exists() else {}
    raw = json.loads(RAW.read_text(encoding="utf-8")) if RAW.exists() else {}
    gap_raw = json.loads(GAP_RAW.read_text(encoding="utf-8")) if GAP_RAW.exists() else {}

    # gap ozetleri onceki ozetlerin ustune yazabilir (eksikleri doldurur)
    merged_ozet = {**ozet, **gap}

    updated = 0
    skipped_animal = 0

    for plant in plants:
        if plant.get("tur") != "Tıbbi Bitkiler":
            plant.pop("ornekVaka", None)
            continue

        pid = str(plant["id"])
        from_gap = pid in gap
        o = merged_ozet.get(pid)
        meta = None
        if from_gap:
            meta = gap_raw.get(pid) if gap_raw.get(pid, {}).get("status") == "ok" else None
        elif raw.get(pid, {}).get("status") == "ok":
            meta = raw.get(pid)

        if not o:
            if meta and meta.get("status") == "ok" and meta.get("pmid"):
                o = {
                    "baslik": f"{plant['ad']} — yayımlanmış klinik örnek",
                    "sorun": "Yayımlanan klinik kayıtta kişinin sağlık şikayeti anlatılmıştır.",
                    "yaklasim": f"{plant['ad']} içeren bitkisel yaklaşım klinik olarak belgelenmiştir.",
                    "sonuc": "Ayrıntılar kaynak makalede yer alır.",
                    "anlatim": (
                        f"Güvenilir tıbbi kaynaklarda {plant['ad']} ile ilgili gerçek bir klinik "
                        f"kayıt yayımlanmıştır. Makale başlığı: “{meta.get('title') or 'Klinik kayıt'}”. "
                        "Tam ayrıntı için kaynak bağlantısına bakabilirsiniz."
                    ),
                }
            else:
                plant.pop("ornekVaka", None)
                continue

        pmid = str(o.get("pubmedId") or (meta or {}).get("pmid") or "").strip()
        url = (
            o.get("pubmedUrl")
            or (meta or {}).get("url")
            or (f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "")
        )
        title = o.get("makaleBasligi") or (meta or {}).get("title") or ""
        year = o.get("yil") or (meta or {}).get("year") or ""

        # Hayvan modeli kontrolu: gap ile elle eklenen insan vakalarinda eski ham ozeti yok say
        check_blob = " ".join(
            [
                o.get("baslik", ""),
                o.get("anlatim", ""),
                o.get("sorun", ""),
                title,
            ]
        )
        if not from_gap:
            check_blob += " " + ((meta or {}).get("abstract") or "")

        if is_animal(check_blob):
            plant.pop("ornekVaka", None)
            skipped_animal += 1
            continue

        plant["ornekVaka"] = {
            "baslik": o.get("baslik") or f"{plant['ad']} — gerçek klinik örnek",
            "sorun": o.get("sorun") or "",
            "yaklasim": o.get("yaklasim") or o.get("yaklaşım") or "",
            "sonuc": o.get("sonuc") or "",
            "anlatim": o.get("anlatim") or "",
            "pubmedId": pmid,
            "pubmedUrl": url,
            "makaleBasligi": title,
            "yil": year,
            "kaynakAdi": o.get("kaynakAdi") or ("PubMed" if pmid else "Klinik kaynak"),
        }
        updated += 1

    PLANTS.write_text(json.dumps(plants, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    med = [p for p in plants if p.get("tur") == "Tıbbi Bitkiler"]
    have = sum(1 for p in med if p.get("ornekVaka"))
    print(f"updated={updated} medicinal_with_vaka={have}/{len(med)} skipped_animal={skipped_animal}")


if __name__ == "__main__":
    main()
