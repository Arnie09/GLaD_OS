from TTS_engine import TTS
import os
import sys
import RPi.GPIO as GPIO

class iotControl():

    def __init__(self,message):
        print("Here")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(3,GPIO.OUT)
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
            GPIO.output(3,False)
            print("Here")    

        elif "OFF" in self.message:
            '''turn lights off'''
            obj = TTS("Turning lights off!")
            del obj
            GPIO.output(3,True)
            
    def fans(self):

        if("ON" in self.message):
            '''turn lights on'''
            print("here")
            TTS("Turning fans on!")
            GPIO.output(2,False)

        elif "OFF" in self.message:
            '''turn lights off'''
            TTS("Turning fans off!")
            GPIO.output(2,True)
