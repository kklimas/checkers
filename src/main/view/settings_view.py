from src.main.enum.game_lang import GameLang
from src.main.enum.game_theme import GameTheme
from src.main.enum.setting_type import SettingType
from src.main.model.drop_down import DropDown
from src.resources.constants import WHITE, FONT_TITLE, FONT, WIDTH


class SettingsView:
    def __init__(self, window, game_mode, i18n_provider):
        self.i18n = i18n_provider
        self.window = window
        self.game_mode = game_mode
        self.font_title = FONT_TITLE
        self.font = FONT
        self._setup_dropdowns()

    def _setup_dropdowns(self):
        langs = [e.stringify() for e in GameLang]
        current_lang = langs[self.game_mode.language.value]

        themes = [t.stringify() for t in GameTheme]
        current_theme = themes[self.game_mode.theme.value]

        self.dropdowns = [
            DropDown(350, 130, current_lang, langs, SettingType.LANG),
            DropDown(550, 130, current_theme, themes, SettingType.THEME),
        ]

    def draw(self):
        self._draw_labels()
        for dropdown in self.dropdowns:
            dropdown.draw(self.window)

    def _draw_labels(self):
        # app settings
        self._center(0, WIDTH, 10, 'app.title', True)
        self._center(350, 450, 90, 'app.language')
        self._center(550, 650, 90, 'app.theme')

    def _center(self, x1, x2, y, key, title_font=False):
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
