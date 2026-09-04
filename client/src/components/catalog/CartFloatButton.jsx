import { useNavigate } from "react-router-dom";
import { useCart } from "../../context/CartContext.jsx";

/** Sabit sepet kısayolu — sepet sayfasına gider. */
export function CartFloatButton() {
  const { itemCount, closeCart } = useCart();
  const navigate = useNavigate();

  return (
    <button
      type="button"
      className="cart-float"
      onClick={() => {
        closeCart();
        navigate("/sepet");
      }}
      aria-label={itemCount > 0 ? `Sepetim, ${itemCount} ürün` : "Sepetim"}
      title="Sepetim"
    >
      <span className="cart-float__label">Sepet</span>
      {itemCount > 0 ? <span className="cart-float__badge">{itemCount}</span> : null}
    </button>
  );
}
