from enum import Enum


date_format: str = '%Y-%m-%d'


class MediaPaths(Enum):
    MAIN_MENU: str = 'data/media/albanec.jpg'


class Privilege(Enum):
    DEVELOPER: str = 'developer'
    ADMIN: str = 'admin'
    USER: str = 'user'
