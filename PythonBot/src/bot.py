import paho.mqtt.client as mqtt
from iotControl import iotControl
from TTS_engine import TTS
import threading
import pygame
import os
import sys
import json
from dialogflow_class import DialogFlow

counter = 0
message_main  = ""
user_id = ""
mqtt_thred_to_get_userid = None

def mqttclient():

    def on_connect(client,userdata,flags,rc):
        
        global user_id
        
        print("subscribing to: GladOs/messages/"+user_id)
        client.subscribe("GladOs/messages/"+user_id)

    def on_message(client,userdata,mssg):
        global message_main
        if  "GladOs/messages" in mssg.topic :
            message = str(mssg.payload)[2:-1]
            
            message = message.upper()

            #print(message)
            message_main = message

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com",1883,60)

    client.loop_forever()

def mqttclient_to_get_userid():

    def execute():
        global mqtt_thred_to_get_userid
        print("onexecute")
        client.disconnect
        mqtt_thred_to_get_userid.exit()
        # with open(os.path.join(sys.path[0],"assets/user_id.json")) as user_id_file__:
        #         data = {"username":userid }
        #         user_id_file__.seek(0)
        #         json.dump(data,user_id_file__)
        #         user_id_file__.truncate()

        
    
    def on_connect(client,userdata,flags,rc):
        
        print("Subscribed to channel user id:")
        client.subscribe("GladOs/userid")

    def on_message(client,userdata,mssg):
        global user_id
        if  "GladOs/userid" in mssg.topic :
            id = str(mssg.payload)[2:-1]

            print(id)
            user_id = id

        execute()

            

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com",1883,60)

    client.loop_forever()


'''this is the beginning of the script'''

with open(os.path.join(sys.path[0],"assets/user_id.json")) as user_id_file:
    data = json.load(user_id_file)
    user_id = data["username"]
    print(user_id)
    if(user_id == ""):
        mqtt_thred_to_get_userid = threading.Thread(target = mqttclient_to_get_userid)
        mqtt_thred_to_get_userid.start()    

print("I am here ")
while(True):
    if(len(user_id)>0):
        with open(os.path.join(sys.path[0],"assets/user_id.json"),'r+') as user_id_file:
            data = {"username":user_id}
            user_id_file.seek(0)
            json.dump(data,user_id_file)
            user_id_file.truncate()
        break
            
print("I am here now")
mqtt_thred = threading.Thread(target = mqttclient)
mqtt_thred.start()

def play_anthem():

    print("playing a song...")
    play_still_alive = threading.Thread(target = function_that_play_still_alive)
    play_still_alive.start()

def function_that_play_still_alive():

    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(sys.path[0],"assets","audio","Portal - Still Alive.mp3"))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.quit()



while(True):

    if(message_main!= ""):
        print(message_main)
        

        if("TURN" in message_main or "LIGHT" in message_main or "FAN" in message_main):
                    print("HI")
                    iotControl_obj =iotControl(message_main,counter)
                    counter+=1
                    del iotControl_obj

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


