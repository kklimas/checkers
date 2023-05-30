from src.main.enum.difficulty_level import DifficultyLevel
from src.main.enum.opponent_type import OpponentType
from src.main.enum.setting_type import SettingType
from src.main.enum.time_option import TimeOption
from src.main.model.drop_down import DropDown
from src.resources.constants import WHITE, FONT_TITLE, FONT, WIDTH


class PreGameView:
    def __init__(self, window, game_mode, i18n_provider):
        self.i18n = i18n_provider
        self.window = window
        self.game_mode = game_mode
        self.font_title = FONT_TITLE
        self.font = FONT
        self._setup_dropdowns()

    def _setup_dropdowns(self):
        self.dropdowns = [
            DropDown(117, 160, bool_stringify(self.game_mode.king_multiple_moves), given_booleans(),
                     SettingType.KING_MOVE),
            DropDown(450, 160, bool_stringify(self.game_mode.obligatory_best_beat), given_booleans(), SettingType.OBL_BEAT),
            DropDown(784, 160, bool_stringify(self.game_mode.reverse_beat), given_booleans(), SettingType.REV_BEAT),
            DropDown(117, 360, self.game_mode.opponent.value, [op.value for op in OpponentType],
                     SettingType.OPPONENT),
            DropDown(450, 360, self.game_mode.difficulty.value[0], [d.value[0] for d in DifficultyLevel],
                     SettingType.DIFFICULTY),
            DropDown(784, 360, str(self.game_mode.time.value), [str(t.value) for t in TimeOption], SettingType.TIME),
        ]

    def draw(self):
        self._draw_labels()
        for dropdown in self.dropdowns:
            dropdown.draw(self.window)

    def _draw_labels(self):
        # game mode
        self.center(0, WIDTH, 20, 'game.title', True)
        self.center(120, 220, 120, 'game.king_move')
        self.center(450, 550, 120, 'game.obligatory_beat')
        self.center(790, 890, 120, 'game.reverse_beat')
        self.center(120, 220, 320, 'game.opponent.title')
        self.center(450, 550, 320, 'game.opponent.difficulty.title')
        self.center(790, 890, 320, 'game.time.title')

    def center(self, x1, x2, y, key, title_font=False):
        label, font = self._get_label(key, title_font)
        text_width, _ = font.size(self._get(key))
        block_width = x2 - x1

        if text_width < block_width:
            x1 = (block_width - text_width) // 2 + x1
        else:
            x1 -= (text_width - block_width) // 2
        self.window.blit(label, (x1, y))

    def _get_label(self, key, title_font=True):
        if title_font:
            return self.font_title.render(self._get(key), 1, WHITE), self.font_title
        return self.font.render(self._get(key), 1, WHITE), self.font

    def _get(self, key):
        return self.i18n.get('app.settings.' + key)


def bool_stringify(boolean):
    if boolean:
        return 'True'
    return 'False'


def given_booleans():
    return ['True', 'False']
