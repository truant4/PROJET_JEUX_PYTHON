import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"assets/sprites/{name}.png").convert_alpha()

        self.animation_index = 0
        self.clock = 0
        self.speed = 2

        self.frame_size = 32
        self.frames_per_anim = 3

        # Load all animations
        self.images = {
            "idle": {
                "down": self.get_images(0),
                "right": self.get_images(32),
                "up": self.get_images(64)
            },
            "run": {
                "down": self.get_images(96),
                "right": self.get_images(128),
                "up": self.get_images(160)
            },
            "attack": {
                "down": self.get_images(192),
                "right": self.get_images(224),
                "up": self.get_images(256)
            }
        }

        for action in ["idle", "run", "attack"]:
            self.images[action]["left"] = [pygame.transform.flip(img, True, False) for img in self.images[action]["right"]]

        self.image = self.images["idle"]["down"][0]

    def change_animation(self, action, direction):
        frames = self.images[action][direction]
        self.image = frames[self.animation_index]

        self.clock += self.speed * 8
        if self.clock >= 100:
            self.animation_index += 1
            if self.animation_index >= len(frames):
                self.animation_index = 0
            self.clock = 0

    def get_images(self, y):
        return [self.get_image(i * self.frame_size, y) for i in range(self.frames_per_anim)]

    def get_image(self, x, y):
        image = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_size, self.frame_size))
        return image

class HeartDisplay:
    def __init__(self, player, heart_path="assets/sprites/hearts/heartDisplay.png", heart_value=10):
        self.player = player
        self.heart_value = heart_value
        self.heart_image = pygame.image.load(heart_path)
        self.heart_width = self.heart_image.get_width()
        self.spacing = 45 # space between hearts

    def draw(self, screen):
        total_hearts = self.player.max_health // self.heart_value
        current_health = self.player.health
        
        for i in range(total_hearts):
            x = 10 + i * (32 + self.spacing)
            y = 10
            
            if current_health >= self.heart_value:
                heart_index = 0  # full heart
            elif current_health > 0:
                heart_index = 2  # half heart
            else:
                heart_index = 1  # empty heart
            
            heart_image = self.get_heart_image(heart_index)
            screen.blit(heart_image, (x, y))
            
            current_health -= self.heart_value

    def get_heart_image(self, index):
        """
        index: 0 = full, 1 = empty, 2 = half
        """
        image = pygame.Surface((96, 96), pygame.SRCALPHA)  # transparent surface
        image.blit(self.heart_image, (0, 0), (index * 96, 0, 96, 96))
        return image


