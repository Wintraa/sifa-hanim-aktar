# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "data" / "medicinal"
req = [
    "id",
    "commonNameTr",
    "commonNameEn",
    "botanicalName",
    "category",
    "medicinalUses",
    "activeCompounds",
    "edibleParts",
    "warnings",
    "summary",
]

all_plants = []
for i in range(1, 9):
    path = root / f"plants_part{i}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    bad = [
        x.get("id")
        for x in data
        if any(k not in x or not str(x[k]).strip() for k in req)
    ]
    first = data[0]["id"] if data else "-"
    last = data[-1]["id"] if data else "-"
    print(f"part{i}: n={len(data)} ids={first}-{last} missing_fields={bad[:5]}")
    all_plants.extend(data)

print("TOTAL", len(all_plants))
ids = [p["id"] for p in all_plants]
bots = [p["botanicalName"].lower().strip() for p in all_plants]
print("dup_ids", [k for k, v in Counter(ids).items() if v > 1][:20])
print("dup_bots", [k for k, v in Counter(bots).items() if v > 1][:30])
print("categories", Counter(p["category"] for p in all_plants))

expected = [f"{n:03d}" for n in range(1, 201)]
missing = [e for e in expected if e not in ids]
extra = [i for i in ids if i not in expected]
print("missing_ids_count", len(missing), missing[:30])
print("extra_ids", extra[:20])

# Write combined index for convenience
combined_path = root / "plants_all.json"
combined_path.write_text(
    json.dumps(all_plants, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print("wrote", combined_path)
