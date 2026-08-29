const FAVORITES_KEY_GUEST = "dogalBitkilerFavoriler";

function favoritesKey(userId) {
  if (userId) return `sifa_fav_${userId}`;
  return FAVORITES_KEY_GUEST;
}

export const getFavorites = (userId = null) => {
  try {
    const raw = localStorage.getItem(favoritesKey(userId));
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed)
      ? parsed.map(Number).filter((id) => Number.isInteger(id) && id > 0)
      : [];
  } catch {
    return [];
  }
};

export const saveFavorites = (ids, userId = null) => {
  try {
    localStorage.setItem(favoritesKey(userId), JSON.stringify([...new Set(ids)]));
  } catch {
    // Kota hatasında sessizce devam
  }
};

export const isFavorite = (plantId, userId = null) =>
  getFavorites(userId).includes(Number(plantId));

export const toggleFavorite = (plantId, userId = null) => {
  const id = Number(plantId);
  if (!Number.isInteger(id) || id <= 0) return false;
  const current = getFavorites(userId);
  const next = current.includes(id) ? current.filter((item) => item !== id) : [...current, id];
  saveFavorites(next, userId);
  return next.includes(id);
};

/** Misafir favorilerini giriş yapan hesaba taşır (birleştirir). */
export const mergeGuestFavoritesIntoUser = (userId) => {
  if (!userId) return;
  const guest = getFavorites(null);
  if (guest.length === 0) return;
  const userFavs = getFavorites(userId);
  saveFavorites([...new Set([...userFavs, ...guest])], userId);
  localStorage.removeItem(FAVORITES_KEY_GUEST);
};

/** Telefon değişiminde yedek almak için. */
export const exportFavoritesBackup = (userId = null) => ({
  version: 1,
  exportedAt: new Date().toISOString(),
  plantIds: getFavorites(userId),
});

export const importFavoritesBackup = (payload, userId = null) => {
  const ids = Array.isArray(payload?.plantIds)
    ? payload.plantIds.map(Number).filter((id) => Number.isInteger(id) && id > 0)
    : [];
  if (ids.length === 0) {
    throw new Error("Yedekte geçerli favori bulunamadı.");
  }
  const merged = [...new Set([...getFavorites(userId), ...ids])];
  saveFavorites(merged, userId);
  return merged.length;
};
