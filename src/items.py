import pygame

class HealingItem(pygame.sprite.Sprite):
    def __init__(self, x, y, amount):
        super().__init__()
        self.amount = amount
        self.image = pygame.image.load("assets/healing_item.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class HeartReceptacle(pygame.sprite.Sprite):  
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/potion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)