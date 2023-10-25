import json, pygame
from collections import namedtuple

Settings = namedtuple("Settings", "assets bg_color fg_color key_map")


def load_config(config_path="./config.json"):
    data = json.load(open(config_path))
    KEY_MAP = data["KEY_MAP"]
    for key, value in KEY_MAP.items():
        KEY_MAP[key] = eval("pygame.K_" + value)

    return Settings(data["ASSETS_PATH"], data["BG_COLOR"], data["FG_COLOR"], KEY_MAP)


settings = load_config()
