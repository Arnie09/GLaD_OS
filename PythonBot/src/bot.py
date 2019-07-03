import socket
from iotControl import iotControl
from TTS_engine import TTS
import threading
from playsound import playsound
import os
import sys

class Robot:

    def __init__(self):
        self.listener()

    def listener(self):
        socket_object = socket.socket()          
        port = 12345                
        socket_object.bind(('', port))         
        
        # put the socket into listening mode 
        socket_object.listen(5)      
        print ("socket is listening")            
        
        while True: 
            connection, addr = socket_object.accept()      
            #print (('Got connection from'), addr )
            
            message = str(connection.recv(1024))[1:]
            message = message.upper()

            print(message)

            if("TURN" in message or "LIGHT" in message or "FAN" in message):
                iotControl_obj =iotControl(message)

            elif("PLAY" in message):
                self.play_anthem()
            elif("PLAY" in message and "SONG" not in message):
                self.playfromYoutube()

            connection.close() 

    def play_anthem(self):

        play_still_alive = threading.Thread(target = self.function_that_play_still_alive)
        play_still_alive.start()

    def function_that_play_still_alive(self):

        playsound(os.path.join(sys.path[0],"assets","audio","Portal - Still Alive.mp3"))


Robot()
