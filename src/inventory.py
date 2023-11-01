import json

import pygame
from pygame.math import Vector2

import player
import assets
from settings import settings


class Item:
    def __init__(self, filepath):
        data = json.load(open(filepath + ".json"))

        self.name = data["name"]
        self.desc = data["desc"]
        self.image = assets.load_asset("sprite", data["name"].lower() + ".png")
        self.collectable = data.get("collectable", True)
        self.one_shot = data.get("one_shot", False)
        self.has_script = data.get("has_script", False)
        self.state = data.get("state", {})

    def render(self, surface, pos):
        item_rect = self.image.get_rect()
        item_rect.center = pos
        surface.blit(self.image, item_rect)

    def use(self, app):
        if self.has_script:
            status = assets.load_asset(
                "script", self.name + ".py", app=app, player=player.get_player()
            )
        else:
            app.clear_alerts()
            status = assets.load_asset(
                "script", "default.py", app=app, player=player.get_player()
            )
        return status


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
                    settings.palette["WHITE"],
                    None,
                    300,
                )
                # get bounding rect from font render and then inflate and draw separately items
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

    def get_item_slot(self, item_name):
        for idx, slot in enumerate(self.slots):
            if slot.item is not None and (slot.item.name.lower() == item_name.lower()):
                return slot, idx

        return (None, None)

    def get_items(self):
        return [slot.item for slot in self.slots if slot.item is not None]

    def is_full(self):
        items = [slot.item for slot in self.slots]
        return not (None in items)

    def add_item(self, item):
        # check if item is already in inventory to stack
        idx = next(
            (
                i
                for i, name in enumerate(
                    [
                        (slot.item.name if slot.item is not None else "")
                        for slot in self.slots
                    ]
                )
                if name == item.name
            ),
            -1,
        )

        if idx >= 0:
            self.slots[idx].quantity += 1
            return
        else:
            for i, slot in enumerate(self.slots):
                if slot.item is None:
                    slot.item = item
                    self.active = i
                    return

    def drop_item(self):
        item = self.slots[self.active].item
        if self.slots[self.active].quantity > 1:
            self.slots[self.active].quantity -= 1
        else:
            self.slots[self.active].item = None
        return item
