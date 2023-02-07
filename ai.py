from asyncio.windows_events import NULL
from tkinter import W
import datetime
import os
import speech_recognition as sr   # voice recognition library
import random                     # to choose random words from list
import pyttsx3                    # offline Text to Speech
import datetime                   # to get date and time
import webbrowser                 # to open and perform web tasks
import serial                     # for serial communication
import pywhatkit                  # for more web automation
from lecturer_search import check_db, check_lecturer, window, take_jokes
import time
from PIL import Image

try:
    port = serial.Serial("COM5", 9600)
    print("Phycial body, connected.")
except:
    print("Unable to connect to my physical body")

# random words list
hi_words = [ 'hi', 'hello']
bye_words = ['bye', 'goodbye']

# initilize things
listener = sr.Recognizer()                 # initialize speech recognition API
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice
newVoiceRate = 140 
engine.setProperty('rate',newVoiceRate)

# connect with NiNi motor driver board over serial communication
def listen():
    """ listen to what user says"""
    try:
        with sr.Microphone() as source:
            print("Talk>>")
            listener.energy_threshold = 700
            voice = listener.listen(source)                     # listen from microphone
            try:
                listener.recognize_google(voice).lower
            except sr.UnknownValueError:
                print("Could not understand audio")
                listen()
            command = listener.recognize_google(voice)  # use google API
            print('command', command)
            command = command.lower()         
            process(command)                 # call process funtion to take action
    except:
        pass

def process(words):
    """ process what user says and take actions """
    print('your words are', words) # check if it received any command
    word_list = words.split(' ')
    print(word_list)

    if 'play' in word_list:
        """if command for playing things, play from youtube"""
        talk("Okay boss, playing")
        extension = ' '.join(word_list[1:])                   # search without the command word
        port.write(b'u')
        pywhatkit.playonyt(extension)  
        port.write(b'l')          

    elif 'university' in word_list:
        port.write(b'u')
        talk("Okay boss, what do you want to know?")
        port.write(b'l') 
        win = window()

    elif 'search' in word_list:
        """if command for google search"""
        port.write(b'u')
        talk("Okay boss, searching")
        port.write(b'l')
        extension = ' '.join(word_list[1:])
        extension = extension.replace(' ', '+')
        url = "google.com/search?q={}".format(extension)
        os.system('start chrome ' + url)
    
    elif 'joke' in word_list:
        jokes = take_jokes()
        talk(random.choice(jokes))
        #im = Image.open(r"joke.jpeg") 
        #im.show() 
        port.write(b'c')
        im = Image.open(r"joke.jpeg") 
        im.show() 

    elif 'time' in word_list:
        port.write(b'l')
        current_time = datetime.datetime.now().strftime("%H:%M")
        talk(current_time)
        return True
    
    elif 'day' in word_list:
        port.write(b'l')
        current_day = datetime.datetime.now().strftime("%Y-%m-%d")
        talk(current_day)

    elif 'uppercut' in word_list:
        port.write(b'U')

    # now check for matches
    for word in word_list:
        if word in hi_words:
            """ if user says hi/hello greet him accordingly"""
            port.write(b'h')               # send command to wave hand
            talk(random.choice(hi_words))

        elif word in bye_words:
            """ if user says bye etc"""
            port.write(b'h') 
            talk(random.choice(bye_words))
    
    word_list = []

def talk(sentence):
    """ talk / respond to the user """
    engine = pyttsx3.init()                    # init text to speech engine
    voices = engine.getProperty('voices')      #check for voices
    engine.setProperty('voice', voices[2].id)  # female voice
    engine.say(sentence)
    engine.runAndWait()

while True:
    data = port.readline()[:-2] #the last bit gets rid of the new-line chars
    data_str = data.decode()
    if data_str == "on":
        res = listen()
        data_str = ''
        data = b''
