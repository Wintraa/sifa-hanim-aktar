import { useEffect, useRef, useState } from "react";
import { saveProductOverride, deleteProductOverride } from "../../lib/products.js";
import { getCategoryNames, CATEGORIES_CHANGED } from "../../lib/product-categories.js";
import { compressImageFile } from "../../lib/imageUpload.js";
import { productImageUrl } from "../../lib/assetUrl.js";
import { showToast } from "../../lib/toast.js";

/** Aktar vitrininde sık kullanılan birimler */
const BIRIM_SECENEKLERI = [
  "adet",
  "50 g",
  "100 g",
  "150 g",
  "200 g",
  "250 g",
  "500 g",
  "1 kg",
  "10 ml",
  "20 ml",
  "50 ml",
  "100 ml",
  "set",
  "paket",
];

export function ProductEditModal({ product, isNew = false, onClose, onSaved }) {
  const [form, setForm] = useState({ ...product, etiketlerText: "" });
  const [categories, setCategories] = useState(() => getCategoryNames());
  const [saving, setSaving] = useState(false);
  const [imageLoading, setImageLoading] = useState(false);
  const [imageFileName, setImageFileName] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    setForm({
      ...product,
      etiketlerText: (product.etiketler || []).join(", "),
    });
    setImageFileName("");
    setIsDragging(false);
  }, [product]);

  useEffect(() => {
    const reload = () => setCategories(getCategoryNames());
    reload();
    window.addEventListener(CATEGORIES_CHANGED, reload);
    return () => window.removeEventListener(CATEGORIES_CHANGED, reload);
  }, []);

  if (!product) return null;

  const birimSecenekleri = BIRIM_SECENEKLERI.includes(form.birim)
    ? BIRIM_SECENEKLERI
    : form.birim
      ? [form.birim, ...BIRIM_SECENEKLERI]
      : BIRIM_SECENEKLERI;

  const setField = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const applyImageFile = async (file) => {
    if (!file) return;
    setImageLoading(true);
    try {
      const dataUrl = await compressImageFile(file);
      setField("resimUrl", dataUrl);
      setImageFileName(file.name);
      showToast("Görsel seçildi. Kaydetmeyi unutmayın.", "success");
    } catch (err) {
      showToast(err.message || "Görsel yüklenemedi.", "error");
    } finally {
      setImageLoading(false);
    }
  };

  const handleImagePick = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    await applyImageFile(file);
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!imageLoading) setIsDragging(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!imageLoading) setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.currentTarget.contains(e.relatedTarget)) return;
    setIsDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (imageLoading) return;
    const file = e.dataTransfer.files?.[0];
    await applyImageFile(file);
  };

  const clearImage = () => {
    setField("resimUrl", "");
    setImageFileName("");
  };

  const handleSave = (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const kategori =
        categories.length > 0
          ? String(form.kategori || categories[0]).trim()
          : String(form.kategoriManual || "").trim();

      if (!kategori) {
        throw new Error("Önce sol menüden kategori ekleyin veya kategori adı yazın.");
      }

      const payload = {
        id: Number(form.id),
        ad: String(form.ad || "").trim(),
        kisaAciklama: String(form.kisaAciklama || "").trim(),
        aciklama: String(form.aciklama || "").trim(),
        birim: String(form.birim || "adet").trim(),
        kategori,
        resimUrl: String(form.resimUrl || "").trim(),
        oneCikan: Boolean(form.oneCikan),
        stokta: form.stokta !== false,
        etiketler: String(form.etiketlerText || "")
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      };
      if (!payload.ad) throw new Error("Ürün adı zorunlu.");
      saveProductOverride(payload);
      showToast(isNew ? "Ürün eklendi." : "Ürün güncellendi.", "success");
      onSaved?.();
    } catch (err) {
      showToast(err.message || "Kaydedilemedi.", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = () => {
    if (!window.confirm(`"${product.ad}" silinsin mi?`)) return;
    deleteProductOverride(product.id);
    showToast("Ürün silindi.", "info");
    onSaved?.();
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="modal-card product-edit-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="productEditTitle"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="modal-card__header">
          <h2 id="productEditTitle">{isNew ? "Yeni Ürün" : "Ürünü Düzenle"}</h2>
          <button type="button" className="modal-card__close" onClick={onClose} aria-label="Kapat">
            ×
          </button>
        </header>

        <form className="product-edit-form" onSubmit={handleSave}>
          <p className="product-edit-form__intro">Zorunlu alanları doldurup kaydet.</p>

          <div
            className={`product-edit-form__image${isDragging ? " is-dragging" : ""}`}
            onDragEnter={handleDragEnter}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <span className="product-edit-form__image-label">Ürün görseli</span>

            {!form.resimUrl ? (
              <label
                htmlFor="product-edit-image-input"
                className="product-edit-form__dropzone"
              >
                <span className="product-edit-form__dropzone-icon" aria-hidden="true">
                  +
                </span>
                <span className="product-edit-form__dropzone-hint">
                  Fotoğrafı buraya sürükleyip bırakın
                </span>
                <span className="product-edit-form__dropzone-sub">
                  veya tıklayıp bilgisayardan seçin
                </span>
              </label>
            ) : (
              <div className="product-edit-form__dropzone product-edit-form__dropzone--has-image">
                <div className="product-edit-form__preview">
                  <img src={productImageUrl(form.resimUrl)} alt="Seçilen ürün görseli önizlemesi" />
                </div>
              </div>
            )}

            <input
              id="product-edit-image-input"
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp,image/gif,image/*"
              hidden
              onChange={handleImagePick}
            />

            <div className="product-edit-form__image-actions">
              {imageLoading ? (
                <span className="add-product-btn product-edit-form__pick-btn is-disabled" aria-live="polite">
                  Görsel işleniyor…
                </span>
              ) : (
                <label htmlFor="product-edit-image-input" className="add-product-btn product-edit-form__pick-btn">
                  {form.resimUrl ? "Görseli Değiştir" : "Görsel Ekle"}
                </label>
              )}
              {form.resimUrl ? (
                <button
                  className="dropdown-link dropdown-link--button"
                  type="button"
                  onClick={clearImage}
                >
                  Görseli Kaldır
                </button>
              ) : null}
            </div>

            {imageFileName ? (
              <p className="product-edit-form__image-name">Seçilen dosya: {imageFileName}</p>
            ) : null}
          </div>

          <label className="profile-field">
            <span>Ürün adı *</span>
            <input
              required
              autoFocus
              placeholder="Örn: Kuru Adaçayı"
              value={form.ad || ""}
              onChange={(e) => setField("ad", e.target.value)}
            />
          </label>

          <label className="profile-field">
            <span>Birim *</span>
            <select
              required
              value={form.birim || "adet"}
              onChange={(e) => setField("birim", e.target.value)}
            >
              {birimSecenekleri.map((birim) => (
                <option key={birim} value={birim}>
                  {birim}
                </option>
              ))}
            </select>
          </label>

          {categories.length > 0 ? (
            <label className="profile-field">
              <span>Kategori *</span>
              <select
                value={form.kategori || categories[0]}
                onChange={(e) => setField("kategori", e.target.value)}
              >
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </label>
          ) : (
            <label className="profile-field">
              <span>Kategori * (sol menüden de ekleyebilirsin)</span>
              <input
                required
                placeholder="Örn: Sıcak Çaylar"
                value={form.kategoriManual || ""}
                onChange={(e) => setField("kategoriManual", e.target.value)}
              />
            </label>
          )}

          <label className="profile-field">
            <span>Kısa açıklama</span>
            <input
              placeholder="Vitrinde görünen tek cümle"
              value={form.kisaAciklama || ""}
              onChange={(e) => setField("kisaAciklama", e.target.value)}
            />
          </label>

          <label className="profile-field">
            <span>Detaylı açıklama</span>
            <textarea
              rows={3}
              placeholder="Kullanım, içerik, notlar…"
              value={form.aciklama || ""}
              onChange={(e) => setField("aciklama", e.target.value)}
            />
          </label>

          <div className="product-edit-form__checks">
            <label className="checkbox-field">
              <input
                type="checkbox"
                checked={form.stokta !== false}
                onChange={(e) => setField("stokta", e.target.checked)}
              />
              Stokta var
            </label>
            <label className="checkbox-field">
              <input
                type="checkbox"
                checked={Boolean(form.oneCikan)}
                onChange={(e) => setField("oneCikan", e.target.checked)}
              />
              Öne çıkan
            </label>
          </div>

          <div className="profile-form-actions">
            <button className="add-product-btn" type="submit" disabled={saving}>
              {saving ? "Kaydediliyor…" : isNew ? "Ürünü Kaydet" : "Değişiklikleri Kaydet"}
            </button>
            {!isNew ? (
              <button className="dropdown-link dropdown-link--button" type="button" onClick={handleDelete}>
                Sil
              </button>
            ) : null}
          </div>
        </form>
      </div>
    </div>
  );
}
