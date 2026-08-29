const FAVORITES_KEY = "dogalBitkilerFavoriler";

// Yerel depodan favori kimlik listesini okur.
export const getFavorites = () => {
  try {
    const raw = localStorage.getItem(FAVORITES_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed)
      ? parsed.map(Number).filter((id) => Number.isInteger(id) && id > 0)
      : [];
  } catch (error) {
    return [];
  }
};

// Favori listesini yerel depoya yazar.
export const saveFavorites = (ids) => {
  try {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify([...new Set(ids)]));
  } catch (error) {
    // Kota veya erişim hatasında uygulama çökmesin.
  }
};

// Belirli bir bitkinin favori olup olmadığını kontrol eder.
export const isFavorite = (plantId) => getFavorites().includes(Number(plantId));

// Favori durumunu aç/kapa yapar ve güncel durumu döndürür.
export const toggleFavorite = (plantId) => {
  const id = Number(plantId);

  if (!Number.isInteger(id) || id <= 0) {
    return false;
  }

  const current = getFavorites();
  const next = current.includes(id) ? current.filter((item) => item !== id) : [...current, id];
  saveFavorites(next);
  return next.includes(id);
};
