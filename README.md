# GLaD_OS

A handy personal assistant who talks sharp and turns on your lights and fans and plays you music if you feel lonely.
GLaD_OS is actually the AI protagonist of the game [Portal](https://store.steampowered.com/app/400/Portal/). But unlike GLaD_OS in the game, this glados will be help you,willingly or unwillingly that is not assured.

**Working Demo video:** [https://www.youtube.com/watch?v=hbyxTZWnGm4&t=65s](https://www.youtube.com/watch?v=hbyxTZWnGm4&t=65s)

**Platform** : Raspberry Pi(all functions), Linux(no IOT), Windows(no IOT), Windows(IOT with Arduino)

**Android App Link** : [Glados](https://drive.google.com/file/d/1jObCxR3bFt-ClH5SYRpttJHcYlUBgH-j/view?usp=sharing)

## Table of contents

1. [What does Glados do?](#What-does-glados-do)
2. [Getting Started](#Getting-Started)
3. [Prerequisites](#Prerequisites)
4. [Installing](#Installing)
5. [How Glados works](#How-Glados-works)
6. [Creator's-note](#Creator's-note)
7. [Techstack-used](#Techstack-used)
8. [Team](#Team)

### What-does-glados-do

* **Glados controls the main electrical appliances at your home.** 
  (Currently it can work only at your commands but on future updates automated updates and reminders to switch off stuff can be implemented.) If the number of controlled appliances is large, ML algorithms to optimise electric bill can also be implemented easily over the existing model of the application.
* **Glados can play your songs at voice commands**
* **Glados can maintain its own playlist with options to add/remove more songs**
* **Glados can talk to you if you feel lonely.** (Get some friends noob)
* **Glados can fetch you information directly from wikipedia.**
* **If you say** Glados play despacito **,Glados will play despacito.**
* **Glados doesn't kill you although she can be mean at times**

### Getting-Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.
Let's first discuss the hardware side of things:

1. Raspberry Pi 3 (You can also run this bot on any windows or Linux machine but you wont be able to get IOT features i that way)
2. An android smartphone
3. A wifi connection
4. A bluetooth speaker/A wired speaker
5. Lights fans or any other electronic device that you want to enable/disable using this bot.

Now coming to the software:

1. To run the software you will need an installation of Python3.5+ on the raspberry pi or any oother device you want to try this on.
2. The list of python modules that need to be pip installed are all mentioned in the list of modules file. 
3. Bash script/ batch script has been providded to autodownload these files for the respective platforms. Please locate the files under 
   "Scripts to install modules"
4. The android app needs to be downloaded from the link [here](https://www.google.com)
5. **An aditional google account is required to be created to use this product.** Youtube should be active on that account and you need    to create a playlist named **my_playlist** in that account. 

### Installing

##### **On Linux/Rasperry Pi**

The steps to get the software installed on a raspberry pi are as follows:

* Download/Clone this repository and copy the folder Raspberry_pi_Glados_bot 
  The folder can be found in PythonBot/src/. Paste the folder in a location where you would want to store the software.
* Download andd install the application on your mobile phone. Donot open it yet.
* The steps to install the Chromedriver can be found [here](https://github.com/Arnie09/GLaD_OS/blob/master/PythonBot/src/Raspberry_Pi_Glados_client/Chromedriver_Rasp/installation.md) 
* Run the bash script to install all necessary python modules required by the python script. **This step may take a lot of time especially in case of a raspberry pi** But donot worry let the installation finish.
* Next copy paste the boot menu file into the boot folder so that the program auto starts after booting in raspberry pi.
* After making sure that you have a google acccount and a youtube acccount with a playlist called my_playlist,run the file called 
  **bot.py**. Open the android app as well.
  
###### Setup-of-the-app
* Enter unique username at the screen below:
   ![enter unique userid](https://github.com/Arnie09/GLaD_OS/blob/master/images/App1.jpeg)
* Click the connect button
   ![Click the connect button](https://github.com/Arnie09/GLaD_OS/blob/master/images/App4.jpeg)
* Enter the email and password of the google account you created for glados.
   ![Enter email and password](https://github.com/Arnie09/GLaD_OS/blob/master/images/App3.jpeg)
* Wait for glados to log in and set up everything you will receive an audio cue when she is done.
   ![Wait for the setup](https://github.com/Arnie09/GLaD_OS/blob/master/images/App2.jpeg)
* Enjoy!
   ![Enjoy](https://github.com/Arnie09/GLaD_OS/blob/master/images/App5.jpeg)
   
##### **On Linux**

* Download/Clone this repository and copy the folder Linux_Glados_client 
  The folder can be found in PythonBot/src/. Paste the folder in a location where you would want to store the software.
* Download andd install the application on your mobile phone. Donot open it yet.
* The steps to install the Chromedriver can be found [here](https://github.com/Arnie09/GLaD_OS/blob/master/PythonBot/src/Raspberry_Pi_Glados_client/Chromedriver_Rasp/installation.md) 
* Run the bash script to install all necessary python modules required by the python script.
* after making sure that you have a google acccount and a youtube acccount with a playlist called my_playlist,run the file called 
  **bot.py**. Open the android app as well.
* Set up of the app is the same as [this](#Setup-of-the-app)

##### **On Windows**

* Download/Clone this repository and copy the folder Windows_Glados_client 
  The folder can be found in PythonBot/src/. Paste the folder in a location where you would want to store the software.
* Download andd install the application on your mobile phone. Donot open it yet.
* Chromedriver is aldready suplied no need to install it saperately!
* Run the batch script to install all necessary python modules required by the python script.
* after making sure that you have a google acccount and a youtube acccount with a playlist called my_playlist,run the file called 
  **bot.py**. Open the android app as well.
* Set up of the app is the same as [this](#Setup-of-the-app)

##### **On Windows with Arduino**

* Download/Clone this repository and copy the folder Windows_Glados_with_arduino
* Other steps are same as previous windows guide
* Make sure to keep the laptop/PC connected with the arduino via USB cable in order to fecilitate instruction transfer.

### How-Glados-works

A breif overview of working of glados has been depicted in the picture below.
![layout](https://github.com/Arnie09/GLaD_OS/blob/master/images/layout.jpg)

### Creator's-note

* In case of any problems or issues that you may have faced, feel free to contact any of the developers.
* As the app is in development there will be bugs so please raise issues if and when you find them.
* You can add more modules to the app just issue the pull request and we will review the request.

### Techstack-used

* Python3.7
* Paho Mqtt Client
* Native Andoid - Java
* Dialogflow
* Sellenium Web Browser

The python module list has been included.
The software was tested on Raspberry pi 3B+ running raspbian, Linux(Elementry OS), Windows 10.

### Team

This project was created out of curiosity to learn new tech stack by:
* **Arnab Chanda** 
   [LinkedIn](https://www.linkedin.com/in/arnab-chanda-aa671017a/)
   [Github](https://github.com/Arnie09)
* **Sandeep Singh**
   [LinkedIn](https://www.linkedin.com/in/sandeep-singh-850157184/)
   [Github](https://github.com/sandeep1103)
* **Somdutta Roy**
   [LinkedIn](https://www.linkedin.com/in/somdutta-roy-396329178/)
