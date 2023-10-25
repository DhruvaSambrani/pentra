import re

import pygame

import assets
from utils import pause


### Adapted from: https://stackoverflow.com/questions/64042648/how-do-i-blit-text-letter-by-letter-in-pygame-like-in-those-retro-rpg-games
def generate_letters(word, pos, font, txt_col):
    
    surfaces = []
    positions  = []
    previousWidth = 0

    for i in range(len(word)):
        surf = font.render(word[i], True, txt_col)
        surfaces.append(surf)
    for i in range(len(surfaces)):
        previousWidth += surfaces[i-1].get_rect().width
        positions.append([previousWidth + pos[0], pos[1]])
    return surfaces, positions

def type_text(line, pos, app, txt_col):
     letters, positions = generate_letters(line, pos, app.font, txt_col)
     for i in range(len(letters)):
        app._display_surf.blit(letters[i], (positions[i][0], positions[i][1])) 
        pause(1, app.FPS)
        pygame.display.update()
###

class Scene:
    def __init__(self, filepath, bg_col, fg_col, line_spacing=40):
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
                type_text(data, [300, 250 + self.line_spacing * i], app, self.txt_col)
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
