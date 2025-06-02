import pygame
from bullet import Bullet
import random
from assets import load_assets
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import math



# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y, image, speed, health=1, alien_type=1, point_value=10):
#         super().__init__()
#         self.image = image
#         self.rect = self.image.get_rect(topleft=(x, y))
#         self.speed = speed
#         self.original_speed = speed
#         self.health = health
#         self.max_health = health
#         self.point_value = point_value
#         self.alien_type = alien_type
#         self.alive = True
#
#     def move(self):
#         if not self.alive:
#             return
#         self.rect.x += self.speed
#         self.rect.y += 1
#         if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
#             self.speed = -self.speed
#
#     def update(self):
#         self.move()
#
#     def hit(self):
#         self.health -= 1
#         if self.health <= 0:
#             self.alive = False
#
#     def reset_speed(self):
#         self.speed = self.original_speed
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)

import math
import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, health=1, alien_type=1, point_value=10, wave_amplitude=120, wave_frequency=0.00007):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_x = x
        self.speed = speed
        self.original_speed = speed
        self.health = health
        self.max_health = health
        self.point_value = point_value
        self.alien_type = alien_type
        self.alive = True
        self.spawn_time = pygame.time.get_ticks()
        self.wave_amplitude = wave_amplitude
        self.wave_frequency = wave_frequency

    def move(self):
        if not self.alive:
            return
        time_elapsed = pygame.time.get_ticks() - self.spawn_time
        offset = self.wave_amplitude * math.sin(time_elapsed * self.wave_frequency)
        self.rect.x = self.base_x + offset
        self.rect.y += self.speed

    def update(self):
        self.move()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def reset_speed(self):
        self.speed = self.original_speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)



class EnemyBullet:
    def __init__(self, x, y, speed=5):
        self.rect = pygame.Rect(x - 2, y, 4, 10)
        self.speed = speed
        self.color = (255, 0, 0)

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# class FastAlien(Enemy):
#     def __init__(self, x, y, image):
#         super().__init__(x, y, image, speed=2.5, health=1, point_value=10)
#         self.spawn_offset = random.uniform(0, 2 * 3.14)
#
#     def move(self):
#         self.rect.y += self.speed
#         self.rect.x += int(5 * math.sin(pygame.time.get_ticks() * 0.005 + self.spawn_offset))

class FastAlien(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, speed=1, health=1, point_value=10, wave_amplitude=120, wave_frequency=0.0007)

    def move(self):
        if not self.alive:
            return
        time_elapsed = pygame.time.get_ticks() - self.spawn_time
        offset = self.wave_amplitude * math.sin(time_elapsed * self.wave_frequency)
        self.rect.x = self.base_x + offset
        self.rect.y += self.speed


class ZigzagAlien(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, speed=2, health=1, point_value=15, wave_amplitude=200, wave_frequency=0.0009)
        self.direction = random.choice([-1, 1])

    def move(self):
        if not self.alive:
            return
        time_elapsed = pygame.time.get_ticks() - self.spawn_time
        wave_offset = self.wave_amplitude * math.sin(time_elapsed * self.wave_frequency)
        self.rect.x = self.base_x + wave_offset + self.direction * 3
        self.rect.y += self.speed
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1


class TeleportAlien(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, speed=1, health=1, point_value=20,  wave_amplitude=140, wave_frequency=0.0007)
        self.teleport_timer = 0

    def move(self):
        self.rect.y += self.speed
        self.teleport_timer += 1
        if self.teleport_timer > 90:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.teleport_timer = 0


class DiveAlien(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, speed=2, health=1, point_value=15, wave_amplitude=120, wave_frequency=0.00007)
        self.diving = False
        self.dive_speed = 0
        self.dive_duration = 0

    def move(self):
        if not self.diving and random.random() < 0.005:
            self.diving = True
            self.dive_speed = random.randint(5, 10)
            self.dive_duration = random.randint(30, 60)  # frames

        if self.diving:
            self.rect.y += self.dive_speed
            self.dive_duration -= 1
            if self.dive_duration <= 0:
                self.diving = False
        else:
            # Move in a wavy pattern if not diving
            time_elapsed = pygame.time.get_ticks() - self.spawn_time
            offset = self.wave_amplitude * math.sin(time_elapsed * self.wave_frequency)
            self.rect.x = self.base_x + offset
            self.rect.y += self.speed



class TankAlien(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, speed=1, health=3, point_value=25,  wave_amplitude=160, wave_frequency=0.000001)

    def move(self):
        if not self.alive:
            return
        time_elapsed = pygame.time.get_ticks() - self.spawn_time
        offset = (self.wave_amplitude * 0.3) * math.sin(time_elapsed * self.wave_frequency * 0.3)
        self.rect.x = self.base_x + offset
        self.rect.y += self.speed


class BossEnemy(Enemy):
    def __init__(self, x, y, image, speed=1, health=10, alien_type=None):
        super().__init__(x, y, image, speed=speed, health=health)
        self.alien_type = alien_type
        self.max_health = health  # For the health bar display
        self.image = pygame.transform.scale(image, (160, 100))  # Optional: make boss bigger
        self.rect = self.image.get_rect(topleft=(x, y))

class RareAlien(Enemy):
    def __init__(self, x, y, images_dict):
        color_type = random.choice(["orange", "purple"])
        chosen_image = images_dict[color_type]

        # Slightly bigger than normal enemies
        super().__init__(
            x, y,
            chosen_image,
            speed=1.2,
            health=3 if color_type == "orange" else 4,
            point_value=100 if color_type == "orange" else 150,
            wave_amplitude=200,
            wave_frequency=0.0008
        )


