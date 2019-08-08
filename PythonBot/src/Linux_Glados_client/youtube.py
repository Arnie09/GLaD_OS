from iotControl import iotControl
from TTS_engine import TTS
import threading
from playsound import playsound
import os
import json
import sys
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


class Youtube():

    def __init__(self,email,password):
        self.song = ""
        self.CHROMESTAT=0
        self.VIDEOSTAT=-1
        self.length = 0
        self.browser = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver') #For raspberry pi only!
        #self.browser=webdriver.Chrome(executable_path=os.path.join(sys.path[0],'chromedriver.exe'))
        self.browser.get("https://www.google.com")
        self.browser.find_element_by_css_selector('#gb_70').click()
        self.browser.find_element_by_name('identifier').send_keys(email)
        self.browser.find_element_by_xpath('//*[@id="identifierNext"]/span').click()
        sleep(1)
        while(1):
            try:
                self.browser.find_element_by_name('password').send_keys(password)
                break;
            except:
                continue;
        self.browser.find_element_by_xpath('//*[@id="passwordNext"]/span/span').click()
        sleep(2)

        self.browser.get("https://www.youtube.com")
        self.browser.find_element_by_xpath('//*[@id="guide-icon"]').click()
        sleep(1)
        a=self.browser.find_elements_by_id('endpoint')
        self.browser.get(a[10].get_attribute("href"))
        sleep(2)
        songs = self.browser.find_elements_by_id("video-title")
        
        playlist_songs=[]
        for i in songs:
            playlist_songs.append(i.text)
        self.add_songs_to_json(playlist_songs)


        #self.playsong()
    
    def add_songs_to_json(self,playlist_songs):

        with open(os.path.join(sys.path[0],"assets/my_playlist.json"),'r+') as playliistfile:
            data = {"songs":playlist_songs}
            playliistfile.seek(0)
            json.dump(data,playliistfile)
            playliistfile.truncate()

    def playsong(self,message):
        #obj = TTS("Playing "+self.song)
        if self.VIDEOSTAT!=-1:
            self.browser.get("https://www.google.com")
        self.song = message
        search = self.browser.find_element_by_name('q')
        search.send_keys(self.song+" Youtube")
        search.send_keys(Keys.RETURN)
        self.VIDEOSTAT=1
        try:
            self.browser.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/h3/a/h3").click()
        except:
            self.browser.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/div[1]/a/h3").click()

    def play_playlist(self):
        self.browser.get('https://www.youtube.com/')
        self.browser.find_element_by_xpath('//*[@id="guide-icon"]').click()
        sleep(1)
        a=self.browser.find_elements_by_id('endpoint')
        for i in a:
            print(i.get_attribute("href"))
        self.browser.get(a[10].get_attribute("href"))
        self.browser.find_element_by_xpath('//*[@id="overlays"]/ytd-thumbnail-overlay-side-panel-renderer/yt-formatted-string').click()

        self.VIDEOSTAT = 1

    def instructions(self,msg):

        print(msg,self.VIDEOSTAT)

        if ("PLAY" in msg or "RESUME" in msg) and self.VIDEOSTAT==0:
            self.browser.find_element_by_class_name("ytp-play-button").click()
            self.VIDEOSTAT=1

        elif ("PAUSE" in msg or "STOP" in msg) and self.VIDEOSTAT==1:
            self.browser.find_element_by_class_name("ytp-play-button").click()
            self.VIDEOSTAT=0

        elif("QUIT" in msg or "EXIT" in msg):
            self.browser.get("https://www.google.com")
            return False

        elif("ADD TO PLAYLIST" in msg):

            url = self.browser.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
            print(url)
            with open(os.path.join(sys.path[0],"assets/my_playlist.json"),'r+') as my_playlist_file:
                data = json.load(my_playlist_file)
                if(url not in data["songs"]):

                    self.browser.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-button-renderer[2]/a').click()
                    sleep(2)
                    self.browser.find_element_by_xpath('(//*[@id="checkboxContainer"])[2]').click()
                    self.browser.find_element_by_xpath('//*[@id="close-button"]').click()

                    listofsongs = data["songs"]
                    listofsongs.append(url)
                    my_playlist_file.seek(0)
                    json.dump(data,my_playlist_file)
                    my_playlist_file.truncate()

        elif("REMOVE" in msg and "PLAYLIST" in msg):
            url = self.browser.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
            print(url)
            with open(os.path.join(sys.path[0],"assets/my_playlist.json"),'r+') as my_playlist_file:
                data = json.load(my_playlist_file)
                if url in data["songs"]:

                    self.browser.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-button-renderer[2]/a').click()
                    sleep(2)
                    self.browser.find_element_by_xpath('(//*[@id="checkboxContainer"])[2]').click()
                    self.browser.find_element_by_xpath('//*[@id="close-button"]').click()

                    listofsongs = data["songs"]
                    listofsongs.remove(url)
                    my_playlist_file.seek(0)
                    json.dump(data,my_playlist_file)
                    my_playlist_file.truncate()

        elif("NEXT" in msg):
            next = self.browser.find_element_by_css_selector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button').click()

        return True



