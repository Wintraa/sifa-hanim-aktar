import { useEffect, useState } from "react";
import { productImageUrl } from "../../lib/assetUrl.js";

/** Ürün görseli — yüklenemezse placeholder. */
export function ProductImage({ src, alt, className, width, height, loading, decoding }) {
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    setFailed(false);
  }, [src]);

  const url = failed ? "/assets/product-placeholder.svg" : productImageUrl(src);

  return (
    <img
      className={className}
      src={url}
      alt={alt}
      width={width}
      height={height}
      loading={loading}
      decoding={decoding}
      onError={() => setFailed(true)}
    />
  );
}
