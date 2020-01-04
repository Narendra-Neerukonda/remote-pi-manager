import os
import requests
import json
import time
import configparser


from storage.storage_assistant import (
    save_new_data,
    load_prev_data
    )


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


def main(go=True):
    prev_data = json.loads(load_prev_data(storage_config['received']['updates']).strip("\n"))
    while go:  
        time.sleep(int(timer_config['polling_delay']['time']))
        try:
            offset = prev_data['update_id'] if prev_data['update_id'] > 0 else False
            data = get_updates(token_config['bot']['token'], offset)
            if prev_data['update_id'] == data['result'][-1]['update_id']:
                pass
            else:
                if not prev_data['update_id'] == 0:
                    save_new_data(data, prev_data)
                if data['ok']:
                    if data['result']:
                        prev_data = data['result'][-1]
        except Exception as e:
            print(e)
 
    while not go: # this block is for testing purpose only
        prev_data = json.loads(load_prev_data(storage_config['received']['updates']).strip("\n"))
        offset = prev_data['update_id'] if prev_data['update_id'] > 0 else False
        data = get_updates(token_config['bot']['token'], offset)
        save_new_data(data, prev_data)
        return True

if __name__=="__main__":
    main()
