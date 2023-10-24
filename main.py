import pygame
from pygame.locals import *

BGCOLOR=(0,0,0)

class Player(pygame.sprite.Sprite):
    def __init__(self, startloc):
        super().__init__()
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = startloc 

    def update(self, keys):
        if keys[K_UP]:
            self.rect.move_ip(0, -5)
        if keys[K_DOWN]:
            self.rect.move_ip(0, +5)
        if keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(+5, 0)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 800
        self.FPS = pygame.time.Clock()
        self.player = Player((640, 400))

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(BGCOLOR)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        self.player.update(pygame.key.get_pressed())

    def on_render(self):
        self._display_surf.fill(BGCOLOR)
        self.player.draw(self._display_surf)

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.update()
            self.FPS.tick(30)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

