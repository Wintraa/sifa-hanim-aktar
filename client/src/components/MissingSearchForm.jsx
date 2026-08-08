import { useState } from "react";

export function MissingSearchForm({ onSubmit, items }) {
  const [value, setValue] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const text = value.trim();
    if (text.length < 2) {
      setIsError(true);
      setMessage("En az 2 karakter yazın.");
      return;
    }

    setBusy(true);
    setMessage("");
    setIsError(false);
    try {
      await onSubmit(text);
      setValue("");
      setMessage("Kayıt eklendi.");
    } catch (err) {
      setIsError(true);
      setMessage(err.message || "Kayıt başarısız.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="missing">
      <h2>Bulunamayan arama ekle (POST örneği)</h2>
      <form onSubmit={handleSubmit}>
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Örn. aslan yelesi"
          disabled={busy}
        />
        <button type="submit" disabled={busy}>
          {busy ? "Kaydediliyor…" : "Kaydet"}
        </button>
      </form>
      {message && (
        <p className={`feedback${isError ? " feedback--error" : ""}`}>
          {message}
        </p>
      )}
      {items?.length > 0 && (
        <ul>
          {items.slice(0, 10).map((item) => (
            <li key={item.id}>
              {item.aramaMetni} — {item.tekrarSayisi}x
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
