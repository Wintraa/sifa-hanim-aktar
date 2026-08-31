import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../services/api.js";
import { applyPageSeo } from "../lib/seo.js";
import { recordProductClick } from "../lib/product-clicks.js";
import { saveProductOverride } from "../lib/products.js";
import { isAdminUser } from "../lib/auth.js";
import { useAuth } from "../context/AuthContext.jsx";
import { showToast } from "../lib/toast.js";
import { SHOP } from "../config/shop.js";
import { AdminProductImageControls } from "../components/catalog/AdminProductImageControls.jsx";
import { ProductContactLinks } from "../components/catalog/ProductContactLinks.jsx";
import { ProductImage } from "../components/catalog/ProductImage.jsx";
import { RelatedProducts } from "../components/catalog/RelatedProducts.jsx";
import { ShopTrustStrip } from "../components/catalog/ShopHero.jsx";
import { WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";

export default function ProductDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const isAdmin = isAdminUser(user);
  const [product, setProduct] = useState(null);
  const [allProducts, setAllProducts] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const [data, list] = await Promise.all([
          api.getProductWithFallback(id),
          api.getProductsWithFallback(),
        ]);
        if (!cancelled) {
          setProduct(data);
          setAllProducts(list);
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

  const relatedProducts = useMemo(() => {
    if (!product?.kategori) return [];
    return allProducts.filter(
      (p) => p.kategori === product.kategori && Number(p.id) !== Number(product.id)
    );
  }, [allProducts, product]);

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
        <div className="product-detail__skeleton" aria-hidden="true">
          <div className="skeleton-block skeleton-block--wide" />
          <div className="skeleton-block" />
        </div>
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

  const lead = product.kisaAciklama?.replace(/\s*—\s*Şifa Hanım Aktar\.?\s*$/i, "") || product.kategori;

  const handleAdminImageChange = (resimUrl) => {
    try {
      const updated = { ...product, resimUrl };
      saveProductOverride(updated);
      setProduct(updated);
      showToast("Ürün resmi kaydedildi.", "success");
    } catch (err) {
      showToast(err.message || "Kaydedilemedi.", "error");
    }
  };

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
            <ProductImage
              className="product-detail__photo"
              src={product.resimUrl}
              alt={`${product.ad} görseli`}
              width="960"
              height="720"
            />
            <AdminProductImageControls
              isAdmin={isAdmin}
              imageUrl={product.resimUrl}
              showPreview={false}
              onImageChange={handleAdminImageChange}
            />
          </figure>

          <div className="product-detail__side">
            <article className="info-card product-detail__info">
              <p className="product-detail__lead">{lead}</p>
              {product.aciklama ? <p className="product-detail__body">{product.aciklama}</p> : (
                <p className="product-detail__body">
                  Sipariş ve fiyat bilgisi için WhatsApp veya Instagram üzerinden bize ulaşın — genelde birkaç
                  dakika içinde dönüş yapılır.
                </p>
              )}
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

        <RelatedProducts
          products={relatedProducts}
          currentId={product.id}
          title={`${product.kategori} — benzer ürünler`}
        />
      </main>

      <WhatsAppFloatButton />
    </>
  );
}
