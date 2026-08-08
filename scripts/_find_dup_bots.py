# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "data" / "medicinal"
parts = {}
for i in range(1, 9):
    path = root / f"plants_part{i}.json"
    parts[i] = json.loads(path.read_text(encoding="utf-8"))

# id -> (part, index, plant)
by_bot = defaultdict(list)
for part_no, plants in parts.items():
    for idx, plant in enumerate(plants):
        key = plant["botanicalName"].lower().strip()
        by_bot[key].append((part_no, idx, plant["id"], plant["commonNameTr"]))

for key, items in by_bot.items():
    if len(items) > 1:
        print(key, items)
