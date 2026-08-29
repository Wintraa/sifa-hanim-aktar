import { useEffect, useState } from "react";
import { saveProductOverride, deleteProductOverride } from "../../lib/products.js";
import { showToast } from "../../lib/toast.js";

const CATEGORIES = [
  "Sıcak Çaylar",
  "Soğuk Bitki Demlemeleri",
  "Baharat & Harc",
  "Bitkisel Yağlar",
  "Aktar Karışımları",
  "Kurutulmuş Otlar",
];

export function ProductEditModal({ product, onClose, onSaved }) {
  const [form, setForm] = useState({ ...product });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm({ ...product });
  }, [product]);

  if (!product) return null;

  const setField = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        ...form,
        id: Number(form.id),
        fiyat: Number(form.fiyat),
        oneCikan: Boolean(form.oneCikan),
        stokta: Boolean(form.stokta),
        etiketler: String(form.etiketlerText || "")
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      };
      delete payload.etiketlerText;
      saveProductOverride(payload);
      showToast("Ürün kaydedildi.", "success");
      onSaved?.();
      onClose?.();
    } catch (err) {
      showToast(err.message || "Kaydedilemedi.", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = () => {
    if (!window.confirm(`"${product.ad}" vitrinden kaldırılsın mı?`)) return;
    deleteProductOverride(product.id);
    showToast("Ürün vitrinden kaldırıldı.", "info");
    onSaved?.();
    onClose?.();
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
          <h2 id="productEditTitle">Ürün Düzenle — Admin</h2>
          <button type="button" className="modal-card__close" onClick={onClose} aria-label="Kapat">
            ×
          </button>
        </header>

        <form className="product-edit-form" onSubmit={handleSave}>
          <label className="profile-field">
            <span>Ürün adı</span>
            <input
              required
              value={form.ad || ""}
              onChange={(e) => setField("ad", e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Kısa açıklama</span>
            <input
              required
              value={form.kisaAciklama || ""}
              onChange={(e) => setField("kisaAciklama", e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Detay açıklama</span>
            <textarea
              rows={4}
              value={form.aciklama || ""}
              onChange={(e) => setField("aciklama", e.target.value)}
            />
          </label>
          <div className="profile-form-grid">
            <label className="profile-field">
              <span>Fiyat (₺)</span>
              <input
                type="number"
                min="0"
                required
                value={form.fiyat ?? ""}
                onChange={(e) => setField("fiyat", e.target.value)}
              />
            </label>
            <label className="profile-field">
              <span>Birim</span>
              <input
                required
                value={form.birim || ""}
                onChange={(e) => setField("birim", e.target.value)}
              />
            </label>
          </div>
          <label className="profile-field">
            <span>Kategori</span>
            <select
              value={form.kategori || CATEGORIES[0]}
              onChange={(e) => setField("kategori", e.target.value)}
            >
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>
          <label className="profile-field">
            <span>Görsel yolu</span>
            <input
              value={form.resimUrl || ""}
              onChange={(e) => setField("resimUrl", e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Etiketler (virgülle)</span>
            <input
              value={form.etiketlerText ?? (form.etiketler || []).join(", ")}
              onChange={(e) => setField("etiketlerText", e.target.value)}
            />
          </label>
          <div className="product-edit-form__checks">
            <label className="checkbox-field">
              <input
                type="checkbox"
                checked={Boolean(form.oneCikan)}
                onChange={(e) => setField("oneCikan", e.target.checked)}
              />
              Öne çıkan
            </label>
            <label className="checkbox-field">
              <input
                type="checkbox"
                checked={form.stokta !== false}
                onChange={(e) => setField("stokta", e.target.checked)}
              />
              Stokta
            </label>
          </div>
          <div className="profile-form-actions">
            <button className="back-button" type="submit" disabled={saving}>
              {saving ? "Kaydediliyor…" : "Kaydet"}
            </button>
            <button className="dropdown-link dropdown-link--button" type="button" onClick={handleDelete}>
              Vitrinden kaldır
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
