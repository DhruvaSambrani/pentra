import json
from collections import namedtuple

Settings = namedtuple("Settings", "assets bg_color fg_color")


def load_config(config_path="./config.json"):
    data = json.load(open(config_path))
    return Settings(data["ASSETS_PATH"], data["BG_COLOR"], data["FG_COLOR"])


settings = load_config()
