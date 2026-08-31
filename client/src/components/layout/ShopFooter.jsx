import { Link } from "react-router-dom";
import { SHOP } from "../../config/shop.js";
import { whatsappUrl, instagramUrl, mapsUrl } from "../../lib/whatsapp.js";

/** Mağaza sayfası alt bilgi — iletişim ve güven sinyalleri. */
export function ShopFooter() {
  return (
    <footer className="shop-footer">
      <div className="shop-footer__grid">
        <div className="shop-footer__brand">
          <p className="section-label">{SHOP.tagline}</p>
          <h2>{SHOP.name}</h2>
          <p className="shop-footer__text">
            Çan&apos;daki yerel aktarımızda baharat, çay, macun, sirke ve doğal ürünler. Sipariş ve
            fiyat bilgisi için WhatsApp üzerinden hızlıca ulaşabilirsiniz.
          </p>
        </div>

        <div className="shop-footer__col">
          <h3>İletişim</h3>
          <ul className="shop-footer__list">
            <li>
              <a href={whatsappUrl()} target="_blank" rel="noopener noreferrer">
                WhatsApp · {SHOP.phoneDisplay}
              </a>
            </li>
            <li>
              <a href={`tel:${SHOP.phoneTel}`}>{SHOP.phoneDisplay}</a>
            </li>
            <li>
              <a href={`mailto:${SHOP.email}`}>{SHOP.email}</a>
            </li>
            <li>
              <a href={instagramUrl()} target="_blank" rel="noopener noreferrer">
                Instagram @{SHOP.instagram}
              </a>
            </li>
          </ul>
        </div>

        <div className="shop-footer__col">
          <h3>Adres &amp; Saatler</h3>
          <p className="shop-footer__address">{SHOP.address}</p>
          <p className="shop-footer__hours">{SHOP.hours.weekdays}</p>
          <p className="shop-footer__hours">{SHOP.hours.sunday}</p>
          <a
            className="shop-footer__map"
            href={mapsUrl()}
            target="_blank"
            rel="noopener noreferrer"
          >
            Haritada aç
          </a>
        </div>
      </div>

      <div className="shop-footer__bar">
        <span>© {new Date().getFullYear()} {SHOP.name}</span>
        <nav className="shop-footer__nav" aria-label="Alt menü">
          <Link to="/bitkiler">Bitki Kütüphanesi</Link>
          <Link to="/iletisim">İletişim</Link>
        </nav>
      </div>
    </footer>
  );
}
