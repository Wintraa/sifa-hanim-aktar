import { useRef, useState } from "react";
import { productImageUrl } from "../../lib/assetUrl.js";
import { compressImageFile } from "../../lib/imageUpload.js";
import { showToast } from "../../lib/toast.js";
import { ImageEditorPortal } from "./ImageEditorPortal.jsx";

/**
 * Sadece admin: Görsel Ekle + Görsel Düzenle.
 * overlay = fotoğrafın üstünde bar (vitrin kartları).
 */
export function AdminProductImageControls({
  isAdmin = false,
  imageUrl = "",
  onImageChange,
  showPreview = true,
  overlay = false,
}) {
  const fileInputRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editorSrc, setEditorSrc] = useState("");

  if (!isAdmin) return null;

  const hasImage = Boolean(String(imageUrl || "").trim());

  const handlePickFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setLoading(true);
    try {
      const dataUrl = await compressImageFile(file);
      onImageChange?.(dataUrl);
      showToast("Görsel eklendi. «Görsel Düzenle» ile yerleştir.", "success");
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
    setEditorSrc(productImageUrl(imageUrl));
    setEditorOpen(true);
  };

  const handleEditorApply = (dataUrl) => {
    onImageChange?.(dataUrl);
    setEditorOpen(false);
    setEditorSrc("");
    showToast("Görsel kaydedildi.", "success");
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
            <img src={productImageUrl(imageUrl)} alt="Ürün görseli önizlemesi" />
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
