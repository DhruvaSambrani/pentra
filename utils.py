import json, os
import pygame

def pause(time, clock):
    for i in range(time):
        clock.tick(30)
    
def load_config(config_path = "./config.json"):
    data = json.load(open(config_path))
    return data["IMG_PATH"], data["AUDIO_PATH"], data["BG_COLOR"], data["FG_COLOR"]

def load_image(file_name):
    return pygame.image.load(os.path.join(IMG_PATH, file_name))

def load_music(file_name):
    return pygame.mixer.music.load(os.path.join(AUDIO_PATH, file_name))

def play_sound(file_name):
    return pygame.mixer.Sound(os.path.join(AUDIO_PATH, file_name)).play()

IMG_PATH, AUDIO_PATH, BG_COLOR, FG_COLOR = load_config()
