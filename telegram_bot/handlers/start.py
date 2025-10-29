"""
Start command and user registration handlers
"""

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from states import RegistrationStates
from keyboards import (
    get_phone_keyboard,
    get_cities_keyboard,
    get_main_menu_keyboard
)
from services import api_client

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Handle /start command
    Check if user exists, if not - start registration
    """
    telegram_id = message.from_user.id

    # Check if user already registered
    user = await api_client.get_user(telegram_id)

    if user:
        # User already registered
        language = user.get("language", "uk")

        welcome_texts = {
            "uk": f"Привіт, {user['full_name']}! 👋\n\n"
                  f"Рад бачити вас знову! Використовуйте меню нижче для навігації.",
            "en": f"Hello, {user['full_name']}! 👋\n\n"
                  f"Good to see you again! Use the menu below for navigation.",
            "ru": f"Привет, {user['full_name']}! 👋\n\n"
                  f"Рад видеть вас снова! Используйте меню ниже для навигации."
        }

        await message.answer(
            welcome_texts.get(language, welcome_texts["uk"]),
            reply_markup=get_main_menu_keyboard(language)
        )

        # Clear any existing state
        await state.clear()
    else:
        # Start registration
        registration_texts = {
            "uk": "👋 Вітаємо в PizzaMat!\n\n"
                  "Для оформлення замовлень, будь ласка, зареєструйтесь.\n\n"
                  "📱 Поділіться номером телефону, щоб продовжити:",
            "en": "👋 Welcome to PizzaMat!\n\n"
                  "To place orders, please register.\n\n"
                  "📱 Share your phone number to continue:",
            "ru": "👋 Добро пожаловать в PizzaMat!\n\n"
                  "Для оформления заказов, пожалуйста, зарегистрируйтесь.\n\n"
                  "📱 Поделитесь номером телефона, чтобы продолжить:"
        }

        language_code = message.from_user.language_code or "uk"
        if language_code not in ["uk", "en", "ru"]:
            language_code = "uk"

        await state.update_data(language=language_code)
        await state.set_state(RegistrationStates.waiting_for_phone)

        await message.answer(
            registration_texts.get(language_code, registration_texts["uk"]),
            reply_markup=get_phone_keyboard(language_code)
        )


@router.message(RegistrationStates.waiting_for_phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    """
    Handle phone number from contact
    """
    data = await state.get_data()
    language = data.get("language", "uk")

    # Validate that the contact is user's own number
    if message.contact.user_id != message.from_user.id:
        error_texts = {
            "uk": "❌ Будь ласка, поділіться саме своїм номером телефону.",
            "en": "❌ Please share your own phone number.",
            "ru": "❌ Пожалуйста, поделитесь именно своим номером телефона."
        }
        await message.answer(
            error_texts.get(language, error_texts["uk"]),
            reply_markup=get_phone_keyboard(language)
        )
        return

    phone = message.contact.phone_number

    # Store phone
    await state.update_data(phone=phone)

    # Ask for full name
    await state.set_state(RegistrationStates.waiting_for_name)

    name_texts = {
        "uk": "✅ Дякуємо!\n\n"
              "Тепер введіть ваше повне ім'я:",
        "en": "✅ Thank you!\n\n"
              "Now enter your full name:",
        "ru": "✅ Спасибо!\n\n"
              "Теперь введите ваше полное имя:"
    }

    await message.answer(
        name_texts.get(language, name_texts["uk"]),
        reply_markup=None  # Remove keyboard
    )


@router.message(RegistrationStates.waiting_for_name, F.text)
async def process_name(message: Message, state: FSMContext):
    """
    Handle full name
    """
    data = await state.get_data()
    language = data.get("language", "uk")

    full_name = message.text.strip()

    # Validate name (at least 2 characters)
    if len(full_name) < 2:
        error_texts = {
            "uk": "❌ Будь ласка, введіть коректне ім'я (мінімум 2 символи).",
            "en": "❌ Please enter a valid name (at least 2 characters).",
            "ru": "❌ Пожалуйста, введите корректное имя (минимум 2 символа)."
        }
        await message.answer(error_texts.get(language, error_texts["uk"]))
        return

    # Store name
    await state.update_data(full_name=full_name)

    # Ask for city
    await state.set_state(RegistrationStates.waiting_for_city)

    # Get available cities
    cities = await api_client.get_cities()

    if not cities:
        # No cities available, create user without city
        await finalize_registration(message, state, city_id=None)
        return

    city_texts = {
        "uk": "🌆 Оберіть ваше місто:",
        "en": "🌆 Select your city:",
        "ru": "🌆 Выберите ваш город:"
    }

    await message.answer(
        city_texts.get(language, city_texts["uk"]),
        reply_markup=get_cities_keyboard(cities, language)
    )


@router.callback_query(RegistrationStates.waiting_for_city, F.data.startswith("city_"))
async def process_city(callback: CallbackQuery, state: FSMContext):
    """
    Handle city selection
    """
    city_id = int(callback.data.split("_")[1])

    # Store city
    await state.update_data(city_id=city_id)

    # Finalize registration
    await finalize_registration(callback.message, state, city_id)
    await callback.answer()


async def finalize_registration(message: Message, state: FSMContext, city_id: int = None):
    """
    Finalize user registration - create user in database
    """
    data = await state.get_data()
    language = data.get("language", "uk")
    phone = data.get("phone")
    full_name = data.get("full_name")
    telegram_id = message.chat.id

    # Create user in database
    user = await api_client.create_user(
        telegram_id=telegram_id,
        phone=phone,
        full_name=full_name,
        city_id=city_id,
        language=language
    )

    if user:
        success_texts = {
            "uk": f"✅ Реєстрація успішно завершена!\n\n"
                  f"Вітаємо, {full_name}! 🎉\n\n"
                  f"Тепер ви можете замовляти піцу через наш бот.\n"
                  f"Використовуйте меню нижче для навігації.",
            "en": f"✅ Registration completed successfully!\n\n"
                  f"Welcome, {full_name}! 🎉\n\n"
                  f"Now you can order pizza through our bot.\n"
                  f"Use the menu below for navigation.",
            "ru": f"✅ Регистрация успешно завершена!\n\n"
                  f"Добро пожаловать, {full_name}! 🎉\n\n"
                  f"Теперь вы можете заказывать пиццу через наш бот.\n"
                  f"Используйте меню ниже для навигации."
        }

        await message.answer(
            success_texts.get(language, success_texts["uk"]),
            reply_markup=get_main_menu_keyboard(language)
        )

        # Clear state
        await state.clear()

        logger.info(f"User {telegram_id} registered successfully")
    else:
        error_texts = {
            "uk": "❌ Помилка при реєстрації. Спробуйте ще раз: /start",
            "en": "❌ Registration error. Please try again: /start",
            "ru": "❌ Ошибка при регистрации. Попробуйте ещё раз: /start"
        }

        await message.answer(error_texts.get(language, error_texts["uk"]))
        await state.clear()

        logger.error(f"Failed to register user {telegram_id}")
