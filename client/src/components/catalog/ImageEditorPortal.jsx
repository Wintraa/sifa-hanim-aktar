import { createPortal } from "react-dom";
import { ProductImageEditor } from "./ProductImageEditor.jsx";

/** Tam ekran fotoğraf editörü — modal içinde kaybolmasın diye body'ye portal. */
export function ImageEditorPortal({ imageSrc, title = "Resmi Düzenle", onApply, onCancel }) {
  if (!imageSrc || typeof document === "undefined") return null;

  return createPortal(
    <div className="image-editor-portal" role="dialog" aria-modal="true" aria-label={title}>
      <button
        type="button"
        className="image-editor-portal__backdrop"
        aria-label="Kapat"
        onClick={onCancel}
      />
      <div className="image-editor-portal__panel">
        <header className="image-editor-portal__head">
          <h3>{title}</h3>
          <button type="button" className="modal-card__close" onClick={onCancel} aria-label="Kapat">
            ×
          </button>
        </header>
        <ProductImageEditor imageSrc={imageSrc} onApply={onApply} onCancel={onCancel} />
      </div>
    </div>,
    document.body
  );
}
