"""
FSM States for user registration and other flows
"""

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for user registration process"""
    waiting_for_phone = State()
    waiting_for_name = State()
    waiting_for_city = State()


class OrderStates(StatesGroup):
    """States for order process"""
    waiting_for_receipt = State()
    confirming_cancel = State()


class SupportStates(StatesGroup):
    """States for support/feedback process"""
    waiting_for_message = State()
    waiting_for_order_number = State()
    in_conversation = State()


class SettingsStates(StatesGroup):
    """States for settings changes"""
    changing_language = State()
    changing_city = State()
    changing_name = State()
