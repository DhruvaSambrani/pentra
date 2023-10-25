import os

import pygame

import scene
from settings import settings


def load_asset(assettype, name):
    filepath = os.path.join(settings.assets, assettype, name)
    if assettype in ["image", "sprite"]:
        return pygame.image.load(filepath)
    if assettype == "scene":
        return scene.Scene(filepath, settings.bg_color, settings.fg_color)
    if assettype == "sound":
        return pygame.mixer.Sound(filepath)
    if assettype == "music":
        pygame.mixer.music.load(filepath)
        return
    return filepath


def play_music(file_name, repeat=-1):
    pygame.mixer.music.stop()
    load_asset("music", file_name)
    pygame.mixer.music.play(repeat)
