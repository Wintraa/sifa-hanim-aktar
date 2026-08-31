import { Link } from "react-router-dom";
import { recordProductClick } from "../../lib/product-clicks.js";
import { ProductContactLinks } from "./ProductContactLinks.jsx";
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

  return (
    <article
      className={`product-card${inVitrin ? " product-card--featured" : ""}${!product.stokta ? " product-card--soldout" : ""}${isAdmin ? " product-card--admin" : ""}`}
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
            width="150"
            height="150"
            loading={visibleIndex < 6 ? "eager" : "lazy"}
            decoding="async"
          />
        </Link>
        {isAdmin ? (
          <AdminProductImageControls
            isAdmin
            overlay
            showPreview={false}
            imageUrl={product.resimUrl}
            onImageChange={(url) => onImageChange?.({ ...product, resimUrl: url })}
          />
        ) : null}
        {product.oneCikan ? (
          <span className="product-card__ribbon">Öne Çıkan</span>
        ) : inVitrin ? (
          <span className="product-card__ribbon">Popüler</span>
        ) : null}
        {!product.stokta ? (
          <span className="product-card__ribbon product-card__ribbon--muted product-card__ribbon--right">Tükendi</span>
        ) : null}
      </div>

      <div className="product-card__content">
        <span className="product-card__category">{product.kategori}</span>
        <h4 className="product-card__title">
          <Link to={detailHref} onClick={trackClick}>
            {product.ad}
          </Link>
        </h4>
        {product.birim && product.birim !== "adet" ? (
          <p className="product-card__unit">{product.birim}</p>
        ) : null}
        <div className="product-card__footer">
          {product.stokta ? (
            <ProductContactLinks productName={product.ad} birim={product.birim} card />
          ) : (
            <span className="product-card__soldout">Stokta yok — bilgi için yazın</span>
          )}
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
