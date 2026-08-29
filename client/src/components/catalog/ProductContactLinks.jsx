import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl } from "../../lib/whatsapp.js";

function orderMessage(productName, birim) {
  if (!productName) return SHOP.whatsappMessages.order;
  const unit = birim ? ` (${birim})` : "";
  return `Merhaba, ${productName}${unit} sipariş etmek istiyorum. Fiyat bilgisi alabilir miyim?`;
}

/** Fiyat yok — WhatsApp / Instagram ile siparişe yönlendirir. */
export function ProductContactLinks({
  productName = "",
  birim = "",
  compact = false,
  panel = false,
}) {
  const message = orderMessage(productName, birim);
  const waLabel = compact ? "Sipariş Ver" : "WhatsApp ile Sipariş Ver";

  if (panel) {
    return (
      <aside className="product-order-panel" aria-label="Sipariş ve iletişim">
        <p className="product-order-panel__eyebrow">Sipariş</p>
        <h2 className="product-order-panel__title">Fiyat ve stok için bize yazın</h2>
        <p className="product-order-panel__text">
          Ürünü sepete eklemek yerine WhatsApp veya Instagram üzerinden doğrudan sipariş
          verebilirsiniz. Genelde birkaç dakika içinde dönüş yapılır.
        </p>
        <ul className="product-order-panel__list">
          <li>Hızlı fiyat bilgisi</li>
          <li>Çan / Çanakkale teslimat seçenekleri</li>
          <li>Güvenilir aktar danışmanlığı</li>
        </ul>
        <div className="product-order-panel__actions">
          <a
            className="product-order-panel__cta product-order-panel__cta--whatsapp"
            href={whatsappUrl(message)}
            target="_blank"
            rel="noopener noreferrer"
          >
            WhatsApp Sipariş
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
