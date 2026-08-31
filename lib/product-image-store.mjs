/**
 * Ürün görselini data/products.json + assets/products/ içine kalıcı yazar.
 * Local: dosya sistemi. Vercel: GitHub Contents API (GITHUB_TOKEN gerekir).
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");

export function getRepoRoot() {
  return REPO_ROOT;
}

export function parseImagePayload(image) {
  const raw = String(image || "").trim();
  if (!raw) throw new Error("Görsel verisi boş.");

  if (raw.startsWith("data:")) {
    const comma = raw.indexOf(",");
    if (comma < 0) throw new Error("Geçersiz data URL.");
    const buffer = Buffer.from(raw.slice(comma + 1), "base64");
    if (!buffer.length) throw new Error("Görsel decode edilemedi.");
    return buffer;
  }

  const buffer = Buffer.from(raw, "base64");
  if (!buffer.length) throw new Error("Geçersiz base64 görsel.");
  return buffer;
}

export function resolveImageRelativePath(product) {
  const cleaned = String(product?.resimUrl || "")
    .trim()
    .split("?")[0]
    .replace(/^\//, "");
  if (cleaned.startsWith("assets/products/") && /\.(jpe?g|png|webp)$/i.test(cleaned)) {
    return cleaned;
  }
  const slug = String(product?.ad || "urun")
    .toLocaleLowerCase("tr")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 48);
  const id = String(product.id).padStart(2, "0");
  return `assets/products/${id}-${slug || "urun"}.jpg`;
}

export async function loadProductsJson(repoRoot = REPO_ROOT) {
  const filePath = path.join(repoRoot, "data", "products.json");
  const raw = await fs.readFile(filePath, "utf8");
  const list = JSON.parse(raw);
  if (!Array.isArray(list)) throw new Error("products.json geçersiz.");
  return list;
}

export async function saveProductsJson(products, repoRoot = REPO_ROOT) {
  const filePath = path.join(repoRoot, "data", "products.json");
  await fs.writeFile(filePath, `${JSON.stringify(products, null, 2)}\n`, "utf8");
}

async function mirrorToClientPublic(repoRoot, relPath, jsonProducts) {
  const publicAsset = path.join(repoRoot, "client", "public", relPath);
  const sourceAsset = path.join(repoRoot, relPath);
  await fs.mkdir(path.dirname(publicAsset), { recursive: true });
  await fs.copyFile(sourceAsset, publicAsset);

  const publicJson = path.join(repoRoot, "client", "public", "data", "products.json");
  await fs.mkdir(path.dirname(publicJson), { recursive: true });
  await fs.writeFile(publicJson, `${JSON.stringify(jsonProducts, null, 2)}\n`, "utf8");
}

export async function persistProductImageLocal(productId, imageBuffer, repoRoot = REPO_ROOT) {
  const products = await loadProductsJson(repoRoot);
  const idx = products.findIndex((p) => Number(p.id) === Number(productId));
  if (idx < 0) throw new Error("Ürün bulunamadı.");

  const product = products[idx];
  const relPath = resolveImageRelativePath(product);
  const absPath = path.join(repoRoot, ...relPath.split("/"));
  await fs.mkdir(path.dirname(absPath), { recursive: true });
  await fs.writeFile(absPath, imageBuffer);

  const version = `v${Date.now()}`;
  const resimUrl = `${relPath}?${version}`;
  products[idx] = { ...product, resimUrl };
  await saveProductsJson(products, repoRoot);
  await mirrorToClientPublic(repoRoot, relPath, products);

  return { id: Number(productId), resimUrl, path: relPath };
}

async function githubGetFile({ owner, repo, token, filePath }) {
  const url = `https://api.github.com/repos/${owner}/${repo}/contents/${filePath}`;
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
    },
  });
  if (res.status === 404) return null;
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`GitHub okuma hatası (${filePath}): ${err}`);
  }
  return res.json();
}

async function githubPutFile({ owner, repo, token, filePath, buffer, message, sha }) {
  const url = `https://api.github.com/repos/${owner}/${repo}/contents/${filePath}`;
  const body = {
    message,
    content: buffer.toString("base64"),
  };
  if (sha) body.sha = sha;

  const res = await fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "X-GitHub-Api-Version": "2022-11-28",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`GitHub yazma hatası (${filePath}): ${err}`);
  }
  return res.json();
}

export async function persistProductImageGitHub(productId, imageBuffer, options = {}) {
  const token = options.token || process.env.GITHUB_TOKEN;
  const repoFull = options.repo || process.env.GITHUB_REPO || "Wintraa/sifa-hanim-aktar";
  if (!token) {
    throw new Error("GITHUB_TOKEN tanımlı değil. Vercel ortam değişkenlerine ekleyin.");
  }

  const [owner, repo] = repoFull.split("/");
  if (!owner || !repo) throw new Error("GITHUB_REPO geçersiz.");

  const productsRaw = await githubGetFile({
    owner,
    repo,
    token,
    filePath: "data/products.json",
  });
  if (!productsRaw?.content) throw new Error("products.json GitHub'da bulunamadı.");

  const products = JSON.parse(Buffer.from(productsRaw.content, "base64").toString("utf8"));
  const idx = products.findIndex((p) => Number(p.id) === Number(productId));
  if (idx < 0) throw new Error("Ürün bulunamadı.");

  const product = products[idx];
  const relPath = resolveImageRelativePath(product);
  const version = `v${Date.now()}`;
  const resimUrl = `${relPath}?${version}`;
  products[idx] = { ...product, resimUrl };

  const imageExisting = await githubGetFile({ owner, repo, token, filePath: relPath });
  await githubPutFile({
    owner,
    repo,
    token,
    filePath: relPath,
    buffer: imageBuffer,
    message: `Ürün #${productId} görseli güncellendi`,
    sha: imageExisting?.sha,
  });

  await githubPutFile({
    owner,
    repo,
    token,
    filePath: "data/products.json",
    buffer: Buffer.from(`${JSON.stringify(products, null, 2)}\n`, "utf8"),
    message: `Ürün #${productId} resimUrl güncellendi`,
    sha: productsRaw.sha,
  });

  return { id: Number(productId), resimUrl, path: relPath, github: true };
}

export function verifyAdminKey(provided) {
  const expected = process.env.ADMIN_API_KEY || process.env.ADMIN_UPLOAD_SECRET || "99161202";
  return String(provided || "") === String(expected);
}
