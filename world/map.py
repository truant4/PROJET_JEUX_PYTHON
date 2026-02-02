import os
import xml.etree.ElementTree as ET
import pygame
from pytmx.util_pygame import load_pygame

class TiledMap:
    def __init__(self, tmx_path):  # <-- AJOUTE ÇA
        self.tmx = load_pygame(tmx_path)
        self.tmx = load_pygame(tmx_path)

        self.tile_w = self.tmx.tilewidth
        self.tile_h = self.tmx.tileheight
        self.width_tiles = self.tmx.width
        self.height_tiles = self.tmx.height
        self.width_px = self.width_tiles * self.tile_w
        self.height_px = self.height_tiles * self.tile_h

        self._render_cache = None

    def build_cache(self):
        surface = pygame.Surface((self.width_px, self.height_px), pygame.SRCALPHA)

        for layer in self.tmx.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    if image:
                        surface.blit(image, (x * self.tile_w, y * self.tile_h))

        self._render_cache = surface

    def draw(self, screen, camera_x, camera_y):
        if self._render_cache is None:
            self.build_cache()
        screen.blit(self._render_cache, (-camera_x, -camera_y))
