import os
import configparser
import json


import requests


auth_config = configparser.ConfigParser()
auth_config.read(os.path.join(os.path.dirname(__file__),"..","conf","auth.ini"))


def get_weather_data(city_id, api_key):

    url = "http://api.openweathermap.org/data/2.5/weather"
    querystring = {"id":city_id,"appid":api_key}

    response = requests.request("GET", url, params=querystring)

    data = json.loads(response.text)

    return data

def get_comfort_level(data):
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

def weather_requirement():
    return get_comfort_level(get_weather_data("1277333", auth_config['weather']['api_key']))

