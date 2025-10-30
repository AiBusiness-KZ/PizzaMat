import { useState, useEffect } from 'react';
import { ShoppingCart, MapPin } from 'lucide-react';
import { Category, Product, PickupLocation } from '@/shared/types';
import { useCart } from '@/hooks/useCart';
import { useLanguage } from '@/contexts/LanguageContext';
import ProductCard from '@/components/ProductCard';
import CartSidebar from '@/components/CartSidebar';
import LanguageSwitch from '@/components/LanguageSwitch';
import { useNavigate } from 'react-router';

interface City {
  id: number;
  name: string;
  is_active: boolean;
}

export default function Home() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [pickupLocations, setPickupLocations] = useState<PickupLocation[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | 'all'>('all');
  const [selectedCity, setSelectedCity] = useState<number | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<string>('');
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { t } = useLanguage();

  const {
    items,
    addToCart,
    removeFromCart,
    updateQuantity,
    totalAmount,
    totalItems,
  } = useCart();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [categoriesRes, productsRes, citiesRes, locationsRes] = await Promise.all([
        fetch('/api/categories'),
        fetch('/api/products'),
        fetch('/api/cities'),
        fetch('/api/pickup-locations'),
      ]);

      const [categoriesData, productsData, citiesData, locationsData] = await Promise.all([
        categoriesRes.json(),
        productsRes.json(),
        citiesRes.json(),
        locationsRes.json(),
      ]);

      console.log('Categories loaded:', categoriesData);
      console.log('Products loaded:', productsData);
      console.log('Cities loaded:', citiesData);
      console.log('Locations loaded:', locationsData);
      
      if (categoriesData.success) setCategories(categoriesData.data);
      if (productsData.success) setProducts(productsData.data);
      if (citiesData.success) {
        setCities(citiesData.data);
        // Auto-select first city if available
        if (citiesData.data.length > 0) {
          setSelectedCity(citiesData.data[0].id);
        }
      }
      if (locationsData.success) {
        setPickupLocations(locationsData.data);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckout = async () => {
    console.log('Checkout attempt:', {
      selectedCity,
      selectedLocation,
      filteredLocations,
      items: items.length
    });
    
    if (!selectedCity) {
      alert(t('messages.selectCity') || 'Пожалуйста, выберите город');
      return;
    }
    
    if (!selectedLocation || selectedLocation === '') {
      alert(t('messages.selectLocation') || 'Пожалуйста, выберите точку выдачи');
      return;
    }
    
    if (items.length === 0) {
      alert(t('messages.emptyCart') || 'Корзина пуста');
      return;
    }
    
    try {
      // Get telegram_id from Telegram WebApp or URL params
      let telegramId: number | null = null;
      
      if (window.Telegram?.WebApp?.initDataUnsafe?.user?.id) {
        telegramId = window.Telegram.WebApp.initDataUnsafe.user.id;
      } else {
        // Fallback: get from URL params
        const urlParams = new URLSearchParams(window.location.search);
        const tgId = urlParams.get('telegram_id');
        if (tgId) {
          telegramId = parseInt(tgId);
        }
      }
      
      if (!telegramId) {
        alert('Не удалось получить telegram_id. Пожалуйста, откройте через бота.');
        return;
      }
      
      // Prepare order data
      const orderData = {
        telegram_id: telegramId,
        location_id: parseInt(selectedLocation),
        total_amount: totalAmount,
        items: items.map(item => ({
          product_id: item.product.id,
          quantity: item.quantity,
          unit_price: item.product.base_price,
          selected_options: item.selectedOptions.length > 0 ? {
            options: item.selectedOptions
          } : null,
          options_price: item.selectedOptions.reduce((sum, opt) => sum + opt.price_modifier, 0),
          total_price: item.totalPrice
        }))
      };
      
      console.log('Creating order:', orderData);
      
      // Create order
      const response = await fetch('/api/orders/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
      });
      
      const result = await response.json();
      
      if (result.success) {
        // Clear cart
        items.forEach(item => removeFromCart(item.id));
        
        // Show success message
        alert(`${result.message}\n\nКод заказа: ${result.order.order_code}`);
        
        // Close WebApp and return to bot
        if (window.Telegram?.WebApp) {
          window.Telegram.WebApp.close();
        }
      } else {
        alert('Ошибка при создании заказа. Попробуйте еще раз.');
      }
    } catch (error) {
      console.error('Error creating order:', error);
      alert('Ошибка при создании заказа. Попробуйте еще раз.');
    }
    
    setIsCartOpen(false);
  };

  // Filter locations by selected city
  const filteredLocations = selectedCity
    ? pickupLocations.filter(loc => loc.city_id === selectedCity)
    : pickupLocations;

  // Auto-select first location when city changes
  useEffect(() => {
    console.log('Auto-select location effect:', {
      filteredLocationsCount: filteredLocations.length,
      currentSelection: selectedLocation,
      firstLocation: filteredLocations[0]?.id
    });
    
    if (filteredLocations.length > 0) {
      // Check if current selection is valid for filtered locations
      // Use id instead of location_id since location_id is null in database
      const isValidSelection = filteredLocations.some(loc => String(loc.id) === selectedLocation);
      
      if (!isValidSelection) {
        // Auto-select first location using id
        const firstLocationId = String(filteredLocations[0].id);
        console.log('Auto-selecting location:', firstLocationId);
        setSelectedLocation(firstLocationId);
      }
    } else {
      // No locations available, reset selection
      setSelectedLocation('');
    }
  }, [selectedCity, filteredLocations]);

  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(p => p.category_id === selectedCategory);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
        <p className="mt-4 text-gray-600">{t('messages.loading')}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-3 py-3">
          {/* First row: Title and Cart */}
          <div className="flex items-center justify-between mb-3">
            <div className="flex-1 min-w-0">
              <h1 className="text-lg font-bold text-gray-900 truncate">🍕 {t('app.title')}</h1>
              <p className="text-xs text-gray-600 truncate">{t('app.subtitle')}</p>
            </div>
            
            <div className="flex items-center space-x-2 ml-2">
              <LanguageSwitch />
              <button
                onClick={() => setIsCartOpen(true)}
                className="relative bg-orange-500 hover:bg-orange-600 text-white p-2 rounded-lg transition-colors flex-shrink-0"
              >
                <ShoppingCart className="w-5 h-5" />
                {totalItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                    {totalItems}
                  </span>
                )}
              </button>
            </div>
          </div>
          
          {/* Second row: Location selectors */}
          <div className="flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-gray-500 flex-shrink-0" />
            <select
              value={selectedCity || ''}
              onChange={(e) => setSelectedCity(Number(e.target.value))}
              className="text-sm border border-gray-300 rounded-lg px-2 py-1 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 flex-1 min-w-0"
            >
              <option value="">{t('location.selectCity') || 'Город'}</option>
              {cities.map(city => (
                <option key={city.id} value={city.id}>
                  {city.name}
                </option>
              ))}
            </select>
            {selectedCity && (
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="text-sm border border-gray-300 rounded-lg px-2 py-1 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 flex-1 min-w-0"
              >
                <option value="">{t('location.placeholder') || 'Точка'}</option>
                {filteredLocations.map(location => (
                  <option key={location.id} value={String(location.id)}>
                    {location.name}
                  </option>
                ))}
              </select>
            )}
          </div>
        </div>
      </header>

      {/* Categories filter - only show if categories loaded */}
      {categories.length > 0 && (
        <div className="bg-white border-b">
          <div className="max-w-6xl mx-auto px-3">
            <div className="flex space-x-1 overflow-x-auto py-2.5 scrollbar-hide">
              <button
                onClick={() => setSelectedCategory('all')}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-colors flex-shrink-0 ${
                  selectedCategory === 'all'
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {t('navigation.all') || 'Все'}
              </button>
              {categories.map(category => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-colors flex-shrink-0 ${
                    selectedCategory === category.id
                      ? 'bg-orange-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {category.name}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      <main className="max-w-6xl mx-auto px-3 py-4">
        {!selectedCity && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <p className="text-yellow-800 font-medium">
              {t('messages.cityWarning') || 'Пожалуйста, выберите город'}
            </p>
          </div>
        )}
        
        {selectedCity && !selectedLocation && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <p className="text-yellow-800 font-medium">
              {t('messages.locationWarning')}
            </p>
          </div>
        )}
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map(product => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={addToCart}
            />
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">{t('category.empty')}</p>
          </div>
        )}
      </main>

      <CartSidebar
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        items={items}
        onUpdateQuantity={updateQuantity}
        onRemoveItem={removeFromCart}
        totalAmount={totalAmount}
        onCheckout={handleCheckout}
      />
    </div>
  );
}
