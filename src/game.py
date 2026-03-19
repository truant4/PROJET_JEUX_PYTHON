import pygame
import pytmx
import pyscroll
from dialog import DialogBox
from données import FPS, BG_COLOR, PLAYER_SIZE
from enemy import Enemy,Boss
from projectile import Projectile
from player import *
from map import *
from animation import HeartDisplay, BossBar
class Game:
    def __init__(self, screen):
        self.running = True
        self.map = "map"
        self.screen = screen  

        pygame.display.set_caption("BasiqueGame")

        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        self.death_timer = None
        self.death_delay = 3000

        self.clock = pygame.time.Clock()
        self.player = Player("player", 0, 0)
        self.dialog_box = DialogBox(self.WIDTH,self.HEIGHT)

        self.map_manager = MapManager(self.screen, self.player, self.clock, self.dialog_box)
        self.attack_rect = None
        self.projectiles = []

        current_map = self.map_manager.maps[self.map]
        tmx = current_map.tmx_data
        self.map_width = tmx.width * tmx.tilewidth
        self.map_height = tmx.height * tmx.tileheight

        self.heart_value = 10
        self.heart_display = HeartDisplay(self.player)

        self.boss = next(
            (e for map_data in self.map_manager.maps.values()
            for e in map_data.enemies if isinstance(e, Boss)),
            None
        )
        self.boss_bar = BossBar(self.boss) if self.boss else None
        self.player.game_clock = self.clock
        for map_data in self.map_manager.maps.values():
            for enemy in map_data.enemies:
                enemy.game_clock = self.clock

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if self.player.is_dead():
            return

        if pressed[pygame.K_ESCAPE]:
            self.running = False

        self.player.move_vector = (0, 0)

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()

        if self.player.move_vector == (0,0):
            self.player.stop()

        if pressed[pygame.K_SPACE]:
            self.player.melee_attack()
    @property
    def enemies(self):
        return self.map_manager.get_map().enemies

    def update(self):
        if self.player.action == "attack" and getattr(self.player, "current_attack_rect", None):
            attack_rect = self.player.current_attack_rect
            for enemy in self.enemies:
                print(f"enemy.feet={enemy.feet} | attack_rect={attack_rect} | collides={attack_rect.colliderect(enemy.feet)}")
                if attack_rect.colliderect(enemy.feet):
                    print("HIT via feet!")
                    enemy.take_damage(self.player.melee_damage)
                    if not getattr(enemy,"immune_to_knockback",False):
                        dx = enemy.feet.centerx - self.player.feet.centerx
                        dy = enemy.feet.centery - self.player.feet.centery
                        distance = max((dx**2 + dy**2) ** 0.5, 1)
                        knockback_strength = 2
                        enemy.knockback_vector = (dx / distance * knockback_strength, dy / distance * knockback_strength)
                        enemy.knockback_timer = enemy.knockback_duration
                        enemy.can_attack = False
            self.player.current_attack_rect = None

        self.map_manager.update()
        self.player.update()

        if self.player.action == "attack" and self.player.clock >= 100:
            if self.player.move_vector != (0, 0):
                self.player.action = "run"
            else:
                self.player.action = "idle"

        for enemy in self.enemies[:]:
            if not enemy.alive():  
                self.enemies.remove(enemy)

        if self.player.is_dead() and self.death_timer is None:
            self.player.direction = "down"
            self.player.action = "death"  
            self.death_timer = pygame.time.get_ticks()

        if self.death_timer is not None:
            elapsed = pygame.time.get_ticks() - self.death_timer
            if elapsed >= self.death_delay:
                print("Player died!")
                self.running = False

    def run(self):
        while self.running:
            self.player.save_location()
            for enemy in self.enemies:
                enemy.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.heart_display.draw(self.screen)
            if self.boss_bar and self.boss.alive():
                self.boss_bar.draw(self.screen)            
            self.dialog_box.render(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.map_manager.check_npc_collisions(self.dialog_box)

            self.clock.tick(40)
