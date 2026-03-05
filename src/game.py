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

    def __init__(self):
        # Démarrage
        self.running = True
        self.map = "map"


        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((1920, 1200))
        pygame.display.set_caption("BasiqueGame")

 
        # Générer le joeur
        self.player = Player(0,0,0)
        self.map_manager = MapManager(self.screen, self.player)
        
        self.dialog_box = DialogBox()

        self.clock = pygame.time.Clock()
        self.attack_rect = None
        self.projectiles = []
        self.enemies = self.map_manager.get_map().enemies

        current_map = self.map_manager.maps[self.map]
        tmx = current_map.tmx_data
        self.map_width = tmx.width * tmx.tilewidth
        self.map_height = tmx.height * tmx.tileheight

        self.heart_value = 10

# in Game.__init__
        self.heart_display = HeartDisplay(self.player)


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        else:
            self.player.stop()
        
        # Melee attack
        if pressed[pygame.K_SPACE]:
            self.player.melee_attack()

                
              
    def update(self):
        self.map_manager.update()

        self.player.update()

        for bullet in self.projectiles[:]:
            bullet.update()

            if bullet.off_screen(self.map_width, self.map_height):
                self.projectiles.remove(bullet)

        for bullet in self.projectiles[:]:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.ranged_damage)
                    self.projectiles.remove(bullet)
                    break

      
        if self.player.action == "attack" and getattr(self.player, "current_attack_rect", None):
            attack_rect = self.player.current_attack_rect
            for enemy in self.enemies:
                # Debug
                print("FOUND ENEMY!", enemy.rect)
                print("Player attacking:", attack_rect)

                if attack_rect.colliderect(enemy.rect):
                    print("Enemy took damage!")
                    enemy.take_damage(self.player.melee_damage)
                    print("enemy health:", enemy.health)

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

        # Clock
        while self.running:

            self.player.save_location()
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

            self.clock.tick(60)

        pygame.quit()
