/**
 * Netlify / Vercel / production build öncesi:
 * - Bitki fotoğraflarını client/public/assets altına kopyala
 *   (Windows junction Linux'ta çalışmaz)
 * - plants.json yedeğini public/data altına koy
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const clientRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = path.resolve(clientRoot, "..");

const destAssets = path.join(clientRoot, "public", "assets");
const destData = path.join(clientRoot, "public", "data");
const srcAssets = path.join(repoRoot, "assets");
const srcJson = path.join(repoRoot, "data", "plants.json");
const srcProducts = path.join(repoRoot, "data", "products.json");

/** Windows junction / bozuk symlink varsa kaldır, sonra klasör aç. */
function ensureRealDir(dir) {
  try {
    const st = fs.lstatSync(dir);
    if (st.isSymbolicLink()) {
      fs.unlinkSync(dir);
    } else if (!st.isDirectory()) {
      fs.rmSync(dir, { force: true });
    }
  } catch (err) {
    if (err.code !== "ENOENT") throw err;
  }
  fs.mkdirSync(dir, { recursive: true });
}

ensureRealDir(path.join(clientRoot, "public"));
ensureRealDir(destData);

if (!fs.existsSync(srcJson)) {
  throw new Error(`plants.json bulunamadı: ${srcJson}`);
}
fs.copyFileSync(srcJson, path.join(destData, "plants.json"));

if (!fs.existsSync(srcProducts)) {
  throw new Error(`products.json bulunamadı: ${srcProducts}`);
}
fs.copyFileSync(srcProducts, path.join(destData, "products.json"));

if (!fs.existsSync(srcAssets)) {
  throw new Error(`assets klasörü bulunamadı: ${srcAssets}`);
}

// Junction varsa kaldır; Vercel'de bozuk symlink bırakmasın
try {
  const st = fs.lstatSync(destAssets);
  if (st.isSymbolicLink()) {
    fs.unlinkSync(destAssets);
  }
} catch (err) {
  if (err.code !== "ENOENT") throw err;
}

ensureRealDir(destAssets);

const sameAssets =
  fs.existsSync(destAssets) &&
  fs.existsSync(srcAssets) &&
  fs.realpathSync(srcAssets) === fs.realpathSync(destAssets);

if (!sameAssets) {
  // İçini temizleyip kopyala (hedef gerçek klasör)
  for (const name of fs.readdirSync(destAssets)) {
    fs.rmSync(path.join(destAssets, name), { recursive: true, force: true });
  }
  fs.cpSync(srcAssets, destAssets, { recursive: true, force: true });
}

console.log("public hazır:", destAssets, destData);
