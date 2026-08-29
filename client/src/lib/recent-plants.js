const RECENT_KEY = "dogalBitkilerSonBakilanlar";
const MAX_RECENT = 6;

export const getRecentPlantIds = () => {
  try {
    const raw = localStorage.getItem(RECENT_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed)
      ? parsed.map(Number).filter((id) => Number.isInteger(id) && id > 0).slice(0, MAX_RECENT)
      : [];
  } catch {
    return [];
  }
};

export const addRecentPlant = (plantId) => {
  const id = Number(plantId);
  if (!Number.isInteger(id) || id <= 0) return getRecentPlantIds();
  const next = [id, ...getRecentPlantIds().filter((item) => item !== id)].slice(0, MAX_RECENT);
  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify(next));
  } catch {
    // sessiz
  }
  return next;
};

export const clearRecentPlants = () => {
  try {
    localStorage.removeItem(RECENT_KEY);
  } catch {
    // yok say
  }
};
