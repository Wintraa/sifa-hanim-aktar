#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Veritabanini test etmek icin basit sorgu araci.

Ornekler:
    python scripts/db_query.py list
    python scripts/db_query.py get 1
    python scripts/db_query.py search papatya
    python scripts/db_query.py tur "Tıbbi Bitkiler"
    python scripts/db_query.py eksik
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "bitki.db"


def connect():
    if not DB_PATH.exists():
        print("HATA: Once python scripts/init_db.py calistirin.")
        print(f"      Beklenen dosya: {DB_PATH}")
        raise SystemExit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def cmd_list(limit: int = 10) -> None:
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, ad, tur FROM bitkiler ORDER BY id LIMIT ?", (limit,)
        ).fetchall()
    print(f"Ilk {limit} bitki:")
    for r in rows:
        print(f"  [{r['id']}] {r['ad']} ({r['tur']})")


def cmd_get(plant_id: int) -> None:
    with connect() as conn:
        plant = conn.execute(
            "SELECT * FROM bitkiler WHERE id = ?", (plant_id,)
        ).fetchone()
        vaka = conn.execute(
            "SELECT * FROM ornek_vakalar WHERE bitki_id = ?", (plant_id,)
        ).fetchone()

    if not plant:
        print(f"Bitki bulunamadi: id={plant_id}")
        return

    print(f"=== {plant['ad']} ({plant['botanik_ad']}) ===")
    print(f"Tur: {plant['tur']}")
    print(f"Resim: {plant['resim_url']}")
    print(f"Tavsiye: {(plant['genel_tavsiye'] or '')[:120]}...")

    if vaka:
        print("\n--- Ornek vaka ---")
        print(f"Baslik: {vaka['baslik']}")
        print(f"Sorun: {(vaka['sorun'] or '')[:160]}...")
        print(f"Sonuc: {(vaka['sonuc'] or '')[:160]}...")
    else:
        print("\n(Bu bitkide ornek vaka kaydi yok)")


def cmd_search(term: str, limit: int = 10) -> None:
    like = f"%{term}%"
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, ad, botanik_ad, tur
            FROM bitkiler
            WHERE ad LIKE ? OR botanik_ad LIKE ?
            ORDER BY ad
            LIMIT ?
            """,
            (like, like, limit),
        ).fetchall()

    print(f"'{term}' aramasi -> {len(rows)} sonuc:")
    for r in rows:
        print(f"  [{r['id']}] {r['ad']} | {r['botanik_ad']} | {r['tur']}")


def cmd_tur(tur: str, limit: int = 20) -> None:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, ad FROM bitkiler
            WHERE tur = ?
            ORDER BY ad
            LIMIT ?
            """,
            (tur, limit),
        ).fetchall()

    print(f"Tur: {tur} -> {len(rows)} kayit (max {limit}):")
    for r in rows:
        print(f"  [{r['id']}] {r['ad']}")


def cmd_eksik(limit: int = 50) -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bulunamayan_aramalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arama_metni TEXT NOT NULL,
                arama_norm TEXT NOT NULL,
                tekrar_sayisi INTEGER NOT NULL DEFAULT 1,
                ilk_tarih TEXT DEFAULT (datetime('now','localtime')),
                son_tarih TEXT DEFAULT (datetime('now','localtime'))
            )
            """
        )
        rows = conn.execute(
            """
            SELECT arama_metni, tekrar_sayisi, son_tarih
            FROM bulunamayan_aramalar
            ORDER BY tekrar_sayisi DESC, son_tarih DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    if not rows:
        print("Henuz bulunamayan arama kaydi yok.")
        return

    print(f"Bulunamayan aramalar ({len(rows)}):")
    for r in rows:
        print(f"  {r['tekrar_sayisi']}x  {r['arama_metni']}  (son: {r['son_tarih']})")


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print(__doc__)
        return 0

    cmd = sys.argv[1].lower()

    if cmd == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        cmd_list(limit)
    elif cmd == "get":
        if len(sys.argv) < 3:
            print("Kullanim: python scripts/db_query.py get <id>")
            return 1
        cmd_get(int(sys.argv[2]))
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Kullanim: python scripts/db_query.py search <kelime>")
            return 1
        cmd_search(" ".join(sys.argv[2:]))
    elif cmd == "tur":
        if len(sys.argv) < 3:
            print('Kullanim: python scripts/db_query.py tur "Tıbbi Bitkiler"')
            return 1
        cmd_tur(" ".join(sys.argv[2:]))
    elif cmd == "eksik":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        cmd_eksik(limit)
    else:
        print(f"Bilinmeyen komut: {cmd}")
        print(__doc__)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
