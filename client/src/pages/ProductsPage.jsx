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
import { CategoryEditModal } from "../components/catalog/CategoryEditModal.jsx";
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
  const [editingCategory, setEditingCategory] = useState(null);
  const [addingNew, setAddingNew] = useState(false);
  const [addingCategory, setAddingCategory] = useState(false);
  const [page, setPage] = useState(1);

  const selectedCategory = searchParams.get("kat") || "";
  const featuredOnly = searchParams.get("one") === "1";

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

  const updateParams = useCallback(
    (patch) => {
      const next = new URLSearchParams(searchParams);
      Object.entries(patch).forEach(([key, value]) => {
        if (value === null || value === undefined || value === "" || value === false) {
          next.delete(key);
        } else {
          next.set(key, String(value));
        }
      });
      next.delete("page");
      setSearchParams(next, { replace: true });
      setPage(1);
    },
    [searchParams, setSearchParams]
  );

  const handleFilter = (value) => {
    setMenuOpen(false);
    if (value === "Tumu") {
      updateParams({ kat: null, one: null });
    } else if (value === "OneCikan") {
      updateParams({ one: "1", kat: null });
    } else {
      updateParams({ kat: value, one: null });
    }
  };

  const openAddCategory = () => {
    if (!isAdmin) {
      showToast("Kategori eklemek için admin girişi yapın.", "info");
      navigate("/giris?return=/");
      return;
    }
    setAddingCategory(true);
    setEditingCategory({});
  };

  const closeCategoryForm = () => {
    setEditingCategory(null);
    setAddingCategory(false);
  };

  const filteredProducts = useMemo(() => {
    let list = [...products];
    if (featuredOnly) list = list.filter((p) => p.oneCikan);
    else if (selectedCategory) list = list.filter((p) => p.kategori === selectedCategory);
    return list;
  }, [products, featuredOnly, selectedCategory]);

  const totalPages = Math.max(1, Math.ceil(filteredProducts.length / PAGE_SIZE));
  const safePage = Math.min(page, totalPages);
  const visible = useMemo(
    () => filteredProducts.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE),
    [filteredProducts, safePage]
  );

  return (
    <>
      <div className="site-shell">
        <Sidebar
          mode="products"
          selectedCategory={selectedCategory}
          featuredOnly={featuredOnly}
          onFilter={handleFilter}
          isOpen={menuOpen}
          isAdmin={isAdmin}
          onAddCategory={openAddCategory}
          onEditCategory={(cat) => {
            setAddingCategory(false);
            setEditingCategory(cat);
          }}
        />

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

              {!loading && !error && products.length > 0 && filteredProducts.length === 0 ? (
                <div className="empty-state admin-empty">
                  <h4>Bu kategoride ürün yok</h4>
                  <button className="back-button empty-state__cta" type="button" onClick={() => handleFilter("Tumu")}>
                    Tüm ürünlere dön
                  </button>
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
      {isAdmin && editingCategory !== null ? (
        <CategoryEditModal
          category={addingCategory ? {} : editingCategory}
          onClose={closeCategoryForm}
          onSaved={closeCategoryForm}
        />
      ) : null}
    </>
  );
}
