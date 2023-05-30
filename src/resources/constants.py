import pygame

pygame.init()

WIDTH, BOARD_WIDTH, HEIGHT = 1000, 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
GREEN = (119, 149, 86)
CREAM = (235, 236, 208)

LIGHT_THEME = {
    "background": (179, 205, 224),
    "white-field": CREAM,
    "black-field": GREEN
}
DARK_THEME = {
    "background": (1, 31, 75),
    "white-field": GREY,
    "black-field": BLACK
}

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

CLOCK_COUNTER_TICK = 10

CROWN = pygame.transform.scale(pygame.image.load('src/resources/assets/crown.png'), (45, 45))

FONT_TITLE = pygame.font.SysFont("arialblack", 40)
FONT = pygame.font.SysFont("arialblack", 20)
RESULTS_FONT = pygame.font.SysFont("arialblack", 16)

CONFIG_FILE_PATH = "src/resources/config.json"

FPS = 30
