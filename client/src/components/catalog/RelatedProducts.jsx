import { Link } from "react-router-dom";
import { ProductImage } from "./ProductImage.jsx";

export function RelatedProducts({ products, currentId, title = "Benzer ürünler" }) {
  const related = products
    .filter((p) => Number(p.id) !== Number(currentId) && p.stokta !== false)
    .slice(0, 3);

  if (!related.length) return null;

  return (
    <section className="related-products" aria-labelledby="relatedProductsTitle">
      <h2 id="relatedProductsTitle">{title}</h2>
      <div className="related-products__grid">
        {related.map((product) => (
          <Link key={product.id} className="related-products__card" to={`/urun/${product.id}`}>
            <ProductImage
              className="related-products__img"
              src={product.resimUrl}
              alt={product.ad}
              width="320"
              height="240"
              loading="lazy"
            />
            <span className="related-products__cat">{product.kategori}</span>
            <strong className="related-products__name">{product.ad}</strong>
          </Link>
        ))}
      </div>
    </section>
  );
}
