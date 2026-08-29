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

/** Kart / detay için boyutlandırılmış görsel (Vercel/Netlify CDN). */
export function plantImageUrl(path, { width = 640, quality = 75 } = {}) {
  const src = assetUrl(path);
  if (!src || import.meta.env.DEV) return src;

  const isPhoto = /\.(jpe?g|png|webp)$/i.test(src);
  if (!isPhoto) return src;

  const encoded = encodeURIComponent(src);
  const host = typeof window !== "undefined" ? window.location.hostname : "";

  if (host.includes("vercel.app") || host.includes("vercel.com")) {
    return `/_vercel/image?url=${encoded}&w=${width}&q=${quality}`;
  }
  if (host.includes("netlify.app")) {
    return `/.netlify/images?url=${encoded}&w=${width}&h=${Math.round(width * 0.75)}&fit=cover&q=${quality}`;
  }

  return src;
}
