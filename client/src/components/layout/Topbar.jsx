import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.jsx";
import { useCart } from "../../context/CartContext.jsx";

export function Topbar({
  catalogMode = "products",
  searchValue,
  onSearchChange,
  onMenuToggle,
  menuOpen,
  onFavoritesClick,
  favoriteCount,
  isAdmin = false,
}) {
  const [menuOpenUser, setMenuOpenUser] = useState(false);
  const { user, isLoggedIn, logout } = useAuth();
  const { itemCount, closeCart } = useCart();
  const navigate = useNavigate();
  const dropdownRef = useRef(null);

  useEffect(() => {
    const onDocClick = (e) => {
      if (!dropdownRef.current?.contains(e.target)) {
        setMenuOpenUser(false);
      }
    };
    document.addEventListener("click", onDocClick);
    return () => document.removeEventListener("click", onDocClick);
  }, []);

  const displayName = user?.fullName || user?.firstName || "Misafir";

  const handleLogout = () => {
    logout();
    setMenuOpenUser(false);
    navigate("/");
  };

  const isPlants = catalogMode === "plants";

  return (
    <header className="topbar">
      <div className="topbar__left">
        <button
          className="menu-toggle"
          id="menuToggle"
          type="button"
          aria-label="Menüyü aç veya kapat"
          aria-expanded={menuOpen}
          aria-controls="sidebar"
          onClick={onMenuToggle}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <div>
          <h1>Şifa Hanım Aktar</h1>
          <p className="topbar__subtitle">
            {isPlants ? "Şifalı bitki kütüphanesi" : "Doğal ürünler & aktar vitrini"}
            {isAdmin ? " · Admin modu" : ""}
          </p>
        </div>
      </div>

      <div className="topbar__right">
        {!isPlants ? (
          <Link
            to="/sepet"
            className="topbar__cart"
            onClick={closeCart}
            aria-label={itemCount > 0 ? `Sepetim, ${itemCount} ürün` : "Sepetim"}
          >
            Sepet
            {itemCount > 0 ? <span className="topbar__cart-badge">{itemCount}</span> : null}
          </Link>
        ) : null}

        <label className="search-box" htmlFor="searchInput">
          <span className="visually-hidden">
            {isPlants ? "Bitki ara" : "Ürün ara"}. Kısayol: / odaklanır, Esc kapatır.
          </span>
          <span className="search-box__field">
            <input
              id="searchInput"
              type="search"
              name="q"
              placeholder={
                isPlants
                  ? "Bitki veya botanik adı ara... [/]"
                  : "Aktar ürünlerinde ara... [/]"
              }              autoComplete="off"
              enterKeyHint="search"
              value={searchValue}
              onChange={(e) => onSearchChange(e.target.value)}
            />
            <span className="search-box__shortcuts" aria-hidden="true">
              <kbd>/</kbd>
              <kbd>Esc</kbd>
            </span>
          </span>
        </label>

        <div className="user-menu" ref={dropdownRef}>
          <button
            className="user-menu__trigger"
            id="userMenuButton"
            type="button"
            aria-expanded={menuOpenUser}
            aria-haspopup="menu"
            aria-controls="userDropdown"
            aria-label="Kullanıcı menüsü"
            onClick={() => setMenuOpenUser((v) => !v)}
          >
            <img
              src="/assets/avatar-default.svg"
              alt=""
              width="44"
              height="44"
              decoding="async"
            />
            <span className="user-menu__name">{displayName}</span>
          </button>

          <div
            className="user-menu__dropdown"
            id="userDropdown"
            role="menu"
            hidden={!menuOpenUser}
          >
            {isLoggedIn ? (
              <>
                <Link
                  to="/profil"
                  className="dropdown-link"
                  role="menuitem"
                  onClick={() => setMenuOpenUser(false)}
                >
                  Profilim
                </Link>
                <button
                  className="dropdown-link dropdown-link--button"
                  id="favoritesMenuLink"
                  type="button"
                  role="menuitem"
                  onClick={() => {
                    setMenuOpenUser(false);
                    onFavoritesClick?.();
                  }}
                >
                  {favoriteCount > 0 ? `Favorilerim (${favoriteCount})` : "Favorilerim"}
                </button>
                <Link
                  to="/ayarlar"
                  className="dropdown-link"
                  id="settingsMenuLink"
                  role="menuitem"
                  onClick={() => setMenuOpenUser(false)}
                >
                  Ayarlar
                </Link>
                <Link
                  to="/iletisim"
                  className="dropdown-link"
                  role="menuitem"
                  onClick={() => setMenuOpenUser(false)}
                >
                  İletişim &amp; WhatsApp
                </Link>
                <button
                  className="dropdown-link dropdown-link--button"
                  id="logoutMenuLink"
                  type="button"
                  role="menuitem"
                  onClick={handleLogout}
                >
                  Oturumu Kapat
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/giris"
                  className="dropdown-link"
                  role="menuitem"
                  onClick={() => setMenuOpenUser(false)}
                >
                  Giriş Yap
                </Link>
                <Link
                  to="/kayit"
                  className="dropdown-link dropdown-link--button dropdown-link--accent"
                  role="menuitem"
                  onClick={() => setMenuOpenUser(false)}
                >
                  Hesap Aç
                </Link>
                <button
                  className="dropdown-link dropdown-link--button"
                  type="button"
                  role="menuitem"
                  onClick={() => {
                    setMenuOpenUser(false);
                    onFavoritesClick?.();
                  }}
                >
                  {favoriteCount > 0 ? `Favorilerim (${favoriteCount})` : "Favorilerim"}
                </button>
                <Link
                  to="/iletisim"
                  className="dropdown-link"
                  role="menuitem"
                  onClick={() => setMenuOpenUser(false)}
                >
                  İletişim &amp; WhatsApp
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

