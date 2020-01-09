"""!
Code for the Soil Moisture Sensor
"""

from src.utilities.sensor_template import Sensor
from datetime import datetime
import RPi.GPIO as GPIO

class SoilMoistureSensor(Sensor):

    channel: int = None

    def __init__(self, name="default", queue=None, polling_interval=2):
        super().__init__(name, queue, polling_interval)
        self.channel = 16 # TODO: This should maybe be passed in???
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)


    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading.
        # For testing, to simulate asynchronous I/O, we create a random number at random intervals
        import random
        import time
        rand = random.Random()
        current_time = datetime.now()
        self._previous_val = self._current_val

        self._current_val = GPIO.input(self.channel)
        
        ## FOR TESTING
        # self._current_val = round(rand.random()*100,2)

        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the reading
        self.queue.put(self._current_val)
        
        # Step 3: Log the reading
        with open("logs/"+self.name+".txt","a+") as f:
            f.write(str(current_time)+":"+str(self._current_val)+"\n")
