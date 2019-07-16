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


class Youtube():

    def __init__(self):
        self.song = ""
        self.CHROMESTAT=0
        self.VIDEOSTAT=-1
        self.length = 0
        #self.browser = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver') #For raspberry pi only!
        self.browser=webdriver.Chrome(executable_path=os.path.join(sys.path[0],'chromedriver.exe'))
        #self.playsong()
       

    def playsong(self,message):
        #obj = TTS("Playing "+self.song)
        self.song = message
        self.browser.get("https://www.google.com")
        search = self.browser.find_element_by_name('q')
        search.send_keys(self.song+" Youtube")
        search.send_keys(Keys.RETURN)
        self.VIDEOSTAT=1
        try:
            self.browser.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/h3/a/h3").click()
        except:
            self.browser.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/div[1]/a/h3").click()
        sleep(1.5)
        length_str = self.driver.find_element_by_class_name("ytp-time-duration").text
        print("Length: ",length_str)
        min,sec = map(int,length_str.split(":"))
        time = min*60+sec
        self.length = time

    def instructions(self,msg):
        
        print(msg,self.VIDEOSTAT)
        print("check0")
        if ("PLAY" in msg or "RESUME" in msg) and self.VIDEOSTAT==0:
            
            self.browser.find_element_by_class_name("ytp-play-button").click()
            self.VIDEOSTAT=1
        elif ("PAUSE" in msg or "STOP" in msg) and self.VIDEOSTAT==1:
            print("check1")
            self.browser.find_element_by_class_name("ytp-play-button").click()
            self.VIDEOSTAT=0
        elif("QUIT" in msg or "EXIT" in msg):
            self.browser.get("https://www.google.com")
            return False
        return True
