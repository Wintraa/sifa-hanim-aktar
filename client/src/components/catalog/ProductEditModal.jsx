import { useEffect, useState } from "react";
import { saveProductOverride, deleteProductOverride } from "../../lib/products.js";
import { getCategoryNames, CATEGORIES_CHANGED } from "../../lib/product-categories.js";
import { showToast } from "../../lib/toast.js";

export function ProductEditModal({ product, isNew = false, onClose, onSaved }) {
  const [form, setForm] = useState({ ...product, etiketlerText: "" });
  const [categories, setCategories] = useState(() => getCategoryNames());
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm({
      ...product,
      etiketlerText: (product.etiketler || []).join(", "),
    });
  }, [product]);

  useEffect(() => {
    const reload = () => setCategories(getCategoryNames());
    reload();
    window.addEventListener(CATEGORIES_CHANGED, reload);
    return () => window.removeEventListener(CATEGORIES_CHANGED, reload);
  }, []);

  if (!product) return null;

  const setField = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

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
        fiyat: Number(form.fiyat),
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
      if (!Number.isFinite(payload.fiyat) || payload.fiyat < 0) {
        throw new Error("Geçerli bir fiyat girin.");
      }
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

          <label className="profile-field">
            <span>Ürün adı *</span>
            <input
              required
              autoFocus
              placeholder="Örn: Papatya Çiçeği"
              value={form.ad || ""}
              onChange={(e) => setField("ad", e.target.value)}
            />
          </label>

          <div className="profile-form-grid">
            <label className="profile-field">
              <span>Fiyat (₺) *</span>
              <input
                type="number"
                min="0"
                step="1"
                required
                placeholder="89"
                value={form.fiyat ?? ""}
                onChange={(e) => setField("fiyat", e.target.value)}
              />
            </label>
            <label className="profile-field">
              <span>Birim *</span>
              <input
                required
                placeholder="100 g, adet, 10 ml…"
                value={form.birim || ""}
                onChange={(e) => setField("birim", e.target.value)}
              />
            </label>
          </div>

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

          <label className="profile-field">
            <span>Fotoğraf yolu (isteğe bağlı)</span>
            <input
              placeholder="assets/plants/photos/01-matricaria-chamomilla.jpg"
              value={form.resimUrl || ""}
              onChange={(e) => setField("resimUrl", e.target.value)}
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
