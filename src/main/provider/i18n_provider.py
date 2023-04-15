from src.main.config.config import *


class I18NProvider(I18NConfig):
    def __init__(self):
        I18NConfig.__init__(self)

    @staticmethod
    def get(key):
        return i.t(key)

    def change_locale(self, locale):
        if locale not in self.locales:
            raise NameError
        self.set_locale(locale)
