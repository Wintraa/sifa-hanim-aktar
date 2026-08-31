/** Admin görsel yükleme API anahtarı (Vercel'de ADMIN_API_KEY ile aynı olmalı). */
function adminApiKey() {
  return import.meta.env.VITE_ADMIN_API_KEY || "99161202";
}

/**
 * Düzenlenen görseli kalıcı kaydet: assets/products + data/products.json
 * Local: Express diske yazar. Canlı: GitHub commit (deploy sonrası herkes görür).
 */
export async function uploadProductImagePermanent(productId, imageDataUrl) {
  const id = Number(productId);
  if (!Number.isInteger(id) || id <= 0) {
    throw new Error("Geçersiz ürün id.");
  }

  const response = await fetch(`/api/products/image?id=${id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-Admin-Key": adminApiKey(),
    },
    body: JSON.stringify({ id, image: imageDataUrl }),
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || data.hint || "Görsel sunucuya kaydedilemedi.");
  }
  return data;
}
