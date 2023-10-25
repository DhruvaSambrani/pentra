import re

import pygame

import assets
from utils import pause


class Scene:
    def __init__(self, filepath, bg_col, fg_col, line_spacing=30):
        self.txt_col = fg_col
        self.bg_col = bg_col
        self.line_spacing = line_spacing
        self.file = open(filepath, "r")

    def invert_colors(self):
        self.bg_col, self.txt_col = self.txt_col, self.bg_col
        return self

    def set_colors(self, b, t):
        self.bg_col, self.txt_col = b, t
        return self

    def play(self, app):
        app._display_surf.fill(self.bg_col)
        pygame.display.update()
        i = 0
        for line in self.file.readlines():
            data = re.findall(r'"(.+?)"', line)[0]
            if line[0] == ">":
                app._display_surf.blit(
                    app.font.render(data, True, self.txt_col),
                    (250, 330 + self.line_spacing * i),
                )
                pygame.display.update()
                i += 1
            elif line[0] == "-":
                if ".ogg" in data:
                    assets.load_asset("sound", data).play()
                elif ".mp3" in data:
                    fn = data.split("#")[0]
                    assets.play_music(
                        fn, -1 if "#" not in data else int(data.split("#")[1])
                    )
            elif line[0] == ".":
                pause(int(data), app.FPS)
