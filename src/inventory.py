import pygame, os, json
from pygame.math import Vector2

from settings import settings
from assets import load_asset

class Item:
    def __init__(self, name, desc, image):
        self.name = name
        self.desc = desc
        self.image = image

class Slot:
    def __init__(self, item = None):
        self.item = item

    def render(self, pos, border, surface, show_tip=False):
        r = pygame.Rect(*pos, 60, 60)

        # render slot
        surface.fill(settings.palette["GREY1"], r)
        pygame.draw.rect(surface, settings.palette["GREY2"], r, border, 3)

        # render item sprite
        item_rect = self.item.image.get_rect()
        item_rect.center = pos + Vector2(30, 30)
        surface.blit(self.item.image, item_rect)

        # render description
        if show_tip and not (self.item is None):
            ft = pygame.font.SysFont("Verdana", 16).render(
                self.item.name.upper() + "\n" + self.item.desc,
                True,
                (0, 0, 0),
                None,
                300
            )
            #get bounding rect from font render and then inflate and draw separately
            desc_rect = ft.get_rect(topleft=item_rect.topright + Vector2(30, -13)).inflate(Vector2(10, 10))
            pygame.draw.rect(surface, settings.palette["GREY1"], desc_rect, 0, 3)
            surface.blit(ft, desc_rect.topleft + Vector2(8, 3))


class Inventory:
    def __init__(self, num_slots, items):
        self.slots = [Slot(items[i]) for i in range(num_slots)]
        self.active = 0
        self.show_info = False

    def render(self, surface):
        for i, slot in enumerate(self.slots):
            if i == self.active:
                slot.render(Vector2(30, 60 + i * 80), 4, surface, self.show_info)
            else:
                slot.render(Vector2(30, 60 + i * 80), 1, surface)

    def update(self, shift):
        self.active = (self.active + shift) % len(self.slots)

def load_items():
    ITEM_PATH = os.path.join(settings.assets, "item")

    items = []
    for file in os.listdir(ITEM_PATH):
        print(os.path.join(ITEM_PATH, file))
        data = json.load(open(os.path.join(ITEM_PATH, file)))
        image = load_asset("sprite", data["name"].lower() + ".png")
        
        items.append(Item(data["name"], data["desc"], image))

    return items