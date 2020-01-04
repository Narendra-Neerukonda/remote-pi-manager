import configparser
import json
import os


storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


def save_new_data(data, prev_data):
    if data['ok']:
        if data['result']:
            for item in data['result']:
                if item['update_id'] > prev_data['update_id']:
                    storage = open(storage_config['received']['updates'],'a')
                    storage.write(json.dumps(item)+"\n")
                    storage.close()


def load_prev_data(fpath):
    if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
        prev_data = open(fpath, 'r')
        last_line = prev_data.readlines()[-1]
        prev_data.close()
        return last_line
    else:
        return "{\"update_id\":0}"