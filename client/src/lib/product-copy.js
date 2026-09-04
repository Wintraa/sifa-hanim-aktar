/** Vitrin için ikna odaklı kısa metin ve rozet mantığı — ürün verisini bozmaz. */

const CATEGORY_HOOKS = {
  "Ağrı Kremi": "Rahatlama hissi için günlük rutine ekle — doğal destek, güçlü etki.",
  Baharat: "Mutfağını zenginleştir; aroma ve lezzet bir adım önde.",
  Çay: "Her yudumda dinginlik — taze demlik, gerçek aktar kalitesi.",
  Macun: "Geleneksel tarif, modern özen — sofrana güç kat.",
  Sirke: "Doğal ferahlık ve lezzet dengesi — mutfak vazgeçilmezi.",
  Yağ: "Saf dokunuş; bakım ve lezzette premium seçim.",
  Bal: "Doğanın kendi tatlısı — enerji ve keyif bir arada.",
};

/**
 * @param {{ id?: number, oneCikan?: boolean, stokta?: boolean }} product
 * @param {boolean} inVitrin
 * @returns {{ label: string, tone: string }[]}
 */
export function productBadges(product, inVitrin = false) {
  const badges = [];
  if (product.stokta === false) {
    badges.push({ label: "Tükendi", tone: "muted" });
    return badges;
  }
  if (product.oneCikan) badges.push({ label: "Özel Seri", tone: "special" });
  if (inVitrin && !product.oneCikan) badges.push({ label: "Çok Satan", tone: "hot" });
  const id = Number(product.id) || 0;
  if (id % 5 === 0) badges.push({ label: "Fırsat Ürünü", tone: "deal" });
  else if (id % 11 === 0) badges.push({ label: "Sınırlı Stok", tone: "limited" });
  return badges.slice(0, 2);
}

/** Fayda odaklı kısa açıklama — reklam dili. */
export function productTeaser(product) {
  const raw = String(product.kisaAciklama || "")
    .replace(/\s*—\s*Şifa Hanım Aktar\.?\s*$/i, "")
    .trim();
  const kat = String(product.kategori || "").trim();
  const hook = CATEGORY_HOOKS[kat];
  if (raw && raw.length > 12 && !/^Şifa Hanım/i.test(raw)) {
    return raw.length > 96 ? `${raw.slice(0, 93).trim()}…` : raw;
  }
  if (hook) return hook;
  return `${product.ad} — aktar tezgâhından seçilmiş, WhatsApp ile anında fiyat ve stok.`;
}
