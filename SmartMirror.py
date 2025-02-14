import socket
from datetime import datetime , date
import requests
import json
import traceback
import time
import locale
import feedparser
import sys
if sys.version_info[0] == 3:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
else:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter

from PIL import Image, ImageTk
from contextlib import contextmanager

GEOIPKEY = "659815d5fd02d324c19ab5a3cb1a6e0d"
WEATHERKEY = "afc268111c03d7cd3c092df5ca36de77"
NEWSKEY = "aa7d7cc0a33848f4a203ffe607aff75f"

latitude = None #should only be set if an IP lookup cannot be done
longitude = None #should only be set if an IP lookup cannot be done
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
xsmall_text_size = 12
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}
class News(Frame):
    def __init__(self,parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        '''
        HEADLINES:
        ** First Headline
        ** Second Headline
        ** Third Headline
        '''
        self.config(bg = 'black')
        self.HeadLine = 'Headlines:'
        self.Title = ''
        self.Summary = ''
        self.HeadLineLbl = Label(self, text = self.HeadLine,font=('Helvetica', large_text_size), fg="white", bg="black")
        self.HeadLineLbl.pack(side = TOP, anchor = W)
        self.TitleContainer = Frame(self, bg="black")
        self.TitleContainer.pack(side = TOP)
        self.get_headlines()

    
    def get_headlines(self):
        try:
            for widget in self.TitleContainer.winfo_children():
                widget.destroy()

            news_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey="+NEWSKEY
            req = requests.get(news_url)
            news_json = json.loads(req.text)
            
            if(news_json['totalResults'] >= 5):
                for article_index in range(0,6):
                    self.Title = news_json['articles'][article_index]['title']
                    self.Summary = news_json['articles'][article_index]['description']
                    title = Headlines(self.TitleContainer,self.Title,self.Summary)
                    title.pack(side = TOP, anchor  = W)
            else:
                print("Not enough stories posted check back later!")

        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get headlines" % e

        self.after(600000, self.get_headlines)

class Headlines(Frame):
    def __init__(self,parent, event_name = "", description = ""):
        Frame.__init__(self, parent, bg = 'black')
        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)
        
        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)

        self.Description = "    " + description
        self.DescriptionLbl = Label(self, text = self.Description, font = ('Helvetica', xsmall_text_size), fg = "white", bg = "black")
        self.DescriptionLbl.pack(side = TOP, anchor = W)

class Clock(Frame):
    def __init__(self,parent, *args, **kwargs):
        Frame.__init__(self,parent,bg = 'black')
        self.dayofweek = ''
        self.time_clock = ''
        self.time_seconds = ''
        self.date_clock = ''
        self.dayofweekLbl = Label(self,font=('Helvetica', large_text_size), fg="white", bg="black")
        self.dayofweekLbl.pack(side = TOP, anchor = E)
        self.dateLbl = Label(self,font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side = TOP, anchor = E)
        self.seconds = Frame(self,bg = 'black')
        self.seconds.pack(side = RIGHT, anchor = E)
        self.secondsLbl = Label(self.seconds,font=('Helvetica', small_text_size), fg="white", bg="black")
        self.secondsLbl.pack(side = TOP, anchor = E)
        self.timeLbl = Label(self,font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.timeLbl.pack(side = TOP, anchor = E)
        self.tick()

    def tick(self):
        try:
            curr_time = datetime.now().time()
            self.time_clock = curr_time.strftime("%I:%M:")
            self.time_seconds = curr_time.strftime("%S %p")
            self.date_clock = date.today()
            self.date_clock = self.date_clock.strftime("%B,%d,%Y")
            self.dayofweek = weekDays[datetime.today().weekday()]

            self.dayofweekLbl.config(text = self.dayofweek)
            self.timeLbl.config(text = self.time_clock)
            self.secondsLbl.config(text = self.time_seconds)
            self.dateLbl.config(text = self.date_clock)

            self.timeLbl.after(200, self.tick)
            
        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get time." % e

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self,parent,bg ='black')
        self.temperature = ''
        self.tempHigh = ''
        self.tempLow = ''
        self.forecast = ''
        self.forecast_imm = ''
        self.CityState = ''
        self.icon = ''
        self.currently = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.tempHighLbl = Label(self,font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.tempHighLbl.pack(side = TOP, anchor = W)
        self.tempLowLbl = Label(self,font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.tempLowLbl.pack(side = TOP, anchor = W)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.forecast_immLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.forecast_immLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.CityStateLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.CityStateLbl.pack(side=TOP, anchor=W)
        '''
        still need to create frames for each section of the weather section
        will need to include frames for the location,forecast,icon,etc
        '''
        self.getWeather()

    def get_ip(self):
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)

        try:
            IPAddr = ip_json['ip']
            return IPAddr

        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get ip." % e

    def get_location(self):
        IPAddr = self.get_ip()
        location_url = "http://api.ipstack.com/"+IPAddr+"?access_key="+GEOIPKEY
        req = requests.get(location_url)
        location_json = json.loads(req.text)

        try:
            City = location_json['city']
            State = location_json['region_code']
            Lat = location_json['latitude']
            Lon = location_json['longitude']
            location_info = {'city' : City, 'state' : State, 'latitude' : Lat , 'longitude' : Lon}
            return location_info

        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get location." % e

    def getWeather(self):
        if latitude is None and longitude is None:
            #retrieve location data
            location = self.get_location()
            weather_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (WEATHERKEY,location['latitude'],location['longitude'],weather_lang,weather_unit)
            req = requests.get(weather_url)
            weather_json = json.loads(req.text)
            self.CityState = "%s,%s" % (location['city'],location['state'])
        else:
            weather_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (WEATHERKEY,latitude,longitude,weather_lang,weather_unit)
            req = requests.get(weather_url)
            weather_json = json.loads(req.text)

        try:
            degree_sign= u'\N{DEGREE SIGN}'
            self.temperature = "%s%s" % (str(weather_json['currently']['temperature']), degree_sign)
            self.forecast_imm = weather_json['minutely']['summary']
            icon_id = weather_json['minutely']['icon']
            self.forecast = weather_json['hourly']['summary']
            self.tempHigh = "%s%s" % (str(weather_json['daily']['data'][0]['temperatureHigh']), degree_sign)
            self.tempLow = "%s%s" % (str(weather_json['daily']['data'][0]['temperatureLow']), degree_sign)

            if icon_id in icon_lookup:
                self.icon = icon_lookup[icon_id]
            if self.icon is not None:
                image = Image.open(self.icon)
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)

                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            self.forecast_immLbl.config(text = self.forecast_imm)
            self.forecastLbl.config(text = self.forecast)
            self.temperatureLbl.config(text = self.temperature)
            self.tempHighLbl.config(text = "High: "+ self.tempHigh)
            self.tempLowLbl.config(text = "Low: " + self.tempLow)
            self.CityStateLbl.config(text = self.CityState)

        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get weather data." % e



class Window:
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background = 'black')
        self.FullScreen = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.topFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill = BOTH, expand = YES)
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.bottomFrame.pack(side = BOTTOM, fill = BOTH, expand = YES)

        self.weather = Weather(self.topFrame)
        self.weather.pack(side = LEFT, anchor = N, padx = 100, pady = 60)
        
        self.clock = Clock(self.topFrame)
        self.clock.pack(side = RIGHT, anchor = N, padx = 100, pady = 60)

        self.news = News(self.bottomFrame)
        self.news.pack(side = LEFT, anchor = S, padx = 100, pady = 60)

    def toggle_fullscreen(self, event = None):
        self.FullScreen = True
        self.tk.attributes("-fullscreen", self.FullScreen)
        return "break"

    def end_fullscreen(self, event = None):
        self.FullScreen = False
        self.tk.attributes("-fullscreen", self.FullScreen)
        return "break"

if __name__ == '__main__':

    w = Window()
    w.tk.mainloop()