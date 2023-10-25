import json, re, os
import pygame
from pygame.locals import *

def pause(time, clock):
    for i in range(time):
        clock.tick(30)
    
def load_config(config_path = "./config.json"):
    data = json.load(open(config_path))
    return data["IMG_PATH"], data["AUDIO_PATH"], data["SCENE_PATH"], data["BG_COLOR"], data["FG_COLOR"]

def load_image(file_name):
    return pygame.image.load(os.path.join(IMG_PATH, file_name))

def play_music(file_name, repeat=-1):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join(AUDIO_PATH, file_name))
    pygame.mixer.music.play(repeat)

def play_sound(file_name):
    return pygame.mixer.Sound(os.path.join(AUDIO_PATH, file_name)).play()
        

IMG_PATH, AUDIO_PATH, SCENE_PATH, BG_COLOR, FG_COLOR = load_config()
