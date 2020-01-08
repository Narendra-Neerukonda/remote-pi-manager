import os
import configparser


import requests


auth_config = configparser.ConfigParser()
auth_config.read(os.path.join(os.path.dirname(__file__),"..","conf","auth.ini"))

def sendtext(message):
    print(message)
    response = requests.get("https://api.telegram.org/bot"+auth_config['bot']['token']+"/sendMessage?chat_id="+auth_config['bot']['chat_id']+"&parse_mode=Markdown&text="+message)

    return response.json()


def send_image(image_location):
    
    url = "https://api.telegram.org/bot"+auth_config['bot']['token']+"/sendPhoto"

    up = {'photo':(image_location, open(image_location, 'rb'), "multipart/form-data")}
    data={'chat_id':auth_config['bot']['chat_id']}

    data = requests.post(url,files=up, data=data)
    return data.text