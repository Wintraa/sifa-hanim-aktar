import { Link } from "react-router-dom";
import { plantImageUrl } from "../../lib/assetUrl.js";

export function RecentRail({ plants }) {
  if (!plants?.length) return null;

  return (
    <section className="recent-section" id="recentSection" aria-labelledby="recentTitle">
      <div className="recent-section__header">
        <p className="section-label">İnceleme geçmişi</p>
        <h3 id="recentTitle">Son incelenen bitkiler</h3>
      </div>
      <div className="recent-rail" id="recentRail">
        {plants.map((plant) => (
          <Link
            key={plant.id}
            className="recent-card"
            to={`/bitki/${plant.id}`}
            title={plant.ad}
          >
            <img
              src={plantImageUrl(plant.resimUrl)}
              alt={`${plant.ad} görseli`}
              width="48"
              height="48"
              loading="lazy"
              decoding="async"
            />
            <strong>{plant.ad}</strong>
          </Link>
        ))}
      </div>
    </section>
  );
}
