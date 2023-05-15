from enum import Enum


class AppState(Enum):
    MENU = 1
    PRE_GAME = 2
    GAME = 3
    BOT_GAME = 4
    AFTER_GAME = 5
    SETTINGS = 6
    QUIT = 7
