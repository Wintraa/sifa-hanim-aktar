import { Link } from "react-router-dom";

const FILTERS = [
  { value: "Tumu", label: "Tüm Bitkiler" },
  {
    value: "Tıbbi Bitkiler",
    label: "Tıbbi Bitkiler",
    title:
      "Şifa Hanım Aktar'ın özel seçkisiyle, yüzyıllardır kullanılan şifalı bitkiler ve faydaları.",
  },
  { value: "Süs Bitkileri", label: "Süs Bitkileri" },
  { value: "Aromatik Bitkiler", label: "Aromatik Bitkiler" },
  { value: "Favoriler", label: "Favorilerim", id: "favoritesFilterButton" },
];

export function Sidebar({
  selectedTypes,
  favoritesOnly,
  onFilter,
  favoriteCount,
  isOpen,
}) {
  const isActive = (value) => {
    if (value === "Tumu") return !favoritesOnly && selectedTypes.length === 0;
    if (value === "Favoriler") return favoritesOnly;
    return selectedTypes.includes(value);
  };

  const favLabel =
    favoriteCount > 0 ? `Favorilerim (${favoriteCount})` : "Favorilerim";

  return (
    <aside className={`sidebar${isOpen ? " is-open" : ""}`} id="sidebar">
      <div className="sidebar__brand">
        <span className="sidebar__eyebrow">Şifa Hanım Aktar</span>
        <h2>Kategoriler</h2>
        <p>
          Doğanın sunduğu şifalı otları, aromatik yağları ve süs bitkilerini kategorilerine göre
          detaylıca inceleyin.
        </p>
      </div>

      <nav className="sidebar__nav" aria-label="Bitki filtreleri" id="sidebarFilters">
        {FILTERS.map((item) => (
          <button
            key={item.value}
            className={`filter-button${isActive(item.value) ? " is-active" : ""}`}
            data-filter={item.value}
            type="button"
            id={item.id}
            title={item.title}
            aria-pressed={isActive(item.value)}
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
          Şifa Hanım Aktar Geleneksel Bitki Rehberi. Bilgiler bilgilendirme amaçlıdır; doğru ürün
          kullanımı ve reçeteler için dükkanımızı ziyaret edebilir veya uzman görüşü alabilirsiniz.
        </p>
      </footer>
    </aside>
  );
}
