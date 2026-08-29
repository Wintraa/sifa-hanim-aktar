import { useEffect, useState } from "react";
import {
  addProductCategory,
  updateProductCategory,
  deleteProductCategory,
  notifyCategoriesChanged,
} from "../../lib/product-categories.js";
import { showToast } from "../../lib/toast.js";

export function CategoryEditModal({ category, onClose, onSaved }) {
  const isNew = !category?.id;
  const [name, setName] = useState(category?.ad || "");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setName(category?.ad || "");
  }, [category]);

  if (category === null || category === undefined) return null;

  const handleSave = (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (isNew) {
        addProductCategory(name);
        showToast("Kategori eklendi.", "success");
      } else {
        updateProductCategory(category.id, name);
        showToast("Kategori güncellendi.", "success");
      }
      notifyCategoriesChanged();
      onSaved?.();
      onClose?.();
    } catch (err) {
      showToast(err.message || "Kaydedilemedi.", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = () => {
    if (!window.confirm(`"${category.ad}" kategorisi silinsin mi?`)) return;
    deleteProductCategory(category.id);
    notifyCategoriesChanged();
    showToast("Kategori silindi.", "info");
    onSaved?.();
    onClose?.();
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        className="modal-card category-edit-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="categoryEditTitle"
        onClick={(e) => e.stopPropagation()}
      >
        <header className="modal-card__header">
          <h2 id="categoryEditTitle">{isNew ? "Kategori Ekle" : "Kategori Düzenle"}</h2>
          <button type="button" className="modal-card__close" onClick={onClose} aria-label="Kapat">
            ×
          </button>
        </header>

        <form className="product-edit-form" onSubmit={handleSave}>
          <label className="profile-field">
            <span>Kategori adı *</span>
            <input
              required
              autoFocus
              placeholder="Örn: Sıcak Çaylar"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </label>
          <div className="profile-form-actions">
            <button className="add-product-btn" type="submit" disabled={saving}>
              {saving ? "Kaydediliyor…" : isNew ? "Kategoriyi Ekle" : "Kaydet"}
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
