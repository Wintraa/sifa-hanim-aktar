import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../services/api.js";
import { productImageUrl } from "../lib/assetUrl.js";
import { applyPageSeo } from "../lib/seo.js";
import { recordProductClick } from "../lib/product-clicks.js";
import { SHOP } from "../config/shop.js";
import { ProductContactLinks } from "../components/catalog/ProductContactLinks.jsx";
import { ShopTrustStrip } from "../components/catalog/ShopHero.jsx";
import { WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";

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
        if (!cancelled) {
          setProduct(data);
          recordProductClick(data.id);
        }
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
      imagePath: product.resimUrl || "/assets/product-placeholder.svg",
      type: "product",
    });
  }, [product]);

  if (loading) {
    return (
      <main className="detail-main product-detail" id="main-content">
        <p className="plants-section__intro">Ürün yükleniyor…</p>
      </main>
    );
  }

  if (error || !product) {
    return (
      <main className="detail-main product-detail" id="main-content">
        <Link className="back-button" to="/">
          Ürünlere dön
        </Link>
        <div className="empty-state">
          <h4>{error || "Ürün bulunamadı"}</h4>
        </div>
      </main>
    );
  }

  return (
    <>
      <main className="detail-main product-detail" id="main-content">
        <header className="detail-header product-detail__header">
          <Link className="back-button" to="/">
            ← Tüm ürünler
          </Link>
          <div className="detail-header__title">
            <p className="section-label">{product.kategori}</p>
            <h1>{product.ad}</h1>
            {product.birim ? (
              <p className="product-detail__unit">
                Birim: <strong>{product.birim}</strong>
              </p>
            ) : null}
          </div>
        </header>

        <ShopTrustStrip />

        <section className="product-detail__layout">
          <figure className="product-detail__media info-card">
            <img
              src={productImageUrl(product.resimUrl)}
              alt={`${product.ad} görseli`}
              width="960"
              height="720"
            />
          </figure>

          <div className="product-detail__side">
            <article className="info-card product-detail__info">
              <p className="product-detail__lead">{product.kisaAciklama}</p>
              {product.aciklama ? <p className="product-detail__body">{product.aciklama}</p> : null}
              {product.etiketler?.length ? (
                <div className="product-card__tags">
                  {product.etiketler.map((tag) => (
                    <span key={tag} className="product-card__tag">
                      {tag}
                    </span>
                  ))}
                </div>
              ) : null}
            </article>

            <ProductContactLinks productName={product.ad} birim={product.birim} panel />
          </div>
        </section>
      </main>

      <WhatsAppFloatButton />
    </>
  );
}
