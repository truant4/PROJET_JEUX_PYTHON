import pygame
from data.données import WIDTH, HEIGHT, FPS, BG_COLOR, PLAYER_SIZE
from entities.player import Player
from entities.enemy import Enemy
from world.map import TiledMap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jeu Pygame POO")
        self.clock = pygame.time.Clock()
        self.running = True
        self.attack_rect = None

        self.map = TiledMap("assets/map.tmx")

        # Joueur au centre du MONDE (pas de l'écran)
        self.player = Player(
            self.map.width_px // 2 - PLAYER_SIZE // 2,
            self.map.height_px // 2 - PLAYER_SIZE // 2
        )

        self.enemies = [
                Enemy(self.map.width_px//2 + 100, self.map.height_px//2),
                Enemy(self.map.width_px//2 - 150, self.map.height_px//2 - 50)
                ]

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

        if keys[pygame.K_SPACE]:
            self.attack_rect = self.player.attack()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        for enemy in self.enemies:
            enemy.update(self.player)

        self.player.rect.clamp_ip(pygame.Rect(0, 0, self.map.width_px, self.map.height_px))

        if self.attack_rect:
            for enemy in self.enemies:
                if self.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.damage)

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

        if self.attack_rect:
            attack_on_screen = self.attack_rect.move(-camera_x, -camera_y)
            pygame.draw.rect(self.screen, (0, 0, 255), attack_on_screen, 2)

        pygame.display.flip()
