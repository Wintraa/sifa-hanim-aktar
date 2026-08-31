import { useEffect, useState } from "react";
import { productImageUrl } from "../../lib/assetUrl.js";

/** Ürün görseli — kadrajı bulanık dolgu ile doldurur, ürünü kırpmaz. */
export function ProductImage({ src, alt, className, width, height, loading, decoding }) {
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    setFailed(false);
  }, [src]);

  const url = failed ? "/assets/product-placeholder.svg" : productImageUrl(src);

  return (
    <span className={`product-photo${className ? ` ${className}` : ""}`}>
      <span
        className="product-photo__fill"
        style={{ backgroundImage: `url(${JSON.stringify(url)})` }}
        aria-hidden="true"
      />
      <span className="product-photo__wash" aria-hidden="true" />
      <img
        className="product-photo__img"
        src={url}
        alt={alt}
        width={width}
        height={height}
        loading={loading}
        decoding={decoding}
        onError={() => setFailed(true)}
      />
    </span>
  );
}
