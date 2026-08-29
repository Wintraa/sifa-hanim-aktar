/**
 * Ürün kategorileri — admin localStorage'da yönetir, sol menüde listelenir.
 */
const STORAGE_KEY = "sifa_product_categories_v1";

function readRaw() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function writeRaw(list) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

export function getProductCategories() {
  return readRaw()
    .filter((c) => c && Number(c.id) && String(c.ad || "").trim())
    .sort((a, b) => Number(a.sira ?? a.id) - Number(b.sira ?? b.id));
}

export function getCategoryNames() {
  return getProductCategories().map((c) => c.ad);
}

export function getNextCategoryId() {
  const list = getProductCategories();
  return list.reduce((max, c) => Math.max(max, Number(c.id) || 0), 0) + 1;
}

export function addProductCategory(ad) {
  const name = String(ad || "").trim();
  if (!name) throw new Error("Kategori adı zorunlu.");
  const list = getProductCategories();
  if (list.some((c) => c.ad.toLocaleLowerCase("tr") === name.toLocaleLowerCase("tr"))) {
    throw new Error("Bu kategori zaten var.");
  }
  const item = { id: getNextCategoryId(), ad: name, sira: list.length + 1 };
  writeRaw([...list, item]);
  return item;
}

export function updateProductCategory(id, ad) {
  const name = String(ad || "").trim();
  if (!name) throw new Error("Kategori adı zorunlu.");
  const numId = Number(id);
  const list = getProductCategories();
  const idx = list.findIndex((c) => Number(c.id) === numId);
  if (idx < 0) throw new Error("Kategori bulunamadı.");
  list[idx] = { ...list[idx], ad: name };
  writeRaw(list);
  return list[idx];
}

export function deleteProductCategory(id) {
  const numId = Number(id);
  writeRaw(getProductCategories().filter((c) => Number(c.id) !== numId));
}

/** Kategori listesi değişince dinlemek için */
export const CATEGORIES_CHANGED = "sifa-categories-changed";

export function notifyCategoriesChanged() {
  window.dispatchEvent(new CustomEvent(CATEGORIES_CHANGED));
}
