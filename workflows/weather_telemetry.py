# -*- coding: utf-8 -*-

import os
import configparser
import json


import requests


from responder.messaging import send_image, sendtext


auth_config = configparser.ConfigParser()
auth_config.read(os.path.join(os.path.dirname(__file__),"..","conf","auth.ini"))


location_config = configparser.ConfigParser()
location_config.read(os.path.join(os.path.dirname(__file__), "..", "conf", "weather.ini"))


storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


def get_weather_data(city_id, api_key):

    #open weather map

    url = "http://api.openweathermap.org/data/2.5/weather"
    querystring = {"id":city_id,"appid":api_key}

    response = requests.request("GET", url, params=querystring)

    data = json.loads(response.text)

    return data

def get_comfort_level(data):

    #open weather map

    weather = data['weather']

    comfort_level = {}

    for item in weather:
        if "clouds" in item['main'].lower():
            comfort_level['main'] = item['main']
            comfort_level['description'] = item['description']
            comfort_level['cloudiness'] = str(data['clouds']['all'])+"%"

        elif "rain" in item['main'].lower():
            comfort_level['main'] = item['main']
            comfort_level['description'] = item['description']
            comfort_level['Rain intensity'] = str(data['rain']['1h'])+" "+"mm"

        elif "clear" not in item['main'].lower():
             comfort_level = item

    return comfort_level


def get_yrno_weather_data(location):
    try:
        url = "https://www.yr.no/place/"+location_config['yr.no'][location]+"/avansert_meteogram.png"
        
        import urllib.request
        try:
            urllib.request.urlretrieve(url, storage_config['received']['downloads']+"/latest.png")
            return True
        except Exception as e:
            sendtext(str(e))
            return False
    except KeyError:
        return False

def weather_requirement(location="bangalore"):

    #open weather requirement
    if location == "":
        return get_comfort_level(get_weather_data("1277333", auth_config['weather']['api_key']))

    if get_yrno_weather_data(location.lower()):
        send_image(storage_config['received']['downloads']+"/latest.png")
