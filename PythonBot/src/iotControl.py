from TTS_engine import TTS
import os
import sys

class iotControl():

    def __init__(self,message,counter):
        print("Here")
        self.message = message
        self.counter = counter
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
            obj = TTS("Turning lights on!",self.counter)
            del obj
            print("Here")
            

        elif "OFF" in self.message:
            '''turn lights off'''
            obj = TTS("Turning lights off!",self.counter)
            del obj
            
        
        

    def fans(self):

        if("ON" in self.message):
            '''turn lights on'''
            TTS("Turning fans on!",self.counter)


        elif "OFF" in self.message:
            '''turn lights off'''
            TTS("Turning fans off!",self.counter)
