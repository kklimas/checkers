from enum import Enum


class AppState(Enum):
    MENU = 0
    GAME = 2,
    SETTINGS = 3,
    QUIT = 4,
    BOT_GAME = 5