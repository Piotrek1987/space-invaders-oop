import pygame
import random
import sys


from settings import *
from player import Player, ClonePlane
# from enemy_manager import EnemyManager
from enemy import Enemy, EnemyBullet, FastAlien, ZigzagAlien, TeleportAlien, DiveAlien, TankAlien, BossEnemy, RareAlien
from bullet import Bullet
from powerup import PowerUp
from ui import draw_text, draw_start_screen, draw_game_over_screen, Button
from fonts import load_fonts
from assets import load_assets
from highscores import load_high_scores, save_high_scores


pygame.init()

class Game:
    def __init__(self, screen, fonts, assets):
        self.screen = screen
        self.fonts = fonts
        self.assets = assets
        self.clock = pygame.time.Clock()
        self.running = True
        self._move_sound_timer = 0
        self.high_scores = load_high_scores()
        self.wave_in_progress = False
        # self.enemy_manager = EnemyManager(Enemy, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.wave_count = 0
        self.waves_since_last_elite = 0

        # Game states
        self.state = "start"  # "start", "playing", "paused", "game_over"
        self.difficulty = None  # Will be set to "easy" or "hard"

        # Entities
        self.player = Player(self.assets["player_image"])
        self.enemies = []
        self.enemy_bullets = []
        self.powerups = []

        # Timers
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.enemy_shoot_timer = 0
        self.powerup_timer = 0
        self.wave_timer = 0
        self.slowmo_timer = 0

        # Game variables
        self.score = 0
        self.boss_active = False
        self.boss_defeated = 0
        self.current_alien_type = 1
        self.current_background_index = 0
        self.current_boss = None
        self.boss_fight = False
        self.enemy_direction = 1  # 1 for right, -1 for left
        self.enemy_speed = 2

        # Assets
        self.heart_image = pygame.image.load("img/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        self.medkit_image = pygame.image.load("img/medical-kit.png").convert_alpha()
        self.medkit_image = pygame.transform.scale(self.medkit_image, (40, 40))
        self.bullet_powerup_image = pygame.image.load("img/bullet.png").convert_alpha()
        self.bullet_powerup_image = pygame.transform.scale(self.bullet_powerup_image, (30, 30))
        self.explode_image = pygame.image.load("img/frozen.png").convert_alpha()
        self.explode_image = pygame.transform.scale(self.explode_image, (40, 40))
        self.shield_image = pygame.image.load("img/shield.png").convert_alpha()
        self.shield_image = pygame.transform.scale(self.shield_image, (40, 40))
        self.clone_image = pygame.image.load("img/ship-clone.png").convert_alpha()
        self.clone_image = pygame.transform.scale(self.clone_image, (40, 40))
        self.backgrounds = assets["backgrounds"]
        self.high_scores_bg = pygame.image.load("img/neon-sky.jpg").convert()
        self.high_scores_bg = pygame.transform.scale(self.high_scores_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.start_button = Button(300, 200, 200, 50, "Start", lambda: setattr(self, "state", "choose_difficulty"), self.fonts["medium"])
        self.high_scores_button = Button(300, 300, 220, 50, "High Scores", lambda: setattr(self, "state", "high_scores"), self.fonts["medium"])
        self.quit_button = Button(300, 400, 200, 50, "Quit", self.quit, self.fonts["medium"])
        self.easy_button = Button(300, 300, 200, 50, "Easy Mode", lambda: self.start_game("easy"), self.fonts["medium"])
        self.hard_button = Button(300, 370, 200, 50, "Hard Mode", lambda: self.start_game("hard"), self.fonts["medium"])

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()

            if self.state in ["start", "choose_difficulty"]:
                self.draw_start()
            elif self.state == "playing":
                self.update()
                self.draw()
            elif self.state == "paused":
                self.draw_pause()
            elif self.state == "game_over":
                self.draw_game_over()
            elif self.state == "high_scores":
                self.draw_high_scores()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if self.state == "start":
                self.start_button.handle_event(event)
                self.high_scores_button.handle_event(event)
                self.quit_button.handle_event(event)

            elif self.state == "choose_difficulty":
                self.easy_button.handle_event(event)
                self.hard_button.handle_event(event)

            elif self.state == "high_scores":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "start"

        keys = pygame.key.get_pressed()
        if self.state == "playing":
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self._move_sound_timer > 10:
                    self.assets["sounds"]["player_move"].play()
                    self._move_sound_timer = 0
                self.player.move("left")

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self._move_sound_timer > 10:
                    self.assets["sounds"]["player_move"].play()
                    self._move_sound_timer = 0
                self.player.move("right")

            self._move_sound_timer += 1

            if keys[pygame.K_SPACE]:
                if self.player.shoot():  # assuming shoot() returns True if bullet fired
                    self.assets["sounds"]["player_shoot"].play()

            if keys[pygame.K_p]:
                self.state = "paused"

            if keys[pygame.K_k]:
                self.kill_all_enemies()

        
        elif self.state == "paused" and keys[pygame.K_p]:
            self.state = "playing"
        elif self.state == "game_over":
            if keys[pygame.K_ESCAPE]:
                self.quit()
            elif keys[pygame.K_r]:
                self.reset_game()

    def update(self):
        self.player.update()

        self.spawn_timer += 1
        if not self.boss_active and self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.move()
            if not enemy.alive:
                continue
            if enemy.rect.bottom >= SCREEN_HEIGHT - DANGER_ZONE_HEIGHT:
                self.enemies.remove(enemy)
                self.player.lives -= 1
                if self.player.lives <= 0:
                    if self.score > self.high_scores[self.difficulty]:
                        self.high_scores[self.difficulty] = self.score
                        save_high_scores(self.high_scores)
                    self.state = "game_over"

        self.handle_collisions()
        self.handle_enemy_shooting()
        self.update_enemy_bullets()
        self.update_powerups()

        # Boss and background logic
        if not self.boss_active and self.score >= (self.boss_defeated + 1) * 700:
            self.spawn_boss()
            self.boss_active = True

        if self.boss_active and not any(e.health > 1 for e in self.enemies):
            self.boss_active = False
            self.boss_defeated += 1
            self.current_boss = None  # 👈 Clear the boss reference
            self.next_cycle()

        # if random.randint(0, 600) == 1:
        #     self.spawn_elite_enemy()

        if self.slowmo_timer > 0:
            for enemy in self.enemies:
                enemy.speed = enemy.original_speed // 2
            self.slowmo_timer -= 1
        else:
            for enemy in self.enemies:
                enemy.reset_speed()

        # if self.player.invulnerable:
        #     self.player.shield_timer -= 1
        #     if self.player.shield_timer <= 0:
        #         self.player.invulnerable = False

        if not self.enemies:
            if self.wave_in_progress:
                self.wave_in_progress = False
                self.boss_fight = True

            elif self.boss_fight:
                self.boss_fight = False
                self.current_alien_type += 1
                self.current_alien_type = min(self.current_alien_type, 5)
                self.wave_timer = 60
            elif self.wave_timer > 0:
                self.wave_timer -= 1
                if self.wave_timer == 0:
                    self.spawn_wave()

        if self.wave_timer > 0:
            self.wave_timer -= 1
            if self.wave_timer == 0:
                if not self.boss_fight:
                    self.spawn_boss()
                else:
                    self.spawn_wave()

    def spawn_enemy(self):
        x = random.randint(0, SCREEN_WIDTH - 60)
        y = 0

        alien_type = self.current_alien_type  # 👈 stick to current wave's alien type

        if alien_type == 1:
            speed = 3
            health = 1
            image = self.assets["alien_images"][1]
        elif alien_type == 2:
            speed = 2
            health = 2
            image = self.assets["alien_images"][2]
        elif alien_type == 3:
            speed = 1
            health = 2
            image = self.assets["alien_images"][3]
        elif alien_type == 4:
            speed = 2
            health = 2
            image = self.assets["alien_images"][4]
        elif alien_type == 5:
            speed = 1
            health = 4
            image = self.assets["alien_images"][5]

        alien_class_map = {
            1: FastAlien,
            2: ZigzagAlien,
            3: TeleportAlien,
            4: DiveAlien,
            5: TankAlien
        }

        alien_cls = alien_class_map.get(self.current_alien_type, Enemy)
        enemy = alien_cls(x, y, self.assets["alien_images"][self.current_alien_type])
        self.enemies.append(enemy)

    # def spawn_wave(self):
    #     self.wave_in_progress = True
    #     for _ in range(6):  # spawn regular enemies
    #         self.spawn_enemy()
    #
    #     # Occasionally add rare elite
    #     if random.random() < 0.1:
    #         self.spawn_elite_enemy()

    def spawn_wave(self):
        self.wave_in_progress = True
        self.wave_count += 1
        self.waves_since_last_elite += 1

        for _ in range(6):
            self.spawn_enemy()

        # Guaranteed elite every 3 waves
        if self.waves_since_last_elite >= 2:
            self.spawn_elite_enemy()
            self.waves_since_last_elite = 0
        # Otherwise, 10% random chance
        elif random.random() < 0.5:
            self.spawn_elite_enemy()
            self.waves_since_last_elite = 0

    def spawn_boss(self):
        x = SCREEN_WIDTH // 2 - 60
        y = 0
        boss_health = 10 + self.current_alien_type * 2
        boss_speed = 1
        image = self.assets["alien_images"][self.current_alien_type]

        boss = BossEnemy(x, y, image, speed=boss_speed, health=boss_health, alien_type=self.current_alien_type)
        self.current_boss = boss
        self.enemies.append(boss)

    def spawn_elite_enemy(self):
        x = random.randint(0, SCREEN_WIDTH - 60)
        y = 0

        # Get rare enemy image dictionary from self.assets
        images_dict = self.assets["rare_enemy_images"]

        rare_alien = RareAlien(x, y, images_dict)
        self.enemies.add(rare_alien)

    # 99 for elites

    def handle_collisions(self):
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.hit()
                    try:
                        self.player.bullets.remove(bullet)
                    except ValueError:
                        pass
                    if not enemy.alive:
                        self.assets["sounds"]["enemy_die"].play()
                        self.score += 10
                        try:
                            self.enemies.remove(enemy)
                        except ValueError:
                            pass
                    break

        for bullet in self.player.bullets[:]:
            for powerup in self.powerups:
                if bullet.rect.colliderect(powerup.rect):

                    if powerup.kind == "medkit" and self.player.lives < self.player.max_lives:
                        self.player.lives += 1
                        self.assets["sounds"]["powerup_health"].play()

                    elif powerup.kind == "medkit" and self.player.lives == self.player.max_lives:
                        points_awarded = 0
                        for enemy in self.enemies:
                            if enemy.alive:
                                points_awarded += enemy.point_value
                                enemy.alive = False
                        self.enemies.clear()
                        self.score += points_awarded
                        self.assets["sounds"]["powerup_ammo"].play()

                    elif powerup.kind == "ammo":
                        if self.difficulty == "easy":
                            self.player.bullet_count += 50
                        else:  # hard mode
                            self.player.bullet_count += 30
                        self.assets["sounds"]["powerup_ammo"].play()

                    elif powerup.kind == "shield" and self.player.lives < self.player.max_lives:
                        self.player.lives += 2
                        self.assets["sounds"]["powerup_health"].play()

                    elif powerup.kind == "shield" and self.player.lives == self.player.max_lives:
                        self.player.bullet_count += 25
                        self.assets["sounds"]["powerup_health"].play()

                    elif powerup.kind == "explode":
                        points_awarded = 0
                        for enemy in self.enemies:
                            if enemy.alive:
                                points_awarded += enemy.point_value  # or use enemy.point_value if you added that
                                enemy.alive = False
                        self.enemies.clear()
                        self.score += points_awarded
                        self.assets["sounds"]["powerup_ammo"].play()

                    elif powerup.kind == "clone":
                        self.player.clone_mode_active = True
                        self.player.clone_timer_start = pygame.time.get_ticks()
                        self.player.clones = pygame.sprite.Group(
                            ClonePlane(-60, self.player),
                            ClonePlane(60, self.player)
                        )

                    try:
                        self.player.bullets.remove(bullet)
                    except ValueError:
                        pass
                    self.powerups.remove(powerup)
                    break

        # Player collides with powerup (in case they can't shoot it)
        for powerup in self.powerups[:]:
            if self.player.rect.colliderect(powerup.rect):
                if powerup.kind == "medkit" and self.player.lives < self.player.max_lives:
                    self.player.lives += 1
                    self.assets["sounds"]["powerup_health"].play()

                elif powerup.kind == "medkit" and self.player.lives == self.player.max_lives:
                    points_awarded = 0
                    for enemy in self.enemies:
                        if enemy.alive:
                            points_awarded += enemy.point_value
                            enemy.alive = False
                    self.enemies.clear()
                    self.score += points_awarded
                    self.assets["sounds"]["powerup_ammo"].play()

                elif powerup.kind == "ammo":
                    if self.difficulty == "easy":
                        self.player.bullet_count += 50
                    else:
                        self.player.bullet_count += 30
                    self.assets["sounds"]["powerup_ammo"].play()

                elif powerup.kind == "shield" and self.player.lives < self.player.max_lives:
                    self.player.lives += 2
                    self.assets["sounds"]["powerup_health"].play()

                elif powerup.kind == 'shield' and self.player.lives == self.player.max_lives:
                    self.player.bullet_count += 25
                    self.assets["sounds"]["powerup_health"].play()

                elif powerup.kind == "explode":
                    points_awarded = 0
                    for enemy in self.enemies:
                        if enemy.alive:
                            points_awarded += enemy.point_value  # or use enemy.point_value if you added that
                            enemy.alive = False
                    self.enemies.clear()
                    self.score += points_awarded
                    self.assets["sounds"]["powerup_ammo"].play()

                elif powerup.kind == "clone":
                    self.player.clone_mode_active = True
                    self.player.clone_timer_start = pygame.time.get_ticks()
                    self.player.clones = pygame.sprite.Group(
                        ClonePlane(-60, self.player),
                        ClonePlane(60, self.player)
                    )

                self.powerups.remove(powerup)
                break

    def handle_enemy_shooting(self):
        self.enemy_shoot_timer += 1
        interval = 45 if self.boss_active else 90
        if self.enemy_shoot_timer >= interval:
            alive = [e for e in self.enemies if e.alive]
            if alive:
                shooter = random.choice(alive)
                self.enemy_bullets.append(EnemyBullet(shooter.rect.centerx, shooter.rect.bottom))
                self.assets["sounds"]["enemy_shoot"].play()
            self.enemy_shoot_timer = 0

    def update_enemy_bullets(self):
        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                if self.player.lives <= 0:
                    if self.score > self.high_scores[self.difficulty]:
                        self.high_scores[self.difficulty] = self.score
                        save_high_scores(self.high_scores)
                    self.assets["sounds"]["game_over"].play()
                    self.state = "game_over"

    def update_powerups(self):
        self.powerup_timer += 1
        if self.powerup_timer >= 600:
            self.spawn_powerup()
            self.powerup_timer = 0

        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.rect.top > SCREEN_HEIGHT:
                self.powerups.remove(powerup)

    def spawn_powerup(self):
        x = random.randint(0, SCREEN_WIDTH - 40)
        y = 0
        kind = random.choice(["medkit", "ammo", "shield", "explode", "clone"])
        if kind == "medkit":
            image = self.medkit_image
        elif kind == "ammo":
            image = self.bullet_powerup_image
        elif kind == "shield":
            image = self.shield_image
        elif kind == "explode":
            image = self.explode_image
        elif kind == "clone":
            image = self.clone_image

        self.powerups.append(PowerUp(x, y, kind, image))

    def draw(self):
        self.screen.blit(self.backgrounds[self.current_background_index], (0, 0))

        # Danger zone
        danger_surface = pygame.Surface((SCREEN_WIDTH, DANGER_ZONE_HEIGHT), pygame.SRCALPHA)
        danger_surface.fill(DANGER_ZONE_COLOR)
        self.screen.blit(danger_surface, (0, SCREEN_HEIGHT - DANGER_ZONE_HEIGHT))

        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # UI elements
        draw_text(self.screen, f"Score: {self.score}", 80, 20)
        if self.difficulty:
            draw_text(self.screen, f"High Score ({self.difficulty.title()}): {self.high_scores[self.difficulty]}", 165,50)
        draw_text(self.screen, f"Ammo: {self.player.bullet_count}", 80, 80)

        # Position lives (hearts) in the top-right corner
        heart_spacing = 40
        start_x = SCREEN_WIDTH - (self.player.max_lives * heart_spacing) - 10
        y = 20  # Align with score text

        for i in range(self.player.max_lives):
            x = start_x + i * heart_spacing
            heart = self.heart_image if i < self.player.lives else self.heart_image.copy()
            if i >= self.player.lives:
                heart.fill((100, 100, 100, 100), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(heart, (x, y))

        # Boss Health Bar
        if self.current_boss:
            bar_width = 400
            bar_height = 20
            x = SCREEN_WIDTH // 2 - bar_width // 2
            y = 10

            health_ratio = self.current_boss.health / self.current_boss.max_health
            current_bar_width = int(bar_width * health_ratio)

            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, current_bar_width, bar_height))
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    def draw_start(self):
        start_background = pygame.image.load("img/spaceship1.jpg").convert()
        start_background = pygame.transform.scale(start_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(start_background, (0, 0))

        if self.state == "start":
            draw_start_screen(self.screen, self.start_button, self.quit_button)
            self.start_button.draw(self.screen)
            self.high_scores_button.draw(self.screen)
            self.quit_button.draw(self.screen)

        elif self.state == "choose_difficulty":
            draw_text(self.screen, "Select Difficulty", SCREEN_WIDTH // 2 - 100, 150, self.fonts["large"],(255, 255, 255))
            self.easy_button.draw(self.screen)
            self.hard_button.draw(self.screen)

    def draw_high_scores(self):
        self.screen.blit(self.high_scores_bg, (0, 0))
        draw_text(self.screen, "HIGH SCORES", SCREEN_WIDTH // 2 - 100, 100, self.fonts["large"])
        draw_text(self.screen, f"Easy: {self.high_scores['easy']}", SCREEN_WIDTH // 2 - 80, 200)
        draw_text(self.screen, f"Hard: {self.high_scores['hard']}", SCREEN_WIDTH // 2 - 80, 250)
        draw_text(self.screen, "Press ESC to return", SCREEN_WIDTH // 2 - 130, 400)


    def draw_pause(self):
        draw_text(self.screen, "PAUSED - Press P to resume", SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2)

    def draw_game_over(self):
        draw_game_over_screen(self.screen, self.score)

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.player = Player(self.assets["player_image"])

        if self.difficulty == "easy":
            self.player.bullet_count = 150
        elif self.difficulty == "hard":
            self.player.bullet_count = 70

        self.enemies = []
        self.enemy_bullets = []
        self.powerups = []

        self.spawn_timer = 0
        self.enemy_shoot_timer = 0
        self.powerup_timer = 0
        self.score = 0
        self.boss_active = False
        self.boss_defeated = 0
        self.current_alien_type = 1
        self.current_background_index = 0
        self.state = "playing"
        self.current_boss = None  # 👈 Clear it here too

        self.spawn_enemy()

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.player.bullet_count = 150 if difficulty == "easy" else 70
        self.state = "playing"

    def next_cycle(self):
        self.boss_active = False
        self.spawn_timer = 0
        self.enemy_shoot_timer = 0
        self.powerup_timer = 0
        self.current_alien_type = (self.boss_defeated % 5) + 1
        self.current_background_index = self.boss_defeated % len(self.backgrounds)
        self.enemies = []
        self.enemy_bullets = []
        self.powerups = []
        self.current_boss = None

    def kill_all_enemies(self):
        points_awarded = 0
        for enemy in self.enemies:
            if enemy.alive:
                points_awarded += enemy.point_value  # or use enemy.point_value if you added that
                enemy.alive = False
        self.enemies.clear()
        self.score += points_awarded
        # print(f"[CHEAT] All enemies eliminated. +{points_awarded} points awarded.")


