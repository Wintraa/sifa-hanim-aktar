#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plants.json -> SQLite (database/bitki.db) aktarım scripti.

Kullanım:
    python scripts/init_db.py

Ne yapar?
    1. database/bitki.db dosyasını oluşturur (veya sıfırlar)
    2. database/schema.sql ile tabloları açar
    3. data/plants.json içindeki 212 bitkiyi yazar
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "bitki.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"
PLANTS_PATH = ROOT / "data" / "plants.json"


def json_dumps(value) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    if not PLANTS_PATH.exists():
        print(f"HATA: {PLANTS_PATH} bulunamadi.")
        return 1

    plants = json.loads(PLANTS_PATH.read_text(encoding="utf-8"))
    if SCHEMA_PATH.exists():
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
    else:
        # schema.sql yoksa gomulu sema kullan
        schema = """
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS bitkiler (
            id INTEGER PRIMARY KEY, ad TEXT NOT NULL, botanik_ad TEXT NOT NULL,
            tur TEXT NOT NULL, resim_url TEXT, genel_tavsiye TEXT, eski_id INTEGER,
            temel_bilgiler TEXT, saglik_kullanim TEXT, cografya_mevsim TEXT,
            bakim_yetistirme TEXT, kaynak TEXT, pfaf_orijinal TEXT,
            olusturulma TEXT DEFAULT (datetime('now')),
            guncelleme TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_bitkiler_tur ON bitkiler(tur);
        CREATE INDEX IF NOT EXISTS idx_bitkiler_ad ON bitkiler(ad);
        CREATE TABLE IF NOT EXISTS ornek_vakalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, bitki_id INTEGER NOT NULL UNIQUE,
            baslik TEXT, sorun TEXT, yaklasim TEXT, sonuc TEXT, anlatim TEXT,
            pubmed_id TEXT, pubmed_url TEXT, makale_basligi TEXT, yil TEXT, kaynak_adi TEXT,
            FOREIGN KEY (bitki_id) REFERENCES bitkiler(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_vakalar_bitki ON ornek_vakalar(bitki_id);
        """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(schema)

        bitki_rows = []
        vaka_rows = []

        for plant in plants:
            bitki_rows.append(
                (
                    plant["id"],
                    plant["ad"],
                    plant["botanikAd"],
                    plant["tur"],
                    plant.get("resimUrl"),
                    plant.get("genelTavsiyeMetni"),
                    plant.get("eskiId"),
                    json_dumps(plant.get("temelBilgiler")),
                    json_dumps(plant.get("saglikKullanim")),
                    json_dumps(plant.get("cografyaMevsim")),
                    json_dumps(plant.get("bakimYetistirme")),
                    json_dumps(plant.get("kaynak")),
                    json_dumps(plant.get("_pfafOrijinal")),
                )
            )

            vaka = plant.get("ornekVaka")
            if vaka:
                vaka_rows.append(
                    (
                        plant["id"],
                        vaka.get("baslik"),
                        vaka.get("sorun"),
                        vaka.get("yaklasim"),
                        vaka.get("sonuc"),
                        vaka.get("anlatim"),
                        str(vaka.get("pubmedId") or ""),
                        vaka.get("pubmedUrl"),
                        vaka.get("makaleBasligi"),
                        str(vaka.get("yil") or ""),
                        vaka.get("kaynakAdi"),
                    )
                )

        conn.executemany(
            """
            INSERT INTO bitkiler (
                id, ad, botanik_ad, tur, resim_url, genel_tavsiye, eski_id,
                temel_bilgiler, saglik_kullanim, cografya_mevsim,
                bakim_yetistirme, kaynak, pfaf_orijinal
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            bitki_rows,
        )

        conn.executemany(
            """
            INSERT INTO ornek_vakalar (
                bitki_id, baslik, sorun, yaklasim, sonuc, anlatim,
                pubmed_id, pubmed_url, makale_basligi, yil, kaynak_adi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            vaka_rows,
        )

        conn.commit()

        bitki_count = conn.execute("SELECT COUNT(*) FROM bitkiler").fetchone()[0]
        vaka_count = conn.execute("SELECT COUNT(*) FROM ornek_vakalar").fetchone()[0]
        tur_count = conn.execute(
            "SELECT tur, COUNT(*) AS n FROM bitkiler GROUP BY tur ORDER BY n DESC"
        ).fetchall()

        print("Veritabani hazir!")
        print(f"  Dosya: {DB_PATH}")
        print(f"  Bitki: {bitki_count}")
        print(f"  Ornek vaka: {vaka_count}")
        print("  Tur dagilimi:")
        for row in tur_count:
            print(f"    - {row['tur']}: {row['n']}")

    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
