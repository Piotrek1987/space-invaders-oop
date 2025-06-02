import pygame
from fonts import load_fonts
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

FONTS = load_fonts()

def draw_text(surface, text, x, y, size=24, center=False, color=(255, 255, 255), font=None):
    if font is None:
        font_map = {24: "small", 32: "medium", 48: "large"}
        font = FONTS.get(font_map.get(size, "medium"))
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y) if center else (x, y))
    surface.blit(text_surface, rect)

class Button:
    def __init__(self, x, y, width, height, text, callback, font=None,
                 color=(50, 50, 50), hover_color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font or FONTS["medium"]  # fallback to medium font if not provided
        self.hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)

        draw_text(
            surface,
            self.text,
            self.rect.centerx,
            self.rect.centery,
            font=self.font,
            center=True,
            color=self.text_color
        )


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.callback()


def draw_start_screen(screen, start_btn=None, quit_btn=None):
    draw_text(screen, "SPACE INVADERS", SCREEN_WIDTH // 2, 150, size=48, center=True)

    if start_btn and quit_btn:
        start_btn.draw(screen)
        quit_btn.draw(screen)

def draw_game_over_screen(screen, score, restart_btn=None):
    draw_text(screen, "GAME OVER", SCREEN_WIDTH // 2, 150, size=48, center=True)
    draw_text(screen, f"Score: {score}", SCREEN_WIDTH // 2, 220, size=32, center=True)
    draw_text(screen, "Press R to restart or ESC to quit", SCREEN_WIDTH // 2, 280, size=24, center=True)

    if restart_btn:
        restart_btn.draw(screen)