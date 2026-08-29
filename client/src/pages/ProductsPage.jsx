import { useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { api } from "../services/api.js";
import { useAuth } from "../context/AuthContext.jsx";
import { isAdminUser } from "../lib/auth.js";
import { applyPageSeo } from "../lib/seo.js";
import { Sidebar } from "../components/layout/Sidebar.jsx";
import { Topbar } from "../components/layout/Topbar.jsx";
import { ProductCard } from "../components/catalog/ProductCard.jsx";
import { ProductEditModal } from "../components/catalog/ProductEditModal.jsx";
import { Pagination } from "../components/catalog/Pagination.jsx";
import { ShopContactCards, WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";
import { SHOP } from "../config/shop.js";
import { whatsappUrl } from "../lib/whatsapp.js";

const PAGE_SIZE = 9;

export default function ProductsPage() {
  const { user } = useAuth();
  const isAdmin = isAdminUser(user);
  const [searchParams, setSearchParams] = useSearchParams();

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchInput, setSearchInput] = useState(searchParams.get("q") || "");
  const [editingProduct, setEditingProduct] = useState(null);

  const selectedCategory = searchParams.get("kat") || "";
  const featuredOnly = searchParams.get("one") === "1";
  const searchQuery = (searchParams.get("q") || "").trim().toLocaleLowerCase("tr");
  const currentPage = Math.max(1, Number(searchParams.get("page")) || 1);

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
      title: `${SHOP.name} — Doğal Ürünler & Aktar`,
      description:
        "Şifa Hanım Aktar dükkan vitrini: sıcak çaylar, baharatlar, bitkisel yağlar ve özel karışımlar. Çan / Çanakkale.",
      path: "/",
    });
  }, []);

  const updateParams = useCallback(
    (patch, { resetPage = true } = {}) => {
      const next = new URLSearchParams(searchParams);
      Object.entries(patch).forEach(([key, value]) => {
        if (value === null || value === undefined || value === "" || value === false) {
          next.delete(key);
        } else {
          next.set(key, String(value));
        }
      });
      if (resetPage) next.delete("page");
      setSearchParams(next, { replace: true });
    },
    [searchParams, setSearchParams]
  );

  const handleFilter = (value) => {
    if (value === "Tumu") {
      updateParams({ kat: null, one: null });
    } else if (value === "OneCikan") {
      updateParams({ one: "1", kat: null });
    } else {
      updateParams({ kat: value, one: null });
    }
    setMenuOpen(false);
  };

  const handleSearchChange = (value) => {
    setSearchInput(value);
    updateParams({ q: value.trim() || null });
  };

  const filtered = useMemo(() => {
    let list = [...products];
    if (featuredOnly) list = list.filter((p) => p.oneCikan);
    else if (selectedCategory) list = list.filter((p) => p.kategori === selectedCategory);
    if (searchQuery) {
      list = list.filter((p) => {
        const hay = `${p.ad} ${p.kisaAciklama} ${p.kategori} ${(p.etiketler || []).join(" ")}`.toLocaleLowerCase("tr");
        return hay.includes(searchQuery);
      });
    }
    return list;
  }, [products, featuredOnly, selectedCategory, searchQuery]);

  const featured = useMemo(() => products.filter((p) => p.oneCikan).slice(0, 6), [products]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const safePage = Math.min(currentPage, totalPages);
  const visible = filtered.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE);

  return (
    <>
      <div className="site-shell">
        <Sidebar
          mode="products"
          selectedCategory={selectedCategory}
          featuredOnly={featuredOnly}
          onFilter={handleFilter}
          isOpen={menuOpen}
        />

        <button
          type="button"
          className={`overlay${menuOpen ? " is-visible" : ""}`}
          aria-label="Menüyü kapat"
          aria-hidden={!menuOpen}
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
          />

          <main className="content" id="main-content">
            <section className="shop-hero" aria-labelledby="shopHeroTitle">
              <div className="shop-hero__copy">
                <p className="section-label">Şifa Hanım Aktar • Doğal Ürünler</p>
                <h1 id="shopHeroTitle">Dükkandan Sofranıza, Doğanın En Saf Haliyle.</h1>
                <p className="shop-hero__text">
                  Çan’daki dükkanımızda yıllardır seçtiğimiz kurutulmuş otlar, çay karışımları, baharatlar ve
                  bitkisel yağlar — şimdi online vitrinde. WhatsApp ile sipariş, kapıda güven.
                </p>
                <div className="shop-hero__actions">
                  <a className="shop-hero__cta" href={whatsappUrl(SHOP.whatsappMessages.order)}>
                    WhatsApp Sipariş
                  </a>
                  <Link className="shop-hero__ghost" to="/bitkiler">
                    Bitki kütüphanesine geç
                  </Link>
                </div>
              </div>
              <div className="shop-hero__stats">
                <div className="shop-stat">
                  <strong>{loading ? "…" : products.length}</strong>
                  <span>ürün</span>
                </div>
                <div className="shop-stat">
                  <strong>100%</strong>
                  <span>doğal</span>
                </div>
                <div className="shop-stat">
                  <strong>Çan</strong>
                  <span>yerel aktar</span>
                </div>
              </div>
            </section>

            <section className="trust-strip" aria-label="Güven rozetleri">
              <span>🌿 El ayıklı kurutulmuş ot</span>
              <span>📦 WhatsApp ile hızlı sipariş</span>
              <span>🏪 Çan / Çanakkale dükkan</span>
              <span>☕ Uzman aktar tavsiyesi</span>
            </section>

            {!loading && featured.length > 0 && !selectedCategory && !searchQuery && !featuredOnly ? (
              <section className="featured-rail" aria-labelledby="featuredTitle">
                <div className="plants-section__header">
                  <div>
                    <p className="section-label">Vitrin</p>
                    <h2 id="featuredTitle">Öne çıkan ürünler</h2>
                  </div>
                </div>
                <div className="featured-rail__grid">
                  {featured.map((product, index) => (
                    <ProductCard
                      key={product.id}
                      product={product}
                      visibleIndex={index}
                      isAdmin={isAdmin}
                      onEdit={setEditingProduct}
                    />
                  ))}
                </div>
              </section>
            ) : null}

            <section className="plants-section products-section" aria-labelledby="productsTitle">
              <div className="plants-section__header">
                <div>
                  <p className="section-label">Katalog</p>
                  <h2 id="productsTitle">Tüm ürünler</h2>
                </div>
                <p className="plants-section__meta">
                  {featuredOnly
                    ? "Öne çıkanlar"
                    : selectedCategory || searchQuery
                      ? [selectedCategory, searchQuery && `Arama: “${searchInput.trim()}”`]
                          .filter(Boolean)
                          .join(" · ")
                      : "Tüm ürünler"}
                </p>
              </div>

              {loading ? <p className="plants-section__intro">Ürünler yükleniyor…</p> : null}
              {error ? (
                <div className="empty-state">
                  <h4>Veri yüklenemedi</h4>
                  <p>{error}</p>
                </div>
              ) : null}

              {!loading && !error && filtered.length === 0 ? (
                <div className="empty-state">
                  <h4>Ürün bulunamadı</h4>
                  <p>Farklı bir kategori deneyin veya WhatsApp’tan sorun.</p>
                  <button className="back-button empty-state__cta" type="button" onClick={() => handleFilter("Tumu")}>
                    Tüm ürünlere dön
                  </button>
                </div>
              ) : null}

              {!loading && !error && visible.length > 0 ? (
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
              ) : null}

              {!loading && !error ? (
                <Pagination
                  currentPage={safePage}
                  totalPages={totalPages}
                  onPageChange={(page) =>
                    updateParams({ page: page > 1 ? page : null }, { resetPage: false })
                  }
                />
              ) : null}
            </section>

            <footer className="site-footer" aria-label="Site bilgisi">
              <div className="site-footer__grid">
                <div>
                  <p>
                    <strong>{SHOP.name}</strong> — {SHOP.address}. Bilgiler bilgilendirme amaçlıdır.
                  </p>
                  <p className="site-footer__link-row">
                    <Link to="/bitkiler">Bitki kütüphanesi</Link>
                    {" · "}
                    <Link to="/iletisim">İletişim</Link>
                  </p>
                </div>
                <ShopContactCards compact />
              </div>
            </footer>
          </main>
        </div>
      </div>

      <WhatsAppFloatButton />
      {isAdmin && editingProduct ? (
        <ProductEditModal
          product={editingProduct}
          onClose={() => setEditingProduct(null)}
          onSaved={loadProducts}
        />
      ) : null}
    </>
  );
}
