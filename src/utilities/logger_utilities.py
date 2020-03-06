"""!
Contains all functionality for the generation and access of loggers
"""

import logging
import sys
import os

def get_logger(name="Main", stdout_stream=True):
    file_handler = logging.FileHandler(filename="logs/"+name+'.log')
    if stdout_stream:
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [file_handler]

    logger = logging.getLogger(name)

    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)

    return logger

def generate_unique_filename(name):
    file_name = "logs/"+name+".txt"
    if os.path.exists(file_name):
        expand = 1
        while True:
            expand += 1
            new_file_name = file_name.split(".txt")[0] + "_" + str(expand) + ".txt"
            if not os.path.exists(new_file_name):
                return new_file_name
    return file_name