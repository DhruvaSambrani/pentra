import json
import os

from pygame.math import Vector2
from inventory import load_item
from settings import settings


class Map:
    def __init__(self, name, items_data):
        self.name = name
        self.items = [load_item(elt) for elt in items_data.keys()]
        self.item_locs = [Vector2(elt) for elt in items_data.values()]

    def pickup_item(self, pos):
        for i in range(len(self.items)):
            if (pos - self.item_locs[i]).magnitude() <= 50:
                item, _ = self.items.pop(i), self.item_locs.pop(i)
                return item
        return None

    def place_item(self, item, pos):
        self.items.append(item)
        self.item_locs.append(pos)

    def render(self, surface):
        for i in range(len(self.items)):
            self.items[i].render(surface, self.item_locs[i])


def load_maps():
    MAP_PATH = os.path.join(settings.assets, "map")

    maps = []
    for file in os.listdir(MAP_PATH):
        data = json.load(open(os.path.join(MAP_PATH, file)))

        maps.append(Map(data["name"], data["items_on_load"]))

    return maps
