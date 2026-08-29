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

/** Kart/detay görselleri — dosyalar build öncesi sıkıştırılıyor, direkt URL kullan. */
export function plantImageUrl(path) {
  return assetUrl(path);
}
