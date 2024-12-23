# config.py
import pygame

# Initialize Pygame
pygame.init()

# Colors
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 127, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (34, 139, 34)
}

# Screen and Court Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COURT_MARGIN = 50
COURT_WIDTH = SCREEN_WIDTH - (2 * COURT_MARGIN)
COURT_HEIGHT = SCREEN_HEIGHT - (2 * COURT_MARGIN)
WINNING_SCORE = 5

# Initialize Game Screen
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Table Tennis")
font = pygame.font.SysFont("monospace", 50)
small_font = pygame.font.SysFont("monospace", 30)