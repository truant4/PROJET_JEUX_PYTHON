import pygame
from data.données import WIDTH, HEIGHT, FPS, BG_COLOR, PLAYER_SIZE
from entities.player import Player
from world.map import TiledMap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jeu Pygame POO")
        self.clock = pygame.time.Clock()
        self.running = True

        self.map = TiledMap("assets/map.tmx")

        # Joueur au centre du MONDE (pas de l'écran)
        self.player = Player(
            self.map.width_px // 2 - PLAYER_SIZE // 2,
            self.map.height_px // 2 - PLAYER_SIZE // 2
        )

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

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Clamp joueur dans la map
        self.player.rect.clamp_ip(pygame.Rect(0, 0, self.map.width_px, self.map.height_px))

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

        pygame.display.flip()
