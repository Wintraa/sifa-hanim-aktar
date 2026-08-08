import { useEffect, useMemo, useState } from "react";
import { api } from "./services/api.js";
import { PlantList } from "./components/PlantList.jsx";
import { MissingSearchForm } from "./components/MissingSearchForm.jsx";
import "./App.css";

export default function App() {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [missing, setMissing] = useState([]);

  const loadPlants = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.getPlants();
      setPlants(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || "Veriler yüklenemedi.");
    } finally {
      setLoading(false);
    }
  };

  const loadMissing = async () => {
    try {
      const data = await api.getMissingSearches();
      setMissing(Array.isArray(data) ? data : []);
    } catch {
      // Liste opsiyonel; sessiz geç
    }
  };

  useEffect(() => {
    loadPlants();
    loadMissing();
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLocaleLowerCase("tr");
    if (!q) return plants;
    return plants.filter((p) => {
      const hay = `${p.ad} ${p.botanikAd} ${p.tur}`.toLocaleLowerCase("tr");
      return hay.includes(q);
    });
  }, [plants, query]);

  const handleMissingSubmit = async (text) => {
    await api.postMissingSearch(text);
    await loadMissing();
  };

  return (
    <div className="app">
      <header className="app__header">
        <h1>Şifa Hanım Aktar</h1>
        <p>React + Express + SQLite — bitki listesi</p>
      </header>

      <section className="app__toolbar">
        <input
          type="search"
          placeholder="Bitki veya botanik adı ara…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Bitki ara"
        />
        <button type="button" onClick={loadPlants}>
          Yenile
        </button>
      </section>

      {loading && <p className="status">Yükleniyor…</p>}
      {error && <p className="status status--error">{error}</p>}

      {!loading && !error && (
        <PlantList plants={filtered} total={plants.length} />
      )}

      <MissingSearchForm
        onSubmit={handleMissingSubmit}
        items={missing}
      />
    </div>
  );
}
