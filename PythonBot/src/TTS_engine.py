import os
import sys
from gtts import gTTS 
from playsound import playsound

class TTS():

    def __init__(self, message):
        self.message = message
        self.play()
  

    def play(self):
        language = 'en'
        myobj = gTTS(text=self.message, lang=language, slow=False) 
        myobj.save(os.path.join(sys.path[0],"audio_responses","welcome.mp3"))
        playsound(os.path.join(sys.path[0],"audio_responses","welcome.mp3"))

  
