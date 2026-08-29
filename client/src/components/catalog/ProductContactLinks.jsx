import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl } from "../../lib/whatsapp.js";

/** Fiyat gösterilmez; WhatsApp + Instagram ile iletişim. */
export function ProductContactLinks({ productName = "", compact = false }) {
  const message = productName
    ? `Merhaba, ${productName} hakkında fiyat bilgisi almak istiyorum.`
    : SHOP.whatsappMessages.general;

  return (
    <div className={`product-contact${compact ? " product-contact--compact" : ""}`}>
      <p className="product-contact__text">Fiyat bilgisi için bizimle iletişime geçin.</p>
      <div className="product-contact__links">
        <a
          className="product-contact__btn product-contact__btn--whatsapp"
          href={whatsappUrl(message)}
          target="_blank"
          rel="noopener noreferrer"
        >
          WhatsApp
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
