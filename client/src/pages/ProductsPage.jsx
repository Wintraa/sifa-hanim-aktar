import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { api } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";
import { isAdminUser } from "../lib/auth.js";
import { createEmptyProduct } from "../lib/products.js";
import { applyPageSeo } from "../lib/seo.js";
import { showToast } from "../lib/toast.js";
import { Sidebar } from "../components/layout/Sidebar.jsx";
import { Topbar } from "../components/layout/Topbar.jsx";
import { ProductCard } from "../components/catalog/ProductCard.jsx";
import { ProductEditModal } from "../components/catalog/ProductEditModal.jsx";
import { Pagination } from "../components/catalog/Pagination.jsx";
import { WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";
import { SHOP } from "../config/shop.js";

const PAGE_SIZE = 9;

export default function ProductsPage() {
  const { user } = useAuth();
  const isAdmin = isAdminUser(user);
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [addingNew, setAddingNew] = useState(false);
  const [page, setPage] = useState(1);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getProductsWithFallback();
      setProducts(data);
    } catch (err) {
      setError(err.message || "Ürünler yüklenemedi.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  useEffect(() => {
    applyPageSeo({
      title: `${SHOP.name} — Ürünler`,
      description: "Şifa Hanım Aktar ürün vitrini.",
      path: "/",
    });
  }, []);

  const openAddForm = useCallback(() => {
    if (!isAdmin) {
      showToast("Ürün eklemek için admin girişi yapın.", "info");
      navigate("/giris?return=/?add=1");
      return;
    }
    setAddingNew(true);
    setEditingProduct(createEmptyProduct(products));
  }, [isAdmin, navigate, products]);

  // Giriş sonrası ?add=1 ile formu otomatik aç
  useEffect(() => {
    if (!isAdmin || searchParams.get("add") !== "1") return;
    setAddingNew(true);
    setEditingProduct(createEmptyProduct(products));
    const next = new URLSearchParams(searchParams);
    next.delete("add");
    setSearchParams(next, { replace: true });
  }, [isAdmin, searchParams, setSearchParams, products]);

  const closeForm = () => {
    setEditingProduct(null);
    setAddingNew(false);
  };

  const totalPages = Math.max(1, Math.ceil(products.length / PAGE_SIZE));
  const safePage = Math.min(page, totalPages);
  const visible = useMemo(
    () => products.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE),
    [products, safePage]
  );

  return (
    <>
      <div className="site-shell">
        <Sidebar mode="products" onFilter={() => setMenuOpen(false)} isOpen={menuOpen} />

        <button
          type="button"
          className={`overlay${menuOpen ? " is-visible" : ""}`}
          aria-label="Menüyü kapat"
          onClick={() => setMenuOpen(false)}
        />

        <div className="main-panel">
          <Topbar
            catalogMode="products"
            searchValue=""
            onSearchChange={() => {}}
            onMenuToggle={() => setMenuOpen((v) => !v)}
            menuOpen={menuOpen}
            isAdmin={isAdmin}
          />

          <main className="content" id="main-content">
            <section className="admin-panel" aria-labelledby="productsPanelTitle">
              <div className="admin-panel__head">
                <div>
                  <p className="section-label">Şifa Hanım Aktar</p>
                  <h1 id="productsPanelTitle">Ürünler</h1>
                </div>
                <button className="add-product-btn" type="button" onClick={openAddForm}>
                  + Ürün Ekle
                </button>
              </div>

              {loading ? <p className="plants-section__intro">Yükleniyor…</p> : null}
              {error ? (
                <div className="empty-state">
                  <h4>Hata</h4>
                  <p>{error}</p>
                </div>
              ) : null}

              {!loading && !error && products.length === 0 ? (
                <div className="empty-state admin-empty">
                  <h4>Henüz ürün yok</h4>
                  <p>Ürünleri sen ekleyeceksin. Aşağıdaki butona bas, bilgileri gir, kaydet.</p>
                  <button className="add-product-btn add-product-btn--large" type="button" onClick={openAddForm}>
                    + Ürün Ekle
                  </button>
                  {!isAdmin ? (
                    <p className="admin-panel__hint">
                      Ürün eklemek için{" "}
                      <Link to="/giris?return=/?add=1">admin girişi</Link> yap.
                    </p>
                  ) : null}
                </div>
              ) : null}

              {!loading && !error && visible.length > 0 ? (
                <>
                  <div className="plants-grid products-grid" aria-live="polite">
                    {visible.map((product, index) => (
                      <ProductCard
                        key={product.id}
                        product={product}
                        visibleIndex={index}
                        isAdmin={isAdmin}
                        onEdit={(p) => {
                          setAddingNew(false);
                          setEditingProduct(p);
                        }}
                      />
                    ))}
                  </div>
                  <Pagination currentPage={safePage} totalPages={totalPages} onPageChange={setPage} />
                </>
              ) : null}
            </section>
          </main>
        </div>
      </div>

      <WhatsAppFloatButton />

      {isAdmin && editingProduct ? (
        <ProductEditModal
          product={editingProduct}
          isNew={addingNew}
          onClose={closeForm}
          onSaved={() => {
            loadProducts();
            closeForm();
          }}
        />
      ) : null}
    </>
  );
}
