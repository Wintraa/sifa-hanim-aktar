const USER_PROFILE_KEY = "dogalBitkilerKullaniciProfili";

const DEFAULT_AVATAR = "assets/avatar-default.svg";

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
  avatarType: "default"
};

const ALLOWED_AVATAR_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);

// Varsayılan profilin paylaşılmayan bir kopyasını döndürür.
export const getDefaultProfile = () => {
  if (typeof structuredClone === "function") {
    return structuredClone(DEFAULT_PROFILE);
  }

  return JSON.parse(JSON.stringify(DEFAULT_PROFILE));
};

// Kayıtlı profili yerel depodan okur; yoksa varsayılanla birleştirir.
export const getUserProfile = () => {
  try {
    const raw = localStorage.getItem(USER_PROFILE_KEY);
    const parsed = raw ? JSON.parse(raw) : {};

    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return getDefaultProfile();
    }

    return {
      ...getDefaultProfile(),
      ...parsed
    };
  } catch (error) {
    return getDefaultProfile();
  }
};

// Profilin tamamını yerel depoya yazar.
export const saveUserProfile = (profile) => {
  try {
    localStorage.setItem(USER_PROFILE_KEY, JSON.stringify(profile));
    return { ok: true };
  } catch (error) {
    const isQuotaError =
      error?.name === "QuotaExceededError" ||
      error?.code === 22 ||
      error?.code === 1014;

    return {
      ok: false,
      error: isQuotaError
        ? "Depolama alanı doldu. Daha küçük bir görsel deneyin veya tarayıcı verilerini temizleyin."
        : "Profil kaydedilirken bir hata oluştu."
    };
  }
};

// Sadece güncellenen alanları birleştirip kaydeder.
export const updateUserProfile = (partialProfile) => {
  const nextProfile = {
    ...getUserProfile(),
    ...partialProfile
  };

  const result = saveUserProfile(nextProfile);

  if (!result.ok) {
    const error = new Error(result.error);
    error.code = "PROFILE_SAVE_FAILED";
    throw error;
  }

  return nextProfile;
};

// Kullanıcı avatarını varsayılan görsele geri alır.
export const resetUserAvatar = () =>
  updateUserProfile({
    avatarUrl: DEFAULT_AVATAR,
    avatarType: "default"
  });

// Tarihi okunabilir Türkiye biçimine çevirir.
export const formatJoinDate = (dateValue) => {
  try {
    return new Intl.DateTimeFormat("tr-TR", {
      day: "2-digit",
      month: "long",
      year: "numeric"
    }).format(new Date(dateValue));
  } catch (error) {
    return dateValue;
  }
};

// Profil fotoğrafı dosyasının temel kurallara uygun olup olmadığını denetler.
export const validateAvatarFile = (file) => {
  if (!file) {
    return "Lütfen bir görsel dosyası seçin.";
  }

  if (!ALLOWED_AVATAR_TYPES.has(file.type)) {
    return "Yalnızca JPG, PNG veya WEBP görselleri yükleyebilirsiniz.";
  }

  const maxSizeInBytes = 2 * 1024 * 1024;

  if (file.size > maxSizeInBytes) {
    return "Profil fotoğrafı en fazla 2 MB olabilir.";
  }

  return "";
};

// Kullanıcı adı formatını doğrular.
export const validateUsername = (username) => {
  const value = String(username ?? "").trim();

  if (value.length < 3 || value.length > 30) {
    return "Kullanıcı adı 3-30 karakter olmalıdır.";
  }

  if (!/^[a-zA-Z0-9._]+$/.test(value)) {
    return "Kullanıcı adı yalnızca harf, rakam, nokta ve alt çizgi içerebilir.";
  }

  return "";
};

// E-posta formatını doğrular.
export const validateEmail = (email) => {
  const value = String(email ?? "").trim();

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    return "Geçerli bir e-posta adresi girin.";
  }

  return "";
};
