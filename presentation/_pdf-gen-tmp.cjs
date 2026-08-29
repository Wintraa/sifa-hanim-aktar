
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto("file:///C:/Users/musta/OneDrive/Desktop/Bitki/presentation/sifa-hanim-aktar-sunum.html", { waitUntil: 'networkidle0', timeout: 120000 });
  await page.pdf({
    path: "C:\\Users\\musta\\OneDrive\\Desktop\\Bitki\\presentation\\Sifa-Hanim-Aktar-Proje-Sunumu.pdf",
    format: 'A4',
    landscape: true,
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    preferCSSPageSize: true,
  });
  await browser.close();
  console.log('PDF yazıldı:', "C:\\Users\\musta\\OneDrive\\Desktop\\Bitki\\presentation\\Sifa-Hanim-Aktar-Proje-Sunumu.pdf");
})().catch((e) => { console.error(e); process.exit(1); });
