import { productImageUrl } from "../../lib/assetUrl.js";
import { ProductImage } from "./ProductImage.jsx";
import { useCart } from "../../context/CartContext.jsx";

/** Sepet listesi + WhatsApp ile toplu bilgi butonu. */
export function CartPanel({ onContinue }) {
  const { items, setQuantity, removeItem, clearCart, itemCount, lineCount, whatsappHref } = useCart();

  if (items.length === 0) {
    return (
      <div className="cart-panel__empty">
        <p>Henüz ürün eklemedin.</p>
        <p className="cart-drawer__empty-hint">
          Vitrinden «Sepete Ekle» ile ürünleri biriktir, tek mesajla toplu bilgi al.
        </p>
        {onContinue ? (
          <button type="button" className="add-product-btn" onClick={onContinue}>
            Alışverişe devam
          </button>
        ) : null}
      </div>
    );
  }

  return (
    <div className="cart-panel">
      <ul className="cart-drawer__list cart-panel__list">
        {items.map((item) => (
          <li key={item.id} className="cart-line">
            <div className="cart-line__thumb">
              <ProductImage
                src={productImageUrl(item.resimUrl || `/assets/products/${String(item.id).padStart(2, "0")}.jpg`)}
                alt=""
                width="56"
                height="56"
              />
            </div>
            <div className="cart-line__body">
              {item.kategori ? <span className="cart-line__cat">{item.kategori}</span> : null}
              <strong className="cart-line__name">{item.ad}</strong>
              {item.birim && item.birim !== "adet" ? <span className="cart-line__unit">{item.birim}</span> : null}
              <div className="cart-line__qty">
                <button type="button" aria-label="Azalt" onClick={() => setQuantity(item.id, item.quantity - 1)}>
                  −
                </button>
                <span>{item.quantity}</span>
                <button type="button" aria-label="Artır" onClick={() => setQuantity(item.id, item.quantity + 1)}>
                  +
                </button>
              </div>
            </div>
            <button
              type="button"
              className="cart-line__remove"
              aria-label={`${item.ad} kaldır`}
              onClick={() => removeItem(item.id)}
            >
              ×
            </button>
          </li>
        ))}
      </ul>

      <footer className="cart-drawer__foot cart-panel__foot">
        <p className="cart-drawer__note">
          {lineCount} çeşit · {itemCount} adet. Sepetteki tüm ürünler tek WhatsApp mesajında gider.
        </p>
        <a className="cart-drawer__wa" href={whatsappHref} target="_blank" rel="noopener noreferrer">
          WhatsApp ile Toplu Bilgi Al
        </a>
        <p className="cart-drawer__wa-hint">Sepetteki tüm ürünler tek mesajda listelenir.</p>
        <button type="button" className="cart-drawer__clear" onClick={clearCart}>
          Sepeti temizle
        </button>
      </footer>
    </div>
  );
}
