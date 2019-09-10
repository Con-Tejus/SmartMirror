import socket
import requests
import json
import traceback
import time
import locale
import feedparser

GEOIPKEY = "659815d5fd02d324c19ab5a3cb1a6e0d"
WEATHERKEY = "afc268111c03d7cd3c092df5ca36de77"

latitude = None
longitude = None
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values

class Weather():
    def __init__(self, *args, **kwargs):
        #Frame.__init__(self,parent,bg ='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
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
            print(City+""+State)
            return location_info

        except Exception as e:
            traceback.print_exc()
            return "Error %s, could not get ip." % e

    def getWeather(self):
        if latitude is None and longitude is None:
            #retrieve location data
            location = self.get_location()
            weather_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (WEATHERKEY,location['latitude'],location['longitude'],weather_lang,weather_unit)
            req = requests.get(weather_url)
            weather_json = json.loads(req.text)
            try:
                temp = weather_json['currently']['temperature']
                summary = weather_json['minutely']['summary']
                print("The current temp:" + str(temp) + " " + summary)
                return temp

            except Exception as e:
                traceback.print_exc()
                return "Error %s, could not get ip." % e



if __name__ == '__main__':
    weather = Weather()