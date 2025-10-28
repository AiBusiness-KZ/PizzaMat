import { useState } from 'react';
import { Plus, Minus } from 'lucide-react';
import { Product, ProductOption } from '@/shared/types';

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product, selectedOptions: ProductOption[], quantity: number) => void;
}

export default function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const [selectedOptions, setSelectedOptions] = useState<Record<string, ProductOption>>({});
  const [quantity, setQuantity] = useState(1);
  const [showOptions, setShowOptions] = useState(false);

  const optionTypes = product.options ? [...new Set(product.options.map(opt => opt.type))] : [];
  
  const calculatePrice = () => {
    const optionsPrice = Object.values(selectedOptions).reduce((sum, option) => sum + option.price_modifier, 0);
    return (product.base_price + optionsPrice) * quantity;
  };

  const handleOptionSelect = (optionType: string, option: ProductOption) => {
    setSelectedOptions(prev => ({
      ...prev,
      [optionType]: option,
    }));
  };

  const handleAddToCart = () => {
    const options = Object.values(selectedOptions);
    onAddToCart(product, options, quantity);
    setQuantity(1);
    setShowOptions(false);
  };

  const canAddToCart = optionTypes.length === 0 || optionTypes.every(type => selectedOptions[type]);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
      {product.photo_url && (
        <div className="aspect-video w-full overflow-hidden">
          <img
            src={product.photo_url}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        </div>
      )}
      
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 mb-1">{product.name}</h3>
        {product.description && (
          <p className="text-sm text-gray-600 mb-3">{product.description}</p>
        )}
        
        <div className="flex items-center justify-between mb-3">
          <span className="text-lg font-bold text-gray-900">
            {calculatePrice()} ₴
          </span>
          {product.base_price !== calculatePrice() / quantity && (
            <span className="text-sm text-gray-500 line-through">
              {product.base_price * quantity} ₴
            </span>
          )}
        </div>

        {optionTypes.length > 0 && (
          <div className="mb-4">
            <button
              onClick={() => setShowOptions(!showOptions)}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              {showOptions ? 'Скрыть опції' : 'Показати опції'}
            </button>
            
            {showOptions && (
              <div className="mt-3 space-y-3">
                {optionTypes.map(optionType => {
                  const typeOptions = product.options!.filter(opt => opt.type === optionType);
                  return (
                    <div key={optionType}>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        {optionType}
                      </label>
                      <div className="flex flex-wrap gap-2">
                        {typeOptions.map(option => (
                          <button
                            key={`${option.type}-${option.name}`}
                            onClick={() => handleOptionSelect(optionType, option)}
                            className={`px-3 py-1 text-sm rounded-full border transition-colors ${
                              selectedOptions[optionType]?.name === option.name
                                ? 'bg-blue-500 text-white border-blue-500'
                                : 'bg-gray-50 text-gray-700 border-gray-200 hover:border-gray-300'
                            }`}
                          >
                            {option.name}
                            {option.price_modifier > 0 && ` +${option.price_modifier}₴`}
                          </button>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setQuantity(Math.max(1, quantity - 1))}
              className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
              disabled={quantity <= 1}
            >
              <Minus className="w-4 h-4" />
            </button>
            <span className="font-medium min-w-[2rem] text-center">{quantity}</span>
            <button
              onClick={() => setQuantity(quantity + 1)}
              className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>

          <button
            onClick={handleAddToCart}
            disabled={!canAddToCart}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              canAddToCart
                ? 'bg-orange-500 hover:bg-orange-600 text-white'
                : 'bg-gray-200 text-gray-500 cursor-not-allowed'
            }`}
          >
            В кошик
          </button>
        </div>
      </div>
    </div>
  );
}
