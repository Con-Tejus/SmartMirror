import socket
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

latitude = None #should only be set if an IP lookup cannot be done
longitude = None #should only be set if an IP lookup cannot be done
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values

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

class Weather():
    def __init__(self, *args, **kwargs):
        #Frame.__init__(self,parent,bg ='black')
        self.temperature = ''
        self.forecast = ''
        self.forecast_imm = ''
        self.CityState = ''
        self.icon = ''
        self.currently = ''
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
            print("current IP is:" + IPAddr)
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
            #print(City+" "+State)
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
            CityState = "%s %s" % (location['city'],location['state'])
        else:
            weather_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (WEATHERKEY,latitude,longitude,weather_lang,weather_unit)
            req = requests.get(weather_url)
            weather_json = json.loads(req.text)
            CityState = ""

        try:
            degree_sign= u'\N{DEGREE SIGN}'
            temperature = "%s%s" % (str(weather_json['currently']['temperature']), degree_sign)
            forecast_imm = weather_json['minutely']['summary']
            icon_id = weather_json['minutely']['icon']
            forecast = weather_json['hourly']['summary']
            temp_high = "%s%s" % (str(weather_json['daily']['data'][0]['temperatureHigh']), degree_sign)
            temp_low = "%s%s" % (str(weather_json['daily']['data'][0]['temperatureLow']), degree_sign)
            print(CityState)
            print("The current temp:" + temperature + "\nThe immediate forcast: " + forecast_imm)
            print("Daily forcast: " + forecast)
            print("The High for today will be: " + temp_high + "\nThe Low for today will be: " + temp_low)

            if icon_id in icon_lookup:
                icon = icon_lookup[icon_id]
            if icon is not None:
                image = Image.open(icon)
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)

                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            return temperature

        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get weather data." % e



if __name__ == '__main__':
    weather = Weather()