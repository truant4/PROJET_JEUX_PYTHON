import pygame
import pytmx
import pyscroll
from dialog import DialogBox
from données import WIDTH, HEIGHT, FPS, BG_COLOR, PLAYER_SIZE
from enemy import Enemy
from projectile import Projectile
from player import *
from map import *


class Game:

    def __init__(self):
        # Démarrage
        self.running = True
        self.map = "map"


        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("BasiqueGame")


        # Générer le joeur
        self.player = Player(0,0,0)
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()

        self.clock = pygame.time.Clock()
        self.attack_rect = None
        self.projectiles = []

        self.enemies = [
            Enemy(self.map.width_px//2 + 100, self.map.height_px//2),
            Enemy(self.map.width_px//2 - 150, self.map.height_px//2 - 50)
                ]

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


    def update(self):
        self.map_manager.update()

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        for bullet in self.projectiles[:]:
            bullet.update()
            if bullet.off_screen(self.map.width_px,self.map.height_px):
                self.projectiles.remove(bullet)

        for bullet in self.projectiles[:]:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.ranged_damage)
                    self.enemies = [e for e in self.enemies if not e.is_dead()]

                    if bullet in self.projectiles:
                        self.projectiles.remove(bullet)

        for enemy in self.enemies:
            enemy.update(self.player)
 
            if enemy.rect.colliderect(self.player.rect):
                self.player.take_dmg(enemy.damage)

            if enemy.attack_rect is not None and enemy.attack_rect.colliderect(self.player.rect):
                self.player.take_dmg(enemy.damage)

                if self.player.is_dead():
                    self.running = False

        self.player.rect.clamp_ip(pygame.Rect(0, 0, self.map.width_px, self.map.height_px))

        if self.attack_rect:
            for enemy in self.enemies:
                if self.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.melee_damage)

            self.enemies = [e for e in self.enemies if not e.is_dead()]


    def draw(self):
        self.screen.fill(BG_COLOR)

        # Caméra centrée sur le joueur
        camera_x = self.player.rect.centerx - WIDTH // 2
        camera_y = self.player.rect.centery - HEIGHT // 2

        # Clamp caméra dans la map
        camera_x = max(0, min(camera_x, self.map.width_px - WIDTH))
        camera_y = max(0, min(camera_y, self.map.height_px - HEIGHT))

        # Dessin map puis joueur
        self.map.draw(self.screen, camera_x, camera_y)
        self.player.draw(self.screen, camera_x, camera_y)

        for enemy in self.enemies:
            enemy.draw(self.screen, camera_x, camera_y)
            if enemy.attack_rect is not None:
                attack_on_screen = enemy.attack_rect.move(-camera_x, -camera_y)
                pygame.draw.rect(self.screen, (255, 255, 0), attack_on_screen, 2)
        
        for bullet in self.projectiles:
            bullet.draw(self.screen, camera_x, camera_y)

        if self.attack_rect:
            attack_on_screen = self.attack_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(self.screen, (0, 0, 255), attack_on_screen, 2)

        pygame.display.flip()



    def run(self):
        clock = pygame.time.Clock()

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)

            clock.tick(60)

        pygame.quit()