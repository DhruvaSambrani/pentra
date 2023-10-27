import os

import pygame
from pygame.math import Vector2

from assets import load_asset
from inventory import Inventory, load_items
from settings import settings

# Center pygame window upon creation
os.environ["SDL_VIDEO_CENTERED"] = "1"


class Player(pygame.sprite.Sprite):
    def __init__(self, startloc):
        super().__init__()
        self.image = load_asset("sprite", "player.png")
        self.rect = self.image.get_rect()
        self.rect.center = startloc
        self.speed = 4
        self._steps_since_sound = 0
        self._steps_for_sound = 30

    def update(self, keys):
        dir = Vector2(
            (
                keys[settings.key_map["move_right"]]
                - keys[settings.key_map["move_left"]]
            ),
            (keys[settings.key_map["move_down"]] - keys[settings.key_map["move_up"]]),
        )
        if dir != Vector2(0, 0):
            dir = (
                dir.normalize()
                * self.speed
                * (2 if keys[settings.key_map["run"]] else 1)
            )
            self._steps_since_sound += 3 if keys[settings.key_map["run"]] else 1
        if self._steps_since_sound > self._steps_for_sound:
            load_asset("sound", "steps.ogg").play()
            self._steps_since_sound = 0
        self.rect.move_ip(*dir)

    def render(self, surface):
        surface.blit(self.image, self.rect)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 800
        self.player = Player((640, 400))
        pygame.font.init()
        self.font = pygame.font.Font("./assets/font/DancingScript.ttf", 30)

        self.items = load_items()
        self.inventory = Inventory(7, self.items)
        self.current_scene = None

    def on_init(self, debug):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        self._hud_surf = pygame.Surface(
            self._display_surf.get_size(), flags=pygame.SRCALPHA
        )
        self._hud_surf.set_alpha(200)

        self.FPS = pygame.time.Clock()
        self._display_surf.fill(settings.palette["BLACK"])
        self._running = True
        self.current_scene = load_asset("scene", "open1.scn", self) if not debug else None
        self.next_scene = None

    def on_event(self, event):
        # handle global events (such as quit or other)
        if event.type == pygame.QUIT:
            self._running = False

        if self.current_scene and self.current_scene.blocking:
            return

        # handle game specific events (player/inventory movement)
        if event.type == pygame.KEYDOWN:
            if event.key == settings.key_map["inv_right"]:
                self.inventory.update(1)
            if event.key == settings.key_map["inv_left"]:
                self.inventory.update(-1)
            if event.key == settings.key_map["inv_info"]:
                self.inventory.show_info = not self.inventory.show_info

    def on_loop(self):
        if self.current_scene is not None:
            self.next_scene = self.current_scene.next(self)
            if self.current_scene.blocking:
                return
        self.player.update(pygame.key.get_pressed())

    def on_render(self):
        self._display_surf.fill(load_asset("color", "BLACK"))
        if self.current_scene is not None:
            self.current_scene.render(self._display_surf)
            if self.current_scene.blocking:
                return
        self._hud_surf.fill(settings.palette["TRANSPARENT"])
        self.player.render(self._display_surf)
        self.inventory.render(self._hud_surf)
        self._display_surf.blit(self._hud_surf, (0, 0))

    def on_cleanup(self):
        pygame.mixer.music.stop()
        pygame.quit()

    def on_execute(self, debug = False):
        self.on_init(debug)
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.flip()
            self.FPS.tick(30)
            self.current_scene = self.next_scene
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute(debug=True)
