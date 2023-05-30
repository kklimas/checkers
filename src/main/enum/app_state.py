from enum import Enum


class AppState(Enum):
    MENU = 1
    PRE_GAME = 2
    HISTORY = 3,
    GAME = 4
    BOT_GAME = 5
    AFTER_GAME = 6
    SETTINGS = 7
    QUIT = 8
