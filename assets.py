import pygame

def load_assets(screen_size):
    # Load images
    player_image = pygame.image.load("img/ship2.png").convert_alpha()

    alien_images = {
        1: pygame.image.load("img/alien1.png").convert_alpha(),
        2: pygame.image.load("img/alien2.png").convert_alpha(),
        3: pygame.image.load("img/alien3.png").convert_alpha(),
        4: pygame.image.load("img/alien4.png").convert_alpha(),
        5: pygame.image.load("img/alien5.png").convert_alpha(),
    }

    # Resize alien images
    for key in alien_images:
        alien_images[key] = pygame.transform.scale(alien_images[key], (60, 50))

    # ✅ Load rare enemies
    rare_enemy_images = {
        "orange": pygame.transform.scale(
            pygame.image.load("img/rare-orange.png").convert_alpha(), (60, 50)
        ),
        "purple": pygame.transform.scale(
            pygame.image.load("img/rare-purple.png").convert_alpha(), (60, 50)
        )
    }

    # ✅ Load powerup images
    powerup_images = {
        "health": pygame.image.load("img/medical-kit.png").convert_alpha(),
        "ammo": pygame.image.load("img/bullet.png").convert_alpha(),
        "shield": pygame.image.load("img/shield.png").convert_alpha(),
        "explode": pygame.image.load("img/frozen.png").convert_alpha(),
        "clone": pygame.image.load("img/ship-clone.png").convert_alpha()
    }

    # Resize powerups if needed
    for key in powerup_images:
        powerup_images[key] = pygame.transform.scale(powerup_images[key], (40, 40))

    # Load and scale backgrounds
    backgrounds = [
        pygame.image.load("img/space0.jpg").convert(),
        pygame.image.load("img/space1.jpg").convert(),
        pygame.image.load("img/space2.jpg").convert(),
        pygame.image.load("img/space3.jpg").convert(),
        pygame.image.load("img/moon1.jpg").convert(),
    ]

    backgrounds = [pygame.transform.scale(bg, screen_size) for bg in backgrounds]

    # Load sounds
    sounds = {
        "powerup_health": pygame.mixer.Sound("sounds/Arcade Power Up 02.wav"),
        "powerup_ammo": pygame.mixer.Sound("sounds/Arcade Power Up 03.wav"),
        "enemy_die": pygame.mixer.Sound("sounds/Comical Metal Gong.wav"),
        "game_over": pygame.mixer.Sound("sounds/Game Over 01.wav"),
        "player_move": pygame.mixer.Sound("sounds/Hydraulics 01.wav"),
        "enemy_move": pygame.mixer.Sound("sounds/Ping Pong Paddle 01.wav"),
        "player_shoot": pygame.mixer.Sound("sounds/Space Gun 01.wav"),
        "enemy_shoot": pygame.mixer.Sound("sounds/Space Gun 06.wav"),
    }

    for sound in sounds.values():
        sound.set_volume(0.4)

    return {
        "player_image": player_image,
        "alien_images": alien_images,
        "rare_enemy_images": rare_enemy_images,
        "powerup_images": powerup_images,
        "backgrounds": backgrounds,
        "sounds": sounds
    }
