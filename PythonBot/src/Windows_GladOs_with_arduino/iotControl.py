from TTS_engine import TTS
import os
import sys
import serial

class iotControl():

    def __init__(self):
        print("Here")
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(2, GPIO.OUT)
        # GPIO.setup(3,GPIO.OUT)
        try:
            self.ser1=serial.Serial('COM8',9600)
            print("serial connection done")
        except:
            print("Error in serial connetion")

    def determine(self,message):
        '''check what the message is about'''
        if("LIGHT" in message):
            self.lights(message)
        else:
            self.fans(message)

    def lights(self,message):

        if("ON" in message):
            '''turn lights on'''
            #obj = TTS("Turning lights on!")

            self.ser1.write('a'.encode())
            print("lights on")

            # GPIO.output(3,False)
            print("Here")

        elif "OFF" in message:
            '''turn lights off'''
            #obj = TTS("Turning lights off!")
            self.ser1.write('b'.encode())

            # GPIO.output(3,True)

    def fans(self,message):

        if("ON" in message):
            '''turn lights on'''
            #obj = TTS("Turning lights on!")

            self.ser1.write('c'.encode())
            print("lights on")

            # GPIO.output(3,False)
            print("Here")

        elif "OFF" in message:
            '''turn lights off'''
            #obj = TTS("Turning lights off!")
            self.ser1.write('d'.encode())
