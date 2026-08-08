-- SQLite schema
PRAGMA foreign_keys = ON;

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
    guncellema TEXT DEFAULT (datetime('now'))
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
