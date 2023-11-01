import pygame
import assets
import random
from pygame.math import Vector2
import itertools
import json


class Enemy(pygame.sprite.Sprite):
    def __init__(self, filepath, pos, light_range_pixel):
        super().__init__()
        deets = json.load(open(filepath))
        self.name = deets["name"]
        self.eyesight = deets["eyesight"]
        self.image = assets.load_asset("sprite", deets["sprite"])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.attack_filter = pygame.surface.Surface(
            self.image.get_size(), flags=pygame.SRCALPHA
        )
        self.attack_filter.fill((252, 128, 5))
        self.light_range_pixel = light_range_pixel
        self.speed = 2
        self._steps_for_chdir = 60
        self._steps_for_sound = 120
        self._steps_since_chdir = 601
        self._steps_since_sound = 0
        self.current_dir = Vector2(0, 0)
        self.attacking = False

    def random_move(self, map):
        if self._steps_since_chdir > self._steps_for_chdir:
            self.current_dir = Vector2(random.randint(-1, 1), random.randint(-1, 1))
            if self.current_dir != Vector2(0, 0):
                self.current_dir = self.current_dir.normalize() * self.speed
            self._steps_since_chdir = 0
        self._steps_since_chdir += 1
        self._steps_since_sound += 1
        self.rect.move_ip(*self.current_dir)
        if map.check_wall_collision(self):
            self._steps_since_chdir += self._steps_for_chdir
            self.rect.move_ip(*-self.current_dir)
        if self._steps_since_sound > self._steps_for_sound:
            assets.load_asset("sound", "faraway_roar.ogg").play()
            self._steps_since_sound = 0

    def attack(self, map, player_pos):
        dir = Vector2(player_pos) - Vector2(self.rect.center)
        if dir != Vector2(0, 0):
            dir = dir.normalize() * self.speed * 2
            self._steps_since_sound += 2
        self.rect.move_ip(*dir)
        if map.check_wall_collision(self):
            self._steps_since_chdir = 0
            self.rect.move_ip(*-dir)
        if self._steps_since_sound > self._steps_for_sound:
            assets.load_asset("sound", "monster-attack-roar.ogg").play()
            self._steps_since_sound = 0

    def update(self, map, player_pos):
        if self.can_see(player_pos):
            if not self.attacking:
                self._steps_since_sound = self._steps_for_sound + 1
            self.attacking = True
            self.attack(map, player_pos)
        else:
            self.attacking = False
            self.random_move(map)

    def can_see(self, player_pos):
        return (
            Vector2(self.rect.center) - Vector2(player_pos)
        ).magnitude() < self.light_range_pixel * self.eyesight

    def render(self, surface, offset):
        r = self.rect.copy()
        r.move_ip(*offset)
        surface.blit(self.image, r)
        if self.attacking:
            surface.blit(self.attack_filter, r, special_flags=pygame.BLEND_RGB_MULT)

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
