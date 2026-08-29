/**
 * HTML sunumunu PDF'e dönüştürür (Chrome headless).
 * Kullanım: node presentation/generate-pdf.mjs
 */
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(dir, "sifa-hanim-aktar-sunum.html");
const pdfPath = path.join(dir, "Sifa-Hanim-Aktar-Proje-Sunumu.pdf");

const chromePaths = [
  process.env.CHROME_PATH,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  `${process.env.LOCALAPPDATA}\\Google\\Chrome\\Application\\chrome.exe`,
].filter(Boolean);

const chrome = chromePaths.find((p) => fs.existsSync(p));
if (!chrome) {
  console.error("Chrome bulunamadı. HTML dosyasını tarayıcıda açıp Ctrl+P ile PDF kaydedin:");
  console.error(htmlPath);
  process.exit(1);
}

const fileUrl = `file:///${htmlPath.replace(/\\/g, "/")}`;
const result = spawnSync(
  chrome,
  ["--headless=new", "--disable-gpu", "--no-pdf-header-footer", `--print-to-pdf=${pdfPath}`, fileUrl],
  { encoding: "utf-8" }
);

if (result.status !== 0 || !fs.existsSync(pdfPath)) {
  console.error(result.stderr || result.stdout);
  process.exit(1);
}

const sizeKb = Math.round(fs.statSync(pdfPath).size / 1024);
console.log(`PDF hazır: ${pdfPath} (${sizeKb} KB)`);
