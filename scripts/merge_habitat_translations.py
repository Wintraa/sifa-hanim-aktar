# -*- coding: utf-8 -*-
"""habitats_tr_*.json parcalarini tek habitats_tr.json dosyasinda birlestirir."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PFAF_DIR = ROOT / "data" / "pfaf"
OUT = PFAF_DIR / "habitats_tr.json"

ENGLISH_HINTS = re.compile(
    r"\b(the|and|woodland|meadows|roadsides|found|places|soils|banks)\b",
    re.I,
)


def main() -> None:
    todo: dict[str, str] = {}
    for path in sorted(PFAF_DIR.glob("habitats_todo_*.json")):
        todo.update(json.loads(path.read_text(encoding="utf-8")))

    merged: dict[str, str] = {}
    for path in sorted(PFAF_DIR.glob("habitats_tr_*.json")):
        chunk = json.loads(path.read_text(encoding="utf-8"))
        merged.update({k: (v or "").strip() for k, v in chunk.items()})
        print(f"{path.name}: {len(chunk)} kayit")

    missing = sorted(set(todo) - set(merged))
    extra = sorted(set(merged) - set(todo))
    empty = sorted(k for k, v in merged.items() if not v)
    suspicious = sorted(
        k for k, v in merged.items() if v and len(ENGLISH_HINTS.findall(v)) >= 2
    )

    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\nBirlestirildi: {len(merged)} / kaynak {len(todo)}")
    print(f"Eksik: {len(missing)}  Fazla: {len(extra)}  Bos: {len(empty)}")
    print(f"Ingilizce kalmis olabilir: {len(suspicious)}")
    for k in suspicious[:15]:
        print("  -", k, "->", merged[k][:90])
    print(f"Yazildi: {OUT}")


if __name__ == "__main__":
    main()
