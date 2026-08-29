/**
 * API'den gelen göreli asset yollarını (assets/...) kökten çözümler.
 */
export function assetUrl(path) {
  const value = String(path ?? "").trim();
  if (!value) return "";
  if (/^(https?:|data:|blob:)/i.test(value)) return value;
  if (value.startsWith("/")) return value;
  return `/${value}`;
}

/** Kart/detay görselleri — boşsa marka placeholder. */
export function productImageUrl(path) {
  const url = assetUrl(path);
  return url || "/assets/product-placeholder.svg";
}

/** @deprecated Bitki görselleri için; ürünlerde productImageUrl kullanın. */
export function plantImageUrl(path) {
  return assetUrl(path) || "/assets/product-placeholder.svg";
}
