import os
import configparser


storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


def start_torrent_data_download(torrent_file):
    
    download_status = os.popen("aria2c -T"+" "+ torrent_file+" "+"--seed-time=0 --file-allocation=none"+" "+"-d"+" "+storage_config['save_files']['torrents']+" "+"--on-download-complete=exit").read()
    return "Download Completed"