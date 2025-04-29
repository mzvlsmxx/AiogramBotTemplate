from enum import Enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.stable_texts import ButtonTexts


def build_keyboard_for_enum(
        buttons: dict[str, str | dict[str, str]], *adds: InlineKeyboardButton
) -> InlineKeyboardMarkup:
    """
    Creates a keyboard with given buttons

    :param buttons: Dict of buttons
    {'label': 'callback_data', 'row_label': {'row_element_label': 'row_element_callback_data', 'row_element_label':
    'row_element_callback_data'}, ...}
    :param adds: Additional buttons that can be added to keyboard after all from given dict
    :return: An instance of InlineKeyboardMarkup with given buttons added
    """
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

    for label, callback_data in buttons.items():

        if isinstance(callback_data, dict):
            each_row_list: list[InlineKeyboardButton] = []
            for row_element_label, row_callback_data in callback_data.items():
                each_row_list.append(InlineKeyboardButton(text=row_element_label, callback_data=row_callback_data))
            keyboard.row(*each_row_list)

        else:
            keyboard.add(InlineKeyboardButton(text=label, callback_data=callback_data))

    for button in adds:
        keyboard.add(button)

    return keyboard


class Buttons(Enum):
    TEST: InlineKeyboardButton = InlineKeyboardButton(
        text='‹\000\000test\000\000›',
        callback_data='callback_test'
    )

    TO_MAIN_MENU: InlineKeyboardButton = InlineKeyboardButton(
        text=ButtonTexts.TO_MAIN_MENU.value,
        callback_data='head_back_to_main_menu'
    )

    BACK_TO_MAIN_MENU: InlineKeyboardButton = InlineKeyboardButton(
        text=ButtonTexts.BACK.value,
        callback_data='head_back_to_main_menu'
    )

    TO_ADMIN_DASHBOARD: InlineKeyboardButton = InlineKeyboardButton(
        text=ButtonTexts.TO_MAIN_MENU.value,
        callback_data='head_back_to_admin_dashboard'
    )

    BACK_TO_ADMIN_DASHBOARD: InlineKeyboardButton = InlineKeyboardButton(
        text=ButtonTexts.BACK.value,
        callback_data='head_back_to_admin_dashboard'
    )

    TO_DEV_DASHBOARD: InlineKeyboardButton = InlineKeyboardButton(
        text=ButtonTexts.TO_MAIN_MENU.value,
        callback_data='head_back_to_dev_dashboard'
    )


class Keyboards(Enum):
    MAIN_MENU: InlineKeyboardMarkup = build_keyboard_for_enum(
        {
            '‹\000\000Кнопка\000\000›': 'trash_callback'
        }
    )

    TO_MAIN_MENU: InlineKeyboardMarkup = build_keyboard_for_enum(
        {},
        Buttons.TO_MAIN_MENU.value
    )

    TO_ADMIN_DASHBOARD: InlineKeyboardMarkup = build_keyboard_for_enum(
        {},
        Buttons.TO_ADMIN_DASHBOARD.value
    )

    DEV_TOOLS: InlineKeyboardMarkup = build_keyboard_for_enum(
        {
            '‹\000\000Экспорт БД\000\000›': 'export_database',
            '‹\000\000Импорт БД\000\000›': 'import_database',
            '‹\000\000Экспорт логов\000\000›': 'export_logs',
            '‹\000\000Очистка логов\000\000›': 'clear_logs',
            ButtonTexts.TO_MAIN_MENU.value: 'head_back_to_main_menu'
        }
    )

    TO_DEV_DASHBOARD: InlineKeyboardMarkup = build_keyboard_for_enum(
        {},
        Buttons.TO_DEV_DASHBOARD.value
    )
