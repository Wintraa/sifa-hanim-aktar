const ACCOUNTS_KEY = "sifaHanimAccounts_v1";
const SESSION_KEY = "sifaHanimSession_v1";
const ADMIN_ID = "sifa-admin-v1";
const ADMIN_USERNAME = "admin123";
const ADMIN_EMAIL = "admin@sifahanimaktar.local";

const textEncoder = new TextEncoder();

function randomSalt() {
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

async function hashPassword(password, salt) {
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    textEncoder.encode(password),
    "PBKDF2",
    false,
    ["deriveBits"]
  );
  const bits = await crypto.subtle.deriveBits(
    {
      name: "PBKDF2",
      salt: textEncoder.encode(salt),
      iterations: 120000,
      hash: "SHA-256",
    },
    keyMaterial,
    256
  );
  return Array.from(new Uint8Array(bits), (b) => b.toString(16).padStart(2, "0")).join("");
}

function ensureAdminAccount() {
  const accounts = readAccounts();
  if (accounts.some((a) => a.id === ADMIN_ID)) return;
  accounts.push({
    id: ADMIN_ID,
    email: ADMIN_EMAIL,
    username: ADMIN_USERNAME,
    firstName: "Admin",
    lastName: "Şifa Hanım",
    role: "admin",
    salt: "admin-seed",
    passwordHash: "local-only",
    createdAt: new Date().toISOString().slice(0, 10),
  });
  writeAccounts(accounts);
}

function isAdminIdentifier(value) {
  const v = String(value || "").trim().toLocaleLowerCase("tr");
  return v === ADMIN_USERNAME || v === ADMIN_EMAIL;
}

function readAccounts() {
  try {
    const raw = localStorage.getItem(ACCOUNTS_KEY);
    const list = raw ? JSON.parse(raw) : [];
    return Array.isArray(list) ? list : [];
  } catch {
    return [];
  }
}

function writeAccounts(list) {
  localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(list));
}

function normalizeEmail(email) {
  return String(email || "")
    .trim()
    .toLocaleLowerCase("tr");
}

export function getSession() {
  try {
    // Tarayıcı kapanınca da oturum kalsın (telefon/yenileme)
    const raw =
      localStorage.getItem(SESSION_KEY) || sessionStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    // Eski sessionStorage oturumunu kalıcıya taşı
    if (parsed?.userId && !localStorage.getItem(SESSION_KEY)) {
      localStorage.setItem(SESSION_KEY, raw);
    }
    return parsed;
  } catch {
    return null;
  }
}

export function getCurrentUser() {
  const session = getSession();
  if (!session?.userId) return null;
  const account = readAccounts().find((a) => a.id === session.userId);
  if (!account) {
    clearSession();
    return null;
  }
  return {
    id: account.id,
    email: account.email,
    username: account.username || account.email,
    role: account.role === "admin" ? "admin" : "user",
    firstName: account.firstName,
    lastName: account.lastName,
    fullName: `${account.firstName}${account.lastName ? ` ${account.lastName}` : ""}`.trim(),
    joinDate: account.createdAt,
  };
}

export function isAdminUser(user) {
  return user?.role === "admin";
}

function setSession(userId, email) {
  const payload = JSON.stringify({ userId, email, at: new Date().toISOString() });
  localStorage.setItem(SESSION_KEY, payload);
  try {
    sessionStorage.removeItem(SESSION_KEY);
  } catch {
    /* ignore */
  }
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY);
  try {
    sessionStorage.removeItem(SESSION_KEY);
  } catch {
    /* ignore */
  }
}

export async function registerAccount({ firstName, lastName, email, password }) {
  const mail = normalizeEmail(email);
  if (isAdminIdentifier(mail) || String(email || "").trim().toLocaleLowerCase("tr") === ADMIN_USERNAME) {
    throw new Error("Bu kullanıcı adı rezerve edilmiş.");
  }
  if (!mail || !mail.includes("@")) {
    throw new Error("Geçerli bir e-posta girin.");
  }
  if (!password || password.length < 6) {
    throw new Error("Şifre en az 6 karakter olmalı.");
  }
  const fname = String(firstName || "").trim() || "Üye";
  const lname = String(lastName || "").trim();

  const accounts = readAccounts();
  if (accounts.some((a) => a.email === mail)) {
    throw new Error("Bu e-posta ile zaten kayıt var. Giriş yapmayı deneyin.");
  }

  const salt = randomSalt();
  const passwordHash = await hashPassword(password, salt);
  const account = {
    id: crypto.randomUUID(),
    email: mail,
    firstName: fname,
    lastName: lname,
    salt,
    passwordHash,
    createdAt: new Date().toISOString().slice(0, 10),
  };
  accounts.push(account);
  writeAccounts(accounts);
  setSession(account.id, account.email);
  return getCurrentUser();
}

export async function loginAccount({ email, password }) {
  if (isAdminIdentifier(email)) {
    if (String(password) !== "99161202") {
      throw new Error("Kullanıcı adı veya şifre hatalı.");
    }
    ensureAdminAccount();
    setSession(ADMIN_ID, ADMIN_EMAIL);
    return getCurrentUser();
  }

  const mail = normalizeEmail(email);
  const account = readAccounts().find((a) => a.email === mail);
  if (!account) {
    throw new Error("E-posta veya şifre hatalı.");
  }
  const hash = await hashPassword(password, account.salt);
  if (hash !== account.passwordHash) {
    throw new Error("E-posta veya şifre hatalı.");
  }
  setSession(account.id, account.email);
  return getCurrentUser();
}

export function logoutAccount() {
  clearSession();
}

export async function updateAccountProfile(userId, partial) {
  const accounts = readAccounts();
  const idx = accounts.findIndex((a) => a.id === userId);
  if (idx < 0) throw new Error("Hesap bulunamadı.");
  const next = { ...accounts[idx] };
  if (partial.firstName !== undefined) next.firstName = String(partial.firstName).trim() || "Üye";
  if (partial.lastName !== undefined) next.lastName = String(partial.lastName).trim();
  accounts[idx] = next;
  writeAccounts(accounts);
  return getCurrentUser();
}
