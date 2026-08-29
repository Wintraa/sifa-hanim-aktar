const PREFERENCES_KEY = "dogalBitkilerTercihler";
const DEFAULT_PREFERENCES = { density: "comfortable" };

export const getPreferences = () => {
  try {
    const raw = localStorage.getItem(PREFERENCES_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return { ...DEFAULT_PREFERENCES };
    }
    return {
      ...DEFAULT_PREFERENCES,
      ...parsed,
      density: parsed.density === "compact" ? "compact" : "comfortable",
    };
  } catch {
    return { ...DEFAULT_PREFERENCES };
  }
};

export const savePreferences = (partial) => {
  const next = { ...getPreferences(), ...partial };
  try {
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(next));
  } catch {
    // sessiz
  }
  return next;
};

export const applyDensityPreference = (density = getPreferences().density) => {
  document.body.dataset.density = density === "compact" ? "compact" : "comfortable";
};
