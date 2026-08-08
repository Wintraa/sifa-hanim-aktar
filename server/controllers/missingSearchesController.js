const { db } = require("../config/database");

function listMissingSearches(_req, res) {
  try {
    const rows = db
      .prepare(
        `
        SELECT id, arama_metni, tekrar_sayisi, ilk_tarih, son_tarih
        FROM bulunamayan_aramalar
        ORDER BY tekrar_sayisi DESC, son_tarih DESC
        LIMIT 100
      `
      )
      .all();

    res.json(
      rows.map((r) => ({
        id: r.id,
        aramaMetni: r.arama_metni,
        tekrarSayisi: r.tekrar_sayisi,
        ilkTarih: r.ilk_tarih,
        sonTarih: r.son_tarih,
      }))
    );
  } catch (error) {
    console.error("listMissingSearches:", error);
    res.status(500).json({ error: "Liste alınamadı." });
  }
}

function createMissingSearch(req, res) {
  try {
    let raw = String(req.body?.arama || req.body?.query || "").trim();
    if (raw.length < 2) {
      return res.status(400).json({ error: "Arama metni çok kısa." });
    }
    if (raw.length > 120) {
      raw = raw.slice(0, 120).trim();
    }

    const norm = raw.toLocaleLowerCase("tr-TR");
    const existing = db
      .prepare("SELECT id, tekrar_sayisi FROM bulunamayan_aramalar WHERE arama_norm = ?")
      .get(norm);

    let id;
    let tekrarSayisi;

    if (existing) {
      db.prepare(
        `
        UPDATE bulunamayan_aramalar
        SET tekrar_sayisi = tekrar_sayisi + 1,
            son_tarih = datetime('now','localtime'),
            arama_metni = ?
        WHERE id = ?
      `
      ).run(raw, existing.id);
      id = existing.id;
      tekrarSayisi = existing.tekrar_sayisi + 1;
    } else {
      const result = db
        .prepare(
          `
          INSERT INTO bulunamayan_aramalar (arama_metni, arama_norm)
          VALUES (?, ?)
        `
        )
        .run(raw, norm);
      id = Number(result.lastInsertRowid);
      tekrarSayisi = 1;
    }

    const row = db
      .prepare("SELECT * FROM bulunamayan_aramalar WHERE id = ?")
      .get(id);

    res.status(201).json({
      ok: true,
      kayit: {
        id: row.id,
        aramaMetni: row.arama_metni,
        tekrarSayisi,
        ilkTarih: row.ilk_tarih,
        sonTarih: row.son_tarih,
      },
    });
  } catch (error) {
    console.error("createMissingSearch:", error);
    res.status(500).json({ error: "Kayıt eklenemedi." });
  }
}

module.exports = { listMissingSearches, createMissingSearch };
