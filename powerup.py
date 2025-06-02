import pygame
from settings import AMMO_REPLENISH
from assets import load_assets


class PowerUp:
    def __init__(self, x, y, kind, image):
        self.kind = kind  # "medkit", "ammo", "slow
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def apply(self, player):
        player.bullet_count += AMMO_REPLENISH