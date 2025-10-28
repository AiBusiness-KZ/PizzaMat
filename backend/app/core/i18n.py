"""
Internationalization (i18n) support
Supports: Ukrainian (uk), English (en), Russian (ru)
"""

from typing import Dict
from app.config import settings


# Translation dictionaries
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Common
    "app_name": {
        "uk": "PizzaMat",
        "en": "PizzaMat",
        "ru": "PizzaMat"
    },
    "welcome": {
        "uk": "Ласкаво просимо!",
        "en": "Welcome!",
        "ru": "Добро пожаловать!"
    },
    "success": {
        "uk": "Успішно",
        "en": "Success",
        "ru": "Успешно"
    },
    "error": {
        "uk": "Помилка",
        "en": "Error",
        "ru": "Ошибка"
    },
    
    # Auth
    "auth_required": {
        "uk": "Необхідна авторизація",
        "en": "Authorization required",
        "ru": "Требуется авторизация"
    },
    "invalid_credentials": {
        "uk": "Невірні облікові дані",
        "en": "Invalid credentials",
        "ru": "Неверные учетные данные"
    },
    "user_registered": {
        "uk": "Користувач успішно зареєстрований",
        "en": "User registered successfully",
        "ru": "Пользователь успешно зарегистрирован"
    },
    "user_exists": {
        "uk": "Користувач вже існує",
        "en": "User already exists",
        "ru": "Пользователь уже существует"
    },
    
    # Orders
    "order_created": {
        "uk": "Замовлення створено",
        "en": "Order created",
        "ru": "Заказ создан"
    },
    "order_not_found": {
        "uk": "Замовлення не знайдено",
        "en": "Order not found",
        "ru": "Заказ не найден"
    },
    "order_confirmed": {
        "uk": "Замовлення підтверджено",
        "en": "Order confirmed",
        "ru": "Заказ подтвержден"
    },
    "order_cancelled": {
        "uk": "Замовлення скасовано",
        "en": "Order cancelled",
        "ru": "Заказ отменен"
    },
    "order_pending": {
        "uk": "Очікує оплати",
        "en": "Pending payment",
        "ru": "Ожидает оплаты"
    },
    "order_paid": {
        "uk": "Оплачено",
        "en": "Paid",
        "ru": "Оплачен"
    },
    "order_completed": {
        "uk": "Виконано",
        "en": "Completed",
        "ru": "Выполнен"
    },
    
    # Receipt
    "receipt_uploaded": {
        "uk": "Чек завантажено",
        "en": "Receipt uploaded",
        "ru": "Чек загружен"
    },
    "receipt_invalid": {
        "uk": "Невірний чек",
        "en": "Invalid receipt",
        "ru": "Недействительный чек"
    },
    "receipt_duplicate": {
        "uk": "Цей чек вже використовувався",
        "en": "This receipt has already been used",
        "ru": "Этот чек уже использовался"
    },
    "receipt_validating": {
        "uk": "Перевірка чеку...",
        "en": "Validating receipt...",
        "ru": "Проверка чека..."
    },
    
    # Products
    "product_not_found": {
        "uk": "Товар не знайдено",
        "en": "Product not found",
        "ru": "Товар не найден"
    },
    "product_unavailable": {
        "uk": "Товар недоступний",
        "en": "Product unavailable",
        "ru": "Товар недоступен"
    },
    
    # Locations
    "location_not_found": {
        "uk": "Точку видачі не знайдено",
        "en": "Pickup location not found",
        "ru": "Точка выдачи не найдена"
    },
    "select_location": {
        "uk": "Оберіть точку видачі",
        "en": "Select pickup location",
        "ru": "Выберите точку выдачи"
    },
    
    # Validation
    "validation_error": {
        "uk": "Помилка валідації",
        "en": "Validation error",
        "ru": "Ошибка валидации"
    },
    "required_field": {
        "uk": "Обов'язкове поле",
        "en": "Required field",
        "ru": "Обязательное поле"
    },
    "invalid_format": {
        "uk": "Невірний формат",
        "en": "Invalid format",
        "ru": "Неверный формат"
    },
    "file_too_large": {
        "uk": "Файл занадто великий",
        "en": "File too large",
        "ru": "Файл слишком большой"
    },
    "invalid_file_type": {
        "uk": "Невірний тип файлу",
        "en": "Invalid file type",
        "ru": "Неверный тип файла"
    },
    
    # Cart
    "cart_empty": {
        "uk": "Кошик порожній",
        "en": "Cart is empty",
        "ru": "Корзина пуста"
    },
    "add_to_cart": {
        "uk": "Додати до кошика",
        "en": "Add to cart",
        "ru": "Добавить в корзину"
    },
    
    # Buttons
    "confirm": {
        "uk": "Підтвердити",
        "en": "Confirm",
        "ru": "Подтвердить"
    },
    "cancel": {
        "uk": "Скасувати",
        "en": "Cancel",
        "ru": "Отменить"
    },
    "save": {
        "uk": "Зберегти",
        "en": "Save",
        "ru": "Сохранить"
    },
    "delete": {
        "uk": "Видалити",
        "en": "Delete",
        "ru": "Удалить"
    },
    "back": {
        "uk": "Назад",
        "en": "Back",
        "ru": "Назад"
    },
}


class Translator:
    """Simple translator class"""
    
    def __init__(self, language: str = None):
        self.language = language or settings.DEFAULT_LANGUAGE
        if self.language not in settings.SUPPORTED_LANGUAGES:
            self.language = settings.DEFAULT_LANGUAGE
    
    def translate(self, key: str, **kwargs) -> str:
        """
        Translate a key to current language
        
        Args:
            key: Translation key
            **kwargs: Format arguments
            
        Returns:
            Translated string
        """
        translation_dict = TRANSLATIONS.get(key, {})
        text = translation_dict.get(self.language, translation_dict.get("en", key))
        
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text
    
    def t(self, key: str, **kwargs) -> str:
        """Shorthand for translate()"""
        return self.translate(key, **kwargs)


def get_translator(language: str = None) -> Translator:
    """Get translator instance for specified language"""
    return Translator(language)


# Default translator
_ = get_translator()
