import json, re, os
import pygame
from pygame.locals import *

class Scene:
    def __init__(self, file_name, bg_col, fg_col): 
        self.def_pause = 60
        self.line_spacing = 30
        self.file_name = file_name
        self.txt_col = fg_col
        self.bg_col = bg_col

    def play(self, app):
        file = open(os.path.join(SCENE_PATH, self.file_name), 'r')
        
        app._display_surf.fill(self.bg_col)
        pygame.display.update()
        pause(self.def_pause, app.FPS)

        for i, line in enumerate(file.readlines()):
            data = re.findall(r'"(.+?)"', line)[0]

            if line[0] == ">":
                app._display_surf.blit(app.font.render(data, True, self.txt_col), (250, 330 + self.line_spacing * i))
                pygame.display.update()
            elif line[0] == "-":
                if ".ogg" in data:
                    play_sound(data)
                elif ".mp3" in data:
                    pygame.mixer.music.stop()
                    load_music(data)
                    pygame.mixer.music.play(-1)

            pause(self.def_pause, app.FPS)

def pause(time, clock):
    for i in range(time):
        clock.tick(30)
    
def load_config(config_path = "./config.json"):
    data = json.load(open(config_path))
    return data["IMG_PATH"], data["AUDIO_PATH"], data["SCENE_PATH"], data["BG_COLOR"], data["FG_COLOR"]

def load_image(file_name):
    return pygame.image.load(os.path.join(IMG_PATH, file_name))

def load_music(file_name):
    return pygame.mixer.music.load(os.path.join(AUDIO_PATH, file_name))

def play_sound(file_name):
    return pygame.mixer.Sound(os.path.join(AUDIO_PATH, file_name)).play()
        

IMG_PATH, AUDIO_PATH, SCENE_PATH, BG_COLOR, FG_COLOR = load_config()
