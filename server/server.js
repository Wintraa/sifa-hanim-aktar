/**
 * Şifa Hanım Aktar — Express API sunucusu
 * SQLite: ../../database/bitki.db
 */
const express = require("express");
const cors = require("cors");
const path = require("path");

const { DB_PATH } = require("./config/database");
const plantsRouter = require("./routes/plants");
const missingSearchesRouter = require("./routes/missingSearches");
const productImagesRouter = require("./routes/productImages");

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json({ limit: "12mb" }));

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, db: path.basename(DB_PATH) });
});

app.use("/api/bitkiler", plantsRouter);
app.use("/api/plants", plantsRouter); // İngilizce alias
app.use("/api/bulunamayan-aramalar", missingSearchesRouter);
app.use("/api/missing-searches", missingSearchesRouter);
app.use("/api/products", productImagesRouter);

app.use((err, _req, res, _next) => {
  console.error("Unhandled:", err);
  res.status(500).json({ error: "Sunucu hatası." });
});

app.listen(PORT, () => {
  console.log(`API çalışıyor → http://127.0.0.1:${PORT}`);
  console.log(`SQLite      → ${DB_PATH}`);
  console.log(`GET  /api/bitkiler`);
  console.log(`GET  /api/bitkiler/:id`);
  console.log(`GET  /api/bulunamayan-aramalar`);
  console.log(`POST /api/bulunamayan-aramalar  { "arama": "..." }`);
  console.log(`POST /api/products/:id/image  (kalıcı ürün görseli)`);
});
