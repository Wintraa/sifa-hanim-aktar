/**
 * SQLite satırlarını frontend'in beklediği camelCase JSON'a çevirir.
 */
function parseJsonField(value) {
  if (!value) return null;
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function mapVaka(row) {
  if (!row) return null;
  return {
    baslik: row.baslik,
    sorun: row.sorun,
    yaklasim: row.yaklasim,
    sonuc: row.sonuc,
    anlatim: row.anlatim,
    pubmedId: row.pubmed_id || "",
    pubmedUrl: row.pubmed_url,
    makaleBasligi: row.makale_basligi,
    yil: row.yil || "",
    kaynakAdi: row.kaynak_adi,
  };
}

function mapPlant(row, vakaRow = null) {
  const plant = {
    id: row.id,
    ad: row.ad,
    botanikAd: row.botanik_ad,
    tur: row.tur,
    resimUrl: row.resim_url,
    genelTavsiyeMetni: row.genel_tavsiye,
  };

  if (row.eski_id != null) {
    plant.eskiId = row.eski_id;
  }

  const nested = [
    ["temel_bilgiler", "temelBilgiler"],
    ["saglik_kullanim", "saglikKullanim"],
    ["cografya_mevsim", "cografyaMevsim"],
    ["bakim_yetistirme", "bakimYetistirme"],
    ["kaynak", "kaynak"],
    ["pfaf_orijinal", "_pfafOrijinal"],
  ];

  for (const [dbKey, jsKey] of nested) {
    const parsed = parseJsonField(row[dbKey]);
    if (parsed != null) plant[jsKey] = parsed;
  }

  if (vakaRow) {
    plant.ornekVaka = mapVaka(vakaRow);
  }

  return plant;
}

module.exports = { mapPlant, mapVaka, parseJsonField };
