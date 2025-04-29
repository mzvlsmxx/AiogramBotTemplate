from aiogram import Dispatcher, types


async def testing(message: types.Message) -> None:
    """
    A debug function to test functional

    :param message: /test command
    :return: None
    """
    await message.delete()


async def callback_testing(callback: types.CallbackQuery) -> None:
    """
    A debug function to test functional

    :param callback: A callback data
    :return: None
    """
    await callback.answer('Test')


def register_handlers(dp: Dispatcher) -> None:
    """
    Registration of all handlers

    :param dp: An aiogram Dispatcher object
    :return: None
    """

    # Debug
    dp.register_callback_query_handler(callback_testing, text='callback_test')
    dp.register_message_handler(testing, commands=['test'])
