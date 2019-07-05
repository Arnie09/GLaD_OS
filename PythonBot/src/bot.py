import paho.mqtt.client as mqtt
from iotControl import iotControl
from TTS_engine import TTS
import threading
from playsound import playsound
import os
import sys
from dialogflow_class import DialogFlow

counter = 0
message_main  = ""

def mqttclient():

    def on_connect(client,userdata,flags,rc):
        client.subscribe("GladOs/messages")

    def on_message(client,userdata,mssg):
        global message_main
        if mssg.topic == "GladOs/messages":
            message = str(mssg.payload)[2:-1]
            
            message = message.upper()

            #print(message)
            message_main = message

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com",1883,60)

    client.loop_forever()

mqtt_thred = threading.Thread(target = mqttclient)
mqtt_thred.start()

def play_anthem():

    print("playing a song...")
    play_still_alive = threading.Thread(target = function_that_play_still_alive)
    play_still_alive.start()

def function_that_play_still_alive():

    playsound(os.path.join(sys.path[0],"assets","audio","Portal - Still Alive.mp3"))


while(True):
    if(message_main!= ""):
        print(message_main)
        

        if("TURN" in message_main or "LIGHT" in message_main or "FAN" in message_main):
                    print("HI")
                    iotControl_obj =iotControl(message_main,counter)
                    counter+=1

        elif("PLAY" in message_main and "SONG" in message_main):
            play_anthem()
        elif("PLAY" in message_main and "SONG" not in message_main):
            #playfromYoutube()
            '''add other functions for which basic tasks are done using custom scripts like email'''
            '''Some example commands are - CHECK MY EMAIL - for which some gmail api needs to be integrated'''
            ''' CALCULATE - make a universal calculation bot in python'''
            ''' ADD to playlist -  ability to add songs to playlists'''
            '''play a specific playlist'''
            '''take reminders'''
            '''integrating dialog flow here'''
        else:
            df_obj = DialogFlow(message_main)
            if(df_obj.response):
                TTS(df_obj.response,counter)
                counter+=1  
        message_main = ""         


