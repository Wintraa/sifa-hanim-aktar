import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { showToast } from "../lib/toast.js";

export default function LoginPage() {
  const { login, isLoggedIn } = useAuth();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const returnTo = params.get("return") || "/profil";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  if (isLoggedIn) {
    navigate(returnTo, { replace: true });
    return null;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login({ email, password });
      showToast("Giriş yapıldı.", "success");
      navigate(returnTo, { replace: true });
    } catch (err) {
      showToast(err.message || "Giriş yapılamadı.", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="detail-main auth-page" id="main-content" style={{ paddingTop: "2rem" }}>
      <header className="detail-header" style={{ position: "static", marginBottom: "1.5rem" }}>
        <Link className="back-button" to="/bitkiler">
          Bitki kütüphanesine dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">Hesap</p>
          <h1>Giriş Yap</h1>
        </div>
      </header>

      <section className="info-card auth-card">
        <p className="auth-card__lead">
          Favorileriniz ve profiliniz hesabınıza bağlanır. Aynı cihazda tekrar giriş yapmanız gerekmez.
        </p>
        <form className="care-form" onSubmit={handleSubmit}>
          <label className="profile-field">
            <span>E-posta veya kullanıcı adı</span>
            <input
              type="text"
              autoComplete="username"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          <label className="profile-field">
            <span>Şifre</span>
            <input
              type="password"
              autoComplete="current-password"
              required
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <div className="profile-form-actions">
            <button className="back-button" type="submit" disabled={loading}>
              {loading ? "Giriş yapılıyor…" : "Giriş Yap"}
            </button>
          </div>
        </form>
        <p className="auth-card__footer">
          Hesabınız yok mu? <Link to={`/kayit?return=${encodeURIComponent(returnTo)}`}>Kayıt olun</Link>
        </p>
      </section>
    </main>
  );
}
