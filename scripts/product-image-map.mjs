/**
 * Ürün görselleri için Wikimedia arama terimleri ve yerel bitki fotoğrafı yedekleri.
 * fetch script: search → Commons; yoksa fallbackPath kullanılır.
 */
export const IMAGE_MAP = {
  // ── Ağrı Kremi (1–4) ──────────────────────────────────────────────────────
  1: { search: "herbal pain relief cream jar product" },
  2: {
    search: "juniper berry extract ointment",
    fallbackPath: "assets/plants/photos/207-juniperus-communis.jpg",
  },
  3: { search: "herbal massage cream tube natural" },
  4: { search: "massage cream herbal product jar" },

  // ── Aromatik Yağlar (5–10) ────────────────────────────────────────────────
  5: {
    search: "nigella sativa black seed oil bottle",
    fallbackPath: "assets/plants/photos/22-nigella-sativa.jpg",
  },
  6: {
    search: "hypericum perforatum st johns wort oil",
    fallbackPath: "assets/plants/photos/25-openverse.jpg",
  },
  7: {
    search: "costus root oil oud hindi",
    fallbackPath: "assets/plants/photos/204-saussurea-costus.jpg",
  },
  8: {
    search: "castor oil ricinus communis bottle",
    fallbackPath: "assets/plants/photos/208-ricinus-communis.jpg",
  },
  9: { search: "organic virgin coconut oil jar" },
  10: { search: "coconut oil bottle product" },

  // ── Baharatlar (11–30) ────────────────────────────────────────────────────
  11: {
    search: "red pepper flakes spice",
    fallbackPath: "assets/plants/photos/137-capsicum-annuum.jpg",
  },
  12: {
    search: "sweet paprika flakes spice",
    fallbackPath: "assets/plants/photos/137-capsicum-annuum.jpg",
  },
  13: {
    search: "hot chili powder spice",
    fallbackPath: "assets/plants/photos/137-capsicum-annuum.jpg",
  },
  14: {
    search: "sweet paprika powder spice",
    fallbackPath: "assets/plants/photos/137-capsicum-annuum.jpg",
  },
  15: { search: "urfa biber isot pepper flakes" },
  16: {
    search: "cumin seeds spice",
    fallbackPath: "assets/plants/photos/27-cumin.jpg",
  },
  17: {
    search: "dried thyme oregano herb",
    fallbackPath: "assets/plants/photos/109-origanum-vulgare.jpg",
  },
  18: { search: "cinnamon powder spice ground" },
  19: {
    search: "black peppercorns spice",
    fallbackPath: "assets/plants/photos/148-piper-longum.jpg",
  },
  20: { search: "sumac spice powder rhus coriaria" },
  21: { search: "cinnamon sticks spice cinnamomum" },
  22: {
    search: "ginger powder spice",
    fallbackPath: "assets/plants/photos/13-ginger.jpg",
  },
  23: {
    search: "turmeric powder spice curcuma longa",
    fallbackPath: "assets/plants/photos/14-openverse.jpg",
  },
  24: { search: "white sesame seeds spice" },
  25: { search: "sesame seeds spice simit" },
  26: {
    search: "clove spice syzygium aromaticum",
    fallbackPath: "assets/plants/photos/138-syzygium-aromaticum.jpg",
  },
  27: {
    search: "nigella sativa black cumin seeds",
    fallbackPath: "assets/plants/photos/22-nigella-sativa.jpg",
  },
  28: {
    search: "flax seeds linum usitatissimum",
    fallbackPath: "assets/plants/photos/225-linum-usitatissimum.jpg",
  },
  29: {
    search: "fennel seeds spice foeniculum",
    fallbackPath: "assets/plants/photos/16-fennel.jpg",
  },
  30: { search: "henna powder lawsonia inermis" },

  // ── Çay (31–38) ───────────────────────────────────────────────────────────
  31: { search: "winter herbal tea blend loose" },
  32: { search: "herbal atom tea blend loose" },
  33: { search: "herbal slimming tea blend" },
  34: {
    search: "white tea camellia sinensis",
    fallbackPath: "assets/plants/photos/96-camellia-sinensis.jpg",
  },
  35: {
    search: "green tea bags camellia sinensis",
    fallbackPath: "assets/plants/photos/96-camellia-sinensis.jpg",
  },
  36: {
    search: "loose green tea leaves",
    fallbackPath: "assets/plants/photos/96-camellia-sinensis.jpg",
  },
  37: {
    search: "ceylon black tea leaves",
    fallbackPath: "assets/plants/photos/96-camellia-sinensis.jpg",
  },
  38: {
    search: "herbal tea apricot rosemary blend",
    fallbackPath: "assets/plants/photos/05-salvia-rosmarinus.jpg",
  },

  // ── Detox Ürünleri (39–48) ────────────────────────────────────────────────
  39: { search: "bromelain pineapple extract syrup bottle" },
  40: { search: "herbal thermogenic detox supplement powder" },
  41: {
    search: "bitter melon momordica charantia supplement",
    fallbackPath: "assets/plants/photos/79-momordica-charantia.jpg",
  },
  42: { search: "apple cider vinegar detox bottle" },
  43: { search: "apple cider vinegar mastic gum bottle" },
  44: { search: "acerola cherry extract malpighia" },
  45: { search: "matcha green tea powder detox" },
  46: { search: "matcha bromelain powder supplement" },
  47: { search: "strawberry matcha powder" },
  48: {
    search: "chicory root coffee cichorium intybus",
    fallbackPath: "assets/plants/photos/179-cichorium-intybus.jpg",
  },

  // ── Kahve (49–51) ─────────────────────────────────────────────────────────
  49: { search: "turkish coffee ground cezve" },
  50: { search: "turkish dibek coffee ground" },
  51: {
    search: "menengic coffee pistacia terebinthus",
    fallbackPath: "assets/plants/photos/82-prunus-mahaleb.jpg",
  },

  // ── Kurutulmuş Ürünler (52–56) ────────────────────────────────────────────
  52: {
    search: "dried red pepper dolma",
    fallbackPath: "assets/plants/photos/137-capsicum-annuum.jpg",
  },
  53: { search: "dried eggplant dolma aubergine" },
  54: { search: "sun dried tomatoes" },
  55: {
    search: "dried figs ficus carica",
    fallbackPath: "assets/plants/photos/165-ficus-carica.jpg",
  },
  56: { search: "dried mulberry fruit" },

  // ── Macunlar (57–67) ──────────────────────────────────────────────────────
  57: { search: "turkish herbal paste macun jar" },
  58: {
    search: "ginseng honey pollen herbal paste",
    fallbackPath: "assets/plants/photos/69-panax-ginseng.jpg",
  },
  59: {
    search: "artichoke turmeric herbal paste macun",
    fallbackPath: "assets/plants/photos/060-cynara-scolymus.jpg",
  },
  60: { search: "herbal bitter paste macun jar" },
  61: { search: "energy herbal paste macun performance" },
  62: { search: "mandarin orange marmalade paste" },
  63: { search: "children herbal paste macun jar" },
  64: {
    search: "pine cone syrup kozalak",
    fallbackPath: "assets/plants/photos/210-abies-alba.jpg",
  },
  65: { search: "propolis honey paste jar" },
  66: { search: "turkish sultan macun herbal paste" },
  67: {
    search: "pine cone syrup stevia kozalak",
    fallbackPath: "assets/plants/photos/210-abies-alba.jpg",
  },

  // ── Meyve Özü (68–76) ─────────────────────────────────────────────────────
  68: { search: "tropical fruit juice concentrate bottle" },
  69: {
    search: "bilberry blueberry juice vaccinium myrtillus",
    fallbackPath: "assets/plants/photos/169-vaccinium-myrtillus.jpg",
  },
  70: { search: "sour cherry juice prunus cerasus" },
  71: { search: "black mulberry juice morus nigra" },
  72: {
    search: "elecampane andiz pekmez inula helenium",
    fallbackPath: "assets/plants/photos/37-inula-helenium.jpg",
  },
  73: { search: "date molasses syrup phoenix dactylifera" },
  74: { search: "carob molasses ceratonia siliqua" },
  75: { search: "mulberry molasses pekmez dut" },
  76: {
    search: "cranberry juice vaccinium macrocarpon",
    fallbackPath: "assets/plants/photos/170-vaccinium-macrocarpon.jpg",
  },

  // ── Sirkeler / Suyu (77–86) ──────────────────────────────────────────────
  77: { search: "apple cider vinegar bottle" },
  78: {
    search: "pine cone syrup bottle kozalak",
    fallbackPath: "assets/plants/photos/210-abies-alba.jpg",
  },
  79: {
    search: "hawthorn berry vinegar crataegus",
    fallbackPath: "assets/plants/photos/95-crataegus-monogyna.jpg",
  },
  80: { search: "pineapple vinegar bottle" },
  81: {
    search: "artichoke vinegar cynara scolymus",
    fallbackPath: "assets/plants/photos/060-cynara-scolymus.jpg",
  },
  82: {
    search: "grape vinegar vitis vinifera bottle",
    fallbackPath: "assets/plants/photos/167-vitis-vinifera.jpg",
  },
  83: {
    search: "rose vinegar rosa damascena bottle",
    fallbackPath: "assets/plants/photos/179-rosa-damascena.jpg",
  },
  84: { search: "herbal vinegar bottle turkish" },
  85: {
    search: "burdock root juice arctium lappa",
    fallbackPath: "assets/plants/photos/180-arctium-lappa.jpg",
  },
  86: {
    search: "artichoke juice cynara scolymus bottle",
    fallbackPath: "assets/plants/photos/060-cynara-scolymus.jpg",
  },
};
