import pygame

class Bullet:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x - 2, y, 4, 10)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)