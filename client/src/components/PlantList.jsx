export function PlantList({ plants, total }) {
  if (plants.length === 0) {
    return <p className="status">Eşleşen bitki yok.</p>;
  }

  return (
    <section>
      <p className="plant-list__meta">
        Gösterilen: {plants.length} / Toplam: {total}
      </p>
      <ul className="plant-grid">
        {plants.map((plant) => (
          <li key={plant.id} className="plant-card">
            <h3>{plant.ad}</h3>
            <p className="botanik">{plant.botanikAd}</p>
            <span className="tur">{plant.tur}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
