import os

import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.math import Vector2

from inventory import Item, Inventory
from assets import load_asset
from settings import settings
from utils import pause

# Center pygame window upon creation
os.environ['SDL_VIDEO_CENTERED'] = '1'

class Player(pygame.sprite.Sprite):
    def __init__(self, startloc):
        super().__init__()
        self.image = load_asset("sprite", "player.png")
        self.rect = self.image.get_rect()
        self.rect.center = startloc
        self.speed = 6
        self._steps_since_sound = 0
        self._steps_for_sound = 15

    def update(self, keys):
        dir = Vector2(
            (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), 
            (keys[pygame.K_DOWN] - keys[pygame.K_UP])
            )
        if dir != Vector2(0, 0):
            dir = dir.normalize() * self.speed
            self._steps_since_sound += 1
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
        self.inventory = Inventory(5)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.FPS = pygame.time.Clock()
        return True

    def actual_init(self):
        self._display_surf.fill(settings.bg_color)
        self._running = True

    def startup_sequence(self):
        pause(30, self.FPS)
        load_asset("scene", "open1.scn").invert_colors().play(self)
        load_asset("scene", "open2.scn").play(self)
        pause(30, self.FPS)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.inventory.update(1)
            if event.key == pygame.K_w:
                self.inventory.update(-1)

    def on_loop(self):
        self.player.update(pygame.key.get_pressed())

    def on_render(self):
        self._display_surf.fill(settings.bg_color)
        self.player.render(self._display_surf)
        self.inventory.render(self._display_surf)

    def on_cleanup(self):
        pygame.mixer.music.stop()
        pygame.quit()

    def on_execute(self, debug = False):
        if not self.on_init():
            self._running = False

        if self._running:
            if not debug: self.startup_sequence()  # ONLY FOR DEV PURPOSE
            self.actual_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.update()
            self.FPS.tick(30)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute(debug = True)
