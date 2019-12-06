"""!
This is the base class for any sensor class (sensors classes will inherit this class).

A sensor process will run until signalled to stop by received the string
"STOP" in its queue. Since this process runs indefinitely
until told to stop, it is a worker process.
"""

import time
from abc import ABC, abstractmethod
from multiprocessing import Queue

class Sensor(ABC):
    """!
    This is the class that all sensors inherit.
    @param name: The name of the sensor. Must be unique.
    @param previous_val: The previous value that the sensor read.
    @param current_val: The current value that the sensor just read.
    @param queue: The queue between the main thread and the sensor process.
    @param polling_interval: The time between sensor measurements in seconds.
    """

    name: str = "Default"
    previous_val: int = None
    current_val: int = None
    queue: Queue = None
    polling_interval: int = None

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

    def run(self):
        """!
        This is the main loop for any sensor.
        Based on the polling_interval, it will read data and report it by placing it into the queue.
        """

        while True:
            # Check if it receiving a message from the main thread.
            if not self.queue.empty(): # If there is a message from the main thread...
                msg = self.queue.get()
                if msg == "STOP":
                    print(self.name,"shutting down.")
                    return 0
            self.poll()
            time.sleep(self.polling_interval)

    @abstractmethod
    def poll(self):
        """!
        This method captures & reports sensor data.
        """

        pass
