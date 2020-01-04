import os
import configparser


import requests


auth_config = configparser.ConfigParser()
auth_config.read(os.path.join(os.path.dirname(__file__),"..","conf","auth.ini"))

def sendtext(message):
    print(message)
    response = requests.get("https://api.telegram.org/bot"+auth_config['bot']['token']+"/sendMessage?chat_id="+auth_config['bot']['chat_id']+"&parse_mode=Markdown&text="+message)

    return response.json()
