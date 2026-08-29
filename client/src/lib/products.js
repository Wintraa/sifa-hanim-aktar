/**
 * Ürün verisi + admin düzenlemeleri (localStorage birleşimi).
 */
const OVERRIDES_KEY = "sifa_product_overrides_v1";
const DELETED_KEY = "sifa_product_deleted_v1";
const PRODUCTS_CACHE_KEY = "sifa-products-v1";

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

export function mergeProducts(baseList) {
  const overrides = readProductOverrides();
  const deleted = new Set(readDeletedProductIds());
  const byId = new Map();

  for (const item of baseList) {
    if (!isValidProduct(item) || deleted.has(Number(item.id))) continue;
    byId.set(Number(item.id), { ...item, ...(overrides[item.id] || {}) });
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
    fiyat: "",
    birim: "adet",
    kategori: "Genel",
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
  overrides[id] = { ...product, id };
  localStorage.setItem(OVERRIDES_KEY, JSON.stringify(overrides));
  try {
    sessionStorage.removeItem(PRODUCTS_CACHE_KEY);
  } catch {
    /* ignore */
  }
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
