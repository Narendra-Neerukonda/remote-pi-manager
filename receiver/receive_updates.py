import os
import requests
import json
import time
import configparser


storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


timer_config = configparser.ConfigParser()
timer_config.read(os.path.join(os.path.dirname(__file__),"..","conf","timing.ini"))


token_config = configparser.ConfigParser()
token_config.read(os.path.join(os.path.dirname(__file__),"..","conf","auth.ini"))


def get_updates(token, offset=False):
    if not offset:
        data = requests.get("https://api.telegram.org/bot"+token+"/getUpdates?offset=-1")
    if offset:
        data = requests.get("https://api.telegram.org/bot"+token+"/getUpdates?offset="+str(offset)+'"')
    data = json.loads(data.text)
    return data


def load_prev_data(fpath):
    if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
        prev_data = open(fpath, 'r')
        last_line = prev_data.readlines()[-1]
        prev_data.close()
        return last_line
    else:
        return "{\"update_id\":0}"

prev_data = json.loads(load_prev_data(storage_config['received']['updates']).strip("\n"))


def save_new_data(data):
    if data['ok']:
        if data['result']:
            for item in data['result']:
                print(len(data['result']))
                print(item['update_id'])
                print(prev_data['update_id'])
                if item['update_id'] > prev_data['update_id']:
                    storage = open(storage_config['received']['updates'],'a')
                    storage.write(json.dumps(item)+"\n")
                    storage.close()




while True:  
    time.sleep(int(timer_config['polling_delay']['time']))
    try:
        offset = prev_data['update_id'] if prev_data['update_id'] > 0 else False
        data = get_updates(token_config['bot']['token'], offset)
        print(prev_data['update_id'])
        print(data['result'])
        if prev_data['update_id'] == data['result'][-1]['update_id']:
            pass
        else:
            if not prev_data['update_id'] == 0:
                save_new_data(data)
            if data['ok']:
                if data['result']:
                    prev_data = data['result'][-1]
    except Exception as e:
        print(e)
    


