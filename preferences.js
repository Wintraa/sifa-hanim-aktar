import { getFavorites, saveFavorites } from "./favorites.js";
import { getCareNotes, replaceCareNotes } from "./care-notes.js";
import { clearRecentPlants, getRecentPlantIds } from "./recent-plants.js";
import {
  getDefaultProfile,
  getUserProfile,
  saveUserProfile
} from "./user-profile.js";

const PREFERENCES_KEY = "dogalBitkilerTercihler";
const EXPORT_VERSION = 1;

const DEFAULT_PREFERENCES = {
  density: "comfortable"
};

// Liste yoğunluğu tercihini okur.
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
      density: parsed.density === "compact" ? "compact" : "comfortable"
    };
  } catch (error) {
    return { ...DEFAULT_PREFERENCES };
  }
};

// Tercihleri kaydeder.
export const savePreferences = (partial) => {
  const next = {
    ...getPreferences(),
    ...partial,
    density: partial?.density === "compact" ? "compact" : "comfortable"
  };

  try {
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(next));
    return { ok: true, preferences: next };
  } catch (error) {
    return { ok: false, error: "Tercihler kaydedilemedi." };
  }
};

// body öğesine yoğunluk sınıfını uygular.
export const applyDensityPreference = (density = getPreferences().density) => {
  document.body.dataset.density = density === "compact" ? "compact" : "comfortable";
};

// Profil tamamlanma yüzdesini hesaplar.
export const getProfileCompletion = (profile = getUserProfile()) => {
  const checks = [
    Boolean(profile.firstName?.trim()),
    Boolean(profile.lastName?.trim()),
    Boolean(profile.username?.trim()),
    Boolean(profile.email?.trim()),
    Boolean(profile.title?.trim()),
    Boolean(profile.bio?.trim()) && profile.bio.trim().length >= 20,
    Boolean(profile.joinDate),
    profile.avatarType === "uploaded"
  ];

  const filled = checks.filter(Boolean).length;
  const percent = Math.round((filled / checks.length) * 100);

  return {
    percent,
    filled,
    total: checks.length,
    missingAvatar: profile.avatarType !== "uploaded",
    missingBio: !(profile.bio?.trim() && profile.bio.trim().length >= 20)
  };
};

// Favori, profil, bakım notu ve tercihleri tek JSON olarak dışa aktarır.
export const exportUserData = () => {
  const payload = {
    version: EXPORT_VERSION,
    exportedAt: new Date().toISOString(),
    favorites: getFavorites(),
    profile: getUserProfile(),
    careNotes: getCareNotes(),
    recentPlantIds: getRecentPlantIds(),
    preferences: getPreferences()
  };

  return JSON.stringify(payload, null, 2);
};

// JSON dosyasından kullanıcı verisini içe aktarır.
export const importUserData = (jsonText) => {
  let parsed;

  try {
    parsed = JSON.parse(jsonText);
  } catch (error) {
    return { ok: false, error: "Geçersiz JSON dosyası." };
  }

  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    return { ok: false, error: "Dosya beklenen formatta değil." };
  }

  if (parsed.version && Number(parsed.version) !== EXPORT_VERSION) {
    return { ok: false, error: "Bu dışa aktarım sürümü desteklenmiyor." };
  }

  if (Array.isArray(parsed.favorites)) {
    saveFavorites(parsed.favorites);
  }

  if (parsed.profile && typeof parsed.profile === "object") {
    const result = saveUserProfile({
      ...getDefaultProfile(),
      ...parsed.profile
    });

    if (!result.ok) {
      return result;
    }
  }

  if (parsed.careNotes) {
    const careResult = replaceCareNotes(parsed.careNotes);
    if (!careResult.ok) {
      return careResult;
    }
  }

  if (parsed.preferences) {
    const prefResult = savePreferences(parsed.preferences);
    if (!prefResult.ok) {
      return prefResult;
    }
  }

  if (Array.isArray(parsed.recentPlantIds)) {
    try {
      localStorage.setItem(
        "dogalBitkilerSonBakilanlar",
        JSON.stringify(
          parsed.recentPlantIds.map(Number).filter((id) => Number.isInteger(id) && id > 0).slice(0, 6)
        )
      );
    } catch (error) {
      // Yok say.
    }
  }

  applyDensityPreference();
  return { ok: true };
};

export const resetLocalUserData = () => {
  saveFavorites([]);
  replaceCareNotes({});
  clearRecentPlants();
  savePreferences(DEFAULT_PREFERENCES);
  saveUserProfile(getDefaultProfile());
  applyDensityPreference();
};
