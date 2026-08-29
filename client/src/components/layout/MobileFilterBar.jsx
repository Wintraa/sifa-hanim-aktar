const CHIPS = [
  { value: "Tumu", label: "Tümü" },
  { value: "Tıbbi Bitkiler", label: "Tıbbi", title: "Şifa Hanım Aktar'ın özel seçkisiyle, yüzyıllardır kullanılan şifalı bitkiler ve faydaları." },
  { value: "Süs Bitkileri", label: "Süs" },
  { value: "Aromatik Bitkiler", label: "Aromatik" },
  { value: "Favoriler", label: "Favoriler", id: "mobileFavoritesChip" },
];

export function MobileFilterBar({ selectedTypes, favoritesOnly, onFilter, favoriteCount }) {
  const isActive = (value) => {
    if (value === "Tumu") return !favoritesOnly && selectedTypes.length === 0;
    if (value === "Favoriler") return favoritesOnly;
    return selectedTypes.includes(value);
  };

  return (
    <nav className="mobile-filter-bar" id="mobileFilterBar" aria-label="Hızlı kategori filtresi">
      <div className="mobile-filter-bar__track" id="mobileFilterTrack">
        {CHIPS.map((item) => (
          <button
            key={item.value}
            className={`mobile-filter-chip${isActive(item.value) ? " is-active" : ""}`}
            data-filter={item.value}
            type="button"
            id={item.id}
            title={item.title}
            aria-pressed={isActive(item.value)}
            onClick={() => onFilter(item.value)}
          >
            {item.value === "Favoriler" && favoriteCount > 0
              ? `Favoriler (${favoriteCount})`
              : item.label}
          </button>
        ))}
      </div>
    </nav>
  );
}
