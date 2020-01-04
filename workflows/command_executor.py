import os

def execute_command(command):
    execution_result = os.popen(command).read()
    return execution_result