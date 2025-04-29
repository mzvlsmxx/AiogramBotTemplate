from aiogram import Dispatcher, types


async def answer_trash_callback(callback: types.CallbackQuery) -> None:
    """
    Answers all callback data from filler buttons

    :param callback: Callback data to proceed
    :return: None
    """
    await callback.answer()


async def delete_trash(message: types.Message) -> None:
    """
    Deleting all trash messages that does not belong to any handler

    :param message: A message to delete
    :return: None
    """
    await message.delete()


def register_handlers(dp: Dispatcher) -> None:
    """
    Registration of all handlers

    :param dp: An aiogram Dispatcher object
    :return: None
    """
    dp.register_callback_query_handler(answer_trash_callback, text='trash_callback')
    dp.register_message_handler(delete_trash, content_types=['any'])
