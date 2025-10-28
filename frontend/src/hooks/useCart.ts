import { useState, useCallback } from 'react';
import { Product, ProductOption } from '@/shared/types';

export interface CartItem {
  id: string;
  product: Product;
  quantity: number;
  selectedOptions: ProductOption[];
  totalPrice: number;
}

export function useCart() {
  const [items, setItems] = useState<CartItem[]>([]);

  const addToCart = useCallback((product: Product, selectedOptions: ProductOption[], quantity: number = 1) => {
    const optionsPrice = selectedOptions.reduce((sum, option) => sum + option.price_modifier, 0);
    const itemPrice = (product.base_price + optionsPrice) * quantity;
    
    // Создаем уникальный ID на основе продукта и выбранных опций
    // Используем product.id вместо product_id, так как product_id может быть null
    const itemId = `${product.id}-${selectedOptions.map(o => `${o.type}:${o.name}`).join('-')}`;
    
    setItems(prev => {
      const existingItemIndex = prev.findIndex(item => item.id === itemId);
      
      if (existingItemIndex >= 0) {
        // Обновляем существующий элемент
        const newItems = [...prev];
        newItems[existingItemIndex] = {
          ...newItems[existingItemIndex],
          quantity: newItems[existingItemIndex].quantity + quantity,
          totalPrice: newItems[existingItemIndex].totalPrice + itemPrice,
        };
        return newItems;
      } else {
        // Добавляем новый элемент
        return [...prev, {
          id: itemId,
          product,
          selectedOptions,
          quantity,
          totalPrice: itemPrice,
        }];
      }
    });
  }, []);

  const removeFromCart = useCallback((itemId: string) => {
    setItems(prev => prev.filter(item => item.id !== itemId));
  }, []);

  const updateQuantity = useCallback((itemId: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeFromCart(itemId);
      return;
    }

    setItems(prev => prev.map(item => {
      if (item.id === itemId) {
        const optionsPrice = item.selectedOptions.reduce((sum, option) => sum + option.price_modifier, 0);
        const unitPrice = item.product.base_price + optionsPrice;
        return {
          ...item,
          quantity: newQuantity,
          totalPrice: unitPrice * newQuantity,
        };
      }
      return item;
    }));
  }, [removeFromCart]);

  const clearCart = useCallback(() => {
    setItems([]);
  }, []);

  const totalAmount = items.reduce((sum, item) => sum + item.totalPrice, 0);
  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);

  return {
    items,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    totalAmount,
    totalItems,
  };
}
