import pygame
from config import COURT_MARGIN, SCREEN_HEIGHT, SCREEN_WIDTH
from game_objects import GameObject

class Ball(GameObject):
    def __init__(self, x, y, radius, color, xv, yv):
        super().__init__(x, y, color)
        self.radius = radius
        self.xv = xv
        self.yv = yv
        self.initial_speed = (xv, yv)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.xv
        self.y += self.yv

        if self.y - self.radius <= COURT_MARGIN:
            self.y = COURT_MARGIN + self.radius
            self.yv *= -1
        elif self.y + self.radius >= SCREEN_HEIGHT - COURT_MARGIN:
            self.y = SCREEN_HEIGHT - COURT_MARGIN - self.radius
            self.yv *= -1

    def reset(self, going_left=False):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.xv = -self.initial_speed[0] if going_left else self.initial_speed[0]
        self.yv = self.initial_speed[1]