const express = require("express");
const path = require("path");

const router = express.Router();
const repoRoot = path.resolve(__dirname, "../..");

async function handleImageUpload(req, res) {
  try {
    const {
      parseImagePayload,
      persistProductImageLocal,
      verifyAdminKey,
    } = await import("../../lib/product-image-store.mjs");

    const adminKey = req.headers["x-admin-key"] || req.body?.adminKey;
    if (!verifyAdminKey(adminKey)) {
      return res.status(401).json({ error: "Admin yetkisi gerekli." });
    }

    const productId = Number(req.params.id || req.query.id || req.body?.id);
    if (!Number.isInteger(productId) || productId <= 0) {
      return res.status(400).json({ error: "Geçersiz ürün id." });
    }

    const buffer = parseImagePayload(req.body?.image || req.body?.imageBase64);
    const result = await persistProductImageLocal(productId, buffer, repoRoot);
    return res.json({ ok: true, ...result });
  } catch (err) {
    console.error("[product-image]", err);
    return res.status(500).json({ error: err.message || "Görsel kaydedilemedi." });
  }
}

/** POST /api/products/:id/image */
router.post("/:id/image", handleImageUpload);

/** POST /api/products/image?id= — Vercel ile aynı uç */
router.post("/image", handleImageUpload);

module.exports = router;
