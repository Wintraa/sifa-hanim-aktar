import { Link } from "react-router-dom";
import { plantImageUrl } from "../../lib/assetUrl.js";
import { whatsappUrl } from "../../lib/whatsapp.js";
import { recordProductClick } from "../../lib/product-clicks.js";

function formatPrice(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "";
  return new Intl.NumberFormat("tr-TR", {
    style: "currency",
    currency: "TRY",
    maximumFractionDigits: 0,
  }).format(n);
}

export function ProductCard({ product, visibleIndex = 0, isAdmin = false, onEdit, inVitrin = false }) {
  const detailHref = `/urun/${product.id}`;
  const orderUrl = whatsappUrl(`Merhaba, ${product.ad} (${product.birim}) için sipariş vermek istiyorum.`);

  const trackClick = () => recordProductClick(product.id);

  return (
    <article className={`product-card${inVitrin ? " product-card--featured" : ""}`}>
      <div className="product-card__media">
        <Link
          className="product-card__image-link"
          to={detailHref}
          aria-label={`${product.ad} detayı`}
          onClick={trackClick}
        >
          <img
            className="product-card__image"
            src={plantImageUrl(product.resimUrl)}
            alt={`${product.ad} ürün görseli`}
            width="640"
            height="480"
            loading={visibleIndex < 3 ? "eager" : "lazy"}
            decoding="async"
          />
        </Link>
        {inVitrin ? <span className="product-card__ribbon">Vitrin · Popüler</span> : null}
        {!product.stokta ? <span className="product-card__ribbon product-card__ribbon--muted">Tükendi</span> : null}
      </div>

      <div className="product-card__content">
        <span className="product-card__category">{product.kategori}</span>
        <h4 className="product-card__title">
          <Link to={detailHref} onClick={trackClick}>{product.ad}</Link>
        </h4>
        <p className="product-card__desc">{product.kisaAciklama}</p>
        {product.etiketler?.length ? (
          <div className="product-card__tags">
            {product.etiketler.slice(0, 3).map((tag) => (
              <span key={tag} className="product-card__tag">
                {tag}
              </span>
            ))}
          </div>
        ) : null}
        <div className="product-card__footer">
          <div className="product-card__price">
            <strong>{formatPrice(product.fiyat)}</strong>
            <small> / {product.birim}</small>
          </div>
          <div className="product-card__actions">
            {product.stokta ? (
              <a
                className="product-card__order"
                href={orderUrl}
                target="_blank"
                rel="noopener noreferrer"
              >
                Sipariş
              </a>
            ) : (
              <span className="product-card__soldout">Stok yok</span>
            )}
            {isAdmin ? (
              <button className="product-card__edit" type="button" onClick={() => onEdit?.(product)}>
                Düzenle
              </button>
            ) : null}
          </div>
        </div>
      </div>
    </article>
  );
}
