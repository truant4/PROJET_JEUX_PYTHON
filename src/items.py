import pygame

class HealingItem(pygame.sprite.Sprite):
    def __init__(self, x, y, amount):
        super().__init__()
        self.amount = amount
        self.image = pygame.image.load("assets/potion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = pygame.Rect (0,0,4,4)
        self.rect.topleft = (x, y)

class HeartReceptacle(HealingItem):  
    def __init__(self, x, y, amount = None):
        super().__init__(x, y, amount = None)
        self.image = pygame.image.load("assets/healing_item.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = pygame.Rect (0,0,4,4)
        self.rect.topleft = (x, y)
