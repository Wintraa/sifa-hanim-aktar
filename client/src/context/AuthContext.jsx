import { createContext, useCallback, useContext, useMemo, useState } from "react";
import {
  getCurrentUser,
  loginAccount,
  logoutAccount,
  registerAccount,
  updateAccountProfile,
} from "../lib/auth.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => getCurrentUser());

  const refresh = useCallback(() => {
    setUser(getCurrentUser());
  }, []);

  const login = useCallback(async (credentials) => {
    const next = await loginAccount(credentials);
    setUser(next);
    return next;
  }, []);

  const register = useCallback(async (payload) => {
    const next = await registerAccount(payload);
    setUser(next);
    return next;
  }, []);

  const logout = useCallback(() => {
    logoutAccount();
    setUser(null);
  }, []);

  const updateProfile = useCallback(async (partial) => {
    if (!user?.id) throw new Error("Oturum gerekli.");
    const next = await updateAccountProfile(user.id, partial);
    setUser(getCurrentUser());
    return next;
  }, [user?.id]);

  const value = useMemo(
    () => ({
      user,
      isLoggedIn: Boolean(user),
      login,
      register,
      logout,
      updateProfile,
      refresh,
    }),
    [user, login, register, logout, updateProfile, refresh]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth AuthProvider içinde kullanılmalı.");
  return ctx;
}
