import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl } from "../../lib/whatsapp.js";

export function ShopHero({ productCount = 0 }) {
  return (
    <section className="shop-hero" aria-labelledby="shopHeroTitle">
      <div className="shop-hero__copy">
        <p className="section-label">Çan · Çanakkale</p>
        <h1 id="shopHeroTitle">{SHOP.name}</h1>
        <p className="shop-hero__text">
          Baharat, çay, macun, sirke ve doğal ürünler — yerel aktarımızdan kapınıza. Fiyat ve stok
          için WhatsApp&apos;tan yazmanız yeterli; genelde birkaç dakika içinde dönüş yapılır.
        </p>
        <div className="shop-hero__actions">
          <a
            className="shop-hero__cta"
            href={whatsappUrl(SHOP.whatsappMessages.order)}
            target="_blank"
            rel="noopener noreferrer"
          >
            WhatsApp ile Sipariş Ver
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
      <div className="shop-hero__stats">
        <div className="shop-stat">
          <strong>{productCount || "—"}</strong>
          <span>Ürün çeşidi</span>
        </div>
        <div className="shop-stat">
          <strong>09–19</strong>
          <span>Hafta içi açık</span>
        </div>
        <div className="shop-stat">
          <strong>Çan</strong>
          <span>Yerel aktar</span>
        </div>
      </div>
    </section>
  );
}

export function ShopTrustStrip() {
  const items = [
    "Yerel aktar dükkanı",
    "WhatsApp ile hızlı sipariş",
    "Anında fiyat bilgisi",
    "Çan teslimat",
  ];

  return (
    <div className="trust-strip" role="note" aria-label="Güven bilgileri">
      {items.map((item) => (
        <span key={item} className="trust-strip__pill">
          {item}
        </span>
      ))}
    </div>
  );
}
