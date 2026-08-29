export const escapeHtml = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

export const debounce = (callback, delay = 180) => {
  let timeoutId;
  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => callback(...args), delay);
  };
};

export const setMetaContent = (selector, content) => {
  const element = document.querySelector(selector);
  const value = String(content ?? "").trim();
  if (element && value) {
    element.setAttribute("content", value);
  }
};
