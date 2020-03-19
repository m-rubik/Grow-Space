"""!
This is the base class for any sensor class (sensors classes will inherit this class).

A sensor process will run until signalled to stop by received the string
"STOP" in its queue. Since this process runs indefinitely
until told to stop, it is a worker process.
"""

import time
from abc import ABC, abstractmethod
from multiprocessing import Queue
from datetime import datetime, timedelta
from src.utilities.logger_utilities import get_logger
from src.utilities.file_utilities import generate_unique_filename
import atexit
import os

class Sensor(ABC):
    """!
    This is the class that all sensors inherit.
    @param name: The name of the sensor. Must be unique.
    @param _previous_val: The previous value that the sensor read.
    @param _current_val: The current value that the sensor just read.
    @param queue: The queue between the main thread and the sensor process.
    @param polling_interval: The time between sensor measurements in seconds.
    @param log_file_name: The unique filename for logging the sensor's readings.
    """

    name: str = "Default"
    _previous_val: int = None
    _current_val: int = None
    queue: Queue = None
    polling_interval: int = None
    log_file_name: str = None

    def __init__(self, name="default", queue=None, polling_interval=2):
        """!
        Standard initialization.
        @param name: The name of the sensor. Must be unique.
        @param queue: The queue between the main thread and the sensor process.
        @param polling_interval: The time between sensor measurements in seconds.
        """

        self.name = name
        self.queue = queue
        self.polling_interval = polling_interval

        # Generate unique log file name
        self.log_file_name = generate_unique_filename(self.name, 'txt')

        # Register shutdown event
        atexit.register(self.shutdown)

    def run(self):
        """!
        This is the main loop for any sensor.
        Based on the polling_interval, it will read data and report it by placing it into the queue.
        """

        current_time = datetime.now()
        next_poll_time = current_time + timedelta(seconds=self.polling_interval)
        while True:
            if datetime.now() > next_poll_time:
                self.poll()
                current_time = datetime.now()
                next_poll_time = current_time + timedelta(seconds=self.polling_interval)
                # print("Next poll scheduled for:", next_poll_time)
            else:
                time.sleep(0.1)  # Quick delay to eliminate run-away memory consumption
                pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def poll(self):
        """!
        This method captures sensor data.
        Since it is an abstract method, it MUST be implemented by all derived classes.
        """
        pass