from dataclasses import dataclass
import pygame, pytmx, pyscroll
import dialog
from player import *
from enemy import *
from items import HealingItem

@dataclass
class Portals():
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str
from enemy import Enemy, Goblin, Slime

@dataclass
class Map:
    name : str
    walls : list[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    npcs: list[NPC]
    enemies: list
    items: list
    portals : list[Portals]

class MapManager():
     
    def __init__(self, screen, player,clock):
          self.maps = dict()
          self.screen = screen
          self.player = player
          self.clock = clock
          self.current_map = "map"
          self.enemies = []
          self.register_map("map", npcs=[
            NPC("paul", nb_points = 4, dialog=["Salut", "bien", "au revoir"],npc_col=0),
            NPC("robin", nb_points= 2, dialog=["coucou", "cool", "au revoir"],npc_col=1),
            ],
            enemies=[
            Slime("slime1",self.player,nb_points=2),
            Slime("slime2",self.player,nb_points=2),
            Goblin("goblin1",self.player,nb_points=2),
            Boss("boss", self.player, nb_points=1)
        ],
            portals=[
                Portals(from_world="map", origin_point="enter_house1", target_world="house1", teleport_point="spawn_house1"),
                Portals(from_world="map", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house2"),
                Portals(from_world="map", origin_point="enter_dungeon", target_world="dungeon", teleport_point="spawn_dungeon"),
                Portals(from_world="map", origin_point="enter_house3", target_world="house3", teleport_point="spawn_house3")
        ])
        self.register_map("house1", portals=[
            Portals(from_world="house1", origin_point="enter_room1", target_world="house1_room1", teleport_point="spawn_room1_house1" ),
            Portals(from_world="house1", origin_point="exit_house1", target_world="map", teleport_point="enter_exit_house1" )
        ])
        self.register_map("house1_room1", portals=[
            Portals(from_world="house1_room1", origin_point="exit_room1_house1", target_world="house1", teleport_point="enter_exit_room1_house1" )
        ])
        self.register_map("house2", portals=[
            Portals(from_world="house2", origin_point="exit_house2", target_world="map", teleport_point="enter_exit_house2" )
        ])
        self.register_map("house3", portals=[
            Portals(from_world="house3", origin_point="exit_house3", target_world="map", teleport_point="enter_exit_house3" )
        ])
        self.register_map("dungeon")

        self.teleportation_player("player")
        self.teleport_npcs()
        # self.teleport_enem

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC and sprite.feet.colliderect(self.player.rect):
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleportation_player(copy_portal.teleport_point)


        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else :
                    sprite.speed = 1
                    
        # Walls pour le player uniquement
        if self.player.feet.collidelist(self.get_walls()) > -1:
            self.player.move_back()

        # Walls pour les NPCs uniquement
        for npc in self.get_map().npcs:
            if npc.feet.collidelist(self.get_walls()) > -1:
                npc.move_back()

        for npc in self.get_map().npcs:
            if self.player.feet.colliderect(npc.feet):
                self.player.move_back()

        for item in self.get_map().items:
            if self.player.rect.colliderect(item.rect):
                self.player.health = min(self.player.health + item.amount, self.player.max_health)
                item.kill()
                self.get_map().items.remove(item)
            

    def teleportation_player(self,name):
        point = self.get_object(name)
        self.player.position[0]=point.x
        self.player.position[1]=point.y
        self.player.save_location()

            
    def register_map(self, name, npcs=None, enemies=None, portals=None):
        if npcs is None:
            npcs = []
        if enemies is None:
            enemies = []
        if portals is None:
            portals = []

        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 5

        # Les collisions
        walls = []
        walls_enemy =[]

        tile_height = tmx_data.tileheight

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                ))
                walls_enemy.append(pygame.Rect(
                    obj.x,
                    obj.y + tile_height,
                    obj.width,
                    obj.height
                ))
        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=17)
        group.add(self.player)

        #recuperer tout les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)
        
        for enemy in enemies:
            enemy.game_clock = self.clock
            group.add(enemy)
            enemy.walls = walls_enemy

        items = []
        for obj in tmx_data.objects:
            if obj.type == "healing_item":
                amount = int(obj.properties.get("amount", 10))
                item = HealingItem(obj.x, obj.y, amount)
                items.append(item)
                group.add(item)

    
        self.maps[name] = Map(name, walls, group, tmx_data, npcs,enemies, items, portals)


        self.maps[name] = Map(name, walls, group, tmx_data, npcs,enemies,items,portals)


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
                enemy.teleport_spawn() 

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