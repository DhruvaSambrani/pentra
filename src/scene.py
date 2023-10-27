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


def _build_scn_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=[
            "type",
            "print",
            "sound",
            "music",
            "pause",
            "manipulate",
            "clear",
            "load_scene",
        ],
    )
    parser.add_argument("data")
    # print
    parser.add_argument("-l", required=False)
    parser.add_argument("-f", required=False)
    # music
    parser.add_argument("-r", type=int, required=False)
    return parser


def _build_meta_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("fgcolor")
    parser.add_argument("bgcolor")
    parser.add_argument("--blocking", action="store_true")
    return parser


class Scene:
    def __init__(self, filepath, app, line_spacing=40):
        self.line_spacing = line_spacing
        self.file = open(filepath, "r")
        self.state = -1
        self.textline = 0
        self._display_surf = pygame.Surface(
            app._display_surf.get_size(), flags=pygame.SRCALPHA
        )
        self._display_surf.set_alpha(255)
        self._parse()

    def _parse(self):
        parser = _build_scn_parser()
        self.actions = []
        lines = self.file.readlines()
        meta_line = _build_meta_parser().parse_args(shlex.split(lines[0]))
        self.blocking = meta_line.blocking
        self.fgcolor = meta_line.fgcolor
        self.bgcolor = meta_line.bgcolor
        for line in lines[1:]:
            self.actions.append(parser.parse_args(shlex.split(line)))
        self._display_surf.fill(assets.load_asset("color", self.bgcolor))

    def render(self, main_surf):
        main_surf.blit(self._display_surf, (0, 0))

    def next(self, app):
        if len(self.actions) < 1:
            return None
        action = self.actions.pop(0)
        if False and action.action == "type":
            # currently broken TODO:fix
            type_text(
                action.data,
                [300, 250 + self.line_spacing * self.textline],
                app,
                assets.load_asset("color", self.fgcolor),
            )  # TODO: user defined pos, font
            self.textline += 1
        elif action.action == "print" or action.action == "type":
            self._display_surf.blit(
                app.font.render(
                    action.data,
                    True,
                    assets.load_asset("color", self.fgcolor),
                ),
                [300, 250 + self.line_spacing * self.textline],
            )
            self.textline += 1
        elif action.action == "sound":
            assets.load_asset("sound", action.data).play()
        elif action.action == "music":
            assets.play_music(action.data, action.r)
        elif action.action == "pause":
            action.data = int(action.data) - 1
            if action.data != 0:
                self.actions.insert(0, action)
        elif action.action == "clear":
            self._display_surf.fill(self.bgcolor)
        elif action.action == "load_scene":
            return assets.load_asset("scene", action.data, app)
        return self
