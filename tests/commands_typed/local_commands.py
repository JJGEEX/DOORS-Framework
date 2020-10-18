import time #for stopwatch
import requests, json #for weather
from fuzzywuzzy import fuzz #for music
from fuzzywuzzy import process #for music
import os #for music
import pwd #for music
import eyed3 #for mp3 metadata pulling
from word2number import w2n #for settting reminder
import signal #for setting a reminder

class Stopwatch:
    
    def __init__(self):
        self.start = 0.0

    def handler(self, task):
        if task == "start":
            self.start = time.time()
            print("started",self.start)
        elif task == "stop":
            print("in stop",self.start)
            if(self.start != 0):
                stop = time.time() - self.start 
                print("stopwatch ran for",stop,"seconds")
                self.start = 0
            else:
                print("stopwatch was never started")
        else:
            print(task,"is not a known task")

def handler(signal, frame): #handler for timer
    print("time is up!!!")

def setReminder(timeStr): #only going to focus on time for now
    temp = ""
    timeSwitch = { #dicionary for scaling the time
            "second": 1,
            "minute": 60,
            "hour": 3600,
            }
    for f in timeStr.split():
        try:
            numTemp = w2n.word_to_num(f)
            temp = temp + str(numTemp) + " "
        except ValueError:
            temp = temp + f + " "
    found = False
    num = 0
    timeFormat = ""
    for f in temp.split():
        if found:
            timeFormat = f
            break
        if f.isnumeric():
            num = int(f)
            found = True
    if(timeFormat[-1] is "s"): #removing trailing s. EX: seconds, minutes
        timeFormat = timeFormat[:-1]
    if timeFormat in timeSwitch:
        print("setting timer for",num,timeFormat)
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(num * timeSwitch[timeFormat])
        #time.sleep(num * timeSwitch[timeFormat] + 1)
    else:
        print(timeFormat,"is not a supported time format")
    return 0

def playSong(songName):
    songs = []
    highDis = 0
    highTitle = ""
    path = "/home/"+pwd.getpwuid(os.getuid()).pw_name+"/Music/" #dir for music for current user
    onlyfiles = [f for f in os.listdir(path) if f.endswith(".mp3")] #only mp3 files pulled
    for i in onlyfiles:
        audFile = eyed3.load(path+i)
        print("artist: ",audFile.tag.artist," album: ",audFile.tag.album," title: ",audFile.tag.title) #check metadata of mp3 file
        dis = fuzz.ratio(songName.lower(), audFile.tag.title.lower())
        if dis > 79: # 80% similarity or more is saved
            songs.append([dis, audFile.tag.title])
            if dis > highDis: #getting the most similar
                highDis = dis
                highTitle = audFile.tag.title
        print("ratio", dis)
    print("songs")
    for j in songs:
        print("comparison: ", j[0], " title:", j[1])
    print("highest", highDis, highTitle)
    return 0

def getWeather():
    #reference https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    api_key = "5985bc671ecc377555ecb761fbc53914"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Denver"
    print("using city,",city_name,"\n")

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404": #404 = city not found
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
      
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
      
        # store the value corresponding 
        # to the "pressure" key of y 
        current_pressure = y["pressure"] 
      
        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidiy = y["humidity"] 
      
        # store the value of "weather" 
        # key in variable z 
        z = x["weather"] 
      
        # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
        weather_description = z[0]["description"] 
      
        # print following values 
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) + 
              "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
              "\n humidity (in percentage) = " +
                        str(current_humidiy) +
              "\n description = " +
                        str(weather_description)) 

    else:
        print(" City Not Found ")
    return 0

def check_command(match, original):
    if(match == "homie set a reminder"):
        data = original.replace(match, "")
        setReminder(data)
    elif(match == "homie play the song"):
        data = original.replace(match, "")
        playSong(data)
    elif(match == "homie what's the weather like"):
        getWeather()
    elif(match == "homie start a stopwatch"):
        original.handler("start")
        return original
    elif(match == "homie stop the stopwatch"):
        original.handler("stop")
        return original
    else:
        print(match, "is not a known command")