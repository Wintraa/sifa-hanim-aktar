/**
 * Clipboard ürün listesini data/products.json + data/product-categories.json üretir.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const ROWS = `
Esila Kuyruk Yağlı Krem	Ağrı Kremi
Ardıç Özlü Krem	Ağrı Kremi
Akıllı Krem	Ağrı Kremi
Radian Masaj Kremi	Ağrı Kremi
Çörek Otu Yağı	Aromatik Yağlar
Kantaron Yağı	Aromatik Yağlar
Udi Hindi Yağı	Aromatik Yağlar
Hint Yağı	Aromatik Yağlar
Hindistan Cevizi Yağı 150ml (Organik Sertifikalı)	Aromatik Yağlar
Hindistan Cevizi Yağı 150ml	Aromatik Yağlar
Pul Biber Acı Dökme	Baharatlar
Pul Biber Tatlı Dökme	Baharatlar
Toz Biber Acı Dökme	Baharatlar
Toz Biber Tatlı Dökme	Baharatlar
İsot Dökme	Baharatlar
Kimyon Dökme	Baharatlar
Kekik Dökme	Baharatlar
Tarçın Dökme	Baharatlar
Kara Biber Dökme	Baharatlar
Sumak Dökme	Baharatlar
Çubuk Tarçın Dökme	Baharatlar
Zencefil Toz Dökme	Baharatlar
Zerdeçal Toz Dökme	Baharatlar
Beyaz Susam Dökme	Baharatlar
Simitlik Susam Dökme	Baharatlar
Karanfil Dökme	Baharatlar
Çörek Otu Dökme	Baharatlar
Keten Tohumu Dökme	Baharatlar
Rezene Dökme	Baharatlar
Kına Dökme	Baharatlar
Kış Çayı 200gr	Çay
Atom Çayı 150gr	Çay
Form Çayı 130gr	Çay
Beyaz Çay Demlik Poşet 20'Li	Çay
Yeşil Çay Demlik Poşet 20'Li	Çay
Yeşil Çay Dökme	Çay
Seylan Çayı	Çay
Esila Kayısılı Biberiyeli Karışık Bitkisel Çay	Çay
Zühre Ana Bromelain Şurubu	Detox Ürünleri
Zühre Ana Kekre Termojenik Mix	Detox Ürünleri
Momordica Coconut Mix	Detox Ürünleri
Lokman Aktar Detox Sirkesi	Detox Ürünleri
Sandaloz Sakızlı Elma Sirkesi	Detox Ürünleri
Aserola Extract	Detox Ürünleri
Matcha Detox Sade	Detox Ürünleri
Matcha Bromelain	Detox Ürünleri
Matcha Çilekli	Detox Ürünleri
Hindibalı Diyet Kahvesi	Detox Ürünleri
Şifa Hanım Türk Kahvesi	Kahve
Adıyaman Kervansaray Dibek Kahvesi 200gr	Kahve
Adıyaman Kervansaray Menengiç Kahvesi 200gr	Kahve
Dolmalık Biber Kurusu (50'Lik Dizi)	Kurutulmuş Ürünler
Dolmalık Kuru Patlıcan (50'Li Dizi)	Kurutulmuş Ürünler
Kuru Domates	Kurutulmuş Ürünler
Kuru İncir	Kurutulmuş Ürünler
Dut Kurusu	Kurutulmuş Ürünler
Civan Perçemli Hayıt Tohumlu Bitkisel Karışımlı Macun	Macunlar
Ballı Polenli Ginsengli Bitkisel Karışımlı Macun	Macunlar
Andız Pekmezli Enginarlı Zerdeçallı Bitkisel Karışımlı Macun	Macunlar
Yakı Otlu Provit Bitkisel Karışımlı Macun	Macunlar
45+ Performans Enerji Güç	Macunlar
Bodrum Mandalina Macunu	Macunlar
Zühre Ana Kids Macunu	Macunlar
Zühre Ana Kozalak Macunu	Macunlar
Zühre Ana Propolis Macunu	Macunlar
Zühre Ana Sultan Macunu	Macunlar
Zühre Ana Stevia Katkılı Kozolak Macunu	Macunlar
Zühre Ana Tropikal Meyve Özü	Meyve Özü
Zühre Ana Yaban Mersini Özü	Meyve Özü
Zühre Ana Vişne Özü	Meyve Özü
Zühre Ana Karadut Özü	Meyve Özü
Andız Pekmez Özü	Meyve Özü
Hurma Pekmez Özü	Meyve Özü
Harnup (Keçi Boynuzu Özü)	Meyve Özü
Dut Pekmez Özü	Meyve Özü
Mesir-i Şifa Kızılcık Özü	Meyve Özü
Elma Sirkesi	Sirkeler
Kozalak Şurubu	Sirkeler
Alıç Sirkesi	Sirkeler
Ananas Sirkesi	Sirkeler
Enginar Sirkesi	Sirkeler
Üzüm Sirkesi	Sirkeler
Gül Sirkesi	Sirkeler
Şifa Hanım Sultan Sirkesi	Sirkeler
Çakşır Kökü Suyu	Sirkeler
Enginar Suyu	Sirkeler
`.trim();

const CATEGORY_ORDER = [
  "Ağrı Kremi",
  "Aromatik Yağlar",
  "Baharatlar",
  "Çay",
  "Detox Ürünleri",
  "Kahve",
  "Kurutulmuş Ürünler",
  "Macunlar",
  "Meyve Özü",
  "Sirkeler",
];

const parsed = ROWS.split("\n")
  .map((line) => line.trim())
  .filter(Boolean)
  .map((line) => {
    const tab = line.lastIndexOf("\t");
    if (tab === -1) {
      const parts = line.split(/\t+/);
      return { ad: parts[0]?.trim(), kategori: parts[1]?.trim() };
    }
    return {
      ad: line.slice(0, tab).trim().replace(/\s+/g, " "),
      kategori: line.slice(tab + 1).trim(),
    };
  });

// Tab yoksa ad/kategori ayır (clipboard bazen boşlukla gelir)
const items = parsed.every((p) => p.ad && p.kategori)
  ? parsed
  : ROWS.split("\n")
      .map((l) => l.trim())
      .filter(Boolean)
      .map((line) => {
        const m = line.match(/^(.+?)\s{2,}(.+)$/);
        if (m) return { ad: m[1].trim(), kategori: m[2].trim() };
        const tabIdx = line.indexOf("\t");
        if (tabIdx > -1) {
          return { ad: line.slice(0, tabIdx).trim(), kategori: line.slice(tabIdx + 1).trim() };
        }
        return null;
      })
      .filter(Boolean);

if (!items.length) {
  throw new Error("Ürün satırı parse edilemedi.");
}

const products = items.map((item, index) => ({
  id: index + 1,
  ad: item.ad,
  kisaAciklama: `${item.kategori} — Şifa Hanım Aktar.`,
  aciklama: "",
  birim: "adet",
  kategori: item.kategori,
  resimUrl: "",
  oneCikan: false,
  stokta: true,
  etiketler: [],
}));

const categorySet = new Set(products.map((p) => p.kategori));
const categories = CATEGORY_ORDER.filter((c) => categorySet.has(c))
  .concat([...categorySet].filter((c) => !CATEGORY_ORDER.includes(c)).sort())
  .map((ad, i) => ({ id: i + 1, ad, sira: i + 1 }));

fs.writeFileSync(path.join(repoRoot, "data", "products.json"), JSON.stringify(products, null, 2) + "\n", "utf8");
fs.writeFileSync(
  path.join(repoRoot, "data", "product-categories.json"),
  JSON.stringify(categories, null, 2) + "\n",
  "utf8"
);

console.log(`Yazıldı: ${products.length} ürün, ${categories.length} kategori`);
