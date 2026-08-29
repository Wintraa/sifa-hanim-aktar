/**
 * plants.json'dan sitemap.xml üretir → client/public/sitemap.xml
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const clientRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot   = path.resolve(clientRoot, "..");
const srcJson    = path.join(repoRoot, "data", "plants.json");
const srcProducts = path.join(repoRoot, "data", "products.json");
const outFile    = path.join(clientRoot, "public", "sitemap.xml");

const rawBase =
  process.env.SITE_URL ||
  process.env.VERCEL_PROJECT_PRODUCTION_URL ||
  process.env.VERCEL_URL ||
  "https://sifahanimaktar.vercel.app";
const BASE = rawBase.startsWith("http") ? rawBase.replace(/\/$/, "") : `https://${rawBase.replace(/\/$/, "")}`;
const TODAY = new Date().toISOString().slice(0, 10);

const plants = JSON.parse(fs.readFileSync(srcJson, "utf-8"));
const products = fs.existsSync(srcProducts)
  ? JSON.parse(fs.readFileSync(srcProducts, "utf-8"))
  : [];

const staticUrls = [
  { loc: `${BASE}/`, changefreq: "daily", priority: "1.0" },
  { loc: `${BASE}/bitkiler`, changefreq: "weekly", priority: "0.9" },
  { loc: `${BASE}/iletisim`, changefreq: "monthly", priority: "0.7" },
  { loc: `${BASE}/giris`, changefreq: "monthly", priority: "0.3" },
  { loc: `${BASE}/kayit`, changefreq: "monthly", priority: "0.5" },
  { loc: `${BASE}/profil`, changefreq: "monthly", priority: "0.4" },
  { loc: `${BASE}/ayarlar`, changefreq: "monthly", priority: "0.3" },
];

const plantUrls = plants.map((p) => ({
  loc: `${BASE}/bitki/${p.id}`,
  changefreq: "monthly",
  priority: "0.8",
}));

const productUrls = products.map((p) => ({
  loc: `${BASE}/urun/${p.id}`,
  changefreq: "weekly",
  priority: "0.85",
}));

const all = [...staticUrls, ...productUrls, ...plantUrls];

const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...all.map(
    (u) =>
      `  <url>\n    <loc>${u.loc}</loc>\n    <lastmod>${TODAY}</lastmod>\n    <changefreq>${u.changefreq}</changefreq>\n    <priority>${u.priority}</priority>\n  </url>`
  ),
  "</urlset>",
].join("\n");

fs.writeFileSync(outFile, xml, "utf-8");

const robotsFile = path.join(clientRoot, "public", "robots.txt");
fs.writeFileSync(
  robotsFile,
  `User-agent: *\nAllow: /\n\nSitemap: ${BASE}/sitemap.xml\n`,
  "utf-8"
);

console.log(`sitemap yazıldı: ${outFile} (${all.length} URL) base=${BASE}`);
