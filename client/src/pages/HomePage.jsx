import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { api } from "../services/api.js";
import { useFavorites } from "../context/FavoritesContext.jsx";
import { getRecentPlantIds } from "../lib/recent-plants.js";
import { debounce } from "../lib/utils.js";
import { applyHomeSeo } from "../lib/seo.js";
import { plantMatchesTag, getTagLabel } from "../lib/plant-tags.js";
import { Sidebar } from "../components/layout/Sidebar.jsx";
import { Topbar } from "../components/layout/Topbar.jsx";
import { MobileFilterBar } from "../components/layout/MobileFilterBar.jsx";
import { PlantCard } from "../components/catalog/PlantCard.jsx";
import { Pagination } from "../components/catalog/Pagination.jsx";
import { RecentRail } from "../components/catalog/RecentRail.jsx";
import { FilterChips } from "../components/catalog/FilterChips.jsx";
import { ShopContactCards, WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";

const PAGE_SIZE = 9;
const TYPE_FILTERS = new Set(["Tıbbi Bitkiler", "Süs Bitkileri", "Aromatik Bitkiler"]);
const CATEGORY_INTROS = {
  "Tıbbi Bitkiler":
    "Şifa Hanım Aktar'ın özel seçkisiyle, yüzyıllardır kullanılan şifalı bitkiler ve faydaları.",
};

export default function HomePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { favoriteSet, favoriteCount } = useFavorites();

  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchInput, setSearchInput] = useState(searchParams.get("q") || "");

  const selectedTypes = useMemo(() => {
    const tur = searchParams.get("tur") || "";
    return tur
      .split(",")
      .map((t) => t.trim())
      .filter((t) => TYPE_FILTERS.has(t));
  }, [searchParams]);

  const favoritesOnly = searchParams.get("fav") === "1";
  const activeTag = searchParams.get("etiket") || "";
  const searchQuery = (searchParams.get("q") || "").trim().toLocaleLowerCase("tr");
  const currentPage = Math.max(1, Number(searchParams.get("page")) || 1);

  const lastMissingRef = useRef("");

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

  useEffect(() => {
    applyHomeSeo();
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const data = await api.getPlantsWithFallback();
        if (!cancelled) setPlants(data);
      } catch (err) {
        if (!cancelled) setError(err.message || "Veriler yüklenemedi.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Arama kısayolları
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
    if (value === "Tumu") {
      updateParams({ tur: null, fav: null });
    } else if (value === "Favoriler") {
      updateParams({ fav: "1", tur: null });
    } else {
      // Tek kategori seçimi (çoklu seçim: toggle)
      let nextTypes = [...selectedTypes];
      if (nextTypes.includes(value)) {
        nextTypes = nextTypes.filter((t) => t !== value);
      } else {
        nextTypes.push(value);
      }
      updateParams({
        tur: nextTypes.length ? nextTypes.join(",") : null,
        fav: null,
      });
    }
    setMenuOpen(false);
  };

  const handleClearChip = (kind, typeValue) => {
    if (kind === "all") {
      setSearchInput("");
      updateParams({ tur: null, fav: null, q: null });
    } else if (kind === "type") {
      const next = selectedTypes.filter((t) => t !== typeValue);
      updateParams({ tur: next.length ? next.join(",") : null });
    } else if (kind === "favorites") {
      updateParams({ fav: null });
    } else if (kind === "search") {
      setSearchInput("");
      updateParams({ q: null });
    } else if (kind === "tag") {
      updateParams({ etiket: null });
    }
  };

  const filteredPlants = useMemo(() => {
    let result = [...plants];
    if (favoritesOnly) {
      result = result.filter((p) => favoriteSet.has(Number(p.id)));
    } else if (selectedTypes.length > 0) {
      const selected = new Set(selectedTypes);
      result = result.filter((p) => selected.has(p.tur));
    }
    if (searchQuery) {
      result = result.filter((p) => {
        const hay = `${p.ad ?? ""} ${p.botanikAd ?? ""} ${p.tur ?? ""}`.toLocaleLowerCase("tr");
        return hay.includes(searchQuery);
      });
    }
    if (activeTag) {
      result = result.filter((p) => plantMatchesTag(p, activeTag));
    }
    return result;
  }, [plants, favoritesOnly, selectedTypes, searchQuery, activeTag, favoriteSet]);

  const totalPages = Math.max(1, Math.ceil(filteredPlants.length / PAGE_SIZE));
  const safePage = Math.min(currentPage, totalPages);
  const startIndex = (safePage - 1) * PAGE_SIZE;
  const visiblePlants = filteredPlants.slice(startIndex, startIndex + PAGE_SIZE);

  // Boş aramayı kaydet
  useEffect(() => {
    if (loading || favoritesOnly || !searchQuery || filteredPlants.length > 0) return;
    const raw = searchInput.trim() || searchQuery;
    if (raw.length < 2) return;
    const key = raw.toLocaleLowerCase("tr");
    if (key === lastMissingRef.current) return;
    lastMissingRef.current = key;
    api.postMissingSearch(raw).catch(() => {
      lastMissingRef.current = "";
    });
  }, [loading, favoritesOnly, searchQuery, filteredPlants.length, searchInput]);

  const recentPlants = useMemo(() => {
    return getRecentPlantIds()
      .map((id) => plants.find((p) => Number(p.id) === id))
      .filter(Boolean);
  }, [plants]);

  const filterLabelParts = [];
  if (favoritesOnly) filterLabelParts.push("Favori Bitkilerim");
  else if (selectedTypes.length > 0) filterLabelParts.push(...selectedTypes);
  else filterLabelParts.push("Tüm Bitkiler");
  if (searchQuery) {
    filterLabelParts.push(`Arama: “${searchInput.trim() || searchQuery}”`);
  }
  if (activeTag) {
    filterLabelParts.push(`Etiket: #${getTagLabel(activeTag)}`);
  }

  const singleType =
    !favoritesOnly && selectedTypes.length === 1 ? selectedTypes[0] : null;
  const categoryIntro = singleType ? CATEGORY_INTROS[singleType] : "";

  return (
    <>
      <div className="site-shell">
        <Sidebar
          mode="plants"
          selectedTypes={selectedTypes}
          favoritesOnly={favoritesOnly}
          onFilter={handleFilter}
          favoriteCount={favoriteCount}
          isOpen={menuOpen}
        />

        <button
          type="button"
          className={`overlay${menuOpen ? " is-visible" : ""}`}
          id="overlay"
          aria-label="Menüyü kapat"
          aria-hidden={!menuOpen}
          tabIndex={menuOpen ? 0 : -1}
          onClick={() => setMenuOpen(false)}
        />

        <div className="main-panel">
          <Topbar
            catalogMode="plants"
            searchValue={searchInput}
            onSearchChange={handleSearchChange}
            onMenuToggle={() => setMenuOpen((v) => !v)}
            menuOpen={menuOpen}
            onFavoritesClick={() => handleFilter("Favoriler")}
            favoriteCount={favoriteCount}
          />

          <main className="content" id="main-content">
            <section className="hero-card" aria-labelledby="heroTitle">
              <div>
                <p className="section-label">Şifa Hanım Aktar • Şifalı Bitki Kütüphanesi</p>
                <h2 id="heroTitle">Doğanın Şifası, Yılların Tecrübesiyle Buluşuyor.</h2>
                <p className="hero-card__text">
                  Şifa Hanım Aktar olarak; asırlık geleneksel bitki bilgeliğini modern ve bilimsel
                  verilerle harmanladık. Tıbbi, aromatik ve şifalı bitkilerin tüm detaylarını,
                  doğru kullanım alanlarını ve geleneksel reçetelerini bu rehberde keşfedebilirsiniz.
                </p>
              </div>
              <div className="hero-card__badge">
                <span id="plantCount">{loading ? "…" : filteredPlants.length}</span>
                <small id="plantCountLabel">bitki</small>
              </div>
            </section>

            <FilterChips
              selectedTypes={selectedTypes}
              favoritesOnly={favoritesOnly}
              searchRaw={searchInput.trim()}
              activeTag={activeTag}
              onClear={handleClearChip}
            />

            <RecentRail plants={recentPlants} />

            <section className="plants-section" aria-labelledby="plantsTitle">
              <div className="plants-section__header">
                <div>
                  <p className="section-label">Katalog</p>
                  <h3 id="plantsTitle">Bitki listesi</h3>
                  {categoryIntro ? (
                    <p className="plants-section__intro" id="categoryIntro">
                      {categoryIntro}
                    </p>
                  ) : null}
                </div>
                <p className="plants-section__meta" id="activeFilterLabel">
                  {filterLabelParts.join(" · ")}
                </p>
              </div>

              {loading ? (
                <p className="plants-section__intro">Bitkiler yükleniyor…</p>
              ) : null}

              {error ? (
                <div className="empty-state">
                  <h4>Veri yüklenemedi</h4>
                  <p>{error}</p>
                </div>
              ) : null}

              {!loading && !error && filteredPlants.length === 0 ? (
                <div className="empty-state" id="emptyState">
                  {favoritesOnly ? (
                    <>
                      <h4>Favori listesi boş</h4>
                      <p>
                        Bitki kartlarındaki kalp simgesiyle seçtiğiniz maddeler burada toplanır.
                      </p>
                    </>
                  ) : (
                    <>
                      <h4>Arşivde bulunamadı</h4>
                      <p>
                        Aradığınız şifalı ot arşivimizde bulunamadı. Şifa Hanım Aktar özel
                        karışımları ve danışma için bizimle iletişime geçebilirsiniz.
                        {searchQuery ? (
                          <>
                            <br />
                            <small>Bu arama not edildi; eksik bitki listesine eklendi.</small>
                          </>
                        ) : null}
                      </p>
                    </>
                  )}
                  <button
                    className="back-button empty-state__cta"
                    type="button"
                    onClick={() => handleClearChip("all")}
                  >
                    Tüm bitkilere dön
                  </button>
                </div>
              ) : null}

              {!loading && !error && visiblePlants.length > 0 ? (
                <div className="plants-grid" id="plantsGrid" aria-live="polite">
                  {visiblePlants.map((plant, index) => (
                    <PlantCard
                      key={plant.id}
                      plant={plant}
                      visibleIndex={index}
                      showCare={favoritesOnly}
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
                    <strong>Şifa Hanım Aktar</strong> — geleneksel bitki rehberi. Bilgiler
                    bilgilendirme amaçlıdır; teşhis veya tedavi yerine geçmez.
                  </p>
                  <p className="site-footer__link-row">
                    <Link to="/">Ürün vitrini</Link>
                    {" · "}
                    <Link to="/iletisim">İletişim &amp; WhatsApp</Link>
                    {" · "}
                    <Link to="/kayit">Hesap aç</Link>
                  </p>
                </div>
                <ShopContactCards compact />
              </div>
            </footer>
          </main>
        </div>
      </div>

      <MobileFilterBar
        selectedTypes={selectedTypes}
        favoritesOnly={favoritesOnly}
        onFilter={handleFilter}
        favoriteCount={favoriteCount}
      />
      <WhatsAppFloatButton />
    </>
  );
}
