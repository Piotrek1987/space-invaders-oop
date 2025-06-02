import pygame
import os

FONTS = {}

def load_fonts():
    global FONTS

    custom_font_path = os.path.join("fonts", "Orbitron-VariableFont_wght.ttf")

    try:
        # Try loading the custom font
        FONTS = {
            "small": pygame.font.Font(custom_font_path, 24),
            "medium": pygame.font.Font(custom_font_path, 32),
            "large": pygame.font.Font(custom_font_path, 48),
        }
        print("Orbitron font loaded successfully.")
    except Exception as e:
        print(f"[Font Warning] Could not load custom font, using system default. ({e})")
        FONTS = {
            "small": pygame.font.SysFont("consolas", 24, bold=True),
            "medium": pygame.font.SysFont("consolas", 32, bold=True),
            "large": pygame.font.SysFont("consolas", 48, bold=True),
        }

    return FONTS
