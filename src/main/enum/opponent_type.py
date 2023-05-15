from enum import Enum


class OpponentType(Enum):
    HUMAN = 'Human'
    COMPUTER = 'Computer'

    @staticmethod
    def from_string(value):
        if value == 'Human':
            return OpponentType.HUMAN
        return OpponentType.COMPUTER
