import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('src/resources/assets/crown.png'), (44, 25))

FONT = pygame.font.SysFont("arialblack", 40)

# images
RESUME_IMG_PATH = "src/resources/assets/button_resume.png"
SETTINGS_IMG_PATH = "src/resources/assets/button_options.png"
QUIT_IMG_PATH = "src/resources/assets/button_quit.png"

FPS = 30
