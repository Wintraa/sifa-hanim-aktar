/**
 * Merkezi API istemcisi.
 * Vite proxy: /api → http://127.0.0.1:4000
 * Canlıda: Netlify Forms + yerel kuyruk yedeği.
 */
import { enqueueMissingSearch } from "../lib/missing-searches.js";
import {
  mergeProducts,
  PRODUCTS_CACHE_KEY,
  isValidProduct,
  purgeLegacyDemoProducts,
  syncCatalogImagesOverStaleOverrides,
} from "../lib/products.js";

const API_BASE = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json().catch(() => null)
    : null;

  if (!response.ok || data == null) {
    const message = data?.error || `İstek başarısız (${response.status})`;
    throw new Error(message);
  }

  return data;
}

const isValidPlant = (plant) =>
  plant &&
  Number.isInteger(Number(plant.id)) &&
  String(plant.ad || "").trim() &&
  String(plant.botanikAd || "").trim() &&
  String(plant.tur || "").trim();

const PLANTS_CACHE_KEY = "sifa-plants-v1";

function readPlantsCache() {
  try {
    const raw = sessionStorage.getItem(PLANTS_CACHE_KEY);
    if (!raw) return null;
    const list = JSON.parse(raw);
    return Array.isArray(list) ? list.filter(isValidPlant) : null;
  } catch {
    return null;
  }
}

function writePlantsCache(list) {
  try {
    sessionStorage.setItem(PLANTS_CACHE_KEY, JSON.stringify(list));
  } catch {
    /* kota doluysa sessizce devam */
  }
}

async function postMissingViaNetlifyForm(arama) {
  const body = new URLSearchParams({
    "form-name": "missing-searches",
    arama: String(arama).trim(),
    tarih: new Date().toISOString(),
  });
  const response = await fetch("/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  // Netlify 200/302 döner; SPA fallback bazen HTML 200 verir — yeterli
  if (!response.ok && response.status !== 302) {
    throw new Error("Form kaydı başarısız");
  }
}

async function postMissingViaVercelApi(arama) {
  const response = await fetch("/api/missing-searches", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ arama: String(arama).trim() }),
  });
  if (!response.ok) throw new Error("API kaydı başarısız");
}

export const api = {
  getPlants: () => request("/bitkiler"),
  getPlant: (id) => request(`/bitkiler/${id}`),
  getMissingSearches: () => request("/bulunamayan-aramalar"),

  async postMissingSearch(arama) {
    const q = String(arama || "").trim();
    if (q.length < 2) return { ok: false };

    // Her durumda yerel yedek
    enqueueMissingSearch(q);

    // 1) Yerel Express
    if (import.meta.env.DEV) {
      try {
        return await request("/bulunamayan-aramalar", {
          method: "POST",
          body: JSON.stringify({ arama: q }),
        });
      } catch {
        /* devam */
      }
    }

    // 2) Vercel serverless
    try {
      await postMissingViaVercelApi(q);
      return { ok: true };
    } catch {
      /* devam */
    }

    // 3) Netlify Forms
    try {
      await postMissingViaNetlifyForm(q);
      return { ok: true };
    } catch {
      return { ok: true, localOnly: true };
    }
  },

  /** API yoksa (Netlify gibi) plants.json yedeğine düşer. */
  async getPlantsWithFallback() {
    const cached = readPlantsCache();
    if (cached?.length) {
      return cached;
    }

    if (import.meta.env.DEV) {
      try {
        const data = await request("/bitkiler");
        if (Array.isArray(data) && data.length > 0) {
          return data.filter(isValidPlant);
        }
      } catch {
        // JSON yedeğine düş
      }
    }

    const response = await fetch("/data/plants.json");
    if (!response.ok) {
      throw new Error("Bitki verileri yüklenemedi.");
    }
    const data = await response.json();
    const list = Array.isArray(data) ? data : data?.plants;
    if (!Array.isArray(list)) {
      throw new Error("Bitki verisi geçersiz.");
    }
    const valid = list.filter(isValidPlant);
    writePlantsCache(valid);
    return valid;
  },

  async getPlantWithFallback(id) {
    const numId = Number(id);
    if (!Number.isInteger(numId) || numId <= 0) {
      throw new Error("Bitki bulunamadı.");
    }

    if (import.meta.env.DEV) {
      try {
        const data = await request(`/bitkiler/${numId}`);
        if (isValidPlant(data)) return data;
      } catch {
        // JSON yedeğine düş
      }
    }

    const all = await api.getPlantsWithFallback();
    const found = all.find((p) => Number(p.id) === numId);
    if (!found) throw new Error("Bitki bulunamadı.");
    return found;
  },

  async getProductsWithFallback() {
    purgeLegacyDemoProducts();
    syncCatalogImagesOverStaleOverrides();

    const response = await fetch("/data/products.json?v=aktar-v1", { cache: "no-store" });
    if (!response.ok) {
      throw new Error("Ürün verileri yüklenemedi.");
    }
    const data = await response.json();
    const list = Array.isArray(data) ? data : data?.products;
    if (!Array.isArray(list)) {
      throw new Error("Ürün verisi geçersiz.");
    }
    const merged = mergeProducts(list.filter(isValidProduct));
    try {
      sessionStorage.setItem(PRODUCTS_CACHE_KEY, JSON.stringify(merged));
    } catch {
      /* ignore */
    }
    return merged;
  },

  /** Tarayıcı override'ları ile anında birleştir (ağ beklemeden). */
  remergeProducts(baseList) {
    return mergeProducts(baseList.filter(isValidProduct));
  },

  async getProductWithFallback(id) {
    const numId = Number(id);
    if (!Number.isInteger(numId) || numId <= 0) {
      throw new Error("Ürün bulunamadı.");
    }
    const all = await api.getProductsWithFallback();
    const found = all.find((p) => Number(p.id) === numId);
    if (!found) throw new Error("Ürün bulunamadı.");
    return found;
  },
};
