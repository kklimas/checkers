from enum import Enum


class TimeOption(Enum):
    TENTH = 0.1
    HALF = 0.5
    ONE = 1
    THREE = 3
    FIVE = 5

    @staticmethod
    def from_string(value):
        match value:
            case '0.1':
                return TimeOption.TENTH
            case '0.5':
                return TimeOption.HALF
            case '1':
                return TimeOption.ONE
            case '3':
                return TimeOption.THREE
            case _:
                return TimeOption.FIVE

    def stringify(self):
        return str(self.value)
