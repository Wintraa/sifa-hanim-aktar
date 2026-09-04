import { useCart } from "../../context/CartContext.jsx";

/** Ürün kartı / detay sayfası sepete ekle butonu. */
export function AddToCartButton({ product, className = "", compact = false, stopPropagation = false }) {
  const { addItem, isInCart } = useCart();
  const inCart = isInCart(product?.id);

  const handleClick = (e) => {
    if (stopPropagation) {
      e.preventDefault();
      e.stopPropagation();
    }
    if (product) addItem(product, 1);
  };

  const cls = [
    "add-to-cart-btn",
    compact ? "add-to-cart-btn--compact" : "",
    inCart ? "add-to-cart-btn--in-cart" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button type="button" className={cls} onClick={handleClick} aria-pressed={inCart}>
      {inCart ? "Sepette ✓" : compact ? "+ Sepet" : "Sepete Ekle"}
    </button>
  );
}
