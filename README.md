# GLaD_OS

A handy personal assistant who talks sharp and turns on your lights and fans and plays you music if you feel lonely.
GLaD_OS is actually the AI protagonist of the game [Portal](https://store.steampowered.com/app/400/Portal/). But unlike GLaD_OS in the game, this glados will be help you,willingly or unwillingly that is not assured.

**Platform** : Raspberry Pi(all functions), Linux(no IOT), Windows(no IOT).

## Table of contents

1. [Getting Started](#Getting-Started)
2. [Prerequisites](#Prerequisites)
3. [Installing](#Installing)
4. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)

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

* Download/Clone this repository and copy the folder Linux_Glados_client or Raspberry_pi_Glados_bot depending on your platform
  The folder can be found in PythonBot/src/. Paste the folder in a location where you would want to store the software.
* Download andd install the application on your mobile phone. Donot open it yet.
* Run the bash script to install all necessary python modules required by the python script. **This step may take a lot of time           especially in case of a raspberry pi** But donot worry let the installation finish.
* Next copy paste the boot menu file into the boot folder so that the program auto starts after booting in araspberry pi.
* after making sure that you have a google acccount and a youtube acccount with a playlist called my_playlist,run the file called 
  **bot.py**. Open the android app as well. 
* Enter unique username at the screen below:
   ![enter unique userid](https://github.com/Arnie09/GLaD_OS/blob/master/images/App1.jpeg)
   
