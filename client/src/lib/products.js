/**
 * Ürün verisi + admin düzenlemeleri (localStorage birleşimi).
 */
import { getCategoryNames } from "./product-categories.js";

const OVERRIDES_KEY = "sifa_product_overrides_v1";
const DELETED_KEY = "sifa_product_deleted_v1";
const PRODUCTS_CACHE_KEY = "sifa-products-v5";
const PURGE_FLAG = "sifa_demo_catalog_purged_v1";
const IMAGE_SYNC_FLAG = "sifa_catalog_images_synced_v1";
/** Admin görsel kaydedince tüm sayfalar dinler. */
export const PRODUCTS_CHANGED = "sifa-products-changed";

export function notifyProductsChanged() {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new Event(PRODUCTS_CHANGED));
  }
}
/** Eski demo vitrin (Papatya, Ihlamur vb.) — artık gösterilmez. */
const LEGACY_DEMO_IDS = new Set(Array.from({ length: 24 }, (_, i) => i + 1));

/** Admin'in tarayıcıya yüklediği görsel (data/blob). Katalog yolunu ezmesin. */
function isUserUploadedImage(url) {
  return /^(data:|blob:)/i.test(String(url || "").trim());
}

const isValidProduct = (p) =>
  p &&
  Number.isInteger(Number(p.id)) &&
  String(p.ad || "").trim();

export function readProductOverrides() {
  try {
    const raw = localStorage.getItem(OVERRIDES_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

export function readDeletedProductIds() {
  try {
    const raw = localStorage.getItem(DELETED_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list.map(Number) : [];
  } catch {
    return [];
  }
}

/** Tarayıcıda kalan eski demo ürünleri (id 1–24) bir kez temizler. */
export function purgeLegacyDemoProducts() {
  if (localStorage.getItem(PURGE_FLAG)) return;

  const overrides = readProductOverrides();
  let changed = false;
  for (const id of LEGACY_DEMO_IDS) {
    if (overrides[id]) {
      delete overrides[id];
      changed = true;
    }
  }
  if (changed) {
    localStorage.setItem(OVERRIDES_KEY, JSON.stringify(overrides));
  }

  try {
    sessionStorage.removeItem(PRODUCTS_CACHE_KEY);
    sessionStorage.removeItem("sifa-products-v2");
    sessionStorage.removeItem("sifa-products-v1");
  } catch {
    /* ignore */
  }

  localStorage.setItem(PURGE_FLAG, "1");
}

/**
 * Admin kaydı eski placeholder / bitki SVG / boş yolu tutuyorsa
 * katalog (Aktar) fotoğraflarını ezer. Bir kez temizle.
 */
export function syncCatalogImagesOverStaleOverrides() {
  if (localStorage.getItem(IMAGE_SYNC_FLAG)) return;

  const overrides = readProductOverrides();
  let changed = false;
  for (const [id, patch] of Object.entries(overrides)) {
    if (!patch || typeof patch !== "object") continue;
    if (isUserUploadedImage(patch.resimUrl)) continue;
    if ("resimUrl" in patch) {
      delete patch.resimUrl;
      overrides[id] = patch;
      changed = true;
    }
  }
  if (changed) {
    localStorage.setItem(OVERRIDES_KEY, JSON.stringify(overrides));
  }

  try {
    sessionStorage.removeItem(PRODUCTS_CACHE_KEY);
    sessionStorage.removeItem("sifa-products-v4");
    sessionStorage.removeItem("sifa-products-v3");
    sessionStorage.removeItem("sifa-products-v2");
    sessionStorage.removeItem("sifa-products-v1");
  } catch {
    /* ignore */
  }

  localStorage.setItem(IMAGE_SYNC_FLAG, "1");
}

/** Admin panelinde "Öne çıkan" işaretli ürünler. */
export function getFeaturedProducts(products) {
  return products.filter((p) => Boolean(p.oneCikan));
}

export function mergeProducts(baseList) {
  const overrides = readProductOverrides();
  const deleted = new Set(readDeletedProductIds());
  const byId = new Map();

  for (const item of baseList) {
    if (!isValidProduct(item) || deleted.has(Number(item.id))) continue;
    const patch = overrides[item.id] || overrides[String(item.id)];
    const next = { ...item, ...(patch || {}), id: Number(item.id) };
    // Admin override görseli her zaman katalog fotosunun önüne geçer.
    if (patch?.resimUrl) {
      next.resimUrl = patch.resimUrl;
    } else if (item.resimUrl) {
      next.resimUrl = item.resimUrl;
    }
    byId.set(Number(item.id), next);
  }

  for (const [id, patch] of Object.entries(overrides)) {
    const numId = Number(id);
    if (deleted.has(numId) || byId.has(numId) || !patch?.ad) continue;
    byId.set(numId, { ...patch, id: numId });
  }

  return [...byId.values()].sort((a, b) => Number(a.id) - Number(b.id));
}

/** Admin yeni ürün eklerken kullanılacak sıradaki id. */
export function getNextProductId(baseList = []) {
  const merged = mergeProducts(baseList);
  const maxId = merged.reduce((max, p) => Math.max(max, Number(p.id) || 0), 0);
  return maxId + 1;
}

export function createEmptyProduct(baseList = []) {
  return {
    id: getNextProductId(baseList),
    ad: "",
    kisaAciklama: "",
    aciklama: "",
    birim: "adet",
    kategori: getCategoryNames()[0] || "",
    resimUrl: "",
    oneCikan: false,
    stokta: true,
    etiketler: [],
  };
}

export function saveProductOverride(product) {
  const id = Number(product.id);
  if (!id || !String(product.ad || "").trim()) {
    throw new Error("Ürün adı zorunlu.");
  }
  const overrides = readProductOverrides();
  const prev = overrides[id] || overrides[String(id)] || {};
  overrides[id] = { ...prev, ...product, id };
  localStorage.setItem(OVERRIDES_KEY, JSON.stringify(overrides));
  try {
    sessionStorage.removeItem(PRODUCTS_CACHE_KEY);
  } catch {
    /* ignore */
  }
  notifyProductsChanged();
}

/** Sadece görsel güncelle — vitrin + detay aynı anda senkron kalır. */
export function saveProductImageOverride(product, resimUrl) {
  const id = Number(product.id);
  if (!id) throw new Error("Ürün id geçersiz.");
  const overrides = readProductOverrides();
  const prev = overrides[id] || overrides[String(id)] || {};
  overrides[id] = { ...product, ...prev, id, resimUrl: String(resimUrl || "").trim() };
  localStorage.setItem(OVERRIDES_KEY, JSON.stringify(overrides));
  try {
    sessionStorage.removeItem(PRODUCTS_CACHE_KEY);
  } catch {
    /* ignore */
  }
  notifyProductsChanged();
  return overrides[id];
}

export function deleteProductOverride(id) {
  const numId = Number(id);
  const deleted = readDeletedProductIds();
  if (!deleted.includes(numId)) {
    deleted.push(numId);
    localStorage.setItem(DELETED_KEY, JSON.stringify(deleted));
  }
  const overrides = readProductOverrides();
  delete overrides[numId];
  localStorage.setItem(OVERRIDES_KEY, JSON.stringify(overrides));
  try {
    sessionStorage.removeItem(PRODUCTS_CACHE_KEY);
  } catch {
    /* ignore */
  }
}

export { PRODUCTS_CACHE_KEY, isValidProduct };
