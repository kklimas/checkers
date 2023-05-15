from src.main.enum.difficulty_level import DifficultyLevel
from src.main.enum.game_lang import GameLang
from src.main.enum.game_theme import GameTheme
from src.main.enum.opponent_type import OpponentType
from src.main.enum.time_option import TimeOption


class GameMode:
    def __init__(self, king_multiple_moves=True, obligatory_beat=False, reverse_beat=False, theme=GameTheme.DARK,
                 lang=GameLang.ENGLISH, opponent=OpponentType.HUMAN, difficulty=DifficultyLevel.EASY,
                 time=TimeOption.FIVE, first_player=None, second_player=None):
        self.theme = theme
        self.language = lang
        self.reverse_beat = reverse_beat
        self.obligatory_beat = obligatory_beat
        self.king_multiple_moves = king_multiple_moves
        self.opponent = opponent
        self.difficulty = difficulty
        self.time = time
        self.first_player = first_player
        self.second_player = second_player
