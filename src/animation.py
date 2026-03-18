from os import walk
import pygame

class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, name, sprite_type="player", npc_col = 0):
        super().__init__()

        self.frame_size = 32
        self.frames_per_anim = 3

        self.animation_index = 0
        self.clock = 0
        self.speed = 2
        self.action = "idle"
        self.direction = "down"


        self.animation_priority = {
            "idle": 0,
            "run": 0,
            "attack": 1,
            "hurt": 2,
            "death": 3
        }


        if sprite_type == "slime":
            self.slime_animation()
        elif sprite_type == "goblin":
            self.goblin_animation()
        elif sprite_type == "npc":
            self.sprite_sheet = pygame.image.load(
                f"assets/sprites/NPCS.png"
            ).convert_alpha()
            self.npc_animation(npc_col)

        elif sprite_type == "boss":
            self.sprite_sheet = pygame.image.load(
                f"assets/sprites/boss.png"
            ).convert_alpha()
            self.load_boss_style()

        else:
            self.sprite_sheet = pygame.image.load(
                f"assets/sprites/{name}.png"
            ).convert_alpha()
            self.load_player_style()

        self.image = self.images[self.action][self.direction][0]

    def npc_animation(self, npc_col=0):
        self.frame_size = 16
        self.frames_per_anim = 3

        char_col = npc_col % 2
        char_row = npc_col // 2

        # local variables, not stored on self
        x_offset = char_col * 3 * self.frame_size
        y_offset = char_row * 4 * self.frame_size

        def get_npc_image(frame_index, local_row):
            x = x_offset + frame_index * self.frame_size
            y = y_offset + local_row * self.frame_size
            image = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
            image.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_size, self.frame_size))
            return image

        def get_npc_images(local_row):
            return [get_npc_image(i, local_row) for i in range(self.frames_per_anim)]

        self.images = {
            "idle": {
                "down":  get_npc_images(0),
                "left":  get_npc_images(1),
                "right": get_npc_images(2),
                "up":    get_npc_images(3),
            },
            "run": {
                "down":  get_npc_images(0),
                "left":  get_npc_images(1),
                "right": get_npc_images(2),
                "up":    get_npc_images(3),
            },
            "attack": {
                "down":  get_npc_images(0),
                "left":  get_npc_images(1),
                "right": get_npc_images(2),
                "up":    get_npc_images(3),
            },
        }

    def get_npc_images(self, y):
        """Slice 3 frames from the correct NPC column at row y."""
        return [self.get_npc_image(i, y) for i in range(self.frames_per_anim)]


    def get_npc_image(self, frame_index, y):
        x = self.npc_col_offset + frame_index * self.frame_size
        image = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_size, self.frame_size))
        return image

    def slime_animation(self):
        self.frame_size = 64

        walk = pygame.image.load("assets/sprites/Slime/Blue-Slime/walk.png").convert_alpha()
        attack = pygame.image.load("assets/sprites/Slime/Blue-Slime/attack.png").convert_alpha()
        idle = pygame.image.load("assets/sprites/Slime/Blue-Slime/idle.png").convert_alpha()
        hurt = pygame.image.load("assets/sprites/Slime/Blue-Slime/hurt.png").convert_alpha()
        death = pygame.image.load("assets/sprites/Slime/Blue-Slime/death.png").convert_alpha()

        self.images = {
            "idle": {"down": self.slice_sheet(idle)},
            "run": {"down": self.slice_sheet(walk)},
            "attack": {"down": self.slice_sheet(attack)},
            "hurt": {"down": self.slice_sheet(hurt)},
            "death": {"down": self.slice_sheet(death)}
        }

        for action in self.images:
            frames = self.images[action]["down"]
            self.images[action]["up"] = frames
            self.images[action]["left"] = [
                pygame.transform.flip(img, True, False) for img in frames
            ]
            self.images[action]["right"] = frames






    def goblin_animation(self):
        self.frame_size = 64

        walk = pygame.image.load("assets/sprites/Goblin/walk.png").convert_alpha()
        attack = pygame.image.load("assets/sprites/Goblin/attack.png").convert_alpha()
        idle = pygame.image.load("assets/sprites/Goblin/idle.png").convert_alpha()
        hurt = pygame.image.load("assets/sprites/Goblin/hurt.png").convert_alpha()
        death = pygame.image.load("assets/sprites/Goblin/death.png").convert_alpha()

        self.images = {
            "idle": {"right": self.slice_sheet(idle)},
            "run": {"right": self.slice_sheet(walk)},
            "attack": {"right": self.slice_sheet(attack)},
            "hurt": {"right": self.slice_sheet(hurt)},
            "death": {"right": self.slice_sheet(death)}
        }

        for action in self.images:
            right_frames = self.images[action]["right"]

            self.images[action]["left"] = [
                pygame.transform.flip(img, True, False) for img in right_frames
            ]

            self.images[action]["up"] = right_frames
            self.images[action]["down"] = right_frames






    def slice_sheet(self, sheet):
        frames = []

        frame_height = sheet.get_height()
        frame_width = frame_height   # assumes square frames

        num_frames = sheet.get_width() // frame_width

        for i in range(num_frames):
            image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frames.append(image)

        return frames



    def change_animation(self, action, direction):
        if self.animation_priority[action] >= self.animation_priority[self.action]:
            if action != self.action:
                self.action = action
                self.animation_index = 0
                self.clock = 0

        self.direction = direction
        frames = self.images[self.action][self.direction]
        anim_speed = getattr(self, "animation_speed", self.speed)  # ← use animation_speed if set
        self.clock += anim_speed * 8
        if self.clock >= 100:
            self.animation_index += 1
            self.clock = 0

            if self.animation_index >= len(frames):
                if self.action in ("attack", "death","hurt"):  # ← add death here
                    self.animation_index = len(frames) - 1
                else:
                    self.animation_index = 0

        self.animation_index = min(self.animation_index, len(frames) - 1)
        self.image = frames[self.animation_index]

    def get_images(self, y):
        return [self.get_image(i * self.frame_size, y) for i in range(self.frames_per_anim)]

    def get_image(self, x, y):
        image = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_size, self.frame_size))
        return image

    def load_player_style(self):
        self.images = {
            "idle": {
                "down":  self.get_images(0),
                "right": self.get_images(32),
                "up":    self.get_images(64)
            },
            "run": {
                "down":  self.get_images(96),
                "right": self.get_images(128),
                "up":    self.get_images(160)
            },
            "attack": {
                "down":  self.get_images(192),
                "right": self.get_images(224),
                "up":    self.get_images(256)
            },
            "death": {
                "down":  self.get_images(288),
                "right": self.get_images(320),
                "up":    self.get_images(352)
                }
            }
        for action in ["idle", "run", "attack", "death"]:
            self.images[action]["left"] = [
                pygame.transform.flip(img, True, False)
                for img in self.images[action]["right"]
            ]

    def load_boss_style(self):
        self.frame_size= 80
        self.frames_per_anim= 8
        FRAME_W = 80
        FRAME_H = 80

        self.images = {
            "idle": {
                "down": self.get_images(0 * FRAME_H),
                "right": self.get_images(0 * FRAME_H),
                "up": self.get_images(0 * FRAME_H)
                
            },
            "run": {
                "down": self.get_images(0 * FRAME_H),
                "right": self.get_images(0 * FRAME_H),
                "up": self.get_images(0 * FRAME_H)
            },
            "attack": {
                "down": self.get_images(1 * FRAME_H),
                "right": self.get_images(1 * FRAME_H),
                "up": self.get_images(1 * FRAME_H)

            },  
            "death": {
                "down": self.get_images(3 * FRAME_H),
                "right": self.get_images(3 * FRAME_H),
                "up": self.get_images(3 * FRAME_H)

            }

        }
            # Switch frame count BEFORE slicing the hurt row
        self.frames_per_anim = 2
        self.images["hurt"] = {
                "down":  self.get_images(2 * FRAME_H),
                "right": self.get_images(2 * FRAME_H),
                "up":    self.get_images(2 * FRAME_H),
            }
        self.frames_per_anim = 8  # restore for anything else
        for action in ["idle", "run", "attack","hurt","death"]:
            if self.action == "hurt":
                self.frames_per_anim =2
            self.images[action]["left"] = [
                pygame.transform.flip(img, True, False)
                for img in self.images[action]["right"]
            ]
        

class HeartDisplay:
    def __init__(self, player, heart_path="assets/sprites/hearts/heartDisplay.png", heart_value=20):
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


