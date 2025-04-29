from os import getenv
from enum import Enum


class ButtonTexts(Enum):

    TO_MAIN_MENU: str = '—\000в меню\000—'

    BACK: str = '—\000назад\000—'

    CANCEL: str = '—\000отмена\000—'

    CONFIRM: str = '—\000подтвердить\000—'

    APPROVE: str = '—\000одобрить\000—'

    DENY: str = '—\000отклонить\000—'

    FINISH: str = '—\000готово\000—'

    RIGHT_ARROW: str = '›\000\000›\000\000›'
    LEFT_ARROW: str = '‹\000\000‹\000\000‹'


class Texts(Enum):

    CANCEL: str = (
        '\n\n——\000/cancel для отмены\000——'
    )

    MAIN_MENU_HEADER: str = (
        '<b>▸🗿◂\000│\000Главное меню</b>'
    )

    MAIN_MENU: str = (
        f'{MAIN_MENU_HEADER}'
    )

    DEV_HEADER: str = (
        '<b>▸⚙️◂\000│\000Панель разработчика</b>'
    )

    DEV_TOOLS: str = (
        f'{DEV_HEADER}'
        '\n\n'
        f'<b>Bot version</b> — <code>{getenv("VERSION")}</code>'
    )

    IMPORT_DATABASE: str = (
        f'{DEV_HEADER}'
        '\n\n'
        'Отправьте новый файл базы данных в этот чат...'
        '\n\n'
        '<i>Примечание: файл должен быть с расширением <code>.db</code></i>'
        f'{CANCEL}'
    )

    DATABASE_SUCCESSFULLY_IMPORTED: str = (
        f'{DEV_HEADER}'
        '\n\n'
        'База данных успешно импортированна.'
    )


class InformationTexts(Enum):
    HEADER: str = 'ℹ️<b>\000\000›\000\000Информация</b>\n'

    ENTER_FIELD_CANCEL: str = (
        'ℹ️<b>\000\000›\000\000Ввод поля отменен.</b>\n'
    )

    ADDING_ADMIN_CANCEL: str = (
        'ℹ️<b>\000\000›\000\000Добавление администратора отменено.</b>\n'
    )

    ADDING_WORKHOURS_CANCEL: str = (
        'ℹ️<b>\000\000›\000\000Подача часов отменена.</b>\n'
    )

    USER_PROFILE_EDITING_CANCEL: str = (
        'ℹ️<b>\000\000›\000\000Редактирование профиля отменено.</b>\n'
    )

    USER_SEARCH_CANCEL: str = (
        'ℹ️<b>\000\000›\000\000Поиск пользователя отменен.</b>\n'
    )

    DATABASE_IMPORT_CANCEL: str = (
        'ℹ️<b>\000\000›\000\000Импорт БД отменен.</b>\n'
    )

    MESSAGES_CLEARED: str = (
        f'♻️<b>\000\000›\000\000Ненужные сообщения очищены!</b>'
    )


class ErrorTexts(Enum):
    HEADER: str = '⚠️️<b>\000\000›\000\000Ошибка</b>\n'

    EDIT_MENU_MESSAGE_CAPTION: str = (
        f'{HEADER}'
        'Пожалуйста, введите /start для начала работы бота!'
    )

    INVALID_INPUT: str = (
        f'{HEADER}'
        'Введены некорректные данные.'
    )

    WRONG_DOCUMENT_TYPE: str = (
        f'{HEADER}'
        'Неподходящее расширение файла.'
    )

    NO_FILE_ATTACHED: str = (
        f'{HEADER}'
        'Сообщение не содержит целевой файл.'
    )

    DB_FILE_IS_EMPTY: str = (
        f'{HEADER}'
        'Файл БД не содержит данных.'
    )
