import { SHOP } from "../config/shop.js";

const CART_KEY = "sifa_cart_v1";

/** @typedef {{ id: number, ad: string, birim: string, kategori?: string, quantity: number }} CartItem */

export function readCart() {
  try {
    const raw = localStorage.getItem(CART_KEY);
    const list = raw ? JSON.parse(raw) : [];
    if (!Array.isArray(list)) return [];
    return list
      .filter((item) => item && Number.isInteger(Number(item.id)) && String(item.ad || "").trim())
      .map((item) => ({
        id: Number(item.id),
        ad: String(item.ad).trim(),
        birim: String(item.birim || "adet").trim(),
        kategori: item.kategori ? String(item.kategori) : "",
        resimUrl: item.resimUrl ? String(item.resimUrl) : "",
        quantity: Math.max(1, Math.min(99, Number(item.quantity) || 1)),
      }));
  } catch {
    return [];
  }
}

export function writeCart(items) {
  localStorage.setItem(CART_KEY, JSON.stringify(items));
}

/** Ürünü sepete ekler veya adet artırır. */
export function addToCart(product, quantity = 1) {
  const qty = Math.max(1, Math.min(99, Number(quantity) || 1));
  const items = readCart();
  const id = Number(product.id);
  const idx = items.findIndex((item) => item.id === id);

  if (idx >= 0) {
    items[idx] = {
      ...items[idx],
      birim: String(product.birim || items[idx].birim || "adet").trim(),
      kategori: String(product.kategori || items[idx].kategori || "").trim(),
      resimUrl: product.resimUrl ? String(product.resimUrl) : items[idx].resimUrl || "",
      quantity: Math.min(99, items[idx].quantity + qty),
    };
  } else {
    items.push({
      id,
      ad: String(product.ad || "").trim(),
      birim: String(product.birim || "adet").trim(),
      kategori: String(product.kategori || "").trim(),
      resimUrl: product.resimUrl ? String(product.resimUrl) : "",
      quantity: qty,
    });
  }

  writeCart(items);
  return items;
}

export function setCartQuantity(productId, quantity) {
  const id = Number(productId);
  const items = readCart();
  const idx = items.findIndex((item) => item.id === id);
  if (idx < 0) return items;

  const qty = Number(quantity);
  if (!Number.isFinite(qty) || qty <= 0) {
    items.splice(idx, 1);
  } else {
    items[idx] = { ...items[idx], quantity: Math.min(99, Math.max(1, Math.round(qty))) };
  }

  writeCart(items);
  return items;
}

export function removeFromCart(productId) {
  const id = Number(productId);
  const items = readCart().filter((item) => item.id !== id);
  writeCart(items);
  return items;
}

export function clearCart() {
  writeCart([]);
  return [];
}

export function cartItemCount(items = readCart()) {
  return items.reduce((sum, item) => sum + item.quantity, 0);
}

export function cartLineCount(items = readCart()) {
  return items.length;
}

/** Sepetteki tüm ürünler için WhatsApp fiyat mesajı. */
export function buildCartWhatsAppMessage(items = readCart()) {
  if (!items.length) return SHOP.whatsappMessages.order;

  const lines = items.map((item, i) => {
    const unit = item.birim && item.birim !== "adet" ? ` (${item.birim})` : "";
    return `${i + 1}. ${item.ad}${unit} — ${item.quantity} adet`;
  });

  const total = cartItemCount(items);
  return [
    "Merhaba, Şifa Hanım Aktar sitesinden sepetim için toplu bilgi almak istiyorum:",
    "",
    ...lines,
    "",
    `Toplam ${items.length} çeşit, ${total} adet. Fiyat ve stok bilgisi rica ederim.`,
  ].join("\n");
}
