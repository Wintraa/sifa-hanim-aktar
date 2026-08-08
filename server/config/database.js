/**
 * SQLite bağlantısı (Node.js yerleşik node:sqlite).
 * Mevcut database/bitki.db dosyasını kullanır.
 *
 * Not: Node 22.5+ için --experimental-sqlite bayrağı gerekebilir.
 */
const { DatabaseSync } = require("node:sqlite");
const path = require("path");
const fs = require("fs");

const DB_PATH = path.join(__dirname, "..", "..", "database", "bitki.db");

function createConnection() {
  const dir = path.dirname(DB_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const db = new DatabaseSync(DB_PATH);
  db.exec("PRAGMA journal_mode = WAL;");
  db.exec("PRAGMA foreign_keys = ON;");
  return db;
}

/** Tablolar yoksa oluşturur; varsa dokunmaz (veri silinmez). */
function initializeSchema(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS bitkiler (
      id INTEGER PRIMARY KEY,
      ad TEXT NOT NULL,
      botanik_ad TEXT NOT NULL,
      tur TEXT NOT NULL,
      resim_url TEXT,
      genel_tavsiye TEXT,
      eski_id INTEGER,
      temel_bilgiler TEXT,
      saglik_kullanim TEXT,
      cografya_mevsim TEXT,
      bakim_yetistirme TEXT,
      kaynak TEXT,
      pfaf_orijinal TEXT,
      olusturulma TEXT DEFAULT (datetime('now')),
      guncelleme TEXT DEFAULT (datetime('now'))
    );

    CREATE INDEX IF NOT EXISTS idx_bitkiler_tur ON bitkiler(tur);
    CREATE INDEX IF NOT EXISTS idx_bitkiler_ad ON bitkiler(ad);

    CREATE TABLE IF NOT EXISTS ornek_vakalar (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      bitki_id INTEGER NOT NULL UNIQUE,
      baslik TEXT,
      sorun TEXT,
      yaklasim TEXT,
      sonuc TEXT,
      anlatim TEXT,
      pubmed_id TEXT,
      pubmed_url TEXT,
      makale_basligi TEXT,
      yil TEXT,
      kaynak_adi TEXT,
      FOREIGN KEY (bitki_id) REFERENCES bitkiler(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_vakalar_bitki ON ornek_vakalar(bitki_id);

    CREATE TABLE IF NOT EXISTS bulunamayan_aramalar (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      arama_metni TEXT NOT NULL,
      arama_norm TEXT NOT NULL,
      tekrar_sayisi INTEGER NOT NULL DEFAULT 1,
      ilk_tarih TEXT DEFAULT (datetime('now','localtime')),
      son_tarih TEXT DEFAULT (datetime('now','localtime'))
    );

    CREATE INDEX IF NOT EXISTS idx_bulunamayan_norm ON bulunamayan_aramalar(arama_norm);
  `);
}

const db = createConnection();
initializeSchema(db);

module.exports = { db, DB_PATH };
