/**
 * API'den gelen göreli asset yollarını (assets/...) kökten çözümler.
 * /bitki/1 gibi alt rotalarda kırılmayı önler.
 */
export function assetUrl(path) {
  const value = String(path ?? "").trim();
  if (!value) return "";
  if (/^(https?:|data:|blob:)/i.test(value)) return value;
  if (value.startsWith("/")) return value;
  return `/${value}`;
}
