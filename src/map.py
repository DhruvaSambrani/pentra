import json
import os

import pygame
from pygame.math import Vector2

from inventory import load_item
from settings import settings


class Map:
    def __init__(self, name, items_on_load):
        self.name = name
        self.item_data = items_on_load

    def render(self, surface):
        for elt in self.item_data.keys():
            item = load_item(elt)
            item.render(surface, self.item_data[elt])


def load_maps():
    MAP_PATH = os.path.join(settings.assets, "map")

    maps = []
    for file in os.listdir(MAP_PATH):
        data = json.load(open(os.path.join(MAP_PATH, file)))

        maps.append(Map(data["name"], data["items_on_load"]))

    return maps
