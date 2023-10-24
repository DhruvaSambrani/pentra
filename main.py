import pygame
import math 
from pygame.locals import *

BGCOLOR=(17,17,27)
FGCOLOR=(242,213,207)

def pause(time, clock):
    for i in range(time):
        clock.tick(30)

class Player(pygame.sprite.Sprite):
    def __init__(self, startloc):
        super().__init__()
        self.image = pygame.image.load("./assets/sprite/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = startloc
        self.speed = 5 
        self._steps_since_sound = 0
        self._steps_for_sound = 15

    def update(self, keys):
        a = [0, 0]
        if keys[K_UP]:
            a[1] += -1
        if keys[K_DOWN]:
            a[1] += +1
        if keys[K_LEFT]:
            a[0] += -1
        if keys[K_RIGHT]:
            a[0] += +1
        l = math.sqrt(a[0]**2 + a[1]**2)
        if l != 0:
            a[0] *= self.speed/l
            a[1] *= self.speed/l
            self._steps_since_sound += 1
        if self._steps_since_sound > self._steps_for_sound:
            pygame.mixer.Sound("./assets/audio/steps.ogg").play()
            self._steps_since_sound = 0
        self.rect.move_ip(*a)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 800
        self.player = Player((640, 400))

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.FPS = pygame.time.Clock()

    def actual_init(self):
        self._display_surf.fill(BGCOLOR)
        self._running = True

    def startup_sequence(self, passthrough=False):
        if passthrough:
            font = pygame.font.SysFont("Verdana", 30)
            pygame.mixer.music.load("./assets/audio/scary.mp3")
            pygame.mixer.music.play(-1)
            return

        self._display_surf.fill(FGCOLOR)
        pygame.mixer.music.load("./assets/audio/lofi.mp3")
        pygame.mixer.music.play(-1)
        font = pygame.font.SysFont("Verdana", 30)
        self._display_surf.blit(font.render("A nice Saturday night", True, BGCOLOR), (250, 330))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("You are nearly done with your homework", True, BGCOLOR), (250, 370))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("Its almost 12am", True, BGCOLOR), (250, 410))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("The weather is surprisingly nice. Not hot, but definitely not cold", True, BGCOLOR), (250, 450))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("The vending machine coffee is not GREAT, but you've had worse...", True, BGCOLOR), (250, 490))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("This music is pretty catchy hunh?", True, BGCOLOR), (250, 530))
        pygame.display.update()
        pause(30, self.FPS)
        pygame.mixer.Sound("./assets/audio/earthquake.ogg").play()
        pause(60, self.FPS)
        self._display_surf.fill(BGCOLOR)        
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./assets/audio/scary.mp3")
        pygame.mixer.music.play(-1)
        pause(90, self.FPS)
        self._display_surf.blit(font.render("Wha... What just happened???", True, FGCOLOR), (250, 300))
        pygame.display.update()
        pause(120, self.FPS)
        self._display_surf.blit(font.render("Did the lights go out?", True, FGCOLOR), (250, 330))
        pygame.display.update()
        pause(120, self.FPS)
        self._display_surf.blit(font.render("Aaah typical IISER infrastructure, amirite?", True, FGCOLOR), (250, 360))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("What was that sound though?", True, FGCOLOR), (250, 390))
        pygame.display.update()
        pause(60, self.FPS)
        pygame.mixer.Sound("./assets/audio/bell.ogg").play()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("Ahh it's midnight", True, FGCOLOR), (250, 420))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("Since when is there a bell at IISER?", True, FGCOLOR), (250, 450))
        pygame.display.update()
        pause(60, self.FPS)
        self._display_surf.blit(font.render("Something is weird. Where is my phone?", True, FGCOLOR), (250, 480))
        pygame.display.update()
        pause(90, self.FPS)
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    
    def on_loop(self):
        self.player.update(pygame.key.get_pressed())

    def on_render(self):
        self._display_surf.fill(BGCOLOR)
        self.player.draw(self._display_surf)

    def on_cleanup(self):
        pygame.mixer.music.stop()
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        if self._running:
            self.startup_sequence(passthrough=True) ## ONLY FOR DEV PURPOSE
            self.actual_init()
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

