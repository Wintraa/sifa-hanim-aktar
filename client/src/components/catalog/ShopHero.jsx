import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl } from "../../lib/whatsapp.js";

export function ShopHero({ productCount = 0 }) {
  return (
    <section className="shop-hero shop-hero--vitrine" aria-labelledby="shopHeroTitle">
      <div className="shop-hero__glow" aria-hidden="true" />
      <div className="shop-hero__copy">
        <p className="shop-hero__eyebrow">Çan · Çanakkale · Yerel aktar</p>
        <h1 id="shopHeroTitle" className="shop-hero__brand">
          {SHOP.name}
        </h1>
        <p className="shop-hero__lead">
          Doğanın en seçilmişleri — tezgâhtan sepete, sepetten kapına. Baharat, çay, macun ve
          şifalı ürünler; fiyatı öğrenmek bir mesaj kadar yakın.
        </p>
        <div className="shop-hero__actions">
          <a
            className="shop-hero__cta shop-hero__cta--primary"
            href="#productsPanelTitle"
          >
            Vitrine Göz At
          </a>
          <a
            className="shop-hero__cta shop-hero__cta--wa"
            href={whatsappUrl(SHOP.whatsappMessages.order)}
            target="_blank"
            rel="noopener noreferrer"
          >
            WhatsApp ile Sipariş
          </a>
          <a
            className="shop-hero__ghost"
            href={instagramUrl()}
            target="_blank"
            rel="noopener noreferrer"
          >
            @{SHOP.instagram}
          </a>
        </div>
      </div>
      <div className="shop-hero__stats" aria-label="Mağaza özeti">
        <div className="shop-stat">
          <strong>{productCount || "—"}+</strong>
          <span>Ürün çeşidi</span>
        </div>
        <div className="shop-stat">
          <strong>Anında</strong>
          <span>Fiyat yanıtı</span>
        </div>
        <div className="shop-stat">
          <strong>09–19</strong>
          <span>Aktif hizmet</span>
        </div>
      </div>
    </section>
  );
}

export function ShopTrustStrip() {
  const items = [
    { title: "Güvenilir aktar", text: "Yılların tezgâh deneyimi" },
    { title: "Hızlı dönüş", text: "WhatsApp’tan dakikalar içinde" },
    { title: "Seçilmiş ürün", text: "Kalite odaklı vitrin" },
    { title: "Çan teslimat", text: "Yerel & kolay ulaşım" },
  ];

  return (
    <div className="trust-strip trust-strip--vitrine" role="note" aria-label="Güven bilgileri">
      {items.map((item) => (
        <div key={item.title} className="trust-strip__item">
          <strong>{item.title}</strong>
          <span>{item.text}</span>
        </div>
      ))}
    </div>
  );
}
