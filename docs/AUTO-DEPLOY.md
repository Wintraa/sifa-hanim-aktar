# Otomatik Git deploy rehberi (Netlify + Vercel)

## Nasil calisir?
1. Kodu GitHub `main` branch'ine push edersin
2. Netlify ve Vercel repo'yu izler, build alir, siteyi gunceller
3. Manuel `netlify deploy` gerekmez

## GitHub'a push (ilk kurulum)
```powershell
cd C:\Users\musta\OneDrive\Desktop\Bitki
git add .
git status
git commit -m "React vitrin, iletisim, hesap ve SEO guncellemeleri"
git push origin main
```

## Netlify — repo bagla
1. https://app.netlify.com → site: sifahanimaktar
2. **Site configuration → Build & deploy → Continuous deployment**
3. **Link repository** → GitHub → `Wintraa/sifa-hanim-aktar`
4. Branch: `main`
5. Build ayarlari `netlify.toml` dosyasindan otomatik gelir (base: client)
6. **Deploy site**

Her push sonrasi: Netlify → Deploys sekmesinde yeni build gorursun.

## Vercel — repo bagla
1. https://vercel.com/dashboard → proje `sifahanimaktar`
2. **Settings → Git**
3. **Connect Git Repository** → GitHub → `Wintraa/sifa-hanim-aktar`
4. Production branch: `main`
5. Build ayarlari `vercel.json` dosyasindan gelir

## Bundan sonra guncelleme
```powershell
git add .
git commit -m "Ne degisti kisa aciklama"
git push origin main
```
2-3 dakika icinde her iki site de guncellenir.

## Netlify Forms (bulunamayan arama)
Deploy sonrasi Netlify → **Forms** sekmesinde `missing-searches` formu gorunmeli.
