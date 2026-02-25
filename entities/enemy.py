import pygame
import math
class Enemy:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,32,32)
        self.health = 50
        self.max_health = 50
        self.speed = 1
        self.color = (200,50,50)
        self.direction = (0,0)
        self.damage = 2
        self.attack_rect = None
        self.last_attack_time = 0
        self.attack_duration = 200 

    def take_damage(self,amount):
        self.health -= amount

    def is_dead(self):
        return self.health <= 0

    
    def update(self, player):
        now = pygame.time.get_ticks()

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        attack_range = 40 
        attack_cooldown = 500

        if self.attack_rect and now - self.last_attack_time > self.attack_duration:
            self.attack_rect = None

        if distance > attack_range:
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed

            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed

        else:
            if now - self.last_attack_time > attack_cooldown:
                self.attack_rect = self.attack(player)
                self.last_attack_time = now

    def get_facing_direction(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                return "right"
            else:
                return "left"
        else:
            if dy > 0:
                return "down"
            else:
                return "up"

    
    
    def attack(self, player):
        direction = self.get_facing_direction(player)

        attack_size = 24 
        attack_length = 28 
        attack_rect = None

        if direction == "right":
            attack_rect = pygame.Rect(
                self.rect.right,
                self.rect.centery - attack_size // 2,
                attack_length,
                attack_size
            )

        elif direction == "left":
            attack_rect = pygame.Rect(
                self.rect.left - attack_length,
                self.rect.centery - attack_size // 2,
                attack_length,
                attack_size
            )

        elif direction == "down":
            attack_rect = pygame.Rect(
                self.rect.centerx - attack_size // 2,
                self.rect.bottom,
                attack_size,
                attack_length
            )

        elif direction == "up":
            attack_rect = pygame.Rect(
                self.rect.centerx - attack_size // 2,
                self.rect.top - attack_length,
                attack_size,
                attack_length
            )

        return attack_rect


    def draw(self, screen, camera_x, camera_y):
        rect_on_screen = self.rect.move(-camera_x, -camera_y)
        pygame.draw.rect(screen, self.color, rect_on_screen)

        bar_width = self.rect.width
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

    
