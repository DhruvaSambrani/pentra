import json
import os

import pygame
from pygame.math import Vector2
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
            tile[0] < 2
            or tile[0] > self.shades.get_size()[0] - 2
            or tile[1] < 2
            or tile[1] > self.shades.get_size()[1] - 2
        )

    def check_wall_collision(self, sprite):
        tiles = sprite.get_all_tile(self.shader_scale)
        for tile in tiles:
            if self._tile_not_in_bounds(tile):
                return True

        return sum([self.shades.get_at(tile)[0] for tile in tiles]) > 0

    def pickup_item(self, pos):
        for i in range(len(self.items)):
            if self.items[i].collectable:
                if (pos - self.item_locs[i]).magnitude() <= 35:
                    item, _ = self.items.pop(i), self.item_locs.pop(i)
                    return item
        return None

    def place_item(self, item, pos):
        self.items.append(item)
        self.item_locs.append(pos)

    def update_lighting(self, start_tile, render_range, scale):
        def neighbors(tile):
            l = [
                (tile[0] - 1, tile[1]),
                (tile[0] + 1, tile[1]),
                (tile[0], tile[1] - 1),
                (tile[0], tile[1] + 1),
            ]
            return l

        _list = [start_tile]
        _dict = {start_tile: 1}
        for i in range((render_range + 1) ** 2 + render_range**2):
            for n in neighbors(_list[i]):
                if n not in _dict.keys():
                    _list.append(n)
                if self._tile_not_in_bounds(n):
                    _dict[n] = 0
                    break
                newval = _dict[_list[i]] * scale * (1 - self.shades.get_at(n)[0] / 255)
                if _dict.get(n, -1) < newval:
                    _dict[n] = newval

        new_surf = pygame.Surface(self.shades.get_size(), flags=pygame.SRCALPHA)
        for pixel in _dict.keys():
            new_surf.set_at(
                pixel,
                [255, 255, 255, int(_dict[pixel] * 255)],
            )
        pygame.transform.smoothscale_by(new_surf, self.shader_scale, self.light_surf)

    def render(self, disp_surface, viewport):
        light_range, light_scale = 20, 0.85

        p = player.get_player()
        x, y = p.rect.center
        x1 = x - (light_range * self.shader_scale)
        y1 = y - (light_range * self.shader_scale)
        rvp_size = (2 * light_range + 1) * self.shader_scale

        x1 = max(0, min(x1, self.map_surf.get_size()[0] - rvp_size))
        y1 = max(0, min(y1, self.map_surf.get_size()[1] - rvp_size))

        rvp = pygame.rect.Rect(x1, y1, rvp_size, rvp_size)

        temp_surface = self.map_surf.subsurface(rvp).copy()
        for i in range(len(self.items)):
            if (
                x1 < self.item_locs[i][0] < x1 + rvp_size
                and y1 < self.item_locs[i][1] < y1 + rvp_size
            ):
                self.items[i].render(temp_surface, self.item_locs[i] - rvp.topleft)
        p.render(temp_surface, offset=-Vector2(rvp.topleft))
        self.update_lighting(p.get_tile(self.shader_scale), light_range, light_scale)

        temp_surface.blit(
            self.light_surf.subsurface(rvp),
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT,
        )
        disp_surface.blit(
            temp_surface, Vector2(rvp.topleft) - Vector2(viewport.topleft)
        )


def load_maps():
    maps = []
    for file in assets.list_assets("map"):
        maps.append(assets.load_asset("map", file))
    return maps
