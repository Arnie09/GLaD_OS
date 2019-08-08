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
import hashlib

counter = 0
message_main  = ""
user_id = ""
mqtt_thred_to_get_userid = None
youtube_instance = None
SongPlaying = False
SongName = ""
password = ""
active = True

'''This is the mqtt client that takes the message from user and processes it'''
def mqttclient():

    global user_id
    global youtube_instance
    global password

    def resetAcc(client):
        global active

        with open(os.path.join(sys.path[0],"assets/ussername_pass.json"),'r+') as passfile:
            data = {"email":"","password":""}
            passfile.seek(0)
            json.dump(data,passfile)
            passfile.truncate()
        with open(os.path.join(sys.path[0],"assets/user_id.json"),'r+') as user_id_file:
            data = {"username":""}
            user_id_file.seek(0)
            json.dump(data,user_id_file)
            user_id_file.truncate()

        print("I have reset myself master!")

        #TTS("I have reset myself master!")
        client.disconnect()
        active = False
        sys.exit()

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
        TTS("Playing your playlist...")
        SongPlaying = True
        youtube_instance.play_playlist()

    def iotControl_subroutine(message):

        iotControl_obj =iotControl(message)
        del iotControl_obj

    def play_anthem():

        print("playing a song...")
        TTS("Playing a song")
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

    def setpassword(message,client):
        global youtube_instance
        global password
        global user_id
        print("In set password")

        with open(os.path.join(sys.path[0],"assets/ussername_pass.json"),'r+') as passfile:
            data = json.load(passfile)
            email = data["email"]
            passs = data["password"]
            credentials = message[9:]
            username,password_ = credentials.split(",")
            print(username)
            print(password_)
            if passs == "":
                print("Here")
                hashpass = hashlib.sha256(str.encode(password_)).hexdigest()
                print(hashpass)
                data = {"email":username,"password":hashpass}
                passfile.seek(0)
                json.dump(data,passfile)
                passfile.truncate()
                youtube_instance = Youtube(username,password_)
                password = password_
                client.publish("GladOs/messages/raspberry2phone"+user_id,"Everything OK")
                TTS("I am ready to take your commands master!")
            else:

                if(hashlib.sha256(str.encode(password_)).hexdigest() == passs):
                    print("Here")
                    youtube_instance = Youtube(username,password_)
                    client.publish("GladOs/messages/raspberry2phone"+user_id,"Everything OK")
                    TTS("I am ready to take your commands master!")
                else:
                    client.publish("GladOs/messages/raspberry2phone"+user_id,"Wrong password enter again!")

    def initialinteraction(client):
        if password == "":
            client.publish("GladOs/messages/raspberry2phone"+user_id,"Enter the password")
        else:
            client.publish("GladOs/messages/raspberry2phone"+user_id,"Everything OK")

    def on_message(client,userdata,mssg):
        global youtube_instance
        global SongPlaying
        global SongName

        print("Bot.py SongPlaying status: ",SongPlaying)
        print("Bot.py SongName status: ",SongName)


        if  "GladOs/messages" in mssg.topic :
            message = str(mssg.payload)[2:-1]

            if("Password" in message and youtube_instance == None):
                print("Calling password")
                setpassword(message,client)
            elif("Password" in message):
                client.publish("GladOs/messages/raspberry2phone"+user_id,"Everything OK")

            if(message == "RESET ACCOUNT"):
                print("resetting account")
                resetAcc(client)

            message = message.upper()
            print("Bot.py mqtt client:",message)
            '''here we list all the choices'''

            if("TURN" in message or "LIGHT" in message or "FAN" in message) and "PLAY" not in message:
                print("IOT Call...")
                iotControl_subroutine(message)

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

            elif("CALLING ALPHABASE" in message):
                initialinteraction(client)

            elif ("PLAY " not in message and "PAUSE" not in message and "PASSWORD" not in message):
                print("Time for dialogflow...")
                instantiate_dialogflow(message)


    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com",1883,60)
    

    client.loop_forever()


'''This client is only called if the script cannot find any userid'''
def mqttclient_to_get_userid():

    def on_disconnect(client, userdata,rc=0):
        client.loop_stop()

    def execute(client):
        global mqtt_thred_to_get_userid
        print("onexecute")
        client.disconnect()
        # mqtt_thred_to_get_userid.exit()

    def on_connect(client,userdata,flags,rc):

        print("Subscribed to channel user id")
        client.subscribe("GladOs/userid")

    def on_message(client,userdata,mssg):
        global user_id
        if  "GladOs/userid" in mssg.topic :
            id = str(mssg.payload)[2:-1]

            print("In mqttclient to get userid",id)
            user_id = id
            TTS("New user id received. Welcome,",id)

        execute(client)

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

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
        mqtt_thred_to_get_userid.daemon = True
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
mqtt_thred.daemon = True
mqtt_thred.start()

while(True):
    if active == False:
        print("Exiting main thread")
        sys.exit()