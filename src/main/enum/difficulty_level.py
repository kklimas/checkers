from enum import Enum


class DifficultyLevel(Enum):
    EASY = 'Easy', 1
    MEDIUM = "Medium", 2
    HARD = 'Hard', 3

    @staticmethod
    def from_string(value):
        match value:
            case 'Easy':
                return DifficultyLevel.EASY
            case 'Medium':
                return DifficultyLevel.MEDIUM
            case 'Hard':
                return DifficultyLevel.HARD
