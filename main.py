import pygame
pygame.init() 

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from fonts import load_fonts
from assets import load_assets
from game import Game


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")


assets = load_assets((SCREEN_WIDTH, SCREEN_HEIGHT))
fonts = load_fonts()

game = Game(screen, fonts, assets)
game.run()