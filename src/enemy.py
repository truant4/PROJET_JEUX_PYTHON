import pygame
from player import NPC  # Assuming NPC inherits from Entity
from projectile import Projectile

class Enemy(NPC):
    def __init__(self, name, player, nb_points=0, dialog=[], detection_range=100,
                 speed=0.5, health=50, damage=5, attack_range=40, attack_cooldown=800):
        super().__init__(name, nb_points=nb_points, dialog=dialog)
        self.player = player

        # Stats
        self.health = health
        self.max_health = health
        self.damage = damage
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0

        # Movement & AI
        self.detection_range = detection_range
        self.awake = False
        self.speed = speed

        # Animation
        self.action = "idle"
        self.direction = "down"

    # Health
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_dead(self):
        return self.health <= 0

    # Update per frame
    def update(self):
        """AI: detect, chase player, patrol, and update animation."""
        # Vector to player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = abs(dx) + abs(dy)
        chase_range = self.detection_range + 50

        # Detection
        if distance <= self.detection_range:
            self.awake = True
        elif distance > chase_range:
            self.awake = False

        # Reset movement vector
        self.move_vector = (0, 0)
        self.action = "idle"

        if self.awake:
            if distance > self.attack_range:
                # Move toward player
                self.move_toward(self.player.rect.centerx, self.player.rect.centery)
                self.action = "run"
            else:
                # Attack
                self.attack()
                self.action = "attack"
        else:
            # Patrol logic
            if self.nb_points > 0:
                patrol_point = self.points[self.current_point].center
                self.move_toward(*patrol_point)
                self.action = "run"

                # Check if reached patrol point
                if abs(self.rect.centerx - patrol_point[0]) <= self.speed and \
                   abs(self.rect.centery - patrol_point[1]) <= self.speed:
                    self.current_point = (self.current_point + 1) % self.nb_points
            else:
                # fallback idle
                self.action = "idle"

        # Update animation and rect
        self.change_animation(self.action, self.direction)
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom

    # Determine cardinal direction based on movement vector
    def get_facing_direction(self, dx, dy):
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        else:
            return "down" if dy > 0 else "up"

    # Axis-aligned movement
    def move_toward(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery

        step_x = min(self.speed, abs(dx)) * (1 if dx > 0 else -1) if dx != 0 else 0
        step_y = min(self.speed, abs(dy)) * (1 if dy > 0 else -1) if dy != 0 else 0

        self.save_location()

        # Update position
        self.position[0] += step_x
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom
        if self.feet.collidelist(self.walls) > -1:
            self.move_back()
            step_x = 0


        self.save_location()
        self.position[1] += step_y
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom
        if self.feet.collidelist(self.walls) > -1:
            self.move_back()
            step_y = 0

        # Set move_vector for attacks and collisions
        self.move_vector = (step_x, step_y)

        # Set facing direction for animation
        if step_x != 0 or step_y != 0:
            self.direction = self.get_facing_direction(step_x, step_y)

    # Attack logic
    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time < self.attack_cooldown:
            return

        dx = abs(self.player.rect.centerx - self.rect.centerx)
        dy = abs(self.player.rect.centery - self.rect.centery)
        if dx + dy <= self.attack_range:
            self.player.take_dmg(self.damage)
            self.last_attack_time = now
