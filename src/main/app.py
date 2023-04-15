import pygame
import i18n as i
from src.main.enum.app_state import AppState
from src.main.enum.game_lang import GameLang
from src.main.enum.game_theme import GameTheme
from src.main.enum.setting_type import SettingType
from src.main.model.game_mode import GameMode
from src.main.provider.button_provider import ButtonProvider
from src.main.provider.i18n_provider import I18NProvider
from src.main.view.game_view import GameView
from src.main.view.settings_view import SettingsView
from src.resources.constants import WIDTH, HEIGHT, FPS, SQUARE_SIZE, LIGHT_THEME, DARK_THEME


class App:
    def __init__(self):
        self._init()

    def _init(self):
        self.app_state = AppState.MENU
        self.i18n = I18NProvider()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(self.i18n.get('app.title'))
        self.button_provider = ButtonProvider()
        self.game_mode = GameMode()
        self._update_theme()
        self.game = None
        self.settings = None
        self.run = False
        self._run()

    def _run(self):

        self.run = True
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(FPS)
            self.screen.fill(self.theme.get('background'))
            event_list = pygame.event.get()
            match self.app_state:
                case AppState.MENU:
                    if self.button_provider.resume_button.draw(self.screen):
                        self.game = GameView(self.screen, self.game_mode)
                        self.app_state = AppState.GAME

                    if self.button_provider.settings_button.draw(self.screen):
                        self.app_state = AppState.SETTINGS
                        self.settings = SettingsView(self.screen, self.game_mode, self.i18n)

                    if self.button_provider.quit_button.draw(self.screen):
                        self.app_state = AppState.QUIT
                case AppState.GAME:
                    self.game.update()
                    if self.game.winner() is not None:
                        # todo handle data storage about the result of game
                        print(self.game.winner())
                        self.app_state = AppState.MENU

                case AppState.SETTINGS:
                    self._handle_settings_refresh(event_list)

            self._handle_events(event_list)

            pygame.display.flip()

        pygame.quit()

    def _handle_events(self, event_list):
        for event in event_list:
            if AppState.MENU != self.app_state and event.type == pygame.QUIT:
                self.app_state = AppState.MENU

            elif AppState.QUIT == self.app_state or (event.type == pygame.QUIT and AppState.MENU == self.app_state):
                self.run = False

            if AppState.GAME == self.app_state and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                self.game.select(row, col)

    def _update_theme(self):
        if self.game_mode.theme == GameTheme.DARK:
            self.theme = DARK_THEME
        else:
            self.theme = LIGHT_THEME

    def _handle_settings_refresh(self, event_list):
        for dropdown in self.settings.dropdowns:
            selected = dropdown.update(event_list)
            if selected >= 0:
                dropdown.main = dropdown.options[selected]
                allow_mode = dropdown.main == 'True'
                match dropdown.type:
                    case SettingType.LANG:
                        self.game_mode.language = GameLang.serialize(dropdown.main)
                        self.i18n.change_locale(dropdown.main.lower())
                    case SettingType.THEME:
                        self.game_mode.theme = GameTheme.serialize(dropdown.main)
                        self._update_theme()
                    case SettingType.OBL_BEAT:
                        self.game_mode.obligatory_beat = allow_mode
                    case SettingType.REV_BEAT:
                        self.game_mode.reverse_beat = allow_mode
                    case SettingType.KING_MOVE:
                        self.game_mode.king_multiple_moves = allow_mode

        self.settings.draw()

    def _draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
