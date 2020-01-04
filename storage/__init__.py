import os
import configparser

storage_dir = configparser.ConfigParser()
storage_dir.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


for directory in storage_dir['datadir']['all'].split(","):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "..", directory)):
        os.mkdir(os.path.join(os.path.dirname(__file__), "..", directory))