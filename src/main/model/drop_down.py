import pygame as pg

from src.resources.constants import FONT, COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_ACTIVE, COLOR_LIST_INACTIVE, BLACK


class DropDown:
    def __init__(self, x, y, main, options, setting_type):
        self.color_menu = [COLOR_INACTIVE, COLOR_ACTIVE]
        self.color_option = [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE]
        self.rect = pg.Rect(x, y, 120, 50)
        self.font = FONT
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.type = setting_type

    def draw(self, surf):
        pg.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, BLACK)
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pg.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, BLACK)
                surf.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mouse_position = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mouse_position)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mouse_position):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1
