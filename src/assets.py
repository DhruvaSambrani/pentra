import os

import pygame

import map
import inventory
import scriptable
from settings import settings
import enemy

def exists(assettype, name):
    filepath = os.path.join(settings.assets, assettype, name)
    return os.path.exists(filepath)


def load_asset(assettype, name, **kwargs):
    filepath = os.path.join(settings.assets, assettype, name).lower()
    if assettype in ["image", "sprite"]:
        return pygame.image.load(filepath)
    if assettype == "scene":
        return scriptable.Scriptable(filepath, **kwargs)
    if assettype == "sound":
        return pygame.mixer.Sound(filepath)
    if assettype == "music":
        pygame.mixer.music.load(filepath)
        return
    if assettype == "color":
        c = settings.palette[name]
        if len(c) == 3:
            c.append(255)
        return c
    if assettype == "font":
        return pygame.font.Font(filepath, **kwargs)
    if assettype == "map":
        return map.Map(filepath)
    if assettype == "item":
        return inventory.Item(filepath)
    if assettype == "script":
        newlocal = {}
        try:
            exec(open(filepath).read(), globals(), newlocal)
            return newlocal["main"](**kwargs)
        except Exception as e:
            print("ERROR: while running external script ", name)
            print(e)
            exit(0)
    if assettype == "enemy":
        return enemy.Enemy(filepath, **kwargs)
    return filepath


def list_assets(assettype):
    return os.listdir(os.path.join(settings.assets, assettype))


def play_music(file_name, repeat=-1):
    pygame.mixer.music.stop()
    load_asset("music", file_name)
    pygame.mixer.music.play(repeat)
