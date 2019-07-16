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

counter = 0
message_main  = ""
user_id = ""
mqtt_thred_to_get_userid = None
youtube_instance = Youtube()
SongPlaying = False
SongName = ""

def mqttclient():

    def add_to_playlist():
        print(SongName,youtube_instance.length)
        conn = sqlite3.connect(os.path.join(sys.path[0],"assets/playlist_database.db"))
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS my_playlist(
        songname = number,
        length = number
        )"""
        c.execute(sql)
        print("Here2")
        conn.commit()
        
        sql = "INSERT OR REPLACE INTO my_playlist(songname,length) VALUES(?,?,?)",(SongName,youtube_instance.length)
        c.execute(sql)
        conn.commit()
        conn.close()

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
        # while pygame.mixer.Channel(2).get_busy() == True:
        #     continue
        # pygame.mixer.Channel(2).quit()

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

        print(SongPlaying)
        print(SongName)
        if  "GladOs/messages" in mssg.topic :
            message = str(mssg.payload)[2:-1]
            
            message = message.upper()
            print(message)
            '''here we list all the choices'''

            if("TURN" in message or "LIGHT" in message or "FAN" in message):
                iotControl_subroutine(message)
                    
            elif("PLAY" in message and "SONG" in message):
                play_anthem()

            elif(("PAUSE" in message or "PLAY" in message or "RESUME" in message or "STOP" in message or "QUIT" in message or "EXIT" in message) and SongPlaying == True and "PLAYLIST" not in message):
                print("Sending message to instruction!")
                send_instructions_to_youtube(message)

            elif("PLAY" in message and "SONG" not in message and "LIST" not in message):
                play_songs_from_youtube(message)
            
                '''add other functions for which basic tasks are done using custom scripts like email'''
                '''Some example commands are - CHECK MY EMAIL - for which some gmail api needs to be integrated'''
                ''' CALCULATE - make a universal calculation bot in python'''
                ''' ADD to playlist -  ability to add songs to playlists'''
                '''play a specific playlist'''
                '''take reminders'''
                '''integrating dialog flow here'''
            elif("ADD" in message and "PLAYLIST" in message and SongPlaying == True and SongName is not ""):
                add_to_playlist()

            else:
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
   


