# -*- coding: utf-8 -*-
"""SQLite -> site JSON formatina donusturme."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "bitki.db"

JSON_FIELDS = (
    ("temel_bilgiler", "temelBilgiler"),
    ("saglik_kullanim", "saglikKullanim"),
    ("cografya_mevsim", "cografyaMevsim"),
    ("bakim_yetistirme", "bakimYetistirme"),
    ("kaynak", "kaynak"),
    ("pfaf_orijinal", "_pfafOrijinal"),
)


def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Veritabani bulunamadi: {DB_PATH}. Once: python scripts/init_db.py"
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _parse_json(value: str | None):
    if not value:
        return None
    return json.loads(value)


def vaka_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "baslik": row["baslik"],
        "sorun": row["sorun"],
        "yaklasim": row["yaklasim"],
        "sonuc": row["sonuc"],
        "anlatim": row["anlatim"],
        "pubmedId": row["pubmed_id"] or "",
        "pubmedUrl": row["pubmed_url"],
        "makaleBasligi": row["makale_basligi"],
        "yil": row["yil"] or "",
        "kaynakAdi": row["kaynak_adi"],
    }


def plant_row_to_dict(row: sqlite3.Row, vaka: sqlite3.Row | None = None) -> dict:
    plant: dict = {
        "id": row["id"],
        "ad": row["ad"],
        "botanikAd": row["botanik_ad"],
        "tur": row["tur"],
        "resimUrl": row["resim_url"],
        "genelTavsiyeMetni": row["genel_tavsiye"],
    }
    if row["eski_id"] is not None:
        plant["eskiId"] = row["eski_id"]

    for db_col, js_key in JSON_FIELDS:
        parsed = _parse_json(row[db_col])
        if parsed is not None:
            plant[js_key] = parsed

    if vaka is not None:
        plant["ornekVaka"] = vaka_row_to_dict(vaka)

    return plant


def fetch_all_plants() -> list[dict]:
    with connect() as conn:
        plants = conn.execute(
            "SELECT * FROM bitkiler ORDER BY id"
        ).fetchall()
        vakalar = {
            row["bitki_id"]: row
            for row in conn.execute("SELECT * FROM ornek_vakalar").fetchall()
        }
    return [plant_row_to_dict(p, vakalar.get(p["id"])) for p in plants]


def fetch_plant_by_id(plant_id: int) -> dict | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM bitkiler WHERE id = ?", (plant_id,)
        ).fetchone()
        if not row:
            return None
        vaka = conn.execute(
            "SELECT * FROM ornek_vakalar WHERE bitki_id = ?", (plant_id,)
        ).fetchone()
    return plant_row_to_dict(row, vaka)


MISSING_SEARCH_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS bulunamayan_aramalar (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    arama_metni     TEXT NOT NULL,
    arama_norm      TEXT NOT NULL,
    tekrar_sayisi   INTEGER NOT NULL DEFAULT 1,
    ilk_tarih       TEXT DEFAULT (datetime('now','localtime')),
    son_tarih       TEXT DEFAULT (datetime('now','localtime'))
);
CREATE INDEX IF NOT EXISTS idx_bulunamayan_norm ON bulunamayan_aramalar(arama_norm);
"""


def ensure_missing_search_table() -> None:
    """Bulunamayan arama rafini acar (mevcut veriyi silmez)."""
    with connect() as conn:
        conn.executescript(MISSING_SEARCH_TABLE_SQL)
        conn.commit()


def save_missing_search(query: str) -> dict:
    """
    Sonuc bulunamayan aramayi kaydeder.
    Ayni kelime tekrar aranirsa tekrar_sayisi artar.
    """
    raw = (query or "").strip()
    if len(raw) < 2:
        raise ValueError("Arama metni cok kisa.")

    # Cok uzun / anlamsiz kayitlari engelle
    if len(raw) > 120:
        raw = raw[:120].strip()

    norm = raw.casefold()
    ensure_missing_search_table()

    with connect() as conn:
        existing = conn.execute(
            "SELECT id, tekrar_sayisi FROM bulunamayan_aramalar WHERE arama_norm = ?",
            (norm,),
        ).fetchone()

        if existing:
            conn.execute(
                """
                UPDATE bulunamayan_aramalar
                SET tekrar_sayisi = tekrar_sayisi + 1,
                    son_tarih = datetime('now','localtime'),
                    arama_metni = ?
                WHERE id = ?
                """,
                (raw, existing["id"]),
            )
            row_id = existing["id"]
            count = existing["tekrar_sayisi"] + 1
        else:
            cur = conn.execute(
                """
                INSERT INTO bulunamayan_aramalar (arama_metni, arama_norm)
                VALUES (?, ?)
                """,
                (raw, norm),
            )
            row_id = cur.lastrowid
            count = 1

        conn.commit()
        row = conn.execute(
            "SELECT * FROM bulunamayan_aramalar WHERE id = ?", (row_id,)
        ).fetchone()

    return {
        "id": row["id"],
        "aramaMetni": row["arama_metni"],
        "tekrarSayisi": count,
        "ilkTarih": row["ilk_tarih"],
        "sonTarih": row["son_tarih"],
    }


def list_missing_searches(limit: int = 100) -> list[dict]:
    ensure_missing_search_table()
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, arama_metni, tekrar_sayisi, ilk_tarih, son_tarih
            FROM bulunamayan_aramalar
            ORDER BY tekrar_sayisi DESC, son_tarih DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "id": r["id"],
            "aramaMetni": r["arama_metni"],
            "tekrarSayisi": r["tekrar_sayisi"],
            "ilkTarih": r["ilk_tarih"],
            "sonTarih": r["son_tarih"],
        }
        for r in rows
    ]
