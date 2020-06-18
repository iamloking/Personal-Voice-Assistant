#pyttsx3 is a text-to-speech conversion library in Python.
#The pyttsx3 module supports two voices first is female and 
# the second is male which is provided by “sapi5” for windows.
import pyttsx3       #pip install pyttsx3 and see the exp.txt

import datetime
import speech_recognition as sr # pip install SpeechRecognition
import wikipedia as wp  #pip install wikipedia

#“smtplib” creates a Simple Mail Transfer Protocol client session 
# object which is used to send emails to any valid email id on the internet. 
#Different websites use different port numbers.
import smtplib

import webbrowser as wb
from time import sleep
import os
from selenium import webdriver #pip install selenium and chromedriver
from random import randint

#Psutil is a Python cross-platform library used to access system details and process utilities.
import psutil  # pip install psutil
import pyjokes   #pip install pyjokes
import sys

# init function to get an engine instance for the speech synthesis 
engine = pyttsx3.init( )

#TO CHANGE THE VOICE OF THE ASSISTANT
# voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
# engine.setProperty('voice',voice)


def speak(*audio):

    # say method on the engine that passing input text to be spoken 
    engine.say(audio)
    # run and wait method, it processes the voice commands.  
    engine.runAndWait( )

def time():
    Time = datetime.datetime.now().strftime("%I hours %M mins %S seconds")
    speak("the current time is", Time)

def date():
    year = (datetime.datetime.now().year)
    month = (datetime.datetime.now().month)
    date = (datetime.datetime.now().day)
    speak( "the current date is" ,(date,month,year))

def sendemail(content):

    #to create a session, we will be using its instance SMTP to encapsulate an SMTP connection
    server = smtplib.SMTP("smtp.gmail.com",587)

    #To identify yourself to the server, .helo() (SMTP) or .ehlo() (ESMTP) should be called after
    #  creating an .SMTP() object, and again after .starttls(). This function is implicitly called by
    #  .starttls() and .sendmail() if needed, so unless you want to check the SMTP service extensions of the server
    # , it is not necessary to use .helo() or .ehlo() explicitly
    server.ehlo()

    # start TLS for security
    server.starttls()

    server.ehlo()   #can be ommitted, as it is called upon automatically, if needed

    # Authentication 
    server.login("firstperson@gmail.com","password")

    # Using the sendmail() instance, send your message. sendmail() uses three parameters:
    #  sender_email_id, receiver_email_id and message_to_be_sent.
    #  The parameters need to be in the same sequence. 
    server.sendmail("firstperson@gmail.com","secondperson@gmail.com",content)

    # terminating the session 
    server.quit()

def wish():
    hour = datetime.datetime.now().hour
    
    if hour>=6 and hour<12:
        speak("Good Morning Sir.","")
    elif hour>=12 and hour<18:
        speak("Good afternoon Sir.","")
    elif hour>=18 and hour<24:
        speak("Good evening Sir.","")
    else:
        speak("Good Night Sir","")
    
    speak("Jarvis at your service ."," please tell me how can i help you?")
    
def takecom():

    #The primary purpose of a Recognizer instance is,
    #  of course, to recognize speech. 
    # Each instance comes with a variety of settings and 
    # functionality for recognizing speech from an audio source.

    #Each Recognizer instance has seven methods for recognizing speech from an audio source using various APIs.
    #  These are:

    # recognize_bing(): Microsoft Bing Speech
    # recognize_google(): Google Web Speech API   [DEFAULT] , others will require id and password.
    # recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
    # recognize_houndify(): Houndify by SoundHound
    # recognize_ibm(): IBM Speech to Text
    # recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
    # recognize_wit(): Wit.ai

    r = sr.Recognizer()

    #To access your microphone with SpeechRecognizer, you’ll have to install the PyAudio package. 
    #That is "pip install pyaudio".
    #  Now, instead of using an audio file as the source, you will use the default system microphone.
    #  You can access this by creating an instance of the Microphone class
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1

        #To handle ambient noise, you’ll need to use the adjust_for_ambient_noise() method of the Recognizer
        #r.adjust_for_ambient_noise(source)


        #You can capture input from the microphone using the 
        # listen() method of the Recognizer class inside of the with block.
        #  This method takes an audio source as its first argument and records input from the source 
        audio = r.listen(source)
    try:
        print("Recognizing...")

        #recognize_*() methods of the Recognizer class require an audio_data argument.
        query = r.recognize_google(audio ,language = 'en-in')
        print(query)
        
    except Exception as e:
        print(e)
        speak("Unable to recognize..."," Try again")

        query = takecom()
    
    return(query)


def cpu():

    #– This function calculates the current system-wide CPU utilization as a percentage.
    usage = str(psutil.cpu_percent())
    speak("CPU is at",usage,"percent")

    #psutil.sensors_battery() – This function gives battery status information as a named tuple.
    #it has three attributes: percent  battery power left as a percentage.
    #secsleft – an approximate time in seconds before battery is completely discharged.
    #power_plugged – True if the AC power cable is connected, False if it is not connected. 
    battery = psutil.sensors_battery()
    speak("Your battery is at",battery.percent,"percent")

def jokes():
    speak("Here is a funny one for you.",pyjokes.get_joke())

if __name__ == "__main__" :
    wish()
    while True:
        query = takecom().lower()
        if "time" in query:
            time()
        if "date" in query:
            date()
        if "wikipedia" in query:
            speak("Searching","")
            query = query.replace("wikipedia","")
            result = wp.summary(query,sentences = 3)
            print(result)
            speak(result)
        if "offline" in query:
            speak("Jarvis signing off","")
            sys.exit(0)
        if "send" in query and "email" in query:
            speak("Sending email","")
            try:
                speak("What should i say?","")
                
                content = takecom()
                sendemail(content)
                speak("Email has been sent.",'')
            except Exception as e:
                print(e)
                speak('Unable to send email',"")
        if "search" in query and "chrome" in query:
            speak("What should i search?","")
            search = takecom().lower()

            driver = webdriver.Chrome(executable_path ="chromedriver/chromedriver.exe")
            
            driver.get("https:/"+search+".com")
        
        if "logout" in query:
            os.system("shutdown -l")

        if "shutdown" in query:
            os.system("shutdown /s")

        

        if "play" in query and "songs" in query:
            songs_dir = "your_music_folder_path"
            songs = os.listdir(songs_dir)
            song_temp = len(songs)
            shuffle = randint(0,song_temp)

            os.startfile(os.path.join(songs_dir,songs[shuffle]))
        if "paint" in query:
            os.startfile("F:\projects\paintman\\build\exe.win32-3.8\paintman.exe")

        if "code" in query:
            os.startfile(r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe")

        if "text" in query and 'editor' in query:
            os.startfile(r"C:\Windows\System32\notepad.exe")

        if "remember" in query and "that" in query:
            speak("What should i remember?","")
            data = takecom()
            remember = open("data.txt","w")
            remember.write(data)
            remember.close()

        if "remember" in query and "what" in query:
            datafile = open("data.txt","r")
            datacontent = datafile.read()
            datafile.close()
            speak("you told me to remember",datacontent)


        if "cpu" in query or "battery" in query:
            cpu()
        
        if "joke"  in query:
            jokes()
        
            



        else:
            speak("Can i help you in any other way Sir?","")

