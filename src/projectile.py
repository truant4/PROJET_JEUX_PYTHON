import pygame

class Projectile(object):
    def __init__(self, x, y, radius, color, dir_x, dir_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 8

        self.vel_x = dir_x * self.speed
        self.vel_y = dir_y * self.speed

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, win, camera_x=0, camera_y=0):
        pygame.draw.circle(
        win,
        self.color,
        (int(self.x - camera_x), int(self.y - camera_y)),
        self.radius
    )
    
    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def off_screen(self, width, height):
        return not (0 <= self.x <= width and 0 <= self.y <= height)
