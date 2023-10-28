import json
import os

import pygame

import map
import scene
from settings import settings


def load_asset(assettype, name, additional=None):
    filepath = os.path.join(settings.assets, assettype, name)
    if assettype in ["image", "sprite"]:
        return pygame.image.load(filepath)
    if assettype == "scene":
        return scene.Scene(filepath, additional)
    if assettype == "sound":
        return pygame.mixer.Sound(filepath)
    if assettype == "music":
        pygame.mixer.music.load(filepath)
        return
    if assettype == "color":
        return settings.palette[name]
    if assettype == "font":
        return pygame.font.Font(filepath, additional)
    if assettype == "map":
        meta = json.load(open(os.path.join(filepath, "meta.json")))
        map_surf = pygame.image.load(os.path.join(filepath, "map.png"))
        return map.Map(map_surf, meta)
    return filepath


def list_assets(assettype):
    return os.listdir(os.path.join(settings.assets, assettype))


def play_music(file_name, repeat=-1):
    pygame.mixer.music.stop()
    load_asset("music", file_name)
    pygame.mixer.music.play(repeat)
