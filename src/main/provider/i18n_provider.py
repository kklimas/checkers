from src.main.config.config import *


class I18NProvider(I18NConfig):
    def __init__(self, locale):
        I18NConfig.__init__(self, locale)
        self.change_locale(self.locale)

    @staticmethod
    def get(key):
        return i.t(key)

    def change_locale(self, locale):
        if locale not in self.locales:
            raise NameError
        self.set_locale(locale)
