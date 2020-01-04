import os
import json
import configparser

from workflows.command_executor import execute_command

storage_config = configparser.ConfigParser()
storage_config.read(os.path.join(os.path.dirname(__file__),"..","conf","storage.ini"))

def parse():
    with open(os.path.join(os.path.dirname(__file__),"..",storage_config['received']['updates']), 'r') as to_be_processed:
        for line in to_be_processed:
            loaded_line = json.loads(line)
            if 'message' in loaded_line:

                # Code block to execute specific shell commands
                if 'text' in loaded_line['message']:
                    if 'command' in loaded_line['message']['text']:
                        command = loaded_line['message']['text'].split(':')
                        if len(command) > 1:
                            execute_command(command[1])



if __name__=="__main__":
    parse()