import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";
import { isAdminUser } from "../lib/auth.js";
import { createEmptyProduct } from "../lib/products.js";
import { applyPageSeo } from "../lib/seo.js";
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

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
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

  const openNewProduct = () => {
    setEditingProduct(createEmptyProduct(products));
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
                  <h1 id="productsPanelTitle">Ürün Vitrini</h1>
                  <p className="admin-panel__lead">
                    {isAdmin
                      ? "Buradan ürün ekleyip düzenlersin. Vitrin boş başlar — hepsini sen dolduracaksın."
                      : "Dükkan ürünleri burada listelenir."}
                  </p>
                </div>
                {isAdmin ? (
                  <button className="shop-hero__cta" type="button" onClick={openNewProduct}>
                    + Yeni Ürün Ekle
                  </button>
                ) : (
                  <Link className="shop-hero__ghost" to="/giris?return=/">
                    Admin girişi
                  </Link>
                )}
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
                  <p>
                    {isAdmin
                      ? "Yukarıdaki “Yeni Ürün Ekle” ile ilk ürününü oluştur."
                      : "Ürünler yakında eklenecek."}
                  </p>
                  {isAdmin ? (
                    <button className="back-button empty-state__cta" type="button" onClick={openNewProduct}>
                      İlk ürünü ekle
                    </button>
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
                        onEdit={setEditingProduct}
                      />
                    ))}
                  </div>
                  <Pagination
                    currentPage={safePage}
                    totalPages={totalPages}
                    onPageChange={setPage}
                  />
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
          isNew={!products.some((p) => Number(p.id) === Number(editingProduct.id))}
          onClose={() => setEditingProduct(null)}
          onSaved={loadProducts}
        />
      ) : null}
    </>
  );
}
