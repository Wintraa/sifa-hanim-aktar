# Şifa Hanım Aktar — React + Express + SQLite

## Klasör hiyerarşisi

```
Bitki/
├── database/
│   └── bitki.db                 # Mevcut SQLite dosyası
├── server/                      # Node.js + Express API
│   ├── config/
│   │   └── database.js          # better-sqlite3 bağlantı + şema
│   ├── db/
│   │   └── mappers.js           # Satır → JSON dönüşümü
│   ├── controllers/
│   │   ├── plantsController.js
│   │   └── missingSearchesController.js
│   ├── routes/
│   │   ├── plants.js
│   │   └── missingSearches.js
│   ├── server.js                # Giriş noktası
│   └── package.json
└── client/                      # React (Vite)
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── App.css
        ├── index.css
        ├── services/
        │   └── api.js           # Merkezi fetch
        └── components/
            ├── PlantList.jsx
            └── MissingSearchForm.jsx
```

## API uçları

| Method | URL | Açıklama |
|--------|-----|----------|
| GET | `/api/bitkiler` | Tüm bitkiler (+ örnek vaka) |
| GET | `/api/bitkiler/:id` | Tek bitki |
| GET | `/api/bulunamayan-aramalar` | Eksik aramalar |
| POST | `/api/bulunamayan-aramalar` | `{ "arama": "..." }` |

SQLite erişimi: Node.js yerleşik `node:sqlite` (C++ derlemesi gerekmez).

## Çalıştırma

**1) Node.js 20+ kurulu olmalı.**

**2) Backend**
```powershell
cd server
npm install
npm run start
```
→ http://127.0.0.1:4000

**3) Frontend (ayrı terminal)**
```powershell
cd client
npm install
npm run dev
```
→ http://127.0.0.1:5173

Vite, `/api` isteklerini otomatik 4000 portuna proxy eder.

## Kalıcı ürün görseli (admin)

`POST /api/products/image?id=42` — body: `{ "image": "data:image/jpeg;base64,..." }`  
Header: `X-Admin-Key: 99161202` (veya `ADMIN_API_KEY` ortam değişkeni)

Local Express diske yazar: `assets/products/` + `data/products.json`.

**Vercel (canlı):** aynı uç GitHub'a commit atar. Ortam değişkenleri:

| Değişken | Açıklama |
|----------|----------|
| `GITHUB_TOKEN` | repo yazma yetkili PAT |
| `GITHUB_REPO` | `Wintraa/sifa-hanim-aktar` |
| `ADMIN_API_KEY` | admin yükleme şifresi (opsiyonel) |

Deploy bitince herkes yeni görseli görür.
