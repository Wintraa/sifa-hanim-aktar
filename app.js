import { getFavorites, toggleFavorite } from "./favorites.js";
import { getRecentPlantIds } from "./recent-plants.js";
import { applyDensityPreference } from "./preferences.js";
import { getUserProfile } from "./user-profile.js";
import { showToast } from "./toast.js";
import { getPlants } from "./plant-data.js";
import { createPlantCardMarkup, createRecentCardMarkup } from "./plant-card.js";
import { debounce, escapeHtml } from "./utils.js";

const PAGE_SIZE = 9;
const TYPE_FILTERS = new Set(["Tıbbi Bitkiler", "Süs Bitkileri", "Aromatik Bitkiler"]);

// Aynı oturumda aynı boş aramayı tekrar tekrar yazmamak için
let lastRecordedMissingSearch = "";

/** Sonucsuz aramayı sunucuya / database'e kaydeder. */
const recordMissingSearch = (query) => {
  const trimmed = String(query || "").trim();
  if (trimmed.length < 2) {
    return;
  }

  const key = trimmed.toLocaleLowerCase("tr");
  if (key === lastRecordedMissingSearch) {
    return;
  }
  lastRecordedMissingSearch = key;

  fetch("/api/bulunamayan-aramalar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ arama: trimmed })
  }).catch(() => {
    // Sunucu kapalıysa sessizce geç; site çalışmaya devam etsin.
    lastRecordedMissingSearch = "";
  });
};

// Kategori seçildiğinde katalog alanında gösterilen kurumsal tanıtım metinleri
const CATEGORY_INTROS = {
  "Tıbbi Bitkiler":
    "Şifa Hanım Aktar'ın özel seçkisiyle, yüzyıllardır kullanılan şifalı bitkiler ve faydaları."
};

const state = {
  plants: [],
  filteredPlants: [],
  selectedTypes: [],
  favoritesOnly: false,
  searchQuery: "",
  currentPage: 1,
  isLoading: false
};

const elements = {
  plantsGrid: document.querySelector("#plantsGrid"),
  pagination: document.querySelector("#pagination"),
  filterButtons: document.querySelectorAll(".filter-button"),
  mobileFilterChips: document.querySelectorAll(".mobile-filter-chip"),
  activeFilterLabel: document.querySelector("#activeFilterLabel"),
  categoryIntro: document.querySelector("#categoryIntro"),
  plantCount: document.querySelector("#plantCount"),
  plantCountLabel: document.querySelector("#plantCountLabel"),
  emptyState: document.querySelector("#emptyState"),
  filterChips: document.querySelector("#filterChips"),
  resetFiltersButton: document.querySelector("#resetFiltersButton"),
  recentSection: document.querySelector("#recentSection"),
  recentRail: document.querySelector("#recentRail"),
  userMenuButton: document.querySelector("#userMenuButton"),
  userDropdown: document.querySelector("#userDropdown"),
  menuToggle: document.querySelector("#menuToggle"),
  sidebar: document.querySelector("#sidebar"),
  overlay: document.querySelector("#overlay"),
  searchInput: document.querySelector("#searchInput"),
  favoritesMenuLink: document.querySelector("#favoritesMenuLink"),
  favoritesFilterButton: document.querySelector("#favoritesFilterButton"),
  mobileFavoritesChip: document.querySelector("#mobileFavoritesChip"),
  userMenuAvatar: document.querySelector(".user-menu__trigger img"),
  userMenuName: document.querySelector(".user-menu__name"),
  logoutMenuLink: document.querySelector("#logoutMenuLink")
};

// Uygulamanın ilk yükleniş akışlarını yönetir.
const init = async () => {
  applyDensityPreference();
  renderUserMenuProfile();
  readStateFromUrl();
  bindEvents();
  await loadPlants();
};

// JSON kaynağından bitki verilerini getirir ve ilk görünümü hazırlar.
const loadPlants = async () => {
  setLoadingState(true);

  try {
    state.plants = await getPlants();
  } catch (error) {
    state.isLoading = false;
    renderErrorState(error.message || "Beklenmeyen bir hata oluştu.");
    return;
  }

  state.isLoading = false;
  applyFilters({ syncUrl: true });
  renderRecentSection();
};

// Yükleme durumunu grid alanında gösterir.
const setLoadingState = (isLoading) => {
  state.isLoading = isLoading;

  if (!isLoading || !elements.plantsGrid || !elements.emptyState || !elements.pagination) {
    return;
  }

  elements.emptyState.hidden = true;
  elements.pagination.innerHTML = "";
  elements.plantsGrid.innerHTML = `
    <div class="loading-state" role="status" aria-live="polite">
      <p>Bitkiler yükleniyor...</p>
    </div>
  `;
};

// Tüm tıklama ve pencere olaylarını tek noktadan bağlar.
const bindEvents = () => {
  const handleSearch = debounce((rawValue) => {
    state.searchQuery = rawValue.trim().toLocaleLowerCase("tr");
    state.currentPage = 1;
    applyFilters({ syncUrl: true });
  });

  const onFilterClick = (event) => {
    const button = event.target.closest("[data-filter]");

    if (!button) {
      return;
    }

    handleFilterSelection(button.dataset.filter);
    closeSidebar({ restoreFocus: true });
  };

  document.querySelector("#sidebarFilters")?.addEventListener("click", onFilterClick);
  document.querySelector("#mobileFilterTrack")?.addEventListener("click", onFilterClick);

  elements.searchInput?.addEventListener("input", (event) => {
    handleSearch(event.target.value);
  });

  elements.resetFiltersButton?.addEventListener("click", () => {
    resetAllFilters();
  });

  elements.filterChips?.addEventListener("click", (event) => {
    const chip = event.target.closest("[data-chip-action]");

    if (!chip) {
      return;
    }

    const action = chip.dataset.chipAction;

    if (action === "clear-all") {
      resetAllFilters();
      return;
    }

    if (action === "clear-search") {
      state.searchQuery = "";
      if (elements.searchInput) {
        elements.searchInput.value = "";
      }
      state.currentPage = 1;
      applyFilters({ syncUrl: true });
      return;
    }

    if (action === "clear-favorites") {
      state.favoritesOnly = false;
      state.currentPage = 1;
      applyFilters({ syncUrl: true });
      return;
    }

    if (action === "clear-type") {
      const type = chip.dataset.chipValue;
      state.selectedTypes = state.selectedTypes.filter((item) => item !== type);
      state.currentPage = 1;
      applyFilters({ syncUrl: true });
    }
  });

  elements.favoritesMenuLink?.addEventListener("click", () => {
    handleFilterSelection("Favoriler");
    closeUserDropdown();
  });

  elements.logoutMenuLink?.addEventListener("click", (event) => {
    event.preventDefault();
    closeUserDropdown();
    showToast("Oturum bu cihazda kapatıldı. Verileriniz yalnızca tarayıcınızda saklanır.", "info");
  });

  elements.userMenuButton?.addEventListener("click", () => {
    const isExpanded = elements.userMenuButton.getAttribute("aria-expanded") === "true";
    elements.userMenuButton.setAttribute("aria-expanded", String(!isExpanded));
    elements.userDropdown.hidden = isExpanded;

    if (!isExpanded) {
      window.requestAnimationFrame(() =>
        elements.userDropdown?.querySelector('[role="menuitem"]')?.focus()
      );
    }
  });

  elements.userDropdown?.addEventListener("keydown", (event) => {
    const menuItems = [...elements.userDropdown.querySelectorAll('[role="menuitem"]')];
    const currentIndex = menuItems.indexOf(document.activeElement);

    if (event.key === "Escape") {
      event.preventDefault();
      closeUserDropdown({ restoreFocus: true });
      return;
    }

    if (!["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
      return;
    }

    event.preventDefault();
    const nextIndex =
      event.key === "Home"
        ? 0
        : event.key === "End"
          ? menuItems.length - 1
          : (currentIndex + (event.key === "ArrowDown" ? 1 : -1) + menuItems.length) %
            menuItems.length;

    menuItems[nextIndex]?.focus();
  });

  elements.menuToggle?.addEventListener("click", () => {
    const isOpen = elements.sidebar.classList.contains("is-open");
    isOpen ? closeSidebar({ restoreFocus: true }) : openSidebar();
  });

  elements.overlay?.addEventListener("click", () => closeSidebar({ restoreFocus: true }));

  elements.plantsGrid?.addEventListener("click", (event) => {
    const button = event.target.closest("[data-favorite-id]");

    if (!button) {
      return;
    }

    event.preventDefault();
    const plantId = Number(button.dataset.favoriteId);
    const active = toggleFavorite(plantId);
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
    button.setAttribute("aria-label", active ? "Favorilerden çıkar" : "Favorilere ekle");
    button.title = active ? "Favorilerden çıkar" : "Favorilere ekle";

    const icon = button.querySelector("span");
    if (icon) {
      icon.textContent = active ? "♥" : "♡";
    }

    // Mikro-animasyon: scale-up pulse (tekrar tıklamada da tetiklensin)
    button.classList.remove("is-animating");
    void button.offsetWidth;
    button.classList.add("is-animating");
    button.addEventListener(
      "animationend",
      () => {
        button.classList.remove("is-animating");
      },
      { once: true }
    );

    updateFavoriteCounters();
    showToast(active ? "Favorilere eklendi." : "Favorilerden çıkarıldı.", "success");

    if (state.favoritesOnly) {
      applyFilters({ syncUrl: true });
    }
  });

  elements.pagination?.addEventListener("click", (event) => {
    const button = event.target.closest("[data-page]");

    if (!button || button.disabled) {
      return;
    }

    const nextPage = Number(button.dataset.page);

    if (!Number.isInteger(nextPage) || nextPage < 1) {
      return;
    }

    state.currentPage = nextPage;
    renderCurrentPage();
    syncUrlFromState();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  document.addEventListener("click", (event) => {
    const target = event.target;

    if (
      elements.userDropdown &&
      !elements.userDropdown.hidden &&
      !target.closest(".user-menu")
    ) {
      closeUserDropdown();
    }
  });

  document.addEventListener("keydown", (event) => {
    const tag = event.target?.tagName?.toLowerCase();
    const isTypingField =
      tag === "input" || tag === "textarea" || event.target?.isContentEditable;

    if (event.key === "/" && !isTypingField) {
      event.preventDefault();
      elements.searchInput?.focus();
      elements.searchInput?.select();
      return;
    }

    if (event.key === "Escape") {
      closeSidebar({ restoreFocus: true });
      closeUserDropdown({ restoreFocus: true });
      elements.searchInput?.blur();
      return;
    }

    if (event.key === "Tab" && elements.sidebar?.classList.contains("is-open")) {
      const focusable = [
        ...elements.sidebar.querySelectorAll(
          'a[href], button:not(:disabled), input:not(:disabled), [tabindex]:not([tabindex="-1"])'
        )
      ];
      const first = focusable[0];
      const last = focusable.at(-1);

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last?.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first?.focus();
      }
    }
  });

  window.addEventListener("popstate", () => {
    readStateFromUrl();
    applyFilters({ syncUrl: false });
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 900) {
      closeSidebar();
    }
  });
};

// Filtre düğmesi seçimini (çoklu tür desteğiyle) işler.
const handleFilterSelection = (filterValue) => {
  if (filterValue === "Tumu") {
    state.selectedTypes = [];
    state.favoritesOnly = false;
    state.currentPage = 1;
    applyFilters({ syncUrl: true });
    return;
  }

  if (filterValue === "Favoriler") {
    state.favoritesOnly = !state.favoritesOnly;
    if (state.favoritesOnly) {
      state.selectedTypes = [];
    }
    state.currentPage = 1;
    applyFilters({ syncUrl: true });
    return;
  }

  if (!TYPE_FILTERS.has(filterValue)) {
    return;
  }

  state.favoritesOnly = false;
  const exists = state.selectedTypes.includes(filterValue);
  state.selectedTypes = exists
    ? state.selectedTypes.filter((item) => item !== filterValue)
    : [...state.selectedTypes, filterValue];
  state.currentPage = 1;
  applyFilters({ syncUrl: true });
};

// Tüm filtreleri ve aramayı sıfırlar.
const resetAllFilters = (focusSearch = false) => {
  state.selectedTypes = [];
  state.favoritesOnly = false;
  state.searchQuery = "";
  state.currentPage = 1;

  if (elements.searchInput) {
    elements.searchInput.value = "";
  }

  applyFilters({ syncUrl: true });

  if (focusSearch) {
    elements.searchInput?.focus();
  }
};

// Ana sayfadaki avatar ve isim alanını kayıtlı profil verisiyle eşler.
const renderUserMenuProfile = () => {
  const profile = getUserProfile();

  if (elements.userMenuAvatar) {
    elements.userMenuAvatar.src = profile.avatarUrl;
    elements.userMenuAvatar.alt = `${profile.fullName} profil fotoğrafı`;
  }

  if (elements.userMenuName) {
    elements.userMenuName.textContent = profile.fullName;
  }

  updateFavoriteCounters();
};

// Favori sayaçlarını menü ve filtre düğmelerinde günceller.
const updateFavoriteCounters = () => {
  const count = getFavorites().length;
  const filterLabel = count > 0 ? `Favori Bitkilerim (${count})` : "Favori Bitkilerim";
  const menuLabel = count > 0 ? `Favori Bitkilerim (${count})` : "Favori Bitkilerim";
  const mobileLabel = count > 0 ? `Favoriler (${count})` : "Favoriler";

  if (elements.favoritesFilterButton) {
    elements.favoritesFilterButton.textContent = filterLabel;
  }

  if (elements.favoritesMenuLink) {
    elements.favoritesMenuLink.textContent = menuLabel;
  }

  if (elements.mobileFavoritesChip) {
    elements.mobileFavoritesChip.textContent = mobileLabel;
  }
};

// Kategori, arama ve favori filtresini birlikte uygular.
const applyFilters = ({ syncUrl = false } = {}) => {
  const favorites = new Set(getFavorites());
  let result = [...state.plants];

  if (state.favoritesOnly) {
    result = result.filter((plant) => favorites.has(plant.id));
  } else if (state.selectedTypes.length > 0) {
    const selected = new Set(state.selectedTypes);
    result = result.filter((plant) => selected.has(plant.tur));
  }

  if (state.searchQuery) {
    result = result.filter((plant) => {
      const haystack = `${plant.ad ?? ""} ${plant.botanikAd ?? ""} ${plant.tur ?? ""}`.toLocaleLowerCase("tr");
      return haystack.includes(state.searchQuery);
    });
  }

  state.filteredPlants = result;
  updateActiveFilterStyles();
  renderFilterChips();
  renderCurrentPage();
  updateFavoriteCounters();

  if (syncUrl) {
    syncUrlFromState();
  }
};

// Aktif filtre görünümlerini günceller.
const updateActiveFilterStyles = () => {
  const isAll =
    !state.favoritesOnly && state.selectedTypes.length === 0 && !state.searchQuery;

  const syncButtons = (buttons) => {
    buttons.forEach((button) => {
      const value = button.dataset.filter;
      let active = false;

      if (value === "Tumu") {
        active = !state.favoritesOnly && state.selectedTypes.length === 0;
      } else if (value === "Favoriler") {
        active = state.favoritesOnly;
      } else {
        active = state.selectedTypes.includes(value);
      }

      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  };

  syncButtons(elements.filterButtons);
  syncButtons(elements.mobileFilterChips);

  const parts = [];

  if (state.favoritesOnly) {
    parts.push("Favori Bitkilerim");
  } else if (state.selectedTypes.length > 0) {
    parts.push(...state.selectedTypes);
  } else {
    parts.push("Tüm Bitkiler");
  }

  if (state.searchQuery) {
    parts.push(`Arama: “${elements.searchInput?.value.trim() || state.searchQuery}”`);
  }

  elements.activeFilterLabel.textContent = parts.join(" · ");

  // Tek kategori seçiliyse kurumsal tanıtım metnini göster
  if (elements.categoryIntro) {
    const singleType =
      !state.favoritesOnly && state.selectedTypes.length === 1 ? state.selectedTypes[0] : null;
    const intro = singleType ? CATEGORY_INTROS[singleType] : "";

    if (intro) {
      elements.categoryIntro.hidden = false;
      elements.categoryIntro.textContent = intro;
    } else {
      elements.categoryIntro.hidden = true;
      elements.categoryIntro.textContent = "";
    }
  }

  if (isAll) {
    // Etiketi sade tut.
  }
};

// Aktif filtreleri çip olarak gösterir.
const renderFilterChips = () => {
  if (!elements.filterChips) {
    return;
  }

  const chips = [];

  state.selectedTypes.forEach((type) => {
    chips.push(`
      <button class="filter-chip" type="button" data-chip-action="clear-type" data-chip-value="${escapeHtml(type)}">
        ${escapeHtml(type)} <span aria-hidden="true">×</span>
      </button>
    `);
  });

  if (state.favoritesOnly) {
    chips.push(`
      <button class="filter-chip" type="button" data-chip-action="clear-favorites">
        Favoriler <span aria-hidden="true">×</span>
      </button>
    `);
  }

  if (state.searchQuery) {
    const raw = elements.searchInput?.value.trim() || state.searchQuery;
    chips.push(`
      <button class="filter-chip" type="button" data-chip-action="clear-search">
        Arama: “${escapeHtml(raw)}” <span aria-hidden="true">×</span>
      </button>
    `);
  }

  if (chips.length === 0) {
    elements.filterChips.innerHTML = `
      <p class="filter-chips__empty">Şu anda ek bir filtre uygulanmıyor.</p>
    `;
    return;
  }

  elements.filterChips.innerHTML = `
    ${chips.join("")}
    <button class="filter-chip filter-chip--clear" type="button" data-chip-action="clear-all">
      Tümünü temizle
    </button>
  `;
};

// O anki sayfa dilimini hesaplar ve kartları ekrana basar.
const renderCurrentPage = () => {
  if (state.isLoading) {
    return;
  }

  const totalPages = Math.max(1, Math.ceil(state.filteredPlants.length / PAGE_SIZE));

  if (state.currentPage > totalPages) {
    state.currentPage = totalPages;
  }

  const startIndex = (state.currentPage - 1) * PAGE_SIZE;
  const visiblePlants = state.filteredPlants.slice(startIndex, startIndex + PAGE_SIZE);
  const favoriteIds = new Set(getFavorites());
  const count = state.filteredPlants.length;

  elements.plantCount.textContent = String(count);
  if (elements.plantCountLabel) {
    elements.plantCountLabel.textContent = count === 1 ? "bitki" : "bitki";
  }

  elements.emptyState.hidden = count !== 0;

  if (count === 0) {
    const rawSearch = elements.searchInput?.value.trim() || "";
    const hasSearchMiss = Boolean(state.searchQuery) && !state.favoritesOnly;

    elements.emptyState.innerHTML =
      state.favoritesOnly
        ? `
          <h4>Favori listesi boş</h4>
          <p>Bitki kartlarındaki kalp simgesiyle seçtiğiniz maddeler burada toplanır.</p>
          <button class="back-button empty-state__cta" type="button" data-chip-action="clear-all" id="emptyResetBtn">
            Tüm bitkilere dön
          </button>
        `
        : `
          <h4>Arşivde bulunamadı</h4>
          <p>
            Aradığınız şifalı ot arşivimizde bulunamadı. Şifa Hanım Aktar özel karışımları ve
            danışma için bizimle iletişime geçebilirsiniz.
            ${hasSearchMiss ? "<br /><small>Bu arama not edildi; eksik bitki listesine eklendi.</small>" : ""}
          </p>
          <button class="back-button empty-state__cta" type="button" id="emptyResetBtn">
            Tüm bitkilere dön
          </button>
        `;

    elements.emptyState.querySelector("#emptyResetBtn")?.addEventListener("click", () => {
      resetAllFilters();
    });

    // Anne/ziyaretçi arayıp bulamayınca kelimeyi database'e yaz.
    if (hasSearchMiss) {
      recordMissingSearch(rawSearch || state.searchQuery);
    }
  }

  elements.plantsGrid.innerHTML = visiblePlants
    .map((plant, index) =>
      createPlantCardMarkup(plant, favoriteIds, {
        visibleIndex: index,
        showCare: state.favoritesOnly
      })
    )
    .join("");
  renderPagination();
};

// Son bakılan bitkileri yatay şeritte gösterir.
const renderRecentSection = () => {
  if (!elements.recentSection || !elements.recentRail) {
    return;
  }

  const ids = getRecentPlantIds();
  const plants = ids
    .map((id) => state.plants.find((plant) => plant.id === id))
    .filter(Boolean);

  if (plants.length === 0) {
    elements.recentSection.hidden = true;
    elements.recentRail.innerHTML = "";
    return;
  }

  elements.recentSection.hidden = false;
  elements.recentRail.innerHTML = plants
    .map(createRecentCardMarkup)
    .join("");
};

// Google benzeri numaralı sayfalama düğmelerini oluşturur.
const renderPagination = () => {
  const totalPages = Math.ceil(state.filteredPlants.length / PAGE_SIZE);

  if (totalPages <= 1) {
    elements.pagination.innerHTML = "";
    return;
  }

  const pageNumbers = Array.from({ length: totalPages }, (_, index) => index + 1);

  elements.pagination.innerHTML = [
    createPaginationButton("Önceki", state.currentPage === 1, state.currentPage - 1),
    ...pageNumbers.map((pageNumber) =>
      createPaginationButton(String(pageNumber), false, pageNumber, pageNumber === state.currentPage)
    ),
    createPaginationButton("Sonraki", state.currentPage === totalPages, state.currentPage + 1)
  ].join("");
};

// Tekil bir sayfalama düğmesi HTML'i döndürür.
const createPaginationButton = (label, disabled, page, isActive = false) => `
  <button
    class="pagination__button ${isActive ? "is-active" : ""}"
    type="button"
    data-page="${page}"
    aria-label="${isActive ? `Sayfa ${page}, mevcut sayfa` : `${label} sayfasına git`}"
    ${isActive ? 'aria-current="page"' : ""}
    ${disabled ? "disabled" : ""}
  >
    ${escapeHtml(label)}
  </button>
`;

// Hata durumunda liste alanında kullanıcıya yönlendirici mesaj gösterir.
const renderErrorState = (message) => {
  elements.plantCount.textContent = "0";
  elements.emptyState.hidden = false;
  elements.plantsGrid.innerHTML = "";
  elements.pagination.innerHTML = "";
  elements.emptyState.innerHTML = `
    <h4>Veri yüklenemedi</h4>
    <p>${escapeHtml(message)}</p>
  `;
};

// URL sorgu parametrelerinden filtre durumunu okur.
const readStateFromUrl = () => {
  const params = new URLSearchParams(window.location.search);
  const turParam = params.get("tur") || "";
  const types = turParam
    .split(",")
    .map((item) => item.trim())
    .filter((item) => TYPE_FILTERS.has(item));

  state.selectedTypes = types;
  state.favoritesOnly = params.get("fav") === "1";
  state.searchQuery = (params.get("q") || "").trim().toLocaleLowerCase("tr");
  state.currentPage = Math.max(1, Number(params.get("page")) || 1);

  if (elements.searchInput) {
    elements.searchInput.value = params.get("q") || "";
  }

  if (state.favoritesOnly) {
    state.selectedTypes = [];
  }
};

// Güncel filtre durumunu paylaşılabilir URL’ye yazar.
const syncUrlFromState = () => {
  const params = new URLSearchParams();

  if (state.favoritesOnly) {
    params.set("fav", "1");
  } else if (state.selectedTypes.length > 0) {
    params.set("tur", state.selectedTypes.join(","));
  }

  const rawQuery = elements.searchInput?.value.trim() || "";
  if (rawQuery) {
    params.set("q", rawQuery);
  }

  if (state.currentPage > 1) {
    params.set("page", String(state.currentPage));
  }

  const query = params.toString();
  const nextUrl = query ? `${window.location.pathname}?${query}` : window.location.pathname;
  window.history.replaceState({}, "", nextUrl);
};

// Mobil menüyü kapalı ve temiz halde tutar.
const openSidebar = () => {
  elements.sidebar?.classList.add("is-open");
  elements.overlay?.classList.add("is-visible");
  elements.overlay?.setAttribute("aria-hidden", "false");
  elements.overlay?.setAttribute("tabindex", "0");
  elements.menuToggle?.setAttribute("aria-expanded", "true");
  document.body.classList.add("has-open-menu");
  window.requestAnimationFrame(() => elements.sidebar?.querySelector("button")?.focus());
};

// Mobil menüyü kapalı ve temiz halde tutar.
const closeSidebar = ({ restoreFocus = false } = {}) => {
  const wasOpen = elements.sidebar?.classList.contains("is-open");
  elements.sidebar?.classList.remove("is-open");
  elements.overlay?.classList.remove("is-visible");
  elements.overlay?.setAttribute("aria-hidden", "true");
  elements.overlay?.setAttribute("tabindex", "-1");
  elements.menuToggle?.setAttribute("aria-expanded", "false");
  document.body.classList.remove("has-open-menu");

  if (restoreFocus && wasOpen) {
    elements.menuToggle?.focus();
  }
};

// Kullanıcı açılır menüsünü kapatır.
const closeUserDropdown = ({ restoreFocus = false } = {}) => {
  const wasOpen = elements.userDropdown && !elements.userDropdown.hidden;
  if (elements.userDropdown) {
    elements.userDropdown.hidden = true;
  }
  elements.userMenuButton?.setAttribute("aria-expanded", "false");

  if (restoreFocus && wasOpen) {
    elements.userMenuButton?.focus();
  }
};

init();
