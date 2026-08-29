import { getCareNote } from "./care-notes.js";
import { escapeHtml } from "./utils.js";

// Kart metinlerinin ızgara yüksekliğini bozmaması için kontrollü kısaltma yapar.
const truncateText = (text, length) => {
  const value = String(text ?? "").trim();
  if (value.length <= length) {
    return value;
  }

  const slice = value.slice(0, length);
  const sentenceEnd = Math.max(slice.lastIndexOf(". "), slice.lastIndexOf("! "), slice.lastIndexOf("? "));
  if (sentenceEnd >= Math.floor(length * 0.45)) {
    return `${slice.slice(0, sentenceEnd + 1).trim()}`;
  }

  const wordEnd = slice.lastIndexOf(" ");
  const cut = wordEnd > 40 ? slice.slice(0, wordEnd) : slice;
  return `${cut.trim()}…`;
};

const escapeRegExp = (value) => String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

// Kart başlığında zaten görünen ad/botanik adını açıklama metninin başından düşürür.
const stripLeadingPlantName = (text, ad, botanikAd) => {
  let value = String(text ?? "").trim();
  if (!value) {
    return "";
  }

  const patterns = [
    new RegExp(`^${escapeRegExp(ad)}\\s*\\(\\s*${escapeRegExp(botanikAd)}\\s*\\)\\s*[,:—\\-–]?\\s*`, "i"),
    new RegExp(`^${escapeRegExp(ad)}\\s*[,:—\\-–]?\\s*`, "i"),
  ];

  for (const pattern of patterns) {
    value = value.replace(pattern, "");
  }

  value = value.trim();
  if (!value) {
    return "";
  }

  // Türkçe baş harf büyütme (i → İ)
  const first = value.charAt(0);
  const rest = value.slice(1);
  const upperMap = { i: "İ", ı: "I", ş: "Ş", ğ: "Ğ", ü: "Ü", ö: "Ö", ç: "Ç" };
  const upper = upperMap[first] || first.toLocaleUpperCase("tr");
  return upper + rest;
};

const isMedicinal = (plant) => plant?.tur === "Tıbbi Bitkiler";

// Liste ekranındaki erişilebilir bitki kartı HTML'ini üretir.
export const createPlantCardMarkup = (
  plant,
  favoriteIds,
  { visibleIndex = 0, showCare = false } = {}
) => {
  const favorite = favoriteIds.has(Number(plant.id));
  const medicinal = isMedicinal(plant);
  const ad = escapeHtml(plant.ad);
  const botanikAd = escapeHtml(plant.botanikAd);
  const tur = escapeHtml(plant.tur);
  const resimUrl = escapeHtml(plant.resimUrl);
  const rawDescription = stripLeadingPlantName(plant.genelTavsiyeMetni, plant.ad, plant.botanikAd);
  const description = escapeHtml(truncateText(rawDescription, 180));
  const id = Number(plant.id);
  const detailHref = `detail.html?id=${id}`;
  const care = getCareNote(id);
  const careMarkup =
    showCare && !medicinal && care
      ? `<p class="plant-card__care">Her ${escapeHtml(String(care.intervalDays))} günde bir sulama${
          care.note ? ` · ${escapeHtml(care.note)}` : ""
        }</p>`
      : "";

  return `
    <article class="plant-card">
      <div class="plant-card__media">
        <a class="plant-card__image-link" href="${detailHref}" aria-label="${ad} ayrıntılarını aç">
          <img
            class="plant-card__image"
            src="${resimUrl}"
            alt="${ad} görseli"
            width="640"
            height="480"
            loading="${visibleIndex < 3 ? "eager" : "lazy"}"
            decoding="async"
            ${visibleIndex === 0 ? 'fetchpriority="high"' : ""}
          />
        </a>
        <button
          class="favorite-button ${favorite ? "is-active" : ""}"
          type="button"
          data-favorite-id="${id}"
          aria-pressed="${favorite}"
          aria-label="${favorite ? "Favorilerden çıkar" : "Favorilere ekle"}"
          title="${favorite ? "Favorilerden çıkar" : "Favorilere ekle"}"
        >
          <span aria-hidden="true">${favorite ? "♥" : "♡"}</span>
        </button>
      </div>
      <div class="plant-card__content">
        <span class="plant-card__badge">${tur}</span>
        <h4 class="plant-card__title">
          <a class="plant-card__title-link" href="${detailHref}">${ad}</a>
        </h4>
        <p class="plant-card__subtitle">${botanikAd}</p>
        <p class="plant-card__description">${description}</p>
        ${careMarkup}
      </div>
    </article>
  `;
};

// Son bakılanlar şeridindeki küçük kartı üretir.
export const createRecentCardMarkup = (plant) => {
  const ad = escapeHtml(plant.ad);
  const resimUrl = escapeHtml(plant.resimUrl);

  return `
    <a class="recent-card" href="detail.html?id=${Number(plant.id)}" title="${ad}">
      <img src="${resimUrl}" alt="${ad} görseli" width="48" height="48" loading="lazy" decoding="async" />
      <strong>${ad}</strong>
    </a>
  `;
};
