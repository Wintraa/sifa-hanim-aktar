import { getTagLabel } from "../../lib/plant-tags.js";

export function FilterChips({ selectedTypes, favoritesOnly, searchRaw, activeTag, onClear }) {
  const chips = [];

  selectedTypes.forEach((type) => {
    chips.push({
      key: `type-${type}`,
      label: type,
      action: () => onClear("type", type),
    });
  });

  if (favoritesOnly) {
    chips.push({
      key: "fav",
      label: "Favoriler",
      action: () => onClear("favorites"),
    });
  }

  if (searchRaw) {
    chips.push({
      key: "search",
      label: `Arama: “${searchRaw}”`,
      action: () => onClear("search"),
    });
  }

  if (activeTag) {
    chips.push({
      key: "tag",
      label: `Etiket: #${getTagLabel(activeTag)}`,
      action: () => onClear("tag"),
    });
  }

  return (
    <section className="filter-chips-section" aria-label="Aktif filtreler">
      <div className="filter-chips" id="filterChips">
        {chips.length === 0 ? (
          <p className="filter-chips__empty">Şu anda ek bir filtre uygulanmıyor.</p>
        ) : (
          <>
            {chips.map((chip) => (
              <button
                key={chip.key}
                className="filter-chip"
                type="button"
                onClick={chip.action}
              >
                {chip.label} <span aria-hidden="true">×</span>
              </button>
            ))}
            <button
              className="filter-chip filter-chip--clear"
              type="button"
              onClick={() => onClear("all")}
            >
              Tümünü temizle
            </button>
          </>
        )}
      </div>
    </section>
  );
}
