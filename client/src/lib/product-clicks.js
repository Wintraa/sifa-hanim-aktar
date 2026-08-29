/**
 * Ürün tıklama sayıları — ana sayfada «Çok tıklananlar» bandı için (öne çıkan değil).
 */
const STORAGE_KEY = "sifa_product_clicks_v1";
export const CLICKS_CHANGED = "sifa-product-clicks-changed";
const DEFAULT_VITRIN_LIMIT = 6;

function readCounts() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function writeCounts(counts) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(counts));
}

/** Ürün kartı veya detay sayfası tıklanınca sayacı artır. */
export function recordProductClick(productId) {
  const id = Number(productId);
  if (!Number.isInteger(id) || id <= 0) return;
  const counts = readCounts();
  counts[id] = (counts[id] || 0) + 1;
  writeCounts(counts);
  window.dispatchEvent(new CustomEvent(CLICKS_CHANGED, { detail: { id } }));
}

export function getProductClickCount(productId) {
  return readCounts()[Number(productId)] || 0;
}

/** En çok tıklanan ürünleri sıralı döndürür (en az 1 tıklama gerekir). */
export function getTopClickedProducts(products, limit = DEFAULT_VITRIN_LIMIT) {
  const counts = readCounts();
  return [...products]
    .filter((p) => (counts[Number(p.id)] || 0) > 0)
    .sort((a, b) => (counts[Number(b.id)] || 0) - (counts[Number(a.id)] || 0))
    .slice(0, limit);
}

export function isInVitrin(productId, products, limit = DEFAULT_VITRIN_LIMIT) {
  const topIds = new Set(getTopClickedProducts(products, limit).map((p) => Number(p.id)));
  return topIds.has(Number(productId));
}

export { DEFAULT_VITRIN_LIMIT };
