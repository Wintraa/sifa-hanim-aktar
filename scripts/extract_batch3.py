import json

with open(r'C:\Users\musta\OneDrive\Desktop\Bitki\data\vaka-rewrite-input.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

n = len(data)
start = 2 * n // 3
batch = data[start:]
print(f'Total items: {n}, start index: {start}, count: {len(batch)}')
for i, item in enumerate(batch, start):
    print(f'{i}: id={item.get("id")} ad={item.get("ad")} pmid={item.get("pmid")}')

# Write batch to temp file for processing
with open(r'C:\Users\musta\OneDrive\Desktop\Bitki\data\vaka-rewrite-batch3-raw.json', 'w', encoding='utf-8') as f:
    json.dump(batch, f, ensure_ascii=False, indent=2)
