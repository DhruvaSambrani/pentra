import argparse
import shlex

import pygame

import assets
from utils import pause


# Adapted from: https://stackoverflow.com/questions/64042648/how-do-i-blit-text-letter-by-letter-in-pygame-like-in-those-retro-rpg-games
def generate_letters(word, pos, font, txt_col):
    surfaces = []
    positions = []
    previousWidth = 0

    for i in range(len(word)):
        surf = font.render(word[i], True, txt_col)
        surfaces.append(surf)
    for i in range(len(surfaces)):
        previousWidth += surfaces[i - 1].get_rect().width
        positions.append([previousWidth + pos[0], pos[1]])
    return surfaces, positions


def type_text(line, pos, app, txt_col):
    letters, positions = generate_letters(line, pos, app.font, txt_col)
    for i in range(len(letters)):
        app._display_surf.blit(letters[i], (positions[i][0], positions[i][1]))
        pause(1, app.FPS)
        pygame.display.update()


###


def _build_scn_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["type", "print", "sound", "music", "pause", "manipulate"]
    )
    parser.add_argument("data")
    # print
    parser.add_argument("-l", required=False)
    parser.add_argument("-f", required=False)
    # music
    parser.add_argument("-r", type=int, required=False)
    return parser


class Scene:
    def __init__(self, filepath, bg_col, fg_col, line_spacing=40):
        self.txt_col = fg_col
        self.bg_col = bg_col
        self.line_spacing = line_spacing
        self.file = open(filepath, "r")
        self._parse()

    def _parse(self):
        parser = _build_scn_parser()
        self.actions = []
        for line in self.file.readlines():
            self.actions.append(parser.parse_args(shlex.split(line)))

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
        for action in self.actions:
            if action.action == "type":
                type_text(
                    action.data, [300, 250 + self.line_spacing * i], app, self.txt_col
                )  # TODO: user defined
                i += 1
            elif action.action == "print":
                app._display_surf.blit(
                    app.font.render(action.data, True, self.txt_col),
                    [300, 250 + self.line_spacing * i],
                )
                pygame.display.update()
                i += 1
            elif action.action == "sound":
                assets.load_asset("sound", action.data).play()
            elif action.action == "music":
                assets.play_music(action.data, action.r)
            elif action.action == "pause":
                pause(int(action.data), app.FPS)
