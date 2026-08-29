import { setMetaContent } from "./utils.js";
import { assetUrl } from "./assetUrl.js";

const SITE_NAME = "Şifa Hanım Aktar";
const SITE_TAGLINE = "Şifalı Bitki Kütüphanesi";
/** Google için tek ana adres (çift deploy duplicate content önlemi). */
export const CANONICAL_ORIGIN = "https://sifahanimaktar.vercel.app";
/** Arama sonuçları / paylaşım önizlemesi için marka logosu. */
export const SITE_LOGO_PATH = "/assets/brand/sifa-hanim-logo.png";
const DEFAULT_DESCRIPTION =
  "Şifa Hanım Aktar bitki kütüphanesi: şifalı bitkiler, tıbbi ve aromatik otlar. Ne işe yarar, nasıl kullanılır, nelere dikkat edilir — aktar rehberi.";

const JSON_LD_ID = "sifa-jsonld";

function absoluteUrl(path) {
  const base = CANONICAL_ORIGIN;
  if (!path) return base;
  if (/^https?:\/\//i.test(path)) return path;
  return `${base}${path.startsWith("/") ? path : `/${path}`}`;
}

function upsertMeta(attr, key, content) {
  if (!content) return;
  let el = document.querySelector(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement("meta");
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute("content", content);
}

function upsertLink(rel, href) {
  if (!href) return;
  let el = document.querySelector(`link[rel="${rel}"]`);
  if (!el) {
    el = document.createElement("link");
    el.setAttribute("rel", rel);
    document.head.appendChild(el);
  }
  el.setAttribute("href", href);
}

function setJsonLd(data) {
  let el = document.getElementById(JSON_LD_ID);
  if (!el) {
    el = document.createElement("script");
    el.id = JSON_LD_ID;
    el.type = "application/ld+json";
    document.head.appendChild(el);
  }
  el.textContent = JSON.stringify(data);
}

export function applyPageSeo({
  title,
  description,
  path = "/",
  imagePath = "/assets/plants/photos/01-matricaria-chamomilla.jpg",
  type = "website",
  jsonLd,
}) {
  const fullTitle = title.includes(SITE_NAME) ? title : `${title} | ${SITE_NAME}`;
  const desc = description || DEFAULT_DESCRIPTION;
  const url = absoluteUrl(path);
  const image = absoluteUrl(assetUrl(imagePath));

  document.title = fullTitle;
  setMetaContent('meta[name="description"]', desc);

  upsertMeta("property", "og:title", fullTitle);
  upsertMeta("property", "og:description", desc);
  upsertMeta("property", "og:type", type);
  upsertMeta("property", "og:url", url);
  upsertMeta("property", "og:image", image);
  upsertMeta("property", "og:locale", "tr_TR");
  upsertMeta("property", "og:site_name", SITE_NAME);

  upsertMeta("name", "twitter:card", "summary_large_image");
  upsertMeta("name", "twitter:title", fullTitle);
  upsertMeta("name", "twitter:description", desc);
  upsertMeta("name", "twitter:image", image);

  upsertLink("canonical", url);

  if (jsonLd) setJsonLd(jsonLd);
}

export function applyHomeSeo() {
  const base = CANONICAL_ORIGIN;
  const logoUrl = absoluteUrl(SITE_LOGO_PATH);
  applyPageSeo({
    title: `${SITE_NAME} — ${SITE_TAGLINE}`,
    description: DEFAULT_DESCRIPTION,
    path: "/",
    imagePath: SITE_LOGO_PATH,
    jsonLd: {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": `${base}/#organization`,
          name: SITE_NAME,
          alternateName: `${SITE_NAME} ${SITE_TAGLINE}`,
          url: base,
          description: DEFAULT_DESCRIPTION,
          logo: {
            "@type": "ImageObject",
            url: logoUrl,
            width: 512,
            height: 512,
          },
        },
        {
          "@type": "WebSite",
          "@id": `${base}/#website`,
          url: base,
          name: `${SITE_NAME} — ${SITE_TAGLINE}`,
          description: DEFAULT_DESCRIPTION,
          publisher: { "@id": `${base}/#organization` },
          inLanguage: "tr-TR",
          potentialAction: {
            "@type": "SearchAction",
            target: `${base}/?q={search_term_string}`,
            "query-input": "required name=search_term_string",
          },
        },
      ],
    },
  });
}

export function applyPlantSeo(plant) {
  if (!plant) return;
  const base = CANONICAL_ORIGIN;
  const desc = `${plant.ad}: ne işe yarar, nasıl kullanılır, nelere dikkat edilir. ${SITE_NAME} şifalı bitki rehberi.`;
  applyPageSeo({
    title: `${plant.ad} — ${SITE_TAGLINE}`,
    description: desc,
    path: `/bitki/${plant.id}`,
    imagePath: plant.resimUrl,
    type: "article",
    jsonLd: {
      "@context": "https://schema.org",
      "@type": "WebPage",
      name: `${plant.ad} | ${SITE_NAME}`,
      description: desc,
      url: `${base}/bitki/${plant.id}`,
      inLanguage: "tr-TR",
      isPartOf: { "@type": "WebSite", name: SITE_NAME, url: base },
      about: {
        "@type": "Thing",
        name: plant.ad,
        description: plant.saglikKullanim?.faydalari?.slice(0, 200) || desc,
      },
    },
  });
}
