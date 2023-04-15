from enum import Enum


class GameLang(Enum):
    ENGLISH = 0
    POLISH = 1

    def stringify(self):
        match self.value:
            case 0:
                return 'EN'
            case 1:
                return 'PL'

    @staticmethod
    def serialize(value):
        match value:
            case 'EN':
                return GameLang.ENGLISH
            case 'PL':
                return GameLang.POLISH
