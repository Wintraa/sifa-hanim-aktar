import { isFavorite, toggleFavorite } from "./favorites.js";
import { getCareNote, removeCareNote, saveCareNote } from "./care-notes.js";
import { addRecentPlant } from "./recent-plants.js";
import { applyDensityPreference } from "./preferences.js";
import { showToast } from "./toast.js";
import { getPlants } from "./plant-data.js";
import { escapeHtml, setMetaContent } from "./utils.js";

const elements = {
  detailTitle: document.querySelector("#detailTitle"),
  detailHero: document.querySelector("#detailHero"),
  detailImage: document.querySelector("#detailImage"),
  detailType: document.querySelector("#detailType"),
  detailName: document.querySelector("#detailName"),
  detailBotanicalName: document.querySelector("#detailBotanicalName"),
  detailOverview: document.querySelector("#detailOverview"),
  tablesGrid: document.querySelector("#tablesGrid"),
  tableBasic: document.querySelector("#tableBasic"),
  tableHealth: document.querySelector("#tableHealth"),
  tableGeo: document.querySelector("#tableGeo"),
  tableCare: document.querySelector("#tableCare"),
  careInfoCard: document.querySelector("#careInfoCard"),
  detailEmpty: document.querySelector("#detailEmpty"),
  detailFavoriteButton: document.querySelector("#detailFavoriteButton"),
  detailFavoriteLabel: document.querySelector("#detailFavoriteLabel"),
  detailLoading: document.querySelector("#detailLoading"),
  shareButton: document.querySelector("#shareButton"),
  printButton: document.querySelector("#printButton"),
  carePanel: document.querySelector("#carePanel"),
  careForm: document.querySelector("#careForm"),
  careIntervalInput: document.querySelector("#careIntervalInput"),
  careNoteInput: document.querySelector("#careNoteInput"),
  careRemoveButton: document.querySelector("#careRemoveButton"),
  careFeedback: document.querySelector("#careFeedback"),
  similarSection: document.querySelector("#similarSection"),
  similarGrid: document.querySelector("#similarGrid"),
  sourceNote: document.querySelector("#sourceNote"),
  caseExperience: document.querySelector("#caseExperience"),
  caseExperienceLead: document.querySelector("#caseExperienceLead"),
  caseProblem: document.querySelector("#caseProblem"),
  caseApproach: document.querySelector("#caseApproach"),
  caseOutcome: document.querySelector("#caseOutcome"),
  caseStory: document.querySelector("#caseStory"),
  caseSource: document.querySelector("#caseSource")
};

let currentPlantId = null;
let currentPlantType = "";
let favoriteBound = false;
let actionsBound = false;

// URL üzerindeki bitki kimliğini okuyup detay sayfasını başlatır.
const init = async () => {
  applyDensityPreference();
  const plantId = getPlantIdFromUrl();

  if (!plantId) {
    showEmptyState();
    return;
  }

  setLoadingState(true);

  try {
    const plants = await getPlants();

    const selectedPlant = plants.find((plant) => plant.id === plantId);

    if (!selectedPlant || !isValidPlantRecord(selectedPlant)) {
      showEmptyState("İstenen bitki kaydı bulunamadı veya eksik alanlar içeriyor.");
      return;
    }

    currentPlantId = selectedPlant.id;
    currentPlantType = selectedPlant.tur ?? "";
    addRecentPlant(selectedPlant.id);
    renderPlantDetail(selectedPlant);
    renderSimilarPlants(selectedPlant, plants);
    bindFavoriteButton();
    bindActionButtons();
    bindCareForm();
  } catch (error) {
    showEmptyState(error.message || "Beklenmeyen bir hata oluştu.");
  } finally {
    setLoadingState(false);
  }
};

// URL sorgu parametresinden sayısal ID değerini güvenli şekilde döndürür.
const getPlantIdFromUrl = () => {
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get("id"));

  return Number.isInteger(id) && id > 0 ? id : null;
};

// Detay renderı için asgari şema kontrolü yapar.
const isValidPlantRecord = (plant) =>
  Boolean(
    plant &&
      plant.temelBilgiler &&
      plant.saglikKullanim &&
      plant.cografyaMevsim &&
      plant.bakimYetistirme
  );

// Seçili bitkinin başlık, görsel ve tablo alanlarını doldurur.
const renderPlantDetail = (plant) => {
  document.title = `${plant.ad} | Şifa Hanım Aktar`;
  const metaDescription = `${plant.ad} (${plant.botanikAd}): tanıtım, kullanım bilgileri ve PubMed klinik vaka özeti.`;
  setMetaContent('meta[name="description"]', metaDescription);
  setMetaContent('meta[property="og:title"]', `${plant.ad} | Şifa Hanım Aktar`);
  setMetaContent('meta[property="og:description"]', metaDescription);
  setMetaContent('meta[property="og:image"]', new URL(plant.resimUrl, window.location.href).href);
  elements.detailTitle.textContent = plant.ad ?? "Bitki";
  elements.detailName.textContent = plant.ad ?? "";
  elements.detailType.textContent = plant.tur ?? "";
  elements.detailBotanicalName.textContent = plant.botanikAd ?? "";
  elements.detailOverview.textContent = plant.genelTavsiyeMetni ?? "";
  elements.detailImage.src = plant.resimUrl ?? "";
  elements.detailImage.alt = `${plant.ad ?? "Bitki"} görseli`;

  elements.tableBasic.innerHTML = createRows([
    ["Türkçe Adı", plant.temelBilgiler?.turkceAdi],
    ["Botanik Adı", plant.temelBilgiler?.botanikAdi],
    ["Yetişme biçimi", plant.temelBilgiler?.bitkiTuru]
  ]);

  elements.tableHealth.innerHTML = createRows([
    ["Faydaları", plant.saglikKullanim?.faydalari],
    ["Kullanım Şekli", plant.saglikKullanim?.kullanimSekli],
    ["Yan Etkiler & Uyarılar", plant.saglikKullanim?.yanEtkilerUyarilar]
  ]);

  elements.tableGeo.innerHTML = createRows([
    ["Yetiştiği Yerler", plant.cografyaMevsim?.yetistigiYerler],
    ["Hasat Mevsimi", plant.cografyaMevsim?.hasatMevsimi],
    ["Çiçeklenme Zamanı", plant.cografyaMevsim?.ciceklenmeZamani]
  ]);

  const medicinal = plant.tur === "Tıbbi Bitkiler";

  // Tıbbi bitkilerde sulama ve bakım-yetiştirme bölümü gösterilmez.
  if (elements.careInfoCard) {
    elements.careInfoCard.hidden = medicinal;
  }

  if (!medicinal) {
    elements.tableCare.innerHTML = createRows([
      ["Işık İhtiyacı", plant.bakimYetistirme?.isikIhtiyaci],
      ["Sulama Sıklığı", plant.bakimYetistirme?.sulamaSikligi],
      ["Toprak Tipi", plant.bakimYetistirme?.toprakTipi]
    ]);
  } else if (elements.tableCare) {
    elements.tableCare.innerHTML = "";
  }

  renderSourceNote(plant);
  renderCaseExperience(plant);

  updateFavoriteButton(isFavorite(plant.id));
  elements.detailFavoriteButton.hidden = false;
  elements.shareButton.hidden = false;
  elements.printButton.hidden = false;
  elements.detailHero.hidden = false;
  elements.tablesGrid.hidden = false;
  elements.detailEmpty.hidden = true;
  syncCarePanel(medicinal);
};

// PubMed kaynaklı klinik vaka / hasta deneyimi bölümünü doldurur.
const renderCaseExperience = (plant) => {
  const section = elements.caseExperience;
  if (!section) {
    return;
  }

  const vaka = plant.ornekVaka;
  const hasStory = Boolean(vaka && (vaka.anlatim || vaka.sorun));

  if (!hasStory) {
    section.hidden = true;
    return;
  }

  if (elements.caseExperienceLead) {
    elements.caseExperienceLead.textContent =
      vaka.baslik ||
      `${plant.ad} ile ilgili, yayımlanmış gerçek bir klinik kayıt özeti`;
  }

  if (elements.caseProblem) {
    elements.caseProblem.textContent = vaka.sorun || "—";
  }
  if (elements.caseApproach) {
    elements.caseApproach.textContent = vaka.yaklasim || vaka.yaklaşım || "—";
  }
  if (elements.caseOutcome) {
    elements.caseOutcome.textContent = vaka.sonuc || "—";
  }
  if (elements.caseStory) {
    elements.caseStory.textContent = vaka.anlatim || "";
    elements.caseStory.hidden = !vaka.anlatim;
  }

  if (elements.caseSource) {
    const pmid = vaka.pubmedId || vaka.pmid || "";
    const url = vaka.pubmedUrl || (pmid ? `https://pubmed.ncbi.nlm.nih.gov/${pmid}/` : "");
    const year = vaka.yil ? ` (${vaka.yil})` : "";
    const title = vaka.makaleBasligi ? ` — ${vaka.makaleBasligi}` : "";

    if (url && pmid) {
      elements.caseSource.innerHTML = `Kaynak: <a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">PubMed / bilimsel makale (PMID ${escapeHtml(String(pmid))})</a>${escapeHtml(year)}${escapeHtml(title)}`;
    } else if (url) {
      elements.caseSource.innerHTML = `Kaynak: <a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(vaka.kaynakAdi || "Güvenilir tıbbi kaynak")}</a>${escapeHtml(year)}${escapeHtml(title)}`;
    } else {
      elements.caseSource.textContent = "Kaynak: Yayımlanmış klinik kayıt";
    }
  }

  section.hidden = false;
};

// Yalnızca tıbbi feragatname gösterir; kaynak künyesi kullanıcıya gösterilmez.
const renderSourceNote = (plant) => {
  if (!elements.sourceNote) {
    return;
  }

  elements.sourceNote.innerHTML = `
    <p class="source-note__disclaimer">
      <strong>Tıbbi uyarı:</strong> Buradaki içerik yalnızca bilgilendirme
      amaçlıdır ve tıbbi tavsiye, teşhis veya tedavi yerine geçmez. Hiçbir
      bitkiyi tedavi amacıyla kullanmadan önce hekiminize veya eczacınıza
      danışın. Gebelik, emzirme, kronik hastalık ve düzenli ilaç kullanımı
      durumlarında bitkisel ürünler ciddi riskler taşıyabilir.
    </p>
  `;
  elements.sourceNote.hidden = false;
};

// Aynı türden en fazla 6 benzer bitkiyi kompakt ızgarada önerir.
const renderSimilarPlants = (plant, plants) => {
  const similar = plants
    .filter((item) => item.id !== plant.id && item.tur === plant.tur)
    .slice(0, 6);

  if (!elements.similarSection || !elements.similarGrid || similar.length === 0) {
    if (elements.similarSection) {
      elements.similarSection.hidden = true;
    }
    return;
  }

  elements.similarSection.hidden = false;
  elements.similarGrid.innerHTML = similar
    .map((item) => {
      const ad = escapeHtml(item.ad);
      const botanik = escapeHtml(item.botanikAd);
      const resim = escapeHtml(item.resimUrl);
      return `
        <a class="similar-card" href="detail.html?id=${Number(item.id)}">
          <img src="${resim}" alt="${ad} görseli" width="160" height="160" loading="lazy" decoding="async" />
          <div>
            <strong>${ad}</strong>
            <span>${botanik}</span>
          </div>
        </a>
      `;
    })
    .join("");
};

// Favori düğmesi tıklama olayını yalnızca bir kez bağlar.
const bindFavoriteButton = () => {
  if (favoriteBound) {
    return;
  }

  elements.detailFavoriteButton?.addEventListener("click", () => {
    if (!currentPlantId) {
      return;
    }

    const active = toggleFavorite(currentPlantId);
    updateFavoriteButton(active);

    const button = elements.detailFavoriteButton;
    button.classList.remove("is-animating");
    void button.offsetWidth;
    button.classList.add("is-animating");
    button.addEventListener(
      "animationend",
      () => {
        button.classList.remove("is-animating");
      },
      { once: true }
    );

    syncCarePanel(currentPlantType === "Tıbbi Bitkiler");
    showToast(active ? "Favorilere eklendi." : "Favorilerden çıkarıldı.", "success");
  });

  favoriteBound = true;
};

// Paylaş ve yazdır düğmelerini bağlar.
const bindActionButtons = () => {
  if (actionsBound) {
    return;
  }

  elements.shareButton?.addEventListener("click", async () => {
    const url = window.location.href;

    try {
      if (navigator.share) {
        await navigator.share({ title: document.title, url });
        showToast("Bitki bağlantısı paylaşıldı.", "success");
      } else {
        await navigator.clipboard.writeText(url);
        showToast("Bağlantı panoya kopyalandı.", "success");
      }
    } catch (error) {
      if (error?.name === "AbortError") {
        return;
      }
      showToast("Bağlantı kopyalanamadı. Adresi manuel olarak kopyalayabilirsiniz.", "error");
    }
  });

  elements.printButton?.addEventListener("click", () => {
    window.print();
  });

  actionsBound = true;
};

// Bakım hatırlatıcısı formunu bağlar.
const bindCareForm = () => {
  elements.careForm?.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!currentPlantId) {
      return;
    }

    const result = saveCareNote(currentPlantId, {
      intervalDays: Number(elements.careIntervalInput.value),
      note: elements.careNoteInput.value
    });

    if (!result.ok) {
      elements.careFeedback.textContent = result.error;
      showToast(result.error, "error");
      return;
    }

    elements.careFeedback.textContent = "Bakım hatırlatıcısı kaydedildi.";
    showToast("Bakım hatırlatıcısı kaydedildi.", "success");
  });

  elements.careRemoveButton?.addEventListener("click", () => {
    if (!currentPlantId) {
      return;
    }

    const result = removeCareNote(currentPlantId);

    if (!result.ok) {
      elements.careFeedback.textContent = result.error;
      showToast(result.error, "error");
      return;
    }

    elements.careIntervalInput.value = "7";
    elements.careNoteInput.value = "";
    elements.careFeedback.textContent = "Bakım hatırlatıcısı silindi.";
    showToast("Bakım hatırlatıcısı silindi.", "info");
  });
};

// Favori durumuna göre bakım panelini gösterir ve doldurur.
const syncCarePanel = (medicinal = false) => {
  if (!elements.carePanel || !currentPlantId) {
    return;
  }

  // Tıbbi bitkilerde sulama hatırlatıcısı kullanılmaz.
  if (medicinal) {
    elements.carePanel.hidden = true;
    return;
  }

  const favorite = isFavorite(currentPlantId);
  elements.carePanel.hidden = !favorite;

  if (!favorite) {
    return;
  }

  const note = getCareNote(currentPlantId);
  elements.careIntervalInput.value = String(note?.intervalDays || 7);
  elements.careNoteInput.value = note?.note || "";
  elements.careFeedback.textContent = "";
};

// Favori düğmesinin görünen durumunu günceller.
const updateFavoriteButton = (active) => {
  if (!elements.detailFavoriteButton) {
    return;
  }

  elements.detailFavoriteButton.classList.toggle("is-active", active);
  elements.detailFavoriteButton.setAttribute("aria-pressed", String(active));

  const icon = elements.detailFavoriteButton.querySelector("span[aria-hidden='true']");
  if (icon) {
    icon.textContent = active ? "♥" : "♡";
  }

  if (elements.detailFavoriteLabel) {
    elements.detailFavoriteLabel.textContent = active ? "Favorilerden Çıkar" : "Favorilere Ekle";
  }
};

// Bilgi tablolarında kaçışlı satır üretir.
const createRows = (entries) =>
  entries
    .map(([label, value]) => {
      const text = typeof value === "string" ? value.trim() : "";
      // Kaynakta karşılığı olmayan alan uydurulmaz; açıkça belirtilir.
      const cell = text
        ? escapeHtml(text)
        : '<span class="table-empty">Bu alanda kaynakta bilgi bulunmamaktadır</span>';

      return `
        <tr>
          <th scope="row">${escapeHtml(label)}</th>
          <td>${cell}</td>
        </tr>
      `;
    })
    .join("");

// Yükleme durumunu açar/kapatır.
const setLoadingState = (isLoading) => {
  if (elements.detailLoading) {
    elements.detailLoading.hidden = !isLoading;
  }

  if (isLoading) {
    elements.detailHero.hidden = true;
    elements.tablesGrid.hidden = true;
    elements.detailEmpty.hidden = true;
    elements.detailFavoriteButton.hidden = true;
    elements.shareButton.hidden = true;
    elements.printButton.hidden = true;
    elements.carePanel.hidden = true;
    elements.similarSection.hidden = true;
    elements.detailTitle.textContent = "Bitki yükleniyor...";
  }
};

// Geçersiz ID veya veri hatasında boş durum ekranını gösterir.
const showEmptyState = (message = "İstenen bitki kaydı bulunamadı.") => {
  elements.detailHero.hidden = true;
  elements.tablesGrid.hidden = true;
  elements.detailFavoriteButton.hidden = true;
  elements.shareButton.hidden = true;
  elements.printButton.hidden = true;
  elements.carePanel.hidden = true;
  elements.similarSection.hidden = true;
  if (elements.caseExperience) {
    elements.caseExperience.hidden = true;
  }
  if (elements.sourceNote) {
    elements.sourceNote.hidden = true;
  }

  if (elements.detailLoading) {
    elements.detailLoading.hidden = true;
  }
  elements.detailEmpty.hidden = false;
  elements.detailTitle.textContent = "Bitki bulunamadı";
  elements.detailEmpty.querySelector("p").textContent = message;
};

init();
