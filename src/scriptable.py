import argparse
import shlex

import pygame

import assets
import player


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
            "run_script",
            "clear",
            "load_scene",
            "fade_in",
            "fade_out",
        ],
    )
    parser.add_argument("data")
    parser.add_argument("-l", required=False)
    parser.add_argument("-f", required=False)
    parser.add_argument("--v_dummy", required=False, default=-1)
    parser.add_argument("-r", type=int, required=False)
    return parser


def _build_meta_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("fgcolor")
    parser.add_argument("bgcolor")
    parser.add_argument("-ls", "--line_spacing", type=int, default=40)
    parser.add_argument("-n", "--name", type=str, default="")
    parser.add_argument("--blocking", action="store_true")
    return parser


class Scriptable:
    def __init__(self, file, app, open_as_file=True):
        self.lines = open(file, "r").readlines() if open_as_file else file
        self.lastline = (0, 0)
        self._display_surf = pygame.Surface(
            app._display_surf.get_size(), flags=pygame.SRCALPHA
        )
        self._display_surf.set_alpha(255)
        self._parse()

    def _parse(self):
        parser = _build_scn_parser()
        self.actions = []
        meta_line = _build_meta_parser().parse_args(shlex.split(self.lines[0]))
        self.blocking = meta_line.blocking
        self.fgcolor = meta_line.fgcolor
        self.bgcolor = meta_line.bgcolor
        self.line_spacing = meta_line.line_spacing
        self.name = meta_line.name
        for line in self.lines[1:]:
            self.actions.append(parser.parse_args(shlex.split(line)))
        self._display_surf.fill(assets.load_asset("color", self.bgcolor))

    def render(self, main_surf):
        main_surf.blit(self._display_surf, (0, 0))

    def next(self, app):
        if len(self.actions) < 1:
            return True
        action = self.actions.pop(0)
        if action.action == "type":
            font = assets.load_asset("font", action.f) if action.f else app.font
            if action.l:
                x, y = action.l.split("x")
                pos = (int(x), int(y))
            else:
                pos = (self.lastline[0], self.lastline[1] + self.line_spacing)

            letter_surf = font.render(
                action.data[0], True, assets.load_asset("color", self.fgcolor)
            )
            self._display_surf.blit(letter_surf, pos)
            if action.v_dummy == -1:
                self.lastline = pos
            if len(action.data) > 1:
                action.v_dummy = 0
                action.data = action.data[1:]
                action.l = (
                    str(pos[0] + letter_surf.get_rect().width) + "x" + str(pos[1])
                )
                self.actions.insert(0, action)

        elif action.action == "print":
            font = assets.load_asset("font", action.f) if action.f else app.font
            if action.l:
                x, y = action.l.split("x")
                pos = (int(x), int(y))
            else:
                pos = (self.lastline[0], self.lastline[1] + self.line_spacing)

            self._display_surf.blit(
                font.render(
                    action.data,
                    True,
                    assets.load_asset("color", self.fgcolor),
                ),
                pos,
            )
            self.lastline = pos
        elif action.action == "sound":
            assets.load_asset("sound", action.data).play()
        elif action.action == "music":
            assets.play_music(action.data, action.r)
        elif action.action == "pause":
            action.data = int(action.data) - 1
            if action.data != 0:
                self.actions.insert(0, action)
        elif action.action == "clear":
            self._display_surf.fill(assets.load_asset("color", self.bgcolor))
        elif action.action == "load_scene":
            app.current_scenes.append(assets.load_asset("scene", action.data, app=app))
        elif action.action == "fade_in":
            data = action.data.strip().split("-")
            if len(data) == 1:
                data.append("1")
            bgcol = assets.load_asset("color", self.bgcolor)
            bgcol[3] = int(int(data[1]) / int(data[0]) * 255)
            self._display_surf.fill(bgcol)
            action.data = data[0] + "-" + str(int(data[1]) + 1)
            if data[1] != data[0]:
                self.actions.insert(0, action)
        elif action.action == "fade_out":
            data = action.data.split("-")
            if len(data) == 1:
                data.append("1")
            bgcol = assets.load_asset("color", self.bgcolor)
            bgcol[3] = int(255 * (1 - int(data[1]) / int(data[0])))
            self._display_surf.fill(bgcol)
            action.data = data[0] + "-" + str(int(data[1]) + 1)
            if data[1] != data[0]:
                self.actions.insert(0, action)
        elif action.action == "run_script":
            assets.load_asset(
                "script",
                action.data,
                app=app,
                player=player.get_player(),
                source=self.name.lower(),
            )
        return False
