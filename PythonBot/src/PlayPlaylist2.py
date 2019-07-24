from youtube import Youtube
import threading
import os
import sys
import json
from time import sleep
import paho.mqtt.client as mqtt

youtubeinstance = Youtube()
userid = ""
with open(os.path.join(sys.path[0],"assets/user_id.json"),'r')as user_id_file:
    data = json.load(user_id_file)
    userid = data["username"]

class PlayPlaylist():

    def __init__(self):
        self.STATUS = False
        threadingmqtt = threading.Thread(target = self.mqttclient)
        threadingmqtt.start()
        print(self.STATUS)

    def send_instruction_to_youtube(self,inst):
        global youtubeinstance
        youtubeinstance.instructions(inst)
        

    def mqttclient(self):

        def send_instruction(message):
            
            global youtubeinstance
            is_song_still_playing  = youtubeinstance.instructions(message)
            if(is_song_still_playing == False):
                self.STATUS = False

        def callingsongsthread():
            global youtubeinstance
            with open(os.path.join(sys.path[0],"assets/my_playlist.json"),'r') as playlist_file:
                data = json.load(playlist_file)
                for songs in data:
                    youtubeinstance.playsong(songs)
                    if(youtubeinstance.length == data[songs]):
                        sleep(data[songs])
                    else:
                        sleep(data[songs]+youtubeinstance.length)
                send_instruction("EXIT")
        
        def startcallingsongs(client):
            threading.Thread(target = callingsongsthread).start()
            #client.loop.stop()

        def on_connect(client,userdata,flags,rc):
            global userid
            print("Subscribed to userid from playlist")
            client.subscribe("GladOs/messages/"+userid)
            startcallingsongs(client)

        def on_message(client,userdata,mssg):
            global userid
            print("STATUS = ",self.STATUS)
            if  "GladOs/messages" in mssg.topic  and self.STATUS == True:
                message = str(mssg.payload)[2:-1]
            
                message = message.upper()
                print(message + " in playlist thread receiver")
                if(("PAUSE" in message or "PLAY" in message or "RESUME" in message or "STOP" in message or "QUIT" in message or "EXIT" in message)):
                    send_instruction(message)

            
        client = mqtt.Client()

        client.on_connect = on_connect
        client.on_message = on_message

        self.STATUS = True

        client.connect("broker.hivemq.com",1883,60)
        print("dbahbdhabshdbahjdhjsabdhbahjbdhajhdjahbdhabhbsdhbashbdhasdhabshdb")
        client.loop_forever()
        return
