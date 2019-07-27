import paho.mqtt.client as mqtt
from iotControl import iotControl
from TTS_engine import TTS
import threading
import pygame
import sqlite3
import os
import sys
import json
from dialogflow_class import DialogFlow
from youtube import Youtube
import wikipedia

counter = 0
message_main  = ""
user_id = ""
mqtt_thred_to_get_userid = None
youtube_instance = Youtube()
SongPlaying = False
SongName = ""

def mqttclient():

    def wikipedia_search(message):
        global SongPlaying
        global youtube_instance

        summary=wikipedia.summary(message[14:],sentences=1)

        if(SongPlaying == True):
            youtube_instance.instructions("PAUSE")
            TTS(summary)
            youtube_instance.instructions("RESUME")

        else:
            TTS(summary)

    def play_my_playlist():

        global youtube_instance
        global SongPlaying
        print("In play my playlist...")
        SongPlaying = True
        youtube_instance.play_playlist()

    def iotControl_subroutine(message):

        iotControl_obj =iotControl(message)
        del iotControl_obj

    def play_anthem():

        print("playing a song...")
        play_still_alive = threading.Thread(target = function_that_play_still_alive)
        play_still_alive.start()

    def function_that_play_still_alive():

        pygame.mixer.init()
        song = pygame.mixer.Sound(os.path.join(sys.path[0],"assets","audio","Portal - Still Alive.wav"))
        print(type(song))
        pygame.mixer.Channel(2).play(song)

    def send_instructions_to_youtube(message):

        global SongPlaying
        global youtube_instance
        is_song_still_playing  = youtube_instance.instructions(message)
        if(is_song_still_playing == False):
            SongPlaying = False
            SongName = ""


    def play_songs_from_youtube(message):

        global youtube_instance
        global SongPlaying
        global SongName

        SongName = message[4:]
        SongPlaying = True
        youtube_instance.playsong(message[4:])
        print("SongPlaying = ",SongPlaying)

    def on_connect(client,userdata,flags,rc):

        global user_id
        print("subscribing to: GladOs/messages/"+user_id)
        client.subscribe("GladOs/messages/"+user_id)

    def instantiate_dialogflow(message):
        df_obj = DialogFlow(message)
        if(df_obj.response):
            TTS(df_obj.response)

    def on_message(client,userdata,mssg):
        global youtube_instance
        global SongPlaying
        global SongName

        print("Bot.py SongPlaying status: ",SongPlaying)
        print("Bot.py SongName status: ",SongName)


        if  "GladOs/messages" in mssg.topic :
            message = str(mssg.payload)[2:-1]

            message = message.upper()
            print("Bot.py mqtt client:",message)
            '''here we list all the choices'''

            if("TURN" in message or "LIGHT" in message or "FAN" in message) and "PLAY" not in message:
                print("IOT Call...")
                #iotControl_subroutine(message)

            elif("PLAY " in message and "PLAYLIST" in message):
                print("Calling play my playlist")
                play_my_playlist()

            elif("PLAY " in message and "SONG" in message):
                print("Playing anthem....")
                play_anthem()



            elif("PLAY " in message and len(message)>5):
                print("Playsongs from youtube....")
                play_songs_from_youtube(message)

            elif(("PAUSE" in message or ("PLAY" in message and len(message)<5) or "RESUME" in message or "STOP" in message or "QUIT" in message or "EXIT" in message or "NEXT" in message or (("ADD" in message or "REMOVE" in message or "DELETE" in message) and  "PLAYLIST" in message)) and SongPlaying == True):
                print("Sending message to instruction!")
                send_instructions_to_youtube(message)

            elif("TELL ME ABOUT" in message):
                print("Search from wikipedia...")
                wikipedia_search(message)

            elif ("PLAY " not in message and "PAUSE" not in message):
                print("Time for dialogflow...")
                instantiate_dialogflow(message)

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

    def on_connect(client,userdata,flags,rc):

        print("Subscribed to channel user id")
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

'''initially we check whether the user had loggin in before or not'''
'''if he had then we will use that logged in username and proceed'''
'''otherwise the mqtt client listens to the userid channel to receive the username from phone'''
with open(os.path.join(sys.path[0],"assets/user_id.json")) as user_id_file:
    data = json.load(user_id_file)
    user_id = data["username"]
    print(user_id)
    if(user_id == ""):
        mqtt_thred_to_get_userid = threading.Thread(target = mqttclient_to_get_userid)
        mqtt_thred_to_get_userid.start()

'''this loop checks whether the username had been passed or not.'''
'''if new username is passed it is written onto disk'''
while(True):
    if(len(user_id)>0):
        with open(os.path.join(sys.path[0],"assets/user_id.json"),'r+') as user_id_file:
            data = {"username":user_id}
            user_id_file.seek(0)
            json.dump(data,user_id_file)
            user_id_file.truncate()
        break

'''calling the main message thread from here'''
mqtt_thred = threading.Thread(target = mqttclient)
mqtt_thred.start()
