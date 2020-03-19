"""!
Code for simulating a Soil Moisture Sensor.
"""

import random
from src.utilities.sensor_template import Sensor
from datetime import datetime

class SoilMoistureSensor(Sensor):
    """!
    Contains the code for the simulation of a soil moisture sensor
    """

    def __init__(self, name="default", queue=None, polling_interval=2):
        super().__init__(name, queue, polling_interval)
        self._previous_val = random.randint(40, 90)
    
    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Generate a reading
        sudden_change = random.randint(0,100) <= 10 # 10% chance of a sudden change
        if sudden_change:
            peak_negative = bool(random.getrandbits(1)) # With the change be +ve or -ve
            if peak_negative:
                delta= random.randint(-40,-20)*self._previous_val/100 # Change by 20-40%
            else:
                delta= random.randint(20,40)*self._previous_val/100
            self._current_val = self._previous_val + delta
            if self._current_val > 100:
                self._current_val = 100
            if self._current_val < 0:
                self._current_val = 0
        else:
            negative_progression = bool(random.getrandbits(1))
            if negative_progression:
                delta= random.randint(-5,0)*self._previous_val/100 # Change by 0-5%
            else:
                delta= random.randint(0,5)*self._previous_val/100
            self._current_val = self._previous_val + delta
            if self._current_val > 100:
                self._current_val = 100
            if self._current_val < 0:
                self._current_val = 0
            self._previous_val = self._current_val

        # Step 2: Relay the reading
        self.queue.put(self._current_val)
        
        # Step 3: Log the reading
        current_time = datetime.now()
        with open(self.log_file_name,"a+") as f:
            f.write(str(current_time)+": "+str(self._current_val)+"\n")

    def shutdown(self):
        """!
        Shutdown event bound to the atexit condition.
        Currently does not have any special functionality.
        """
        print(self.name, "shutting down.")
