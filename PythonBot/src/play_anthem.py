import pygame
import os
import sys


class Play_Still_Alive():
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(sys.path[0],"assets","audio","Portal - Still Alive.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        pygame.mixer.quit()