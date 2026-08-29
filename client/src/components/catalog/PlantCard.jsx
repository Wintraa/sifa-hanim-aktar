import { Link } from "react-router-dom";
import { getCareNote } from "../../lib/care-notes.js";
import { assetUrl } from "../../lib/assetUrl.js";
import { useFavorites } from "../../context/FavoritesContext.jsx";

const truncateText = (text, length) => {
  const value = String(text ?? "").trim();
  if (value.length <= length) return value;
  const slice = value.slice(0, length);
  const sentenceEnd = Math.max(
    slice.lastIndexOf(". "),
    slice.lastIndexOf("! "),
    slice.lastIndexOf("? ")
  );
  if (sentenceEnd >= Math.floor(length * 0.45)) {
    return slice.slice(0, sentenceEnd + 1).trim();
  }
  const wordEnd = slice.lastIndexOf(" ");
  const cut = wordEnd > 40 ? slice.slice(0, wordEnd) : slice;
  return `${cut.trim()}…`;
};

const escapeRegExp = (value) => String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const stripLeadingPlantName = (text, ad, botanikAd) => {
  let value = String(text ?? "").trim();
  if (!value) return "";
  const patterns = [
    new RegExp(`^${escapeRegExp(ad)}\\s*\\(\\s*${escapeRegExp(botanikAd)}\\s*\\)\\s*[,:—\\-–]?\\s*`, "i"),
    new RegExp(`^${escapeRegExp(ad)}\\s*[,:—\\-–]?\\s*`, "i"),
  ];
  for (const pattern of patterns) {
    value = value.replace(pattern, "");
  }
  value = value.trim();
  if (!value) return "";
  const first = value.charAt(0);
  const rest = value.slice(1);
  const upperMap = { i: "İ", ı: "I", ş: "Ş", ğ: "Ğ", ü: "Ü", ö: "Ö", ç: "Ç" };
  const upper = upperMap[first] || first.toLocaleUpperCase("tr");
  return upper + rest;
};

export function PlantCard({ plant, visibleIndex = 0, showCare = false }) {
  const { isFavorite, toggle } = useFavorites();
  const favorite = isFavorite(plant.id);
  const medicinal = plant.tur === "Tıbbi Bitkiler";
  const detailHref = `/bitki/${plant.id}`;
  const rawDescription = stripLeadingPlantName(
    plant.genelTavsiyeMetni,
    plant.ad,
    plant.botanikAd
  );
  const description = truncateText(rawDescription, 180);
  const care = getCareNote(plant.id);

  return (
    <article className="plant-card">
      <div className="plant-card__media">
        <Link
          className="plant-card__image-link"
          to={detailHref}
          aria-label={`${plant.ad} ayrıntılarını aç`}
        >
          <img
            className="plant-card__image"
            src={assetUrl(plant.resimUrl)}
            alt={`${plant.ad} görseli`}
            width="640"
            height="480"
            loading={visibleIndex < 3 ? "eager" : "lazy"}
            decoding="async"
            {...(visibleIndex === 0 ? { fetchPriority: "high" } : {})}
          />
        </Link>
        <button
          className={`favorite-button${favorite ? " is-active" : ""}`}
          type="button"
          aria-pressed={favorite}
          aria-label={favorite ? "Favorilerden çıkar" : "Favorilere ekle"}
          title={favorite ? "Favorilerden çıkar" : "Favorilere ekle"}
          onClick={(e) => {
            e.preventDefault();
            const btn = e.currentTarget;
            btn.classList.remove("is-pulsing");
            void btn.offsetWidth;
            btn.classList.add("is-pulsing");
            toggle(plant.id);
          }}
        >
          <span aria-hidden="true">{favorite ? "♥" : "♡"}</span>
        </button>
      </div>
      <div className="plant-card__content">
        <span className="plant-card__badge">{plant.tur}</span>
        <h4 className="plant-card__title">
          <Link className="plant-card__title-link" to={detailHref}>
            {plant.ad}
          </Link>
        </h4>
        <p className="plant-card__subtitle">
          {plant.temelBilgiler?.bitkiTuru || "Şifa kullanımı"}
        </p>
        <p className="plant-card__description">{description}</p>
        {showCare && !medicinal && care ? (
          <p className="plant-card__care">
            Her {care.intervalDays} günde bir sulama
            {care.note ? ` · ${care.note}` : ""}
          </p>
        ) : null}
      </div>
    </article>
  );
}
