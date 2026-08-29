/** Bitki metninden konu etiketleri çıkarır (ana sayfa filtresi + detay chip). */
const TAG_RULES = [
  { id: "mide", label: "mide", patterns: [/mide/i, /sindirim/i, /hazımsız/i, /şişkin/i, /gaz/i, /kramp/i] },
  { id: "uyku", label: "uyku", patterns: [/uyku/i, /uykusuz/i, /sakinle/i] },
  { id: "stres", label: "stres", patterns: [/stres/i, /kaygı/i, /gergin/i, /sinir/i, /anksiyete/i] },
  { id: "cilt", label: "cilt", patterns: [/cilt/i, /yara/i, /yanık/i, /döküntü/i, /egzama/i, /sürerek/i] },
  { id: "bogaz", label: "boğaz", patterns: [/boğaz/i, /gargara/i, /öksürük/i, /balgam/i, /soğuk algın/i] },
  { id: "cay", label: "çay", patterns: [/çay/i, /demle/i, /infüzyon/i, /demlen/i] },
  { id: "agri", label: "ağrı", patterns: [/ağrı/i, /ağrı/i, /romatiz/i, /kas/i] },
  { id: "bagisiklik", label: "bağışıklık", patterns: [/bağışıklık/i, /grip/i, /ateş/i, /soğuk algın/i] },
  { id: "idrar", label: "idrar", patterns: [/idrar/i, /böbrek/i, /mesane/i] },
  { id: "sus", label: "süs bitki", patterns: [/süs bitk/i], tur: "Süs Bitkileri" },
  { id: "aromatik", label: "aromatik", patterns: [/aromatik/i, /koku/i, /baharat/i], tur: "Aromatik Bitkiler" },
  { id: "tibbi", label: "tıbbi bitki", patterns: [/tıbbi/i], tur: "Tıbbi Bitkiler" },
];

const plantText = (plant) =>
  [
    plant.ad,
    plant.tur,
    plant.genelTavsiyeMetni,
    plant.saglikKullanim?.faydalari,
    plant.saglikKullanim?.kullanimSekli,
  ]
    .filter(Boolean)
    .join(" ")
    .toLocaleLowerCase("tr");

export function getPlantTags(plant, limit = 8) {
  if (!plant) return [];
  const text = plantText(plant);
  const tags = [];

  for (const rule of TAG_RULES) {
    if (rule.tur && plant.tur !== rule.tur) continue;
    if (rule.patterns.some((re) => re.test(text))) {
      tags.push({ id: rule.id, label: rule.label });
    }
  }

  if (tags.length === 0 && plant.tur) {
    if (plant.tur === "Tıbbi Bitkiler") tags.push({ id: "tibbi", label: "tıbbi bitki" });
    else if (plant.tur === "Aromatik Bitkiler") tags.push({ id: "aromatik", label: "aromatik" });
  }

  const seen = new Set();
  return tags.filter((t) => {
    if (seen.has(t.id)) return false;
    seen.add(t.id);
    return true;
  }).slice(0, limit);
}

export function plantMatchesTag(plant, tagId) {
  if (!tagId) return true;
  return getPlantTags(plant, 12).some((t) => t.id === tagId);
}

export function getTagLabel(tagId) {
  const rule = TAG_RULES.find((r) => r.id === tagId);
  return rule?.label || tagId;
}
