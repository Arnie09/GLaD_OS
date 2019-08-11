import os
import sys
from gtts import gTTS 
import pygame

class TTS():

    def __init__(self, message):

        self.message = message
        self.play()
  

    def play(self):
        language = 'en'
        myobj = gTTS(text=self.message, lang=language, slow=False) 
        myobj.save("message.mp3")
        del myobj
        pygame.mixer.init()
        pygame.mixer.music.load("message.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        #pygame.mixer.quit()
        os.remove("message.mp3")



  
