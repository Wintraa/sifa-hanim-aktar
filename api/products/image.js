/**
 * Vercel: POST /api/products/image?id=42
 * Kalıcı görsel — GitHub'a yazar, deploy sonrası herkes görür.
 */
import {
  parseImagePayload,
  persistProductImageGitHub,
  verifyAdminKey,
} from "../../lib/product-image-store.mjs";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-Admin-Key");

  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const adminKey = req.headers["x-admin-key"] || req.body?.adminKey;
  if (!verifyAdminKey(adminKey)) {
    return res.status(401).json({ error: "Admin yetkisi gerekli." });
  }

  const productId = Number(req.query?.id || req.body?.id);
  if (!Number.isInteger(productId) || productId <= 0) {
    return res.status(400).json({ error: "Geçersiz ürün id." });
  }

  try {
    const buffer = parseImagePayload(req.body?.image || req.body?.imageBase64);
    const result = await persistProductImageGitHub(productId, buffer);
    return res.status(200).json({ ok: true, ...result });
  } catch (err) {
    console.error("[product-image]", err);
    return res.status(500).json({
      error: err.message || "Görsel kaydedilemedi.",
      hint: "Vercel'de GITHUB_TOKEN ve GITHUB_REPO ortam değişkenlerini ayarlayın.",
    });
  }
}

export const config = {
  api: {
    bodyParser: {
      sizeLimit: "12mb",
    },
  },
};
