import pygame

class Enemy:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,32,32)
        self.health = 50
        self.max_health = 50
        self.speed = 1
        self.color = (200,50,50)

    def take_damage(self,amount):
        self.health -= amount

    def is_dead(self):
        return self.health <= 0

    def update(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

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

    
