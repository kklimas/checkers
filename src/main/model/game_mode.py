from src.main.enum.game_lang import GameLang
from src.main.enum.game_theme import GameTheme


class GameMode:
    def __init__(self, king_multiple_moves=True, obligatory_beat=False, reverse_beat=False, theme=GameTheme.DARK,
                 lang=GameLang.ENGLISH):
        self.king_multiple_moves = king_multiple_moves
        self.obligatory_beat = obligatory_beat
        self.reverse_beat = reverse_beat
        self.theme = theme
        self.language = lang
