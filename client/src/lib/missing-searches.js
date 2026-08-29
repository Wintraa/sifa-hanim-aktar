const QUEUE_KEY = "sifaMissingSearchesQueue_v1";

function readQueue() {
  try {
    const raw = localStorage.getItem(QUEUE_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function writeQueue(list) {
  try {
    localStorage.setItem(QUEUE_KEY, JSON.stringify(list.slice(-200)));
  } catch {
    /* kota */
  }
}

/** Yerel yedek kuyruk (API yoksa da kaybolmasın). */
export function enqueueMissingSearch(arama) {
  const q = String(arama || "").trim();
  if (q.length < 2) return;
  const list = readQueue();
  const key = q.toLocaleLowerCase("tr");
  if (list.some((item) => item.arama.toLocaleLowerCase("tr") === key)) return;
  list.push({ arama: q, at: new Date().toISOString() });
  writeQueue(list);
}

export function getMissingSearchQueue() {
  return readQueue();
}

export function clearMissingSearchQueue() {
  writeQueue([]);
}
