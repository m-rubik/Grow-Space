"""!
Contains all functionality for the generation and access of loggers.
"""


import logging
import sys
from src.utilities.file_utilities import generate_unique_filename


def get_logger(name="Main", stdout_stream=True):
    """!
    Function used to get access to a new logger object.
    @param name: Name of the logger.
    @param stdout_stream: Boolean for if all log messages should also print to console.
    """

    # Get a unique log name
    filename = generate_unique_filename(name, 'log')

    # Create file handler with unique log name
    file_handler = logging.FileHandler(filename=filename)

    if stdout_stream:
        # Create stdout stream handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [file_handler]

    # Get a new logger with the unique name
    logger = logging.getLogger(name)

    # Create a log message formatter
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')

    for handler in handlers:
        # Update the handlers with the new message format
        handler.setFormatter(formatter)
        # Add the handler to the logger object
        logger.addHandler(handler)

    # Set the level of the logger
    # NOTE: DEBUG level means ALL levels of log messages will be captured
    logger.setLevel(logging.DEBUG)

    return logger