import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { showToast } from "../lib/toast.js";

export default function RegisterPage() {
  const { register, isLoggedIn } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const returnTo = params.get("return") || "/profil";

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);

  if (isLoggedIn) {
    navigate(returnTo, { replace: true });
    return null;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirm) {
      showToast("Şifreler eşleşmiyor.", "error");
      return;
    }
    setLoading(true);
    try {
      await register({ firstName, lastName, email, password });
      showToast("Hesap oluşturuldu.", "success");
      navigate(returnTo, { replace: true });
    } catch (err) {
      showToast(err.message || "Kayıt olunamadı.", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="detail-main auth-page" id="main-content" style={{ paddingTop: "2rem" }}>
      <header className="detail-header" style={{ position: "static", marginBottom: "1.5rem" }}>
        <Link className="back-button" to="/">
          Kataloğa Dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">Hesap</p>
          <h1>Kayıt Ol</h1>
        </div>
      </header>

      <section className="info-card auth-card">
        <p className="auth-card__lead">
          Ücretsiz hesap açın; favori bitkilerinizi kaydedin, profilinizi düzenleyin.
        </p>
        <form className="care-form" onSubmit={handleSubmit}>
          <label className="profile-field">
            <span>Ad</span>
            <input
              required
              autoComplete="given-name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Soyad</span>
            <input autoComplete="family-name" value={lastName} onChange={(e) => setLastName(e.target.value)} />
          </label>
          <label className="profile-field">
            <span>E-posta</span>
            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Şifre (en az 6 karakter)</span>
            <input
              type="password"
              required
              minLength={6}
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Şifre tekrar</span>
            <input
              type="password"
              required
              minLength={6}
              autoComplete="new-password"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
            />
          </label>
          <div className="profile-form-actions">
            <button className="back-button" type="submit" disabled={loading}>
              {loading ? "Kaydediliyor…" : "Hesap Aç"}
            </button>
          </div>
        </form>
        <p className="auth-card__footer">
          Zaten hesabınız var mı? <Link to={`/giris?return=${encodeURIComponent(returnTo)}`}>Giriş yapın</Link>
        </p>
      </section>
    </main>
  );
}
