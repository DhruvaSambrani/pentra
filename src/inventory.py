import pygame
from pygame.math import Vector2 

from settings import settings
from assets import load_asset

class Item:
    def __init__(self, file):
        self.name = "Guy"
        self.image = load_asset("sprite", file)
        self.tool_tip = "Guy"
        pass

guy = Item("player.png")

class Slot:
    def __init__(self, item = guy):
        self.item = item
        
    def render(self, pos, border, surface, show_tip = False):
        r = pygame.Rect(*pos, 60, 60)

        # render slot
        surface.fill(settings.palette["GREY1"], r)
        pygame.draw.rect(surface, settings.palette["GREY2"], r, border, 3)

        # render item sprite
        item_rect = self.item.image.get_rect()
        item_rect.center = pos + Vector2(30, 30)
        surface.blit(self.item.image, item_rect)

        # render tool tip
        if show_tip:
            ft = pygame.font.SysFont("Verdana", 15).render(self.item.tool_tip, False, (0, 0, 0), (100, 100, 100))
            tooltip_rect = ft.get_rect(center = (60, 30))
            surface.blit(ft, tooltip_rect)
        
class Inventory:    
    def __init__(self, num_slots):
        self.slots = [Slot() for i in range(num_slots)]
        self.active = 0
    
    def render(self, surface):
        for i, slot in enumerate(self.slots):
            if (i == self.active):
                slot.render(Vector2(30, 60 + i * 80), 4, surface, True)
            else:
                slot.render(Vector2(30, 60 + i * 80), 1, surface)

    def update(self, shift):
        self.active = (self.active + shift) % len(self.slots)
