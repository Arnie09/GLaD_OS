import socket
import paho.mqtt.client as mqtt
from iotControl import iotControl
from TTS_engine import TTS
import threading
from playsound import playsound
import os
import sys
from dialogflow_class import DialogFlow


def on_connect(client,userdata,flags,rc):
    client.subscribe("GladOs/messages")

def on_message(client,userdata,message):
    print(message.topic,"  ",str(message.payload))

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com",1883,60)

client.loop_forever()

# class Robot:

#     def __init__(self):
#         self.listener()

#     def listener(self):

#         socket_object = socket.socket()          
#         port = 12345                
#         socket_object.bind(('', port))         
        
#         # put the socket into listening mode 
#         socket_object.listen(5)      
#         print ("socket is listening")            
        
#         counter = 0
#         while True: 
#             connection, addr = socket_object.accept()      
#             #print (('Got connection from'), addr )
            
#             message = str(connection.recv(1024))[1:]
#             message = message.upper()

#             print(message)

#             if("TURN" in message or "LIGHT" in message or "FAN" in message):
#                 iotControl_obj =iotControl(message,counter)
#                 counter+=1

#             elif("PLAY" in message and "SONG" in message):
#                 self.play_anthem()
#             elif("PLAY" in message and "SONG" not in message):
#                 self.playfromYoutube()
#                 '''add other functions for which basic tasks are done using custom scripts like email'''
#                 '''Some example commands are - CHECK MY EMAIL - for which some gmail api needs to be integrated'''
#                 ''' CALCULATE - make a universal calculation bot in python'''
#                 ''' ADD to playlist -  ability to add songs to playlists'''
#                 '''play a specific playlist'''
#                 '''take reminders'''
#                 '''integrating dialog flow here'''
#             else:
#                 df_obj = DialogFlow(message)
#                 if(df_obj.response):
#                     TTS(df_obj.response,counter)
#                     counter+=1


#             connection.close() 
            

#     def play_anthem(self):

#         play_still_alive = threading.Thread(target = self.function_that_play_still_alive)
#         play_still_alive.start()

#     def function_that_play_still_alive(self):

#         playsound(os.path.join(sys.path[0],"assets","audio","Portal - Still Alive.mp3"))


# Robot()
