import os
import json
import configparser

from workflows.command_executor import execute_command
from workflows.file_downloader import download_file

from responder.messaging import sendtext


storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))

def parse():
    with open(os.path.join(os.path.dirname(__file__),"..",storage_config['received']['updates']), 'r') as to_be_processed:
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
                
                if 'document' in loaded_line['message']:
                    if "start download" in loaded_line['message']['caption']:
                        response = download_file(loaded_line['message']['document']['file_id'])
                        sendtext(
                            "Received file"
                        )


if __name__=="__main__":
    parse()