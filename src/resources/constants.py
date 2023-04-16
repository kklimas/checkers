import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

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

CROWN = pygame.transform.scale(pygame.image.load('src/resources/assets/crown.png'), (45, 45))

FONT_TITLE = pygame.font.SysFont("arialblack", 40)
FONT = pygame.font.SysFont("arialblack", 20)

# images
RESUME_IMG_PATH = "src/resources/assets/button_resume.png"
SETTINGS_IMG_PATH = "src/resources/assets/button_options.png"
QUIT_IMG_PATH = "src/resources/assets/button_quit.png"

FPS = 30
