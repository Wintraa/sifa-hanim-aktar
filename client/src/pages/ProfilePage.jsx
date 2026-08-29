import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFavorites } from "../context/FavoritesContext.jsx";
import { formatJoinDate } from "../lib/user-profile.js";
import { exportFavoritesBackup, importFavoritesBackup } from "../lib/favorites.js";
import { showToast } from "../lib/toast.js";

export default function ProfilePage() {
  const { user, isLoggedIn, updateProfile } = useAuth();
  const { refresh, favoriteCount } = useFavorites();
  const navigate = useNavigate();
  const fileRef = useRef(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/giris?return=/profil", { replace: true });
      return;
    }
    setFirstName(user?.firstName || "");
    setLastName(user?.lastName || "");
  }, [isLoggedIn, user, navigate]);

  if (!isLoggedIn || !user) {
    return null;
  }

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateProfile({
        firstName: firstName.trim() || "Üye",
        lastName: lastName.trim(),
      });
      showToast("Profil güncellendi.", "success");
    } catch (err) {
      showToast(err.message || "Kaydedilemedi.", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleExport = () => {
    const backup = exportFavoritesBackup(user.id);
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `sifa-favoriler-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast(`${backup.plantIds.length} favori dışa aktarıldı.`, "success");
  };

  const handleImport = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      const count = importFavoritesBackup(data, user.id);
      refresh();
      showToast(`${count} favori yüklendi.`, "success");
    } catch (err) {
      showToast(err.message || "Yedek okunamadı.", "error");
    }
  };

  return (
    <main className="detail-main" id="main-content" style={{ paddingTop: "2rem" }}>
      <header className="detail-header" style={{ position: "static", marginBottom: "1.5rem" }}>
        <Link className="back-button" to="/">
          Kataloğa Dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">Hesabım</p>
          <h1>Profil</h1>
        </div>
      </header>

      <section className="info-card">
        <div style={{ display: "flex", gap: "1rem", alignItems: "center", marginBottom: "1.25rem" }}>
          <img
            src="/assets/avatar-default.svg"
            alt=""
            width="72"
            height="72"
            style={{ borderRadius: "50%" }}
          />
          <div>
            <strong>{user.fullName}</strong>
            <p className="detail-subtitle" style={{ margin: 0 }}>
              {user.email}
            </p>
            <p className="detail-subtitle" style={{ margin: 0 }}>
              Üyelik: {formatJoinDate(user.joinDate)} · {favoriteCount} favori
            </p>
          </div>
        </div>

        <form className="care-form" onSubmit={handleSave}>
          <label className="profile-field">
            <span>Ad</span>
            <input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
          </label>
          <label className="profile-field">
            <span>Soyad</span>
            <input value={lastName} onChange={(e) => setLastName(e.target.value)} />
          </label>
          <div className="profile-form-actions">
            <button className="back-button" type="submit" disabled={saving}>
              {saving ? "Kaydediliyor…" : "Kaydet"}
            </button>
          </div>
        </form>
      </section>

      <section className="info-card" style={{ marginTop: "1.25rem" }}>
        <h3>Favori yedeği</h3>
        <p className="detail-description">
          Telefon değişince favoriler kaybolmasın diye JSON yedek alın. Yeni telefonda bu dosyayı
          içe aktarın.
        </p>
        <div className="profile-form-actions">
          <button className="back-button" type="button" onClick={handleExport}>
            Favorileri dışa aktar
          </button>
          <button
            className="profile-tertiary-button"
            type="button"
            onClick={() => fileRef.current?.click()}
          >
            Yedekten yükle
          </button>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            hidden
            onChange={handleImport}
          />
        </div>
      </section>
    </main>
  );
}
