import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../services/api.js";
import { plantImageUrl } from "../lib/assetUrl.js";
import { applyPageSeo } from "../lib/seo.js";
import { whatsappUrl } from "../lib/whatsapp.js";
import { SHOP } from "../config/shop.js";

function formatPrice(value) {
  return new Intl.NumberFormat("tr-TR", {
    style: "currency",
    currency: "TRY",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

export default function ProductDetailPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const data = await api.getProductWithFallback(id);
        if (!cancelled) setProduct(data);
      } catch (err) {
        if (!cancelled) setError(err.message || "Ürün bulunamadı.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id]);

  useEffect(() => {
    if (!product) return;
    applyPageSeo({
      title: `${product.ad} — ${SHOP.name}`,
      description: product.kisaAciklama,
      path: `/urun/${product.id}`,
      imagePath: product.resimUrl,
      type: "product",
    });
  }, [product]);

  if (loading) {
    return (
      <main className="detail-main" id="main-content">
        <p className="plants-section__intro">Ürün yükleniyor…</p>
      </main>
    );
  }

  if (error || !product) {
    return (
      <main className="detail-main" id="main-content">
        <Link className="back-button" to="/">
          Ürünlere dön
        </Link>
        <div className="empty-state">
          <h4>{error || "Ürün bulunamadı"}</h4>
        </div>
      </main>
    );
  }

  const orderUrl = whatsappUrl(
    `Merhaba, ${product.ad} (${product.birim}, ${formatPrice(product.fiyat)}) sipariş etmek istiyorum.`
  );

  return (
    <main className="detail-main product-detail" id="main-content">
      <header className="detail-header">
        <Link className="back-button" to="/">
          Ürünlere dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">{product.kategori}</p>
          <h1>{product.ad}</h1>
          <p className="product-detail__price">
            {formatPrice(product.fiyat)} <small>/ {product.birim}</small>
          </p>
        </div>
        <div className="detail-header__actions">
          {product.stokta ? (
            <a className="shop-hero__cta" href={orderUrl} target="_blank" rel="noopener noreferrer">
              WhatsApp Sipariş
            </a>
          ) : (
            <span className="product-card__soldout">Şu an stokta yok</span>
          )}
        </div>
      </header>

      <section className="product-detail__layout">
        <figure className="product-detail__media">
          <img
            src={plantImageUrl(product.resimUrl)}
            alt={`${product.ad} görseli`}
            width="960"
            height="720"
          />
        </figure>
        <article className="info-card product-detail__info">
          <p className="product-detail__lead">{product.kisaAciklama}</p>
          <p>{product.aciklama}</p>
          {product.etiketler?.length ? (
            <div className="product-card__tags">
              {product.etiketler.map((tag) => (
                <span key={tag} className="product-card__tag">
                  {tag}
                </span>
              ))}
            </div>
          ) : null}
          <p className="product-detail__note">
            Fiyat bilgisi bilgilendirme amaçlıdır; güncel stok ve fiyat için WhatsApp veya dükkanımızı arayın.
          </p>
        </article>
      </section>
    </main>
  );
}
