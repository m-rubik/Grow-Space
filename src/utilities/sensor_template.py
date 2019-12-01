"""!
This is the template class for any sensor.
Each sensor will be an instance of this class.

This will run as a seperate process from the main thread,
and will run until signalled to stop by received the string
"STOP" in its queue. Since this process runs indefinitely
until told to stop, it is a worker process.
"""

import time
from multiprocessing import Queue

class Sensor():
    """!
    This is the class that all sensors are instances of.
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
            self.read_and_report()
            time.sleep(self.polling_interval)

    def poll(self):
        """!
        This method allows for manualy triggered capture & reporting of sensor data.
        """
        self.read_and_report()

    def read_and_report(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading.
        # For testing, to simulate asynchronous I/O, we create a random number at random intervals
        import random
        rand = random.Random()
        current_time = time.time()
        self.previous_val = self.current_val
        self.current_val = round(rand.random()*100,2)

        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the reading
        self.queue.put(self.current_val)
        
        # Step 3: Log the reading
        with open("logs/"+self.name+".txt","a+") as f:
            f.write(str(current_time)+":"+str(self.current_val)+"\n")
