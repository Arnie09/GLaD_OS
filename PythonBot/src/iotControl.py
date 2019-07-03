from TTS_engine import TTS

class iotControl():

    def __init__(self,message):
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
            TTS("Turning lights on!")
        elif "OFF" in self.message:
            '''turn lights off'''
            TTS("Turning lights off!")
        
        

    def fans(self):

        if("ON" in self.message):
            '''turn lights on'''
            TTS("Turning fans on!")
        elif "OFF" in self.message:
            '''turn lights off'''
            TTS("Turning fans off!")