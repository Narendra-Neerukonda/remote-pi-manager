import os
import json
import configparser
import time


from workflows.command_executor import execute_command
from workflows.file_downloader import download_file
from workflows.torrent_downloader import start_torrent_data_download


from responder.messaging import sendtext


storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))


timer_config = configparser.ConfigParser()
timer_config.read(os.path.join(os.path.dirname(__file__),"..","conf","timing.ini"))


def parse_and_execute(go = True):

    if not os.path.isfile(storage_config['processed']['objects']):
        create_processed_file = open(storage_config['processed']['objects'], 'w')
        create_processed_file.close()

    while go:
        time.sleep(int(timer_config['polling_delay']['time']))
        with open(storage_config['received']['updates'], 'r') as process_batch, open(storage_config['processed']['objects'], 'r') as processing_complete:
            to_be_processed = [item for item in process_batch if item not in processing_complete]
            for line in to_be_processed:
                loaded_line = json.loads(line)
                if 'message' in loaded_line:

                    # Code block to execute specific shell commands. syntax- command: <actual command>
                    if 'text' in loaded_line['message']:
                        if 'command' in loaded_line['message']['text']:
                            command = loaded_line['message']['text'].split(':')
                            if len(command) > 1:
                                response = execute_command(command[1])
                                sendtext(
                                    "Responding for command "+str(command[1])+"\n"
                                    + str(response)
                                    )
                    # code block to download voice files
                    if 'voice' in loaded_line['message']:
                        response = download_file(loaded_line['message']['voice']['file_id'])
                        sendtext(
                            "Received file"
                        )
                    
                    #code block to download torrents
                    if 'document' in loaded_line['message']:
                        if "start download" in loaded_line['message']['caption']:
                            response = download_file(loaded_line['message']['document']['file_id'])
                            sendtext(
                                "Received file"
                            )
                            torrent_response = start_torrent_data_download(storage_config['received']['downloads']+"/"+response)
                            sendtext(
                                torrent_response
                            )
                with open(storage_config['processed']['objects'],'a+') as processed_objects:
                    processed_objects.write(line)


if __name__=="__main__":
    parse_and_execute()