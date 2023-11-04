import itertools

import pygame
from pygame.math import Vector2

from assets import load_asset
from settings import settings
from scriptable import Scriptable


class Player(pygame.sprite.Sprite):
    def __init__(self, app):
        super().__init__()
        self.image = load_asset("sprite", "player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.speed = 4
        self._steps_since_sound = 0
        self._steps_for_sound = 30
        self.app_context = app

    def die(self, enemy_name):
        self.app_context.current_scenes.append(
            Scriptable(
                [
                    "BLACK PEACH --blocking",
                    "fade_in 60",
                    f'print "Shit that {enemy_name} hit me!" -l 400x350',
                    "pause 60",
                    'print "Luckily it left me alone when I acted dead."',
                    "pause 60",
                    'type "Thank god the first aid box on this floor has medicine."',
                    'type "This is just like those Pikamen games"',
                    "pause 30",
                    "fade_out 90",
                ],
                self.app_context,
                open_as_file=False,
            )
        )
        self.set_position(self.app_context.current_map.first_aid)

    def update(self, map, keys):
        dir = Vector2(
            (
                keys[settings.key_map["move_right"]]
                - keys[settings.key_map["move_left"]]
            ),
            (keys[settings.key_map["move_down"]] - keys[settings.key_map["move_up"]]),
        )
        if dir != Vector2(0, 0):
            dir = (
                dir.normalize()
                * self.speed
                * (2 if keys[settings.key_map["run"]] else 1)
            )
            self._steps_since_sound += 3 if keys[settings.key_map["run"]] else 1
        self.rect.move_ip(*dir)
        if map.check_wall_collision(self):
            self.rect.move_ip(*-dir)
        if self._steps_since_sound > self._steps_for_sound:
            load_asset("sound", "steps.ogg").play()
            self._steps_since_sound = 0

    def render(self, surface, offset):
        r = self.rect.copy()
        r.move_ip(*offset)
        surface.blit(self.image, r)

    def set_position(self, pos):
        self.rect.center = pos

    def get_tile(self, tilesize):
        x, y = self.rect.center
        return (int(x / tilesize), int(y / tilesize))

    def get_all_tile(self, tilesize):
        tl = self.rect.topleft
        br = self.rect.bottomright
        return list(
            itertools.product(
                range(int(tl[0] / tilesize), round(br[0] / tilesize) + 1),
                range(int(tl[1] / tilesize), round(br[1] / tilesize) + 1),
            )
        )


_player = None


def get_player(app):
    global _player
    if _player is None:
        _player = Player(app)
    return _player
