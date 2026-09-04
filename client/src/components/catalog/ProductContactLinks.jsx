import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl } from "../../lib/whatsapp.js";
import { AddToCartButton } from "./AddToCartButton.jsx";

function orderMessage(productName, birim) {
  if (!productName) return SHOP.whatsappMessages.order;
  const unit = birim ? ` (${birim})` : "";
  return `Merhaba, ${productName}${unit} sipariş etmek istiyorum. Fiyat bilgisi alabilir miyim?`;
}

/** Fiyat yok — WhatsApp / Instagram ile siparişe yönlendirir. */
export function ProductContactLinks({
  productName = "",
  birim = "",
  product = null,
  compact = false,
  card = false,
  panel = false,
}) {
  const message = orderMessage(productName, birim);
  const waLabel = card ? "WhatsApp" : compact ? "Sipariş Ver" : "WhatsApp ile Sipariş Ver";

  if (card) {
    return (
      <a
        className="product-card__wa"
        href={whatsappUrl(message)}
        target="_blank"
        rel="noopener noreferrer"
        onClick={(e) => e.stopPropagation()}
      >
        {waLabel}
      </a>
    );
  }

  if (panel) {
    return (
      <aside className="product-order-panel" aria-label="Sipariş ve iletişim">
        <p className="product-order-panel__eyebrow">Sipariş</p>
        <h2 className="product-order-panel__title">Sepete ekle, toplu fiyat sor</h2>
        <p className="product-order-panel__text">
          Sepete ekle, vitrinden biriken ürünleri tek WhatsApp mesajıyla sor — fiyat ve stok
          genelde birkaç dakika içinde gelir. Premium aktar deneyimi, kapına kadar.
        </p>
        <ul className="product-order-panel__list">
          <li>Sepete ekle → toplu fiyat sorusu</li>
          <li>Çan / Çanakkale teslimat seçenekleri</li>
          <li>Güvenilir aktar danışmanlığı</li>
        </ul>
        <div className="product-order-panel__actions">
          {product?.stokta !== false ? (
            <AddToCartButton product={product} className="product-order-panel__cart" />
          ) : null}
          <a
            className="product-order-panel__cta product-order-panel__cta--whatsapp"
            href={whatsappUrl(message)}
            target="_blank"
            rel="noopener noreferrer"
          >
            Tek Ürün WhatsApp
          </a>
          <a
            className="product-order-panel__cta product-order-panel__cta--instagram"
            href={instagramUrl()}
            target="_blank"
            rel="noopener noreferrer"
          >
            Instagram DM
          </a>
        </div>
        <p className="product-order-panel__handle">@{SHOP.instagram}</p>
      </aside>
    );
  }

  return (
    <div className={`product-contact${compact ? " product-contact--compact" : ""}`}>
      <p className="product-contact__text">Fiyat bilgisi için bizimle iletişime geçin.</p>
      <div className="product-contact__links">
        <a
          className="product-contact__btn product-contact__btn--whatsapp product-contact__btn--primary"
          href={whatsappUrl(message)}
          target="_blank"
          rel="noopener noreferrer"
        >
          {waLabel}
        </a>
        <a
          className="product-contact__btn product-contact__btn--instagram"
          href={instagramUrl()}
          target="_blank"
          rel="noopener noreferrer"
        >
          Instagram
        </a>
      </div>
      {!compact ? (
        <span className="product-contact__handle">@{SHOP.instagram}</span>
      ) : null}
    </div>
  );
}
