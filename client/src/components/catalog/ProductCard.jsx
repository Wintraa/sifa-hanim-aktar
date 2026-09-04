import { Link } from "react-router-dom";
import { recordProductClick } from "../../lib/product-clicks.js";
import { productBadges, productTeaser } from "../../lib/product-copy.js";
import { AddToCartButton } from "./AddToCartButton.jsx";
import { ProductImage } from "./ProductImage.jsx";
import { AdminProductImageControls } from "./AdminProductImageControls.jsx";

export function ProductCard({
  product,
  visibleIndex = 0,
  isAdmin = false,
  onEdit,
  onImageChange,
  inVitrin = false,
}) {
  const detailHref = `/urun/${product.id}`;
  const trackClick = () => recordProductClick(product.id);
  const inStock = product.stokta !== false;
  const badges = productBadges(product, inVitrin);
  const teaser = productTeaser(product);

  return (
    <article
      className={`product-card product-card--vitrine${inVitrin || product.oneCikan ? " product-card--featured" : ""}${!inStock ? " product-card--soldout" : ""}${isAdmin ? " product-card--admin" : ""}`}
    >
      <div className="product-card__media">
        <Link
          className="product-card__image-link"
          to={detailHref}
          aria-label={`${product.ad} detayı`}
          onClick={trackClick}
        >
          <ProductImage
            key={product.resimUrl}
            className="product-card__image"
            src={product.resimUrl}
            alt={`${product.ad} ürün görseli`}
            width="320"
            height="240"
            loading={visibleIndex < 6 ? "eager" : "lazy"}
            decoding="async"
          />
        </Link>

        {badges.length ? (
          <div className="product-card__badges">
            {badges.map((b) => (
              <span key={b.label} className={`product-card__badge product-card__badge--${b.tone}`}>
                {b.label}
              </span>
            ))}
          </div>
        ) : null}

        {isAdmin ? (
          <AdminProductImageControls
            isAdmin
            product={product}
            overlay
            showPreview={false}
            imageUrl={product.resimUrl}
            onImageChange={(url) => onImageChange?.({ ...product, resimUrl: url })}
          />
        ) : null}
      </div>

      <div className="product-card__content">
        <span className="product-card__category">{product.kategori}</span>
        <h4 className="product-card__title">
          <Link to={detailHref} onClick={trackClick}>
            {product.ad}
          </Link>
        </h4>
        <p className="product-card__teaser">{teaser}</p>

        <div className="product-card__price-row" aria-label="Fiyat bilgisi">
          <div className="product-card__price">
            <strong>Anlık fiyat</strong>
            <small>WhatsApp ile öğren</small>
          </div>
          {product.birim && product.birim !== "adet" ? (
            <span className="product-card__unit-pill">{product.birim}</span>
          ) : (
            <span className="product-card__unit-pill product-card__unit-pill--soft">Stokta</span>
          )}
        </div>

        <div className="product-card__actions">
          {inStock ? (
            <AddToCartButton product={product} stopPropagation className="product-card__cta-cart" />
          ) : (
            <span className="product-card__soldout">Stokta yok — bilgi için yazın</span>
          )}
          <Link
            className="product-card__cta-detail"
            to={detailHref}
            onClick={trackClick}
          >
            Hemen İncele
          </Link>
          {isAdmin ? (
            <button className="product-card__edit" type="button" onClick={() => onEdit?.(product)}>
              Ürünü Düzenle
            </button>
          ) : null}
        </div>
      </div>
    </article>
  );
}
