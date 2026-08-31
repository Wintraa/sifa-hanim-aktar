/**
 * Ürün görsellerini doldurur — önce yerel bitki fotoğrafı, sonra Wikimedia.
 * node scripts/apply-product-images.mjs
 * node scripts/apply-product-images.mjs --only-missing
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { IMAGE_MAP } from "./product-image-map.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const productsPath = path.join(repoRoot, "data", "products.json");
const productsOutDir = path.join(repoRoot, "assets", "products");
const onlyMissing = process.argv.includes("--only-missing");

const CATEGORY_FALLBACK = {
  "Ağrı Kremi": "assets/plants/photos/20-althaea-officinalis.jpg",
  "Aromatik Yağlar": "assets/plants/photos/211-simmondsia-chinensis.jpg",
  Baharatlar: "assets/plants/photos/42-cardamom.jpg",
  Çay: "assets/plants/photos/96-camellia-sinensis.jpg",
  "Detox Ürünleri": "assets/plants/photos/205-citrus-limon.jpg",
  Kahve: "assets/plants/photos/230-paullinia-cupana.jpg",
  "Kurutulmuş Ürünler": "assets/plants/photos/165-ficus-carica.jpg",
  Macunlar: "assets/plants/photos/69-panax-ginseng.jpg",
  "Meyve Özü": "assets/plants/photos/166-punica-granatum.jpg",
  Sirkeler: "assets/plants/photos/205-citrus-limon.jpg",
};

function slugify(text) {
  return String(text)
    .toLocaleLowerCase("tr")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 48);
}

function fileExists(relPath) {
  return fs.existsSync(path.join(repoRoot, relPath.replace(/^\//, "")));
}

async function fetchWikimediaUrl(search, retries = 3) {
  for (let attempt = 0; attempt < retries; attempt++) {
    const params = new URLSearchParams({
      action: "query",
      generator: "search",
      gsrsearch: search,
      gsrlimit: "5",
      gsrnamespace: "6",
      prop: "imageinfo",
      iiprop: "url",
      iiurlwidth: "900",
      format: "json",
      origin: "*",
    });
    const res = await fetch(`https://commons.wikimedia.org/w/api.php?${params}`, {
      headers: { "User-Agent": "SifaHanimAktar/1.0 (educational product catalog)" },
    });
    if (res.status === 429) {
      await sleep(2000 * (attempt + 1));
      continue;
    }
    if (!res.ok) return null;
    const data = await res.json();
    const pages = data?.query?.pages;
    if (!pages) return null;
    for (const page of Object.values(pages)) {
      const info = page?.imageinfo?.[0];
      const url = info?.thumburl || info?.url;
      if (url && /\.(jpe?g|png|webp)(\?|$)/i.test(url)) return url;
    }
    return null;
  }
  return null;
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function downloadUrl(url, destFile) {
  const res = await fetch(url, {
    headers: { "User-Agent": "SifaHanimAktar/1.0" },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.length < 800) throw new Error("too small");
  fs.writeFileSync(destFile, buf);
}

function copyLocal(relPath, destFile) {
  fs.copyFileSync(path.join(repoRoot, relPath), destFile);
}

fs.mkdirSync(productsOutDir, { recursive: true });

const products = JSON.parse(fs.readFileSync(productsPath, "utf8"));
let localOk = 0;
let wikiOk = 0;
let catOk = 0;

for (const product of products) {
  const map = IMAGE_MAP[product.id];
  if (!map) continue;
  if (onlyMissing && product.resimUrl) continue;

  const fileName = `${String(product.id).padStart(2, "0")}-${slugify(product.ad)}.jpg`;
  const relOut = `assets/products/${fileName}`;
  const absOut = path.join(productsOutDir, fileName);

  let done = false;

  // 1) Yerel bitki fotoğrafı — en güvenilir
  if (map.fallbackPath && fileExists(map.fallbackPath)) {
    copyLocal(map.fallbackPath, absOut);
    product.resimUrl = relOut;
    localOk++;
    done = true;
    console.log(`local #${product.id} ${product.ad}`);
    continue;
  }

  // 2) Wikimedia
  if (!done && map.search) {
    await sleep(900);
    const url = await fetchWikimediaUrl(map.search);
    if (url) {
      try {
        await downloadUrl(url, absOut);
        product.resimUrl = relOut;
        wikiOk++;
        done = true;
        console.log(`wiki  #${product.id} ${product.ad}`);
      } catch (err) {
        console.warn(`wiki dl #${product.id}: ${err.message}`);
      }
    }
  }

  // 3) Kategori yedek
  if (!done) {
    const catFb = CATEGORY_FALLBACK[product.kategori];
    if (catFb && fileExists(catFb)) {
      copyLocal(catFb, absOut);
      product.resimUrl = relOut;
      catOk++;
      console.log(`cat   #${product.id} ${product.ad}`);
    } else {
      console.warn(`skip  #${product.id} ${product.ad}`);
    }
  }
}

fs.writeFileSync(productsPath, `${JSON.stringify(products, null, 2)}\n`, "utf8");
const missing = products.filter((p) => !p.resimUrl).length;
console.log(`\nlocal=${localOk} wiki=${wikiOk} cat=${catOk} missing=${missing}/86`);
