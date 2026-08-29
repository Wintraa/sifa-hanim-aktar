import { SHOP } from "../../config/shop.js";
import { whatsappUrl, telUrl, mailUrl, mapsUrl } from "../../lib/whatsapp.js";

export function ShopContactCards({ compact = false }) {
  const items = [
    {
      key: "whatsapp",
      label: "WhatsApp",
      value: SHOP.phoneDisplay,
      hint: "Mesaj gönder — tıkla",
      href: whatsappUrl(),
      external: true,
      primary: true,
    },
    {
      key: "phone",
      label: "Telefon",
      value: SHOP.phoneDisplay,
      hint: "Ara",
      href: telUrl(),
      external: false,
    },
    {
      key: "email",
      label: "E-posta",
      value: SHOP.email,
      hint: "Mail at",
      href: mailUrl(),
      external: false,
    },
    {
      key: "address",
      label: "Adres",
      value: SHOP.address,
      hint: "Haritada aç",
      href: mapsUrl(),
      external: true,
    },
  ];

  return (
    <div className={`shop-contact${compact ? " shop-contact--compact" : ""}`}>
      {items.map((item) => (
        <a
          key={item.key}
          className={`shop-contact__card${item.primary ? " shop-contact__card--whatsapp" : ""}`}
          href={item.href}
          target={item.external ? "_blank" : undefined}
          rel={item.external ? "noopener noreferrer" : undefined}
        >
          <span className="shop-contact__label">{item.label}</span>
          <strong className="shop-contact__value">{item.value}</strong>
          <span className="shop-contact__hint">{item.hint}</span>
        </a>
      ))}
      {!compact ? (
        <div className="shop-contact__hours">
          <span className="shop-contact__label">Çalışma saatleri</span>
          <p>{SHOP.hours.weekdays}</p>
          <p>{SHOP.hours.sunday}</p>
        </div>
      ) : null}
    </div>
  );
}

export function WhatsAppFloatButton() {
  return (
    <a
      className="whatsapp-float"
      href={whatsappUrl(SHOP.whatsappMessages.order)}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="WhatsApp ile sipariş ver"
      title="WhatsApp ile sipariş ver"
    >
      <span className="whatsapp-float__label">WhatsApp Sipariş</span>
    </a>
  );
}
