/**
 * Vercel serverless: bulunamayan arama kaydı.
 * Kalıcı depo yoksa en azından 200 döner; istemci localStorage'a da yazar.
 * Loglar Vercel Function loglarında görünür.
 */
export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const arama = String(req.body?.arama || "").trim();
  if (arama.length < 2) {
    return res.status(400).json({ error: "Geçersiz arama" });
  }

  console.log("[missing-search]", JSON.stringify({ arama, at: new Date().toISOString() }));
  return res.status(200).json({ ok: true });
}
