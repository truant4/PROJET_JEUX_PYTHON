import pygame
from data.données import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED

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
