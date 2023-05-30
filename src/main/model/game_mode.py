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
        self.obligatory_best_beat = obligatory_beat
        self.king_multiple_moves = king_multiple_moves
        self.opponent = opponent
        self.difficulty = difficulty
        self.time = time
        self.first_player = first_player
        self.second_player = second_player

    def to_dict(self):
        result = self.__dict__
        result['theme'] = self.theme.stringify()
        result['language'] = self.language.stringify()
        result['opponent'] = self.opponent.value
        result['difficulty'] = self.difficulty.value[0]
        result['time'] = self.time.stringify()
        self.__handle_players(result)
        return result

    def __handle_players(self, result):
        if type(self.first_player) is not str:
            result['first_player'] = self.first_player.username
        if type(self.second_player) is not str:
            result['second_player'] = self.second_player.username

    @staticmethod
    def from_dict(config):
        mode = GameMode()
        mode.first_player = config.get('first_player')
        mode.second_player = config.get('second_player')
        mode.theme = GameTheme.serialize(config.get('theme'))
        mode.language = GameLang.serialize(config.get('language'))
        mode.king_multiple_moves = config.get('king_multiple_moves')
        mode.obligatory_best_beat = config.get('obligatory_best_beat')
        mode.reverse_beat = config.get('reverse_beat')
        mode.king_multiple_moves = config.get('king_multiple_moves')
        mode.opponent = OpponentType.HUMAN.from_string(config.get('opponent'))
        mode.difficulty = DifficultyLevel.from_string(config.get('difficulty'))
        mode.time = TimeOption.from_string(config.get('time'))
        return mode


def stringify_bool(value):
    return str(value).lower()
