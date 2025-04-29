import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from aiogram import Dispatcher, types
from aiogram.types import InputMediaPhoto, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import (
    MessageToDeleteNotFound, MessageNotModified, BadRequest, MessageCantBeDeleted
)

from create import bot, database_path
from logs import actions_logger, root_logger
from utils import *
from data import *
from exceptions import *

# Temp storages
menu_message: dict[int, types.Message] = {}
incorrect_data_messages: dict[int, list[types.Message]] = {}
messages_to_clear: dict[int, list[types.Message]] = {}

# .env management
load_dotenv(find_dotenv())
developer_id: int = int(os.getenv('DEVELOPER_ID'))


async def start(message: types.Message) -> None:
    """
    Starts the bot, creates tables in DB

    :param message: A message that contains /start command from user
    :return: None
    """
    await message.delete()
    actions_logger.info('[%s] Bot started', message.from_user.id)

    create_db_file()

    messages_to_clear.update({message.from_user.id: []})
    incorrect_data_messages.update({message.from_user.id: []})

    await resend_menu_message(
        user_id=message.from_user.id,
        text=Texts.MAIN_MENU.value,
        reply_markup=Keyboards.MAIN_MENU.value
    )


# Dev options
async def open_dev_dashboard(message: types.Message) -> None:
    """
    Opens an admin dashboard

    :param message: Message sent by user with command
    :return: None
    """
    await message.delete()

    if message.from_user.id == int(os.getenv('DEVELOPER_ID')):
        await edit_menu_message_caption(
            user_id=message.from_user.id,
            text=Texts.DEV_TOOLS.value,
            reply_markup=Keyboards.DEV_TOOLS.value
        )


async def send_logs(user_id) -> None:
    """
    Sends all log file to user with given chat id

    :param user_id: Chat ID where bot should send log files to
    :return: None
    """
    log_files: list[InputFile] = []
    for file_path in get_log_paths():
        log_files.append(
            InputFile(file_path)
        )

    for log_file in log_files:
        try:
            bot_message: types.Message = await bot.send_document(chat_id=user_id, document=log_file)
            await append_message_to_clear_list(user_id=user_id, message=bot_message)
        except BadRequest as ex:
            actions_logger.warning('[%s] Log %s was not exported (%s)', user_id, log_file, ex)
    actions_logger.info('[%s] Logs were exported', user_id)


async def export_logs_command(message: types.Message) -> None:
    """
    Clear all unnecessary messages

    :param message: Message sent by user with command
    :return: None
    """
    await message.delete()
    if str(message.from_user.id) == os.getenv('DEVELOPER_ID'):
        await send_logs(message.from_user.id)


async def export_logs(callback: types.CallbackQuery) -> None:
    """
    Bot sending the .log files to the user

    :param callback: A callback data to handle
    :return: None
    """
    await callback.answer()
    await send_logs(callback.from_user.id)


async def clear_logs(callback: types.CallbackQuery) -> None:
    """
    Clear all logs

    :param callback: A callback data to handle
    :return: None
    """
    await callback.answer('Логи очищены!')
    clear_all_logs()
    actions_logger.info('[%s] Logs were cleared', callback.from_user.id)


async def export_database(callback: types.CallbackQuery) -> None:
    """
    Bot sending the .db file to the user

    :param callback: A callback data to handle
    :return: None
    """
    await callback.answer()

    try:
        database_file: InputFile = InputFile(database_path)
        bot_message_1: types.Message = await bot.send_document(chat_id=callback.from_user.id, document=database_file)
        await append_message_to_clear_list(user_id=callback.from_user.id, message=bot_message_1)

        actions_logger.info('[%s] Database was exported', callback.from_user.id)

    except BadRequest as ex:
        await send_error_message(
            user_id=callback.from_user.id,
            text=ErrorTexts.DB_FILE_IS_EMPTY.value,
            delay=5.0
        )
        actions_logger.info('[%s] Database was not exported (%s)', callback.from_user.id, ex)

    except FileNotFoundError:
        pass

    try:
        database_backup_file: InputFile = InputFile(f'{database_path.replace("database", "database_backup")}')
        bot_message_2: types.Message = await bot.send_document(
            chat_id=callback.from_user.id, document=database_backup_file
        )
        await append_message_to_clear_list(user_id=callback.from_user.id, message=bot_message_2)

    except FileNotFoundError:
        pass


class ImportDatabase(StatesGroup):
    input_file: State = State()


async def import_database(callback: types.CallbackQuery) -> None:
    """
    Bot import database from user's file

    :param callback: A callback data to handle
    :return: None
    """
    await callback.answer()
    await edit_menu_message_caption(
        user_id=callback.from_user.id, text=Texts.IMPORT_DATABASE.value
    )
    await ImportDatabase.input_file.set()


async def import_database_state(message: types.Message, state: FSMContext) -> None:
    """
    Bot import database from user's file

    :param message: Message from user with data
    :param state: Corresponding state
    :return: None
    """
    await append_message_to_incorrect_data(message)
    try:
        if message.text == '/cancel':
            raise InputCancelled

        await state.finish()

        if not message.document:
            raise NoFileAttached

        if not message.document.file_name.endswith('.db'):
            raise WrongDocumentType

        await import_new_DB(message.document)
        actions_logger.info('[%s] Database was imported', message.from_user.id)

        await edit_menu_message_caption(
            user_id=message.from_user.id, text=Texts.DATABASE_SUCCESSFULLY_IMPORTED.value,
            reply_markup=Keyboards.TO_DEV_DASHBOARD.value
        )

        await delete_messages(incorrect_data_messages.get(message.from_user.id))
        await clear_incorrect_data_dict(message.from_user.id)

    except IncorrectInputData:
        await ImportDatabase.input_file.set()
        await send_error_message(user_id=message.from_user.id, text=ErrorTexts.INVALID_INPUT.value)

    except NoFileAttached:
        await ImportDatabase.input_file.set()
        await send_error_message(user_id=message.from_user.id, text=ErrorTexts.NO_FILE_ATTACHED.value)

    except WrongDocumentType:
        await ImportDatabase.input_file.set()
        await send_error_message(user_id=message.from_user.id, text=ErrorTexts.WRONG_DOCUMENT_TYPE.value)

    except InputCancelled:
        await cancel_state(message=message, state=state)


async def head_back_to_dev_dashboard(callback: types.CallbackQuery) -> None:
    """
    Head back to dev dashboard

    :param callback: A callback data to handle
    :return: None
    """
    await callback.answer()
    await edit_menu_message_caption(
        user_id=callback.from_user.id,
        text=Texts.DEV_TOOLS.value,
        reply_markup=Keyboards.DEV_TOOLS.value
    )


async def head_back_to_main_menu(callback: types.CallbackQuery) -> None:
    """
    Head back to main menu

    :param callback: A callback data to handle
    :return: None
    """
    await callback.answer()
    await edit_menu_message_caption(
        user_id=callback.from_user.id,
        text=Texts.MAIN_MENU.value,
        reply_markup=Keyboards.MAIN_MENU.value,
        new_photo_path=MediaPaths.MAIN_MENU.value
    )


async def edit_menu_message_caption(
        *,
        user_id: int,
        text: str = Texts.MAIN_MENU.value,
        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(),
        new_photo_path: str = MediaPaths.MAIN_MENU.value
) -> None:
    """
    Edit menu message text, picture and inline keyboard

    :param user_id: Chat ID where menu message should be edited
    :param text: The new text of the menu message
    :param reply_markup: A new reply markup that will be attached to the message
    :param new_photo_path: A path to the new photo for the message
    """
    try:
        with open(f'{new_photo_path}', 'rb') as photo:
            menu_message.update(
                {
                    user_id: await menu_message.get(user_id).edit_media(
                        media=InputMediaPhoto(
                            media=photo,
                            caption=text
                        ),
                        reply_markup=reply_markup
                    )
                }
            )

    except (KeyError, AttributeError) as ex:
        root_logger.warning('[%s] Menu message can not be edited. (%s)', user_id, ex)
        await send_error_message(user_id=user_id, text=ErrorTexts.EDIT_MENU_MESSAGE_CAPTION.value, delay=7.0)

    except MessageNotModified as ex:
        root_logger.warning('[%s] Menu message was not edited. (%s)', user_id, ex)


async def resend_menu_message(
        *,
        user_id: int,
        text: str,
        reply_markup=InlineKeyboardMarkup(),
        new_photo_path: str = MediaPaths.MAIN_MENU.value
) -> None:
    """
    Resend main menu message to the user

    :param user_id: Chat ID where menu message should be resent
    :param text: The new text of the menu message
    :param reply_markup: A new reply markup that will be attached to the new message
    :param new_photo_path: A path to the new photo for the new message
    """
    try:
        await menu_message.get(user_id).delete()

    except MessageCantBeDeleted as ex:
        root_logger.warning('[%s] Menu message was not deleted. Deletion period expired. (%s)', user_id, ex)

    except (AttributeError, MessageToDeleteNotFound) as ex:
        root_logger.warning('[%s] Menu message was not found, sending brand new instead. (%s)', user_id, ex)

    with open(new_photo_path, 'rb') as menu_photo:
        menu_message.update(
            {
                user_id: await bot.send_photo(
                    chat_id=user_id, photo=menu_photo,
                    caption=text, reply_markup=reply_markup)
            }
        )


async def send_error_message(
        *, user_id: int, text: str = ErrorTexts.HEADER.value, delay: float = 2.0
) -> None:
    """
    Sends a message that contains warning. It will disappear after a while

    :param user_id: Chat id where bot should send the message
    :param text: Text of the error message
    :param delay: Time in seconds for message to be deleted
    :return: None
    """
    message: types.Message = await bot.send_message(chat_id=user_id, text=text)
    await asyncio.sleep(delay=delay)
    await message.delete()


async def cancel_state(message: types.Message, state: FSMContext) -> None:
    """
    Cancel the state of FSM

    :param message: Cancelling message that is used for getting user id
    :param state: THe state that should be cancelled
    """
    await message.delete()

    state_name: str = await state.get_state()
    state_data: list[str] = state_name.split(':')

    await state.finish()
    await delete_messages(incorrect_data_messages.get(message.from_user.id))
    await clear_incorrect_data_dict(message.from_user.id)

    match state_data:

        case 'ImportDatabase', 'input_file':
            await edit_menu_message_caption(
                user_id=message.from_user.id, text=Texts.DEV_TOOLS.value, reply_markup=Keyboards.DEV_TOOLS.value
            )
            await send_error_message(user_id=message.from_user.id, text=InformationTexts.DATABASE_IMPORT_CANCEL.value)

        case _:
            await edit_menu_message_caption(
                user_id=message.from_user.id, text=Texts.MAIN_MENU.value, reply_markup=Keyboards.MAIN_MENU.value
            )


async def append_message_to_clear_list(*, user_id: int, message: types.Message = None) -> None:
    """
    Updates the list of messages that will be cleared with certain command

    :param user_id: ID of user which chat message belongs to
    :param message: A message that should be added to messages list
    :return: None
    """
    if message:
        current_messages_to_clear: list[types.Message] = messages_to_clear.get(user_id)
        current_messages_to_clear.append(message)
        messages_to_clear.update({user_id: current_messages_to_clear})
    else:
        messages_to_clear.update({user_id: []})


async def append_message_to_incorrect_data(message: types.Message | None = None) -> None:
    """
    Updates the incorrect data messages storage for user

    :param message: A message that should be added to incorrect messages list
    :return: None
    """
    try:
        if incorrect_data_messages.get(message.from_user.id):
            new_incorrect_data_list: list[types.Message] = incorrect_data_messages.get(message.from_user.id)
            new_incorrect_data_list.append(message)
            incorrect_data_messages.update({message.from_user.id: new_incorrect_data_list})
        else:
            incorrect_data_messages.update({message.from_user.id: [message]})
    except AttributeError:
        pass


async def clear_incorrect_data_dict(user_id: int) -> None:
    """
    Updates the incorrect data messages storage for user

    :param user_id: Telegram ID of the target user
    :return: None
    """
    incorrect_data_messages.update({user_id: []})


async def show_user_id(message: types.Message) -> None:
    """
    Show user's telegram ID

    :param message: Message sent by user with command
    :return: None
    """
    await message.delete()
    bot_message: types.Message = await message.answer(text=f'Ваш id: <code>{message.from_user.id}</code>')
    await append_message_to_clear_list(
        user_id=message.from_user.id, message=bot_message
    )


async def delete_incorrect_data_messages(user_id: int) -> None:
    """
    Deletion of all messages containing incorrect data from user

    :param user_id: ID of user which incorrect messages should be deleted
    :return: None
    """
    try:
        for message in incorrect_data_messages.get(user_id):
            await message.delete()
        incorrect_data_messages.update({user_id: []})

    except (MessageToDeleteNotFound, TypeError):
        pass


async def clear_trash_messages(message: types.Message) -> None:
    """
    Clear all unnecessary messages

    :param message: Message sent by user with command
    :return: None
    """
    await message.delete()
    try:
        await delete_messages(messages_to_clear.get(message.from_user.id))
        await append_message_to_clear_list(user_id=message.from_user.id)
    except KeyError:
        pass
    await send_error_message(user_id=message.from_user.id, text=InformationTexts.MESSAGES_CLEARED.value)


def register_handlers(dp: Dispatcher) -> None:
    """
    Registration of all handlers

    :param dp: An aiogram Dispatcher object
    :return: None
    """
    # Start command
    dp.register_message_handler(start, commands=['start'])

    # Back to menus
    dp.register_callback_query_handler(head_back_to_main_menu, text='head_back_to_main_menu')
    dp.register_callback_query_handler(head_back_to_dev_dashboard, text='head_back_to_dev_dashboard')

    # Dev options
    dp.register_message_handler(open_dev_dashboard, commands=['dev'])
    dp.register_callback_query_handler(export_database, text='export_database')
    dp.register_callback_query_handler(import_database, text='import_database')
    dp.register_message_handler(
        import_database_state, state=ImportDatabase.input_file, content_types=['text', 'document']
    )
    dp.register_callback_query_handler(export_logs, text='export_logs')
    dp.register_message_handler(export_logs_command, commands=['export_logs'])
    dp.register_callback_query_handler(clear_logs, text='clear_logs')

    # Miscellaneous
    dp.register_message_handler(show_user_id, commands=['id'])
    dp.register_message_handler(clear_trash_messages, commands=['clear'])
