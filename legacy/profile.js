import {
  formatJoinDate,
  getUserProfile,
  resetUserAvatar,
  updateUserProfile,
  validateAvatarFile,
  validateEmail,
  validateUsername
} from "./user-profile.js";
import { applyDensityPreference, getProfileCompletion } from "./preferences.js";
import { showToast } from "./toast.js";

const elements = {
  profilePageTitle: document.querySelector("#profilePageTitle"),
  profileAvatarPreview: document.querySelector("#profileAvatarPreview"),
  profileAvatarInput: document.querySelector("#profileAvatarInput"),
  removeAvatarButton: document.querySelector("#removeAvatarButton"),
  avatarFeedback: document.querySelector("#avatarFeedback"),
  summaryFullName: document.querySelector("#summaryFullName"),
  summaryTitle: document.querySelector("#summaryTitle"),
  summaryBio: document.querySelector("#summaryBio"),
  summaryUsername: document.querySelector("#summaryUsername"),
  summaryEmail: document.querySelector("#summaryEmail"),
  summaryJoinDate: document.querySelector("#summaryJoinDate"),
  completionPercent: document.querySelector("#completionPercent"),
  completionFill: document.querySelector("#completionFill"),
  completionBar: document.querySelector("#completionBar"),
  completionHint: document.querySelector("#completionHint"),
  viewFullName: document.querySelector("#viewFullName"),
  viewUsername: document.querySelector("#viewUsername"),
  viewEmail: document.querySelector("#viewEmail"),
  viewTitle: document.querySelector("#viewTitle"),
  viewBio: document.querySelector("#viewBio"),
  profileInfoView: document.querySelector("#profileInfoView"),
  profileForm: document.querySelector("#profileForm"),
  toggleEditButton: document.querySelector("#toggleEditButton"),
  cancelEditButton: document.querySelector("#cancelEditButton"),
  firstNameInput: document.querySelector("#firstNameInput"),
  lastNameInput: document.querySelector("#lastNameInput"),
  usernameInput: document.querySelector("#usernameInput"),
  emailInput: document.querySelector("#emailInput"),
  titleInput: document.querySelector("#titleInput"),
  joinDateInput: document.querySelector("#joinDateInput"),
  bioInput: document.querySelector("#bioInput"),
  profileFormFeedback: document.querySelector("#profileFormFeedback")
};

const state = {
  isEditing: false,
  profile: getUserProfile()
};

// Sayfayı güncel profil verisiyle başlatır.
const init = () => {
  applyDensityPreference();
  bindEvents();
  renderProfile();
};

// Profille ilgili tüm arayüz olaylarını bağlar.
const bindEvents = () => {
  elements.toggleEditButton?.addEventListener("click", () => {
    state.isEditing = true;
    elements.profileFormFeedback.textContent = "";
    fillForm(state.profile);
    syncEditMode();
  });

  elements.cancelEditButton?.addEventListener("click", () => {
    state.isEditing = false;
    elements.profileFormFeedback.textContent = "";
    syncEditMode();
  });

  elements.profileForm?.addEventListener("submit", (event) => {
    event.preventDefault();
    handleProfileSave();
  });

  elements.profileAvatarInput?.addEventListener("change", (event) => {
    handleAvatarChange(event.target.files?.[0]);
  });

  elements.removeAvatarButton?.addEventListener("click", () => {
    try {
      state.profile = resetUserAvatar();
      elements.avatarFeedback.textContent = "Profil fotoğrafı varsayılan görsele döndürüldü.";
      showToast("Profil fotoğrafı sıfırlandı.", "info");
      renderProfile();
    } catch (error) {
      elements.avatarFeedback.textContent = error.message || "Avatar sıfırlanamadı.";
      showToast(error.message || "Avatar sıfırlanamadı.", "error");
    }
  });
};

// Ana görünüm kartları ve form alanlarını profil verisiyle yeniler.
const renderProfile = () => {
  const { profile } = state;

  document.title = `${profile.fullName} | Profilim`;
  elements.profilePageTitle.textContent = profile.fullName;
  elements.profileAvatarPreview.src = profile.avatarUrl;
  elements.profileAvatarPreview.alt = `${profile.fullName} profil fotoğrafı`;
  elements.summaryFullName.textContent = profile.fullName;
  elements.summaryTitle.textContent = profile.title || "Ünvan belirtilmedi";
  elements.summaryBio.textContent = profile.bio || "Henüz bir biyografi eklenmemiş.";
  elements.summaryUsername.textContent = `@${profile.username}`;
  elements.summaryEmail.textContent = profile.email;
  elements.summaryJoinDate.textContent = formatJoinDate(profile.joinDate);
  elements.viewFullName.textContent = profile.fullName;
  elements.viewUsername.textContent = `@${profile.username}`;
  elements.viewEmail.textContent = profile.email;
  elements.viewTitle.textContent = profile.title || "Belirtilmedi";
  elements.viewBio.textContent = profile.bio || "Biyografi alanı boş.";

  renderCompletion(profile);
  fillForm(profile);
  syncEditMode();
};

// Profil tamamlanma çubuğunu günceller.
const renderCompletion = (profile) => {
  const completion = getProfileCompletion(profile);

  if (elements.completionPercent) {
    elements.completionPercent.textContent = `%${completion.percent}`;
  }

  if (elements.completionFill) {
    elements.completionFill.style.width = `${completion.percent}%`;
  }

  if (elements.completionBar) {
    elements.completionBar.setAttribute("aria-valuenow", String(completion.percent));
  }

  if (elements.completionHint) {
    const hints = [];
    if (completion.missingAvatar) {
      hints.push("kendi fotoğrafınızı yükleyin");
    }
    if (completion.missingBio) {
      hints.push("en az 20 karakterlik bir biyografi ekleyin");
    }

    elements.completionHint.textContent =
      completion.percent >= 100
        ? "Profil bilgileriniz tamamlandı."
        : hints.length
          ? `Tamamlamak için: ${hints.join(" ve ")}.`
          : `Profiliniz %${completion.percent} tamamlandı.`;
  }
};

// Form alanlarını mevcut profil verisiyle doldurur.
const fillForm = (profile) => {
  elements.firstNameInput.value = profile.firstName || "";
  elements.lastNameInput.value = profile.lastName || "";
  elements.usernameInput.value = profile.username || "";
  elements.emailInput.value = profile.email || "";
  elements.titleInput.value = profile.title || "";
  elements.joinDateInput.value = profile.joinDate || "";
  elements.bioInput.value = profile.bio || "";
};

// Görüntüleme ve düzenleme modları arasında geçiş yapar.
const syncEditMode = () => {
  elements.profileInfoView.hidden = state.isEditing;
  elements.profileForm.hidden = !state.isEditing;
  elements.toggleEditButton.textContent = state.isEditing
    ? "Düzenleme Modu Açık"
    : "Düzenleme Modunu Aç";
  elements.toggleEditButton.disabled = state.isEditing;
};

// Formdan gelen veriyi doğrulayıp yerel depoya kaydeder.
const handleProfileSave = () => {
  const firstName = elements.firstNameInput.value.trim();
  const lastName = elements.lastNameInput.value.trim();
  const username = elements.usernameInput.value.trim();
  const email = elements.emailInput.value.trim();

  if (!firstName || !lastName || !username || !email) {
    const message = "Ad, soyad, kullanıcı adı ve e-posta alanları zorunludur.";
    elements.profileFormFeedback.textContent = message;
    showToast(message, "error");
    return;
  }

  const usernameError = validateUsername(username);
  if (usernameError) {
    elements.profileFormFeedback.textContent = usernameError;
    showToast(usernameError, "error");
    return;
  }

  const emailError = validateEmail(email);
  if (emailError) {
    elements.profileFormFeedback.textContent = emailError;
    showToast(emailError, "error");
    return;
  }

  try {
    state.profile = updateUserProfile({
      firstName,
      lastName,
      fullName: `${firstName} ${lastName}`.trim(),
      username,
      email,
      title: elements.titleInput.value.trim(),
      joinDate: elements.joinDateInput.value || state.profile.joinDate,
      bio: elements.bioInput.value.trim()
    });

    state.isEditing = false;
    elements.profileFormFeedback.textContent = "Profil bilgileri başarıyla güncellendi.";
    showToast("Profil bilgileri başarıyla güncellendi.", "success");
    renderProfile();
  } catch (error) {
    elements.profileFormFeedback.textContent = error.message || "Profil kaydedilemedi.";
    showToast(error.message || "Profil kaydedilemedi.", "error");
  }
};

// Fotoğraf dosyasını kontrol eder, önizler ve yerel depoya kaydeder.
const handleAvatarChange = (file) => {
  const validationMessage = validateAvatarFile(file);

  if (validationMessage) {
    elements.avatarFeedback.textContent = validationMessage;
    elements.profileAvatarInput.value = "";
    showToast(validationMessage, "error");
    return;
  }

  const reader = new FileReader();

  reader.addEventListener("load", () => {
    try {
      state.profile = updateUserProfile({
        avatarUrl: reader.result,
        avatarType: "uploaded"
      });

      elements.avatarFeedback.textContent = "Yeni profil fotoğrafı yüklendi.";
      showToast("Yeni profil fotoğrafı yüklendi.", "success");
      renderProfile();
    } catch (error) {
      elements.avatarFeedback.textContent = error.message || "Profil fotoğrafı kaydedilemedi.";
      showToast(error.message || "Profil fotoğrafı kaydedilemedi.", "error");
    } finally {
      elements.profileAvatarInput.value = "";
    }
  });

  reader.addEventListener("error", () => {
    elements.avatarFeedback.textContent = "Görsel okunamadı. Lütfen başka bir dosya deneyin.";
    elements.profileAvatarInput.value = "";
    showToast("Görsel okunamadı.", "error");
  });

  reader.addEventListener("abort", () => {
    elements.avatarFeedback.textContent = "Görsel yükleme iptal edildi.";
    elements.profileAvatarInput.value = "";
    showToast("Görsel yükleme iptal edildi.", "info");
  });

  reader.readAsDataURL(file);
};

init();
