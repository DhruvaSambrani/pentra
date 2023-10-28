import json
import os

import pygame
from pygame.math import Vector2
from pygame.transform import average_color

import assets
import player
from inventory import load_item


class Map:
    def __init__(self, folderpath):
        meta = json.load(open(os.path.join(folderpath, "meta.json")))
        map_surf = pygame.image.load(os.path.join(folderpath, "map.png"))
        self.name = meta["name"]
        items_data = meta["items_on_load"]
        self.default_loc = meta["default_loc"]
        self.items = [load_item(elt[0]) for elt in items_data]
        self.item_locs = [Vector2(elt[1]) for elt in items_data]
        self.map_surf = map_surf
        pygame.draw.rect(
            map_surf,
            assets.load_asset("color", "WHITE"),
            pygame.rect.Rect(0, 0, *map_surf.get_size()),
            width=2,
        )

    def check_wall_collision(self, rect):
        return pygame.Color(average_color(self.map_surf, rect)).grayscale()[0] > 10

    def pickup_item(self, pos):
        for i in range(len(self.items)):
            if (pos - self.item_locs[i]).magnitude() <= 35:
                item, _ = self.items.pop(i), self.item_locs.pop(i)
                return item
        return None

    def place_item(self, item, pos):
        self.items.append(item)
        self.item_locs.append(pos)

    def render(self, disp_surface, viewport):
        temp_surface = self.map_surf.copy()
        for i in range(len(self.items)):
            self.items[i].render(temp_surface, self.item_locs[i])
        player.get_player().render(temp_surface)
        disp_surface.blit(temp_surface, (0, 0), viewport)


def load_maps():
    maps = []
    for file in assets.list_assets("map"):
        maps.append(assets.load_asset("map", file))
    return maps
