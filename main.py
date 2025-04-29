from aiogram import executor


if __name__ == '__main__':
    from handlers import handlers, debug_handlers, cleanup_handlers
    from create import dp

    handlers.register_handlers(dp)
    debug_handlers.register_handlers(dp)
    cleanup_handlers.register_handlers(dp)

    executor.start_polling(dp, skip_updates=True, timeout=1_000_000)
