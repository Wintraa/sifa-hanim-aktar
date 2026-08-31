/** Vitrin karesi — fit-products-150.py ile aynı boyut. */
export const IMAGE_EDITOR_SIZE = 400;
export const IMAGE_EDITOR_BG = "#FDFBF7";

/** Görseli canvas'a yükler (data URL, blob veya site içi yol). */
export function loadImageElement(src) {
  const value = String(src ?? "").trim();
  if (!value) {
    return Promise.reject(new Error("Görsel adresi boş."));
  }

  if (/^(data:|blob:)/i.test(value)) {
    return loadViaImageTag(value);
  }

  // Aynı origin dosyalarını blob olarak al — crossOrigin/CORS sorununu önler.
  return fetch(value, { cache: "no-store" })
    .then((res) => {
      if (!res.ok) throw new Error("Görsel indirilemedi.");
      return res.blob();
    })
    .then((blob) => {
      const objectUrl = URL.createObjectURL(blob);
      return loadViaImageTag(objectUrl).finally(() => URL.revokeObjectURL(objectUrl));
    })
    .catch(() => loadViaImageTag(value));
}

function loadViaImageTag(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("Görsel yüklenemedi."));
    img.src = src;
  });
}

/** Ürünü kare alana sığdırır (contain). */
export function fitImageRect(naturalWidth, naturalHeight, size = IMAGE_EDITOR_SIZE, padding = 28) {
  const maxW = size - padding * 2;
  const maxH = size - padding * 2;
  const scale = Math.min(maxW / naturalWidth, maxH / naturalHeight);
  const w = naturalWidth * scale;
  const h = naturalHeight * scale;
  return {
    x: (size - w) / 2,
    y: (size - h) / 2,
    w,
    h,
  };
}

/** Düzenlenmiş kareyi JPEG data URL olarak döner. */
export function renderImageFrame(image, rect, quality = 0.88) {
  const canvas = document.createElement("canvas");
  canvas.width = IMAGE_EDITOR_SIZE;
  canvas.height = IMAGE_EDITOR_SIZE;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Görsel işlenemedi.");

  ctx.fillStyle = IMAGE_EDITOR_BG;
  ctx.fillRect(0, 0, IMAGE_EDITOR_SIZE, IMAGE_EDITOR_SIZE);
  ctx.drawImage(image, rect.x, rect.y, rect.w, rect.h);
  return canvas.toDataURL("image/jpeg", quality);
}

/** Dosyayı düzenleyici için ham data URL'e çevirir. */
export function readImageFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    if (!file?.type?.startsWith("image/")) {
      reject(new Error("Lütfen bir görsel dosyası seçin (JPG, PNG, WebP)."));
      return;
    }
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(new Error("Dosya okunamadı."));
    reader.readAsDataURL(file);
  });
}
