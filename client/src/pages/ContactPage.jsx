import { Link } from "react-router-dom";
import { SHOP } from "../config/shop.js";
import { ShopContactCards, WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";
import { whatsappUrl } from "../lib/whatsapp.js";

export default function ContactPage() {
  return (
    <>
      <main className="detail-main contact-page" id="main-content" style={{ paddingTop: "2rem" }}>
        <header className="detail-header contact-page__header" style={{ position: "static", marginBottom: "1.5rem" }}>
          <Link className="back-button" to="/">
            Kataloğa Dön
          </Link>
          <div className="detail-header__title">
            <p className="section-label">Dükkan</p>
            <h1>İletişim</h1>
          </div>
        </header>

        <section className="hero-card contact-page__intro">
          <div>
            <p className="section-label">{SHOP.name}</p>
            <h2>Sorunuz mu var? WhatsApp’tan yazın.</h2>
            <p className="hero-card__text">
              Hangi bitki size uygun, nasıl demlenir, stokta var mı — dükkan tezgâhında
              sorduğunuz soruları buradan da sorabilirsiniz. Mesajlar WhatsApp’a gider.
            </p>
          </div>
          <a
            className="back-button contact-page__cta"
            href={whatsappUrl(SHOP.whatsappMessages.advice)}
            target="_blank"
            rel="noopener noreferrer"
          >
            WhatsApp’tan Danış
          </a>
        </section>

        <ShopContactCards />

        <section className="info-card contact-page__actions">
          <h3>Hızlı mesaj şablonları</h3>
          <div className="contact-quick-links">
            <a href={whatsappUrl(SHOP.whatsappMessages.general)} target="_blank" rel="noopener noreferrer">
              Genel bilgi
            </a>
            <a href={whatsappUrl(SHOP.whatsappMessages.order)} target="_blank" rel="noopener noreferrer">
              Sipariş / stok
            </a>
            <a href={whatsappUrl(SHOP.whatsappMessages.advice)} target="_blank" rel="noopener noreferrer">
              Bitki danışmanlığı
            </a>
          </div>
        </section>
      </main>
      <WhatsAppFloatButton />
    </>
  );
}
