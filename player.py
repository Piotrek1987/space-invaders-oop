import pygame
from bullet import Bullet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, STARTING_LIVES, MAX_LIVES, STARTING_AMMO
from assets import load_assets




class Player:
    def __init__(self, image):
        self.image = pygame.transform.scale(image, (60, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5
        self.bullets = []
        self.shoot_cooldown = 0
        self.lives = STARTING_LIVES
        self.max_lives = MAX_LIVES
        self.bullet_count = STARTING_AMMO
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.clone_mode_active = False
        self.clone_timer_start = 0
        self.clones = pygame.sprite.Group()

    def move(self, direction):
        if direction == "left":
            self.rect.x = max(0, self.rect.x - self.speed)
        elif direction == "right":
            self.rect.x = min(SCREEN_WIDTH - self.rect.width, self.rect.x + self.speed)

    def shoot(self):
        if self.shoot_cooldown == 0 and self.bullet_count > 0:
            self.bullets.append(Bullet(self.rect.centerx, self.rect.top, -10))

            if self.clone_mode_active:
                for clone in self.clones:
                    self.bullets.append(Bullet(clone.rect.centerx, clone.rect.top, -10))

            self.shoot_cooldown = 15
            self.bullet_count -= 1  # Only deduct 1 bullet, not 3
            return True
        return False

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)

        if self.clone_mode_active:
            self.clones.update()
            # Handle expiration
            if pygame.time.get_ticks() - self.clone_timer_start > 20000:
                self.clone_mode_active = False
                self.clones.empty()

    def draw(self, surface):
        if self.clone_mode_active:
            self.clones.draw(surface)

        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)


class ClonePlane(pygame.sprite.Sprite):
    def __init__(self, offset_x, player):
        super().__init__()
        self.image = pygame.transform.scale(player.image, (50, 30))
        self.rect = self.image.get_rect()
        self.player = player
        self.offset_x = offset_x


    def update(self):
        self.rect.centerx = self.player.rect.centerx + self.offset_x
        self.rect.bottom = self.player.rect.bottom
