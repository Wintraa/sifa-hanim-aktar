const USER_PROFILE_KEY = "dogalBitkilerKullaniciProfili";
const DEFAULT_AVATAR = "/assets/avatar-default.svg";

const DEFAULT_PROFILE = {
  fullName: "Okuyucu",
  firstName: "Okuyucu",
  lastName: "",
  username: "okuyucu",
  email: "",
  title: "Öğrenci",
  bio: "Bu ansiklopedi üzerinden tıbbi, aromatik ve süs bitkilerini inceliyorum.",
  joinDate: "2024-03-18",
  avatarUrl: DEFAULT_AVATAR,
  avatarType: "default",
};

export const getDefaultProfile = () => JSON.parse(JSON.stringify(DEFAULT_PROFILE));

export const getUserProfile = () => {
  try {
    const raw = localStorage.getItem(USER_PROFILE_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return getDefaultProfile();
    }
    const profile = { ...getDefaultProfile(), ...parsed };
    // Eski göreli yolu React public köküne uyarla
    if (profile.avatarUrl === "assets/avatar-default.svg") {
      profile.avatarUrl = DEFAULT_AVATAR;
    }
    return profile;
  } catch {
    return getDefaultProfile();
  }
};

export const saveUserProfile = (profile) => {
  try {
    localStorage.setItem(USER_PROFILE_KEY, JSON.stringify(profile));
    return { ok: true };
  } catch (error) {
    const isQuota =
      error?.name === "QuotaExceededError" || error?.code === 22 || error?.code === 1014;
    return {
      ok: false,
      error: isQuota
        ? "Depolama alanı doldu."
        : "Profil kaydedilirken bir hata oluştu.",
    };
  }
};

export const updateUserProfile = (partialProfile) => {
  const nextProfile = { ...getUserProfile(), ...partialProfile };
  const result = saveUserProfile(nextProfile);
  if (!result.ok) {
    const error = new Error(result.error);
    error.code = "PROFILE_SAVE_FAILED";
    throw error;
  }
  return nextProfile;
};

export const formatJoinDate = (dateValue) => {
  try {
    return new Intl.DateTimeFormat("tr-TR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    }).format(new Date(dateValue));
  } catch {
    return dateValue;
  }
};
