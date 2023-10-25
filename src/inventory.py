import pygame

from settings import settings


class Item:
    def __init__(self):
        pass


class Slot:
    def __init__(self):
        self.item = None

    def render(self, pos, border, surface):
        r = pygame.Rect(*pos, 60, 60)
        surface.fill(settings.palette["GREY1"], r)
        pygame.draw.rect(surface, settings.palette["GREY2"], r, border)


class Inventory:
    def __init__(self, num_slots):
        self.slots = [Slot() for i in range(num_slots)]
        self.active = 0

    def render(self, surface):
        for i, slot in enumerate(self.slots):
            if i == self.active:
                slot.render([30, 60 + i * 80], 5, surface)
            else:
                slot.render([30, 60 + i * 80], 1, surface)

    def update(self, shift):
        self.active = (self.active + shift) % len(self.slots)
