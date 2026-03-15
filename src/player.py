import pygame
from animation import AnimateSprite
from données import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR
from projectile import Projectile
class Entity(AnimateSprite):
    def __init__(self, name, x, y):
        super().__init__(name)

        # Position and old position
        self.position = [x, y]
        self.old_position = self.position.copy()

        # Animation state
        self.direction = "down"      # string for animation keys
        self.action = "idle"         # "idle", "run", "attack"

        # Movement vector for collisions
        self.move_vector = (0, 0)    # dx, dy

        # Initialize sprite image and rect
        self.image = self.images[self.action][self.direction][0]
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    def save_location(self):
        self.old_position = self.position.copy()

    # Movement methods
    def move_right(self):
        self.direction = "right"
        self.action = "run"
        self.position[0] += self.speed
        self.move_vector = (1, 0)

    def move_left(self):
        self.direction = "left"
        self.action = "run"
        self.position[0] -= self.speed
        self.move_vector = (-1, 0)

    def move_up(self):
        self.direction = "up"
        self.action = "run"
        self.position[1] -= self.speed
        self.move_vector = (0, -1)

    def move_down(self):
        self.direction = "down"
        self.action = "run"
        self.position[1] += self.speed
        self.move_vector = (0, 1)

    # Stop moving (idle)
    def stop(self):
        self.direction = self.direction
        self.action = "idle"
        self.move_vector = (0, 0)

    # Attack animation
    def attack(self):
        self.action = "attack"
        self.direction = self.direction
        self.animation_index = 0
        self.move_vector = (0, 0)  # usually stop movement when attacking

    # Move back to previous position (collision)
    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = tuple(self.position)     
        self.feet.midbottom = self.rect.midbottom 

    # Update animation and position
    def update(self):
        # Update animation based on current action and direction
        self.change_animation(self.action, self.direction)

        # Update rect and feet for collisions
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom    
    

class Player(Entity):
    def __init__(self, name, x, y):
        super().__init__("Player", x, y)

        # Stats
        self.health = 100
        self.max_health = 100

        # Melee
        self.melee_damage = 30
        self.melee_cooldown = 500  # milliseconds
        self.melee_duration = 100
        self.last_melee_time = 0

        # Ranged
        self.ranged_damage = 10
        self.ranged_cooldown = 300
        self.last_ranged_time = 0

    # Health
    def take_dmg(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_dead(self):
        return self.health <= 0

    def melee_attack(self):
        """Start a melee attack in the direction the player is facing."""
        now = pygame.time.get_ticks()
        if now - self.last_melee_time < self.melee_cooldown or self.direction == (0,0):
            return None

        self.last_melee_time = now
        self.action = "attack"  # trigger attack animation

        # Determine attack target rectangle based on facing
        attack_range = 40  # distance in pixels for melee
        px, py = self.rect.center
        dx, dy = self.move_vector

        # Create a small rect in the facing direction
        attack_rect = pygame.Rect(px, py, self.rect.width, self.rect.height)

        if dx > 0:  # right
            attack_rect = pygame.Rect(self.rect.right, self.rect.top, attack_range, self.rect.height)
        elif dx < 0:  # left
            attack_rect = pygame.Rect(self.rect.left - attack_range, self.rect.top, attack_range, self.rect.height)
        elif dy > 0:  # down
            attack_rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, attack_range)
        elif dy < 0:  # up
            attack_rect = pygame.Rect(self.rect.left, self.rect.top - attack_range, self.rect.width, attack_range)
        else:
            attack_rect = pygame.Rect(self.rect.topleft, (self.rect.width, self.rect.height))

        # Save rect to apply damage in Game.update
        self.current_attack_rect = attack_rect
        return attack_rect

    def update(self):
        super().update()  # AnimateSprite update

        if self.action == "attack":
            if self.clock >= 100:  # when animation ends
                if self.move_vector != (0,0):
                    self.action = "run"
                else:
                    self.action = "idle"
    # Ranged attack
    def ranged_attack(self):
        now = pygame.time.get_ticks()

        if now - self.last_ranged_time < self.ranged_cooldown or self.move_vector == (0, 0):
            return None

        self.last_ranged_time = now
        dx, dy = self.move_vector

        return Projectile(
            self.rect.centerx,
            self.rect.centery,
            5,  # speed
            (255, 255, 0),  # color
            dx,
            dy
        )

class NPC(Entity):
    def __init__(self, name, nb_points, dialog):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.speed = 1
        self.current_point = 0



    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()
        if current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point


    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0]= location.x
        self.position[1]= location.y
        self.save_location()

    def load_points(self, tmx_data):
        # Find the object group first
        group = None
        for obj_group in tmx_data.objectgroups:
            if obj_group.name == "NPCPaths":
                group = obj_group
                break

        if group is None:
            print(f"[ERROR] NPCPaths group not found in Tiled map")
            return

        # Search for path objects inside this group
        for num in range(1, self.nb_points + 1):
            point_name = f"{self.name}_path{num}"
            point = None
            for obj in group:
                if obj.name == point_name:
                    point = obj
                    break

            if point is None:
                print(f"[ERROR] No point found in NPCPaths: {point_name}")
                continue

            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
            print(f"[LOADED] {point_name} -> ({point.x}, {point.y})")

        print(f"{self.name} points after load: {self.points}")
               
