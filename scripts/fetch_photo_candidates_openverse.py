# -*- coding: utf-8 -*-
"""iNaturalist adaylari yetersiz kalan bitkiler icin Openverse'ten aday indirir.

iNaturalist bilimsel dogruluk icin iyi ama kultur formlarinda (mor feslegen,
bahce sardunyasi, enginar basi) taninabilir gorsel vermiyor; bu bosluk
Openverse'in CC lisansli fotograflariyla dolduruluyor.
Secim yine gorsel kontrolle yapilir.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

CAND_DIR = Path(__file__).resolve().parent / "_candidates"
UA = "DogalBitkilerRehberi/1.4 (educational local project; plant card photos)"

# id -> Openverse arama terimi
TARGETS: dict[int, str] = {
    34: "purple basil",
    60: "artichoke plant",
    202: "Salvia miltiorrhiza",
}

MAX_CANDIDATES = 6
# Openverse adaylari, iNat adaylariyla karismasin diye 900+ indekste tutulur
INDEX_OFFSET = 900


def http_json(url: str, timeout: int = 45, retries: int = 3):
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(3 + attempt * 4)
    raise last  # type: ignore[misc]


def openverse(term: str) -> list[str]:
    # "category=photograph" filtresi sonuclari sifirladigi icin kullanilmiyor.
    params = urllib.parse.urlencode(
        {
            "q": term,
            "page_size": 20,
            "license": "cc0,pdm,by,by-sa",
        }
    )
    payload = http_json(f"https://api.openverse.org/v1/images/?{params}")
    urls = []
    for item in payload.get("results") or []:
        src = item.get("url")
        if src and str(src).startswith("http"):
            urls.append(str(src))
    return urls


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    if len(data) < 8000:
        raise RuntimeError(f"cok kucuk ({len(data)})")
    dest.write_bytes(data)


def main() -> None:
    manifest_path = CAND_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for plant_id, term in TARGETS.items():
        print(f"[{plant_id}] openverse: {term}")
        try:
            urls = openverse(term)
        except Exception as exc:  # noqa: BLE001
            print(f"   hata: {exc}")
            continue

        entries = [e for e in manifest.get(str(plant_id), []) if e["index"] < INDEX_OFFSET]
        added = 0
        for url in urls:
            if added >= MAX_CANDIDATES:
                break
            idx = INDEX_OFFSET + added + 1
            dest = CAND_DIR / f"{plant_id:03d}-{idx}.jpg"
            try:
                download(url, dest)
                entries.append({"index": idx, "file": dest.name, "url": url})
                added += 1
                print(f"   aday {idx}: {dest.name}")
            except Exception as exc:  # noqa: BLE001
                print(f"   atlandi: {exc}")
            time.sleep(0.4)

        manifest[str(plant_id)] = entries
        time.sleep(1.0)

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("\nBitti.")


if __name__ == "__main__":
    main()
