import random
import time

import i18n
import pygame

from src.main.enum.app_state import AppState
from src.main.enum.difficulty_level import DifficultyLevel
from src.main.enum.game_lang import GameLang
from src.main.enum.game_theme import GameTheme
from src.main.enum.opponent_type import OpponentType
from src.main.enum.setting_type import SettingType
from src.main.enum.time_option import TimeOption
from src.main.model.bot import Bot
from src.main.model.bot2 import Bot2
from src.main.model.button import Button
from src.main.model.game_mode import GameMode
from src.main.model.player import Player
from src.main.model.statistics import Statistics
from src.main.provider.button_provider import ButtonProvider
from src.main.provider.i18n_provider import I18NProvider
from src.main.util.time_prettier import TimePrettier
from src.main.view.game_view import GameView
from src.main.view.pre_game_view import PreGameView
from src.main.view.settings_view import SettingsView
from src.resources.constants import WIDTH, HEIGHT, FPS, SQUARE_SIZE, LIGHT_THEME, DARK_THEME, BLACK, WHITE, FONT, ROWS, \
    COLS, CLOCK_COUNTER_TICK


class App:
    def __init__(self):
        self._init()

    def _init(self):
        self.app_state = AppState.MENU
        self.i18n = I18NProvider()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(self.i18n.get('app.title'))
        self.button_provider = ButtonProvider(self.i18n)
        self.game_mode = GameMode()
        self._update_theme()
        self.game = None
        self.settings = None
        self.pregame = None
        self.run = False
        self.time_winner = None
        self.bot = None
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
                    self.button_provider = ButtonProvider(self.i18n)
                    if self.button_provider.resume_button.draw(self.screen):
                        self.app_state = AppState.PRE_GAME
                        self.pregame = PreGameView(self.screen, self.game_mode, self.i18n)

                    if self.button_provider.settings_button.draw(self.screen):
                        self.app_state = AppState.SETTINGS
                        self.settings = SettingsView(self.screen, self.game_mode, self.i18n)

                    if self.button_provider.quit_button.draw(self.screen):
                        self.app_state = AppState.QUIT

                case AppState.PRE_GAME:
                    self._handle_pregame_refresh(event_list)

                case AppState.GAME:
                    self.game.update()

                    if self.time_winner is not None or self.game.winner() is not None:
                        self.app_state = AppState.AFTER_GAME
                        statistics = Statistics()
                        if self.time_winner == WHITE or self.game.winner() == WHITE:
                            statistics.save_result(self.game_mode.first_player.username, "Wygrana")
                            statistics.save_result(self.game_mode.second_player.username, "Przegrana")
                        else:
                            statistics.save_result(self.game_mode.first_player.username, "Przegrana")
                            statistics.save_result(self.game_mode.second_player.username, "Wygrana")

                    self._check_if_time_end()
                    self._handle_in_game_panel()

                case AppState.BOT_GAME:
                    self.game.update()
                    if self.game.winner() is not None:
                        self.app_state = AppState.AFTER_GAME
                        statistics = Statistics()
                        if self.time_winner == BLACK or self.game.winner() == BLACK:
                            statistics.save_result(self.game_mode.first_player.username, "Wygrana",
                                                   self.game_mode.difficulty.value[0])
                        else:
                            statistics.save_result(self.game_mode.first_player.username, "Przegrana",
                                                   self.game_mode.difficulty.value[0])

                    if self.game.turn == BLACK:
                        self.game.update()
                        pygame.display.flip()

                        # bot = Bot(self.game_mode)
                        # (bot_start_position, bot_move) = bot.find_best_move(self.game.board.board)
                        bot = Bot2(self.game.board.board, self.game_mode)
                        (bot_start_position, bot_move) = bot.make_best_move(self.game.board.board,
                                                                            self.game_mode.difficulty.value[1])

                        time.sleep(random.randint(8, 12) / 10)
                        self.game.select(bot_start_position[0], bot_start_position[1])
                        self.game.update()
                        pygame.display.flip()
                        time.sleep(random.randint(8, 12) / 10)
                        # self.game.select(bot_move[0][0], bot_move[0][1])
                        self.game.select(bot_move[0], bot_move[1])

                    self._draw_back_button()

                case AppState.AFTER_GAME:
                    label = ' ' + self.i18n.get('app.settings.game.won')
                    self._center(0, WIDTH, 100, self._extract_winner() + label)
                    self._handle_buttons(False)
                case AppState.SETTINGS:
                    self._handle_settings_refresh(event_list)

            self._handle_events(event_list)

            pygame.display.flip()

        pygame.quit()

    def _check_if_time_end(self):
        first_player_time = self.game_mode.first_player.current_time
        second_player_time = self.game_mode.second_player.current_time
        if first_player_time <= 0:
            self.time_winner = BLACK
            return
        if second_player_time <= 0:
            self.time_winner = WHITE

    def _extract_winner(self):
        if self._did_white_win():
            return self.game_mode.first_player.username
        return self.game_mode.second_player.username

    def _did_white_win(self):
        w1 = self.game.winner()
        if w1 is not None:
            return w1 == WHITE
        return self.time_winner == WHITE

    def _handle_events(self, event_list):
        for event in event_list:
            if AppState.MENU != self.app_state and event.type == pygame.QUIT:
                self.app_state = AppState.MENU

            elif AppState.QUIT == self.app_state or (event.type == pygame.QUIT and AppState.MENU == self.app_state):
                self.run = False

            if AppState.GAME == self.app_state and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if row < ROWS and col < COLS:
                    self.game.select(row, col)

            if AppState.BOT_GAME == self.app_state and self.game.turn == WHITE and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if row < ROWS and col < COLS:
                    self.game.select(row, col)

            if self._in_game():
                self._subtract_time()

    def _in_game(self):
        return AppState.BOT_GAME == self.app_state or AppState.GAME == self.app_state

    def _subtract_time(self):
        if self.game.turn == WHITE:
            self.game_mode.first_player.current_time -= CLOCK_COUNTER_TICK
            return
        self.game_mode.second_player.current_time -= CLOCK_COUNTER_TICK

    def _update_theme(self):
        if self.game_mode.theme == GameTheme.DARK:
            self.theme = DARK_THEME
        else:
            self.theme = LIGHT_THEME

    def _handle_pregame_refresh(self, event_list):
        for dropdown in self.pregame.dropdowns:
            selected = dropdown.update(event_list)
            if selected >= 0:
                dropdown.main = dropdown.options[selected]
                allow_mode = dropdown.main == 'True'
                match dropdown.type:
                    case SettingType.OBL_BEAT:
                        self.game_mode.obligatory_beat = allow_mode
                    case SettingType.REV_BEAT:
                        self.game_mode.reverse_beat = allow_mode
                    case SettingType.KING_MOVE:
                        self.game_mode.king_multiple_moves = allow_mode
                    case SettingType.OPPONENT:
                        self.game_mode.opponent = OpponentType.from_string(dropdown.main)
                    case SettingType.DIFFICULTY:
                        self.game_mode.difficulty = DifficultyLevel.from_string(dropdown.main)
                    case SettingType.TIME:
                        self.game_mode.time = TimeOption.from_string(dropdown.main)

        self._handle_buttons()
        self.pregame.draw()

    def _handle_in_game_panel(self):
        self._center(800, 1000, 270, self._from_millis())
        self._center(800, 1000, 300, self.game_mode.first_player.username)
        self._center(800, 1000, 350, 'vs')
        self._center(800, 1000, 400, self.game_mode.second_player.username)
        self._center(800, 1000, 430, self._from_millis(False))
        self._draw_back_button()

    def _draw_back_button(self):
        back_button = Button(850, 700, self.i18n.get('app.menu.back'), FONT, 20)
        if back_button.draw(self.screen):
            self.app_state = AppState.MENU
            self.game = None
            self.game_mode = GameMode()

    def _from_millis(self, is_first_player=True):
        millis = self.game_mode.first_player.current_time \
            if is_first_player \
            else self.game_mode.second_player.current_time
        return TimePrettier.prettify_millis(millis)

    def _handle_buttons(self, is_pre_game_view=True):
        back_button = Button(120, 600, self.i18n.get('app.menu.back'), FONT, 20)
        play_button = Button(780, 600, self.i18n.get('app.menu.play'), FONT, 20)
        if back_button.draw(self.screen):
            self.app_state = AppState.MENU
            self.time_winner = None
            self.game = None
        if is_pre_game_view and play_button.draw(self.screen):
            max_time_millis = self.game_mode.time.value * 60 * 1000

            # todo add place to write username
            self.game_mode.second_player = Player('player 2', max_time_millis)
            if self.game_mode.opponent == OpponentType.HUMAN:
                self.game_mode.first_player = Player('player 1', max_time_millis)
                self.app_state = AppState.GAME
            else:
                self.game_mode.first_player = Player('Computer', max_time_millis)
                self.app_state = AppState.BOT_GAME
                self.bot = Bot(self.game_mode)
            # event to tick every 100ms and subtract value from current player time
            pygame.time.set_timer(pygame.USEREVENT, CLOCK_COUNTER_TICK)
            self.game = GameView(self.screen, self.game_mode)

    def _center(self, x1, x2, y, key):
        label, font = self._get_label(key)
        text_width, _ = font.size(self.i18n.get(key))
        block_width = x2 - x1

        if text_width < block_width:
            x1 = (block_width - text_width) // 2 + x1
        else:
            x1 -= (text_width - block_width) // 2
        self.screen.blit(label, (x1, y))

    def _get_label(self, key):
        return FONT.render(self.i18n.get(key), 1, WHITE), FONT

    def _handle_settings_refresh(self, event_list):
        for dropdown in self.settings.dropdowns:
            selected = dropdown.update(event_list)
            if selected >= 0:
                dropdown.main = dropdown.options[selected]
                match dropdown.type:
                    case SettingType.LANG:
                        self.game_mode.language = GameLang.serialize(dropdown.main)
                        self.i18n.change_locale(dropdown.main.lower())
                    case SettingType.THEME:
                        self.game_mode.theme = GameTheme.serialize(dropdown.main)
                        self._update_theme()

        self._handle_buttons(False)
        self.settings.draw()


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
