import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import { applyDensityPreference } from "./lib/preferences.js";
import { purgeLegacyDemoProducts } from "./lib/products.js";

// Eski sitedeki tasarım sistemi (sırayla)
import "../../styles/tokens.css";
import "../../styles/base.css";
import "../../styles/layout.css";
import "../../styles/components.css";
import "../../styles/pages.css";
import "../../styles/responsive.css";

applyDensityPreference();
purgeLegacyDemoProducts();

const rootEl = document.getElementById("root");
if (!rootEl) {
  throw new Error("Kök öğe (#root) bulunamadı.");
}

try {
  createRoot(rootEl).render(
    <StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </StrictMode>
  );
} catch (err) {
  console.error(err);
  rootEl.innerHTML =
    '<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:1.5rem;text-align:center;font-family:system-ui,sans-serif;background:#fdfbf7;color:#4a3e3d">' +
    "<div><strong>Şifa Hanım Aktar</strong><p style='margin-top:0.75rem;opacity:0.85'>Sayfa açılamadı. Ctrl+Shift+R ile yenileyin.</p></div></div>";
}
