import json
import os

import pygame
from pygame.math import Vector2

from assets import load_asset
from settings import settings


class Item:
    def __init__(self, name, desc, image):
        self.name = name
        self.desc = desc
        self.image = image

    def render(self, surface, pos):
        item_rect = self.image.get_rect()
        item_rect.center = pos
        surface.blit(self.image, item_rect)


class Slot:
    def __init__(self, item=None, quantity=1):
        self.item = item
        self.quantity = quantity

    def render(self, pos, border, surface, show_tip=False):
        r = pygame.Rect(*pos, 60, 60)

        # render slot
        surface.fill(settings.palette["GREY1"], r)
        pygame.draw.rect(surface, settings.palette["GREY2"], r, border, 3)

        # render item sprite
        if self.item is not None:
            self.item.render(surface, pos + Vector2(30, 30))

            # render description
            if show_tip and not (self.item is None):
                qt_label = "" if (self.quantity == 1) else f" (x{self.quantity})"

                ft = pygame.font.SysFont("Verdana", 16).render(
                    self.item.name.upper() + qt_label + "\n" + self.item.desc,
                    True,
                    settings.palette["VOID"],
                    None,
                    300,
                )
                # get bounding rect from font render and then inflate and draw separatelyiitems
                desc_rect = ft.get_rect(topleft=r.topright + Vector2(20, 5)).inflate(
                    Vector2(10, 10)
                )
                pygame.draw.rect(surface, settings.palette["GREY1"], desc_rect, 0, 3)
                surface.blit(ft, desc_rect.topleft + Vector2(8, 3))


class Inventory:
    def __init__(self, num_slots, items):
        self.slots = [Slot(item) for item in items] + [
            Slot() for _ in range(num_slots - len(items))
        ]
        self.active = 0
        self.show_info = False

    def render(self, surface):
        for i, slot in enumerate(self.slots):
            if i == self.active:
                slot.render(Vector2(30, 80 + i * 80), 4, surface, self.show_info)
            else:
                slot.render(Vector2(30, 80 + i * 80), 1, surface)

    def update(self, shift):
        self.active = (self.active + shift) % len(self.slots)

    def get_items(self):
        return [slot.item for slot in self.slots if slot.item is not None]

    def add_item(self, item):
        is_full = True

        for slot in self.slots:
            if slot.item is item:
                slot.quantity += 1
            elif slot.item is None:
                slot.item = item
                is_full = False

        return not is_full

    def remove_item(self, slot):
        self.slots[slot].item = None


def load_item(file):
    ITEM_PATH = os.path.join(settings.assets, "item")

    data = json.load(open(os.path.join(ITEM_PATH, file + ".json")))
    image = load_asset("sprite", data["name"].lower() + ".png")

    return Item(data["name"], data["desc"], image)


# def load_items():
#     ITEM_PATH = os.path.join(settings.assets, "item")

#     items = []
#     for file in os.listdir(ITEM_PATH):
#         data = json.load(open(os.path.join(ITEM_PATH, file)))
#         image = load_asset("sprite", data["name"].lower() + ".png")

#         items.append(Item(data["name"], data["desc"], image))

#     return items
