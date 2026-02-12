import pygame
from data.données import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, screen, camera_x, camera_y):
        rect_on_screen = self.rect.move(-camera_x, -camera_y)

        pygame.draw.rect(screen, PLAYER_COLOR, rect_on_screen)

        bar_width = PLAYER_SIZE
        bar_height = 6
        health_ratio = self.health / self.max_health
        current_width = bar_width * health_ratio

        pygame.draw.rect(screen, (255, 0, 0),
                         (rect_on_screen.x,
                          rect_on_screen.y - 10,
                          bar_width,
                          bar_height))

        pygame.draw.rect(screen, (0, 255, 0),
                         (rect_on_screen.x,
                          rect_on_screen.y - 10,
                          current_width,
                          bar_height))
