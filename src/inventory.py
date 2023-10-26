import pygame
from pygame.math import Vector2

from settings import settings
from assets import load_asset


class Item:
    def __init__(self, file):
        self.name = "Guy"
        self.image = load_asset("sprite", file)
        self.tool_tip = "A guy. You found him lost in the building and you decided to take him under your wing.."
        pass


guy = Item("player.png")


class Slot:
    def __init__(self, item=guy):
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

        # render tool tip
        if show_tip and not (self.item is None):
            ft = pygame.font.SysFont("Verdana", 16).render(
                self.item.name + "\n" + self.item.tool_tip,
                False,
                (0, 0, 0),
                (100, 100, 100),
                300,
            )
            tooltip_rect = ft.get_rect(topleft=item_rect.topright + Vector2(20, 0))
            surface.blit(ft, tooltip_rect)


class Inventory:
    def __init__(self, num_slots):
        self.slots = [Slot() for i in range(num_slots)]
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
