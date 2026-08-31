import { useRef, useState } from "react";
import { productImageUrl } from "../../lib/assetUrl.js";
import { compressImageFile } from "../../lib/imageUpload.js";
import { clearProductImageOverride } from "../../lib/products.js";
import { showToast } from "../../lib/toast.js";
import { uploadProductImagePermanent } from "../../services/productImages.js";
import { ImageEditorPortal } from "./ImageEditorPortal.jsx";

/**
 * Sadece admin: Görsel Ekle + Görsel Düzenle.
 * Kayıt → sunucuya kalıcı (products.json + assets/products).
 */
export function AdminProductImageControls({
  isAdmin = false,
  product = null,
  imageUrl = "",
  onImageChange,
  showPreview = true,
  overlay = false,
}) {
  const fileInputRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editorSrc, setEditorSrc] = useState("");

  if (!isAdmin || !product) return null;

  const hasImage = Boolean(String(imageUrl || product.resimUrl || "").trim());

  const persistImage = async (dataUrl, fromEditor = false) => {
    setLoading(true);
    try {
      const result = await uploadProductImagePermanent(product.id, dataUrl);
      clearProductImageOverride(product.id);
      onImageChange?.(result.resimUrl);
      if (result.github) {
        showToast(
          "Görsel GitHub'a kaydedildi. Vercel deploy bitince herkes görür (1–2 dk).",
          "success"
        );
      } else {
        showToast("Görsel kalıcı kaydedildi — vitrin güncellendi.", "success");
      }
    } catch (err) {
      if (fromEditor) {
        onImageChange?.(dataUrl);
        showToast(
          `Sunucuya yazılamadı (${err.message}). Sadece bu tarayıcıda görünür.`,
          "info"
        );
      } else {
        showToast(err.message || "Görsel kaydedilemedi.", "error");
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePickFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setLoading(true);
    try {
      const dataUrl = await compressImageFile(file);
      setEditorSrc(dataUrl);
      setEditorOpen(true);
      showToast("Fotoğraf yüklendi. Konumlandırıp «Görseli Uygula» de.", "success");
    } catch (err) {
      showToast(err.message || "Görsel yüklenemedi.", "error");
    } finally {
      setLoading(false);
    }
  };

  const openEditor = () => {
    if (!hasImage) {
      showToast("Önce «Görsel Ekle» ile fotoğraf seç.", "info");
      fileInputRef.current?.click();
      return;
    }
    setEditorSrc(productImageUrl(imageUrl || product.resimUrl));
    setEditorOpen(true);
  };

  const handleEditorApply = async (dataUrl) => {
    setEditorOpen(false);
    setEditorSrc("");
    await persistImage(dataUrl, true);
  };

  const handleEditorCancel = () => {
    setEditorOpen(false);
    setEditorSrc("");
  };

  const rootClass = [
    "admin-image-controls",
    overlay ? "admin-image-controls--overlay" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <>
      <div className={rootClass}>
        {showPreview && hasImage && !overlay ? (
          <div className="admin-image-controls__preview">
            <img src={productImageUrl(imageUrl || product.resimUrl)} alt="Ürün görseli önizlemesi" />
          </div>
        ) : null}

        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif,image/*"
          hidden
          onChange={handlePickFile}
        />

        <div className="admin-image-controls__actions">
          <button
            type="button"
            className="admin-image-controls__btn admin-image-controls__btn--add"
            disabled={loading}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              fileInputRef.current?.click();
            }}
          >
            {loading ? "…" : "Görsel Ekle"}
          </button>
          <button
            type="button"
            className="admin-image-controls__btn admin-image-controls__btn--edit"
            disabled={loading}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              openEditor();
            }}
          >
            Görsel Düzenle
          </button>
        </div>
      </div>

      {editorOpen && editorSrc ? (
        <ImageEditorPortal
          imageSrc={editorSrc}
          title="Görseli Düzenle"
          onApply={handleEditorApply}
          onCancel={handleEditorCancel}
        />
      ) : null}
    </>
  );
}
