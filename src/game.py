import pygame
import pytmx
import pyscroll
from dialog import DialogBox
from données import WIDTH, HEIGHT, FPS, BG_COLOR, PLAYER_SIZE
from enemy import Enemy
from projectile import Projectile
from player import *
from map import *
from animation import HeartDisplay

class Game:

    def __init__(self, screen):   

        self.running = True
        self.map = "map"

        self.screen = screen         


        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((1980, 1080))
        pygame.display.set_caption("BasiqueGame")

 
        self.clock = pygame.time.Clock()
        # Générer le joeur
        self.player = Player("player",0,0)
        self.map_manager = MapManager(self.screen, self.player,self.clock)
        
        self.dialog_box = DialogBox()

        self.attack_rect = None
        self.projectiles = []
        self.enemies = self.map_manager.get_map().enemies

        current_map = self.map_manager.maps[self.map]
        tmx = current_map.tmx_data
        self.map_width = tmx.width * tmx.tilewidth
        self.map_height = tmx.height * tmx.tileheight


        self.heart_value = 10
        self.heart_display = HeartDisplay(self.player)
        self.player.game_clock = self.clock
        for enemy in self.map_manager.get_map().enemies:
            enemy.game_clock = self.clock

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False

        # Reset movement each frame
        self.player.move_vector = (0, 0)

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()

        # If no movement happened → idle
        if self.player.move_vector == (0,0):
            self.player.stop()

        # Melee attack
        if pressed[pygame.K_SPACE]:
            self.player.melee_attack()

    def update(self):
        self.map_manager.update()
        self.player.update()


        if self.player.action == "attack" and getattr(self.player, "current_attack_rect", None):
            attack_rect = self.player.current_attack_rect
            for enemy in self.enemies:
                print("FOUND ENEMY!", enemy.rect)
                print("Player attacking:", attack_rect)
      
        if self.player.action == "attack" and getattr(self.player, "current_attack_rect", None):
            attack_rect = self.player.current_attack_rect
            for enemy in self.enemies:
                enemy.save_location()
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.melee_damage)
                    print("enemy health:", enemy.health)

                    # --- APPLY KNOCKBACK ---
                    dx = enemy.rect.centerx - self.player.rect.centerx
                    dy = enemy.rect.centery - self.player.rect.centery

                    distance = max((dx**2 + dy**2) ** 0.5, 1)  # prevent division by zero
                    knockback_strength = 2  # pixels per frame

                    enemy.knockback_vector = (dx/distance * knockback_strength, dy/distance * knockback_strength)
                    enemy.knockback_timer = enemy.knockback_duration
                    enemy.can_attack = False

            self.player.current_attack_rect = None

        if self.player.action == "attack" and self.player.clock >= 100:
            if self.player.move_vector != (0, 0):
                self.player.action = "run"
            else:
                self.player.action = "idle"

        for enemy in self.enemies[:]:
            if enemy.is_dead():
                self.map_manager.get_group().remove(enemy)
                self.enemies.remove(enemy)

        if self.player.is_dead():
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
            self.dialog_box.render(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.map_manager.check_npc_collisions(self.dialog_box)

            self.clock.tick(40)

