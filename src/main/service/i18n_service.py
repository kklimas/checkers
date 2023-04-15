from src.main.config.config import *


class I18NService(I18NConfig):
    def __init__(self):
        I18NConfig.__init__(self)

    def get(self, key):
        return i.t(key)

    def change_locale(self, locale):
        if locale not in self.locales:
            raise NameError
        self.locale = locale
        i.set('locale', self.locale)
