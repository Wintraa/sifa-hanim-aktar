// Bitki verisini tek noktadan yükler.
// Önce SQLite API (/api/bitkiler), olmazsa plants.json yedek.
const API_URL = "/api/bitkiler";
const FALLBACK_URL = "data/plants.json";

let plantsPromise;

const isPlantRecord = (plant) =>
  Boolean(
    plant &&
      Number.isInteger(Number(plant.id)) &&
      typeof plant.ad === "string" &&
      typeof plant.botanikAd === "string" &&
      typeof plant.tur === "string"
  );

const loadFromJson = () =>
  fetch(FALLBACK_URL, { cache: "no-cache" }).then((response) => {
    if (!response.ok) {
      throw new Error("Bitki verileri yüklenemedi.");
    }
    return response.json();
  });

const loadFromApi = () =>
  fetch(API_URL, { cache: "no-cache" }).then((response) => {
    if (!response.ok) {
      throw new Error("API yanıt vermedi.");
    }
    return response.json();
  });

const validatePlants = (payload) => {
  if (!Array.isArray(payload) || !payload.every(isPlantRecord)) {
    throw new Error("Bitki verisi beklenen formatta değil.");
  }
  return payload;
};

export const getPlants = async () => {
  if (!plantsPromise) {
    plantsPromise = loadFromApi()
      .then(validatePlants)
      .catch(() => loadFromJson().then(validatePlants))
      .catch((error) => {
        plantsPromise = undefined;
        throw error;
      });
  }

  return plantsPromise;
};
