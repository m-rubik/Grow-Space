"""!
This is a template class for any sensor input.
Each sensor will be inherit this class, and override/add any methods as required.
Therefore, each sensor is a worker class of this template.

This will run as a seperate process from the main thread.
"""

import os
from multiprocessing import Queue

class Sensor():

    name:str = "Default"
    last_val:int = None
    current_val:int = None
    queue:Queue = None

    def __init__(self, name="default", queue=None):
        self.name = name
        self.queue = queue

    def run(self):
        """!
        This is the main loop for any sensor.
        It will read the value and report it back to the main 
        """

        while True:
            # Step 1: Read & Relay the sensor input.
            # For testing, to simulate asynchronous I/O, we create a random number at random intervals
            import random
            import time
            rand = random.Random()
            time.sleep(rand.random() * 1.5)
            current_time = time.time()
            self.last_val = self.current_val
            self.current_val = rand.random() 
            msg = [self.name, self.current_val]
            self.queue.put(msg)
            
            # Step 2: Log the read value
            if not os.path.exists('logs'):
                os.mkdir('logs')
            with open("logs/"+self.name+".txt","a+") as f:
                f.write(str(current_time)+":"+str(self.current_val)+"\n")

            # (Do other stuff)

    def poll(self):
        """!
        This is a manualy triggered capture & reporting of data.
        """
        # Read sensor value
        # Update current/last val
        # Log val 
        # (Do other stuff)
        # Report to main thread
        pass