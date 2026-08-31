/**
 * Desktop/Aktar → assets/products (kesin dosya adı eşlemesi)
 * node scripts/import-aktar-images.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const aktarDir = path.resolve(repoRoot, "..", "Aktar");
const productsPath = path.join(repoRoot, "data", "products.json");
const outDir = path.join(repoRoot, "assets", "products");

/** id → Aktar dosya adı (tam veya benzersiz parça) */
const EXACT = {
  1: "Esila Kuyruk.jpg",
  2: "adnız.jpg",
  4: "Radian Masaj.jpg",
  5: "çörek otu.jpg",
  9: "coconut.jpeg",
  10: "coconut.jpeg",
  11: "PulBiber.jpeg",
  12: "PulBiber.jpeg",
  13: "Toz Biber.jpeg",
  14: "Toz Biber.jpeg",
  15: "İsot.jpeg",
  16: "kimyon.jpeg",
  17: "Kekik.jpeg",
  18: "Toz Tarçın.jpeg",
  19: "Kara Biber.jpeg",
  20: "Sumak.jpeg",
  21: "Çubuk Tarçın.jpeg",
  22: "Zencefil.jpeg",
  23: "Zerdeçal.jpeg",
  24: "beyaz susam.jpeg",
  25: "Kavruk Susam.jpeg",
  26: "karanfil.jpeg",
  27: "çörek otu.jpg",
  28: "Keten Tohum.jpeg",
  29: "Rezene.jpeg",
  30: "Kına.jpeg",
  31: "Kış Çay.jpeg",
  32: "Atom Çay.jpeg",
  33: "Form Çay.jpeg",
  34: "Beyaz Çay.jpeg",
  35: "Yeşil Çay.jpeg",
  36: "yeşil Çay dökme.jpeg",
  37: "Seylan Çay.jpg",
  38: "Kayısılı Biberiyeli.jpeg",
  39: "Bromelain.jpeg",
  40: "KekreMekre.jpeg",
  41: "momoridca kokonat.jpg",
  42: "detox.jpeg",
  43: "Elmalı bişey sirke.jpeg",
  44: "Aserola.jpeg",
  45: "Matcha Detox.jpeg",
  46: "Matcha Bromelain.jpeg",
  47: "Matcha Yeşil Çay.jpeg",
  48: "Dorm Diyet Kahjvesi.jpeg",
  49: "Şifa HAnım Kahve.jpeg",
  50: "Adıyaman Kervan.jpeg",
  51: "Sütlü Menengiç.jpeg",
  52: "Dolma Biber.jpeg",
  53: "Patlıcan Kuru Askı.jpeg",
  54: "Domates kuru.jpeg",
  55: "incir kuru.jpeg",
  56: "Dut Kuru.jpeg",
  57: "Hayıt Tohumlu Macun.jpeg",
  58: "Ballı Polenli Ginsengli.jpeg",
  59: "andız Pekmezli.jpeg",
  60: "Yakı Otlu Prvoit.jpeg",
  61: "45+ Performans.jpeg",
  62: "Mandalina.jpeg",
  63: "Zühre Ana Kids.jpg",
  64: "Zühre Ana Kozalak.jpg",
  65: "Propolis.jpg",
  66: "Sultan Macun.jpg",
  67: "Stevia.jpg",
  68: "Tropikal.jpg",
  69: "Zühre Ana Yaban Mersini.jpeg",
  70: "vişne.jpg",
  71: "karadut.jpg",
  72: "adnız.jpg",
  73: "hurma.jpg",
  74: "harnup.jpg",
  75: "dut.jpg",
  76: "kızılcık.jpg",
  77: "elma.jpg",
  78: "Kozalak urubu.jpeg",
  79: "Alıç Sireksi.jpeg",
  80: "ananas.jpg",
  81: "enginar.jpg",
  82: "üzüm.jpg",
  83: "Gül Sirkesi.jpeg",
  84: "Sultan.jpeg",
  85: "Çakşır.jpg",
  86: "Enginat.jpg",
};

function slugify(text) {
  return String(text)
    .toLocaleLowerCase("tr")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 52);
}

function resolveFile(wanted, files) {
  if (files.includes(wanted)) return wanted;
  const w = wanted.toLocaleLowerCase("tr");
  return files.find((f) => f.toLocaleLowerCase("tr") === w)
    || files.find((f) => norm(f) === norm(wanted))
    || files.find((f) => norm(f).includes(norm(path.parse(wanted).name)));
}

function norm(s) {
  return String(s)
    .toLocaleLowerCase("tr")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\.(jpe?g|png|webp)$/i, "")
    .replace(/[^a-z0-9+ ]/g, "")
    .trim();
}

if (!fs.existsSync(aktarDir)) {
  console.error("Aktar klasörü yok:", aktarDir);
  process.exit(1);
}

const aktarFiles = fs.readdirSync(aktarDir).filter((f) => /\.(jpe?g|png|webp)$/i.test(f));
fs.mkdirSync(outDir, { recursive: true });

const products = JSON.parse(fs.readFileSync(productsPath, "utf8"));
let ok = 0;
let fail = 0;

for (const product of products) {
  const wanted = EXACT[product.id];
  if (!wanted) {
    if (!product.resimUrl) fail++;
    continue;
  }

  const srcName = resolveFile(wanted, aktarFiles);
  if (!srcName) {
    console.warn(`? #${product.id} dosya yok: ${wanted}`);
    if (!product.resimUrl) fail++;
    continue;
  }

  const ext = path.extname(srcName).toLowerCase();
  const destName = `${String(product.id).padStart(2, "0")}-${slugify(product.ad)}${ext === ".png" ? ".png" : ".jpg"}`;
  fs.copyFileSync(path.join(aktarDir, srcName), path.join(outDir, destName));
  product.resimUrl = `assets/products/${destName}`;
  ok++;
  console.log(`✓ #${product.id} ← ${srcName}`);
}

fs.writeFileSync(productsPath, `${JSON.stringify(products, null, 2)}\n`, "utf8");
const missing = products.filter((p) => !p.resimUrl).length;
console.log(`\n${ok} görsel, eksik: ${missing}/86`);
