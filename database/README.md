# Bitki Veritabani (SQLite)

Bu klasor sitenin **veri dolabidir**.

## Dosyalar

| Dosya | Ne ise yarar? |
|-------|----------------|
| `schema.sql` | Tablo tanimlari (raflar) |
| `bitki.db` | Gercek veritabani dosyasi (212 bitki burada) |

## Ilk kurulum

Proje klasorunde:

```powershell
python scripts/init_db.py
```

Bu komut:
1. `bitki.db` olusturur
2. Tablolari acar
3. `data/plants.json` icindeki veriyi aktarir

## Test sorgulari

```powershell
python scripts/db_query.py list
python scripts/db_query.py get 1
python scripts/db_query.py search papatya
python scripts/db_query.py tur "Tıbbi Bitkiler"
```

## Tablolar

### `bitkiler`
Her satir = 1 bitki.

Onemli sutunlar: `id`, `ad`, `botanik_ad`, `tur`, `resim_url`, `genel_tavsiye`

### `ornek_vakalar`
Her satir = 1 bitkinin PubMed deneyimi.

`bitki_id` sutunu hangi bitkiye ait oldugunu gosterir.

## Siteyi calistirma (SQLite'dan okur)

JSON yerine database kullanmak icin sunucuyu ac:

```powershell
python scripts/serve.py
```

Tarayicida: **http://127.0.0.1:8080**

Site once `/api/bitkiler` uzerinden SQLite'a sorar. Sunucu kapaliysa yedek olarak `plants.json` kullanilir.

