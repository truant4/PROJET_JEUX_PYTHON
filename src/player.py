import pygame
from animation import AnimateSprite
from données import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR
from projectile import Projectile
class Entity(AnimateSprite):
    def __init__(self, name, x, y,sprite_type="player",npc_col=0):
        super().__init__(name,sprite_type,npc_col)

        
        self.position = [x, y]
        self.old_position = self.position.copy()



        
        self.action = "idle"         

        
        self.move_vector = (0, 0)    

        
        self.image = self.images[self.action][self.direction][0]
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    def save_location(self):
        self.old_position = self.position.copy()

    
    def move_right(self):
        self.direction = "right"
        self.position[0] += self.speed
        self.move_vector = (1, 0)

    def move_left(self):
        self.direction = "left"
        self.position[0] -= self.speed
        self.move_vector = (-1, 0)

    def move_up(self):
        self.direction = "up"
        self.position[1] -= self.speed
        self.move_vector = (0, -1)

    def move_down(self):
        self.direction = "down"
        self.position[1] += self.speed
        self.move_vector = (0, 1)

    
    def stop(self):
        self.direction = self.direction
        self.move_vector = (0, 0)

    
    def attack(self):
        self.direction = self.direction
        self.animation_index = 0
        self.move_vector = (0, 0)  

    
    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = tuple(self.position)     
        self.feet.midbottom = self.rect.midbottom 

    
    def update(self):
        
        self.change_animation(self.action, self.direction)

        
        self.rect.topleft = tuple(self.position)
        self.feet.midbottom = self.rect.midbottom    
    

class Player(Entity):
    def __init__(self, name, x, y):
        super().__init__("Player", x, y)
        self.animation_speed = 0.5  
        self.knockback_vector = [0, 0]
        self.knockback_timer = 0
        self.knockback_duration = 200  
        self.knockback_speed = 4

        
        self.health = 100
        self.max_health = 100

        
        self.melee_damage = 20
        self.melee_cooldown = 500  
        self.melee_duration = 100
        self.last_melee_time = 0

        
        self.ranged_damage = 10
        self.ranged_cooldown = 300
        self.last_ranged_time = 0

    
    def take_dmg(self, amount, source_pos=None):
        self.health -= amount
        if self.health < 0:
            self.health = 0

        
        if source_pos:
            px, py = self.rect.center
            sx, sy = source_pos

            dx = px - sx
            dy = py - sy

            length = max((dx**2 + dy**2) ** 0.5, 0.001)

            self.knockback_vector[0] = (dx / length) * self.knockback_speed
            self.knockback_vector[1] = (dy / length) * self.knockback_speed
            self.knockback_timer = self.knockback_duration
    def is_dead(self):
        return self.health <= 0

    def melee_attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_melee_time < self.melee_cooldown or self.direction == (0, 0):
            return None

        self.last_melee_time = now
        self.action = "attack"
        self.animation_index = 0

        reach = 10  
        width = 20  

        cx = self.feet.centerx
        cy = self.feet.centery

        if self.direction == "right":
            attack_rect = pygame.Rect(
                self.feet.right,
                self.feet.top,
                reach + self.feet.width,  
                self.feet.height * 1.5
            )
        elif self.direction == "left":
            attack_rect = pygame.Rect(
                self.feet.left - reach,
                self.feet.top,
                reach + self.feet.width,
                self.feet.height * 1.5
            )
        elif self.direction == "down":
            attack_rect = pygame.Rect(
                cx - width // 2,
                self.feet.bottom,
                width,
                reach + self.feet.height
            )
        elif self.direction == "up":
            attack_rect = pygame.Rect(
                cx - width // 2,
                self.feet.top - reach,
                width,
                reach + self.feet.height
            )
        else:
            attack_rect = pygame.Rect(cx, cy, width, reach)

        self.current_attack_rect = attack_rect
        return attack_rect
    def update(self):
        if self.action == "death":
            super().update()
            return
        
        if self.knockback_timer > 0:
            self.position[0] += self.knockback_vector[0]
            self.position[1] += self.knockback_vector[1]

            
            self.knockback_timer -= self.game_clock.get_time()

            if self.knockback_timer <= 0:
                self.knockback_timer = 0
                self.knockback_vector = [0, 0]

            super().update()
            return
        if self.action == "attack":
            self.change_animation("attack", self.direction)

            if self.animation_index == self.frames_per_anim - 1:
                if self.move_vector != (0,0):
                    self.action = "run"
                else:
                    self.action = "idle"

        else:
            if self.move_vector != (0,0):
                self.change_animation("run", self.direction)
            else:
                self.change_animation("idle", self.direction)

        super().update()

class NPC(Entity):
    def __init__(self, name, nb_points, dialog,sprite_type="npc",npc_col=0,expressions = []):
        super().__init__(name, 0, 0,sprite_type,npc_col)
        self.npc_col = npc_col
        self.expressions = expressions
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
        
        group = None
        for obj_group in tmx_data.objectgroups:
            if obj_group.name == "NPCPaths":
                group = obj_group
                break

        if group is None:
            print(f"[ERROR] NPCPaths group not found in Tiled map")
            return

        
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
               
