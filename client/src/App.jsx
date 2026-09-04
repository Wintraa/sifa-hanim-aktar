import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext.jsx";
import { FavoritesProvider } from "./context/FavoritesContext.jsx";
import { CartProvider } from "./context/CartContext.jsx";
import { CartDrawer } from "./components/catalog/CartDrawer.jsx";
import HomePage from "./pages/HomePage.jsx";
import ProductsPage from "./pages/ProductsPage.jsx";
import ProductDetailPage from "./pages/ProductDetailPage.jsx";
import CartPage from "./pages/CartPage.jsx";
import DetailPage from "./pages/DetailPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";
import ContactPage from "./pages/ContactPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";

export default function App() {
  return (
    <AuthProvider>
      <FavoritesProvider>
        <CartProvider>
          <Routes>
            <Route path="/" element={<ProductsPage />} />
            <Route path="/bitkiler" element={<HomePage />} />
            <Route path="/urun/:id" element={<ProductDetailPage />} />
            <Route path="/sepet" element={<CartPage />} />
            <Route path="/bitki/:id" element={<DetailPage />} />
            <Route path="/profil" element={<ProfilePage />} />
            <Route path="/ayarlar" element={<SettingsPage />} />
            <Route path="/iletisim" element={<ContactPage />} />
            <Route path="/giris" element={<LoginPage />} />
            <Route path="/kayit" element={<RegisterPage />} />
          </Routes>
          <CartDrawer />
        </CartProvider>
      </FavoritesProvider>
    </AuthProvider>
  );
}
