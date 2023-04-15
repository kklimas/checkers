import pygame

from src.resources.constants import FONT_TITLE, BLACK, WHITE


class Button:
    def __init__(self, x, y, text):
        self.text = text
        self.font = FONT_TITLE
        self.text_size = self.font.size(text)
        self.rect = pygame.Rect(x, y, self.text_size[0] + 50, self.text_size[1] + 50)
        self.clicked = False

    def _draw_text(self, surface):
        label = self.font.render(self.text, 1, WHITE)
        surface.blit(label, (self.rect.x + 25, self.rect.y + 25))

    def _draw_rect(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, 3)

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        self._draw_rect(surface)
        self._draw_text(surface)

        return action
