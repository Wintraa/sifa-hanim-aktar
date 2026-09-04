import { createContext, useCallback, useContext, useMemo, useState } from "react";
import {
  addToCart as addToCartStorage,
  buildCartWhatsAppMessage,
  cartItemCount,
  cartLineCount,
  clearCart as clearCartStorage,
  readCart,
  removeFromCart as removeFromCartStorage,
  setCartQuantity as setCartQuantityStorage,
} from "../lib/cart.js";
import { whatsappUrl } from "../lib/whatsapp.js";
import { showToast } from "../lib/toast.js";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [items, setItems] = useState(() => readCart());
  const [isOpen, setIsOpen] = useState(false);

  const sync = useCallback(() => {
    setItems(readCart());
  }, []);

  const openCart = useCallback(() => setIsOpen(true), []);
  const closeCart = useCallback(() => setIsOpen(false), []);
  const toggleCart = useCallback(() => setIsOpen((v) => !v), []);

  const addItem = useCallback(
    (product, quantity = 1) => {
      const next = addToCartStorage(product, quantity);
      setItems(next);
      const name = String(product?.ad || "Ürün");
      showToast(`${name} sepete eklendi.`, "success");
      setIsOpen(true);
      return next;
    },
    []
  );

  const setQuantity = useCallback((productId, quantity) => {
    const next = setCartQuantityStorage(productId, quantity);
    setItems(next);
    return next;
  }, []);

  const removeItem = useCallback((productId) => {
    const next = removeFromCartStorage(productId);
    setItems(next);
    showToast("Ürün sepetten çıkarıldı.", "info");
    return next;
  }, []);

  const clearCart = useCallback(() => {
    clearCartStorage();
    setItems([]);
    showToast("Sepet temizlendi.", "info");
  }, []);

  const isInCart = useCallback(
    (productId) => items.some((item) => item.id === Number(productId)),
    [items]
  );

  const whatsappHref = useMemo(() => whatsappUrl(buildCartWhatsAppMessage(items)), [items]);

  const value = useMemo(
    () => ({
      items,
      isOpen,
      itemCount: cartItemCount(items),
      lineCount: cartLineCount(items),
      addItem,
      setQuantity,
      removeItem,
      clearCart,
      isInCart,
      openCart,
      closeCart,
      toggleCart,
      whatsappHref,
      sync,
    }),
    [
      items,
      isOpen,
      addItem,
      setQuantity,
      removeItem,
      clearCart,
      isInCart,
      openCart,
      closeCart,
      toggleCart,
      whatsappHref,
      sync,
    ]
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart CartProvider içinde kullanılmalı.");
  return ctx;
}
