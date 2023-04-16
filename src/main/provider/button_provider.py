from src.main.model.button import Button
from src.resources.constants import FONT_TITLE, WIDTH


class ButtonProvider:
    def __init__(self, i18n):
        self.i18n = i18n
        self._init_buttons()

    def _init_buttons(self):
        resume_text = self.i18n.get('app.menu.play')
        self.resume_button = Button(self._center_x(resume_text), 125, resume_text)

        setting_text = self.i18n.get('app.menu.options')
        self.settings_button = Button(self._center_x(setting_text), 270, setting_text)

        quit_text = self.i18n.get('app.menu.quit')
        self.quit_button = Button(self._center_x(quit_text), 405, quit_text)

    def _center_x(self, text):
        text = self.i18n.get(text)
        text_size = FONT_TITLE.size(text)
        return (WIDTH - text_size[0]) // 2

