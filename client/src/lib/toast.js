const TOAST_HOST_ID = "toastHost";

const ensureHost = () => {
  let host = document.querySelector(`#${TOAST_HOST_ID}`);
  if (host) return host;
  host = document.createElement("div");
  host.id = TOAST_HOST_ID;
  host.className = "toast-host";
  host.setAttribute("aria-live", "polite");
  host.setAttribute("aria-relevant", "additions");
  document.body.appendChild(host);
  return host;
};

export const showToast = (message, type = "info", durationMs = 3200) => {
  const text = String(message ?? "").trim();
  if (!text) return;
  const host = ensureHost();
  const toast = document.createElement("div");
  toast.className = `toast toast--${type}`;
  toast.setAttribute("role", type === "error" ? "alert" : "status");
  toast.textContent = text;
  host.appendChild(toast);
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const leaveDelay = prefersReducedMotion ? 0 : 220;
  window.setTimeout(() => {
    toast.classList.add("is-leaving");
    window.setTimeout(() => toast.remove(), leaveDelay);
  }, durationMs);
};
