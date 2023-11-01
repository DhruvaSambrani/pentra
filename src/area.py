import assets
import pygame
from pygame import Vector2


class Area:
    def __init__(self, name, rect):
        self.name = name
        wh = Vector2(rect[1]) - Vector2(rect[0])
        self.rect = pygame.rect.Rect(rect[0], wh)
        self.is_inside = False

    def on_entry(self, app):
        filename = self.name + "_enter.scn"

        if assets.exists("scene", filename):
            app.current_scenes.append(assets.load_asset("scene", filename, app))

    def on_exit(self, app):
        filename = self.name + "_exit.scn"

        if assets.exists("scene", filename):
            app.current_scenes.append(assets.load_asset("scene", filename, app))

    def _point_in(self, point):
        return self.rect.collidepoint(point)

    def trigger(self, app, point):
        if not self.is_inside and self._point_in(point):
            self.is_inside = True
            self.on_entry(app)
        elif self.is_inside and not self._point_in(point):
            self.is_inside = False
            self.on_exit(app)
