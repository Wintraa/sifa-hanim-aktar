#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Site + SQLite API sunucusu.

Kullanim:
    python scripts/serve.py

Tarayici:
    http://127.0.0.1:8080

API:
    GET  /api/bitkiler
    GET  /api/bitkiler/1
    POST /api/bulunamayan-aramalar   {"arama": "xxx"}
    GET  /api/bulunamayan-aramalar
"""

from __future__ import annotations

import json
import mimetypes
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from db_api import (  # noqa: E402
    ensure_missing_search_table,
    fetch_all_plants,
    fetch_plant_by_id,
    list_missing_searches,
    save_missing_search,
)

HOST = "127.0.0.1"
PORT = 8080


class BitkiHandler(SimpleHTTPRequestHandler):
    """Statik dosyalar + API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))

    def _send_json(self, payload, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Gecersiz JSON govde.") from exc
        if not isinstance(data, dict):
            raise ValueError("JSON nesne olmali.")
        return data

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path.rstrip("/") == "/api/bulunamayan-aramalar":
            try:
                body = self._read_json_body()
                query = body.get("arama") or body.get("query") or ""
                saved = save_missing_search(str(query))
                self._send_json({"ok": True, "kayit": saved}, status=201)
            except ValueError as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=400)
            except FileNotFoundError as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=503)
            except Exception as exc:  # noqa: BLE001
                self._send_json({"ok": False, "error": str(exc)}, status=500)
            return

        self._send_json({"error": "Bilinmeyen adres"}, status=404)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/api/bitkiler":
            try:
                self._send_json(fetch_all_plants())
            except FileNotFoundError as exc:
                self._send_json({"error": str(exc)}, status=503)
            return

        if path.startswith("/api/bitkiler/"):
            part = path.rstrip("/").split("/")[-1]
            if not part.isdigit():
                self._send_json({"error": "Gecersiz bitki id"}, status=400)
                return
            try:
                plant = fetch_plant_by_id(int(part))
            except FileNotFoundError as exc:
                self._send_json({"error": str(exc)}, status=503)
                return
            if plant is None:
                self._send_json({"error": "Bitki bulunamadi"}, status=404)
                return
            self._send_json(plant)
            return

        if path.rstrip("/") == "/api/bulunamayan-aramalar":
            try:
                self._send_json(list_missing_searches())
            except FileNotFoundError as exc:
                self._send_json({"error": str(exc)}, status=503)
            return

        if path in ("", "/"):
            self.path = "/index.html"

        return super().do_GET()


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    mimetypes.add_type("application/javascript", ".js")
    mimetypes.add_type("text/css", ".css")

    try:
        ensure_missing_search_table()
        print("bulunamayan_aramalar tablosu hazir")
    except FileNotFoundError as exc:
        print(f"UYARI: {exc}")

    server = ThreadingHTTPServer((HOST, PORT), BitkiHandler)
    print("Sifa Hanim Aktar sunucusu calisiyor")
    print(f"  Site:  http://{HOST}:{PORT}/")
    print(f"  API:   http://{HOST}:{PORT}/api/bitkiler")
    print(f"  Eksik: http://{HOST}:{PORT}/eksik-aramalar.html")
    print(f"  DB:    database/bitki.db")
    print("Durdurmak icin Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
