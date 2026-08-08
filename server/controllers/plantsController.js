const { db } = require("../config/database");
const { mapPlant } = require("../db/mappers");

function getAllPlants(_req, res) {
  try {
    const plants = db.prepare("SELECT * FROM bitkiler ORDER BY id").all();
    const vakalar = db.prepare("SELECT * FROM ornek_vakalar").all();
    const byPlantId = new Map(vakalar.map((v) => [v.bitki_id, v]));

    const payload = plants.map((p) => mapPlant(p, byPlantId.get(p.id) || null));
    res.json(payload);
  } catch (error) {
    console.error("getAllPlants:", error);
    res.status(500).json({ error: "Bitkiler yüklenemedi." });
  }
}

function getPlantById(req, res) {
  try {
    const id = Number(req.params.id);
    if (!Number.isInteger(id) || id <= 0) {
      return res.status(400).json({ error: "Geçersiz bitki id." });
    }

    const plant = db.prepare("SELECT * FROM bitkiler WHERE id = ?").get(id);
    if (!plant) {
      return res.status(404).json({ error: "Bitki bulunamadı." });
    }

    const vaka = db
      .prepare("SELECT * FROM ornek_vakalar WHERE bitki_id = ?")
      .get(id);

    res.json(mapPlant(plant, vaka || null));
  } catch (error) {
    console.error("getPlantById:", error);
    res.status(500).json({ error: "Bitki yüklenemedi." });
  }
}

module.exports = { getAllPlants, getPlantById };
