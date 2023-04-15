from enum import Enum


class GameTheme(Enum):
    DARK = 0
    LIGHT = 1

    def stringify(self):
        match self.value:
            case 0:
                return 'Dark'
            case 1:
                return 'Light'

    @staticmethod
    def serialize(value):
        match value:
            case 'Dark':
                return GameTheme.DARK
            case 'Light':
                return GameTheme.LIGHT
