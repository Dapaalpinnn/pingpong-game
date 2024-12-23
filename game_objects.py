import pygame
from config import COURT_MARGIN, SCREEN_HEIGHT

class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        raise NotImplementedError

class Paddle(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dy):
        self.y += dy
        self.y = max(COURT_MARGIN, min(self.y, SCREEN_HEIGHT - COURT_MARGIN - self.height))








