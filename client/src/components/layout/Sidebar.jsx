import { useCallback, useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { getProductCategories, CATEGORIES_CHANGED } from "../../lib/product-categories.js";

const PLANT_FILTERS = [
  { value: "Tumu", label: "Tüm Bitkiler" },
  {
    value: "Tıbbi Bitkiler",
    label: "Tıbbi Bitkiler",
    title: "Yüzyıllardır kullanılan şifalı bitkiler ve faydaları.",
  },
  { value: "Süs Bitkileri", label: "Süs Bitkileri" },
  { value: "Aromatik Bitkiler", label: "Aromatik Bitkiler" },
  { value: "Favoriler", label: "Favorilerim", id: "favoritesFilterButton" },
];

export function Sidebar({
  mode = "products",
  selectedTypes = [],
  selectedCategory = "",
  favoritesOnly = false,
  featuredOnly = false,
  onFilter = () => {},
  favoriteCount = 0,
  isOpen,
  isAdmin = false,
  onAddCategory,
  onEditCategory,
}) {
  const location = useLocation();
  const isProducts = mode === "products";
  const [categories, setCategories] = useState(() => getProductCategories());

  const reloadCategories = useCallback(() => {
    setCategories(getProductCategories());
  }, []);

  useEffect(() => {
    reloadCategories();
    window.addEventListener(CATEGORIES_CHANGED, reloadCategories);
    return () => window.removeEventListener(CATEGORIES_CHANGED, reloadCategories);
  }, [reloadCategories]);

  const isPlantActive = (value) => {
    if (value === "Tumu") return !favoritesOnly && selectedTypes.length === 0;
    if (value === "Favoriler") return favoritesOnly;
    return selectedTypes.includes(value);
  };

  const isProductActive = (value) => {
    if (value === "Tumu") return !featuredOnly && !selectedCategory;
    if (value === "OneCikan") return featuredOnly;
    return selectedCategory === value;
  };

  const favLabel =
    favoriteCount > 0 ? `Favorilerim (${favoriteCount})` : "Favorilerim";

  return (
    <aside className={`sidebar${isOpen ? " is-open" : ""}`} id="sidebar">
      <div className="sidebar__brand">
        <span className="sidebar__eyebrow">Şifa Hanım Aktar</span>
        <h2>{isProducts ? "Ürünler" : "Bitki Kütüphanesi"}</h2>
        <p>
          {isProducts
            ? "Sol menüden kategori seç; admin olarak kendi kategorilerini ekleyebilirsin."
            : "Şifalı otların ne işe yaradığını, nasıl kullanıldığını keşfedin."}
        </p>
      </div>

      <nav className="sidebar__mode-nav" aria-label="Ana bölümler">
        <Link
          to="/"
          className={`sidebar__mode-link${location.pathname === "/" ? " is-active" : ""}`}
        >
          Ürünler
        </Link>
        <Link
          to="/bitkiler"
          className={`sidebar__mode-link${
            location.pathname.startsWith("/bitkiler") || location.pathname.startsWith("/bitki/")
              ? " is-active"
              : ""
          }`}
        >
          Bitkiler
        </Link>
      </nav>

      <nav
        className="sidebar__nav"
        aria-label={isProducts ? "Ürün kategorileri" : "Bitki filtreleri"}
        id="sidebarFilters"
      >
        {isProducts ? (
          <>
            <button
              type="button"
              className={`filter-button${isProductActive("Tumu") ? " is-active" : ""}`}
              aria-pressed={isProductActive("Tumu")}
              onClick={() => onFilter("Tumu")}
            >
              Tüm Ürünler
            </button>
            <button
              type="button"
              className={`filter-button${isProductActive("OneCikan") ? " is-active" : ""}`}
              id="featuredFilterButton"
              aria-pressed={isProductActive("OneCikan")}
              onClick={() => onFilter("OneCikan")}
            >
              Öne Çıkanlar
            </button>
            {categories.length === 0 ? (
              <p className="sidebar__empty-cat">
                {isAdmin ? "Henüz kategori yok — aşağıdan ekle." : "Kategoriler yakında."}
              </p>
            ) : (
              categories.map((cat) => (
                <div key={cat.id} className="sidebar__cat-row">
                  <button
                    type="button"
                    className={`filter-button sidebar__cat-btn${
                      isProductActive(cat.ad) ? " is-active" : ""
                    }`}
                    aria-pressed={isProductActive(cat.ad)}
                    onClick={() => onFilter(cat.ad)}
                  >
                    {cat.ad}
                  </button>
                  {isAdmin ? (
                    <button
                      type="button"
                      className="sidebar__cat-edit"
                      aria-label={`${cat.ad} düzenle`}
                      title="Düzenle"
                      onClick={() => onEditCategory?.(cat)}
                    >
                      ✎
                    </button>
                  ) : null}
                </div>
              ))
            )}
            {isAdmin ? (
              <button type="button" className="filter-button sidebar__add-cat" onClick={onAddCategory}>
                + Kategori Ekle
              </button>
            ) : null}
          </>
        ) : (
          PLANT_FILTERS.map((item) => (
            <button
              key={item.value}
              className={`filter-button${isPlantActive(item.value) ? " is-active" : ""}`}
              data-filter={item.value}
              type="button"
              id={item.id}
              title={item.title}
              aria-pressed={isPlantActive(item.value)}
              onClick={() => onFilter(item.value)}
            >
              {item.value === "Favoriler" ? favLabel : item.label}
            </button>
          ))
        )}
      </nav>

      <div className="sidebar__contact">
        <Link className="filter-button sidebar__contact-link" to="/iletisim">
          İletişim &amp; WhatsApp
        </Link>
      </div>

      <footer className="sidebar__footer">
        <p>Şifa Hanım Aktar — Çan / Çanakkale.</p>
      </footer>
    </aside>
  );
}
