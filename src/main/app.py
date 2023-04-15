import pygame

from src.main.engine.game_engine import GameEngine
from src.main.enum.app_state import AppState
from src.main.model.game_mode import GameMode
from src.main.provider.button_provider import ButtonProvider
from src.resources.constants import WIDTH, HEIGHT, FPS, SQUARE_SIZE


class App:
    def __init__(self):
        self._init()

    def _init(self):
        self.app_state = AppState.MENU
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Main Menu")
        self.button_provider = ButtonProvider()
        self.game = None
        self.game_mode = GameMode()
        self.run = False
        self._run()

    def _run(self):

        self.run = True
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(FPS)
            self.screen.fill((52, 78, 91))

            match self.app_state:
                case AppState.MENU:
                    if self.button_provider.resume_button.draw(self.screen):
                        self.game = GameEngine(self.screen, self.game_mode)
                        self.app_state = AppState.GAME

                    if self.button_provider.settings_button.draw(self.screen):
                        self.app_state = AppState.SETTINGS

                    if self.button_provider.quit_button.draw(self.screen):
                        self.app_state = AppState.QUIT
                case AppState.GAME:
                    self.game.update()
                    if self.game.winner() is not None:
                        # todo handle data storage about the result of game
                        print(self.game.winner())
                        self.app_state = AppState.MENU

                case AppState.SETTINGS:
                    # todo display settings panel
                    pass

            self._handle_events()

            pygame.display.update()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or AppState.QUIT == self.app_state:
                self.run = False
            if AppState.GAME == self.app_state and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                self.game.select(row, col)

    def _set_title(self, title):
        pygame.display.set_caption(title)

    def _draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
