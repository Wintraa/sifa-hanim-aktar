import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../services/api.js";
import { useFavorites } from "../context/FavoritesContext.jsx";
import { addRecentPlant } from "../lib/recent-plants.js";
import { getCareNote, saveCareNote, removeCareNote } from "../lib/care-notes.js";
import { showToast } from "../lib/toast.js";
import { plantImageUrl } from "../lib/assetUrl.js";
import { applyPlantSeo } from "../lib/seo.js";
import { PlantTags } from "../components/catalog/PlantTags.jsx";
import { WhatsAppFloatButton } from "../components/layout/ShopContact.jsx";
import { whatsappUrl } from "../lib/whatsapp.js";
import { SHOP } from "../config/shop.js";

function CaseExperience({ plant }) {
  const vaka = plant.ornekVaka;
  const hasStory = Boolean(vaka && (vaka.anlatim || vaka.sorun));
  if (!hasStory) return null;

  const isAktar = vaka.kaynak === "aktar-senaryo";
  const label = isAktar ? "Aktar tezgâhı örneği" : "Gerçek bir olay";
  const title = isAktar ? "Sık sorulan kullanım senaryosu" : "Bir kişinin başından geçen";

  return (
    <section
      className="info-card case-experience"
      id="caseExperience"
      aria-labelledby="caseExperienceTitle"
    >
      <p className="section-label">{label}</p>
      <h3 id="caseExperienceTitle">{title}</h3>
      <p className="case-experience__lead">
        {vaka.baslik || `${plant.ad} ile ilgili örnek`}
      </p>
      <dl className="case-experience__facts">
        <div>
          <dt>Ne şikayeti vardı?</dt>
          <dd>{vaka.sorun || "—"}</dd>
        </div>
        <div>
          <dt>Ne yapıldı?</dt>
          <dd>{vaka.yaklasim || vaka.yaklaşım || "—"}</dd>
        </div>
        <div>
          <dt>Sonuç ne oldu?</dt>
          <dd>{vaka.sonuc || "—"}</dd>
        </div>
      </dl>
      {vaka.anlatim ? (
        <blockquote className="case-experience__story">{vaka.anlatim}</blockquote>
      ) : null}
      <p className="case-experience__disclaimer">
        {isAktar
          ? "Bu bir klinik çalışma değil; aktar kullanımına dayalı örnek senaryodur. Herkesin sonucu aynı olmaz. Teşhis veya tedavi yerine geçmez."
          : "Bu, yaşanmış bir örneğin özetidir. Herkesin sonucu aynı olmaz. Teşhis veya tedavi yerine geçmez. Bitki kullanmadan önce hekiminize danışın."}
      </p>
    </section>
  );
}

export default function DetailPage() {
  const { id } = useParams();
  const { isFavorite, toggle } = useFavorites();
  const [plant, setPlant] = useState(null);
  const [allPlants, setAllPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [careInterval, setCareInterval] = useState(7);
  const [careNote, setCareNote] = useState("");
  const [careFeedback, setCareFeedback] = useState("");

  const favorite = plant ? isFavorite(plant.id) : false;
  const medicinal = plant?.tur === "Tıbbi Bitkiler";

  useEffect(() => {
    document.body.classList.add("detail-body");
    return () => document.body.classList.remove("detail-body");
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const [item, list] = await Promise.all([
          api.getPlantWithFallback(id),
          api.getPlantsWithFallback().catch(() => []),
        ]);
        if (cancelled) return;
        if (!item?.id) {
          throw new Error("Bitki bulunamadı.");
        }
        setPlant(item);
        setAllPlants(list);
        addRecentPlant(item.id);
        const care = getCareNote(item.id);
        setCareInterval(care?.intervalDays || 7);
        setCareNote(care?.note || "");
      } catch (err) {
        if (!cancelled) {
          setPlant(null);
          setError(err.message || "Bitki bulunamadı.");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id]);

  useEffect(() => {
    if (!plant) return;
    applyPlantSeo(plant);
  }, [plant]);

  const similar = useMemo(() => {
    if (!plant) return [];
    return allPlants
      .filter((item) => item.id !== plant.id && item.tur === plant.tur)
      .slice(0, 6);
  }, [plant, allPlants]);

  const handleShare = async () => {
    const url = window.location.href;
    try {
      if (navigator.share) {
        await navigator.share({ title: plant.ad, url });
      } else {
        await navigator.clipboard.writeText(url);
        showToast("Bağlantı panoya kopyalandı.", "success");
      }
    } catch {
      showToast("Paylaşım iptal edildi.", "info");
    }
  };

  const handleCareSave = (e) => {
    e.preventDefault();
    const result = saveCareNote(plant.id, {
      intervalDays: Number(careInterval),
      note: careNote,
    });
    setCareFeedback(result.ok ? "Bakım notu kaydedildi." : result.error);
    if (result.ok) showToast("Bakım notu kaydedildi.", "success");
  };

  const handleCareRemove = () => {
    removeCareNote(plant.id);
    setCareNote("");
    setCareInterval(7);
    setCareFeedback("Bakım notu silindi.");
    showToast("Bakım notu silindi.", "info");
  };

  return (
    <>
      <header className="detail-header">
        <Link className="back-button" to="/">
          Kataloğa Dön
        </Link>
        <div className="detail-header__title">
          <p className="section-label">Bitki maddesi</p>
          <h1 id="detailTitle">{plant?.ad || (loading ? "Yükleniyor" : "Bitki")}</h1>
        </div>
        <div className="detail-header__actions">
          {plant ? (
            <>
              <button
                className={`favorite-button favorite-button--large${favorite ? " is-active" : ""}`}
                id="detailFavoriteButton"
                type="button"
                aria-pressed={favorite}
                onClick={(e) => {
                  const btn = e.currentTarget;
                  btn.classList.remove("is-pulsing");
                  void btn.offsetWidth;
                  btn.classList.add("is-pulsing");
                  toggle(plant.id);
                }}
              >
                <span aria-hidden="true">{favorite ? "♥" : "♡"}</span>
                <span id="detailFavoriteLabel">
                  {favorite ? "Favorilerden Çıkar" : "Favorilere Ekle"}
                </span>
              </button>
              <button
                className="profile-tertiary-button detail-action-button"
                type="button"
                aria-label="Bitkiyi paylaş"
                onClick={handleShare}
              >
                Paylaş
              </button>
              <button
                className="profile-tertiary-button detail-action-button detail-action-button--whatsapp"
                type="button"
                aria-label="WhatsApp ile sor"
                onClick={() =>
                  window.open(
                    whatsappUrl(`${SHOP.whatsappMessages.advice} Bitki: ${plant.ad}`),
                    "_blank",
                    "noopener,noreferrer"
                  )
                }
              >
                WhatsApp
              </button>
              <button
                className="profile-tertiary-button detail-action-button"
                type="button"
                aria-label="Bitki detayını yazdır"
                onClick={() => window.print()}
              >
                Yazdır
              </button>
            </>
          ) : null}
        </div>
      </header>

      <main className="detail-main" id="main-content">
        {loading ? (
          <section className="loading-state" role="status" aria-live="polite">
            <p>Bitki bilgileri yükleniyor.</p>
          </section>
        ) : null}

        {!loading && (error || !plant) ? (
          <section className="detail-empty" aria-labelledby="detailEmptyTitle">
            <h2 id="detailEmptyTitle">Bitki bulunamadı</h2>
            <p>{error || "İstenen bitki bilgisi yüklenemedi veya bağlantı geçersiz."}</p>
            <Link className="back-button" to="/">
              Kataloğa Dön
            </Link>
          </section>
        ) : null}

        {!loading && plant ? (
          <>
            <section className="detail-hero" aria-labelledby="detailName">
              <img
                src={plantImageUrl(plant.resimUrl)}
                alt={`${plant.ad} görseli`}
                className="detail-hero__image"
                width="840"
                height="630"
                decoding="async"
                fetchPriority="high"
              />
              <div className="detail-hero__content">
                <p className="detail-tag">{plant.tur}</p>
                <h2 id="detailName">{plant.ad}</h2>
                <p className="detail-subtitle">{plant.temelBilgiler?.bitkiTuru || "Şifa kullanımı"}</p>
                <p className="detail-description" style={{ whiteSpace: "pre-line" }}>
                  {plant.genelTavsiyeMetni}
                </p>
              </div>
            </section>

            <PlantTags plant={plant} />

            <section className="tables-grid" aria-label="Şifa bilgileri">
              <article className="info-card" aria-labelledby="headingUse">
                <h3 id="headingUse">Ne işe yarar?</h3>
                <p className="detail-description">{plant.saglikKullanim?.faydalari}</p>
              </article>

              <article className="info-card" aria-labelledby="headingHow">
                <h3 id="headingHow">Nasıl kullanılır?</h3>
                <p className="detail-description">{plant.saglikKullanim?.kullanimSekli}</p>
              </article>

              <article className="info-card" aria-labelledby="headingWarn">
                <h3 id="headingWarn">Nelere dikkat edilir?</h3>
                <p className="detail-description">{plant.saglikKullanim?.yanEtkilerUyarilar}</p>
              </article>
            </section>

            <CaseExperience plant={plant} />

            <section className="source-note" aria-label="Tıbbi uyarı">
              <p className="source-note__disclaimer">
                <strong>Tıbbi uyarı:</strong> Buradaki içerik yalnızca bilgilendirme
                amaçlıdır ve tıbbi tavsiye, teşhis veya tedavi yerine geçmez. Hiçbir
                bitkiyi tedavi amacıyla kullanmadan önce hekiminize veya eczacınıza
                danışın. Gebelik, emzirme, kronik hastalık ve düzenli ilaç kullanımı
                durumlarında bitkisel ürünler ciddi riskler taşıyabilir.
              </p>
            </section>

            {favorite && !medicinal ? (
              <section className="info-card care-panel" aria-labelledby="carePanelTitle">
                <h3 id="carePanelTitle">Kişisel bakım notu</h3>
                <p className="detail-description">
                  Favorilerinize eklediğiniz bitkiler için sulama aralığı ve kısa bir not
                  kaydedebilirsiniz. Bu not yalnızca bu tarayıcıda saklanır.
                </p>
                <form className="care-form" onSubmit={handleCareSave} aria-describedby="careFeedback">
                  <label className="profile-field" htmlFor="careIntervalInput">
                    <span>Sulama aralığı (gün)</span>
                    <input
                      id="careIntervalInput"
                      type="number"
                      min="1"
                      max="60"
                      value={careInterval}
                      onChange={(e) => setCareInterval(e.target.value)}
                      required
                      inputMode="numeric"
                    />
                  </label>
                  <label className="profile-field" htmlFor="careNoteInput">
                    <span>Kısa not</span>
                    <input
                      id="careNoteInput"
                      type="text"
                      maxLength={160}
                      placeholder="Örneğin: Sabah erken sulayın"
                      value={careNote}
                      onChange={(e) => setCareNote(e.target.value)}
                    />
                  </label>
                  <div className="profile-form-actions">
                    <button className="back-button" type="submit">
                      Notu Kaydet
                    </button>
                    <button
                      className="profile-tertiary-button"
                      type="button"
                      onClick={handleCareRemove}
                    >
                      Sil
                    </button>
                  </div>
                  <p id="careFeedback" className="profile-feedback" aria-live="polite" role="status">
                    {careFeedback}
                  </p>
                </form>
              </section>
            ) : null}

            {similar.length > 0 ? (
              <section className="similar-section" aria-labelledby="similarTitle">
                <div className="plants-section__header">
                  <div>
                    <p className="section-label">İlgili maddeler</p>
                    <h3 id="similarTitle">Aynı kategorideki bitkiler</h3>
                  </div>
                </div>
                <div className="similar-grid" id="similarGrid">
                  {similar.map((item) => (
                    <Link key={item.id} className="similar-card" to={`/bitki/${item.id}`}>
                      <img
                        src={plantImageUrl(item.resimUrl)}
                        alt={`${item.ad} görseli`}
                        width="160"
                        height="160"
                        loading="lazy"
                        decoding="async"
                      />
                      <div>
                        <strong>{item.ad}</strong>
                        <span>{item.temelBilgiler?.bitkiTuru || item.tur}</span>
                      </div>
                    </Link>
                  ))}
                </div>
              </section>
            ) : null}
          </>
        ) : null}
      </main>
      <WhatsAppFloatButton />
    </>
  );
}
