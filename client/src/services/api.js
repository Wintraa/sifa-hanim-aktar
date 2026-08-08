/**
 * Merkezi API istemcisi.
 * Vite proxy sayesinde /api → http://127.0.0.1:4000
 */
const API_BASE = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const message = data?.error || `İstek başarısız (${response.status})`;
    throw new Error(message);
  }

  return data;
}

export const api = {
  getPlants: () => request("/bitkiler"),
  getPlant: (id) => request(`/bitkiler/${id}`),
  getMissingSearches: () => request("/bulunamayan-aramalar"),
  postMissingSearch: (arama) =>
    request("/bulunamayan-aramalar", {
      method: "POST",
      body: JSON.stringify({ arama }),
    }),
};
