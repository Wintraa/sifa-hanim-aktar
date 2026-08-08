const CARE_NOTES_KEY = "dogalBitkilerBakimNotlari";

// Tüm bakım notlarını okur.
export const getCareNotes = () => {
  try {
    const raw = localStorage.getItem(CARE_NOTES_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch (error) {
    return {};
  }
};

// Belirli bir bitkinin bakım notunu döndürür.
export const getCareNote = (plantId) => {
  const notes = getCareNotes();
  const note = notes[String(plantId)];
  return note && typeof note === "object" ? note : null;
};

// Bitki için sulama aralığı / not kaydeder.
export const saveCareNote = (plantId, payload) => {
  const id = Number(plantId);

  if (!Number.isInteger(id) || id <= 0) {
    return { ok: false, error: "Geçersiz bitki kimliği." };
  }

  const intervalDays = Number(payload?.intervalDays);
  const note = String(payload?.note ?? "").trim().slice(0, 160);

  if (!Number.isInteger(intervalDays) || intervalDays < 1 || intervalDays > 60) {
    return { ok: false, error: "Sulama aralığı 1–60 gün arasında olmalıdır." };
  }

  const all = getCareNotes();
  all[String(id)] = {
    intervalDays,
    note,
    updatedAt: new Date().toISOString()
  };

  try {
    localStorage.setItem(CARE_NOTES_KEY, JSON.stringify(all));
    return { ok: true, note: all[String(id)] };
  } catch (error) {
    return { ok: false, error: "Bakım notu kaydedilemedi." };
  }
};

// Bitkinin bakım notunu siler.
export const removeCareNote = (plantId) => {
  const all = getCareNotes();
  delete all[String(plantId)];

  try {
    localStorage.setItem(CARE_NOTES_KEY, JSON.stringify(all));
    return { ok: true };
  } catch (error) {
    return { ok: false, error: "Bakım notu silinemedi." };
  }
};

export const replaceCareNotes = (notes) => {
  const safe =
    notes && typeof notes === "object" && !Array.isArray(notes) ? notes : {};

  try {
    localStorage.setItem(CARE_NOTES_KEY, JSON.stringify(safe));
    return { ok: true };
  } catch (error) {
    return { ok: false, error: "Bakım notları içe aktarılamadı." };
  }
};
