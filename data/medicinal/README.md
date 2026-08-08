# UYARI: Bu veri seti DOĞRULANMAMIŞTIR — sitede kullanılmaz

## Durum

Bu klasördeki dosyalar (`plants_part1..8.json`, `plants_all.json`) **doğrulanmış
bir kaynaktan alınmamıştır.** İçerik bir dil modeli tarafından üretilmiştir ve
hiçbir botanik/tıbbi veritabanına karşı denetlenmemiştir.

Bu nedenle:

- Bu dosyalar **sitede kullanılmaz.** `data/plants.json` artık pfaf.org
  kayıtlarından üretilmektedir (bkz. `scripts/build_site_from_pfaf.py`).
- Buradaki hiçbir metin kullanıcıya gösterilmemelidir.
- Buradaki bilgiler tıbbi karar için kullanılmamalıdır.

## Neden burada tutuluyor?

Yalnızca geçmiş kaydı ve karşılaştırma amacıyla saklanıyor. Silinmesi
serbesttir.

## Bilinen sorunlar

1. **Uydurma kaynak atfı (düzeltildi):** 5 kayıtta "PFAF kayıtlarında da
   anılır", "PFAF'ta da geçer" gibi ifadeler vardı. Bu ifadeler gerçek bir
   PFAF sorgusuna dayanmıyordu ve kaldırıldı. Metnin geri kalanı hâlâ
   doğrulanmamış durumdadır.
2. **Şablon dolgu alanları:** Siteye taşınırken coğrafya/mevsim ve
   bakım/yetiştirme alanları tüm bitkiler için aynı jenerik kalıpla
   dolduruluyordu. Bu alanlar artık PFAF verisinden türetiliyor.
3. **Etkinlik iddiaları denetlenmedi:** Fayda ve uyarı metinleri klinik bir
   kaynağa karşı kontrol edilmemiştir.

## Doğrulanmış veri nerede?

| Dosya | İçerik |
|-------|--------|
| `data/plants.json` | Sitede kullanılan, pfaf.org'dan üretilmiş veri |
| `data/pfaf/raw/*.json` | pfaf.org'dan çekilmiş ham kayıtlar (kaynak URL + çekim tarihi ile) |
| `data/pfaf/pfaf_index.json` | Hangi türün PFAF'ta bulunduğu / bulunmadığı |
| `data/unverified_plants.json` | PFAF'ta doğrulanamadığı için siteden çıkarılan bitkiler |

## Kaynak

Doğrulanmış veri: Plants For A Future — <https://pfaf.org>
İçerik © Plants For A Future (kayıtlı hayır kurumu, No. 1057719).
Her bitki kaydında kaynak URL'si ve çekim tarihi saklanır.
