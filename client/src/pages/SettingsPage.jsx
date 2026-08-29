import { useState } from "react";
import { Link } from "react-router-dom";
import {
  applyDensityPreference,
  getPreferences,
  savePreferences,
} from "../lib/preferences.js";
import { showToast } from "../lib/toast.js";

export default function SettingsPage() {
  const [density, setDensity] = useState(() => getPreferences().density);

  const handleDensity = (value) => {
    setDensity(value);
    savePreferences({ density: value });
    applyDensityPreference(value);
    showToast(
      value === "compact" ? "Kompakt görünüm açıldı." : "Rahat görünüm açıldı.",
      "success"
    );
  };

  return (
    <main className="detail-main" id="main-content" style={{ paddingTop: "2rem" }}>
      <header className="detail-header" style={{ position: "static", marginBottom: "1.5rem" }}>
        <Link className="back-button" to="/">
          Kataloğa Dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">Hesap</p>
          <h1>Ayarlar</h1>
        </div>
      </header>

      <section className="info-card">
        <h3>Liste yoğunluğu</h3>
        <p className="detail-description">
          Kart aralıklarını tarayıcınızda nasıl görmek istediğinizi seçin.
        </p>
        <div className="profile-form-actions" style={{ marginTop: "1rem" }}>
          <button
            className={`back-button${density === "comfortable" ? "" : " profile-tertiary-button"}`}
            type="button"
            onClick={() => handleDensity("comfortable")}
          >
            Rahat
          </button>
          <button
            className={`back-button${density === "compact" ? "" : " profile-tertiary-button"}`}
            type="button"
            onClick={() => handleDensity("compact")}
          >
            Kompakt
          </button>
        </div>
      </section>
    </main>
  );
}
