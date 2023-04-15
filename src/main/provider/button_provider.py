import pygame.image

from src.main.model.menu_button import MenuButton
from src.resources.constants import RESUME_IMG_PATH, SETTINGS_IMG_PATH, QUIT_IMG_PATH


class ButtonProvider:
    def __init__(self):
        self._init_buttons()

    def _init_buttons(self):
        resume_img = pygame.image.load(RESUME_IMG_PATH).convert_alpha()
        self.resume_button = MenuButton(304, 125, resume_img, 1)

        settings_img = pygame.image.load(SETTINGS_IMG_PATH).convert_alpha()
        self.settings_button = MenuButton(297, 250, settings_img, 1)

        quit_img = pygame.image.load(QUIT_IMG_PATH).convert_alpha()
        self.quit_button = MenuButton(336, 375, quit_img, 1)
