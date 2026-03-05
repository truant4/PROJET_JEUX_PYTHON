from dataclasses import dataclass
import pygame, pytmx, pyscroll
import dialog
from player import *
from enemy import Enemy

@dataclass
class Map:
    name : str
    walls : list[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    npcs: list[NPC]
    enemies: list

class MapManager:
     
    def __init__(self, screen, player):
          self.maps = dict()
          self.screen = screen
          self.player = player
          self.current_map = "map"
          self.enemies = []
          self.register_map("map", npcs=[
              NPC("paul", nb_points = 4, dialog=["Salut", "bien", "au revoir"]),
              NPC("robin", nb_points= 2, dialog=["coucou", "cool", "au revoir"]),
              ],
              enemies=[
                Enemy("boss1",self.player,nb_points=2),
                Enemy("boss2",self.player,nb_points=2)
            ])

          
          self.teleportation_player("player")
          self.teleport_npcs()
          # self.teleport_enemies()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else :
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls())> -1:
                sprite.move_back()

    def teleportation_player(self,name):
        point = self.get_object(name)
        self.player.position[0]=point.x
        self.player.position[1]=point.y
        self.player.save_location()

            
    def register_map(self, name, npcs=[], enemies=[]):
        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=10)
        group.add(self.player)

        #recuperer tout les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)
        
        for enemy in enemies:
            group.add(enemy)

        #creer un objet ma 
        self.maps[name] = Map(name, walls, group, tmx_data, npcs,enemies)


    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map_name, map_data in self.maps.items():
            # First, load points for NPCs and enemies
            for npc in map_data.npcs:
                print(f"Loading points for NPC: {npc.name}")  # Debug
                npc.load_points(map_data.tmx_data)
            
            for enemy in map_data.enemies:
                print(f"Loading points for Enemy: {enemy.name}")  # Debug
                enemy.load_points(map_data.tmx_data)
            
            # Then, teleport them
            for npc in map_data.npcs:
                npc.teleport_spawn()
            for enemy in map_data.enemies:
                enemy.teleport_spawn()  # <- parentheses!

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()
        for enemy in self.get_map().enemies:
            enemy.update()
