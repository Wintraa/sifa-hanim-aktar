# -*- coding: utf-8 -*-
"""Bitki verilerini Gemini genişletmesi için 50.000 karakterlik MD dosyalarına böler.

Kural: Bir bitki asla iki dosyaya bölünmez. Bir sonraki bitki eklenince
dosya 50.000 karakteri aşacaksa o bitki sonraki dosyaya bırakılır.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "plants.json"
OUT_DIR = ROOT / "exports" / "gemini-md"
CHAR_LIMIT = 50_000


def plant_to_md(plant: dict) -> str:
    """Tek bitkinin tüm site + PFAF ham bilgilerini MD bloğu olarak yazar."""
    tb = plant.get("temelBilgiler") or {}
    sk = plant.get("saglikKullanim") or {}
    cm = plant.get("cografyaMevsim") or {}
    by = plant.get("bakimYetistirme") or {}
    kay = plant.get("kaynak") or {}
    pfaf = plant.get("_pfafOrijinal") or {}

    lines = [
        f"## {plant.get('ad', '')} (id: {plant.get('id')})",
        "",
        f"- **Botanik ad:** {plant.get('botanikAd', '')}",
        f"- **Kategori:** {plant.get('tur', '')}",
        f"- **Türkçe adı:** {tb.get('turkceAdi', plant.get('ad', ''))}",
        f"- **Botanik adı:** {tb.get('botanikAdi', plant.get('botanikAd', ''))}",
        f"- **Bitki türü:** {tb.get('bitkiTuru', '')}",
        "",
        "### Genel tanıtım",
        "",
        (plant.get("genelTavsiyeMetni") or "").strip() or "—",
        "",
        "### Sağlık ve kullanım",
        "",
        f"- **Faydaları:** {(sk.get('faydalari') or '—').strip()}",
        f"- **Kullanım şekli:** {(sk.get('kullanimSekli') or '—').strip()}",
        f"- **Yan etkiler ve uyarılar:** {(sk.get('yanEtkilerUyarilar') or '—').strip()}",
        "",
        "### Coğrafya ve mevsim",
        "",
        f"- **Yetiştiği yerler:** {(cm.get('yetistigiYerler') or '—').strip()}",
        f"- **Hasat mevsimi:** {(cm.get('hasatMevsimi') or '—').strip()}",
        f"- **Çiçeklenme zamanı:** {(cm.get('ciceklenmeZamani') or '—').strip()}",
        "",
        "### Bakım ve yetiştirme",
        "",
        f"- **Işık ihtiyacı:** {(by.get('isikIhtiyaci') or '—').strip()}",
        f"- **Sulama sıklığı:** {(by.get('sulamaSikligi') or '—').strip()}",
        f"- **Toprak tipi:** {(by.get('toprakTipi') or '—').strip()}",
        "",
        "### Kaynak",
        "",
        f"- **Ad:** {(kay.get('ad') or '—').strip()}",
        f"- **URL:** {(kay.get('url') or '—').strip()}",
    ]
    if kay.get("altUrl"):
        lines.append(f"- **Ek URL:** {kay['altUrl']}")
    if kay.get("eslesenAd"):
        lines.append(f"- **Eşleşen ad:** {kay['eslesenAd']}")
    if kay.get("derece"):
        lines.append(f"- **Derece:** {kay['derece']}")
    if kay.get("not"):
        lines.append(f"- **Not:** {kay['not']}")
    if kay.get("cekimTarihi"):
        lines.append(f"- **Çekim tarihi:** {kay['cekimTarihi']}")

    if pfaf:
        lines.extend(["", "### PFAF ham kayıt (İngilizce kaynak metin)", ""])
        for key, label in (
            ("knownHazards", "Known hazards"),
            ("medicinalUses", "Medicinal uses"),
            ("edibleUses", "Edible uses"),
            ("physicalCharacteristics", "Physical characteristics"),
            ("range", "Range"),
            ("cultivationDetails", "Cultivation details"),
        ):
            val = (pfaf.get(key) or "").strip()
            if val:
                lines.append(f"**{label}:**")
                lines.append("")
                lines.append(val)
                lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def file_header(part: int, plant_count: int, id_min: int, id_max: int) -> str:
    return (
        f"# Doğal Bitkiler Ansiklopedisi — Gemini genişletme paketi {part:02d}\n"
        f"\n"
        f"Bu dosya sitedeki mevcut bitki bilgilerini içerir. "
        f"Her bitki bloğu eksiksizdir; karakter sınırı {CHAR_LIMIT} "
        f"(aşılmadan önceki son bitki dahil edilir).\n"
        f"Bu pakette {plant_count} bitki vardır (id {id_min}-{id_max}).\n"
        f"\n---\n\n"
    )


def build_content(part: int, plist: list[dict], body: str) -> str:
    ids = [int(p["id"]) for p in plist]
    return file_header(part, len(plist), min(ids), max(ids)) + body


def main() -> None:
    plants = json.loads(DATA.read_text(encoding="utf-8"))
    plants = sorted(plants, key=lambda p: int(p.get("id") or 0))

    blocks = []
    for p in plants:
        md = plant_to_md(p)
        # Başlık + tek bitki bile sığmalı
        probe = file_header(99, 1, int(p["id"]), int(p["id"])) + md
        if len(probe) > CHAR_LIMIT:
            raise SystemExit(
                f"Tek bitki limiti aşıyor: id={p.get('id')} ad={p.get('ad')} "
                f"len={len(probe)} > {CHAR_LIMIT}"
            )
        blocks.append((p, md))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("bitkiler-part-*.md"):
        old.unlink()

    # Greedy paketleme: gerçek başlık uzunluğuyla ölç
    parts: list[tuple[int, list[dict], str]] = []
    part_num = 1
    current_plants: list[dict] = []
    current_blocks: list[str] = []

    for plant, block in blocks:
        trial_plants = current_plants + [plant]
        trial_body = "".join(current_blocks + [block])
        trial = build_content(part_num, trial_plants, trial_body)

        if current_plants and len(trial) > CHAR_LIMIT:
            # Son bitkiyi alma; dosyayı kapat
            body = "".join(current_blocks)
            parts.append((part_num, current_plants, body))
            part_num += 1
            current_plants = [plant]
            current_blocks = [block]
            # Yeni dosyada tek bitki mutlaka sığmalı (yukarıda kontrol edildi)
            if len(build_content(part_num, current_plants, block)) > CHAR_LIMIT:
                raise SystemExit(f"Yeni part'a sığmıyor: id={plant['id']}")
        else:
            current_plants = trial_plants
            current_blocks.append(block)

    if current_plants:
        parts.append((part_num, current_plants, "".join(current_blocks)))

    index_lines = [
        "# Gemini MD paketleri",
        "",
        f"Toplam bitki: {len(plants)}",
        f"Karakter sınırı: {CHAR_LIMIT:,} (Unicode karakter; 50001 olursa son bitki alınmaz)",
        f"Dosya sayısı: {len(parts)}",
        "",
        "| Dosya | Bitki sayısı | Karakter | ID aralığı | İlk–son |",
        "|-------|--------------|----------|------------|---------|",
    ]

    for num, plist, body in parts:
        content = build_content(num, plist, body)
        if len(content) > CHAR_LIMIT:
            raise SystemExit(f"part {num} overflow: {len(content)}")

        name = f"bitkiler-part-{num:02d}.md"
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        ids = [int(p["id"]) for p in plist]
        index_lines.append(
            f"| `{name}` | {len(plist)} | {len(content):,} | "
            f"{min(ids)}–{max(ids)} | {plist[0]['ad']} -> {plist[-1]['ad']} |"
        )
        print(f"OK {name}: {len(plist)} bitki, {len(content)} karakter")

    (OUT_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"\nToplam {len(parts)} dosya -> {OUT_DIR}")


if __name__ == "__main__":
    main()
