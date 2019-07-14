from TTS_engine import TTS
import os
import sys

class iotControl():

    def __init__(self,message):
        print("Here")
        self.message = message
        self.determine()

    def determine(self):
        '''check what the message is about'''
        if("LIGHT" in self.message):
            self.lights()
        else:
            self.fans()

    def lights(self):

        if("ON" in self.message):
            '''turn lights on'''
            obj = TTS("Turning lights on!")
            del obj
            print("Here")
            

        elif "OFF" in self.message:
            '''turn lights off'''
            obj = TTS("Turning lights off!")
            del obj
            
        
        

    def fans(self):

        if("ON" in self.message):
            '''turn lights on'''
            TTS("Turning fans on!")


        elif "OFF" in self.message:
            '''turn lights off'''
            TTS("Turning fans off!")
