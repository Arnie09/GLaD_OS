import os
import sys
from gtts import gTTS 
from playsound import playsound

class TTS():

    def __init__(self, message,counter):

        self.counter = counter
        self.message = message
        self.play()
  

    def play(self):
        language = 'en'
        myobj = gTTS(text=self.message, lang=language, slow=False) 
        myobj.save("message"+str(self.counter)+".mp3")
        playsound("message"+str(self.counter)+".mp3",True)
        os.remove("message"+str(self.counter)+".mp3")



  
