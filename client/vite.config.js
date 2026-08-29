import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** Canlıda CSS linkinin scriptten önce ve crossorigin'siz gelmesi (mobil/tarayıcı uyumu). */
function fixBuiltHtml() {
  return {
    name: "fix-built-html",
    transformIndexHtml(html) {
      let next = html.replace(
        /<link rel="stylesheet" crossorigin href="(\/assets\/[^"]+\.css)">/,
        '<link rel="stylesheet" href="$1">'
      );

      const cssLink = next.match(/<link rel="stylesheet" href="\/assets\/[^"]+\.css">/);
      const moduleScript = next.match(
        /<script type="module" crossorigin src="\/assets\/[^"]+\.js"><\/script>/
      );

      if (cssLink && moduleScript) {
        next = next.replace(cssLink[0], "").replace(moduleScript[0], `${cssLink[0]}\n    ${moduleScript[0]}`);
      }

      return next;
    },
  };
}

export default defineConfig({
  plugins: [react(), fixBuiltHtml()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    fs: {
      // Üst klasördeki styles/ dosyalarını import edebilmek için
      allow: [path.resolve(__dirname, "..")],
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:4000",
        changeOrigin: true,
      },
    },
  },
});
