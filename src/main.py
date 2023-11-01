import os

import pygame
from pygame.math import Vector2

import player
from assets import load_asset
from inventory import Inventory
from map import load_maps
from settings import settings

# Center pygame window upon creation
os.environ["SDL_VIDEO_CENTERED"] = "1"


def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError(
            "Arg 'amt' must be greater than 1.0, passed in value is %s" % amt
        )
    scale = 1.0 / float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 800
        pygame.font.init()
        self.font = load_asset("font", "DancingScript.ttf", 30)

        self.MAP_ATLAS = load_maps()

        self.current_map = None
        self.inventory = Inventory(
            8,
            [
                load_asset("item", elt)
                for elt in ["camera", "cross", "battery", "flashlight"]
            ],
        )
        self.current_scenes = []
        self.viewport_track_speed = 0.05
        self.viewport = pygame.rect.Rect(0, 0, *self.size)

    def on_init(self, debug):
        pygame.init()
        pygame.transform.set_smoothscale_backend("SSE")
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self._hud_surf = pygame.Surface(
            self._display_surf.get_size(), flags=pygame.SRCALPHA
        )
        self._hud_surf.set_alpha(200)

        self.FPS = pygame.time.Clock()
        self._display_surf.fill(load_asset("color", "BLACK"))
        self._running = True
        if not debug:
            self.current_scenes.append(load_asset("scene", "open1.scn", self))
        self.change_map(self.MAP_ATLAS[0])

    def change_map(self, newmap, loc=None):
        self.current_map = newmap
        if loc:
            player.get_player().set_position(loc)
        else:
            player.get_player().set_position(self.current_map.default_loc)

    def on_event(self, event):
        # handle global events (such as quit or other)
        if event.type == pygame.QUIT:
            self._running = False

        for current_scene in self.current_scenes:
            if current_scene.blocking:
                return

        # handle game specific events (player/inventory movement)
        if event.type == pygame.KEYDOWN:
            if event.key == settings.key_map["inv_down"]:
                self.inventory.update(1)
            if event.key == settings.key_map["inv_up"]:
                self.inventory.update(-1)
            if event.key == settings.key_map["inv_info"]:
                self.inventory.show_info = not self.inventory.show_info
            if event.key == settings.key_map["drop_item"]:
                item = self.inventory.drop_item()
                if item is not None:
                    self.current_map.place_item(
                        item, Vector2(player.get_player().rect.center)
                    )
            if event.key == settings.key_map["interact"]:
                if not self.inventory.is_full():
                    item = self.current_map.pickup_item(
                        Vector2(player.get_player().rect.center)
                    )
                    if item is not None:
                        self.inventory.add_item(item)
            if event.key == settings.key_map["use_item"]:
                item = self.inventory.slots[self.inventory.active].item
                if item is not None:
                    status = item.use(self)
                    if status and item.one_shot:
                        self.inventory.drop_item()

    def on_loop(self):
        for i, current_scene in filter(
            lambda iv: iv[1].blocking, enumerate(self.current_scenes)
        ):
            if current_scene.next(self):
                self.current_scenes.pop(i)
            return
        for i, current_scene in enumerate(self.current_scenes):
            if current_scene.next(self):
                self.current_scenes.pop(i)
        self.viewport.move_ip(
            (Vector2(player.get_player().rect.center) - Vector2(self.viewport.center))
            * self.viewport_track_speed
        )
        self.viewport.clamp_ip(self.current_map.map_surf.get_rect())
        player.get_player().update(self.current_map, pygame.key.get_pressed())
        for enemy in self.current_map.enemies:
            enemy.update(self.current_map, player.get_player().rect.center)
        self.current_map.check_areas(self, player.get_player().rect.center)

    def on_render(self):
        self._display_surf.fill(load_asset("color", "BLACK"))
        for current_scene in filter(lambda iv: iv.blocking, self.current_scenes):
            current_scene.render(self._display_surf)
            return
        for current_scene in self.current_scenes:
            current_scene.render(self._display_surf)
        self._hud_surf.fill(load_asset("color", "TRANSPARENT"))
        self.current_map.render(self._display_surf, self.viewport)
        self.inventory.render(self._hud_surf)
        self._display_surf.blit(self._hud_surf, (0, 0))

    def on_cleanup(self):
        pygame.mixer.music.stop()
        pygame.quit()

    def on_execute(self, debug=False):
        self.on_init(debug)
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.flip()
            self.FPS.tick(30)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute(debug=True)
