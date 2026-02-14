import pygame
from data.données import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.damage = 20
        self.attack_cooldown = 500 # milliseconds
        self.last_attack_time = 0
        self.direction = (0,0)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = (-1,0)
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = (1,0)
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = (0,-1)
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = (0,1)

    def take_dmg(self, amount):
        self.health -= amount

    def attack(self):
        now = pygame.time.get_ticks()

        if now - self.last_attack_time >= self.attack_cooldown and self.direction[0] != 0:
            self.last_attack_time = now 

            attack_rect = self.rect.inflate(50,0)


            attack_rect.x += self.direction[0] * PLAYER_SIZE
            attack_rect.y += self.direction[1] * PLAYER_SIZE

            return attack_rect
        elif now - self.last_attack_time >= self.attack_cooldown and self.direction[1] != 0:
            self.last_attack_time = now 
            attack_rect = self.rect.inflate(0,50)


            attack_rect.x += self.direction[0] * PLAYER_SIZE
            attack_rect.y += self.direction[1] * PLAYER_SIZE

            return attack_rect



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
