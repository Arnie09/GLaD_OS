import paho.mqtt.client as mqtt
from iotControl import iotControl
from TTS_engine import TTS
import threading
from playsound import playsound
import os
import sys
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

CHROMESTAT=0
VIDEOSTAT=-1

browser=webdriver.Chrome(executable_path=r"C:\Users\Sandeep\Desktop\chromedriver.exe")
def playsong(song):
    global VIDEOSTAT
    print("welcome to playsong")
    browser.get("https://www.google.com")
    search = browser.find_element_by_name('q')
    search.send_keys(song+" Youtube")
    search.send_keys(Keys.RETURN)
    VIDEOSTAT=1
    try:
        browser.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/h3/a/h3").click()
    except:
        browser.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/div[1]/a/h3").click()


def execute(msg):
    global VIDEOSTAT
    if(msg.startswith("HEY GLADOS")):
        msg=msg[11:]
        print(msg)
    if(msg.startswith("PLAY") and len(msg)>4):
        song=msg[5:]
        print(song+ "playing")
        playsong(song)
    elif (msg=="PLAY" or msg=="RESUME" ) and VIDEOSTAT==0:
        print("check0")
        browser.find_element_by_class_name("ytp-play-button").click()
        VIDEOSTAT=1
    elif (msg=="PAUSE" or msg=="STOP") and VIDEOSTAT==1:
        print("check1")
        browser.find_element_by_class_name("ytp-play-button").click()
        VIDEOSTAT=0
    elif(msg in ["QUIT","EXIT"]):
        browser.get("https://www.google.com")

def on_connect(client,userdata,flags,rc):
    print("connected")
    client.subscribe("GladOs/messages")

def on_message(client,userdata,mssg):
    if mssg.topic == "GladOs/messages":
        message = str(mssg.payload)[2:-1]
        message=message.upper()
        print("Received "+message)
        execute(message)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com",1883,60)

client.loop_forever()
