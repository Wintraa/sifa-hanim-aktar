import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  getFavorites,
  toggleFavorite as toggleFavoriteStorage,
  mergeGuestFavoritesIntoUser,
} from "../lib/favorites.js";
import { useAuth } from "./AuthContext.jsx";
import { showToast } from "../lib/toast.js";

const FavoritesContext = createContext(null);

export function FavoritesProvider({ children }) {
  const { user } = useAuth();
  const userId = user?.id ?? null;

  const [favoriteIds, setFavoriteIds] = useState(() => getFavorites(userId));

  useEffect(() => {
    if (userId) {
      mergeGuestFavoritesIntoUser(userId);
    }
    setFavoriteIds(getFavorites(userId));
  }, [userId]);

  const refresh = useCallback(() => {
    setFavoriteIds(getFavorites(userId));
  }, [userId]);

  const toggle = useCallback(
    (plantId) => {
      const active = toggleFavoriteStorage(plantId, userId);
      setFavoriteIds(getFavorites(userId));
      showToast(
        active ? "Favorilere eklendi." : "Favorilerden çıkarıldı.",
        active ? "success" : "info"
      );
      return active;
    },
    [userId]
  );

  const favoriteSet = useMemo(() => new Set(favoriteIds), [favoriteIds]);

  const value = useMemo(
    () => ({
      favoriteIds,
      favoriteSet,
      favoriteCount: favoriteIds.length,
      isFavorite: (id) => favoriteSet.has(Number(id)),
      toggle,
      refresh,
    }),
    [favoriteIds, favoriteSet, toggle, refresh]
  );

  return <FavoritesContext.Provider value={value}>{children}</FavoritesContext.Provider>;
}

export function useFavorites() {
  const ctx = useContext(FavoritesContext);
  if (!ctx) {
    throw new Error("useFavorites FavoritesProvider içinde kullanılmalı.");
  }
  return ctx;
}
