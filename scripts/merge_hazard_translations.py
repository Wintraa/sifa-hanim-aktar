# -*- coding: utf-8 -*-
"""hazards_tr_*.json parcalarini tek hazards_tr.json dosyasinda birlestirir.

Ayrica denetim yapar: her ceviri kaydinin kaynakta karsiligi var mi,
eksik/fazla anahtar var mi, ingilizce kalmis metin var mi.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PFAF_DIR = ROOT / "data" / "pfaf"
OUT = PFAF_DIR / "hazards_tr.json"

# Cevrilmemis metni yakalamak icin sik ingilizce kelimeler
ENGLISH_HINTS = re.compile(
    r"\b(the|and|should|plant|leaves|poisonous|toxic|avoid|may cause|contains)\b",
    re.I,
)


def main() -> None:
    todo: dict[str, str] = {}
    for path in sorted(PFAF_DIR.glob("hazards_todo_*.json")):
        todo.update(json.loads(path.read_text(encoding="utf-8")))

    merged: dict[str, str] = {}
    duplicates: list[str] = []
    for path in sorted(PFAF_DIR.glob("hazards_tr_*.json")):
        chunk = json.loads(path.read_text(encoding="utf-8"))
        for key, value in chunk.items():
            if key in merged and merged[key] != value:
                duplicates.append(key)
            merged[key] = (value or "").strip()
        print(f"{path.name}: {len(chunk)} kayit")

    missing = sorted(set(todo) - set(merged))
    extra = sorted(set(merged) - set(todo))
    empty = sorted(k for k, v in merged.items() if not v)
    suspicious = sorted(
        k
        for k, v in merged.items()
        if v and len(ENGLISH_HINTS.findall(v)) >= 2
    )

    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nBirlestirildi: {len(merged)} / kaynak {len(todo)}")
    print(f"Eksik ceviri : {len(missing)}")
    for k in missing[:20]:
        print("   -", k)
    print(f"Fazla anahtar: {len(extra)}")
    for k in extra[:20]:
        print("   -", k)
    print(f"Bos ceviri   : {len(empty)}")
    for k in empty[:20]:
        print("   -", k)
    print(f"Ingilizce kalmis olabilir: {len(suspicious)}")
    for k in suspicious[:20]:
        print("   -", k, "->", merged[k][:80])
    if duplicates:
        print(f"Cakisan anahtar: {len(duplicates)} {duplicates[:10]}")

    print(f"\nYazildi: {OUT}")


if __name__ == "__main__":
    main()
