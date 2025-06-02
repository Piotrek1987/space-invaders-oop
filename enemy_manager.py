import pygame
import random

class EnemyManager:
    def __init__(self, enemy_class, screen_width, screen_height, spawn_interval=2000, scale_factor=1.1):
        self.enemy_class = enemy_class
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_interval = spawn_interval
        self.scale_factor = scale_factor
        self.enemies = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.base_health = 100
        self.base_damage = 10
        self.enemy_speed = 2

    def update(self, player, bullets):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_enemy(player)
            self.last_spawn_time = current_time

        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.rect.colliderect(player.rect):
                player.take_damage(enemy.damage)
                self.enemies.remove(enemy)
                continue

            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.health -= bullet.damage
                    bullets.remove(bullet)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                    break

    def spawn_enemy(self, player):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, self.screen_width), 0
        elif side == "bottom":
            x, y = random.randint(0, self.screen_width), self.screen_height
        elif side == "left":
            x, y = 0, random.randint(0, self.screen_height)
        else:
            x, y = self.screen_width, random.randint(0, self.screen_height)

        health = int(self.base_health)
        damage = int(self.base_damage)
        enemy = self.enemy_class(x, y, health, damage, self.enemy_speed, player)
        self.enemies.append(enemy)

        self.base_health *= self.scale_factor
        self.base_damage *= self.scale_factor

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

    def reset(self):
        self.enemies.clear()
        self.base_health = 100
        self.base_damage = 10
