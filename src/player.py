import pygame
from animation import AnimateSprite
from données import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR
from projectile import Projectile
class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)

        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        

    def get(self):
        self.image = self.images["down"]
        self.image.set_colorkey([0, 0, 0])
        return self.image

    def save_location(self): self.old_position = self.position.copy()

    

    def move_right(self): 
        self.change_animation("right")
        self.position[0] += self.speed
        self.direction = (1,0)

    def move_left(self): 
        self.change_animation("left")
        self.position[0] -= self.speed
        self.direction = (-1,0)

    def move_up(self):
        self.change_animation("up") 
        self.position[1] -= self.speed
        self.direction = (0,-1)

    def move_down(self): 
        self.change_animation("down")
        self.position[1] += self.speed
        self.direction = (0,1)

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()

    
    

class Player(Entity):
    def __init__(self, name, x, y):
        super().__init__("player", 0, 0)
        self.health = 100
        self.max_health = 100
        self.melee_damage = 20
        self.melee_cooldown = 500
        self.last_melee_time = 0
        self.ranged_damage = 10
        self.ranged_cooldown = 300
        self.last_ranged_time = 0
        self.direction = (0,0)



    def take_dmg(self, amount):
        self.health -= amount

    def is_dead(self):
       return self.health <= 0
    
    def melee_attack(self):
        now = pygame.time.get_ticks()

        if now - self.last_melee_time >= self.melee_cooldown and self.direction[0] != 0:
            self.last_melee_time = now 

            attack_rect = self.rect.inflate(50,0)


            attack_rect.x += self.direction[0] * PLAYER_SIZE
            attack_rect.y += self.direction[1] * PLAYER_SIZE

            return attack_rect
        elif now - self.last_melee_time >= self.melee_cooldown and self.direction[1] != 0:
            self.last_melee_time = now 
            attack_rect = self.rect.inflate(0,50)


            attack_rect.x += self.direction[0] * PLAYER_SIZE
            attack_rect.y += self.direction[1] * PLAYER_SIZE

            return attack_rect

    def ranged_attack(self):
        now = pygame.time.get_ticks()

        if now - self.last_ranged_time >= self.ranged_cooldown:
            if self.direction != (0,0):
                    self.last_ranged_time = now

            return Projectile(
                self.rect.centerx,
                self.rect.centery,
                5,
                (255, 255, 0),
                self.direction[0],
                self.direction[1]
                            )
        return None


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
        for num in range (1, self.nb_points+1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)