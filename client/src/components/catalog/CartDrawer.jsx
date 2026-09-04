import { useEffect } from "react";
import { Link } from "react-router-dom";
import { CartPanel } from "./CartPanel.jsx";
import { useCart } from "../../context/CartContext.jsx";

/** Sağdan açılan sepet paneli — toplu WhatsApp bilgi sorusu. */
export function CartDrawer() {
  const { isOpen, closeCart, itemCount } = useCart();

  useEffect(() => {
    document.body.classList.toggle("cart-open", isOpen);
    return () => document.body.classList.remove("cart-open");
  }, [isOpen]);

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") closeCart();
    };
    if (isOpen) window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isOpen, closeCart]);

  if (!isOpen) return null;

  return (
    <>
      <button type="button" className="cart-drawer__backdrop" aria-label="Sepeti kapat" onClick={closeCart} />
      <aside className="cart-drawer" aria-label="Alışveriş sepeti" role="dialog" aria-modal="true">
        <header className="cart-drawer__head">
          <div>
            <h2>Sepetim</h2>
            <p>{itemCount > 0 ? `${itemCount} ürün` : "Sepetin boş"}</p>
          </div>
          <button type="button" className="modal-card__close" onClick={closeCart} aria-label="Kapat">
            ×
          </button>
        </header>

        <CartPanel onContinue={closeCart} />

        {itemCount > 0 ? (
          <p className="cart-drawer__page-link">
            <Link to="/sepet" onClick={closeCart}>
              Sepet sayfasını aç
            </Link>
          </p>
        ) : null}
      </aside>
    </>
  );
}
