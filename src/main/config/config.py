from os import getenv

import i18n as i
from dotenv import load_dotenv

TRANSLATION_CONTEXT_PATH = 'TRANSLATION_CONTEXT_PATH'
TRANSLATION_LOCALE = 'TRANSLATION_LOCALE'
TRANSLATION_LOCALES = 'TRANSLATION_LOCALES'


class AppConfig:
    def __init__(self):
        load_dotenv()
        self.i18n_context_path = getenv(TRANSLATION_CONTEXT_PATH)
        self.locale = getenv(TRANSLATION_LOCALE)
        self.locales = getenv(TRANSLATION_LOCALES).split(",")


class I18NConfig(AppConfig):
    def __init__(self):
        AppConfig.__init__(self)
        i.load_path.append(self.i18n_context_path)

    def set_locale(self, locale):
        self.locale = locale
        i.set('locale', self.locale)
