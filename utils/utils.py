import os

import aiogram.utils.exceptions
from aiogram.types import Document, InlineKeyboardMarkup, InlineKeyboardButton

from create import database_path


def create_db_file() -> None:
    """
    Creates a database file
    """
    if not os.path.isfile(database_path):
        with open(database_path, 'w'):
            pass


async def build_keyboard(
        buttons: dict[str, str | dict[str, str]], *,
        base_keyboard: InlineKeyboardMarkup | None = None,
        additional_buttons: list[InlineKeyboardButton] | None = None
) -> InlineKeyboardMarkup:
    """
    Create a keyboard to attach to message

    :param buttons: The dict[str: str | CallbackData] of buttons to add
    :param base_keyboard: The base keyboard which will be extended with given buttons
    :param additional_buttons: The additional buttons (InlineKeyboardButton) to add
    :return: InlineKeyboardMarkup object with built keyboard
    """
    if base_keyboard:
        keyboard: InlineKeyboardMarkup = base_keyboard
    else:
        keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()

    for label, callback_data in buttons.items():

        if isinstance(callback_data, dict):
            rowList: list[InlineKeyboardButton] = []

            for row_label, row_callback_data in callback_data.items():
                rowList.append(InlineKeyboardButton(text=row_label, callback_data=row_callback_data))
            keyboard.row(*rowList)

        else:
            keyboard.add(
                InlineKeyboardButton(text=label, callback_data=callback_data)
            )

    if additional_buttons:
        for button in additional_buttons:
            keyboard.add(button)

    return keyboard


async def delete_messages(list_of_messages: list[aiogram.types.Message] | None) -> None:
    """
    Deletes all messages from given list

    :param list_of_messages: List of messages that should be deleted
    """
    try:
        if list_of_messages:
            for message in list_of_messages:
                await message.delete()
    except (aiogram.utils.exceptions.MessageToDeleteNotFound, TypeError):
        pass


def get_log_paths() -> list[str]:
    """
    Get all log paths from log folder

    :return: List of file paths of every log file
    """
    filePaths: list[str] = [f'logs/{file}' for file in os.listdir('logs') if os.path.isfile(os.path.join('logs', file))]

    filePaths.remove('logs/__init__.py')
    filePaths.remove('logs/logger.py')

    return filePaths


def clear_all_logs() -> None:
    """
    Clear all logs in logs directory, replaces the files with empty ones
    """
    file_paths: list[str] = get_log_paths()

    for fileName in file_paths:
        with open(f'{fileName}', 'w'):
            pass


async def import_new_DB(file: Document) -> None:
    """
    Replaces old .db file with new from file param

    :param file: A file that is attached to message the current database should be replaced with
    :return: None
    """
    try:
        os.remove('data/database_backup.db')
    except FileNotFoundError:
        pass
    os.rename('data/database.db', 'data/database_backup.db')
    await file.download(destination_file='data/database.db')


async def delete_file(path: str) -> None:
    """
    Deletes xls file

    :param path: File path
    :return: None
    """
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
