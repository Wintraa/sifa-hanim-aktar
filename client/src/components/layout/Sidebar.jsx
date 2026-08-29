import { Link, useLocation } from "react-router-dom";

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

const PRODUCT_CATEGORIES = [
  { value: "Tumu", label: "Tüm Ürünler" },
  { value: "Sıcak Çaylar", label: "Sıcak Çaylar" },
  { value: "Soğuk Bitki Demlemeleri", label: "Soğuk Demlemeler" },
  { value: "Baharat & Harc", label: "Baharat & Harc" },
  { value: "Bitkisel Yağlar", label: "Bitkisel Yağlar" },
  { value: "Aktar Karışımları", label: "Aktar Karışımları" },
  { value: "Kurutulmuş Otlar", label: "Kurutulmuş Otlar" },
  { value: "OneCikan", label: "Öne Çıkanlar", id: "featuredFilterButton" },
];

export function Sidebar({
  mode = "products",
  selectedTypes = [],
  selectedCategory = "",
  favoritesOnly = false,
  featuredOnly = false,
  onFilter,
  favoriteCount = 0,
  isOpen,
}) {
  const location = useLocation();
  const isProducts = mode === "products";

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
        <h2>{isProducts ? "Dükkan" : "Bitki Kütüphanesi"}</h2>
        <p>
          {isProducts
            ? "Doğal ürünler, çaylar, baharatlar ve aktar karışımları — Çan’daki dükkanımızın vitrini."
            : "Şifalı otların ne işe yaradığını, nasıl kullanıldığını ve nelere dikkat edileceğini keşfedin."}
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
        {isProducts
          ? PRODUCT_CATEGORIES.map((item) => (
              <button
                key={item.value}
                className={`filter-button${isProductActive(item.value) ? " is-active" : ""}`}
                type="button"
                id={item.id}
                aria-pressed={isProductActive(item.value)}
                onClick={() => onFilter(item.value)}
              >
                {item.label}
              </button>
            ))
          : PLANT_FILTERS.map((item) => (
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
            ))}
      </nav>

      <div className="sidebar__contact">
        <Link className="filter-button sidebar__contact-link" to="/iletisim">
          İletişim &amp; WhatsApp
        </Link>
      </div>

      <footer className="sidebar__footer">
        <p>
          Şifa Hanım Aktar — Çan / Çanakkale. Bilgiler bilgilendirme amaçlıdır; tedavi yerine geçmez.
        </p>
      </footer>
    </aside>
  );
}
