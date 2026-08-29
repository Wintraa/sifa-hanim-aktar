import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { api } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";
import { isAdminUser } from "../lib/auth.js";
import { createEmptyProduct, getFeaturedProducts } from "../lib/products.js";
import { getTopClickedProducts, isInVitrin } from "../lib/product-clicks.js";
import { debounce } from "../lib/utils.js";
import { applyPageSeo } from "../lib/seo.js";
import { showToast } from "../lib/toast.js";
import { Sidebar } from "../components/layout/Sidebar.jsx";
import { Topbar } from "../components/layout/Topbar.jsx";
import { ProductCard } from "../components/catalog/ProductCard.jsx";
import { ProductEditModal } from "../components/catalog/ProductEditModal.jsx";
import { CategoryEditModal } from "../components/catalog/CategoryEditModal.jsx";
import { Pagination } from "../components/catalog/Pagination.jsx";
import { WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";
import { ShopHero, ShopTrustStrip } from "../components/catalog/ShopHero.jsx";
import { SHOP } from "../config/shop.js";
import { whatsappUrl } from "../lib/whatsapp.js";
import { loadBaseCategories, notifyCategoriesChanged } from "../lib/product-categories.js";

const PAGE_SIZE = 9;

function productMatchesSearch(product, query) {
  if (!query) return true;
  const hay = [
    product.ad,
    product.kategori,
    product.kisaAciklama,
    product.aciklama,
    ...(product.etiketler || []),
  ]
    .join(" ")
    .toLocaleLowerCase("tr");
  return hay.includes(query);
}

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
  const [searchInput, setSearchInput] = useState(() => searchParams.get("q") || "");

  const selectedCategory = searchParams.get("kat") || "";
  const featuredOnly = searchParams.get("one") === "1";
  const searchQuery = (searchParams.get("q") || "").trim().toLocaleLowerCase("tr");

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
    loadBaseCategories().then(() => notifyCategoriesChanged());
  }, []);

  useEffect(() => {
    applyPageSeo({
      title: `${SHOP.name} — Ürünler`,
      description: "Şifa Hanım Aktar ürün vitrini.",
      path: "/",
    });
  }, []);

  useEffect(() => {
    setSearchInput(searchParams.get("q") || "");
  }, [searchParams]);

  useEffect(() => {
    const onKey = (e) => {
      const tag = e.target?.tagName;
      if (e.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") {
        e.preventDefault();
        document.querySelector("#searchInput")?.focus();
      }
      if (e.key === "Escape") {
        document.querySelector("#searchInput")?.blur();
        setMenuOpen(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  useEffect(() => {
    document.body.classList.toggle("has-open-menu", menuOpen);
    return () => document.body.classList.remove("has-open-menu");
  }, [menuOpen]);

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

  const debouncedSearch = useMemo(
    () =>
      debounce((value) => {
        updateParams({ q: value.trim() || null });
      }, 180),
    [updateParams]
  );

  const handleSearchChange = (value) => {
    setSearchInput(value);
    debouncedSearch(value);
  };

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
    if (featuredOnly) {
      list = getFeaturedProducts(list);
    } else if (selectedCategory) {
      list = list.filter((p) => p.kategori === selectedCategory);
    }
    if (searchQuery) {
      list = list.filter((p) => productMatchesSearch(p, searchQuery));
    }
    return list;
  }, [products, featuredOnly, selectedCategory, searchQuery]);

  const showFeaturedRail =
    !loading &&
    !error &&
    products.length > 0 &&
    !searchQuery &&
    !selectedCategory &&
    !featuredOnly;

  const featuredProducts = useMemo(() => {
    if (!showFeaturedRail) return [];
    const manual = getFeaturedProducts(products);
    if (manual.length) return manual.slice(0, 3);
    return getTopClickedProducts(products).slice(0, 3);
  }, [showFeaturedRail, products]);

  const featuredRailUsesClicks =
    showFeaturedRail && getFeaturedProducts(products).length === 0 && featuredProducts.length > 0;

  const resultsLabel = useMemo(() => {
    if (loading || error) return "";
    const n = filteredProducts.length;
    if (searchQuery) return `"${searchParams.get("q")}" için ${n} sonuç`;
    if (featuredOnly) return `Öne çıkan · ${n} ürün`;
    if (selectedCategory) return `${selectedCategory} · ${n} ürün`;
    return `${n} ürün listeleniyor`;
  }, [loading, error, filteredProducts.length, searchQuery, featuredOnly, selectedCategory, searchParams]);

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
            searchValue={searchInput}
            onSearchChange={handleSearchChange}
            onMenuToggle={() => setMenuOpen((v) => !v)}
            menuOpen={menuOpen}
            isAdmin={isAdmin}
            onFavoritesClick={() => navigate("/bitkiler?fav=1")}
          />

          <main className="content" id="main-content">
            <section className="admin-panel shop-page" aria-labelledby="productsPanelTitle">
              {!loading && !error && products.length > 0 ? (
                <>
                  <ShopHero productCount={products.length} />
                  <ShopTrustStrip />
                </>
              ) : (
                <div className="admin-panel__head">
                  <div>
                    <p className="section-label">Şifa Hanım Aktar</p>
                    <h1 id="productsPanelTitle">Ürünler</h1>
                  </div>
                </div>
              )}

              <div className="shop-page__toolbar">
                {resultsLabel ? <p className="shop-page__results">{resultsLabel}</p> : null}
                {isAdmin ? (
                  <button className="add-product-btn" type="button" onClick={openAddForm}>
                    + Ürün Ekle
                  </button>
                ) : null}
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
                  {isAdmin ? (
                    <>
                      <p>Ürünleri sen ekleyeceksin. Aşağıdaki butona bas, bilgileri gir, kaydet.</p>
                      <button className="add-product-btn add-product-btn--large" type="button" onClick={openAddForm}>
                        + Ürün Ekle
                      </button>
                    </>
                  ) : (
                    <p>Yakında yeni ürünler eklenecek. Sipariş için WhatsApp’tan yazabilirsin.</p>
                  )}
                </div>
              ) : null}

              {!loading && !error && products.length > 0 && filteredProducts.length === 0 ? (
                <div className="empty-state admin-empty">
                  <h4>
                    {searchQuery
                      ? `"${searchParams.get("q")}" için sonuç yok`
                      : featuredOnly
                        ? "Henüz öne çıkan ürün yok"
                        : "Bu kategoride ürün yok"}
                  </h4>
                  <p>
                    {searchQuery
                      ? "Farklı bir kelime dene veya aramayı temizle."
                      : featuredOnly
                        ? isAdmin
                          ? "Ürün düzenleme ekranında «Öne çıkan» kutusunu işaretleyip kaydedin."
                          : "Yakında öne çıkan ürünler eklenecek."
                        : null}
                  </p>
                  <button
                    className="back-button empty-state__cta"
                    type="button"
                    onClick={() =>
                      searchQuery ? handleSearchChange("") : handleFilter("Tumu")
                    }
                  >
                    {searchQuery ? "Aramayı temizle" : "Tüm ürünlere dön"}
                  </button>
                </div>
              ) : null}

              {!loading && !error && featuredProducts.length > 0 ? (
                <section className="featured-rail" aria-labelledby="featuredRailTitle">
                  <div className="featured-rail__head">
                    <h2 id="featuredRailTitle">
                      {featuredRailUsesClicks ? "Çok tıklananlar" : "Öne çıkanlar"}
                    </h2>
                    <p>
                      {featuredRailUsesClicks
                        ? "En çok ilgi gören ürünler — hızlı sipariş için tıklayın."
                        : "Dükkanın seçtiği ürünler — hızlı sipariş için tıklayın."}
                    </p>
                  </div>
                  <div className="featured-rail__grid">
                    {featuredProducts.map((product, index) => (
                      <ProductCard
                        key={product.id}
                        product={product}
                        visibleIndex={index}
                        isAdmin={isAdmin}
                        inVitrin
                        onEdit={(p) => {
                          setAddingNew(false);
                          setEditingProduct(p);
                        }}
                      />
                    ))}
                  </div>
                </section>
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
                        inVitrin={Boolean(product.oneCikan) || isInVitrin(product.id, products)}
                        onEdit={(p) => {
                          setAddingNew(false);
                          setEditingProduct(p);
                        }}
                      />
                    ))}
                  </div>
                  <div className="shop-page__cta">
                    <div>
                      <h2>Sipariş için bir mesaj yeter</h2>
                      <p>
                        Fiyat, stok ve teslimat bilgisi için WhatsApp üzerinden yazın — genelde birkaç
                        dakika içinde dönüş yapılır.
                      </p>
                    </div>
                    <a
                      className="shop-page__cta-btn"
                      href={whatsappUrl(SHOP.whatsappMessages.order)}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      WhatsApp ile Sipariş Ver
                    </a>
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
