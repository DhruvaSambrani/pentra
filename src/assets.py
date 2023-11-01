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


def load_asset(assettype, name, additional=None):
    filepath = os.path.join(settings.assets, assettype, name)
    if assettype in ["image", "sprite"]:
        return pygame.image.load(filepath)
    if assettype == "scene":
        return scriptable.Scriptable(filepath, additional)
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
        return map.Map(filepath)
    if assettype == "item":
        return inventory.Item(filepath)
    if assettype == "script":
        newlocal = {}
        exec(open(filepath).read(), globals(), newlocal)
        return newlocal["script_fun"](additional["app"], additional["player"])
    if assettype == "enemy":
        return enemy.Enemy(filepath, additional[0], additional[1])
    return filepath


def list_assets(assettype):
    return os.listdir(os.path.join(settings.assets, assettype))


def play_music(file_name, repeat=-1):
    pygame.mixer.music.stop()
    load_asset("music", file_name)
    pygame.mixer.music.play(repeat)
