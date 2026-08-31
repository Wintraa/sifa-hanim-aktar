/** Ürün listesi yüklenirken gösterilen iskelet grid. */
export function ProductGridSkeleton({ count = 12 }) {
  return (
    <div className="plants-grid products-grid product-grid-skeleton" aria-hidden="true">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="product-card product-card--skeleton">
          <div className="product-card__media skeleton-block" />
          <div className="product-card__content">
            <div className="skeleton-line skeleton-line--short" />
            <div className="skeleton-line" />
            <div className="skeleton-line skeleton-line--btn" />
          </div>
        </div>
      ))}
    </div>
  );
}
