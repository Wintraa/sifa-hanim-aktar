import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl } from "../../lib/whatsapp.js";

export function ShopHero({ productCount = 0 }) {
  return (
    <section className="shop-hero" aria-labelledby="shopHeroTitle">
      <div className="shop-hero__copy">
        <p className="section-label">Çan / Çanakkale · Aktar</p>
        <h1 id="shopHeroTitle">Doğal ürünler, güvenilir dükkan</h1>
        <p className="shop-hero__text">
          Baharat, çay, macun, sirke ve daha fazlası — sipariş ve fiyat bilgisi için WhatsApp veya
          Instagram üzerinden bize ulaşın. Hızlı yanıt, yerel teslimat imkânı.
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
  return (
    <div className="trust-strip" role="note">
      <span>✓ Yerel Şifa Hanım Aktar dükkanı</span>
      <span>✓ WhatsApp ile hızlı sipariş</span>
      <span>✓ Fiyat bilgisi anında</span>
      <span>✓ Güvenli iletişim</span>
    </div>
  );
}
