"""
Main menu keyboards for bot navigation
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from typing import List, Optional


def get_main_menu_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """
    Get main menu keyboard with common actions
    """
    texts = {
        "uk": {
            "menu": "🍕 Меню",
            "orders": "📦 Мої замовлення",
            "support": "💬 Підтримка",
            "settings": "⚙️ Налаштування"
        },
        "en": {
            "menu": "🍕 Menu",
            "orders": "📦 My Orders",
            "support": "💬 Support",
            "settings": "⚙️ Settings"
        },
        "ru": {
            "menu": "🍕 Меню",
            "orders": "📦 Мои заказы",
            "support": "💬 Поддержка",
            "settings": "⚙️ Настройки"
        }
    }

    t = texts.get(language, texts["uk"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["menu"])],
            [KeyboardButton(text=t["orders"]), KeyboardButton(text=t["support"])],
            [KeyboardButton(text=t["settings"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    return keyboard


def get_phone_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """
    Get keyboard for phone number sharing
    """
    texts = {
        "uk": "📱 Поділитися номером",
        "en": "📱 Share phone number",
        "ru": "📱 Поделиться номером"
    }

    text = texts.get(language, texts["uk"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text, request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard


def get_webapp_keyboard(webapp_url: str, language: str = "uk") -> InlineKeyboardMarkup:
    """
    Get keyboard with WebApp button to open menu
    """
    texts = {
        "uk": "🍕 Відкрити меню",
        "en": "🍕 Open menu",
        "ru": "🍕 Открыть меню"
    }

    text = texts.get(language, texts["uk"])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=text,
                web_app=WebAppInfo(url=webapp_url)
            )]
        ]
    )

    return keyboard


def get_cities_keyboard(cities: List[dict], language: str = "uk") -> InlineKeyboardMarkup:
    """
    Get keyboard for city selection
    """
    buttons = []

    for city in cities:
        buttons.append([InlineKeyboardButton(
            text=f"📍 {city['name']}",
            callback_data=f"city_{city['id']}"
        )])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_locations_keyboard(locations: List[dict], language: str = "uk") -> InlineKeyboardMarkup:
    """
    Get keyboard for pickup location selection
    """
    buttons = []

    for location in locations:
        buttons.append([InlineKeyboardButton(
            text=f"📍 {location['name']}",
            callback_data=f"location_{location['id']}"
        )])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_order_actions_keyboard(order_id: int, language: str = "uk") -> InlineKeyboardMarkup:
    """
    Get keyboard for order actions (upload receipt, cancel, etc.)
    """
    texts = {
        "uk": {
            "upload_receipt": "📸 Завантажити чек",
            "cancel": "❌ Скасувати замовлення",
            "view_details": "📋 Деталі замовлення"
        },
        "en": {
            "upload_receipt": "📸 Upload receipt",
            "cancel": "❌ Cancel order",
            "view_details": "📋 Order details"
        },
        "ru": {
            "upload_receipt": "📸 Загрузить чек",
            "cancel": "❌ Отменить заказ",
            "view_details": "📋 Детали заказа"
        }
    }

    t = texts.get(language, texts["uk"])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=t["upload_receipt"],
                callback_data=f"upload_receipt_{order_id}"
            )],
            [InlineKeyboardButton(
                text=t["view_details"],
                callback_data=f"order_details_{order_id}"
            )],
            [InlineKeyboardButton(
                text=t["cancel"],
                callback_data=f"cancel_order_{order_id}"
            )]
        ]
    )

    return keyboard


def get_manager_order_keyboard(order_id: int, language: str = "uk") -> InlineKeyboardMarkup:
    """
    Get keyboard for manager to confirm/reject order
    """
    texts = {
        "uk": {
            "confirm": "✅ Підтвердити",
            "reject": "❌ Відхилити"
        },
        "en": {
            "confirm": "✅ Confirm",
            "reject": "❌ Reject"
        },
        "ru": {
            "confirm": "✅ Подтвердить",
            "reject": "❌ Отклонить"
        }
    }

    t = texts.get(language, texts["uk"])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t["confirm"],
                    callback_data=f"manager_confirm_{order_id}"
                ),
                InlineKeyboardButton(
                    text=t["reject"],
                    callback_data=f"manager_reject_{order_id}"
                )
            ]
        ]
    )

    return keyboard


def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Get keyboard for language selection
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
            ],
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
            ]
        ]
    )

    return keyboard


def get_cancel_keyboard(language: str = "uk") -> ReplyKeyboardMarkup:
    """
    Get keyboard with cancel button
    """
    texts = {
        "uk": "❌ Скасувати",
        "en": "❌ Cancel",
        "ru": "❌ Отменить"
    }

    text = texts.get(language, texts["uk"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard
