import {
  applyDensityPreference,
  exportUserData,
  getPreferences,
  importUserData,
  resetLocalUserData,
  savePreferences
} from "./preferences.js";
import { showToast } from "./toast.js";

const elements = {
  tabs: document.querySelectorAll(".settings-tab"),
  panels: document.querySelectorAll(".settings-panel"),
  densityComfortable: document.querySelector("#densityComfortable"),
  densityCompact: document.querySelector("#densityCompact"),
  exportDataButton: document.querySelector("#exportDataButton"),
  importDataInput: document.querySelector("#importDataInput"),
  dataFeedback: document.querySelector("#dataFeedback"),
  resetDataButton: document.querySelector("#resetDataButton"),
  logoutButton: document.querySelector("#logoutButton")
};

const init = () => {
  applyDensityPreference();
  syncDensityInputs();
  bindEvents();
};

const bindEvents = () => {
  elements.tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      activateTab(tab.dataset.tab);
    });

    tab.addEventListener("keydown", (event) => {
      const supportedKeys = ["ArrowLeft", "ArrowRight", "Home", "End"];
      if (!supportedKeys.includes(event.key)) {
        return;
      }

      event.preventDefault();
      const tabs = [...elements.tabs];
      const currentIndex = tabs.indexOf(tab);
      const nextIndex =
        event.key === "Home"
          ? 0
          : event.key === "End"
            ? tabs.length - 1
            : (currentIndex + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) %
              tabs.length;

      tabs[nextIndex].focus();
      activateTab(tabs[nextIndex].dataset.tab);
    });
  });

  elements.densityComfortable?.addEventListener("change", () => {
    if (elements.densityComfortable.checked) {
      persistDensity("comfortable");
    }
  });

  elements.densityCompact?.addEventListener("change", () => {
    if (elements.densityCompact.checked) {
      persistDensity("compact");
    }
  });

  elements.exportDataButton?.addEventListener("click", () => {
    const blob = new Blob([exportUserData()], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    const stamp = new Date().toISOString().slice(0, 10);
    anchor.href = url;
    anchor.download = `dogal-bitkiler-yedek-${stamp}.json`;
    anchor.click();
    URL.revokeObjectURL(url);
    elements.dataFeedback.textContent = "Yedek dosyası indirildi.";
    showToast("Yedek dosyanız indirildi.", "success");
  });

  elements.importDataInput?.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    try {
      const text = await file.text();
      const result = importUserData(text);

      if (!result.ok) {
        elements.dataFeedback.textContent = result.error;
        showToast(result.error, "error");
        return;
      }

      syncDensityInputs();
      elements.dataFeedback.textContent = "Veriler başarıyla içe aktarıldı.";
      showToast("Veriler başarıyla içe aktarıldı.", "success");
    } catch (error) {
      elements.dataFeedback.textContent = "Dosya okunamadı.";
      showToast("Dosya okunamadı.", "error");
    } finally {
      elements.importDataInput.value = "";
    }
  });

  elements.resetDataButton?.addEventListener("click", () => {
    const confirmed = window.confirm(
      "Tüm yerel kullanıcı verisi silinecek. Bu işlem geri alınamaz. Devam edilsin mi?"
    );

    if (!confirmed) {
      return;
    }

    resetLocalUserData();
    syncDensityInputs();
    showToast("Yerel veri sıfırlandı.", "info");
  });

  elements.logoutButton?.addEventListener("click", () => {
    showToast("Oturum bu cihazda kapatıldı. Verileriniz yalnızca tarayıcınızda saklanır.", "info");
  });
};

const activateTab = (tabId) => {
  elements.tabs.forEach((tab) => {
    const active = tab.dataset.tab === tabId;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
    tab.tabIndex = active ? 0 : -1;
  });

  elements.panels.forEach((panel) => {
    const active = panel.dataset.panel === tabId;
    panel.hidden = !active;
    panel.classList.toggle("is-active", active);
  });
};

const syncDensityInputs = () => {
  const { density } = getPreferences();
  if (elements.densityComfortable) {
    elements.densityComfortable.checked = density !== "compact";
  }
  if (elements.densityCompact) {
    elements.densityCompact.checked = density === "compact";
  }
};

const persistDensity = (density) => {
  const result = savePreferences({ density });

  if (!result.ok) {
    showToast(result.error, "error");
    return;
  }

  applyDensityPreference(density);
  showToast(
    density === "compact" ? "Kompakt görünüm uygulandı." : "Ferah görünüm uygulandı.",
    "success"
  );
};

init();
