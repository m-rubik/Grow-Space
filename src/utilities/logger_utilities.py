"""!
Contains all functionality for the generation and access of loggers
"""

import logging
import sys
import os
from src.utilities.file_utilities import generate_unique_filename

def get_logger(name="Main", stdout_stream=True):
    filename = generate_unique_filename(name, 'log')
    file_handler = logging.FileHandler(filename=filename)
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