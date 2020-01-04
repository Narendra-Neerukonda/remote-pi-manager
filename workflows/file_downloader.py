import os
import json
import configparser


import requests


auth_config = configparser.ConfigParser()
auth_config.read(os.path.join(os.path.dirname(__file__),"..","conf","auth.ini"))

storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


def download_file(file_id):
    file_stat = requests.get("https://api.telegram.org/bot"+auth_config['bot']['token']+"/getFile?file_id=" + file_id)
    file_stat_response = json.loads(file_stat.text)
    if file_stat_response['ok']:
        file_path = file_stat_response['result']['file_path']
        
        data = requests.get("https://api.telegram.org/file/bot"+auth_config['bot']['token']+"/"+file_path)
        with open(storage_config['received']['downloads']+"/"+file_path.split("/")[-1], 'wb') as downloading:
            for chunk in data.iter_content(chunk_size=512*1024):
                if chunk:
                    downloading.write(chunk)
        return file_path.split("/")[-1]
