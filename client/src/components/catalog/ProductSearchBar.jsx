/** Ürünler vitrini için büyük, görünür arama alanı. */
export function ProductSearchBar({
  value = "",
  onChange,
  onClear,
  resultCount = null,
  placeholder = "Ürün, kategori veya içerik ara…",
}) {
  const hasQuery = String(value || "").trim().length > 0;

  return (
    <section className="product-search" aria-label="Ürün arama">
      <div className="product-search__inner">
        <label className="product-search__label" htmlFor="productSearchInput">
          Ürün ara
        </label>
        <div className="product-search__field">
          <span className="product-search__icon" aria-hidden="true">
            ⌕
          </span>
          <input
            id="productSearchInput"
            className="product-search__input"
            type="search"
            name="product-q"
            placeholder={placeholder}
            autoComplete="off"
            enterKeyHint="search"
            value={value}
            onChange={(e) => onChange?.(e.target.value)}
          />
          {hasQuery ? (
            <button
              type="button"
              className="product-search__clear"
              onClick={() => onClear?.()}
              aria-label="Aramayı temizle"
            >
              Temizle
            </button>
          ) : null}
        </div>
        {hasQuery && resultCount !== null ? (
          <p className="product-search__meta" aria-live="polite">
            {resultCount === 0
              ? `"${value.trim()}" için sonuç bulunamadı`
              : `${resultCount} ürün bulundu`}
          </p>
        ) : (
          <p className="product-search__hint">İhlamur, krem, baharat, macun… yazmaya başla</p>
        )}
      </div>
    </section>
  );
}
