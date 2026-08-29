import { SHOP } from "../config/shop.js";

export function whatsappUrl(message = SHOP.whatsappMessages.general) {
  const text = encodeURIComponent(message);
  return `https://wa.me/${SHOP.whatsapp}?text=${text}`;
}

export function telUrl() {
  return `tel:${SHOP.phoneTel.replace(/\s/g, "")}`;
}

export function mailUrl(subject = "Şifa Hanım Aktar — Bilgi") {
  return `mailto:${SHOP.email}?subject=${encodeURIComponent(subject)}`;
}

export function mapsUrl() {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(SHOP.mapQuery || SHOP.address)}`;
}
