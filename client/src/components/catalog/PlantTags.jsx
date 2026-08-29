import { Link } from "react-router-dom";
import { getPlantTags } from "../../lib/plant-tags.js";

export function PlantTags({ plant }) {
  const tags = getPlantTags(plant);
  if (!tags.length) return null;

  return (
    <section className="plant-tags" aria-label="Konu etiketleri">
      <p className="section-label">Bu bitki hangi konularda aranır?</p>
      <div className="filter-chips plant-tags__list">
        {tags.map((tag) => (
          <Link
            key={tag.id}
            className="filter-chip plant-tag-chip"
            to={`/?etiket=${encodeURIComponent(tag.id)}`}
          >
            #{tag.label}
          </Link>
        ))}
      </div>
      <p className="plant-tags__hint">
        Etikete tıklayınca aynı konudaki diğer bitkiler listelenir.
      </p>
    </section>
  );
}
