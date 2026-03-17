import pygame
from animation import AnimateSprite
from player import NPC
from projectile import Projectile


class Enemy(NPC):
    def __init__(self, name, player, nb_points=0, dialog=[],
                 detection_range=100, speed=0.2, health=100,
                 damage=20, attack_range=25, attack_cooldown=800,
                 enemy_type="slime"):

        super().__init__(name, nb_points=nb_points, dialog=dialog, sprite_type=enemy_type)

        self.player = player

        # Stats
        self.health = health
        self.max_health = health
        self.damage = damage
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0
        self.attacking = False
        self.attacking_timer = 0

        # Movement & AI
        self.detection_range = detection_range
        self.awake = False
        self.speed = speed
        self.attack_timer = 0

        # Animation
        self.action = "idle"
        self.direction = "down"

        # Knockback
        self.knockback_vector = (0, 0)
        self.knockback_timer = 0
        self.knockback_duration = 300
        self.can_attack = True
        self.pending_player_knockback = None

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.3)

    # --- Health ---

    def take_damage(self, amount):
        if self.action == "death":
            return

        self.health -= amount

        if self.health <= 0:
            self.health = 0
            self.action = "death"
            self.animation_index = 0
        else:
            # Interrupt attack windup if hit
            if self.attacking:
                self.attacking = False
                self.attacking_timer = 0
                self.attack_timer = 0

            self.action = "hurt"
            self.animation_index = 0

    def is_dead(self):
        return self.health <= 0

    # --- Update per frame ---

    def update(self):
        if self.action == "death":
            frames = self.images["death"][self.direction]
            self.change_animation("death", self.direction)
            
            # Once last frame is reached, remove the sprite
            if self.animation_index >= len(frames) - 1:
                self.kill()
            
            self.rect.topleft = tuple(self.position)
            self.feet.midbottom = self.rect.midbottom
            return

        # Lock enemy during attack windup
        if self.attacking:
            self.attacking_timer -= self.game_clock.get_time()
            self.move_vector = (0, 0)

            if self.attacking_timer <= 0:
                self.perform_attack()  # deal damage at end of windup
                self.attacking = False
                self.action = "idle"
                self.animation_index = 0
            else:
                self.action = "attack"

            self.change_animation(self.action, self.direction)
            self.rect.topleft = tuple(self.position)
            self.feet.midbottom = self.rect.midbottom
            return

        # Handle knockback
        if self.knockback_timer > 0:
            self.position[0] += self.knockback_vector[0]
            self.position[1] += self.knockback_vector[1]

            self.knockback_timer -= self.game_clock.get_time()
            if self.knockback_timer <= 0:
                self.knockback_vector = (0, 0)
                self.knockback_timer = 0
                self.can_attack = True

            self.change_animation(self.action, self.direction)
            self.rect.topleft = tuple(self.position)
            self.feet.midbottom = self.rect.midbottom
            return

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

        if self.awake:
            if distance > self.attack_range:
                # Chase player
                self.move_toward(self.player.rect.centerx, self.player.rect.centery)
                if self.action != "run":
                    self.action = "run"
                self.attack_timer = 0

            else:
                # Player in range → start attack windup if cooldown allows
                self.move_vector = (0, 0)

                if self.action != "attack":
                    now = pygame.time.get_ticks()
                    if now - self.last_attack_time >= self.attack_cooldown:
                        self.action = "attack"
                        self.animation_index = 0
                        self.attacking = True
                        self.attacking_timer = self.attack_windup

        else:
            # Patrol logic
            if self.nb_points > 0:
                patrol_point = self.points[self.current_point].center
                self.move_toward(*patrol_point)
                self.action = "run"

                if abs(self.rect.centerx - patrol_point[0]) <= self.speed and \
                   abs(self.rect.centery - patrol_point[1]) <= self.speed:
                   self.current_point = (self.current_point + 1) % self.nb_points      
            else:
                self.action = "idle"

        # Update animation and rect
        self.change_animation(self.action, self.direction)
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom

    # --- Direction helper ---

    def get_facing_direction(self, dx, dy):
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        else:
            return "down" if dy > 0 else "up"

    # --- Movement ---

    def move_toward(self, target_x, target_y):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        self.direction = self.get_facing_direction(dx, dy)

        step_x = min(self.speed, abs(dx)) * (1 if dx > 0 else -1) if dx != 0 else 0
        step_y = min(self.speed, abs(dy)) * (1 if dy > 0 else -1) if dy != 0 else 0
        self.save_location()


  
        self.position[0] += step_x
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom
        if self.feet.collidelist(self.walls) > -1:
            # Reculer pixel par pixel jusqu'à sortir du wall
            while self.feet.collidelist(self.walls) > -1:
                self.position[0] -= (1 if step_x > 0 else -1)
                self.rect.topleft = tuple(self.position)
                self.feet.midbottom = self.rect.midbottom


        self.position[1] += step_y
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom
        if self.feet.collidelist(self.walls) > -1:
            while self.feet.collidelist(self.walls) > -1:
                self.position[1] -= (1 if step_y > 0 else -1)
                self.rect.topleft = tuple(self.position)
                self.feet.midbottom = self.rect.midbottom

        # Update position

        # self.rect.topleft = tuple(self.position)
        # self.feet.midbottom = self.rect.midbottom
        # if self.feet.collidelist(self.walls) > -1:
        #     self.move_back()
        #     step_y = 0

        # Set move_vector for attacks and collisions

    # --- Attack ---

    def perform_attack(self):
        """Deal damage to player at the end of windup."""
        dx = abs(self.player.rect.centerx - self.rect.centerx)
        dy = abs(self.player.rect.centery - self.rect.centery)

        if dx + dy <= self.attack_range:
            self.player.take_dmg(self.damage, self.rect.center)
            self.last_attack_time = pygame.time.get_ticks()


class Slime(Enemy):

    def __init__(self, name, player, nb_points=0):
        super().__init__(
            name,
            player,
            nb_points=nb_points,
            enemy_type="slime",
            health=100,
            damage=10,
            speed=0.5,
            detection_range=120,
            attack_range=20,
            attack_cooldown=500
        )
        self.attack_windup = 4000


class Goblin(Enemy):

    def __init__(self, name, player, nb_points=0):
        super().__init__(
            name,
            player,
            nb_points=nb_points,
            enemy_type="goblin",
            health=100,
            damage=20,
            speed=0.7,
            detection_range=180,
            attack_range=25,
            attack_cooldown=600
        )
        self.attack_windup = 2350

