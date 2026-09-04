import { Link, useNavigate } from "react-router-dom";
import { CartPanel } from "../components/catalog/CartPanel.jsx";
import { useCart } from "../context/CartContext.jsx";

export default function CartPage() {
  const { itemCount, closeCart, lineCount } = useCart();
  const navigate = useNavigate();

  return (
    <main className="detail-main cart-page" id="main-content">
      <header className="detail-header cart-page__header">
        <Link className="back-button" to="/" onClick={closeCart}>
          ← Ürünlere dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">Sipariş</p>
          <h1>Sepetim</h1>
          <p className="cart-page__meta">
            {itemCount > 0
              ? `${lineCount} çeşit · ${itemCount} adet — toplu fiyat için WhatsApp`
              : "Sepetin boş — vitrinden ürün ekle"}
          </p>
        </div>
      </header>

      <section className="cart-page__panel" aria-label="Alışveriş sepeti">
        <CartPanel onContinue={() => navigate("/")} />
      </section>
    </main>
  );
}
