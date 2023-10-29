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
        self.name = meta["name"]
        items_data = meta["items_on_load"]
        self.default_loc = meta["default_loc"]
        self.shader_scale = meta["shader_scale"]
        self.items = [load_item(elt[0]) for elt in items_data]
        self.item_locs = [Vector2(elt[1]) for elt in items_data]
        self.map_surf = pygame.image.load(os.path.join(folderpath, "map.png"))
        pygame.draw.rect(
            self.map_surf,
            assets.load_asset("color", "WHITE"),
            pygame.rect.Rect(0, 0, *self.map_surf.get_size()),
            width=16,
        )
        self.shades = pygame.image.load(os.path.join(folderpath, "shade.png"))
        self.light_surf = pygame.Surface(
            self.map_surf.get_size(), flags=pygame.SRCALPHA
        )

    def _tile_not_in_bounds(self, tile):
        return (
            tile[0] < 1
            or tile[0] > self.shades.get_size()[0] - 1
            or tile[1] < 1
            or tile[1] > self.shades.get_size()[1] - 1
        )

    def check_wall_collision(self, sprite):
        tiles = sprite.get_all_tile(self.shader_scale)
        for tile in tiles:
            if self._tile_not_in_bounds(tile):
                return True

        return sum([self.shades.get_at(tile)[0] for tile in tiles]) > 0

    def pickup_item(self, pos):
        for i in range(len(self.items)):
            if (pos - self.item_locs[i]).magnitude() <= 35:
                item, _ = self.items.pop(i), self.item_locs.pop(i)
                return item
        return None

    def place_item(self, item, pos):
        self.items.append(item)
        self.item_locs.append(pos)

    def update_lighting(self, start_tile, render_range, scale):
        def neighbors(tile):
            return [
                (tile[0] - 1, tile[1]),
                (tile[0] + 1, tile[1]),
                (tile[0], tile[1] - 1),
                (tile[0], tile[1] + 1),
            ]

        _list = [start_tile]
        _dict = {start_tile: 1}
        for i in range((render_range + 1) ** 2 + render_range**2):
            for n in neighbors(_list[i]):
                if n not in _dict.keys():
                    _list.append(n)
                    if self._tile_not_in_bounds(n):
                        _dict[n] = 0
                    else:
                        _dict[n] = (
                            _dict[_list[i]]
                            * scale
                            * (1 - self.shades.get_at(n)[0] / 255)
                        )
        new_surf = pygame.Surface(self.shades.get_size(), flags=pygame.SRCALPHA)
        new_surf.fill(assets.load_asset("color", "TRANSPARENT"))
        for pixel in _dict.keys():
            new_surf.set_at(
                pixel,
                [255, 255, 255, _dict[pixel] * 255],
            )
        s2x = pygame.transform.scale2x
        self.light_surf = s2x(s2x(s2x(s2x(new_surf))))

    def render(self, disp_surface, viewport):
        temp_surface = self.map_surf.copy()
        for i in range(len(self.items)):
            self.items[i].render(temp_surface, self.item_locs[i])
        p = player.get_player()
        p.render(temp_surface)
        self.update_lighting(p.get_tile(self.shader_scale), 20, 0.85)
        temp_surface.blit(
            self.light_surf, (0, 0)
        )  # , special_flags=pygame.BLEND_RGBA_MULT)
        disp_surface.blit(temp_surface, (0, 0), viewport)


def load_maps():
    maps = []
    for file in assets.list_assets("map"):
        maps.append(assets.load_asset("map", file))
    return maps
