import { X, Minus, Plus, ShoppingBag } from 'lucide-react';
import { CartItem } from '@/hooks/useCart';
import { useLanguage } from '@/contexts/LanguageContext';

interface CartSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  items: CartItem[];
  onUpdateQuantity: (itemId: string, quantity: number) => void;
  onRemoveItem: (itemId: string) => void;
  totalAmount: number;
  onCheckout: () => void;
}

export default function CartSidebar({
  isOpen,
  onClose,
  items,
  onUpdateQuantity,
  onRemoveItem,
  totalAmount,
  onCheckout,
}: CartSidebarProps) {
  const { t } = useLanguage();
  
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-3 border-b flex-shrink-0">
          <div className="flex items-center space-x-2 min-w-0 flex-1">
            <ShoppingBag className="w-5 h-5 text-orange-500 flex-shrink-0" />
            <h2 className="text-base font-semibold truncate">{t('cart.title')}</h2>
            <span className="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded-full flex-shrink-0">
              {items.length}
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-lg transition-colors flex-shrink-0 ml-2"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Items */}
        <div className="flex-1 overflow-y-auto p-3" style={{ maxHeight: 'calc(100vh - 140px)' }}>
          {items.length === 0 ? (
            <div className="text-center py-12">
              <ShoppingBag className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-sm">{t('cart.empty')}</p>
              <p className="text-xs text-gray-400 mt-2">{t('cart.emptyText')}</p>
            </div>
          ) : (
            <div className="space-y-3">
              {items.map(item => (
                <div key={item.id} className="bg-gray-50 rounded-lg p-2.5">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1 min-w-0 pr-2">
                      <h4 className="font-medium text-gray-900 text-sm truncate">{item.product.name}</h4>
                      {item.selectedOptions.length > 0 && (
                        <div className="text-xs text-gray-600 mt-1 flex flex-wrap gap-1">
                          {item.selectedOptions.map(option => (
                            <span key={`${option.type}-${option.name}`} className="inline-block">
                              {option.name}
                              {option.price_modifier > 0 && ` +${option.price_modifier}₴`}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    <button
                      onClick={() => onRemoveItem(item.id)}
                      className="text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                        className="w-7 h-7 rounded-full bg-white hover:bg-gray-100 flex items-center justify-center transition-colors flex-shrink-0"
                        disabled={item.quantity <= 1}
                      >
                        <Minus className="w-3 h-3" />
                      </button>
                      <span className="font-medium min-w-[1.5rem] text-center text-sm">{item.quantity}</span>
                      <button
                        onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                        className="w-7 h-7 rounded-full bg-white hover:bg-gray-100 flex items-center justify-center transition-colors flex-shrink-0"
                      >
                        <Plus className="w-3 h-3" />
                      </button>
                    </div>
                    <span className="font-semibold text-sm">{item.totalPrice} ₴</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer - Fixed at bottom */}
        {items.length > 0 && (
          <div className="border-t p-3 bg-white flex-shrink-0">
            <div className="flex justify-between items-center mb-3">
              <span className="text-base font-semibold">{t('cart.total')}:</span>
              <span className="text-lg font-bold text-orange-600">{totalAmount} ₴</span>
            </div>
            <button
              onClick={onCheckout}
              className="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-2.5 rounded-lg transition-colors text-sm"
            >
              {t('cart.checkout')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
